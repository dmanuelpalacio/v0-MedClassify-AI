#!/usr/bin/env python3
"""
Evaluador principal para el AI + Data Challenge 2025
Carga un CSV con columnas title, abstract, group y genera predicciones con métricas
"""

import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from sklearn.preprocessing import MultiLabelBinarizer
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
import joblib
import os
from datetime import datetime

from src.multilabel_classifier import MedicalTextClassifier
from src.preprocessing import TextPreprocessor
from src.config import DOMAINS, MODEL_CONFIG

def load_test_data(csv_path):
    """Carga datos de prueba desde CSV"""
    try:
        df = pd.read_csv(csv_path)
        required_columns = ['title', 'abstract', 'group']
        
        if not all(col in df.columns for col in required_columns):
            raise ValueError(f"CSV debe contener columnas: {required_columns}")
        
        print(f"✅ Datos cargados: {len(df)} artículos")
        return df
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        return None

def evaluate_predictions(y_true, y_pred, domains=DOMAINS):
    """Evalúa predicciones y genera métricas completas"""
    
    # Convertir a formato binario para evaluación
    mlb = MultiLabelBinarizer(classes=domains)
    y_true_bin = mlb.fit_transform(y_true)
    y_pred_bin = mlb.transform(y_pred)
    
    # Métricas principales
    f1_weighted = f1_score(y_true_bin, y_pred_bin, average='weighted')
    f1_macro = f1_score(y_true_bin, y_pred_bin, average='macro')
    f1_micro = f1_score(y_true_bin, y_pred_bin, average='micro')
    
    # Reporte de clasificación
    report = classification_report(
        y_true_bin, y_pred_bin, 
        target_names=domains,
        output_dict=True,
        zero_division=0
    )
    
    # Matriz de confusión por dominio
    confusion_matrices = {}
    for i, domain in enumerate(domains):
        cm = confusion_matrix(y_true_bin[:, i], y_pred_bin[:, i])
        confusion_matrices[domain] = cm
    
    return {
        'f1_weighted': f1_weighted,
        'f1_macro': f1_macro,
        'f1_micro': f1_micro,
        'classification_report': report,
        'confusion_matrices': confusion_matrices
    }

def plot_confusion_matrices(confusion_matrices, save_path='results/confusion_matrices.png'):
    """Genera visualización de matrices de confusión"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    axes = axes.ravel()
    
    for i, (domain, cm) in enumerate(confusion_matrices.items()):
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[i])
        axes[i].set_title(f'Matriz de Confusión - {domain}')
        axes[i].set_xlabel('Predicción')
        axes[i].set_ylabel('Real')
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"✅ Matrices de confusión guardadas en: {save_path}")

def generate_results_report(metrics, save_path='results/evaluation_report.txt'):
    """Genera reporte detallado de resultados"""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write("="*60 + "\n")
        f.write("REPORTE DE EVALUACIÓN - AI + DATA CHALLENGE 2025\n")
        f.write("="*60 + "\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("MÉTRICAS PRINCIPALES:\n")
        f.write("-"*30 + "\n")
        f.write(f"F1-Score Ponderado (Principal): {metrics['f1_weighted']:.4f}\n")
        f.write(f"F1-Score Macro: {metrics['f1_macro']:.4f}\n")
        f.write(f"F1-Score Micro: {metrics['f1_micro']:.4f}\n\n")
        
        f.write("REPORTE POR DOMINIO:\n")
        f.write("-"*30 + "\n")
        for domain in DOMAINS:
            if domain in metrics['classification_report']:
                domain_metrics = metrics['classification_report'][domain]
                f.write(f"{domain}:\n")
                f.write(f"  Precisión: {domain_metrics['precision']:.4f}\n")
                f.write(f"  Recall: {domain_metrics['recall']:.4f}\n")
                f.write(f"  F1-Score: {domain_metrics['f1-score']:.4f}\n")
                f.write(f"  Soporte: {domain_metrics['support']}\n\n")
    
    print(f"✅ Reporte guardado en: {save_path}")

def main():
    parser = argparse.ArgumentParser(description='Evaluador del modelo de clasificación médica')
    parser.add_argument('--input', '-i', required=True, help='Archivo CSV de entrada')
    parser.add_argument('--model', '-m', default='models/medical_classifier.joblib', help='Modelo entrenado')
    parser.add_argument('--output', '-o', default='results/', help='Directorio de salida')
    
    args = parser.parse_args()
    
    print("🔬 EVALUADOR - AI + DATA CHALLENGE 2025")
    print("="*50)
    
    # Cargar datos
    df = load_test_data(args.input)
    if df is None:
        return
    
    # Cargar modelo
    try:
        classifier = joblib.load(args.model)
        print(f"✅ Modelo cargado desde: {args.model}")
    except Exception as e:
        print(f"❌ Error cargando modelo: {e}")
        print("💡 Entrena el modelo primero con: python cli.py train")
        return
    
    # Preparar datos
    texts = (df['title'] + ' ' + df['abstract']).tolist()
    y_true = [group.split(',') if isinstance(group, str) else [group] for group in df['group']]
    
    # Realizar predicciones
    print("🔄 Realizando predicciones...")
    y_pred = classifier.predict(texts)
    
    # Agregar predicciones al DataFrame
    df['group_predicted'] = [','.join(pred) for pred in y_pred]
    
    # Guardar resultados
    output_csv = os.path.join(args.output, 'predictions.csv')
    os.makedirs(args.output, exist_ok=True)
    df.to_csv(output_csv, index=False)
    print(f"✅ Predicciones guardadas en: {output_csv}")
    
    # Evaluar métricas
    print("📊 Calculando métricas...")
    metrics = evaluate_predictions(y_true, y_pred)
    
    # Mostrar resultados principales
    print("\n" + "="*50)
    print("RESULTADOS PRINCIPALES:")
    print("="*50)
    print(f"F1-Score Ponderado: {metrics['f1_weighted']:.4f}")
    print(f"F1-Score Macro: {metrics['f1_macro']:.4f}")
    print(f"F1-Score Micro: {metrics['f1_micro']:.4f}")
    
    # Generar visualizaciones y reportes
    plot_confusion_matrices(metrics['confusion_matrices'], 
                          os.path.join(args.output, 'confusion_matrices.png'))
    generate_results_report(metrics, 
                          os.path.join(args.output, 'evaluation_report.txt'))
    
    print(f"\n✅ Evaluación completada. Resultados en: {args.output}")
    print("📋 Archivos generados:")
    print(f"  - predictions.csv (predicciones)")
    print(f"  - confusion_matrices.png (matrices de confusión)")
    print(f"  - evaluation_report.txt (reporte detallado)")

if __name__ == "__main__":
    main()
