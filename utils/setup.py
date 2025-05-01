import os
from pathlib import Path

def ensure_project_structure():
    """
    Ensures that all required base directories and __init__.py files exist.
    """
    base_dirs = [
        "agents",
        "tools",
        "utils",
        "workspace",
        "output",  # Aunque output esté dentro de workspace/session, tener uno en raíz puede ser útil.
        "tests",   # Añadido para acomodar pruebas
        "docs"     # Añadido para documentación
    ]

    project_root = Path(__file__).parent.parent  # Asume setup.py está en utils/
    print(f"Project root identified as: {project_root}")

    for dir_name in base_dirs:
        dir_path = project_root / dir_name
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
            print(f"   ✅ Created directory: {dir_path.relative_to(project_root)}")
        else:
            # print(f"   ℹ️ Directory already exists: {dir_path.relative_to(project_root)}")
            pass

        # Create __init__.py en directorios de módulos de Python
        if dir_name in ["agents", "tools", "utils"]:
            init_file = dir_path / "__init__.py"
            if not init_file.exists():
                init_file.touch()
                print(f"   ✅ Created file: {init_file.relative_to(project_root)}")
            else:
                # print(f"   ℹ️ File already exists: {init_file.relative_to(project_root)}")
                pass

if __name__ == "__main__":
    print("🔧 Ensuring project structure...")
    ensure_project_structure()
    print("🔧 Project structure verified.")

