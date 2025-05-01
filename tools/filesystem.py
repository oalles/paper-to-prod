from crewai import Tool

class FileSystemTool(Tool):
    name = "FileSystemTool"
    description = "Lee y escribe archivos en el workspace de la sesión."

    def read_file(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def write_file(self, path, content):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Archivo escrito: {path}"
