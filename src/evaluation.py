import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    f1_score, precision_score, recall_score, accuracy_score,
    classification_report, multilabel_confusion_matrix, hamming_loss
)
import pandas as pd

class ModelEvaluator:
    """
    Evaluador completo para el modelo de clasificación médica
    """
    
    def __init__(self, classes):
        self.classes = classes
    
    def calculate_metrics(self, y_true, y_pred, y_probs=None):
        """Calcula métricas completas"""
        
        metrics = {
            'weighted_f1': f1_score(y_true, y_pred, average='weighted'),
            'macro_f1': f1_score(y_true, y_pred, average='macro'),
            'micro_f1': f1_score(y_true, y_pred, average='micro'),
            'weighted_precision': precision_score(y_true, y_pred, average='weighted'),
            'weighted_recall': recall_score(y_true, y_pred, average='weighted'),
            'hamming_loss': hamming_loss(y_true, y_pred),
            'exact_match_ratio': accuracy_score(y_true, y_pred)
        }
        
        # Métricas por clase
        class_report = classification_report(
            y_true, y_pred, target_names=self.classes, output_dict=True
        )
        
        return metrics, class_report
    
    def plot_confusion_matrices(self, y_true, y_pred, save_path=None):
        """Genera matrices de confusión para cada clase"""
        
        cm_multilabel = multilabel_confusion_matrix(y_true, y_pred)
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.ravel()
        
        for i, (class_name, cm) in enumerate(zip(self.classes, cm_multilabel)):
            sns.heatmap(
                cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['No', 'Yes'], yticklabels=['No', 'Yes'],
                ax=axes[i]
            )
            axes[i].set_title(f'Matriz de Confusión - {class_name}')
            axes[i].set_xlabel('Predicción')
            axes[i].set_ylabel('Real')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
        
        return fig
    
    def plot_metrics_comparison(self, metrics_dict, save_path=None):
        """Visualiza comparación de métricas"""
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Métricas generales
        general_metrics = ['weighted_f1', 'macro_f1', 'micro_f1', 'weighted_precision', 'weighted_recall']
        values = [metrics_dict[metric] for metric in general_metrics]
        
        ax1.bar(general_metrics, values, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'])
        ax1.set_title('Métricas Generales del Modelo')
        ax1.set_ylabel('Score')
        ax1.set_ylim(0, 1)
        ax1.tick_params(axis='x', rotation=45)
        
        # Agregar valores en las barras
        for i, v in enumerate(values):
            ax1.text(i, v + 0.01, f'{v:.3f}', ha='center', va='bottom')
        
        # Métricas por clase (F1-Score)
        class_f1_scores = []
        for class_name in self.classes:
            class_f1_scores.append(metrics_dict.get(f'{class_name}_f1', 0))
        
        ax2.bar(self.classes, class_f1_scores, color=['#e74c3c', '#3498db', '#2ecc71', '#f39c12'])
        ax2.set_title('F1-Score por Clase Médica')
        ax2.set_ylabel('F1-Score')
        ax2.set_ylim(0, 1)
        ax2.tick_params(axis='x', rotation=45)
        
        # Agregar valores en las barras
        for i, v in enumerate(class_f1_scores):
            ax2.text(i, v + 0.01, f'{v:.3f}', ha='center', va='bottom')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
        
        return fig
    
    def generate_detailed_report(self, y_true, y_pred, y_probs, metrics, class_report):
        """Genera reporte detallado"""
        
        report = f"""
# REPORTE DE EVALUACIÓN - CLASIFICADOR MÉDICO

## Métricas Principales
- **F1-Score Ponderado (Métrica Principal)**: {metrics['weighted_f1']:.4f}
- **F1-Score Macro**: {metrics['macro_f1']:.4f}
- **F1-Score Micro**: {metrics['micro_f1']:.4f}
- **Precisión Ponderada**: {metrics['weighted_precision']:.4f}
- **Recall Ponderado**: {metrics['weighted_recall']:.4f}
- **Hamming Loss**: {metrics['hamming_loss']:.4f}
- **Exact Match Ratio**: {metrics['exact_match_ratio']:.4f}

## Métricas por Clase Médica
"""
        
        for class_name in self.classes:
            if class_name.lower() in class_report:
                class_metrics = class_report[class_name.lower()]
                report += f"""
### {class_name}
- Precisión: {class_metrics['precision']:.4f}
- Recall: {class_metrics['recall']:.4f}
- F1-Score: {class_metrics['f1-score']:.4f}
- Soporte: {class_metrics['support']}
"""
        
        return report
