# Specify the Python executable path
PYTHON := python3  # or python, depending on your system

VENV_DIR := venv
VENV_ACTIVATE := . $(VENV_DIR)/bin/activate
PYTHON_VENV := $(VENV_DIR)/bin/python3
PIP_VENV := $(VENV_DIR)/bin/pip3

run:
	$(VENV_ACTIVATE) && $(PYTHON_VENV) main.py "$(PROMPT)" "$(PAPER)"

debug-file:
	@echo "Verificando archivo: $(PAPER)"
	@if [ -f "$(PAPER)" ]; then \
		echo "✅ El archivo existe"; \
	else \
		echo "❌ El archivo NO existe"; \
	fi
	@file "$(PAPER)" 2>/dev/null || echo "❌ Error al inspeccionar el archivo"

clean:
	rm -rf workspace/*

install:
	$(PYTHON_VENV) -m pip install -r requirements.txt

# Updated setup target to use the python script
setup:
	$(PYTHON_VENV) utils/setup.py

test-ollama:
	$(VENV_ACTIVATE) && $(PYTHON_VENV) -c "from tools.ollama_client import OllamaClient; client = OllamaClient(); print(client.generate('Hello, are you working?'))"

venv:
	python3 -m venv $(VENV_DIR)

all: venv setup install

