import os
from pathlib import Path
from typing import Optional

class FileSystemTool:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path).resolve()
        self.base_path.mkdir(parents=True, exist_ok=True)
        print(f"📦 Initialized FileSystemTool with base path: {self.base_path}")

    def _resolve_path(self, relative_path: str) -> Path:
        """Resolves a relative path against the base path and ensures it's within the sandbox."""
        resolved_path = (self.base_path / relative_path).resolve()
        # Security check: Ensure the resolved path is still within the base_path directory
        if self.base_path not in resolved_path.parents and resolved_path != self.base_path:
             # Allow access if it's exactly the base path itself
            if not str(resolved_path).startswith(str(self.base_path)):
                 raise PermissionError(f"Attempted access outside sandbox directory: {resolved_path}")
        return resolved_path

    def write_text(self, relative_path: str, content: str):
        """Writes text content to a file within the workspace."""
        path = self._resolve_path(relative_path)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
            print(f"   📄 Wrote text to: {relative_path}")
        except Exception as e:
            print(f"   ❌ Error writing to {relative_path}: {e}")


    def read_text(self, relative_path: str) -> Optional[str]:
        """Reads text content from a file within the workspace."""
        path = self._resolve_path(relative_path)
        if not path.exists():
            print(f"   ⚠️ File not found: {relative_path}")
            return None
        try:
            content = path.read_text(encoding="utf-8")
            print(f"   📄 Read text from: {relative_path}")
            return content
        except Exception as e:
            print(f"   ❌ Error reading from {relative_path}: {e}")
            return None


    def list_files(self, relative_dir: str = "") -> list:
        """Lists files recursively within a directory in the workspace."""
        dir_path = self._resolve_path(relative_dir)
        if not dir_path.is_dir():
            print(f"   ⚠️ Directory not found for listing: {relative_dir}")
            return []
        try:
            files = [str(p.relative_to(self.base_path)) for p in dir_path.rglob("*") if p.is_file()]
            print(f"   📂 Listed {len(files)} files in: {relative_dir if relative_dir else '.'}")
            return files
        except Exception as e:
            print(f"   ❌ Error listing files in {relative_dir}: {e}")
            return []

    def file_exists(self, relative_path: str) -> bool:
        """Checks if a file exists within the workspace."""
        path = self._resolve_path(relative_path)
        exists = path.exists() and path.is_file()
        # print(f"   ❓ Checked existence of {relative_path}: {'Exists' if exists else 'Not Found'}")
        return exists

    def dir_exists(self, relative_path: str) -> bool:
        """Checks if a directory exists within the workspace."""
        path = self._resolve_path(relative_path)
        exists = path.exists() and path.is_dir()
        # print(f"   ❓ Checked existence of directory {relative_path}: {'Exists' if exists else 'Not Found'}")
        return exists


    def delete_file(self, relative_path: str):
        """Deletes a file within the workspace."""
        path = self._resolve_path(relative_path)
        if path.exists() and path.is_file():
            try:
                path.unlink()
                print(f"   🗑️ Deleted file: {relative_path}")
            except Exception as e:
                print(f"   ❌ Error deleting file {relative_path}: {e}")
        elif not path.exists():
             print(f"   ⚠️ File not found for deletion: {relative_path}")
        else:
             print(f"   ⚠️ Path is not a file, cannot delete: {relative_path}")


    def make_directory(self, relative_path: str):
        """Creates a directory (including parents) within the workspace."""
        path = self._resolve_path(relative_path)
        try:
            path.mkdir(parents=True, exist_ok=True)
            print(f"   📂 Created directory: {relative_path}")
        except Exception as e:
            print(f"   ❌ Error creating directory {relative_path}: {e}")


    def get_full_path(self, relative_path: str) -> str:
        """Gets the absolute path for a relative path within the workspace."""
        return str(self._resolve_path(relative_path))

