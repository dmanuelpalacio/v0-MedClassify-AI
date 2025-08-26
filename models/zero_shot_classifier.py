"""
Zero-shot Classification Model para MedClassify AI
Implementación de clasificación sin entrenamiento usando modelos pre-entrenados
"""

import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import numpy as np
from typing import Dict, List, Tuple
import logging

class ZeroShotMedicalClassifier:
    """
    Clasificador zero-shot para literatura médica usando modelos pre-entrenados
    """
    
    def __init__(self, model_name: str = "facebook/bart-large-mnli"):
        """
        Inicializa el clasificador zero-shot
        
        Args:
            model_name: Nombre del modelo pre-entrenado a usar
        """
        self.model_name = model_name
        self.domains = [
            "Cardiovascular", 
            "Neurológico", 
            "Hepatorrenal", 
            "Oncológico"
        ]
        
        # Hipótesis detalladas para cada dominio médico
        self.domain_hypotheses = {
            "Cardiovascular": [
                "This text is about cardiovascular diseases and heart conditions",
                "This article discusses cardiac disorders and circulatory system",
                "This research focuses on heart disease and vascular conditions"
            ],
            "Neurológico": [
                "This text is about neurological disorders and brain conditions",
                "This article discusses nervous system diseases and neurology",
                "This research focuses on brain disorders and neurological conditions"
            ],
            "Hepatorrenal": [
                "This text is about liver and kidney diseases",
                "This article discusses hepatic and renal disorders",
                "This research focuses on liver and kidney conditions"
            ],
            "Oncológico": [
                "This text is about cancer and oncological conditions",
                "This article discusses tumors and malignant diseases",
                "This research focuses on cancer treatment and oncology"
            ]
        }
        
        self.classifier = None
        self._load_model()
    
    def _load_model(self):
        """Carga el modelo zero-shot"""
        try:
            self.classifier = pipeline(
                "zero-shot-classification",
                model=self.model_name,
                device=0 if torch.cuda.is_available() else -1
            )
            logging.info(f"Modelo zero-shot cargado: {self.model_name}")
        except Exception as e:
            logging.error(f"Error cargando modelo zero-shot: {e}")
            raise
    
    def classify_single(self, title: str, abstract: str) -> Dict[str, float]:
        """
        Clasifica un artículo individual usando zero-shot
        
        Args:
            title: Título del artículo
            abstract: Resumen del artículo
            
        Returns:
            Dict con probabilidades por dominio
        """
        # Combinar título y abstract
        text = f"{title}. {abstract}"
        
        # Clasificar con múltiples hipótesis por dominio
        domain_scores = {}
        
        for domain in self.domains:
            hypotheses = self.domain_hypotheses[domain]
            scores = []
            
            for hypothesis in hypotheses:
                result = self.classifier(text, [hypothesis])
                scores.append(result['scores'][0])
            
            # Promedio de las puntuaciones de las hipótesis
            domain_scores[domain] = np.mean(scores)
        
        return domain_scores
    
    def classify_batch(self, articles: List[Tuple[str, str]]) -> List[Dict[str, float]]:
        """
        Clasifica múltiples artículos
        
        Args:
            articles: Lista de tuplas (título, abstract)
            
        Returns:
            Lista de diccionarios con probabilidades por dominio
        """
        results = []
        for title, abstract in articles:
            result = self.classify_single(title, abstract)
            results.append(result)
        
        return results
    
    def get_predictions(self, scores: Dict[str, float], threshold: float = 0.5) -> List[str]:
        """
        Convierte puntuaciones en predicciones multi-etiqueta
        
        Args:
            scores: Diccionario con puntuaciones por dominio
            threshold: Umbral para clasificación positiva
            
        Returns:
            Lista de dominios predichos
        """
        predictions = []
        for domain, score in scores.items():
            if score >= threshold:
                predictions.append(domain)
        
        # Si no hay predicciones, tomar la de mayor puntuación
        if not predictions:
            best_domain = max(scores.items(), key=lambda x: x[1])[0]
            predictions.append(best_domain)
        
        return predictions
    
    def evaluate_performance(self, test_data: List[Tuple[str, str, List[str]]]) -> Dict[str, float]:
        """
        Evalúa el rendimiento del modelo zero-shot
        
        Args:
            test_data: Lista de tuplas (título, abstract, etiquetas_verdaderas)
            
        Returns:
            Diccionario con métricas de evaluación
        """
        all_predictions = []
        all_true_labels = []
        
        for title, abstract, true_labels in test_data:
            scores = self.classify_single(title, abstract)
            predictions = self.get_predictions(scores)
            
            all_predictions.append(predictions)
            all_true_labels.append(true_labels)
        
        # Calcular métricas
        from sklearn.metrics import classification_report, multilabel_confusion_matrix
        from sklearn.preprocessing import MultiLabelBinarizer
        
        mlb = MultiLabelBinarizer(classes=self.domains)
        y_true = mlb.fit_transform(all_true_labels)
        y_pred = mlb.transform(all_predictions)
        
        # Métricas por clase
        report = classification_report(y_true, y_pred, target_names=self.domains, output_dict=True)
        
        return {
            'macro_f1': report['macro avg']['f1-score'],
            'micro_f1': report['micro avg']['f1-score'],
            'weighted_f1': report['weighted avg']['f1-score'],
            'per_class_metrics': {domain: report[domain] for domain in self.domains}
        }

# Función de utilidad para comparar con otros modelos
def compare_with_baseline(zero_shot_results: Dict, baseline_results: Dict) -> Dict:
    """
    Compara resultados del modelo zero-shot con el baseline
    
    Args:
        zero_shot_results: Resultados del modelo zero-shot
        baseline_results: Resultados del modelo baseline
        
    Returns:
        Diccionario con comparación de métricas
    """
    comparison = {
        'zero_shot_f1': zero_shot_results['weighted_f1'],
        'baseline_f1': baseline_results['weighted_f1'],
        'improvement': zero_shot_results['weighted_f1'] - baseline_results['weighted_f1'],
        'relative_improvement': ((zero_shot_results['weighted_f1'] - baseline_results['weighted_f1']) / baseline_results['weighted_f1']) * 100
    }
    
    return comparison
