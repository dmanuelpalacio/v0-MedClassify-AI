import pandas as pd
import numpy as np
import torch
import joblib
from pathlib import Path
import logging
from .data_loader import MedicalDataLoader
from .model import MedicalClassifierTrainer
from .evaluation import ModelEvaluator

logger = logging.getLogger(__name__)

class MedicalClassificationPipeline:
    """
    Pipeline completo para clasificación de literatura médica
    """
    
    def __init__(self, model_name='emilyalsentzer/Bio_Discharge_Summary_BERT'):
        self.model_name = model_name
        self.data_loader = MedicalDataLoader()
        self.trainer = MedicalClassifierTrainer(model_name)
        self.evaluator = None
        self.model = None
        self.classes = ['Cardiovascular', 'Neurological', 'Hepatorenal', 'Oncological']
        
    def train_pipeline(self, data_path, epochs=3, batch_size=16, learning_rate=2e-5):
        """Entrena el pipeline completo"""
        
        logger.info("Iniciando entrenamiento del pipeline...")
        
        # 1. Cargar y preparar datos
        logger.info("Cargando datos...")
        df = self.data_loader.load_data(data_path)
        data_dict = self.data_loader.prepare_dataset(df)
        
        # 2. Análisis exploratorio
        logger.info("Realizando análisis exploratorio...")
        train_distribution = self.data_loader.get_label_distribution(data_dict['y_train'])
        logger.info(f"Distribución de clases en entrenamiento: {train_distribution}")
        
        # 3. Entrenar modelo
        logger.info("Entrenando modelo...")
        self.model = self.trainer.train_model(
            data_dict, epochs=epochs, batch_size=batch_size, learning_rate=learning_rate
        )
        
        # 4. Evaluación
        logger.info("Evaluando modelo...")
        self.evaluator = ModelEvaluator(self.classes)
        
        # Predicciones en conjunto de prueba
        test_encodings = self.trainer.tokenize_texts(data_dict['X_test'])
        y_pred, y_probs = self.trainer.predict(self.model, data_dict['X_test'])
        
        # Calcular métricas
        metrics, class_report = self.evaluator.calculate_metrics(
            data_dict['y_test'], y_pred, y_probs
        )
        
        # Generar visualizaciones
        self.evaluator.plot_confusion_matrices(data_dict['y_test'], y_pred, 'confusion_matrices.png')
        self.evaluator.plot_metrics_comparison(metrics, 'metrics_comparison.png')
        
        # Reporte detallado
        detailed_report = self.evaluator.generate_detailed_report(
            data_dict['y_test'], y_pred, y_probs, metrics, class_report
        )
        
        # Guardar resultados
        with open('evaluation_report.md', 'w', encoding='utf-8') as f:
            f.write(detailed_report)
        
        # Guardar modelo y componentes
        self.save_pipeline()
        
        logger.info(f"Entrenamiento completado. F1-Score Ponderado: {metrics['weighted_f1']:.4f}")
        
        return metrics, class_report
    
    def predict_batch(self, texts, threshold=0.5):
        """Predice etiquetas para un batch de textos"""
        if self.model is None:
            raise ValueError("Modelo no entrenado. Ejecute train_pipeline() primero.")
        
        # Preprocesar textos
        processed_texts = pd.Series(texts).apply(self.data_loader.preprocess_text)
        
        # Realizar predicciones
        predictions, probabilities = self.trainer.predict(self.model, processed_texts, threshold)
        
        # Convertir a etiquetas legibles
        predicted_labels = []
        for pred in predictions:
            labels = [self.classes[i] for i, val in enumerate(pred) if val == 1]
            predicted_labels.append(labels if labels else ['Oncological'])  # Default fallback
        
        return predicted_labels, probabilities
    
    def evaluate_csv(self, csv_path, output_path='predictions.csv'):
        """Evalúa un archivo CSV y genera predicciones"""
        
        # Cargar datos
        df = pd.read_csv(csv_path)
        
        # Combinar título y abstract
        combined_texts = (df['title'].fillna('') + ' ' + df['abstract'].fillna('')).tolist()
        
        # Realizar predicciones
        predicted_labels, probabilities = self.predict_batch(combined_texts)
        
        # Crear DataFrame de resultados
        results_df = df.copy()
        results_df['group_predicted'] = [','.join(labels) for labels in predicted_labels]
        
        # Agregar probabilidades por clase
        for i, class_name in enumerate(self.classes):
            results_df[f'prob_{class_name}'] = [probs[i] for probs in probabilities]
        
        # Si existe columna 'group' real, calcular métricas
        if 'group' in df.columns:
            # Preparar etiquetas reales
            real_labels = df['group'].apply(self.data_loader.parse_labels).tolist()
            real_binary = self.data_loader.mlb.transform(real_labels)
            pred_binary = self.data_loader.mlb.transform(predicted_labels)
            
            # Calcular métricas
            metrics, class_report = self.evaluator.calculate_metrics(real_binary, pred_binary)
            
            print(f"\n=== MÉTRICAS DE EVALUACIÓN ===")
            print(f"F1-Score Ponderado: {metrics['weighted_f1']:.4f}")
            print(f"Precisión Ponderada: {metrics['weighted_precision']:.4f}")
            print(f"Recall Ponderado: {metrics['weighted_recall']:.4f}")
            print(f"Exact Match Ratio: {metrics['exact_match_ratio']:.4f}")
            
            # Generar matriz de confusión
            self.evaluator.plot_confusion_matrices(real_binary, pred_binary)
        
        # Guardar resultados
        results_df.to_csv(output_path, index=False)
        logger.info(f"Predicciones guardadas en: {output_path}")
        
        return results_df
    
    def save_pipeline(self, path='model_checkpoint'):
        """Guarda el pipeline completo"""
        Path(path).mkdir(exist_ok=True)
        
        # Guardar modelo
        if self.model:
            torch.save(self.model.state_dict(), f'{path}/model.pth')
        
        # Guardar componentes
        joblib.dump(self.data_loader.mlb, f'{path}/label_binarizer.pkl')
        
        # Guardar configuración
        config = {
            'model_name': self.model_name,
            'classes': self.classes,
            'max_length': self.trainer.max_length
        }
        joblib.dump(config, f'{path}/config.pkl')
        
        logger.info(f"Pipeline guardado en: {path}")
    
    def load_pipeline(self, path='model_checkpoint'):
        """Carga el pipeline completo"""
        
        # Cargar configuración
        config = joblib.load(f'{path}/config.pkl')
        self.model_name = config['model_name']
        self.classes = config['classes']
        
        # Cargar componentes
        self.data_loader.mlb = joblib.load(f'{path}/label_binarizer.pkl')
        self.trainer = MedicalClassifierTrainer(self.model_name, config['max_length'])
        
        # Cargar modelo
        from .model import MedicalClassifier
        self.model = MedicalClassifier(self.model_name, len(self.classes))
        self.model.load_state_dict(torch.load(f'{path}/model.pth', map_location=self.trainer.device))
        self.model.to(self.trainer.device)
        
        self.evaluator = ModelEvaluator(self.classes)
        
        logger.info(f"Pipeline cargado desde: {path}")
