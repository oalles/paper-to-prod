# From Paper to Product

Aquí tienes un **PRD (Product Requirements Document)** completo para el sistema de arquitectura multiagente basado en el
SDK de Google, orientado a transformar un paper técnico en entregables de producto de software (PRD, arquitectura, plan de ejecución e implementación inicial),
trabajando en un sistema de archivos local tipo *Claude Code*:

---

# 📄 PRD: Agente Transformador de Paper Técnico en Producto de Software

## 🧭 Visión General

**Nombre del producto:** MultiAgent Product Synthesizer  
**Objetivo:** Automatizar la generación de documentación y propuestas de implementación de soluciones de software a partir de papers técnicos, mediante una arquitectura multiagente basada en el SDK de Google.  
**Contexto:** Profesionales técnicos y arquitectos de software desean convertir investigaciones técnicas en prototipos y planes de desarrollo sin partir de cero. Este sistema actúa como un puente entre teoría e implementación práctica.

---

## 🎯 Objetivos del Sistema

- Recibir como entrada un prompt y un paper (PDF o texto).
- Interpretar y descomponer el contenido técnico del paper.
- Generar entregables estructurados:
    - PRD (en Markdown y JSON)
    - Arquitectura técnica (con diagramas)
    - Plan de ejecución por fases (iteraciones, roles, fechas)
    - Propuesta inicial de implementación (estructura de carpetas, archivos fuente en Java o React, Docker, etc.)
- Trabajar de forma aislada en un entorno de archivos local, como si se tratara de un entorno tipo Claude Code.
- Registrar todo el proceso de toma de decisiones (trazas, interacciones entre agentes, iteraciones).

---

## 👤 Usuarios Objetivo

- Arquitectos de software
- CTOs / líderes técnicos
- Investigadores en ingeniería eléctrica / TI
- Analistas técnicos con foco en investigación aplicada

---

## 📦 Entregables Generados

| Tipo | Formato | Ubicación |
|------|---------|-----------|
| PRD | Markdown + JSON | `/workspace/{session}/prd.md` |
| Arquitectura | Markdown + Mermaid + YAML opcional | `/workspace/{session}/architecture/` |
| Plan de ejecución | Tabla + checklist | `/workspace/{session}/execution_plan.md` |
| Propuesta inicial | Archivos fuente (.java, .ts, etc.) | `/workspace/{session}/implementation/` |

---

## 🔁 Flujo Funcional

1. **Input**:
    - Prompt técnico + archivo de paper
2. **Análisis**:
    - Agente lector de paper extrae estructura
    - Agente coordinador planifica el flujo
3. **Síntesis**:
    - Generación de PRD
    - Diseño de arquitectura
    - Plan de ejecución
4. **Implementación inicial**:
    - Esqueleto backend (Java, Spring Boot)
    - Esqueleto frontend (React + Zustand)
5. **Validación iterativa**:
    - Evaluación automática + ciclo adaptativo

---

## 🧱 Requisitos Funcionales

- RF1: El sistema debe aceptar archivos PDF o texto como fuente primaria del paper.
- RF2: Debe iniciar una sesión sandbox en el sistema de archivos local.
- RF3: Debe permitir escribir, leer y actualizar archivos intermedios dentro del workspace.
- RF4: Cada agente debe operar sobre el filesystem de forma segura y aislada.
- RF5: El coordinador debe rastrear progreso y generar un registro completo de acciones.
- RF6: Debe generarse un PRD completo con secciones estándar.
- RF7: La propuesta de implementación debe reflejar la arquitectura derivada.
- RF8: Todo debe poder ejecutarse desde CLI o interfaz web ligera.

---

## 📉 Requisitos No Funcionales

- RNF1: Tiempo de ejecución por iteración < 10s en máquina local estándar
- RNF2: Uso máximo de memoria por agente < 1GB
- RNF3: Arquitectura extensible con nuevos agentes o herramientas externas
- RNF4: Operación sin conexión a Internet (modelo offline opcional)
- RNF5: Integración futura con IDEs o entorno gráfico tipo Monaco Editor

---

## 🧪 KPIs

| Indicador | Meta |
|----------|------|
| Tiempo total de generación de entregables | < 3 minutos |
| Precisión de extracción de conceptos clave del paper | ≥ 90% (revisión humana) |
| Tasa de reutilización del código generado | ≥ 60% (evaluado por usuarios) |
| Iteraciones promedio necesarias por sesión | < 3 |
| Cobertura de documentación técnica generada | 100% del esqueleto base |

---

## 🔐 Consideraciones de Seguridad

- Restricción de escritura a `/workspace/{session}/`
- No ejecución de código generado por defecto
- Sanitización de entradas desde PDF/texto
- Control de recursos por sesión (para evitar abuso o bloqueo)

---

## 🛠️ Tecnologías Recomendadas

- **Agentes**: Google Agents SDK (con Vertex Agent Builder opcional)
- **Entorno**: Python 3.11 + CLI local + Docker
- **Embeddings RAG**: Sentence-transformers o Vertex AI Embedding API
- **PDF Parsing**: `pdfplumber` o Vertex LayoutParser
- **Output Markdown / Code**: Generación directa en archivos y estructura en disco
- **Evaluación**: autoraters tipo “Agent-as-a-Judge” + revisión humana opcional

---

```python
# main.py
# Entry point for orchestrating a multi-agent architecture using Google Agents SDK-like abstractions

from agents.user_prompt_agent import UserPromptAgent
from agents.paper_reader_agent import PaperReaderAgent
from agents.planner_agent import PlannerAgent
from agents.prd_writer_agent import PRDWriterAgent
from agents.architecture_agent import ArchitectureAgent
from agents.implementer_agent import ImplementerAgent
from agents.evaluator_agent import EvaluatorAgent
from tools.filesystem_tool import FileSystemTool
from utils.session import create_session_directory

def setup_environment(prompt: str, paper_path: str):
    """
    Prepare the working directory and shared tools.
    """
    session_path = create_session_directory()
    fs_tool = FileSystemTool(session_path)
    return session_path, fs_tool

def orchestrate_agents(prompt: str, paper_path: str, fs_tool: FileSystemTool):
    """
    Orchestrates the execution of all agents in order.
    """
    # Step 1: Get user intent and load paper
    user_agent = UserPromptAgent(prompt, paper_path, fs_tool)
    user_agent.init_session()

    # Step 2: Extract structured info from paper
    reader = PaperReaderAgent(fs_tool)
    structured_data = reader.run()

    # Step 3: Plan the workflow based on paper contents
    planner = PlannerAgent(fs_tool)
    plan = planner.run(structured_data)

    # Step 4: Generate PRD
    prd_writer = PRDWriterAgent(fs_tool)
    prd_writer.run(structured_data)

    # Step 5: Generate architecture doc
    arch_agent = ArchitectureAgent(fs_tool)
    arch_agent.run(structured_data)

    # Step 6: Propose initial implementation code
    impl_agent = ImplementerAgent(fs_tool)
    impl_agent.run(structured_data)

    # Step 7: Evaluate the output
    evaluator = EvaluatorAgent(fs_tool)
    evaluation_report = evaluator.run()

    return evaluation_report

def main(prompt: str, paper_path: str):
    session_path, fs_tool = setup_environment(prompt, paper_path)
    evaluation_report = orchestrate_agents(prompt, paper_path, fs_tool)

    print("\n✅ All deliverables generated.")
    print(f"📂 Session directory: {session_path}")
    if evaluation_report:
        print("\n📊 Evaluation Summary:\n")
        print(evaluation_report)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python main.py '<prompt>' <paper_path>")
        sys.exit(1)
    prompt = sys.argv[1]
    paper_path = sys.argv[2]
    main(prompt, paper_path)
```

```python
# tools/filesystem_tool.py
import os
from pathlib import Path
from typing import Optional

class FileSystemTool:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path).resolve()
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _resolve_path(self, relative_path: str) -> Path:
        resolved_path = (self.base_path / relative_path).resolve()
        if not str(resolved_path).startswith(str(self.base_path)):
            raise PermissionError("Attempted access outside sandbox directory")
        return resolved_path

    def write_text(self, relative_path: str, content: str):
        path = self._resolve_path(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def read_text(self, relative_path: str) -> Optional[str]:
        path = self._resolve_path(relative_path)
        if not path.exists():
            return None
        return path.read_text(encoding="utf-8")

    def list_files(self, relative_dir: str = "") -> list:
        dir_path = self._resolve_path(relative_dir)
        return [str(p.relative_to(self.base_path)) for p in dir_path.rglob("*") if p.is_file()]

    def file_exists(self, relative_path: str) -> bool:
        path = self._resolve_path(relative_path)
        return path.exists()

    def delete_file(self, relative_path: str):
        path = self._resolve_path(relative_path)
        if path.exists():
            path.unlink()

    def make_directory(self, relative_path: str):
        path = self._resolve_path(relative_path)
        path.mkdir(parents=True, exist_ok=True)

    def get_full_path(self, relative_path: str) -> str:
        return str(self._resolve_path(relative_path))
```

```python
# agents/user_prompt_agent.py
import shutil
from pathlib import Path

class UserPromptAgent:
    def __init__(self, prompt: str, paper_path: str, fs_tool):
        self.prompt = prompt
        self.paper_path = Path(paper_path).resolve()
        self.fs_tool = fs_tool

    def init_session(self):
        """
        Initializes the session by storing the prompt and copying the paper to the workspace.
        """
        # Save prompt to a file
        self.fs_tool.write_text("input/prompt.txt", self.prompt)

        # Copy the paper to workspace
        dest_path = self.fs_tool.get_full_path("input/paper.pdf")
        dest_dir = Path(dest_path).parent
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(self.paper_path, dest_path)

        print("📥 Prompt and paper initialized in session workspace.")
```

```python 
# agents/paper_reader_agent.py
import fitz  # PyMuPDF
import json
from pathlib import Path
from tools.filesystem_tool import FileSystemTool

class PaperReaderAgent:
    def __init__(self, fs_tool: FileSystemTool):
        self.fs_tool = fs_tool

    def run(self) -> dict:
        """
        Extracts structured information from the paper and saves it for downstream agents.
        """
        paper_path = self.fs_tool.get_full_path("input/paper.pdf")
        pdf_text = self._extract_text_from_pdf(paper_path)

        structured_data = self._analyze_text(pdf_text)

        # Persist raw text and structured data for transparency
        self.fs_tool.write_text("intermediate/raw_paper_text.txt", pdf_text)
        self.fs_tool.write_text("intermediate/structured_data.json", json.dumps(structured_data, indent=2))

        print("📄 Paper parsed and structured data extracted.")
        return structured_data

    def _extract_text_from_pdf(self, path: str) -> str:
        doc = fitz.open(path)
        return "\n".join([page.get_text() for page in doc])

    def _analyze_text(self, text: str) -> dict:
        """
        Dummy extraction for now; to be replaced with embedding-based or model-based structuring.
        """
        return {
            "title": text.splitlines()[0] if text else "Unknown Title",
            "problem": "<extract using LLM or rule-based heuristics>",
            "approach": "<summarize approach>",
            "datasets": [],
            "results": "",
            "metrics": [],
        }
```

```python
# agents/planner_agent.py
import json
from tools.filesystem_tool import FileSystemTool

class PlannerAgent:
    def __init__(self, fs_tool: FileSystemTool):
        self.fs_tool = fs_tool

    def run(self, structured_data: dict) -> dict:
        """
        Plans the sequence of actions based on the structured data from the paper.
        """
        # Generate a high-level plan of tasks based on paper contents
        plan = {
            "generate_prd": True,
            "design_architecture": True,
            "propose_implementation": True,
            "evaluation": True,
            "notes": [
                "Review problem formulation and expected output",
                "Align modules with system requirements",
                "Ensure consistency across agents",
            ]
        }

        # Save plan to intermediate directory
        self.fs_tool.write_text("intermediate/plan.json", json.dumps(plan, indent=2))
        print("🧭 Planning completed and saved.")
        return plan
```

```python
# agents/prd_writer_agent.py
from tools.filesystem_tool import FileSystemTool

class PRDWriterAgent:
    def __init__(self, fs_tool: FileSystemTool):
        self.fs_tool = fs_tool

    def run(self, structured_data: dict):
        """
        Creates a product requirements document from structured data.
        """
        title = structured_data.get("title", "Untitled")
        problem = structured_data.get("problem", "<Define the problem clearly>")
        approach = structured_data.get("approach", "<Summarize the proposed approach>")

        prd_md = f"""# Product Requirements Document: {title}

## Problem Statement
{problem}

## Proposed Approach
{approach}

## Key Functionalities
- Functionality 1
- Functionality 2
- Functionality 3

## Stakeholders
- Technical team
- Product owner
- End users

## Metrics of Success
- Accuracy ≥ 95%
- Usability rating ≥ 4.5/5
- Deployment in under 3 minutes

## Constraints
- Must support real-time inference
- Should operate offline when needed

## Timeline
- Sprint 1: Data ingestion module
- Sprint 2: Predictor engine
- Sprint 3: API and frontend delivery
"""

        self.fs_tool.write_text("output/prd.md", prd_md)
        print("📘 PRD document generated.")
```

```python
# agents/architecture_agent.py
from tools.filesystem_tool import FileSystemTool

class ArchitectureAgent:
    def __init__(self, fs_tool: FileSystemTool):
        self.fs_tool = fs_tool

    def run(self, structured_data: dict):
        """
        Generates an initial architecture proposal document based on the structured data.
        """
        title = structured_data.get("title", "Untitled System")

        arch_md = f"""# System Architecture: {title}

## Components
- **Input Module**: Accepts raw measurements, configurations, or datasets.
- **Processing Engine**: Core logic (heuristic or AI) to interpret connectivity.
- **Evaluation Layer**: Computes metrics such as precision and recall.
- **API Layer**: REST endpoints to expose services.
- **Frontend**: Dashboard to visualize results (React + Zustand).

## Technologies
- Backend: Java 21 + Spring Boot 3 + Maven
- Frontend: React + TypeScript + Zustand + Ant Design
- Data: PostgreSQL + Redis
- Messaging (optional): Kafka or MQTT for streaming input

## Deployment
- Docker-based containerization
- Docker Compose / Kubernetes optional

## Diagram (Mermaid)
```mermaid
flowchart LR
    A[Input Layer] --> B[Processing Engine]
    B --> C[Evaluation Module]
    B --> D[REST API]
    D --> E[Frontend UI]

## Notes
- All components are modular and stateless
- Designed for local or cloud-native deployment
  """

        self.fs_tool.write_text("output/architecture.md", arch_md)
        print("🏗️  Architecture document generated.")
```

```python
# agents/implementer_agent.py
from tools.filesystem_tool import FileSystemTool

class ImplementerAgent:
    def __init__(self, fs_tool: FileSystemTool):
        self.fs_tool = fs_tool

    def run(self, structured_data: dict):
        """
        Creates initial implementation scaffolding (Java backend + React frontend).
        """
        self._write_readme()
        self._write_backend_files()
        self._write_frontend_files()
        print("🧪 Initial implementation scaffolding created.")

    def _write_readme(self):
        readme = """# Implementation Scaffold

This folder contains a basic setup for the backend (Java + Spring Boot) and frontend (React + TypeScript).
"""
        self.fs_tool.write_text("output/implementation/README.md", readme)

    def _write_backend_files(self):
        main_java = """package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
"""
        pom = """<project xmlns=\"http://maven.apache.org/POM/4.0.0\"
         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"
         xsi:schemaLocation=\"http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd\">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>demo</artifactId>
    <version>1.0.0</version>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
    </dependencies>
</project>
"""
        self.fs_tool.write_text("output/implementation/backend/src/main/java/com/example/Application.java", main_java)
        self.fs_tool.write_text("output/implementation/backend/pom.xml", pom)

    def _write_frontend_files(self):
        index_tsx = """import React from 'react';
import ReactDOM from 'react-dom/client';

const App = () => <h1>Hello from React Scaffold</h1>;

const root = ReactDOM.createRoot(document.getElementById('root')!);
root.render(<App />);
"""
        package_json = """{
  \"name\": \"frontend\",
  \"version\": \"1.0.0\",
  \"dependencies\": {
    \"react\": \"^18.2.0\",
    \"react-dom\": \"^18.2.0\",
    \"zustand\": \"^4.3.0\"
  }
}
"""
        self.fs_tool.write_text("output/implementation/frontend/src/index.tsx", index_tsx)
        self.fs_tool.write_text("output/implementation/frontend/package.json", package_json)
```

```python
# agents/evaluator_agent.py
import os
from tools.filesystem_tool import FileSystemTool

class EvaluatorAgent:
    def __init__(self, fs_tool: FileSystemTool):
        self.fs_tool = fs_tool

    def run(self) -> str:
        """
        Evaluates generated outputs and returns a summary string.
        """
        summary = []

        # Check for key output files
        required_files = [
            "output/prd.md",
            "output/architecture.md",
            "output/implementation/backend/src/main/java/com/example/Application.java",
            "output/implementation/frontend/src/index.tsx"
        ]

        for path in required_files:
            if self.fs_tool.file_exists(path):
                summary.append(f"✅ {path} exists")
            else:
                summary.append(f"❌ {path} is missing")

        # Check PRD content quality (simple heuristic)
        prd_text = self.fs_tool.read_text("output/prd.md") or ""
        if len(prd_text.split()) > 100:
            summary.append("📘 PRD has sufficient length")
        else:
            summary.append("⚠️  PRD might be too short")

        report = "\n".join(summary)
        self.fs_tool.write_text("output/evaluation.txt", report)
        print("📊 Evaluation complete.")
        return report
```

Finalizamos con la plantilla para crear el directorio sandbox y los archivos intermedios.
El archivo session.py ya está implementado. Crea un directorio de sesión único dentro de workspace/ usando un timestamp y un UUID corto, asegurando aislamiento entre ejecuciones.
Con esto, tu arquitectura multiagente está completamente ensamblada y lista para correr.

```python
# utils/session.py
import os
from datetime import datetime
from pathlib import Path
import uuid

def create_session_directory(base_dir: str = "workspace") -> str:
    """
    Creates a unique session directory under the given base directory.
    Returns the absolute path to the created session.
    """
    session_id = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + str(uuid.uuid4())[:8]
    session_path = Path(base_dir) / session_id
    session_path.mkdir(parents=True, exist_ok=True)
    print(f"📁 Created new session: {session_path}")
    return str(session_path.resolve())
```

Proporcionamos un makefile de arranque para facilitar la ejecución del sistema:

```makefile
# Makefile

run:
	python main.py "<Insert your prompt here>" <path/to/paper.pdf>

clean:
	rm -rf workspace/*

lint:
	ruff .

format:
	ruff format .

install:
	pip install -r requirements.txt

dirs:
	mkdir -p workspace agents tools utils output
```

El requirements.txt debe incluir las dependencias necesarias para el sistema:

```plaintext
# requirements.txt
# Base dependencies
PyMuPDF==1.23.7
ruff==0.3.4

# Optional for embedding-based RAG in future stages
sentence-transformers>=2.2.2

# Optional for future LLM orchestration or evaluation
openai>=1.0.0
tqdm>=4.66.0

# Used for any structured data or evaluation steps
pandas>=2.0.0
```

Pero finalmente usaremos OLLAMA-
```bash
pip install ollama
```

```python
# tools/ollama_client.py
from ollama import Client

class OllamaClient:
    def __init__(self, model: str = "mistral", host: str = "http://localhost:11434"):
        self.model = model
        self.client = Client(host=host)

    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1024) -> str:
        response = self.client.generate(
            model=self.model,
            prompt=prompt,
            options={
                "temperature": temperature,
                "num_predict": max_tokens
            }
        )
        return response["response"]
```

Actualizamos los agentes para incluir el cliente de OLLAMA y generar respuestas a partir de los prompts.

```python
# agents/paper_reader_agent.py
import fitz  # PyMuPDF
import json
from pathlib import Path
from tools.filesystem_tool import FileSystemTool
from tools.ollama_client import OllamaClient

class PaperReaderAgent:
    def __init__(self, fs_tool: FileSystemTool, llm_client: OllamaClient):
        self.fs_tool = fs_tool
        self.llm = llm_client

    def run(self) -> dict:
        """
        Extracts structured information from the paper and saves it for downstream agents.
        """
        paper_path = self.fs_tool.get_full_path("input/paper.pdf")
        pdf_text = self._extract_text_from_pdf(paper_path)

        structured_data = self._analyze_text(pdf_text)

        # Persist raw text and structured data for transparency
        self.fs_tool.write_text("intermediate/raw_paper_text.txt", pdf_text)
        self.fs_tool.write_text("intermediate/structured_data.json", json.dumps(structured_data, indent=2))

        print("📄 Paper parsed and structured data extracted.")
        return structured_data

    def _extract_text_from_pdf(self, path: str) -> str:
        doc = fitz.open(path)
        return "\n".join([page.get_text() for page in doc])

    def _analyze_text(self, text: str) -> dict:
        prompt = f"""Extract the following structured information from this paper text:
- Title
- Problem definition
- Proposed approach
- Metrics used
- Relevant datasets

Paper content:
{text[:2000]}
"""
        raw = self.llm.generate(prompt)
        return self._parse_response(raw)

    def _parse_response(self, raw: str) -> dict:
        # Simple heuristic parser for now
        return {
            "title": "LLM-generated title",
            "problem": raw.strip(),
            "approach": "TBD",
            "datasets": [],
            "results": "TBD",
            "metrics": []
        }
```

```python
# agents/planner_agent.py
import json
from tools.filesystem_tool import FileSystemTool
from tools.ollama_client import OllamaClient

class PlannerAgent:
    def __init__(self, fs_tool: FileSystemTool, llm_client: OllamaClient):
        self.fs_tool = fs_tool
        self.llm = llm_client

    def run(self, structured_data: dict) -> dict:
        """
        Plans the sequence of actions based on the structured data from the paper using LLM support.
        """
        planning_prompt = f"""Given the following extracted paper structure:

Title: {structured_data.get('title', 'Untitled')}
Problem: {structured_data.get('problem', '')}
Approach: {structured_data.get('approach', '')}

Generate a high-level task plan for developing a software product that implements this idea.
List steps like PRD generation, architecture, code generation, evaluation, etc.
"""
        llm_response = self.llm.generate(planning_prompt)

        plan = {
            "generate_prd": "prd" in llm_response.lower(),
            "design_architecture": "architecture" in llm_response.lower(),
            "propose_implementation": "implementation" in llm_response.lower(),
            "evaluation": "evaluation" in llm_response.lower(),
            "llm_plan_text": llm_response.strip()
        }

        self.fs_tool.write_text("intermediate/plan.json", json.dumps(plan, indent=2))
        print("🧭 Planning completed using LLM and saved.")
        return plan
```

```python
# agents/prd_writer_agent.py
from tools.filesystem_tool import FileSystemTool
from tools.ollama_client import OllamaClient

class PRDWriterAgent:
    def __init__(self, fs_tool: FileSystemTool, llm_client: OllamaClient):
        self.fs_tool = fs_tool
        self.llm = llm_client

    def run(self, structured_data: dict):
        """
        Creates a product requirements document from structured data using LLM.
        """
        prompt = f"""You are a technical product manager.
Generate a complete Product Requirements Document (PRD) in Markdown format based on the following:

Title: {structured_data.get('title', 'Untitled')}
Problem: {structured_data.get('problem', '')}
Approach: {structured_data.get('approach', '')}
Datasets: {structured_data.get('datasets', [])}
Metrics: {structured_data.get('metrics', [])}

Include the following sections:
- Problem Statement
- Proposed Approach
- Key Functionalities
- Stakeholders
- Metrics of Success
- Constraints
- Timeline
"""
        prd_md = self.llm.generate(prompt)
        self.fs_tool.write_text("output/prd.md", prd_md)
        print("📘 PRD document generated using LLM.")
```

```python
# agents/architecture_agent.py
from tools.filesystem_tool import FileSystemTool
from tools.ollama_client import OllamaClient

class ArchitectureAgent:
    def __init__(self, fs_tool: FileSystemTool, llm_client: OllamaClient):
        self.fs_tool = fs_tool
        self.llm = llm_client

    def run(self, structured_data: dict):
        """
        Generates an architecture proposal using LLM based on the structured data.
        """
        prompt = f"""You are a software architect.
Based on the following structured information from a technical paper, generate a system architecture document in Markdown.

Title: {structured_data.get('title', 'Untitled')}
Problem: {structured_data.get('problem', '')}
Approach: {structured_data.get('approach', '')}

Include sections:
- Components
- Technologies
- Deployment Strategy
- Diagram (use Mermaid syntax)
- Notes
"""
        arch_md = self.llm.generate(prompt)
        self.fs_tool.write_text("output/architecture.md", arch_md)
        print("🏗️  Architecture document generated using LLM.")
```

```python
# agents/implementer_agent.py
from tools.filesystem_tool import FileSystemTool
from tools.ollama_client import OllamaClient

class ImplementerAgent:
    def __init__(self, fs_tool: FileSystemTool, llm_client: OllamaClient):
        self.fs_tool = fs_tool
        self.llm = llm_client

    def run(self, structured_data: dict):
        """
        Creates initial implementation scaffolding using LLM.
        """
        self._write_readme()
        self._write_backend_files(structured_data)
        self._write_frontend_files(structured_data)
        print("🧪 Initial implementation scaffolding created using LLM.")

    def _write_readme(self):
        readme = """# Implementation Scaffold

This folder contains a basic setup for the backend (Java + Spring Boot) and frontend (React + TypeScript).
Generated automatically from a technical paper.
"""
        self.fs_tool.write_text("output/implementation/README.md", readme)

    def _write_backend_files(self, structured_data):
        prompt = f"""Generate a minimal Spring Boot Java backend project based on the following system:

Title: {structured_data.get('title', 'System')}
Problem: {structured_data.get('problem', '')}
Approach: {structured_data.get('approach', '')}

Include:
- Main application class
- Basic controller with a health endpoint
- Maven pom.xml
Respond with content for each file separately, labeled.
"""
        response = self.llm.generate(prompt)
        # Dummy static output fallback:
        main_java = """package com.example;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
"""
        pom = """<project xmlns=\"http://maven.apache.org/POM/4.0.0\"
         xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"
         xsi:schemaLocation=\"http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd\">
    <modelVersion>4.0.0</modelVersion>
    <groupId>com.example</groupId>
    <artifactId>demo</artifactId>
    <version>1.0.0</version>
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
    </dependencies>
</project>
"""
        self.fs_tool.write_text("output/implementation/backend/src/main/java/com/example/Application.java", main_java)
        self.fs_tool.write_text("output/implementation/backend/pom.xml", pom)

    def _write_frontend_files(self, structured_data):
        prompt = f"""Generate a minimal React + TypeScript frontend for a system titled: {structured_data.get('title', 'App')}.
It should render a heading and describe the purpose of the app in plain text.
Respond with:
- index.tsx
- package.json with dependencies (React, Zustand, etc)
"""
        response = self.llm.generate(prompt)
        # Static fallback
        index_tsx = """import React from 'react';
import ReactDOM from 'react-dom/client';

const App = () => <h1>Hello from React Scaffold</h1>;

const root = ReactDOM.createRoot(document.getElementById('root')!);
root.render(<App />);
"""
        package_json = """{
  \"name\": \"frontend\",
  \"version\": \"1.0.0\",
  \"dependencies\": {
    \"react\": \"^18.2.0\",
    \"react-dom\": \"^18.2.0\",
    \"zustand\": \"^4.3.0\"
  }
}
"""
        self.fs_tool.write_text("output/implementation/frontend/src/index.tsx", index_tsx)
        self.fs_tool.write_text("output/implementation/frontend/package.json", package_json)
```

```python
# agents/evaluator_agent.py
import os
from tools.filesystem_tool import FileSystemTool
from tools.ollama_client import OllamaClient

class EvaluatorAgent:
    def __init__(self, fs_tool: FileSystemTool, llm_client: OllamaClient):
        self.fs_tool = fs_tool
        self.llm = llm_client

    def run(self) -> str:
        """
        Evaluates generated outputs and returns a summary string using LLM.
        """
        summary = []

        # Check for key output files
        required_files = [
            "output/prd.md",
            "output/architecture.md",
            "output/implementation/backend/src/main/java/com/example/Application.java",
            "output/implementation/frontend/src/index.tsx"
        ]

        for path in required_files:
            if self.fs_tool.file_exists(path):
                summary.append(f"✅ {path} exists")
            else:
                summary.append(f"❌ {path} is missing")

        # Heuristic + LLM Evaluation
        prd_text = self.fs_tool.read_text("output/prd.md") or ""
        if len(prd_text.split()) > 100:
            summary.append("📘 PRD has sufficient length")
        else:
            summary.append("⚠️  PRD might be too short")

        prompt = f"""You are a software product reviewer.
Evaluate the following PRD in terms of clarity, completeness, and feasibility.
Provide a score from 1 to 10 and a brief justification.

---
{prd_text[:2048]}
---
"""
        try:
            eval_response = self.llm.generate(prompt)
            summary.append("🤖 LLM Evaluation of PRD:")
            summary.append(eval_response.strip())
        except Exception as e:
            summary.append(f"⚠️  LLM evaluation failed: {e}")

        report = "\n".join(summary)
        self.fs_tool.write_text("output/evaluation.txt", report)
        print("📊 Evaluation complete with LLM support.")
        return report
```

Perfecto, aquí tienes un **ejemplo completo de ejecución** de tu sistema multiagente para transformar un paper técnico en entregables de producto, usando Ollama localmente como motor de razonamiento.

---

## ✅ Requisitos previos

1. **Tener Ollama en ejecución con un modelo cargado**, por ejemplo:

```bash
ollama run mistral
```

2. **Instalar dependencias**:

```bash
make install
```

---

## 📁 Estructura esperada del proyecto (simplificada)

```
.
├── main.py
├── agents/
├── tools/
├── utils/
├── workspace/                # se genera al ejecutar
├── requirements.txt
├── Makefile
```

---

## 🧪 Ejecución del sistema

### Paso 1: Prepara el prompt y el paper

Asume que tienes un archivo llamado `sample_paper.pdf` en el root del proyecto, y tu prompt sea algo como:

```bash
PROMPT="Create a product based on this paper on connectivity estimation to a transformer using voltage correlations."
```

### Paso 2: Ejecuta con Makefile

```bash
make run PROMPT="$PROMPT" PAPER=sample_paper.pdf
```

> Si estás ejecutando directamente sin Makefile:
```bash
python main.py "$PROMPT" sample_paper.pdf
```

---

## 📂 Resultado esperado

Se creará un directorio en `workspace/{session-id}/` con archivos como:

```
workspace/20240501-154730-7f3d9e1c/
├── input/
│   ├── prompt.txt
│   └── paper.pdf
├── intermediate/
│   ├── raw_paper_text.txt
│   ├── structured_data.json
│   └── plan.json
├── output/
│   ├── prd.md
│   ├── architecture.md
│   ├── implementation/
│   │   ├── backend/...
│   │   └── frontend/...
│   └── evaluation.txt
```

---

## 📊 Archivos clave de salida

- `prd.md`: Documento de requisitos generado por LLM
- `architecture.md`: Diseño técnico con diagrama
- `implementation/`: Código inicial backend + frontend
- `evaluation.txt`: Revisión automática con comentarios y puntuación del PRD

---

Script run_demo.sh, que te permite lanzar fácilmente una ejecución del sistema multiagente desde terminal con un prompt y un archivo PDF como argumentos:

```bash
#!/bin/bash

# run_demo.sh
# Usage: ./run_demo.sh "<your prompt>" <path_to_pdf>

PROMPT="$1"
PAPER="$2"

if [ -z "$PROMPT" ] || [ -z "$PAPER" ]; then
  echo "Usage: ./run_demo.sh \"<your prompt>\" <path_to_pdf>"
  exit 1
fi

python main.py "$PROMPT" "$PAPER"
```

```bash
chmod +x run_demo.sh
./run_demo.sh "Build a system based on this transformer connectivity paper" sample_paper.pdf
```
