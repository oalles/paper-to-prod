class OpenAILLM:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model

    def generate(self, prompt, **kwargs):
        # Aquí deberías integrar la llamada real a OpenAI
        # Por ahora, placeholder
        return f"Respuesta OpenAI ({self.model}): {prompt[:40]}..."
