import sentry_sdk
from main import main

# Inicializa Sentry (reemplaza con tu DSN real)
sentry_sdk.init(
    dsn="https://<your-public-key>@sentry.io/<your-project-id>",
    traces_sample_rate=1.0
)

def sentry_log_hook(log_entry, level):
    if level == "ERROR":
        sentry_sdk.capture_message(log_entry, level="error")
    elif level == "WARNING":
        sentry_sdk.capture_message(log_entry, level="warning")
    else:
        sentry_sdk.capture_message(log_entry, level="info")

if __name__ == "__main__":
    prompt = "Resume y genera un MVP del siguiente paper."
    paper_path = "tests/sample.pdf"
    main(prompt, paper_path, use_crew=True, external_log_hook=sentry_log_hook)
