"""
Módulo de preprocesamiento de texto médico
"""
import pandas as pd
import re
from typing import List, Optional

class MedicalTextPreprocessor:
    def __init__(self, preserve_medical_terms: bool = True):
        self.preserve_medical_terms = preserve_medical_terms
        
    def clean_text(self, text: str) -> str:
        """Limpia y normaliza texto médico"""
        if pd.isna(text):
            return ""
            
        # Normalizar espacios
        text = re.sub(r'\s+', ' ', text)
        
        # Preservar terminología médica si está habilitado
        if not self.preserve_medical_terms:
            text = text.lower()
            
        return text.strip()
    
    def combine_title_abstract(self, title: str, abstract: str) -> str:
        """Combina título y resumen con separador"""
        title_clean = self.clean_text(title)
        abstract_clean = self.clean_text(abstract)
        
        if title_clean and abstract_clean:
            return f"{title_clean}. {abstract_clean}"
        elif title_clean:
            return title_clean
        elif abstract_clean:
            return abstract_clean
        else:
            return ""
    
    def process_dataframe(self, df: pd.DataFrame, 
                         title_col: str = "title",
                         abstract_col: str = "abstract") -> pd.DataFrame:
        """Procesa un DataFrame completo"""
        df_processed = df.copy()
        
        # Combinar título y resumen
        df_processed["text"] = df_processed.apply(
            lambda row: self.combine_title_abstract(
                row.get(title_col, ""), 
                row.get(abstract_col, "")
            ), axis=1
        )
        
        # Filtrar textos muy cortos
        df_processed = df_processed[df_processed["text"].str.len() >= 10]
        
        return df_processed
    
    def parse_labels(self, labels_str: str, separator: str = ";") -> List[str]:
        """Parsea etiquetas separadas por delimitador"""
        if pd.isna(labels_str):
            return []
        
        labels = str(labels_str).split(separator)
        return [label.strip() for label in labels if label.strip()]
