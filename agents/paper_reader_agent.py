import fitz  # PyMuPDF
import json
import re # Import regular expressions for parsing
from pathlib import Path
from tools.filesystem_tool import FileSystemTool
from tools.ollama_client import OllamaClient
from typing import Dict, Optional

class PaperReaderAgent:
    def __init__(self, fs_tool: FileSystemTool, llm_client: OllamaClient):
        self.fs_tool = fs_tool
        self.llm = llm_client
        print("🧐 Initialized PaperReaderAgent.")

    def run(self) -> Optional[Dict]:
        """
        Reads the paper, extracts text, analyzes with LLM for structured data,
        and saves intermediate results. Returns the structured data dictionary or None on failure.
        """
        print("   ➡️ Reading and analyzing paper...")
        paper_path_rel = "input/paper.pdf"
        raw_text_path_rel = "intermediate/raw_paper_text.txt"
        structured_data_path_rel = "intermediate/structured_data.json"

        try:
            # 1. Get full path and check existence
            paper_path_abs = self.fs_tool.get_full_path(paper_path_rel)
            if not self.fs_tool.file_exists(paper_path_rel):
                 print(f"   ❌ Error: Paper file not found at {paper_path_rel}")
                 return None

            # 2. Extract text from PDF
            pdf_text = self._extract_text_from_pdf(paper_path_abs)
            if not pdf_text:
                print("   ❌ Error: Could not extract text from PDF.")
                return None
            self.fs_tool.write_text(raw_text_path_rel, pdf_text) # Save raw text

            # 3. Analyze text with LLM
            structured_data = self._analyze_text_with_llm(pdf_text)
            if not structured_data:
                 print("   ❌ Error: Failed to get structured data from LLM analysis.")
                 return None

            # 4. Save structured data
            self.fs_tool.write_text(structured_data_path_rel, json.dumps(structured_data, indent=2))

            print("   ✅ Paper parsed and structured data extracted successfully.")
            return structured_data

        except Exception as e:
            print(f"   ❌ An unexpected error occurred in PaperReaderAgent: {e}")
            return None


    def _extract_text_from_pdf(self, path: str) -> Optional[str]:
        """Extracts text content from a PDF file."""
        try:
            doc = fitz.open(path)
            text = "\n".join([page.get_text() for page in doc])
            doc.close()
            print(f"      📄 Extracted ~{len(text)} characters from PDF.")
            return text
        except Exception as e:
            print(f"      ❌ Error extracting text from PDF {path}: {e}")
            return None

    def _analyze_text_with_llm(self, text: str) -> Optional[Dict]:
        """Uses LLM to extract structured information from the paper text."""
        # Limit text length to avoid exceeding context window or costs
        max_chars = 8000 # Adjust as needed based on model context window
        text_snippet = text[:max_chars]

        prompt = f"""Please analyze the following research paper text and extract the key information in a structured format. Focus on these fields:

1.  **Title:** The main title of the paper.
2.  **Problem:** Briefly describe the core problem the paper addresses.
3.  **Approach:** Summarize the main methodology or approach proposed.
4.  **Metrics:** List the key metrics used for evaluation.
5.  **Datasets:** Mention any specific datasets used or created.

Respond ONLY with the extracted information, using clear labels for each field (e.g., "Title: ...", "Problem: ...").

--- START PAPER TEXT ---
{text_snippet}
--- END PAPER TEXT ---

Extracted Information:
"""
        print("      🤖 Sending text snippet to LLM for analysis...")
        try:
            llm_response = self.llm.generate(prompt)
            if not llm_response:
                 print("      ⚠️ LLM returned an empty response.")
                 return None
            print("      🤖 Received LLM response. Parsing...")
            # print(f"LLM Raw Response:\n{llm_response[:500]}...") # Optional: for debugging
            parsed_data = self._parse_llm_response(llm_response)
            return parsed_data
        except Exception as e:
            print(f"      ❌ Error during LLM analysis: {e}")
            return None

    def _parse_llm_response(self, response: str) -> Dict:
        """
        Parses the LLM response to extract structured fields.
        This is a basic parser and might need improvement based on LLM output format.
        """
        data = {
            "title": "Unknown Title",
            "problem": "Not extracted",
            "approach": "Not extracted",
            "metrics": [],
            "datasets": []
        }

        # Try to extract fields using simple regex or string splitting
        # This assumes the LLM follows the requested format reasonably well.
        fields = ["Title", "Problem", "Approach", "Metrics", "Datasets"]
        current_field = None
        content_buffer = ""

        lines = response.splitlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue

            matched_field = None
            for field in fields:
                # Check if line starts with "Field:" or "Field Name:" etc.
                if re.match(rf"^\s*{re.escape(field)}\s*[:\-]", line, re.IGNORECASE):
                    matched_field = field
                    # Extract content after the colon/dash
                    content_after_label = re.sub(rf"^\s*{re.escape(field)}\s*[:\-]\s*", "", line, flags=re.IGNORECASE)
                    break # Found the field label for this line

            if matched_field:
                # If we were buffering content for a previous field, save it
                if current_field and content_buffer:
                    if current_field in ["Metrics", "Datasets"]:
                         # Simple list splitting for metrics/datasets
                         items = [item.strip() for item in content_buffer.split(',') if item.strip()]
                         data[current_field.lower()] = items
                    else:
                         data[current_field.lower()] = content_buffer.strip()

                # Start buffering for the new field
                current_field = matched_field
                content_buffer = content_after_label # Start with content on the same line
            elif current_field:
                # If it's not a new field label, append to the current buffer
                content_buffer += " " + line

        # Save the last buffered content
        if current_field and content_buffer:
             if current_field in ["Metrics", "Datasets"]:
                 items = [item.strip() for item in content_buffer.split(',') if item.strip()]
                 data[current_field.lower()] = items
             else:
                 data[current_field.lower()] = content_buffer.strip()


        # Fallback/Refinement: If title wasn't found via label, maybe take the first line?
        if data["title"] == "Unknown Title" and lines:
             potential_title = lines[0].strip()
             # Basic check if it looks like a title (not a label itself)
             is_label = any(re.match(rf"^\s*{re.escape(f)}\s*[:\-]", potential_title, re.IGNORECASE) for f in fields)
             if not is_label and len(potential_title) > 5 and len(potential_title) < 150:
                 data["title"] = potential_title


        print(f"      📊 Parsed structured data: Title='{data.get('title', '')[:50]}...', Problem='{data.get('problem', '')[:50]}...'")
        return data

