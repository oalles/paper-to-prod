# 🗺️ Roadmap del Proyecto: MultiAgent Product Synthesizer

## 📚 Introducción

Este documento describe la evolución de nuestro sistema MultiAgent Product Synthesizer a lo largo del tiempo. 
Sirve como registro educativo de cómo hemos ido incrementando la complejidad y sofisticación de nuestra solución, 
explicando cada etapa del desarrollo, los desafíos encontrados y las técnicas implementadas.

El objetivo es proporcionar una visión clara del proceso de desarrollo iterativo, mostrando cómo se pueden construir 
sistemas complejos de manera gradual, comenzando con soluciones simples que luego se refinan y mejoran.

## 🌱 Iteración 1: Orquestación Secuencial Simple

### 📋 Descripción
En esta primera iteración, implementamos un enfoque directo y lineal para procesar documentos académicos:

- ✅ Estructura de orquestación básica en una función principal (`main.py`)
- ✅ Ejecución secuencial de agentes especializados, cada uno con un rol específico
- ✅ Flujo unidireccional donde cada agente pasa su resultado al siguiente
- ✅ Manejo básico de errores para prevenir fallos catastróficos
- ✅ Sistema de logging para seguimiento del proceso

### 🏗️ Arquitectura
La arquitectura inicial adopta un patrón de "Pipeline" simple:

1. **UserPromptAgent**: Inicializa la sesión con la solicitud del usuario y el paper
2. **PaperReaderAgent**: Lee y estructura el contenido del documento académico
3. **PlannerAgent**: Genera un plan de trabajo basado en el contenido estructurado
4. **PRDWriterAgent**: Crea el documento de requisitos del producto
5. **ArchitectureAgent**: Diseña la arquitectura técnica de la solución
6. **ExecutionPlanAgent**: Detalla el plan de implementación
7. **EvaluatorAgent**: Evalúa la calidad de los artefactos generados

### 💡 Conceptos Clave
- **Composición secuencial**: Los agentes se ejecutan en orden predeterminado
- **Especialización por rol**: Cada agente tiene una función específica y bien definida
- **Persistencia entre pasos**: Uso de sistema de archivos para comunicación entre agentes
- **Gestión de errores básica**: Try/except para evitar que fallos en un agente detengan todo el proceso

### 🔍 Limitaciones Identificadas
- Flujo rígido sin capacidad de adaptar la secuencia dinámicamente
- Sin mecanismos de retroalimentación entre agentes (feedback loops)
- Ausencia de paralelismo para tareas independientes
- Comunicación limitada entre agentes (solo a través de archivos)
- No hay optimización de prompts basada en resultados anteriores
- Invocación directa de tools: No hay abstracción entre agentes y herramientas.
- Sin conocimiento de herramientas: Los LLMs no tienen conciencia de las tools disponibles

### 📈 Próximos Pasos
Evolucionar hacia un sistema más flexible utilizando frameworks de orquestación de agentes que permitan:
- Patrones de comunicación más complejos entre agentes
- Ejecución condicional y dinámica de flujos de trabajo
- Mejor gestión de recursos computacionales
- Retroalimentación y mejora continua entre agentes
- Evaluar y seleccionar un framework principal basado en necesidades específicas
- Refactorizar el sistema actual para utilizar abstracciones del framework
_ Implementar un sistema de memoria compartida entre agentes
- Desarrollar topologías dinámicas basadas en el contenido del documento
_ Integrar capacidades de Tool Calling explícitas en los prompts de los LLMs
- Esta evolución nos permitiría pasar de un sistema de pipeline rígido a un ecosistema flexible de agentes colaborativos con mayor autonomía y capacidad de adaptación.

## 🌱 Iteración 2: Orquestación con Frameworks de Agentes
e comunicación entre agentes: Facilita la comunicación directa, superando la limitación actual de usar solo archivos.