from ollama import Client

class OllamaClient:
    def __init__(self, model: str = "gemma3:12b", host: str = "http://localhost:11434"):
        try:
            self.model = model
            self.client = Client(host=host)
            # Test connection
            self.client.list()
            print(f"✅ Ollama client connected successfully to {host}")
        except ImportError:
            print("❌ Error: 'ollama' package not found. Please install it: pip install ollama")
            self.client = None
        except Exception as e:
            print(f"❌ Error connecting to Ollama at {host}: {e}")
            print("Ensure Ollama is running and the model is available (e.g., 'ollama run mistral').")
            self.client = None

    def generate(self, prompt: str, temperature: float = 0.7, max_tokens: int = 2048) -> str:
        if self.client is None:
            print("⚠️ Ollama client not available. Returning dummy response.")
            return f"Dummy response for: {prompt[:50]}..."

        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                options={
                    "temperature": temperature,
                    "num_predict": max_tokens # Renamed from max_tokens for ollama library
                }
            )
            return response["response"]
        except Exception as e:
            print(f"❌ Error generating response from Ollama: {e}")
            return f"Error generating response for: {prompt[:50]}..."

