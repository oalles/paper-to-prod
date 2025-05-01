import argparse
import os

# Cargar variables de entorno desde .env si existe, y advertir si no existe
from dotenv import load_dotenv, find_dotenv
dotenv_path = find_dotenv()
if dotenv_path:
    load_dotenv(dotenv_path)
    print(f"ℹ️  Archivo .env cargado desde: {dotenv_path}")
else:
    print("⚠️  Archivo .env no encontrado. Si necesitas variables de entorno, crea uno en la raíz del proyecto.")

from main import main

def get_log_hook(log_system):
    if log_system == "sentry":
        sentry_dsn = os.environ.get("SENTRY_DSN")
        if not sentry_dsn:
            print("❌ Debes definir la variable de entorno SENTRY_DSN para usar Sentry.")
            exit(1)
        import sentry_sdk
        sentry_sdk.init(
            dsn=sentry_dsn,
            traces_sample_rate=1.0
        )
        def sentry_log_hook(log_entry, level):
            if level == "ERROR":
                sentry_sdk.capture_message(log_entry, level="error")
            elif level == "WARNING":
                sentry_sdk.capture_message(log_entry, level="warning")
            else:
                sentry_sdk.capture_message(log_entry, level="info")
        return sentry_log_hook
    elif log_system == "datadog":
        api_key = os.environ.get("DATADOG_API_KEY")
        app_key = os.environ.get("DATADOG_APP_KEY")
        if not api_key or not app_key:
            print("❌ Debes definir DATADOG_API_KEY y DATADOG_APP_KEY para usar Datadog.")
            exit(1)
        from datadog import initialize, api
        options = {
            'api_key': api_key,
            'app_key': app_key
        }
        initialize(**options)
        def datadog_log_hook(log_entry, level):
            api.Event.create(
                title=f"Paper-to-Prod [{level}]",
                text=log_entry,
                alert_type=level.lower()
            )
        return datadog_log_hook
    elif log_system == "elastic":
        elastic_url = os.environ.get("ELASTIC_URL", "http://localhost:9200")
        try:
            from elasticsearch import Elasticsearch
            from datetime import datetime
            es = Elasticsearch(elastic_url)
            # Prueba de conexión
            if not es.ping():
                print(f"❌ No se pudo conectar a Elasticsearch en {elastic_url}.")
                exit(1)
        except Exception as e:
            print(f"❌ Error al inicializar Elasticsearch: {e}")
            exit(1)
        def elastic_log_hook(log_entry, level):
            doc = {
                "timestamp": datetime.utcnow().isoformat(),
                "level": level,
                "message": log_entry,
                "source": "paper-to-prod"
            }
            es.index(index="paper_to_prod_logs", document=doc)
        return elastic_log_hook
    else:
        return None

def main_cli():
    parser = argparse.ArgumentParser(
        description="Paper-to-Prod CrewAI CLI",
        epilog="Ejemplo: python cli.py \"Prompt\" paper.pdf --crew --llm huggingface --log-system sentry"
    )
    parser.add_argument("prompt", type=str, help="Prompt del usuario")
    parser.add_argument("paper_path", type=str, help="Ruta al archivo PDF del paper")
    parser.add_argument("--crew", action="store_true", help="Usar flujo CrewAI")
    parser.add_argument("--llm", type=str, choices=["ollama", "openai", "huggingface"], default="ollama", help="Backend LLM a utilizar")
    parser.add_argument("--log-system", type=str, choices=["local", "sentry", "datadog", "elastic"], default="local", help="Sistema de logging externo")
    args = parser.parse_args()

    # Validación de backend LLM
    if args.llm == "huggingface" and not os.environ.get("HF_API_TOKEN"):
        print("❌ Debes definir la variable de entorno HF_API_TOKEN para usar HuggingFace.")
        exit(1)
    if args.llm == "openai":
        print("⚠️  Recuerda configurar tus credenciales de OpenAI en llm/openai_client.py.")

    os.environ["P2P_LLM_BACKEND"] = args.llm
    log_hook = get_log_hook(args.log_system) if args.log_system != "local" else None

    # No crear ni pasar session_path aquí, main se encarga de todo
    main(args.prompt, args.paper_path, use_crew=args.crew, external_log_hook=log_hook)

if __name__ == "__main__":
    main_cli()
