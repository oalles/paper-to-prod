import json
from tools.filesystem_tool import FileSystemTool
from tools.ollama_client import OllamaClient
from typing import Dict, Optional

class PRDWriterAgent:
    def __init__(self, fs_tool: FileSystemTool, llm_client: OllamaClient):
        self.fs_tool = fs_tool
        self.llm = llm_client
        print("✍️ Initialized PRDWriterAgent.")

    def run(self, structured_data: Optional[Dict] = None):
        """
        Creates a Product Requirements Document (PRD) in Markdown format
        from structured data using an LLM.
        """
        print("   ➡️ Generating Product Requirements Document (PRD)...")
        prd_path_rel = "output/prd.md"
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
            prompt = f"""You are a skilled Technical Product Manager. Your task is to generate a comprehensive Product Requirements Document (PRD) in Markdown format. Use the structured information extracted from a research paper provided below.

Extracted Paper Information:
- **Title:** {structured_data.get('title', 'Untitled Project')}
- **Problem:** {structured_data.get('problem', 'No problem description provided.')}
- **Approach:** {structured_data.get('approach', 'No approach description provided.')}
- **Metrics:** {', '.join(structured_data.get('metrics', ['Not specified']))}
- **Datasets:** {', '.join(structured_data.get('datasets', ['Not specified']))}

Please generate the PRD including at least the following sections:
1.  **Introduction/Overview:** Briefly introduce the product and its purpose based on the paper.
2.  **Goals:** What are the primary objectives of this product?
3.  **Problem Statement:** Elaborate on the core problem being solved.
4.  **Proposed Solution/Approach:** Detail the technical approach derived from the paper.
5.  **Key Features/Functionalities:** List the main capabilities the product should have.
6.  **Target Users:** Who is this product intended for?
7.  **Success Metrics:** How will the success of this product be measured (referencing paper metrics if applicable)?
8.  **Constraints/Assumptions:** Any limitations or assumptions made.
9.  **(Optional) Future Considerations:** Potential next steps or enhancements.

Respond ONLY with the complete PRD in well-formatted Markdown. Do not include any introductory text before the PRD content.

--- START PRD ---
# Product Requirements Document: {structured_data.get('title', 'Untitled Project')}

"""
            # (The prompt structure guides the LLM to start the Markdown directly)

            print("      🤖 Sending PRD generation request to LLM...")
            prd_md_content = self.llm.generate(prompt)

            if not prd_md_content:
                 print("      ⚠️ LLM returned empty content for PRD. Skipping file write.")
                 return

            # Ensure the response starts reasonably (sometimes LLMs add preamble)
            # A simple check: if the response doesn't start with '#', prepend the title line.
            if not prd_md_content.strip().startswith("#"):
                 print("      ⚠️ LLM response didn't start with Markdown title, prepending.")
                 prd_md_content = f"# Product Requirements Document: {structured_data.get('title', 'Untitled Project')}\n\n" + prd_md_content

            # Save the generated PRD
            self.fs_tool.write_text(prd_path_rel, prd_md_content)
            print(f"   ✅ PRD document generated and saved to {prd_path_rel}.")

        except Exception as e:
            print(f"   ❌ An unexpected error occurred in PRDWriterAgent: {e}")

