# MultiAgent Product Synthesizer

Este proyecto implementa una arquitectura multiagente para transformar papers técnicos en entregables de software utilizando Ollama como motor LLM local.

---

## 📦 Estructura del Proyecto

```
paper-to-prod/
├── main.py                  # Punto de entrada principal
├── agents/                  # Agentes multiagente (cada uno con una responsabilidad)
│   ├── user_prompt_agent.py
│   ├── paper_reader_agent.py
│   ├── planner_agent.py
│   ├── prd_writer_agent.py
│   ├── architecture_agent.py
│   ├── implementer_agent.py
│   └── evaluator_agent.py
├── tools/                   # Herramientas de soporte (filesystem, cliente Ollama)
│   ├── filesystem_tool.py
│   └── ollama_client.py
├── utils/                   # Utilidades generales (gestión de sesión)
│   ├── session.py
│   └── setup.py
├── workspace/               # Directorio de trabajo (generado dinámicamente por sesión)
├── requirements.txt         # Dependencias del proyecto
├── Makefile                 # Automatización de tareas
├── run_demo.sh              # Script de ejemplo para ejecución rápida
└── README.md                # Documentación del proyecto
```

---

## 🧠 Descripción General

El sistema orquesta varios agentes que colaboran para convertir un paper técnico en:
- Documento de requisitos (PRD)
- Diseño de arquitectura
- Plan de ejecución
- Código inicial backend (Java/Spring Boot) y frontend (React/TS)
- Evaluación automática

Todo el razonamiento y generación de texto/código se apoya en un modelo LLM local vía Ollama.

---

## ⚙️ Flujo de Ejecución

1. **Preparar entorno y dependencias**
    ```bash
    make install
    ```
2. **Asegurarse de que Ollama esté corriendo con un modelo (ejemplo: mistral)**
    ```bash
    ollama run mistral
    ```
3. **Ejecutar el sistema**
    - Usando Makefile:
      ```bash
      make run PROMPT="<tu prompt>" PAPER=<ruta_al_paper.pdf>
      ```
    - O con el script de demo:
      ```bash
      chmod +x run_demo.sh
      ./run_demo.sh "<tu prompt>" <ruta_al_paper.pdf>
      ```
    - O directamente:
      ```bash
      python main.py "<tu prompt>" <ruta_al_paper.pdf>
      ```
4. **Limpiar el entorno**
    ```bash
    make clean
    ```

---

## 🗂️ Estructura de Salida

Cada ejecución crea un directorio único en `workspace/`:

```
workspace/{session-id}/
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
│   │   ├── backend/
│   │   └── frontend/
│   └── evaluation.txt
```

---

## 🤖 Agentes Principales

- **UserPromptAgent**: Inicializa la sesión y almacena el prompt y el paper.
- **PaperReaderAgent**: Extrae texto y estructura básica del paper usando LLM.
- **PlannerAgent**: Planifica tareas a partir del análisis del paper.
- **PRDWriterAgent**: Genera el PRD en Markdown usando LLM.
- **ArchitectureAgent**: Propone la arquitectura técnica (incluye diagrama Mermaid).
- **ImplementerAgent**: Genera el esqueleto de código backend y frontend.
- **EvaluatorAgent**: Evalúa los entregables y produce un informe.

---

## 🛠️ Dependencias

- Python 3.11+
- [Ollama](https://ollama.com/) (modelo recomendado: mistral)
- PyMuPDF, ruff, sentence-transformers, openai, pandas, tqdm

Instalación rápida:
```bash
make install
```

---

## 🧪 Prueba rápida de Ollama

Verifica que Ollama responde correctamente:
```bash
make test-ollama
```

---

## ⚠️ Notas y Recomendaciones

- El sistema requiere que Ollama esté activo y accesible en `localhost:11434`.
- El código generado es un esqueleto inicial, no producción.
- El workspace se limpia con `make clean`.
- Puedes modificar los agentes para personalizar prompts o lógica.

---

## 📄 Ejemplo de ejecución

```bash
PROMPT="Crear un producto basado en este paper sobre estimación de conectividad usando correlaciones de voltaje."
make run PROMPT="$PROMPT" PAPER=sample_paper.pdf
```

---

## 📚 Referencias

- [Ollama](https://ollama.com/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [sentence-transformers](https://www.sbert.net/)
```
