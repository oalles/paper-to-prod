import json
from tools.filesystem_tool import FileSystemTool
from tools.ollama_client import OllamaClient
from typing import Dict, Optional

class PlannerAgent:
    def __init__(self, fs_tool: FileSystemTool, llm_client: OllamaClient):
        self.fs_tool = fs_tool
        self.llm = llm_client
        print("🧭 Initialized PlannerAgent.")

    def run(self, structured_data: dict) -> Optional[Dict]:
        """
        Plans the sequence of actions based on the structured data from the paper using LLM support.
        Returns the plan dictionary or None on failure.
        """
        print("   ➡️ Generating execution plan...")
        plan_path_rel = "intermediate/plan.json"
        structured_data_path_rel = "intermediate/structured_data.json" # Path to read from

        try:
            # Ensure structured_data is available (either passed directly or read from file)
            if not structured_data:
                 print("      ⚠️ Structured data not provided directly, attempting to read from file...")
                 data_str = self.fs_tool.read_text(structured_data_path_rel)
                 if not data_str:
                     print(f"      ❌ Error: Could not read structured data from {structured_data_path_rel}")
                     return None
                 try:
                     structured_data = json.loads(data_str)
                 except json.JSONDecodeError:
                     print(f"      ❌ Error: Invalid JSON in {structured_data_path_rel}")
                     return None

            # Prepare prompt for LLM
            planning_prompt = f"""Given the following extracted information from a research paper:

Title: {structured_data.get('title', 'Untitled')}
Problem: {structured_data.get('problem', 'Not specified')}
Approach: {structured_data.get('approach', 'Not specified')}

Generate a high-level task plan for developing a software product that implements this idea.
List the main steps needed. Focus on including keywords like:
- PRD (for Product Requirements Document)
- Architecture (for system design)
- Implementation (for coding/scaffolding)
- Evaluation (for testing/review)

Respond ONLY with a bulleted or numbered list of the main steps.
Example:
- Generate PRD
- Design Architecture
- Propose Implementation
- Evaluate Results
"""
            print("      🤖 Sending planning request to LLM...")
            llm_response = self.llm.generate(planning_prompt)

            if not llm_response:
                 print("      ⚠️ LLM returned an empty response for planning.")
                 # Create a default plan as fallback?
                 plan = self._create_default_plan(llm_response or "")
            else:
                 print("      🤖 Received planning response from LLM. Parsing...")
                 # Parse the LLM response to determine which steps are included
                 plan = self._parse_llm_plan(llm_response)

            # Save the generated plan
            self.fs_tool.write_text(plan_path_rel, json.dumps(plan, indent=2))
            print("   ✅ Planning completed and saved.")
            return plan

        except Exception as e:
            print(f"   ❌ An unexpected error occurred in PlannerAgent: {e}")
            return None

    def _parse_llm_plan(self, llm_response: str) -> Dict:
        """Parses the LLM response to create a structured plan dictionary."""
        response_lower = llm_response.lower()
        plan = {
            # Check for keywords in the LLM response
            "generate_prd": "prd" in response_lower or "product requirement" in response_lower,
            "design_architecture": "architecture" in response_lower or "design" in response_lower,
            # Exclude implementer for now based on user request
            "propose_implementation": False, # "implementation" in response_lower or "coding" in response_lower or "scaffold" in response_lower,
            "evaluation": "evaluation" in response_lower or "testing" in response_lower or "review" in response_lower,
            "llm_plan_text": llm_response.strip() # Store the raw LLM plan text
        }
        print(f"      📊 Parsed plan: PRD={plan['generate_prd']}, Arch={plan['design_architecture']}, Impl={plan['propose_implementation']}, Eval={plan['evaluation']}")
        if not plan["propose_implementation"]:
             print("      ℹ️ Implementation step explicitly skipped as requested.")
        return plan

    def _create_default_plan(self, llm_response_text: str = "Default plan due to empty LLM response") -> Dict:
         """Creates a default plan if LLM fails."""
         print("      ⚠️ Creating default plan as fallback.")
         return {
            "generate_prd": True,
            "design_architecture": True,
            "propose_implementation": False, # Skipped
            "evaluation": True,
            "llm_plan_text": llm_response_text
        }
