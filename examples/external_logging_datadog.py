from datadog import initialize, api
from main import main

# Configura Datadog (reemplaza con tus credenciales reales)
options = {
    'api_key': 'TU_API_KEY',
    'app_key': 'TU_APP_KEY'
}
initialize(**options)

def datadog_log_hook(log_entry, level):
    # Envía el log como un evento a Datadog
    api.Event.create(
        title=f"Paper-to-Prod [{level}]",
        text=log_entry,
        alert_type=level.lower()
    )

if __name__ == "__main__":
    prompt = "Resume y genera un MVP del siguiente paper."
    paper_path = "tests/sample.pdf"
    main(prompt, paper_path, use_crew=True, external_log_hook=datadog_log_hook)
