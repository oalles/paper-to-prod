import os
import json

class SharedMemory:
    def __init__(self, session_path):
        self.memory_file = os.path.join(session_path, "intermediate", "shared_memory.json")
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump({}, f)

    def read(self):
        with open(self.memory_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def write(self, key, value):
        data = self.read()
        data[key] = value
        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get(self, key, default=None):
        data = self.read()
        return data.get(key, default)
