import os
import uuid
from datetime import datetime

def create_session_directory(base_dir="sessions"):
    session_id = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}"
    session_path = os.path.join(base_dir, session_id)
    os.makedirs(os.path.join(session_path, "intermediate"), exist_ok=True)
    os.makedirs(os.path.join(session_path, "output", "implementation"), exist_ok=True)
    return session_path
