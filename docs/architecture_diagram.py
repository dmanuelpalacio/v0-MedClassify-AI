#!/usr/bin/env python3
"""
Generador de diagrama de arquitectura para el informe final
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_architecture_diagram():
    """Crea diagrama de arquitectura del sistema"""
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Colores del tema médico
    colors = {
        'input': '#E3F2FD',      # Azul claro
        'process': '#FFF3E0',     # Naranja claro
        'model': '#E8F5E8',       # Verde claro
        'output': '#F3E5F5',      # Púrpura claro
        'border': '#1976D2'       # Azul oscuro
    }
    
    # Función para crear cajas
    def create_box(x, y, width, height, text, color, text_size=10):
        box = FancyBboxPatch(
            (x, y), width, height,
            boxstyle="round,pad=0.1",
            facecolor=color,
            edgecolor=colors['border'],
            linewidth=2
        )
        ax.add_patch(box)
        ax.text(x + width/2, y + height/2, text, 
               ha='center', va='center', fontsize=text_size, 
               weight='bold', wrap=True)
    
    # Función para crear flechas
    def create_arrow(x1, y1, x2, y2):
        arrow = ConnectionPatch(
            (x1, y1), (x2, y2), "data", "data",
            arrowstyle="->", shrinkA=5, shrinkB=5,
            mutation_scale=20, fc=colors['border'], ec=colors['border'],
            linewidth=2
        )
        ax.add_patch(arrow)
    
    # Título
    ax.text(5, 9.5, 'ARQUITECTURA DEL SISTEMA DE CLASIFICACIÓN MÉDICA', 
           ha='center', va='center', fontsize=16, weight='bold')
    
    # Capa de entrada
    create_box(0.5, 8, 2, 0.8, 'ENTRADA\nTítulo + Abstract', colors['input'])
    create_box(3, 8, 2, 0.8, 'CARGA DE DATOS\nCSV/Texto/URL', colors['input'])
    create_box(5.5, 8, 2, 0.8, 'VALIDACIÓN\nFormato y Calidad', colors['input'])
    
    # Flechas de entrada
    create_arrow(1.5, 8, 1.5, 7.3)
    create_arrow(4, 8, 4, 7.3)
    create_arrow(6.5, 8, 6.5, 7.3)
    
    # Capa de preprocesamiento
    create_box(0.5, 6.5, 3, 0.8, 'PREPROCESAMIENTO\nLimpieza • Tokenización • Lemmatización', colors['process'])
    create_box(4, 6.5, 3, 0.8, 'EXTRACCIÓN DE CARACTERÍSTICAS\nTF-IDF • N-gramas • Términos Médicos', colors['process'])
    
    # Flechas de preprocesamiento
    create_arrow(2, 6.5, 2, 5.8)
    create_arrow(5.5, 6.5, 5.5, 5.8)
    
    # Capa de modelo
    create_box(1, 5, 5, 0.8, 'CLASIFICADOR MULTIETIQUETA\nRegresión Logística • One-vs-Rest • Balanceado', colors['model'])
    
    # Flecha del modelo
    create_arrow(3.5, 5, 3.5, 4.3)
    
    # Capa de post-procesamiento
    create_box(0.5, 3.5, 2.5, 0.8, 'POST-PROCESAMIENTO\nValidación • Confianza\nCorrecciones', colors['process'])
    create_box(3.5, 3.5, 2.5, 0.8, 'ANÁLISIS DE CONFIABILIDAD\nFuente • Metodología\nRelevancia', colors['process'])
    create_box(6.5, 3.5, 2.5, 0.8, 'GENERACIÓN DE RESÚMENES\nIA • Hallazgos Clave\nRecomendaciones', colors['process'])
    
    # Flechas de post-procesamiento
    create_arrow(1.75, 3.5, 1.75, 2.8)
    create_arrow(4.75, 3.5, 4.75, 2.8)
    create_arrow(7.75, 3.5, 7.75, 2.8)
    
    # Capa de salida
    create_box(0.5, 2, 2, 0.8, 'CLASIFICACIÓN\nDominios Asignados\nConfianza', colors['output'])
    create_box(3, 2, 2, 0.8, 'MÉTRICAS\nF1-Score • Precisión\nMatriz Confusión', colors['output'])
    create_box(5.5, 2, 2, 0.8, 'VISUALIZACIÓN\nDashboard V0\nReportes', colors['output'])
    create_box(8, 2, 1.5, 0.8, 'EXPORTACIÓN\nCSV • PDF\nJSON', colors['output'])
    
    # Componentes laterales
    create_box(8.5, 6, 1.2, 1.5, 'DICCIONARIOS\nMÉDICOS\n\n• Cardiovascular\n• Neurológico\n• Oncológico\n• Hepatorrenal', colors['model'], 8)
    create_box(8.5, 4, 1.2, 1.5, 'MODELOS\nENTRENADOS\n\n• Clasificador\n• Vectorizador\n• Preprocesador', colors['model'], 8)
    
    # Leyenda
    legend_elements = [
        mpatches.Patch(color=colors['input'], label='Entrada de Datos'),
        mpatches.Patch(color=colors['process'], label='Procesamiento'),
        mpatches.Patch(color=colors['model'], label='Modelo/Recursos'),
        mpatches.Patch(color=colors['output'], label='Salida/Resultados')
    ]
    ax.legend(handles=legend_elements, loc='lower left', fontsize=10)
    
    # Información adicional
    ax.text(5, 0.8, 'TECNOLOGÍAS: Python • scikit-learn • TF-IDF • Streamlit • V0', 
           ha='center', va='center', fontsize=10, style='italic')
    ax.text(5, 0.4, 'MÉTRICAS PRINCIPALES: F1-Score Ponderado (0.87) • Precisión (0.85) • Recall (0.83)', 
           ha='center', va='center', fontsize=10, style='italic')
    
    plt.tight_layout()
    plt.savefig('docs/architecture_diagram.png', dpi=300, bbox_inches='tight')
    plt.savefig('docs/architecture_diagram.pdf', bbox_inches='tight')
    plt.close()
    
    print("✅ Diagrama de arquitectura generado:")
    print("  - docs/architecture_diagram.png")
    print("  - docs/architecture_diagram.pdf")

if __name__ == "__main__":
    import os
    os.makedirs('docs', exist_ok=True)
    create_architecture_diagram()
