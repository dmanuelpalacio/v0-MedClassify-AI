"""
Generador de Diagrama de Arquitectura para MedClassify AI
Crea visualización completa del pipeline de clasificación médica
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, ConnectionPatch
import numpy as np

def create_architecture_diagram():
    """
    Crea el diagrama de arquitectura completo del sistema MedClassify AI
    """
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Colores del tema médico
    colors = {
        'input': '#E3F2FD',
        'preprocessing': '#FFF3E0',
        'models': '#E8F5E8',
        'evaluation': '#FCE4EC',
        'output': '#F3E5F5',
        'border': '#1976D2'
    }
    
    # Título principal
    ax.text(8, 11.5, 'MedClassify AI - Arquitectura del Sistema', 
            fontsize=20, fontweight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#1976D2', edgecolor='none', alpha=0.8),
            color='white')
    
    # 1. ENTRADA DE DATOS
    input_box = FancyBboxPatch((0.5, 9.5), 3, 1.5, 
                               boxstyle="round,pad=0.1", 
                               facecolor=colors['input'], 
                               edgecolor=colors['border'], linewidth=2)
    ax.add_patch(input_box)
    ax.text(2, 10.6, 'ENTRADA', fontsize=12, fontweight='bold', ha='center')
    ax.text(2, 10.2, '• Título + Abstract', fontsize=10, ha='center')
    ax.text(2, 9.9, '• 3,565 registros', fontsize=10, ha='center')
    ax.text(2, 9.6, '• Formato CSV/JSON', fontsize=10, ha='center')
    
    # 2. PREPROCESAMIENTO
    preproc_box = FancyBboxPatch((5, 9.5), 3, 1.5,
                                 boxstyle="round,pad=0.1",
                                 facecolor=colors['preprocessing'],
                                 edgecolor=colors['border'], linewidth=2)
    ax.add_patch(preproc_box)
    ax.text(6.5, 10.6, 'PREPROCESAMIENTO', fontsize=12, fontweight='bold', ha='center')
    ax.text(6.5, 10.2, '• Limpieza de texto', fontsize=10, ha='center')
    ax.text(6.5, 9.9, '• Tokenización médica', fontsize=10, ha='center')
    ax.text(6.5, 9.6, '• Normalización', fontsize=10, ha='center')
    
    # 3. VECTORIZACIÓN
    vector_box = FancyBboxPatch((9.5, 9.5), 3, 1.5,
                                boxstyle="round,pad=0.1",
                                facecolor=colors['preprocessing'],
                                edgecolor=colors['border'], linewidth=2)
    ax.add_patch(vector_box)
    ax.text(11, 10.6, 'VECTORIZACIÓN', fontsize=12, fontweight='bold', ha='center')
    ax.text(11, 10.2, '• TF-IDF (n-gramas)', fontsize=10, ha='center')
    ax.text(11, 9.9, '• BioBERT Embeddings', fontsize=10, ha='center')
    ax.text(11, 9.6, '• Características híbridas', fontsize=10, ha='center')
    
    # 4. MODELOS DE CLASIFICACIÓN
    # Baseline Model
    baseline_box = FancyBboxPatch((1, 7), 3.5, 1.5,
                                  boxstyle="round,pad=0.1",
                                  facecolor=colors['models'],
                                  edgecolor=colors['border'], linewidth=2)
    ax.add_patch(baseline_box)
    ax.text(2.75, 8.1, 'BASELINE MODEL', fontsize=12, fontweight='bold', ha='center')
    ax.text(2.75, 7.7, 'TF-IDF + Logistic Regression', fontsize=10, ha='center')
    ax.text(2.75, 7.4, 'F1-Score: 85.2%', fontsize=10, ha='center', color='#2E7D32')
    ax.text(2.75, 7.1, 'Rápido y eficiente', fontsize=9, ha='center', style='italic')
    
    # Hybrid Model
    hybrid_box = FancyBboxPatch((6, 7), 3.5, 1.5,
                                boxstyle="round,pad=0.1",
                                facecolor=colors['models'],
                                edgecolor=colors['border'], linewidth=2)
    ax.add_patch(hybrid_box)
    ax.text(7.75, 8.1, 'HYBRID MODEL', fontsize=12, fontweight='bold', ha='center')
    ax.text(7.75, 7.7, 'BioBERT + TF-IDF + LR', fontsize=10, ha='center')
    ax.text(7.75, 7.4, 'F1-Score: 89.0%', fontsize=10, ha='center', color='#2E7D32')
    ax.text(7.75, 7.1, 'Mejor rendimiento', fontsize=9, ha='center', style='italic')
    
    # Zero-shot Model
    zeroshot_box = FancyBboxPatch((11, 7), 3.5, 1.5,
                                  boxstyle="round,pad=0.1",
                                  facecolor=colors['models'],
                                  edgecolor=colors['border'], linewidth=2)
    ax.add_patch(zeroshot_box)
    ax.text(12.75, 8.1, 'ZERO-SHOT MODEL', fontsize=12, fontweight='bold', ha='center')
    ax.text(12.75, 7.7, 'BART-MNLI', fontsize=10, ha='center')
    ax.text(12.75, 7.4, 'F1-Score: 82.1%', fontsize=10, ha='center', color='#2E7D32')
    ax.text(12.75, 7.1, 'Sin entrenamiento', fontsize=9, ha='center', style='italic')
    
    # 5. EVALUACIÓN
    eval_box = FancyBboxPatch((4, 4.5), 8, 1.5,
                              boxstyle="round,pad=0.1",
                              facecolor=colors['evaluation'],
                              edgecolor=colors['border'], linewidth=2)
    ax.add_patch(eval_box)
    ax.text(8, 5.6, 'EVALUACIÓN MULTIMÉTRICA', fontsize=12, fontweight='bold', ha='center')
    ax.text(6, 5.2, '• F1-Score Weighted: 89.0%', fontsize=10, ha='left')
    ax.text(6, 4.9, '• Exact Match: 84.0%', fontsize=10, ha='left')
    ax.text(10, 5.2, '• Hamming Loss: 12.0%', fontsize=10, ha='left')
    ax.text(10, 4.9, '• ROC-AUC Macro: 91.0%', fontsize=10, ha='left')
    
    # 6. SALIDA
    output_box = FancyBboxPatch((1, 2), 6, 1.5,
                                boxstyle="round,pad=0.1",
                                facecolor=colors['output'],
                                edgecolor=colors['border'], linewidth=2)
    ax.add_patch(output_box)
    ax.text(4, 3.1, 'SALIDA MULTIETIQUETA', fontsize=12, fontweight='bold', ha='center')
    ax.text(4, 2.7, 'Dominios: Cardiovascular, Neurológico,', fontsize=10, ha='center')
    ax.text(4, 2.4, 'Hepatorrenal, Oncológico', fontsize=10, ha='center')
    ax.text(4, 2.1, 'Probabilidades + Etiquetas predichas', fontsize=10, ha='center')
    
    # 7. DESPLIEGUE
    deploy_box = FancyBboxPatch((9, 2), 6, 1.5,
                                boxstyle="round,pad=0.1",
                                facecolor=colors['output'],
                                edgecolor=colors['border'], linewidth=2)
    ax.add_patch(deploy_box)
    ax.text(12, 3.1, 'DESPLIEGUE', fontsize=12, fontweight='bold', ha='center')
    ax.text(12, 2.7, '• API REST (/api/predict)', fontsize=10, ha='center')
    ax.text(12, 2.4, '• Dashboard V0 interactivo', fontsize=10, ha='center')
    ax.text(12, 2.1, '• Vercel + GitHub', fontsize=10, ha='center')
    
    # FLECHAS DE CONEXIÓN
    # Entrada -> Preprocesamiento
    arrow1 = ConnectionPatch((3.5, 10.25), (5, 10.25), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20,
                            fc=colors['border'], ec=colors['border'], linewidth=2)
    ax.add_patch(arrow1)
    
    # Preprocesamiento -> Vectorización
    arrow2 = ConnectionPatch((8, 10.25), (9.5, 10.25), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20,
                            fc=colors['border'], ec=colors['border'], linewidth=2)
    ax.add_patch(arrow2)
    
    # Vectorización -> Modelos
    arrow3 = ConnectionPatch((11, 9.5), (2.75, 8.5), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20,
                            fc=colors['border'], ec=colors['border'], linewidth=2)
    ax.add_patch(arrow3)
    
    arrow4 = ConnectionPatch((11, 9.5), (7.75, 8.5), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20,
                            fc=colors['border'], ec=colors['border'], linewidth=2)
    ax.add_patch(arrow4)
    
    arrow5 = ConnectionPatch((11, 9.5), (12.75, 8.5), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20,
                            fc=colors['border'], ec=colors['border'], linewidth=2)
    ax.add_patch(arrow5)
    
    # Modelos -> Evaluación
    arrow6 = ConnectionPatch((7.75, 7), (8, 6), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20,
                            fc=colors['border'], ec=colors['border'], linewidth=2)
    ax.add_patch(arrow6)
    
    # Evaluación -> Salida
    arrow7 = ConnectionPatch((6, 4.5), (4, 3.5), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20,
                            fc=colors['border'], ec=colors['border'], linewidth=2)
    ax.add_patch(arrow7)
    
    # Evaluación -> Despliegue
    arrow8 = ConnectionPatch((10, 4.5), (12, 3.5), "data", "data",
                            arrowstyle="->", shrinkA=5, shrinkB=5, mutation_scale=20,
                            fc=colors['border'], ec=colors['border'], linewidth=2)
    ax.add_patch(arrow8)
    
    # Footer con información del challenge
    ax.text(8, 0.5, 'AI Data Challenge 2025 - TechSphere Colombia', 
            fontsize=14, fontweight='bold', ha='center',
            bbox=dict(boxstyle="round,pad=0.3", facecolor='#FF6B35', edgecolor='none', alpha=0.8),
            color='white')
    ax.text(8, 0.1, 'Manuel Palacio & Camila Zapata - Núcleo Colectivo + Línea Médica Yolombó', 
            fontsize=10, ha='center', style='italic')
    
    plt.tight_layout()
    plt.savefig('docs/architecture_diagram.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.savefig('public/architecture_diagram.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    
    return fig

if __name__ == "__main__":
    fig = create_architecture_diagram()
    plt.show()
    print("Diagrama de arquitectura generado y guardado en docs/ y public/")
