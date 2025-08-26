# Makefile para MedClassify AI - TechSphere Challenge 2025

.PHONY: help setup install train eval predict app clean test lint format

# Variables
PYTHON := python3
PIP := pip3
VENV := venv
DATA_FILE := data/challenge_data.csv
MODEL_FILE := models/trained_model.joblib

help: ## Mostrar ayuda
	@echo "MedClassify AI - Sistema de Clasificación de Literatura Médica"
	@echo "TechSphere AI Challenge 2025"
	@echo ""
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup: ## Crear entorno virtual e instalar dependencias
	$(PYTHON) -m venv $(VENV)
	./$(VENV)/bin/pip install --upgrade pip
	./$(VENV)/bin/pip install -r requirements.txt
	@echo "✅ Entorno configurado. Actívalo con: source $(VENV)/bin/activate"

install: ## Instalar dependencias en entorno actual
	$(PIP) install -r requirements.txt
	@echo "✅ Dependencias instaladas"

train: ## Entrenar modelo con datos por defecto
	$(PYTHON) cli.py train --data $(DATA_FILE) --save $(MODEL_FILE)

train-custom: ## Entrenar modelo con archivo personalizado (usar DATA=archivo.csv)
	$(PYTHON) cli.py train --data $(DATA) --save $(MODEL_FILE)

eval: ## Evaluar modelo entrenado
	$(PYTHON) cli.py eval --data $(DATA_FILE) --model $(MODEL_FILE)

predict: ## Predecir etiquetas (usar INPUT=archivo.csv OUTPUT=salida.csv)
	$(PYTHON) cli.py predict --input $(INPUT) --output $(OUTPUT) --model $(MODEL_FILE)

classify: ## Clasificar texto individual (usar TITLE="..." ABSTRACT="...")
	$(PYTHON) cli.py classify --title "$(TITLE)" --abstract "$(ABSTRACT)" --model $(MODEL_FILE)

app: ## Lanzar aplicación Streamlit
	streamlit run app_streamlit.py

app-dev: ## Lanzar aplicación en modo desarrollo
	streamlit run app_streamlit.py --server.runOnSave true

test: ## Ejecutar tests
	$(PYTHON) -m pytest tests/ -v

lint: ## Verificar código con flake8
	flake8 src/ tests/ --max-line-length=100

format: ## Formatear código con black
	black src/ tests/ --line-length=100

clean: ## Limpiar archivos temporales
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/

# Comandos de ejemplo
example-train: ## Ejemplo: entrenar modelo
	@echo "Ejemplo de entrenamiento:"
	@echo "make train"
	@echo "# o con archivo personalizado:"
	@echo "make train-custom DATA=mi_dataset.csv"

example-predict: ## Ejemplo: predecir por lotes
	@echo "Ejemplo de predicción por lotes:"
	@echo "make predict INPUT=articulos.csv OUTPUT=resultados.csv"

example-classify: ## Ejemplo: clasificar texto individual
	@echo "Ejemplo de clasificación individual:"
	@echo 'make classify TITLE="Cardiovascular Risk Assessment" ABSTRACT="This study evaluates risk factors..."'

# Pipeline completo
pipeline: install train eval ## Ejecutar pipeline completo: instalar, entrenar y evaluar
	@echo "✅ Pipeline completo ejecutado"

# Desarrollo
dev-setup: setup ## Configurar entorno de desarrollo
	./$(VENV)/bin/pip install -r requirements-dev.txt
	@echo "✅ Entorno de desarrollo configurado"

# Documentación
docs: ## Generar documentación
	@echo "📚 Generando documentación..."
	@echo "Estructura del proyecto:"
	tree -I '__pycache__|*.pyc|$(VENV)' .

# Información del sistema
info: ## Mostrar información del sistema
	@echo "🔍 Información del sistema:"
	@echo "Python: $(shell $(PYTHON) --version)"
	@echo "Pip: $(shell $(PIP) --version)"
	@echo "Directorio actual: $(shell pwd)"
	@echo "Archivos de datos disponibles:"
	@ls -la data/ 2>/dev/null || echo "  Directorio data/ no encontrado"
	@echo "Modelos disponibles:"
	@ls -la models/ 2>/dev/null || echo "  Directorio models/ no encontrado"
