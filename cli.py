#!/usr/bin/env python3
"""
CLI principal para el sistema de clasificación médica
TechSphere AI Challenge 2025
"""

import argparse
import sys
import json
from pathlib import Path
from typing import Dict, Any

from src.multilabel_classifier import MedicalLiteratureClassifier
from src.config import MODELS_DIR, OUTPUTS_DIR, DATA_DIR
import pandas as pd

def main():
    parser = argparse.ArgumentParser(
        description="MedClassify AI - Sistema de Clasificación de Literatura Médica",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  # Entrenar modelo
  python cli.py train --data data/challenge_data.csv --save models/best_model.joblib
  
  # Evaluar modelo
  python cli.py eval --data data/test_data.csv --model models/best_model.joblib
  
  # Predecir por lotes
  python cli.py predict --input data/to_predict.csv --output outputs/predictions.csv
  
  # Clasificar texto individual
  python cli.py classify --title "Cardiovascular Risk Assessment" --abstract "This study evaluates..."
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')
    
    # Comando train
    train_parser = subparsers.add_parser('train', help='Entrenar modelo de clasificación')
    train_parser.add_argument('--data', required=True, help='Archivo CSV con datos de entrenamiento')
    train_parser.add_argument('--save', default=str(MODELS_DIR / 'trained_model.joblib'), 
                             help='Ruta para guardar el modelo entrenado')
    train_parser.add_argument('--test-size', type=float, default=0.2, 
                             help='Proporción de datos para testing (default: 0.2)')
    
    # Comando eval
    eval_parser = subparsers.add_parser('eval', help='Evaluar modelo entrenado')
    eval_parser.add_argument('--data', required=True, help='Archivo CSV con datos de evaluación')
    eval_parser.add_argument('--model', default=str(MODELS_DIR / 'trained_model.joblib'),
                            help='Ruta del modelo entrenado')
    eval_parser.add_argument('--output', default=str(OUTPUTS_DIR / 'evaluation_metrics.json'),
                            help='Archivo de salida para métricas')
    
    # Comando predict
    predict_parser = subparsers.add_parser('predict', help='Predecir etiquetas por lotes')
    predict_parser.add_argument('--input', required=True, help='Archivo CSV con textos a clasificar')
    predict_parser.add_argument('--output', required=True, help='Archivo CSV de salida con predicciones')
    predict_parser.add_argument('--model', default=str(MODELS_DIR / 'trained_model.joblib'),
                               help='Ruta del modelo entrenado')
    
    # Comando classify
    classify_parser = subparsers.add_parser('classify', help='Clasificar texto individual')
    classify_parser.add_argument('--title', required=True, help='Título del artículo')
    classify_parser.add_argument('--abstract', required=True, help='Resumen del artículo')
    classify_parser.add_argument('--model', default=str(MODELS_DIR / 'trained_model.joblib'),
                                help='Ruta del modelo entrenado')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'train':
            train_model(args)
        elif args.command == 'eval':
            evaluate_model(args)
        elif args.command == 'predict':
            predict_batch(args)
        elif args.command == 'classify':
            classify_single(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def train_model(args):
    """Entrenar modelo de clasificación"""
    print(f"🚀 Iniciando entrenamiento con datos: {args.data}")
    
    # Cargar datos
    df = pd.read_csv(args.data)
    print(f"📊 Datos cargados: {len(df)} registros")
    
    # Inicializar y entrenar clasificador
    classifier = MedicalLiteratureClassifier()
    metrics = classifier.train(df)
    
    # Guardar modelo
    classifier.save_model(args.save)
    print(f"💾 Modelo guardado en: {args.save}")
    
    # Mostrar métricas
    print("\n📈 Métricas de entrenamiento:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")
    
    # Guardar métricas
    metrics_file = OUTPUTS_DIR / 'training_metrics.json'
    with open(metrics_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"📋 Métricas guardadas en: {metrics_file}")

def evaluate_model(args):
    """Evaluar modelo entrenado"""
    print(f"🔍 Evaluando modelo: {args.model}")
    
    # Cargar modelo
    classifier = MedicalLiteratureClassifier()
    classifier.load_model(args.model)
    
    # Cargar datos de evaluación
    df = pd.read_csv(args.data)
    print(f"📊 Datos de evaluación: {len(df)} registros")
    
    # Preparar datos
    X, Y = classifier.prepare_data(df)
    
    # Evaluar
    metrics = classifier.evaluate(X, Y)
    
    # Mostrar resultados
    print("\n📈 Métricas de evaluación:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")
    
    # Guardar métricas
    with open(args.output, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"📋 Métricas guardadas en: {args.output}")

def predict_batch(args):
    """Predecir etiquetas por lotes"""
    print(f"🔮 Prediciendo etiquetas para: {args.input}")
    
    # Cargar modelo
    classifier = MedicalLiteratureClassifier()
    classifier.load_model(args.model)
    
    # Cargar datos
    df = pd.read_csv(args.input)
    print(f"📊 Datos a procesar: {len(df)} registros")
    
    # Preparar textos
    texts = []
    for _, row in df.iterrows():
        text = f"{row.get('title', '')}. {row.get('abstract', '')}"
        texts.append(text)
    
    # Predecir
    predictions = classifier.predict(texts)
    probabilities = classifier.predict_proba(texts)
    
    # Crear DataFrame de resultados
    results_df = df.copy()
    results_df['predicted_labels'] = [';'.join(pred) for pred in predictions]
    
    # Agregar probabilidades
    for i, domain in enumerate(classifier.label_binarizer.classes_):
        results_df[f'prob_{domain}'] = [prob[domain] for prob in probabilities]
    
    # Guardar resultados
    results_df.to_csv(args.output, index=False)
    print(f"💾 Predicciones guardadas en: {args.output}")
    
    # Estadísticas
    total_predictions = len(predictions)
    multi_label = sum(1 for pred in predictions if len(pred) > 1)
    print(f"\n📊 Estadísticas:")
    print(f"  Total procesados: {total_predictions}")
    print(f"  Multi-etiqueta: {multi_label} ({multi_label/total_predictions:.1%})")

def classify_single(args):
    """Clasificar texto individual"""
    print("🧠 Clasificando artículo individual...")
    
    # Cargar modelo
    classifier = MedicalLiteratureClassifier()
    classifier.load_model(args.model)
    
    # Combinar título y resumen
    text = f"{args.title}. {args.abstract}"
    
    # Predecir
    predictions = classifier.predict([text])[0]
    probabilities = classifier.predict_proba([text])[0]
    
    # Mostrar resultados
    print(f"\n📄 Título: {args.title}")
    print(f"📝 Resumen: {args.abstract[:100]}...")
    print(f"\n🎯 Predicciones:")
    
    if predictions:
        for label in predictions:
            confidence = probabilities[label]
            print(f"  ✅ {label}: {confidence:.3f} ({confidence*100:.1f}%)")
    else:
        print("  ❌ No se encontraron etiquetas con suficiente confianza")
    
    print(f"\n📊 Todas las probabilidades:")
    for domain, prob in sorted(probabilities.items(), key=lambda x: x[1], reverse=True):
        print(f"  {domain}: {prob:.3f} ({prob*100:.1f}%)")

if __name__ == '__main__':
    main()
