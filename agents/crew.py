from crewai import Agent, Crew, Task
from tools.filesystem import FileSystemTool
from llm.ollama_client import OllamaLLM
from utils.shared_memory import SharedMemory
from llm.llm_factory import get_llm

llm_instance = get_llm()

user_prompt_agent = Agent(
    name="UserPromptAgent",
    llm=llm_instance,
    tools=[FileSystemTool()],
    description="Inicializa la sesión, almacena prompt y paper."
)
paper_reader_agent = Agent(
    name="PaperReaderAgent",
    llm=llm_instance,
    tools=[FileSystemTool()],
    description="Extrae texto y estructura del paper usando LLM."
)
planner_agent = Agent(
    name="PlannerAgent",
    llm=llm_instance,
    tools=[FileSystemTool()],
    description="Define plan de tareas y dependencias."
)
prd_writer_agent = Agent(
    name="PRDWriterAgent",
    llm=llm_instance,
    tools=[FileSystemTool()],
    description="Genera el PRD en Markdown."
)
architecture_agent = Agent(
    name="ArchitectureAgent",
    llm=llm_instance,
    tools=[FileSystemTool()],
    description="Produce arquitectura técnica y diagrama Mermaid."
)
implementer_agent = Agent(
    name="ImplementerAgent",
    llm=llm_instance,
    tools=[FileSystemTool()],
    description="Genera esqueleto backend y frontend."
)
evaluator_agent = Agent(
    name="EvaluatorAgent",
    llm=llm_instance,
    tools=[FileSystemTool()],
    description="Evalúa entregables y produce informe."
)

# Implementación de lógica de tareas
def user_prompt_logic(input_data):
    # Aquí se debe guardar el prompt y el path del paper en un JSON
    import json
    session_path = input_data.get("session_path")
    session_info = {
        "prompt": input_data.get("prompt"),
        "paper_path": input_data.get("paper_path")
    }
    with open(f"{session_path}/intermediate/session_info.json", "w", encoding="utf-8") as f:
        json.dump(session_info, f)
    logger = input_data.get("logger")
    if logger:
        logger.info("Prompt y paper almacenados en session_info.json")
    memory = input_data.get("memory")
    if memory:
        memory.write("prompt", session_info["prompt"])
        memory.write("paper_path", session_info["paper_path"])
    return session_info

def paper_reader_logic(input_data):
    import fitz, json, os, re
    session_path = input_data["session_path"]
    paper_path = input_data.get("paper_path")
    doc = fitz.open(paper_path)
    text = []
    headings = []
    heading_pattern = re.compile(r"^(?:\d+\.)+\s+.+|^[A-Z][A-Z\s\-]{4,}$")

    for page in doc:
        page_text = page.get_text()
        text.append(page_text)
        for line in page_text.splitlines():
            if heading_pattern.match(line.strip()):
                headings.append(line.strip())

    paper_content = {
        "text": "\n".join(text),
        "structure": {
            "headings": headings
        }
    }
    with open(os.path.join(session_path, "intermediate", "paper_content.json"), "w", encoding="utf-8") as f:
        json.dump(paper_content, f, ensure_ascii=False, indent=2)
    logger = input_data.get("logger")
    if logger:
        logger.info(f"Texto y estructura extraídos del paper: {paper_path}")
    memory = input_data.get("memory")
    if memory:
        memory.write("paper_content", paper_content)
    return paper_content

def planner_logic(input_data):
    import json, os
    session_path = input_data["session_path"]
    # Cargar estructura del paper
    with open(os.path.join(session_path, "intermediate", "paper_content.json"), encoding="utf-8") as f:
        paper_content = json.load(f)
    headings = paper_content.get("structure", {}).get("headings", [])
    # Generar plan basado en headings
    plan = {
        "tasks": []
    }
    for h in headings:
        if "introduction" in h.lower():
            plan["tasks"].append("Analizar la introducción para entender el contexto y los objetivos.")
        elif "method" in h.lower():
            plan["tasks"].append("Extraer los métodos propuestos para identificar requerimientos técnicos.")
        elif "experiment" in h.lower() or "evaluation" in h.lower():
            plan["tasks"].append("Revisar experimentos para definir criterios de éxito y métricas.")
        elif "conclusion" in h.lower():
            plan["tasks"].append("Resumir conclusiones para definir entregables y próximos pasos.")
        else:
            plan["tasks"].append(f"Revisar sección: {h}")
    if not plan["tasks"]:
        plan["tasks"] = [
            "Leer paper",
            "Extraer requerimientos",
            "Diseñar arquitectura",
            "Implementar MVP"
        ]
    with open(os.path.join(session_path, "intermediate", "plan.json"), "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    logger = input_data.get("logger")
    if logger:
        logger.info("Plan de desarrollo generado.")
    memory = input_data.get("memory")
    if memory:
        memory.write("plan", plan)
    return plan

def prd_writer_logic(input_data):
    import os, json
    session_path = input_data["session_path"]
    # Cargar contenido y estructura del paper
    with open(os.path.join(session_path, "intermediate", "paper_content.json"), encoding="utf-8") as f:
        paper_content = json.load(f)
    with open(os.path.join(session_path, "intermediate", "plan.json"), encoding="utf-8") as f:
        plan = json.load(f)

    headings = paper_content.get("structure", {}).get("headings", [])
    resumen = paper_content.get("text", "").split("\n")[0:5]
    prd_md = "# Product Requirements Document\n\n"
    prd_md += "## Resumen\n"
    prd_md += "\n".join(resumen) + "\n\n"
    prd_md += "## Estructura del Paper\n"
    for h in headings:
        prd_md += f"- {h}\n"
    prd_md += "\n## Plan de desarrollo\n"
    for t in plan.get("tasks", []):
        prd_md += f"- {t}\n"
    prd_md += "\n## Requerimientos (a completar)\n"
    prd_md += "\n## Referencias (a completar)\n"

    with open(os.path.join(session_path, "output", "prd.md"), "w", encoding="utf-8") as f:
        f.write(prd_md)
    logger = input_data.get("logger")
    if logger:
        logger.info("PRD generado.")
    memory = input_data.get("memory")
    if memory:
        memory.write("prd_md", prd_md)
    return prd_md

def architecture_logic(input_data):
    import os
    session_path = input_data["session_path"]
    prd_path = os.path.join(session_path, "output", "prd.md")
    if os.path.exists(prd_path):
        with open(prd_path, encoding="utf-8") as f:
            prd_content = f.read()
    else:
        prd_content = ""
    # Generar arquitectura y diagrama Mermaid básicos
    architecture_md = "# Arquitectura Técnica\n\n"
    architecture_md += "Basado en el PRD generado, se propone una arquitectura de microservicios simple:\n\n"
    architecture_md += "```mermaid\ngraph TD;\n"
    architecture_md += "Frontend[Frontend Web] --> API[API Backend]\n"
    architecture_md += "API --> DB[(Base de Datos)]\n"
    architecture_md += "```\n\n"
    architecture_md += "## Justificación\n"
    architecture_md += "Esta arquitectura separa la interfaz de usuario del backend y la base de datos, facilitando la escalabilidad y el mantenimiento.\n"
    with open(os.path.join(session_path, "output", "architecture.md"), "w", encoding="utf-8") as f:
        f.write(architecture_md)
    logger = input_data.get("logger")
    if logger:
        logger.info("Arquitectura técnica generada.")
    memory = input_data.get("memory")
    if memory:
        memory.write("architecture_md", architecture_md)
    return architecture_md

def implementer_logic(input_data):
    import os
    session_path = input_data["session_path"]
    implementation_dir = os.path.join(session_path, "output", "implementation")
    os.makedirs(implementation_dir, exist_ok=True)
    # Backend: FastAPI básico
    backend_dir = os.path.join(implementation_dir, "backend")
    os.makedirs(backend_dir, exist_ok=True)
    with open(os.path.join(backend_dir, "main.py"), "w", encoding="utf-8") as f:
        f.write(
            "from fastapi import FastAPI\n\n"
            "app = FastAPI()\n\n"
            "@app.get('/')\n"
            "def read_root():\n"
            "    return {'Hello': 'World'}\n"
        )
    # Frontend: React básico (estructura)
    frontend_dir = os.path.join(implementation_dir, "frontend")
    os.makedirs(frontend_dir, exist_ok=True)
    with open(os.path.join(frontend_dir, "App.jsx"), "w", encoding="utf-8") as f:
        f.write(
            "import React from 'react';\n\n"
            "function App() {\n"
            "  return <h1>Hello World</h1>;\n"
            "}\n\n"
            "export default App;\n"
        )
    with open(os.path.join(frontend_dir, "package.json"), "w", encoding="utf-8") as f:
        f.write(
            '{\n'
            '  "name": "frontend",\n'
            '  "version": "0.1.0",\n'
            '  "private": true,\n'
            '  "dependencies": {\n'
            '    "react": "^18.0.0",\n'
            '    "react-dom": "^18.0.0"\n'
            '  }\n'
            '}\n'
        )
    logger = input_data.get("logger")
    if logger:
        logger.info("Esqueleto de implementación generado.")
    memory = input_data.get("memory")
    if memory:
        memory.write("implementation", "generated")
    return "Implementación generada"

def evaluator_logic(input_data):
    import os
    session_path = input_data["session_path"]
    report_lines = []
    # Evaluar PRD
    prd_path = os.path.join(session_path, "output", "prd.md")
    if os.path.exists(prd_path):
        with open(prd_path, encoding="utf-8") as f:
            prd_content = f.read()
        report_lines.append("✅ PRD generado correctamente.")
        if "# Product Requirements Document" in prd_content:
            report_lines.append("   - El PRD contiene título principal.")
        if "## Estructura del Paper" in prd_content:
            report_lines.append("   - Incluye estructura del paper.")
    else:
        report_lines.append("❌ PRD no encontrado.")

    # Evaluar arquitectura
    arch_path = os.path.join(session_path, "output", "architecture.md")
    if os.path.exists(arch_path):
        with open(arch_path, encoding="utf-8") as f:
            arch_content = f.read()
        report_lines.append("✅ Arquitectura generada correctamente.")
        if "```mermaid" in arch_content:
            report_lines.append("   - Incluye diagrama Mermaid.")
    else:
        report_lines.append("❌ Arquitectura no encontrada.")

    # Evaluar implementación
    backend_main = os.path.join(session_path, "output", "implementation", "backend", "main.py")
    frontend_app = os.path.join(session_path, "output", "implementation", "frontend", "App.jsx")
    if os.path.exists(backend_main):
        report_lines.append("✅ Backend FastAPI generado.")
    else:
        report_lines.append("❌ Backend FastAPI no encontrado.")
    if os.path.exists(frontend_app):
        report_lines.append("✅ Frontend React generado.")
    else:
        report_lines.append("❌ Frontend React no encontrado.")

    # Resumen
    if all("✅" in line for line in report_lines if not line.startswith("   ")):
        report_lines.append("\n🎉 Todos los artefactos principales fueron generados exitosamente.")
    else:
        report_lines.append("\n⚠️ Faltan uno o más artefactos principales.")

    with open(os.path.join(session_path, "output", "evaluation.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))
    logger = input_data.get("logger")
    if logger:
        logger.info("Evaluación de artefactos completada.")
    memory = input_data.get("memory")
    if memory:
        memory.write("evaluation", "completed")
    return "Evaluación completada"

# Definición de tareas CrewAI con lógica conectada
user_prompt_task = Task(
    name="Inicializar sesión",
    agent=user_prompt_agent,
    description="Recibe el prompt y el paper PDF, crea el workspace de la sesión y almacena ambos.",
    output_file="intermediate/session_info.json",
    run=user_prompt_logic
)

paper_reader_task = Task(
    name="Extraer texto y estructura del paper",
    agent=paper_reader_agent,
    description="Extrae el texto y la estructura del paper usando LLM y almacena el resultado.",
    input_files=["intermediate/session_info.json"],
    output_file="intermediate/paper_content.json",
    depends_on=[user_prompt_task],
    run=paper_reader_logic
)

planner_task = Task(
    name="Planificar tareas y dependencias",
    agent=planner_agent,
    description="Define el plan de ejecución y dependencias a partir del prompt y el paper.",
    input_files=["intermediate/paper_content.json"],
    output_file="intermediate/plan.json",
    depends_on=[paper_reader_task],
    run=planner_logic
)

prd_writer_task = Task(
    name="Generar PRD",
    agent=prd_writer_agent,
    description="Genera el PRD en Markdown a partir del plan y el contenido del paper.",
    input_files=["intermediate/plan.json", "intermediate/paper_content.json"],
    output_file="output/prd.md",
    depends_on=[planner_task],
    run=prd_writer_logic
)

architecture_task = Task(
    name="Generar arquitectura técnica",
    agent=architecture_agent,
    description="Produce la arquitectura técnica y el diagrama Mermaid.",
    input_files=["output/prd.md"],
    output_file="output/architecture.md",
    depends_on=[prd_writer_task],
    run=architecture_logic
)

implementer_task = Task(
    name="Generar esqueleto de implementación",
    agent=implementer_agent,
    description="Genera el esqueleto backend y frontend según la arquitectura.",
    input_files=["output/architecture.md"],
    output_dir="output/implementation/",
    depends_on=[architecture_task],
    run=implementer_logic
)

evaluator_task = Task(
    name="Evaluar entregables",
    agent=evaluator_agent,
    description="Evalúa los entregables generados y produce un informe de evaluación.",
    input_files=[
        "output/prd.md",
        "output/architecture.md",
        "output/implementation/"
    ],
    output_file="output/evaluation.txt",
    depends_on=[implementer_task],
    run=evaluator_logic
)

crew = Crew(
    agents=[
        user_prompt_agent,
        paper_reader_agent,
        planner_agent,
        prd_writer_agent,
        architecture_agent,
        implementer_agent,
        evaluator_agent
    ],
    tasks=[
        user_prompt_task,
        paper_reader_task,
        planner_task,
        prd_writer_task,
        architecture_task,
        implementer_task,
        evaluator_task
    ],
    memory=None  # Hook para memoria compartida futura
)

def run(session_path, prompt, paper_path, logger=None):
    import os
    os.makedirs(os.path.join(session_path, "intermediate"), exist_ok=True)
    os.makedirs(os.path.join(session_path, "output", "implementation"), exist_ok=True)

    def log(msg):
        if logger:
            logger.info(msg)
        print(msg)

    memory = SharedMemory(session_path)

    steps = [
        ("🔹 Inicializando sesión...", user_prompt_logic, {"prompt": prompt, "paper_path": paper_path, "session_path": session_path, "logger": logger, "memory": memory}),
        ("🔹 Extrayendo texto y estructura del paper...", paper_reader_logic, {"paper_path": paper_path, "session_path": session_path, "logger": logger, "memory": memory}),
        ("🔹 Generando plan de desarrollo...", planner_logic, {"session_path": session_path, "logger": logger, "memory": memory}),
        ("🔹 Generando PRD...", prd_writer_logic, {"session_path": session_path, "logger": logger, "memory": memory}),
        ("🔹 Generando arquitectura técnica...", architecture_logic, {"session_path": session_path, "logger": logger, "memory": memory}),
        ("🔹 Generando esqueleto de implementación...", implementer_logic, {"session_path": session_path, "logger": logger, "memory": memory}),
        ("🔹 Evaluando entregables...", evaluator_logic, {"session_path": session_path, "logger": logger, "memory": memory}),
    ]

    for msg, func, kwargs in steps:
        log(msg)
        try:
            func(kwargs)
        except Exception as e:
            error_msg = f"❌ Error en el paso '{msg}': {e}"
            log(error_msg)
            if logger:
                logger.error(error_msg)
            raise

    log("✅ Proceso CrewAI finalizado.")

# Sobrescribir el método run del crew para aceptar parámetros
crew.run = run

