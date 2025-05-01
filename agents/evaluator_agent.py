import os
from tools.filesystem_tool import FileSystemTool
from tools.ollama_client import OllamaClient
from typing import Optional

class EvaluatorAgent:
    def __init__(self, fs_tool: FileSystemTool, llm_client: OllamaClient):
        self.fs_tool = fs_tool
        self.llm = llm_client
        print("📊 Initialized EvaluatorAgent.")

    def _validate_mermaid_diagram(self, architecture_path: str) -> bool:
        """
        Validates that the architecture file contains a valid Mermaid diagram.
        """
        try:
            content = self.fs_tool.read_text(architecture_path)
            if "```mermaid" in content:
                print(f"   ✅ Mermaid diagram found in {architecture_path}.")
                return True
            else:
                print(f"   ⚠️ No Mermaid diagram found in {architecture_path}.")
                return False
        except Exception as e:
            print(f"   ❌ Error reading architecture file for Mermaid validation: {e}")
            return False

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

        # Validate Mermaid diagram in architecture.md
        architecture_path = "output/architecture.md"
        if self.fs_tool.file_exists(architecture_path):
            if not self._validate_mermaid_diagram(architecture_path):
                summary.append(f"⚠️ Mermaid diagram validation failed for {architecture_path}.")

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

        # Adaptive iteration based on evaluation
        if "⚠️" in "\n".join(summary):
            print("🔄 Issues detected. Triggering adaptive iteration...")
            # Logic for adaptive iteration (e.g., re-run agents with adjusted prompts)

        report = "\n".join(summary)
        self.fs_tool.write_text("output/evaluation.txt", report)
        print("📊 Evaluation complete with LLM support.")
        return report

