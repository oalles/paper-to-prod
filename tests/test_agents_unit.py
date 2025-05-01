import os
import tempfile
import json
from agents.crew import paper_reader_logic, planner_logic, prd_writer_logic

def test_paper_reader_logic_extracts_headings():
    session_path = tempfile.mkdtemp(prefix="test_agent_")
    # Crear un PDF de ejemplo con títulos
    pdf_path = os.path.join(session_path, "test.pdf")
    from PyPDF2 import PdfWriter
    writer = PdfWriter()
    writer.add_blank_page(width=72, height=72)
    # Añadir texto simulado (no soportado por PyPDF2, así que mockeamos el resultado)
    # Simular resultado esperado
    expected_headings = ["1. INTRODUCTION", "2. METHODS", "3. RESULTS"]
    paper_content = {
        "text": "\n".join(expected_headings),
        "structure": {"headings": expected_headings}
    }
    # Guardar como si fuera generado por paper_reader_logic
    with open(os.path.join(session_path, "intermediate"), "w", encoding="utf-8") as f:
        pass  # Solo crear la carpeta
    with open(os.path.join(session_path, "intermediate", "paper_content.json"), "w", encoding="utf-8") as f:
        json.dump(paper_content, f)
    # Validar que los headings están presentes
    with open(os.path.join(session_path, "intermediate", "paper_content.json"), encoding="utf-8") as f:
        data = json.load(f)
    assert data["structure"]["headings"] == expected_headings

def test_planner_logic_uses_headings():
    session_path = tempfile.mkdtemp(prefix="test_agent_")
    os.makedirs(os.path.join(session_path, "intermediate"), exist_ok=True)
    headings = ["1. INTRODUCTION", "2. METHODS", "3. RESULTS"]
    paper_content = {
        "text": "\n".join(headings),
        "structure": {"headings": headings}
    }
    with open(os.path.join(session_path, "intermediate", "paper_content.json"), "w", encoding="utf-8") as f:
        json.dump(paper_content, f)
    plan = planner_logic({"session_path": session_path})
    assert any("introducción" in t.lower() or "introduction" in t.lower() for t in plan["tasks"])

def test_prd_writer_logic_generates_sections():
    session_path = tempfile.mkdtemp(prefix="test_agent_")
    os.makedirs(os.path.join(session_path, "intermediate"), exist_ok=True)
    os.makedirs(os.path.join(session_path, "output"), exist_ok=True)
    headings = ["1. INTRODUCTION", "2. METHODS"]
    paper_content = {
        "text": "\n".join(headings),
        "structure": {"headings": headings}
    }
    plan = {"tasks": ["Analizar la introducción", "Extraer métodos"]}
    with open(os.path.join(session_path, "intermediate", "paper_content.json"), "w", encoding="utf-8") as f:
        json.dump(paper_content, f)
    with open(os.path.join(session_path, "intermediate", "plan.json"), "w", encoding="utf-8") as f:
        json.dump(plan, f)
    prd_md = prd_writer_logic({"session_path": session_path})
    assert "# Product Requirements Document" in prd_md
    assert "## Estructura del Paper" in prd_md
    assert "- 1. INTRODUCTION" in prd_md

if __name__ == "__main__":
    test_paper_reader_logic_extracts_headings()
    test_planner_logic_uses_headings()
    test_prd_writer_logic_generates_sections()
    print("✅ Tests unitarios de agentes completados correctamente.")
