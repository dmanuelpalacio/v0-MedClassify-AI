"""
Aplicación Streamlit para clasificación de literatura médica
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from pathlib import Path

from src.multilabel_classifier import MedicalLiteratureClassifier
from src.config import MEDICAL_DOMAINS, MODELS_DIR

# Configuración de página
st.set_page_config(
    page_title="MedClassify AI - Challenge 2025",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #3b82f6;
    }
    .domain-card {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏥 MedClassify AI - Challenge 2025</h1>
        <p>Sistema de Clasificación Automática de Literatura Médica</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🔧 Configuración")
    
    # Inicializar modelo
    if 'classifier' not in st.session_state:
        st.session_state.classifier = MedicalLiteratureClassifier()
    
    # Pestañas principales
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📝 Clasificación Individual",
        "📊 Procesamiento por Lotes", 
        "🎯 Entrenamiento",
        "📈 Métricas y Evaluación",
        "📚 Documentación"
    ])
    
    with tab1:
        clasificacion_individual()
    
    with tab2:
        procesamiento_lotes()
    
    with tab3:
        entrenamiento_modelo()
    
    with tab4:
        metricas_evaluacion()
    
    with tab5:
        documentacion()

def clasificacion_individual():
    st.header("📝 Clasificación Individual de Artículos")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Formulario de entrada
        with st.form("clasificacion_form"):
            titulo = st.text_input(
                "Título del artículo",
                placeholder="Ingrese el título del artículo médico..."
            )
            
            resumen = st.text_area(
                "Resumen/Abstract",
                height=200,
                placeholder="Ingrese el resumen o abstract del artículo..."
            )
            
            submitted = st.form_submit_button("🔍 Clasificar Artículo")
        
        if submitted and (titulo or resumen):
            if not st.session_state.classifier.is_trained:
                st.error("⚠️ El modelo no está entrenado. Por favor, entrene el modelo primero en la pestaña 'Entrenamiento'.")
                return
            
            # Combinar título y resumen
            texto_completo = f"{titulo}. {resumen}" if titulo and resumen else (titulo or resumen)
            
            with st.spinner("Clasificando artículo..."):
                try:
                    # Predecir probabilidades
                    probabilidades = st.session_state.classifier.predict_proba([texto_completo])[0]
                    
                    # Mostrar resultados
                    st.success("✅ Clasificación completada")
                    
                    # Crear gráfico de barras
                    fig = px.bar(
                        x=list(probabilidades.keys()),
                        y=list(probabilidades.values()),
                        title="Probabilidades por Dominio Médico",
                        labels={"x": "Dominio", "y": "Probabilidad"},
                        color=list(probabilidades.values()),
                        color_continuous_scale="viridis"
                    )
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Error en la clasificación: {str(e)}")
    
    with col2:
        # Panel de información
        st.markdown("### 📋 Dominios Médicos")
        
        for domain in MEDICAL_DOMAINS:
            st.markdown(f"""
            <div class="domain-card">
                <strong>{domain}</strong><br>
                <small>Especialidad médica objetivo</small>
            </div>
            """, unsafe_allow_html=True)

def procesamiento_lotes():
    st.header("📊 Procesamiento por Lotes")
    
    # Upload de archivo
    uploaded_file = st.file_uploader(
        "Cargar archivo CSV",
        type=['csv'],
        help="El archivo debe contener columnas 'title' y 'abstract'"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Archivo cargado: {len(df)} registros")
            
            # Mostrar preview
            st.subheader("Vista previa de datos")
            st.dataframe(df.head())
            
            # Validar columnas
            required_cols = ['title', 'abstract']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                st.error(f"❌ Faltan columnas requeridas: {missing_cols}")
                return
            
            if st.button("🚀 Procesar Lote"):
                if not st.session_state.classifier.is_trained:
                    st.error("⚠️ El modelo no está entrenado.")
                    return
                
                with st.spinner("Procesando lote..."):
                    # Combinar título y resumen
                    textos = []
                    for _, row in df.iterrows():
                        texto = f"{row.get('title', '')}. {row.get('abstract', '')}"
                        textos.append(texto)
                    
                    # Predecir
                    predicciones = st.session_state.classifier.predict(textos)
                    probabilidades = st.session_state.classifier.predict_proba(textos)
                    
                    # Crear DataFrame de resultados
                    resultados = df.copy()
                    resultados['predicciones'] = [';'.join(pred) for pred in predicciones]
                    
                    # Agregar probabilidades
                    for domain in MEDICAL_DOMAINS:
                        resultados[f'prob_{domain}'] = [
                            prob.get(domain, 0.0) for prob in probabilidades
                        ]
                    
                    st.success("✅ Procesamiento completado")
                    
                    # Mostrar resultados
                    st.subheader("Resultados")
                    st.dataframe(resultados)
                    
                    # Botón de descarga
                    csv = resultados.to_csv(index=False)
                    st.download_button(
                        label="📥 Descargar Resultados CSV",
                        data=csv,
                        file_name="clasificacion_resultados.csv",
                        mime="text/csv"
                    )
                    
                    # Estadísticas
                    st.subheader("📊 Estadísticas del Lote")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Total Procesados", len(resultados))
                    
                    with col2:
                        avg_confidence = np.mean([
                            max(prob.values()) for prob in probabilidades
                        ])
                        st.metric("Confianza Promedio", f"{avg_confidence:.2%}")
                    
                    with col3:
                        multi_label = sum(1 for pred in predicciones if len(pred) > 1)
                        st.metric("Multi-etiqueta", f"{multi_label} ({multi_label/len(predicciones):.1%})")
        
        except Exception as e:
            st.error(f"Error al procesar archivo: {str(e)}")

def entrenamiento_modelo():
    st.header("🎯 Entrenamiento del Modelo")
    
    # Upload de datos de entrenamiento
    uploaded_file = st.file_uploader(
        "Cargar datos de entrenamiento",
        type=['csv'],
        help="El archivo debe contener columnas 'title', 'abstract' y 'labels' (separadas por ;)"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ Datos cargados: {len(df)} registros")
            
            # Validar columnas
            required_cols = ['title', 'abstract', 'labels']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                st.error(f"❌ Faltan columnas requeridas: {missing_cols}")
                return
            
            # Mostrar estadísticas de datos
            st.subheader("📊 Estadísticas de Datos")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Artículos", len(df))
            
            with col2:
                avg_length = df['abstract'].str.len().mean()
                st.metric("Longitud Promedio Abstract", f"{avg_length:.0f} chars")
            
            with col3:
                # Contar etiquetas
                all_labels = []
                for labels_str in df['labels']:
                    if pd.notna(labels_str):
                        all_labels.extend(str(labels_str).split(';'))
                unique_labels = len(set(all_labels))
                st.metric("Etiquetas Únicas", unique_labels)
            
            # Botón de entrenamiento
            if st.button("🚀 Entrenar Modelo"):
                with st.spinner("Entrenando modelo..."):
                    try:
                        # Entrenar
                        metrics = st.session_state.classifier.train(df)
                        
                        st.success("✅ Entrenamiento completado")
                        
                        # Mostrar métricas
                        st.subheader("📈 Métricas de Entrenamiento")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("F1 Macro", f"{metrics['f1_macro']:.3f}")
                        
                        with col2:
                            st.metric("F1 Micro", f"{metrics['f1_micro']:.3f}")
                        
                        with col3:
                            st.metric("Exact Match", f"{metrics['exact_match']:.3f}")
                        
                        with col4:
                            st.metric("Hamming Loss", f"{metrics['hamming_loss']:.3f}")
                        
                        # Guardar modelo
                        model_path = MODELS_DIR / "trained_model.joblib"
                        st.session_state.classifier.save_model(str(model_path))
                        st.info(f"💾 Modelo guardado en: {model_path}")
                        
                    except Exception as e:
                        st.error(f"Error en entrenamiento: {str(e)}")
        
        except Exception as e:
            st.error(f"Error al cargar datos: {str(e)}")

def metricas_evaluacion():
    st.header("📈 Métricas y Evaluación")
    
    if not st.session_state.classifier.is_trained:
        st.warning("⚠️ No hay modelo entrenado para mostrar métricas.")
        return
    
    st.info("🔄 Funcionalidad de métricas detalladas en desarrollo...")
    
    # Placeholder para métricas futuras
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Métricas por Clase")
        # Aquí se mostrarían métricas detalladas por clase
        
    with col2:
        st.subheader("📊 Matrices de Confusión")
        # Aquí se mostrarían las matrices de confusión

def documentacion():
    st.header("📚 Documentación del Sistema")
    
    st.markdown("""
    ## 🎯 Objetivo del Proyecto
    
    Sistema de clasificación automática de literatura médica para el **AI + Data Challenge 2025**.
    
    ### 📋 Dominios de Clasificación
    - **Cardiovascular**: Enfermedades del corazón y sistema circulatorio
    - **Neurológico**: Trastornos del sistema nervioso
    - **Hepatorrenal**: Enfermedades hepáticas y renales  
    - **Oncológico**: Cáncer y tumores malignos
    
    ### 🔧 Metodología
    
    1. **Preprocesamiento**: Limpieza y normalización de texto médico
    2. **Vectorización**: TF-IDF con n-gramas (1,2)
    3. **Clasificación**: Regresión Logística multietiqueta (One-vs-Rest)
    4. **Evaluación**: F1-Score macro/micro, Exact Match, Hamming Loss
    
    ### 📊 Métricas de Evaluación
    
    - **F1-Score Macro**: Promedio no ponderado de F1 por clase
    - **F1-Score Micro**: F1 global considerando todos los casos
    - **Exact Match**: Porcentaje de predicciones exactas
    - **Hamming Loss**: Fracción de etiquetas incorrectas
    
    ### 🚀 Uso del Sistema
    
    1. **Entrenamiento**: Cargar datos con etiquetas en formato CSV
    2. **Clasificación Individual**: Ingresar título y abstract
    3. **Procesamiento por Lotes**: Cargar archivo CSV para clasificar múltiples artículos
    
    ### 📁 Formato de Datos
    
    **Archivo de Entrenamiento:**
    ```csv
    title,abstract,labels
    "Título del artículo","Resumen del artículo","Cardiovascular;Neurológico"
