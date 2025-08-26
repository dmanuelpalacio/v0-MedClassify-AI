"""
Clasificador multietiqueta para literatura médica
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import (
    f1_score, precision_score, recall_score, 
    hamming_loss, accuracy_score, multilabel_confusion_matrix
)
import joblib
from typing import Dict, List, Tuple, Any
import matplotlib.pyplot as plt
import seaborn as sns

from .preprocessing import MedicalTextPreprocessor
from .config import MODEL_CONFIG, MEDICAL_DOMAINS

class MedicalLiteratureClassifier:
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or MODEL_CONFIG
        self.preprocessor = MedicalTextPreprocessor()
        self.vectorizer = None
        self.classifier = None
        self.label_binarizer = None
        self.is_trained = False
        
    def prepare_data(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Prepara datos para entrenamiento"""
        # Preprocesar texto
        df_processed = self.preprocessor.process_dataframe(df)
        
        # Preparar etiquetas
        if "labels" in df_processed.columns:
            df_processed["labels"] = df_processed["labels"].apply(
                lambda x: self.preprocessor.parse_labels(str(x))
            )
            
            # Binarizar etiquetas
            self.label_binarizer = MultiLabelBinarizer()
            Y = self.label_binarizer.fit_transform(df_processed["labels"])
        else:
            Y = None
        
        # Vectorizar texto
        if self.vectorizer is None:
            self.vectorizer = TfidfVectorizer(**self.config["tfidf"])
            X = self.vectorizer.fit_transform(df_processed["text"])
        else:
            X = self.vectorizer.transform(df_processed["text"])
            
        return X, Y
    
    def train(self, df: pd.DataFrame) -> Dict[str, float]:
        """Entrena el modelo"""
        X, Y = self.prepare_data(df)
        
        # Split train/test
        X_train, X_test, y_train, y_test = train_test_split(
            X, Y, **self.config["split"]
        )
        
        # Entrenar clasificador
        self.classifier = OneVsRestClassifier(
            LogisticRegression(**self.config["classifier"])
        )
        self.classifier.fit(X_train, y_train)
        self.is_trained = True
        
        # Evaluar
        metrics = self.evaluate(X_test, y_test)
        return metrics
    
    def predict(self, texts: List[str]) -> List[List[str]]:
        """Predice etiquetas para textos"""
        if not self.is_trained:
            raise ValueError("El modelo debe ser entrenado primero")
            
        # Crear DataFrame temporal
        df_temp = pd.DataFrame({"text": texts})
        X, _ = self.prepare_data(df_temp)
        
        # Predecir
        y_pred = self.classifier.predict(X)
        
        # Convertir a etiquetas
        predictions = self.label_binarizer.inverse_transform(y_pred)
        return [list(pred) for pred in predictions]
    
    def predict_proba(self, texts: List[str]) -> List[Dict[str, float]]:
        """Predice probabilidades para textos"""
        if not self.is_trained:
            raise ValueError("El modelo debe ser entrenado primero")
            
        # Crear DataFrame temporal
        df_temp = pd.DataFrame({"text": texts})
        X, _ = self.prepare_data(df_temp)
        
        # Predecir probabilidades
        y_proba = self.classifier.predict_proba(X)
        
        # Convertir a diccionarios
        results = []
        for i in range(len(texts)):
            proba_dict = {}
            for j, label in enumerate(self.label_binarizer.classes_):
                proba_dict[label] = float(y_proba[i][j])
            results.append(proba_dict)
            
        return results
    
    def evaluate(self, X_test, y_test) -> Dict[str, float]:
        """Evalúa el modelo"""
        y_pred = self.classifier.predict(X_test)
        
        metrics = {
            "f1_weighted": f1_score(y_test, y_pred, average="weighted"),
            "f1_micro": f1_score(y_test, y_pred, average="micro"),
            "f1_macro": f1_score(y_test, y_pred, average="macro"),
            "precision_weighted": precision_score(y_test, y_pred, average="weighted"),
            "recall_weighted": recall_score(y_test, y_pred, average="weighted"),
            "hamming_loss": hamming_loss(y_test, y_pred),
            "exact_match": accuracy_score(y_test, y_pred)
        }
        
        return metrics
    
    def plot_confusion_matrices(self, X_test, y_test, save_path: str = None):
        """Genera matrices de confusión por clase"""
        y_pred = self.classifier.predict(X_test)
        cm = multilabel_confusion_matrix(y_test, y_pred)
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.ravel()
        
        for idx, label in enumerate(self.label_binarizer.classes_):
            if idx < len(axes):
                sns.heatmap(
                    cm[idx], 
                    annot=True, 
                    fmt="d", 
                    cmap="Blues",
                    xticklabels=["No", "Sí"], 
                    yticklabels=["No", "Sí"],
                    ax=axes[idx]
                )
                axes[idx].set_title(f"Matriz de confusión - {label}")
                axes[idx].set_ylabel("Verdadero")
                axes[idx].set_xlabel("Predicho")
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def save_model(self, path: str):
        """Guarda el modelo entrenado"""
        if not self.is_trained:
            raise ValueError("El modelo debe ser entrenado primero")
            
        model_data = {
            "vectorizer": self.vectorizer,
            "classifier": self.classifier,
            "label_binarizer": self.label_binarizer,
            "config": self.config
        }
        
        joblib.dump(model_data, path)
    
    def load_model(self, path: str):
        """Carga un modelo entrenado"""
        model_data = joblib.load(path)
        
        self.vectorizer = model_data["vectorizer"]
        self.classifier = model_data["classifier"]
        self.label_binarizer = model_data["label_binarizer"]
        self.config = model_data["config"]
        self.is_trained = True
