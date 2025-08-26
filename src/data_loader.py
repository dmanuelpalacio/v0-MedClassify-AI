import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MedicalDataLoader:
    """
    Cargador y preprocesador de datos médicos para clasificación multi-etiqueta
    """
    
    def __init__(self):
        self.mlb = MultiLabelBinarizer()
        self.classes = ['Cardiovascular', 'Neurological', 'Hepatorenal', 'Oncological']
        
    def load_data(self, file_path):
        """Carga el dataset desde CSV"""
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Dataset cargado: {len(df)} registros")
            return df
        except Exception as e:
            logger.error(f"Error cargando datos: {e}")
            raise
    
    def preprocess_text(self, text):
        """Preprocesa texto médico"""
        if pd.isna(text):
            return ""
        
        # Convertir a minúsculas
        text = text.lower()
        
        # Remover caracteres especiales pero mantener términos médicos
        text = re.sub(r'[^\w\s\-]', ' ', text)
        
        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def parse_labels(self, group_str):
        """Parsea las etiquetas del campo 'group'"""
        if pd.isna(group_str):
            return []
        
        # Separar por comas y limpiar
        labels = [label.strip() for label in str(group_str).split(',')]
        
        # Filtrar solo las clases válidas
        valid_labels = [label for label in labels if label in self.classes]
        
        return valid_labels if valid_labels else ['Oncological']  # Default fallback
    
    def prepare_dataset(self, df, test_size=0.2, val_size=0.1):
        """Prepara el dataset para entrenamiento"""
        
        # Preprocesar textos
        df['title_clean'] = df['title'].apply(self.preprocess_text)
        df['abstract_clean'] = df['abstract'].apply(self.preprocess_text)
        
        # Combinar título y abstract
        df['combined_text'] = df['title_clean'] + ' ' + df['abstract_clean']
        
        # Parsear etiquetas
        df['labels'] = df['group'].apply(self.parse_labels)
        
        # Crear matriz binaria de etiquetas
        y = self.mlb.fit_transform(df['labels'])
        
        # División de datos
        X_temp, X_test, y_temp, y_test = train_test_split(
            df['combined_text'], y, test_size=test_size, random_state=42, stratify=y
        )
        
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_size/(1-test_size), random_state=42, stratify=y_temp
        )
        
        logger.info(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
        
        return {
            'X_train': X_train, 'y_train': y_train,
            'X_val': X_val, 'y_val': y_val,
            'X_test': X_test, 'y_test': y_test,
            'classes': self.mlb.classes_
        }
    
    def get_label_distribution(self, y):
        """Analiza la distribución de etiquetas"""
        distribution = {}
        for i, class_name in enumerate(self.mlb.classes_):
            distribution[class_name] = np.sum(y[:, i])
        return distribution
