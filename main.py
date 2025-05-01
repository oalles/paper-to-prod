import sys
from pathlib import Path
from agents.user_prompt_agent import UserPromptAgent
from agents.paper_reader_agent import PaperReaderAgent
from agents.planner_agent import PlannerAgent
from agents.prd_writer_agent import PRDWriterAgent
from agents.architecture_agent import ArchitectureAgent
# from agents.implementer_agent import ImplementerAgent # Ignorado por ahora
from agents.evaluator_agent import EvaluatorAgent
from agents.execution_plan_agent import ExecutionPlanAgent
from tools.filesystem_tool import FileSystemTool
from tools.ollama_client import OllamaClient
import logging
from utils.session import create_session_directory
from utils.logging import setup_logger

def setup_logger(log_dir: str, external_hook=None):
    """
    Sets up a logger for the system, writing to a file in the session directory.
    """
    log_file = Path(log_dir) / "system.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("MultiAgentLogger")
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # Add external hook if provided
        if external_hook:
            logger.addHandler(external_hook)

    return logger

def setup_environment(prompt: str, paper_path: str, session_path: str):
    """
    Prepara el entorno usando una carpeta de sesión ya creada.
    """
    print("🚀 Setting up environment...")
    logger = setup_logger(session_path)
    logger.info(f"Session directory created: {session_path}")
    fs_tool = FileSystemTool(session_path)
    ollama_client = OllamaClient()
    logger.info("Environment setup complete.")
    return fs_tool, ollama_client, logger

def orchestrate_agents(prompt: str, paper_path: str, session_path: str, fs_tool: FileSystemTool, llm_client: OllamaClient, logger: logging.Logger):
    """
    Orchestrates the execution of agents in sequence.
    """
    logger.info("\n🤖 Starting agent orchestration...")

    # Step 1: Initialize session with user prompt and paper
    logger.info("\n--- Step 1: User Prompt Agent ---")
    try:
        user_agent = UserPromptAgent(prompt, paper_path, fs_tool)
        user_agent.init_session()
    except Exception as e:
        logger.error(f"❌ Critical Error during User Prompt Agent initialization: {e}", exc_info=True)
        sys.exit(1)

    # Step 2: Read and structure the paper content
    logger.info("\n--- Step 2: Paper Reader Agent ---")
    try:
        reader = PaperReaderAgent(fs_tool, llm_client)
        structured_data = reader.run()
        if not structured_data:
            logger.error("❌ Critical Error: Paper Reader Agent failed to produce structured data. Exiting.")
            sys.exit(1)
        logger.info("   ✅ Paper Reader Agent completed.")
    except Exception as e:
        logger.error(f"❌ Critical Error during Paper Reader Agent execution: {e}", exc_info=True)
        sys.exit(1)

    # Step 3: Plan the workflow
    logger.info("\n--- Step 3: Planner Agent ---")
    try:
        planner = PlannerAgent(fs_tool, llm_client)
        plan = planner.run(structured_data)
        if not plan:
            logger.warning("⚠️ Planner Agent did not produce a detailed plan, continuing with default flow.")
        else:
            logger.info("   ✅ Planner Agent completed.")
    except Exception as e:
        logger.error(f"❌ Error during Planner Agent execution: {e}", exc_info=True)

    # Step 4: Generate Product Requirements Document (PRD)
    logger.info("\n--- Step 4: PRD Writer Agent ---")
    try:
        prd_writer = PRDWriterAgent(fs_tool, llm_client)
        prd_writer.run(structured_data)
        logger.info("   ✅ PRD Writer Agent completed.")
    except Exception as e:
        logger.error(f"❌ Error during PRD Writer Agent execution: {e}", exc_info=True)

    # Step 5: Generate Architecture Document
    logger.info("\n--- Step 5: Architecture Agent ---")
    try:
        arch_agent = ArchitectureAgent(fs_tool, llm_client)
        arch_agent.run(structured_data)
        logger.info("   ✅ Architecture Agent completed.")
    except Exception as e:
        logger.error(f"❌ Error during Architecture Agent execution: {e}", exc_info=True)

    # Step 5.1: Generate Execution Plan
    logger.info("\n--- Step 5.1: Execution Plan Agent ---")
    try:
        exec_plan_agent = ExecutionPlanAgent(fs_tool, llm_client)
        exec_plan_agent.run(structured_data)
        logger.info("   ✅ Execution Plan Agent completed.")
    except Exception as e:
        logger.error(f"❌ Error during Execution Plan Agent execution: {e}", exc_info=True)

    # Step 6: Implementer Agent (Skipped as requested)
    logger.info("\n--- Step 6: Implementer Agent (Skipped) ---")

    # Step 7: Evaluate the generated outputs
    logger.info("\n--- Step 7: Evaluator Agent ---")
    evaluation_report = "Evaluation skipped due to prior errors."
    try:
        evaluator = EvaluatorAgent(fs_tool, llm_client)
        evaluation_report = evaluator.run()
        logger.info("   ✅ Evaluator Agent completed.")
    except Exception as e:
        logger.error(f"❌ Error during Evaluator Agent execution: {e}", exc_info=True)

    logger.info("\n🏁 Agent orchestration finished.")
    return evaluation_report

def validate_input_files(paper_path: str):
    """
    Valida que el archivo de entrada exista, sea un PDF y muestra errores claros.
    """
    from PyPDF2 import PdfReader
    if not Path(paper_path).is_file():
        print(f"❌ El archivo especificado no existe: {paper_path}")
        sys.exit(1)
    try:
        PdfReader(paper_path)
    except Exception as e:
        print(f"❌ El archivo no es un PDF válido o está corrupto: {paper_path}")
        print(f"Detalles: {e}")
        sys.exit(1)

def main(prompt: str, paper_path: str, use_crew: bool = False, external_log_hook=None, session_path: str = None):
    print("Starting MultiAgent Product Synthesizer...")
    try:
        validate_input_files(paper_path)
    except Exception as e:
        print(f"❌ Error validando el archivo de entrada: {e}")
        if 'logger' in locals():
            logger.error(f"Error validando el archivo de entrada: {e}")
        sys.exit(1)

    # Crear la carpeta de sesión solo si no se ha proporcionado
    if session_path is None:
        session_path = create_session_directory()
    print(f"Workspace de sesión: {session_path}")

    logger = setup_logger(session_path, external_hook=external_log_hook)
    logger.info("Sesión iniciada.")
    logger.info(f"Prompt: {prompt}")
    logger.info(f"Paper: {paper_path}")

    try:
        if use_crew:
            # CrewAI siempre disponible, ejecuta directamente
            print("🚀 Ejecutando flujo CrewAI...")
            logger.info("Ejecutando flujo CrewAI.")
            try:
                from crew import crew
                crew.run(session_path=session_path, prompt=prompt, paper_path=paper_path, logger=logger)
            except Exception as e:
                print(f"❌ Error durante la ejecución CrewAI: {e}")
                logger.error(f"Error durante la ejecución CrewAI: {e}")
                sys.exit(1)
            print(f"Flujo CrewAI completado. Revisa la carpeta '{session_path}/output/' para los artefactos generados.")
            logger.info("Flujo CrewAI completado.")
            return

        # Usar la misma carpeta de sesión para todo
        fs_tool, llm_client, logger = setup_environment(prompt, paper_path, session_path)
        logger.info("Main process started.")

        try:
            evaluation_report = orchestrate_agents(prompt, paper_path, session_path, fs_tool, llm_client, logger)

            logger.info("\n\n=========================================")
            logger.info(f"✅ Workflow Complete! Check outputs in: {session_path}")
            logger.info("=========================================")
            if evaluation_report:
                logger.info("\n📊 Evaluation Summary:\n")
                for line in evaluation_report.splitlines():
                    logger.info(line)
                logger.info("=========================================")
            else:
                logger.warning("Evaluation report was not generated.")

        except Exception as e:
            if 'logger' in locals():
                logger.critical(f"🆘 Unhandled exception in main workflow: {e}", exc_info=True)
            else:
                print(f"🆘 Critical Error before logger setup: {e}")
            sys.exit(1)
        finally:
            logger.info("MultiAgent Product Synthesizer finished.")
            print(f"\nOutputs generated in: {session_path}")
    except Exception as e:
        print(f"❌ Error durante la ejecución: {e}")
        if 'logger' in locals():
            logger.error(f"Error durante la ejecución: {e}")
        sys.exit(1)
    finally:
        print("✅ Proceso completado.")

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("\n❌ Usage: python main.py \"<prompt>\" <path_to_paper.pdf> [--use-crew]")
        print("Example: python main.py \"Generate a web app from this paper\" research/mypaper.pdf")
        sys.exit(1)

    user_prompt = sys.argv[1]
    paper_file_path = sys.argv[2]
    use_crew_flag = len(sys.argv) == 4 and sys.argv[3] == "--use-crew"

    main(user_prompt, paper_file_path, use_crew=use_crew_flag)

