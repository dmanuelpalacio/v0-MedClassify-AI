"""
Modelo Híbrido: BioBERT + TF-IDF + Ensemble
Implementación del modelo híbrido requerido por la convocatoria
"""

import pandas as pd
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn as nn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import f1_score, accuracy_score, classification_report
import joblib
from datetime import datetime
import json

class BioBERTEmbedder:
    """
    Extractor de embeddings usando BioBERT
    """
    
    def __init__(self, model_name='dmis-lab/biobert-base-cased-v1.1'):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        
    def get_embeddings(self, texts, batch_size=16):
        """
        Extrae embeddings de BioBERT para una lista de textos
        """
        self.model.eval()
        embeddings = []
        
        with torch.no_grad():
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i+batch_size]
                
                # Tokenizar
                inputs = self.tokenizer(
                    batch_texts,
                    padding=True,
                    truncation=True,
                    max_length=512,
                    return_tensors='pt'
                ).to(self.device)
                
                # Obtener embeddings
                outputs = self.model(**inputs)
                # Usar el token [CLS] como representación de la secuencia
                cls_embeddings = outputs.last_hidden_state[:, 0, :]
                embeddings.append(cls_embeddings.cpu().numpy())
        
        return np.vstack(embeddings)

class HybridBioBERTClassifier:
    """
    Clasificador híbrido que combina BioBERT y TF-IDF
    """
    
    def __init__(self, use_biobert=True, use_tfidf=True):
        self.use_biobert = use_biobert
        self.use_tfidf = use_tfidf
        self.biobert_embedder = None
        self.tfidf_vectorizer = None
        self.classifier = None
        self.label_encoder = None
        self.classes_ = None
        self.training_history = {}
        
    def preprocess_text(self, title, abstract):
        """
        Combina título y abstract
        """
        return f"{title} [SEP] {abstract}".strip()
    
    def fit(self, train_df, val_df=None):
        """
        Entrena el modelo híbrido
        """
        print("Iniciando entrenamiento del modelo híbrido BioBERT...")
        start_time = datetime.now()
        
        # Preparar textos
        X_train_texts = [
            self.preprocess_text(row['title'], row['abstract']) 
            for _, row in train_df.iterrows()
        ]
        y_train = train_df['group'].values
        
        # Configurar label encoder
        self.label_encoder = LabelEncoder()
        y_train_encoded = self.label_encoder.fit_transform(y_train)
        self.classes_ = self.label_encoder.classes_
        
        # Extraer características
        features_list = []
        
        if self.use_biobert:
            print("Extrayendo embeddings de BioBERT...")
            self.biobert_embedder = BioBERTEmbedder()
            biobert_features = self.biobert_embedder.get_embeddings(X_train_texts)
            features_list.append(biobert_features)
            print(f"BioBERT embeddings shape: {biobert_features.shape}")
        
        if self.use_tfidf:
            print("Extrayendo características TF-IDF...")
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=5000,
                ngram_range=(1, 2),
                stop_words='english',
                min_df=2,
                max_df=0.95
            )
            tfidf_features = self.tfidf_vectorizer.fit_transform(X_train_texts).toarray()
            features_list.append(tfidf_features)
            print(f"TF-IDF features shape: {tfidf_features.shape}")
        
        # Combinar características
        if len(features_list) > 1:
            X_train_combined = np.hstack(features_list)
        else:
            X_train_combined = features_list[0]
        
        print(f"Características combinadas shape: {X_train_combined.shape}")
        
        # Entrenar clasificador
        print("Entrenando clasificador híbrido...")
        self.classifier = LogisticRegression(
            random_state=42,
            max_iter=1000,
            class_weight='balanced'
        )
        
        self.classifier.fit(X_train_combined, y_train_encoded)
        
        # Evaluar en validación si está disponible
        if val_df is not None:
            val_metrics = self.evaluate(val_df)
            self.training_history['validation_metrics'] = val_metrics
        
        training_time = (datetime.now() - start_time).total_seconds()
        self.training_history['training_time'] = training_time
        self.training_history['train_samples'] = len(train_df)
        
        print(f"Entrenamiento completado en {training_time:.2f} segundos")
        return self
    
    def _extract_features(self, test_df):
        """
        Extrae características para predicción
        """
        X_test_texts = [
            self.preprocess_text(row['title'], row['abstract']) 
            for _, row in test_df.iterrows()
        ]
        
        features_list = []
        
        if self.use_biobert and self.biobert_embedder:
            biobert_features = self.biobert_embedder.get_embeddings(X_test_texts)
            features_list.append(biobert_features)
        
        if self.use_tfidf and self.tfidf_vectorizer:
            tfidf_features = self.tfidf_vectorizer.transform(X_test_texts).toarray()
            features_list.append(tfidf_features)
        
        if len(features_list) > 1:
            return np.hstack(features_list)
        else:
            return features_list[0]
    
    def predict(self, test_df):
        """
        Realiza predicciones
        """
        X_test_combined = self._extract_features(test_df)
        y_pred_encoded = self.classifier.predict(X_test_combined)
        y_pred = self.label_encoder.inverse_transform(y_pred_encoded)
        return y_pred
    
    def predict_proba(self, test_df):
        """
        Realiza predicciones con probabilidades
        """
        X_test_combined = self._extract_features(test_df)
        y_proba = self.classifier.predict_proba(X_test_combined)
        return y_proba
    
    def evaluate(self, test_df):
        """
        Evaluación completa del modelo
        """
        y_true = test_df['group'].values
        y_pred = self.predict(test_df)
        
        metrics = {
            'f1_weighted': f1_score(y_true, y_pred, average='weighted'),
            'f1_macro': f1_score(y_true, y_pred, average='macro'),
            'accuracy': accuracy_score(y_true, y_pred),
            'exact_match': np.mean(y_true == y_pred)
        }
        
        # Reporte por clase
        class_report = classification_report(
            y_true, y_pred, 
            target_names=self.classes_,
            output_dict=True
        )
        metrics['per_class_metrics'] = class_report
        
        return metrics

def train_hybrid_model():
    """
    Función principal para entrenar el modelo híbrido
    """
    # Cargar datos
    print("Cargando dataset oficial...")
    train_df = pd.read_csv('data/train_split.csv')
    val_df = pd.read_csv('data/val_split.csv')
    test_df = pd.read_csv('data/test_split.csv')
    
    # Entrenar modelo híbrido
    model = HybridBioBERTClassifier(use_biobert=True, use_tfidf=True)
    model.fit(train_df, val_df)
    
    # Evaluar
    test_metrics = model.evaluate(test_df)
    
    print(f"\n=== RESULTADOS DEL MODELO HÍBRIDO ===")
    print(f"F1-Score Weighted: {test_metrics['f1_weighted']:.4f}")
    print(f"Accuracy: {test_metrics['accuracy']:.4f}")
    print(f"Exact Match: {test_metrics['exact_match']:.4f}")
    
    # Guardar resultados
    with open('results/hybrid_results.json', 'w') as f:
        json.dump(test_metrics, f, indent=2, default=str)
    
    return model, test_metrics

if __name__ == "__main__":
    model, metrics = train_hybrid_model()
