from crewai import LLM

class OllamaLLM(LLM):
    def __init__(self, model="gemma3:12b"):
        self.model = model

    def generate(self, prompt, **kwargs):
        # Aquí se debe integrar la llamada real a Ollama
        # Por ahora, placeholder
        return "Respuesta generada por Ollama para: " + prompt
