from tools.filesystem_tool import FileSystemTool
from tools.ollama_client import OllamaClient
import json

class ExecutionPlanAgent:
    def __init__(self, fs_tool: FileSystemTool, llm_client: OllamaClient):
        self.fs_tool = fs_tool
        self.llm = llm_client

    def run(self, structured_data: dict):
        """
        Genera un plan de ejecución detallado en forma de tabla con checklist, 
        basado en la información estructurada extraída del paper.
        """
        print("🗓️ Generando plan de ejecución...")
        
        # Leer datos del PRD y arquitectura para tener contexto adicional
        prd_content = self.fs_tool.read_text("output/prd.md") or ""
        arch_content = self.fs_tool.read_text("output/architecture.md") or ""
        
        # Construir prompt para el LLM
        prompt = f"""Eres un Project Manager experimentado.
Basándote en la siguiente información extraída de un paper técnico y los documentos de PRD y arquitectura ya generados,
crea un plan de ejecución detallado en formato Markdown.

DATOS DEL PAPER:
Título: {structured_data.get('title', 'Proyecto sin título')}
Problema: {structured_data.get('problem', 'No especificado')}
Enfoque: {structured_data.get('approach', 'No especificado')}

EXTRACTO DEL PRD:
{prd_content[:500]}...

EXTRACTO DE ARQUITECTURA:
{arch_content[:500]}...

Tu plan de ejecución debe incluir:
1. Una tabla con las siguientes columnas:
   - Fase/Iteración (con numeración)
   - Actividades principales
   - Roles involucrados
   - Duración estimada
   - Entregables

2. Una sección de "Hitos clave" con fechas relativas (ej: Semana 1, Mes 2)

3. Una sección de "Riesgos y mitigaciones"

4. Una sección "Criterios de aceptación" para cada fase

Usa formato Markdown con tablas bien estructuradas.
"""
        
        # Generar el plan de ejecución usando el LLM
        execution_plan_md = self.llm.generate(prompt)
        
        # Guardar el plan en el filesystem
        self.fs_tool.write_text("output/execution_plan.md", execution_plan_md)
        print("✅ Plan de ejecución generado y guardado exitosamente.")
        
        # Opcional: Tratar de extraer datos estructurados del plan para uso posterior
        try:
            # Extraer fechas y fases clave (análisis simple)
            phases_prompt = f"""
Extrae las fases principales y sus duraciones del siguiente plan de ejecución,
en formato JSON simple con este esquema: 
{{
  "phases": [
    {{"name": "nombre_fase", "duration": "duración_estimada", "deliverables": ["entregable1", "entregable2"]}},
    ...
  ]
}}

Plan:
{execution_plan_md}
"""
            phases_json_str = self.llm.generate(phases_prompt)
            
            # Intentar parsear la respuesta como JSON
            try:
                # Buscar y extraer solo la parte JSON de la respuesta
                import re
                json_match = re.search(r'({.*})', phases_json_str.replace('\n', ' '), re.DOTALL)
                if json_match:
                    phases_data = json.loads(json_match.group(1))
                    self.fs_tool.write_text("intermediate/execution_phases.json", json.dumps(phases_data, indent=2))
            except json.JSONDecodeError:
                print("⚠️ No se pudo extraer datos estructurados del plan de ejecución.")
                
        except Exception as e:
            print(f"⚠️ Error al procesar datos estructurados del plan: {e}")
        
        return execution_plan_md
