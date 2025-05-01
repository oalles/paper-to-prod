import os
from datetime import datetime
from pathlib import Path
import uuid

def create_session_directory(base_dir: str = "workspace") -> str:
    """
    Creates a unique session directory under the given base directory.
    Returns the absolute path to the created session.
    Ensures the base directory exists.
    """
    base_path = Path(base_dir).resolve()
    base_path.mkdir(parents=True, exist_ok=True) # Ensure base workspace exists

    session_id = datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + str(uuid.uuid4())[:8]
    session_path = base_path / session_id
    session_path.mkdir(parents=True, exist_ok=True) # Create the unique session dir
    print(f"📁 Created new session directory: {session_path}")
    return str(session_path)

