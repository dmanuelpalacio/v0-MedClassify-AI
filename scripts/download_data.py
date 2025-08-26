#!/usr/bin/env python3
"""
Script para descargar y preparar el dataset del challenge
"""

import requests
import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_challenge_data():
    """Descarga el dataset oficial del challenge"""
    
    url = "https://techspherecolombia.com/wp-content/uploads/2025/08/challenge_data-18-ago.csv"
    
    try:
        logger.info("Descargando dataset del challenge...")
        response = requests.get(url)
        response.raise_for_status()
        
        # Guardar archivo
        with open('challenge_data.csv', 'wb') as f:
            f.write(response.content)
        
        logger.info("Dataset descargado exitosamente: challenge_data.csv")
        
        # Verificar datos
        df = pd.read_csv('challenge_data.csv')
        logger.info(f"Dataset cargado: {len(df)} registros")
        logger.info(f"Columnas: {list(df.columns)}")
        
        # Estadísticas básicas
        logger.info("\n=== ESTADÍSTICAS DEL DATASET ===")
        logger.info(f"Total de registros: {len(df)}")
        logger.info(f"Registros con título: {df['title'].notna().sum()}")
        logger.info(f"Registros con abstract: {df['abstract'].notna().sum()}")
        
        # Distribución de grupos
        all_groups = []
        for group in df['group'].dropna():
            all_groups.extend([g.strip() for g in str(group).split(',')])
        
        from collections import Counter
        group_counts = Counter(all_groups)
        
        logger.info("\n=== DISTRIBUCIÓN DE GRUPOS ===")
        for group, count in group_counts.most_common():
            logger.info(f"{group}: {count}")
        
        return df
        
    except Exception as e:
        logger.error(f"Error descargando datos: {e}")
        raise

if __name__ == "__main__":
    download_challenge_data()
