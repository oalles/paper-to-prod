# Specify the Python executable path
PYTHON := python3  # or python, depending on your system

VENV_DIR := venv
VENV_ACTIVATE := . $(VENV_DIR)/bin/activate
PYTHON_VENV := $(VENV_DIR)/bin/python3
PIP_VENV := $(VENV_DIR)/bin/pip3

# Variables por defecto (puedes sobreescribirlas al invocar make)
LLM ?= ollama
LOG_SYSTEM ?= local
PROMPT ?= Resume y genera un MVP del siguiente paper
PAPER ?= /home/omar/Documentos/AriadnaGrid/Estudiar/Connectivity/VIP_Phase-topology-identification-in-low-volta.pdf
DAYS ?= 30

run:
	$(VENV_ACTIVATE) && $(PYTHON_VENV) cli.py "$(PROMPT)" "$(PAPER)" --llm $(LLM) --log-system $(LOG_SYSTEM)

run-crew:
	$(VENV_ACTIVATE) && $(PYTHON_VENV) cli.py "$(PROMPT)" "$(PAPER)" --crew --llm $(LLM) --log-system $(LOG_SYSTEM)

debug-file:
	@echo "Verificando archivo: $(PAPER)"
	@if [ -f "$(PAPER)" ]; then \
		echo "✅ El archivo existe"; \
	else \
		echo "❌ El archivo NO existe"; \
	fi
	@file "$(PAPER)" 2>/dev/null || echo "❌ Error al inspeccionar el archivo"

clean:
	rm -rf workspace/* sessions/*

install:
	$(PYTHON_VENV) -m pip install -r requirements.txt

setup:
	$(PYTHON_VENV) utils/setup.py

test:
	$(VENV_ACTIVATE) && $(PYTHON_VENV) -m pytest

lint:
	$(VENV_ACTIVATE) && $(PYTHON_VENV) -m ruff .

test-ollama:
	$(VENV_ACTIVATE) && $(PYTHON_VENV) -c "from tools.ollama_client import OllamaClient; client = OllamaClient(); print(client.generate('Hello, are you working?'))"

venv:
	python3 -m venv $(VENV_DIR)

all: venv setup install
