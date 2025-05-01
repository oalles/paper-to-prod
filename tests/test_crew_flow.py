import os
import shutil
import tempfile
from agents.crew import crew
from utils.shared_memory import SharedMemory

def test_crew_flow():
    # Crear un workspace temporal
    session_path = tempfile.mkdtemp(prefix="test_session_")
    prompt = "Resume y genera un MVP del siguiente paper."
    # Usar un PDF de ejemplo pequeño y válido
    paper_path = os.path.join(os.path.dirname(__file__), "sample.pdf")
    # Crear un PDF mínimo si no existe
    if not os.path.exists(paper_path):
        from PyPDF2 import PdfWriter
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)
        with open(paper_path, "wb") as f:
            writer.write(f)
    # Ejecutar el flujo CrewAI
    crew.run(session_path=session_path, prompt=prompt, paper_path=paper_path)
    # Validar artefactos principales
    prd_path = os.path.join(session_path, "output", "prd.md")
    arch_path = os.path.join(session_path, "output", "architecture.md")
    backend_main = os.path.join(session_path, "output", "implementation", "backend", "main.py")
    frontend_app = os.path.join(session_path, "output", "implementation", "frontend", "App.jsx")
    eval_path = os.path.join(session_path, "output", "evaluation.txt")
    assert os.path.exists(prd_path)
    assert os.path.exists(arch_path)
    assert os.path.exists(backend_main)
    assert os.path.exists(frontend_app)
    assert os.path.exists(eval_path)
    # Validar estructura del PRD
    with open(prd_path, encoding="utf-8") as f:
        prd_content = f.read()
    assert "# Product Requirements Document" in prd_content
    assert "## Resumen" in prd_content
    assert "## Estructura del Paper" in prd_content
    assert "## Plan de desarrollo" in prd_content
    # Validar estructura de arquitectura
    with open(arch_path, encoding="utf-8") as f:
        arch_content = f.read()
    assert "# Arquitectura Técnica" in arch_content
    assert "```mermaid" in arch_content
    # Validar implementación mínima
    with open(backend_main, encoding="utf-8") as f:
        backend_code = f.read()
    assert "FastAPI" in backend_code
    with open(frontend_app, encoding="utf-8") as f:
        frontend_code = f.read()
    assert "React" in frontend_code or "function App" in frontend_code
    # Validar evaluación
    with open(eval_path, encoding="utf-8") as f:
        eval_content = f.read()
    assert "PRD generado correctamente" in eval_content or "✅ PRD generado correctamente." in eval_content
    # Validar memoria compartida
    memory = SharedMemory(session_path)
    assert memory.get("prompt") == prompt
    assert memory.get("paper_content") is not None
    assert memory.get("plan") is not None
    assert memory.get("prd_md") is not None
    assert memory.get("architecture_md") is not None
    assert memory.get("implementation") == "generated"
    assert memory.get("evaluation") == "completed"
    # Limpiar
    shutil.rmtree(session_path)

if __name__ == "__main__":
    test_crew_flow()
    print("✅ Test de flujo CrewAI completado correctamente.")

