import os
import requests

class HuggingFaceLLM:
    def __init__(self, model="google/flan-t5-small"):
        self.model = model
        self.api_token = os.environ.get("HF_API_TOKEN")
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model}"

    def generate(self, prompt, **kwargs):
        if not self.api_token:
            raise RuntimeError("Debes definir la variable de entorno HF_API_TOKEN para usar HuggingFace API.")
        headers = {"Authorization": f"Bearer {self.api_token}"}
        payload = {"inputs": prompt}
        response = requests.post(self.api_url, headers=headers, json=payload)
        if response.status_code != 200:
            raise RuntimeError(f"Error HuggingFace API: {response.status_code} {response.text}")
        result = response.json()
        # El resultado puede variar según el modelo
        if isinstance(result, list) and "generated_text" in result[0]:
            return result[0]["generated_text"]
        elif isinstance(result, dict) and "error" in result:
            raise RuntimeError(f"Error HuggingFace API: {result['error']}")
        else:
            # Fallback: devolver el resultado como string
            return str(result)
