from elasticsearch import Elasticsearch
from datetime import datetime
from main import main

# Configura Elasticsearch (ajusta el host según tu entorno)
es = Elasticsearch("http://localhost:9200")

def elastic_log_hook(log_entry, level):
    doc = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "message": log_entry,
        "source": "paper-to-prod"
    }
    es.index(index="paper_to_prod_logs", document=doc)

if __name__ == "__main__":
    prompt = "Resume y genera un MVP del siguiente paper."
    paper_path = "tests/sample.pdf"
    main(prompt, paper_path, use_crew=True, external_log_hook=elastic_log_hook)
