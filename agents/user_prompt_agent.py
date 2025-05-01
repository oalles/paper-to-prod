import shutil
from pathlib import Path
from tools.filesystem_tool import FileSystemTool # Assuming FileSystemTool is in tools directory

class UserPromptAgent:
    def __init__(self, prompt: str, paper_path: str, fs_tool: FileSystemTool):
        self.prompt = prompt
        # Ensure paper_path is absolute and exists before proceeding
        self.paper_path = Path(paper_path).resolve()
        if not self.paper_path.is_file():
             # This check should ideally be done earlier (e.g., in main.py)
             # but adding a safeguard here.
             raise FileNotFoundError(f"Paper file not found at: {self.paper_path}")
        self.fs_tool = fs_tool
        print("👤 Initialized UserPromptAgent.")

    def init_session(self):
        """
        Initializes the session by storing the prompt and copying the paper
        into the 'input' subdirectory of the session workspace.
        """
        print("   ➡️ Initializing session workspace...")
        try:
            # Define relative paths within the workspace
            prompt_file_rel = "input/prompt.txt"
            paper_file_rel = "input/paper.pdf"

            # Save prompt to a file using FileSystemTool
            self.fs_tool.write_text(prompt_file_rel, self.prompt)

            # Get the destination path within the workspace using FileSystemTool
            dest_path_abs = self.fs_tool.get_full_path(paper_file_rel)
            dest_dir = Path(dest_path_abs).parent

            # Ensure the destination directory exists (FileSystemTool's write_text handles this,
            # but explicit creation might be needed if copying first)
            # self.fs_tool.make_directory("input") # Redundant if write_text is called first

            # Copy the paper file to the workspace input directory
            shutil.copy2(self.paper_path, dest_path_abs)
            print(f"   📄 Copied paper to: {paper_file_rel}")

            print("   ✅ Session workspace initialized successfully.")

        except Exception as e:
            print(f"   ❌ Error initializing session: {e}")
            # Depending on the desired robustness, you might want to re-raise the exception
            # or handle it more gracefully.
            raise # Re-raise the exception to halt execution if init fails

