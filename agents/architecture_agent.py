import json
from tools.filesystem_tool import FileSystemTool
from tools.ollama_client import OllamaClient
from typing import Dict, Optional

class ArchitectureAgent:
    def __init__(self, fs_tool: FileSystemTool, llm_client: OllamaClient):
        self.fs_tool = fs_tool
        self.llm = llm_client
        print("🏗️  Initialized ArchitectureAgent.")

    def run(self, structured_data: Optional[Dict] = None):
        """
        Generates an architecture proposal document in Markdown format using an LLM,
        based on the structured data from the paper.
        """
        print("   ➡️ Generating Architecture Document...")
        arch_path_rel = "output/architecture.md"
        structured_data_path_rel = "intermediate/structured_data.json"

        try:
            # Ensure structured_data is available
            if not structured_data:
                 print("      ⚠️ Structured data not provided directly, attempting to read from file...")
                 data_str = self.fs_tool.read_text(structured_data_path_rel)
                 if not data_str:
                     print(f"      ❌ Error: Could not read structured data from {structured_data_path_rel}")
                     return # Cannot proceed without structured data
                 try:
                     structured_data = json.loads(data_str)
                 except json.JSONDecodeError:
                     print(f"      ❌ Error: Invalid JSON in {structured_data_path_rel}")
                     return # Cannot proceed

            # Prepare prompt for LLM
            prompt = f"""You are a senior Software Architect. Based on the following structured information extracted from a technical paper, generate a concise System Architecture document in Markdown format.

Extracted Paper Information:
- **Title:** {structured_data.get('title', 'Untitled System')}
- **Problem:** {structured_data.get('problem', 'Not specified')}
- **Approach:** {structured_data.get('approach', 'Not specified')}

Include the following sections in the architecture document:
1.  **Overview:** A brief description of the system's purpose.
2.  **Key Components:** List the main logical parts of the system (e.g., Input Processor, Core Engine, API Layer, UI).
3.  **Technology Stack:** Suggest relevant technologies (e.g., Python/Java/Node.js, Database, Frontend framework). Be specific if possible based on the approach.
4.  **Deployment Strategy:** Briefly mention how it could be deployed (e.g., Docker, Serverless, Cloud VM).
5.  **Data Flow Diagram (Mermaid):** Create a simple flowchart or sequence diagram using Mermaid syntax to illustrate the main data flow between components.
6.  **Key Considerations:** Mention 1-2 important architectural considerations (e.g., Scalability, Modularity, Security).

Respond ONLY with the complete architecture document in well-formatted Markdown. Do not include any introductory text before the document content.

--- START ARCHITECTURE DOCUMENT ---
# System Architecture: {structured_data.get('title', 'Untitled System')}

"""
            # (The prompt guides the LLM to start the Markdown directly)

            print("      🤖 Sending architecture generation request to LLM...")
            arch_md_content = self.llm.generate(prompt)

            if not arch_md_content:
                 print("      ⚠️ LLM returned empty content for architecture document. Skipping file write.")
                 return

            # Ensure the response starts reasonably
            if not arch_md_content.strip().startswith("#"):
                 print("      ⚠️ LLM response didn't start with Markdown title, prepending.")
                 arch_md_content = f"# System Architecture: {structured_data.get('title', 'Untitled System')}\n\n" + arch_md_content

            # Save the generated architecture document
            self.fs_tool.write_text(arch_path_rel, arch_md_content)
            print(f"   ✅ Architecture document generated and saved to {arch_path_rel}.")

        except Exception as e:
            print(f"   ❌ An unexpected error occurred in ArchitectureAgent: {e}")

