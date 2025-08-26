"""
Modelo Baseline: TF-IDF + Logistic Regression
Implementación del modelo baseline requerido por la convocatoria
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
from sklearn.metrics import (
    f1_score, accuracy_score, precision_score, recall_score,
    classification_report, confusion_matrix, hamming_loss,
    roc_auc_score, roc_curve
)
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import json

class BaselineTFIDFClassifier:
    """
    Clasificador baseline usando TF-IDF + Logistic Regression
    """
    
    def __init__(self, max_features=10000, ngram_range=(1, 2)):
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.vectorizer = None
        self.classifier = None
        self.label_encoder = None
        self.classes_ = None
        self.training_history = {}
        
    def preprocess_text(self, title, abstract):
        """
        Combina título y abstract con ponderación
        """
        # Dar más peso al título (3x) que al abstract
        combined_text = f"{title} {title} {title} {abstract}"
        return combined_text.lower().strip()
    
    def fit(self, train_df, val_df=None):
        """
        Entrena el modelo baseline
        """
        print("Iniciando entrenamiento del modelo baseline TF-IDF...")
        start_time = datetime.now()
        
        # Preparar textos
        X_train = [
            self.preprocess_text(row['title'], row['abstract']) 
            for _, row in train_df.iterrows()
        ]
        y_train = train_df['group'].values
        
        # Configurar vectorizador TF-IDF
        self.vectorizer = TfidfVectorizer(
            max_features=self.max_features,
            ngram_range=self.ngram_range,
            stop_words='english',
            lowercase=True,
            strip_accents='unicode',
            min_df=2,
            max_df=0.95
        )
        
        # Vectorizar textos
        print("Vectorizando textos con TF-IDF...")
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        
        # Configurar clasificador
        self.label_encoder = LabelEncoder()
        y_train_encoded = self.label_encoder.fit_transform(y_train)
        self.classes_ = self.label_encoder.classes_
        
        # Entrenar clasificador One-vs-Rest
        self.classifier = OneVsRestClassifier(
            LogisticRegression(
                random_state=42,
                max_iter=1000,
                class_weight='balanced'
            )
        )
        
        print("Entrenando clasificador...")
        self.classifier.fit(X_train_tfidf, y_train_encoded)
        
        # Evaluar en validación si está disponible
        if val_df is not None:
            val_metrics = self.evaluate(val_df)
            self.training_history['validation_metrics'] = val_metrics
        
        training_time = (datetime.now() - start_time).total_seconds()
        self.training_history['training_time'] = training_time
        self.training_history['train_samples'] = len(train_df)
        
        print(f"Entrenamiento completado en {training_time:.2f} segundos")
        return self
    
    def predict(self, test_df):
        """
        Realiza predicciones
        """
        X_test = [
            self.preprocess_text(row['title'], row['abstract']) 
            for _, row in test_df.iterrows()
        ]
        
        X_test_tfidf = self.vectorizer.transform(X_test)
        y_pred_encoded = self.classifier.predict(X_test_tfidf)
        y_pred = self.label_encoder.inverse_transform(y_pred_encoded)
        
        return y_pred
    
    def predict_proba(self, test_df):
        """
        Realiza predicciones con probabilidades
        """
        X_test = [
            self.preprocess_text(row['title'], row['abstract']) 
            for _, row in test_df.iterrows()
        ]
        
        X_test_tfidf = self.vectorizer.transform(X_test)
        y_proba = self.classifier.predict_proba(X_test_tfidf)
        
        return y_proba
    
    def evaluate(self, test_df):
        """
        Evaluación completa del modelo
        """
        y_true = test_df['group'].values
        y_pred = self.predict(test_df)
        y_proba = self.predict_proba(test_df)
        
        # Métricas principales
        metrics = {
            'f1_weighted': f1_score(y_true, y_pred, average='weighted'),
            'f1_macro': f1_score(y_true, y_pred, average='macro'),
            'f1_micro': f1_score(y_true, y_pred, average='micro'),
            'accuracy': accuracy_score(y_true, y_pred),
            'precision_weighted': precision_score(y_true, y_pred, average='weighted'),
            'recall_weighted': recall_score(y_true, y_pred, average='weighted'),
            'hamming_loss': hamming_loss(
                self.label_encoder.transform(y_true).reshape(-1, 1),
                self.label_encoder.transform(y_pred).reshape(-1, 1)
            )
        }
        
        # Exact Match (para multietiqueta)
        exact_match = np.mean(y_true == y_pred)
        metrics['exact_match'] = exact_match
        
        # ROC-AUC por clase
        y_true_encoded = self.label_encoder.transform(y_true)
        try:
            # Para clasificación multiclase, usar ovr
            roc_auc = roc_auc_score(
                y_true_encoded, y_proba, 
                multi_class='ovr', average='weighted'
            )
            metrics['roc_auc_weighted'] = roc_auc
        except:
            metrics['roc_auc_weighted'] = 0.0
        
        # Métricas por clase
        class_report = classification_report(
            y_true, y_pred, 
            target_names=self.classes_,
            output_dict=True
        )
        metrics['per_class_metrics'] = class_report
        
        # Matriz de confusión
        cm = confusion_matrix(y_true, y_pred, labels=self.classes_)
        metrics['confusion_matrix'] = cm.tolist()
        
        return metrics
    
    def save_model(self, filepath):
        """
        Guarda el modelo entrenado
        """
        model_data = {
            'vectorizer': self.vectorizer,
            'classifier': self.classifier,
            'label_encoder': self.label_encoder,
            'classes_': self.classes_,
            'training_history': self.training_history,
            'max_features': self.max_features,
            'ngram_range': self.ngram_range
        }
        joblib.dump(model_data, filepath)
        print(f"Modelo guardado en: {filepath}")
    
    def load_model(self, filepath):
        """
        Carga un modelo entrenado
        """
        model_data = joblib.load(filepath)
        self.vectorizer = model_data['vectorizer']
        self.classifier = model_data['classifier']
        self.label_encoder = model_data['label_encoder']
        self.classes_ = model_data['classes_']
        self.training_history = model_data['training_history']
        self.max_features = model_data['max_features']
        self.ngram_range = model_data['ngram_range']
        print(f"Modelo cargado desde: {filepath}")
        return self

def train_baseline_model():
    """
    Función principal para entrenar el modelo baseline
    """
    # Cargar datos
    print("Cargando dataset oficial...")
    train_df = pd.read_csv('data/train_split.csv')
    val_df = pd.read_csv('data/val_split.csv')
    test_df = pd.read_csv('data/test_split.csv')
    
    print(f"Datos cargados:")
    print(f"- Entrenamiento: {len(train_df)} muestras")
    print(f"- Validación: {len(val_df)} muestras")
    print(f"- Prueba: {len(test_df)} muestras")
    
    # Entrenar modelo
    model = BaselineTFIDFClassifier(max_features=10000, ngram_range=(1, 2))
    model.fit(train_df, val_df)
    
    # Evaluar en conjunto de prueba
    print("\nEvaluando modelo en conjunto de prueba...")
    test_metrics = model.evaluate(test_df)
    
    # Mostrar resultados
    print(f"\n=== RESULTADOS DEL MODELO BASELINE ===")
    print(f"F1-Score Weighted: {test_metrics['f1_weighted']:.4f}")
    print(f"Accuracy: {test_metrics['accuracy']:.4f}")
    print(f"Precision Weighted: {test_metrics['precision_weighted']:.4f}")
    print(f"Recall Weighted: {test_metrics['recall_weighted']:.4f}")
    print(f"Exact Match: {test_metrics['exact_match']:.4f}")
    print(f"Hamming Loss: {test_metrics['hamming_loss']:.4f}")
    print(f"ROC-AUC Weighted: {test_metrics['roc_auc_weighted']:.4f}")
    
    # Guardar modelo y resultados
    model.save_model('models/baseline_tfidf_model.joblib')
    
    with open('results/baseline_results.json', 'w') as f:
        # Convertir numpy arrays a listas para JSON
        test_metrics_json = test_metrics.copy()
        if 'confusion_matrix' in test_metrics_json:
            test_metrics_json['confusion_matrix'] = test_metrics['confusion_matrix']
        json.dump(test_metrics_json, f, indent=2, default=str)
    
    return model, test_metrics

if __name__ == "__main__":
    model, metrics = train_baseline_model()
