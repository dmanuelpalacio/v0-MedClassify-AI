"""
Configuración central para el proyecto de clasificación médica
"""
import os
from pathlib import Path

# Rutas del proyecto
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Crear directorios si no existen
for dir_path in [DATA_DIR, MODELS_DIR, OUTPUTS_DIR, REPORTS_DIR]:
    dir_path.mkdir(exist_ok=True)

# Configuración del modelo
MODEL_CONFIG = {
    "tfidf": {
        "ngram_range": (1, 2),
        "min_df": 2,
        "max_features": 20000,
        "stop_words": None
    },
    "classifier": {
        "max_iter": 300,
        "class_weight": "balanced",
        "random_state": 42
    },
    "split": {
        "test_size": 0.2,
        "random_state": 42
    }
}

# Dominios médicos objetivo
MEDICAL_DOMAINS = [
    "Cardiovascular",
    "Neurológico", 
    "Hepatorrenal",
    "Oncológico"
]

# Configuración de evaluación
EVALUATION_METRICS = [
    "f1_weighted",
    "f1_micro", 
    "f1_macro",
    "precision_weighted",
    "recall_weighted",
    "hamming_loss",
    "exact_match"
]
