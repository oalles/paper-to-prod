# 📄 PRD Sprint 2: Evolución MultiAgent Product Synthesizer con CrewAI

---

## 🧭 Visión General

**Nombre del producto:** MultiAgent Product Synthesizer  
**Sprint 2 – Objetivo:** Evolucionar la arquitectura multiagente, migrando la orquestación a CrewAI para mejorar la colaboración, comunicación y flexibilidad entre agentes, manteniendo la automatización de la generación de entregables de producto a partir de papers técnicos.

---

## 🎯 Objetivos del Sprint

- Migrar la orquestación de agentes a CrewAI, manteniendo roles y responsabilidades.
- Mejorar la comunicación y colaboración entre agentes (más allá de archivos).
- Permitir flujos condicionales, paralelismo y retroalimentación entre agentes.
- Integrar herramientas existentes como CrewAI Tools.
- Mantener la trazabilidad y aislamiento por sesión.
- Sentar bases para futuras extensiones (memoria compartida, métricas, UI).

---

## 🏗️ Arquitectura Técnica Sprint 2

### 🧩 Componentes Principales

- **Agentes (CrewAI Agents):**
  - `UserPromptAgent`
  - `PaperReaderAgent`
  - `PlannerAgent`
  - `PRDWriterAgent`
  - `ArchitectureAgent`
  - `ImplementerAgent`
  - `EvaluatorAgent`
- **CrewAI Crew:** Orquesta el flujo, define procesos secuenciales, condicionales y paralelos.
- **Herramientas (CrewAI Tools):**
  - Adaptación de `FileSystemTool` como Tool de CrewAI.
  - Integración de herramientas personalizadas para lectura/escritura de archivos.
- **Memoria Compartida (opcional):** Permite compartir contexto entre agentes.
- **OllamaClient:** Adaptado como LLM para CrewAI.
- **Workspace:** Se mantiene la estructura de carpetas por sesión.

### 🗂️ Estructura de Carpetas

// ...igual que en Sprint 1...

---

## 🔁 Flujo Funcional Sprint 2

1. **Input y Sesión**  
   Prompt y paper PDF, creación de workspace aislado.
2. **CrewAI Crew**  
   Inicializa agentes y tareas como CrewAI Agents y Tasks.
3. **Extracción y Planificación**  
   PaperReaderAgent y PlannerAgent operan como Tasks de CrewAI.
4. **Generación de Entregables**  
   PRDWriterAgent, ArchitectureAgent, ImplementerAgent ejecutan tareas CrewAI.
5. **Evaluación y Retroalimentación**  
   EvaluatorAgent revisa entregables; se habilitan ciclos de mejora si es necesario.
6. **Comunicación y Herramientas**  
   Agentes pueden comunicarse directamente y compartir contexto/memoria.
7. **Salida**  
   Artefactos generados en el workspace de la sesión.

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
- **CrewAI** (orquestación multiagente)
- **Ollama** (modelo recomendado: `gemma3:12b`)
- **PyMuPDF** (extracción de texto de PDF)
- **ruff** (linting y formateo)
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

// ...igual que en Sprint 1...

---

## 🧠 Detalles de los Agentes y CrewAI

- **UserPromptAgent**  
  Inicializa sesión, almacena prompt y paper.
- **PaperReaderAgent**  
  Extrae texto y estructura del paper usando LLM.
- **PlannerAgent**  
  Define plan de tareas y dependencias.
- **PRDWriterAgent**  
  Genera el PRD en Markdown.
- **ArchitectureAgent**  
  Produce arquitectura técnica y diagrama Mermaid.
- **ImplementerAgent**  
  Genera esqueleto backend y frontend.
- **EvaluatorAgent**  
  Evalúa entregables y produce informe.
- **CrewAI Crew**  
  Orquesta el flujo, permite paralelismo, retroalimentación y comunicación directa.
- **Herramientas CrewAI**  
  Adaptación de FileSystemTool y otras utilidades como Tools.

---

## 🔄 Mejoras Clave Sprint 2

- **Orquestación avanzada:** CrewAI permite flujos secuenciales, condicionales y paralelos.
- **Comunicación directa:** Los agentes pueden compartir información sin depender solo de archivos.
- **Retroalimentación y ciclos de mejora:** EvaluatorAgent puede activar refinamientos automáticos.
- **Memoria compartida (opcional):** Contexto persistente entre agentes.
- **Observabilidad y métricas:** CrewAI facilita el seguimiento y análisis del flujo.
- **Preparación para UI ligera:** CrewAI soporta integración futura con interfaces de monitorización.

---

## 📝 Limitaciones y Consideraciones

- La calidad depende del modelo LLM local.
- CrewAI aún está en evolución; se recomienda revisión periódica de alternativas.
- El código generado sigue siendo un esqueleto inicial.
- No hay interfaz web aún, pero la arquitectura lo permite a futuro.
- Todo el procesamiento sigue siendo local y aislado por sesión.

---

## 🚩 Futuras Mejoras

- Integrar memoria compartida CrewAI.
- Añadir métricas y observabilidad avanzadas.
- Implementar UI ligera para monitorización.
- Mejorar parsing estructurado y soporte para nuevos lenguajes.
- Evaluar integración con Google Cloud y ADK si CrewAI resulta insuficiente.

---

## 📚 Referencias

- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [Ollama](https://ollama.com/)
- [PyMuPDF](https://pymupdf.readthedocs.io/)
- [Spring Boot](https://spring.io/projects/spring-boot)
- [React](https://react.dev/)
- [Zustand](https://docs.pmnd.rs/zustand/getting-started/introduction)

---
