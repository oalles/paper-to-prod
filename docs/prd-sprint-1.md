# 📄 PRD: MultiAgent Product Synthesizer

---

## 🧭 Visión General

**Nombre del producto:** MultiAgent Product Synthesizer  
**Propósito:** Automatizar la transformación de papers técnicos en entregables de producto software (PRD, arquitectura, plan, código inicial y evaluación) mediante una arquitectura multiagente orquestada localmente y soportada por LLM (Ollama).  
**Contexto:** Profesionales técnicos, arquitectos y equipos de innovación requieren convertir papers en prototipos funcionales y documentación técnica, acelerando la transferencia de conocimiento y la experimentación.

---

## 🎯 Objetivos del Sistema

- Recibir como entrada un prompt y un paper (PDF).
- Extraer y estructurar la información clave del paper.
- Generar automáticamente:
  - Documento de requisitos (PRD) en Markdown.
  - Diseño de arquitectura técnica (con diagrama Mermaid).
  - Plan de ejecución de tareas.
  - Esqueleto de implementación backend (Java/Spring Boot) y frontend (React/TS).
  - Evaluación automática de los entregables.
- Orquestar el flujo mediante agentes especializados, cada uno responsable de una fase.
- Garantizar aislamiento y trazabilidad por sesión en el sistema de archivos local.

---

## 👤 Usuarios Objetivo

- Arquitectos de software
- CTOs / líderes técnicos
- Investigadores en ingeniería y TI
- Analistas técnicos y equipos de innovación

---

## 🏗️ Arquitectura Técnica

### 🧩 Componentes Principales

- **Agentes** (`/agents/`):
  - `UserPromptAgent`: Inicializa sesión, almacena prompt y paper.
  - `PaperReaderAgent`: Extrae texto y estructura básica del paper (usa LLM).
  - `PlannerAgent`: Planifica tareas a partir del análisis del paper (usa LLM).
  - `PRDWriterAgent`: Genera el PRD en Markdown (usa LLM).
  - `ArchitectureAgent`: Propone la arquitectura técnica y diagrama (usa LLM).
  - `ImplementerAgent`: Genera el esqueleto de código backend y frontend (usa LLM).
  - `EvaluatorAgent`: Evalúa los entregables y produce un informe (usa LLM).
- **Herramientas** (`/tools/`):
  - `FileSystemTool`: Abstracción segura para operaciones en el workspace.
  - `OllamaClient`: Cliente para interactuar con Ollama LLM local.
- **Utilidades** (`/utils/`):
  - `session.py`: Crea y gestiona directorios de sesión únicos.
- **Workspace** (`/workspace/`):  
  Directorio sandbox por sesión, con subcarpetas para input, intermedios y output.

### 🗂️ Estructura de Carpetas

```
paper-to-prod/
├── main.py
├── agents/
├── tools/
├── utils/
├── workspace/
├── requirements.txt
├── Makefile
├── run_demo.sh
└── docs/
```

---

## 🔁 Flujo Funcional

1. **Input**  
   Prompt del usuario y archivo PDF del paper.
2. **Inicialización**  
   Se crea un workspace aislado para la sesión.
3. **Extracción**  
   El agente lector extrae texto y estructura del paper usando LLM.
4. **Planificación**  
   El agente planificador define las tareas y el flujo.
5. **Generación de PRD**  
   El agente PRDWriter produce el documento de requisitos.
6. **Diseño de Arquitectura**  
   El agente Architecture genera el diseño técnico y diagrama.
7. **Implementación Inicial**  
   El agente Implementer crea el esqueleto backend y frontend.
8. **Evaluación**  
   El agente Evaluator revisa los entregables y produce un informe.
9. **Salida**  
   Todos los artefactos quedan en el workspace de la sesión.

---

## 📦 Entregables Generados

| Tipo              | Formato                | Ubicación dentro del workspace         |
|-------------------|-----------------------|----------------------------------------|
| PRD               | Markdown              | `/output/prd.md`                      |
| Arquitectura      | Markdown + Mermaid    | `/output/architecture.md`              |
| Plan de ejecución | JSON + texto libre    | `/intermediate/plan.json`              |
| Implementación    | Código fuente         | `/output/implementation/`              |
| Evaluación        | Texto                 | `/output/evaluation.txt`               |
| Trazas            | Archivos intermedios  | `/intermediate/`                       |

---

## 🛠️ Tecnologías y Dependencias

- **Python 3.11+**
- **Ollama** (modelo recomendado: `gemma3:12b`)
- **PyMuPDF** (extracción de texto de PDF)
- **ruff** (linting y formateo)
- **sentence-transformers, openai, pandas, tqdm** (opcional/futuro)
- **Java 21 + Spring Boot** (backend generado)
- **React + TypeScript + Zustand** (frontend generado)
- **Docker** (opcional para despliegue)

---

## ⚙️ Ejecución y Uso

### 1. Instalar dependencias

```bash
make install
```

### 2. Lanzar Ollama con modelo

```bash
ollama run gemma3:12b
```

### 3. Ejecutar el sistema

```bash
make run PROMPT="Describe el producto a generar" PAPER=sample_paper.pdf
```
O directamente:
```bash
python main.py "Describe el producto a generar" sample_paper.pdf
```

### 4. Limpiar el entorno

```bash
make clean
```

---

## 📂 Estructura de Salida por Sesión

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

## 🧠 Detalles de los Agentes

- **UserPromptAgent**  
  Inicializa la sesión, almacena prompt y paper en `/input/`.
- **PaperReaderAgent**  
  Extrae texto del PDF y genera estructura básica usando LLM. Guarda resultados en `/intermediate/`.
- **PlannerAgent**  
  Usa LLM para definir el plan de tareas y dependencias. Guarda en `/intermediate/plan.json`.
- **PRDWriterAgent**  
  Genera el PRD en Markdown usando LLM y lo guarda en `/output/prd.md`.
- **ArchitectureAgent**  
  Produce el documento de arquitectura y diagrama Mermaid en `/output/architecture.md`.
- **ImplementerAgent**  
  Genera el esqueleto de código backend (Java/Spring Boot) y frontend (React/TS) en `/output/implementation/`.
- **EvaluatorAgent**  
  Evalúa los entregables, revisa la calidad del PRD y produce un informe en `/output/evaluation.txt`.

---

## 🔐 Consideraciones de Seguridad y Restricciones

- Todo el procesamiento ocurre en un workspace aislado por sesión.
- El sistema nunca ejecuta código generado.
- El acceso a archivos está restringido al workspace de la sesión.
- Sanitización básica de entradas desde PDF/texto.
- No requiere conexión a Internet para la inferencia (Ollama local).

---

## 📊 KPIs y Métricas

| Indicador                                    | Meta                       |
|-----------------------------------------------|----------------------------|
| Tiempo total de generación de entregables     | < 3 minutos                |
| Precisión de extracción de conceptos clave    | ≥ 90% (revisión humana)    |
| Tasa de reutilización del código generado     | ≥ 60% (evaluado por usuarios) |
| Iteraciones promedio necesarias por sesión    | < 3                        |
| Cobertura de documentación técnica generada   | 100% del esqueleto base    |

---

## 📝 Limitaciones Actuales

- El análisis y generación dependen de la calidad del modelo LLM local.
- El código generado es un esqueleto inicial, no listo para producción.
- El parsing de respuestas LLM es heurístico y puede requerir ajustes.
- No hay interfaz web, solo CLI.
- No se soporta aún la integración con IDEs o edición colaborativa.

---

## 🚩 Futuras Mejoras

- Mejorar el parsing estructurado de respuestas LLM.
- Añadir soporte para otros lenguajes y frameworks.
- Integrar embeddings y RAG para extracción más precisa.
- Añadir interfaz web ligera y/o integración con editores tipo Monaco.
- Mejorar la evaluación automática y la trazabilidad de decisiones.

---

## 📚 Referencias

- [Ollama](https://ollama.com/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [sentence-transformers](https://www.sbert.net/)
- [Spring Boot](https://spring.io/projects/spring-boot)
- [React](https://react.dev/)
- [Zustand](https://docs.pmnd.rs/zustand/getting-started/introduction)

---
```
