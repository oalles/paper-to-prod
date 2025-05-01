import os

def get_llm():
    llm_backend = os.environ.get("P2P_LLM_BACKEND", "ollama").lower()
    if llm_backend == "ollama":
        from .ollama_client import OllamaLLM
        return OllamaLLM()
    elif llm_backend == "openai":
        from .openai_client import OpenAILLM
        return OpenAILLM()
    elif llm_backend == "huggingface":
        from .huggingface_client import HuggingFaceLLM
        return HuggingFaceLLM()
    else:
        raise ValueError(f"LLM backend no soportado: {llm_backend}")

