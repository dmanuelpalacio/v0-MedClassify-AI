#!/usr/bin/env python3
"""
Solución para el Challenge de Clasificación Biomédica con IA
Tech Sphere 2025

Autor: [Tu nombre/equipo]
Descripción: Pipeline de clasificación multi-etiqueta para literatura médica
usando BioBERT/ClinicalBERT
"""

import argparse
import logging
import sys
from pathlib import Path
from src.pipeline import MedicalClassificationPipeline

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('medical_classification.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='Clasificador de Literatura Médica')
    parser.add_argument('--mode', choices=['train', 'predict', 'evaluate'], required=True,
                       help='Modo de operación')
    parser.add_argument('--data', type=str, required=True,
                       help='Ruta al archivo CSV de datos')
    parser.add_argument('--model', type=str, default='emilyalsentzer/Bio_Discharge_Summary_BERT',
                       help='Modelo base a utilizar')
    parser.add_argument('--epochs', type=int, default=3,
                       help='Número de épocas para entrenamiento')
    parser.add_argument('--batch_size', type=int, default=16,
                       help='Tamaño del batch')
    parser.add_argument('--learning_rate', type=float, default=2e-5,
                       help='Tasa de aprendizaje')
    parser.add_argument('--output', type=str, default='predictions.csv',
                       help='Archivo de salida para predicciones')
    parser.add_argument('--checkpoint', type=str, default='model_checkpoint',
                       help='Directorio para guardar/cargar modelo')
    
    args = parser.parse_args()
    
    # Crear pipeline
    pipeline = MedicalClassificationPipeline(model_name=args.model)
    
    try:
        if args.mode == 'train':
            logger.info("=== INICIANDO ENTRENAMIENTO ===")
            logger.info(f"Datos: {args.data}")
            logger.info(f"Modelo: {args.model}")
            logger.info(f"Épocas: {args.epochs}")
            logger.info(f"Batch size: {args.batch_size}")
            logger.info(f"Learning rate: {args.learning_rate}")
            
            # Entrenar pipeline
            metrics, class_report = pipeline.train_pipeline(
                data_path=args.data,
                epochs=args.epochs,
                batch_size=args.batch_size,
                learning_rate=args.learning_rate
            )
            
            logger.info("=== ENTRENAMIENTO COMPLETADO ===")
            logger.info(f"F1-Score Ponderado Final: {metrics['weighted_f1']:.4f}")
            
        elif args.mode == 'predict':
            logger.info("=== REALIZANDO PREDICCIONES ===")
            
            # Cargar modelo entrenado
            if Path(args.checkpoint).exists():
                pipeline.load_pipeline(args.checkpoint)
            else:
                logger.error(f"No se encontró modelo en {args.checkpoint}")
                return
            
            # Realizar predicciones
            results = pipeline.evaluate_csv(args.data, args.output)
            logger.info(f"Predicciones guardadas en: {args.output}")
            
        elif args.mode == 'evaluate':
            logger.info("=== EVALUANDO MODELO ===")
            
            # Cargar modelo entrenado
            if Path(args.checkpoint).exists():
                pipeline.load_pipeline(args.checkpoint)
            else:
                logger.error(f"No se encontró modelo en {args.checkpoint}")
                return
            
            # Evaluar con métricas
            results = pipeline.evaluate_csv(args.data, args.output)
            logger.info("Evaluación completada")
            
    except Exception as e:
        logger.error(f"Error durante la ejecución: {e}")
        raise

if __name__ == "__main__":
    main()
