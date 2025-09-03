## 🧠 MedClassify AI - Sistema de Clasificación de Literatura Médica
TechSphere AI Challenge 2025

Sistema avanzado de clasificación automática de literatura médica usando modelos de lenguaje pre-entrenados y técnicas de machine learning multietiqueta.

https://v0-landing-page-creation-rosy.vercel.app/

https://v0-medical-literature-classificatio-kappa.vercel.app/

## 🎯 Objetivo
Clasificar automáticamente artículos médicos (título + resumen) en cuatro dominios especializados:

Cardiovascular: Enfermedades del corazón y sistema circulatorio
Neurológico: Trastornos del sistema nervioso
Hepatorrenal: Enfermedades hepáticas y renales
Oncológico: Cáncer y tumores malignos

## 🌐 Despliegue en Vercel - Instrucciones Completas

### 🎯 Objetivo del Despliegue
Desplegar la aplicación de clasificación médica como una API web accesible que funcione tanto como interfaz de usuario como endpoints API para integración.

### 📋 Requisitos Previos
\`\`\`bash
# Instalar Vercel CLI
npm install -g vercel

# Verificar instalación
vercel --version
\`\`\`

### 🚀 Pasos de Despliegue

#### 1. Preparación del Proyecto
\`\`\`bash
# Clonar y preparar el repositorio
git clone https://github.com/medclassify-ai/medical-literature-classification
cd medical-literature-classification

# Instalar dependencias
npm install
pip install -r requirements.txt
\`\`\`

#### 2. Configuración de Vercel
\`\`\`bash
# Inicializar proyecto en Vercel
vercel login
vercel init

# Configurar proyecto
vercel --prod
\`\`\`

#### 3. Variables de Entorno (Opcional)
\`\`\`bash
# Configurar variables si es necesario
vercel env add PYTHON_VERSION 3.9
vercel env add NODE_VERSION 18
\`\`\`

### 🔗 Endpoints API Disponibles

#### Endpoint Principal: `/api/predict`
**Método**: POST  
**URL**: `https://tu-proyecto.vercel.app/api/predict`

**Entrada**:
\`\`\`json
{
  "title": "Efficacy of ACE inhibitors in reducing cardiovascular mortality",
  "abstract": "This study evaluates the effectiveness of ACE inhibitors in patients with cardiovascular disease..."
}
\`\`\`

**Salida**:
\`\`\`json
{
  "scores": {
    "Cardiovascular": 0.87,
    "Neurológico": 0.12,
    "Hepatorrenal": 0.08,
    "Oncológico": 0.05
  },
  "labels": ["Cardiovascular"],
  "confidence": 0.75,
  "processing_time": "0.15s",
  "terms_found": 12
}
\`\`\`

#### Endpoint de Lote: `/api/predict-batch`
**Método**: POST  
**URL**: `https://tu-proyecto.vercel.app/api/predict-batch`

**Entrada CSV**:
\`\`\`csv
title,abstract
"Cardiac surgery outcomes","Analysis of post-operative complications..."
"Brain tumor classification","MRI-based classification of gliomas..."
\`\`\`

**Salida**:
\`\`\`json
{
  "results": [
    {
      "id": 1,
      "title": "Cardiac surgery outcomes",
      "predicted_domains": ["Cardiovascular"],
      "scores": {...},
      "confidence": 0.82
    }
  ],
  "batch_stats": {
    "domain_distribution": {...},
    "average_confidence": 0.78,
    "processing_time": "1.2s"
  },
  "total_processed": 2
}
\`\`\`

### 🧪 Ejemplos de Uso con cURL

#### Clasificación Individual
\`\`\`bash
curl -X POST https://tu-proyecto.vercel.app/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Neurobiología del sueño y su importancia",
    "abstract": "El sueño es un proceso fisiológico fascinante que involucra múltiples estructuras cerebrales y neurotransmisores..."
  }'
\`\`\`

#### Clasificación por Lotes (JSON)
\`\`\`bash
curl -X POST https://tu-proyecto.vercel.app/api/predict-batch \
  -H "Content-Type: application/json" \
  -d '{
    "articles": [
      {
        "title": "Cardiac arrhythmias treatment",
        "abstract": "Study of beta-blockers effectiveness..."
      },
      {
        "title": "Liver cirrhosis progression",
        "abstract": "Analysis of hepatic fibrosis markers..."
      }
    ]
  }'
\`\`\`

#### Clasificación por Lotes (CSV)
\`\`\`bash
curl -X POST https://tu-proyecto.vercel.app/api/predict-batch \
  -H "Content-Type: text/csv" \
  --data-binary @articles.csv
\`\`\`

### ⚙️ Configuración Técnica

#### Archivo `vercel.json`
\`\`\`json
{
  "version": 2,
  "public": true,
  "functions": {
    "api/predict.py": {
      "runtime": "python3.9"
    },
    "api/predict-batch.py": {
      "runtime": "python3.9"
    }
  },
  "routes": [
    {
      "src": "/api/predict",
      "dest": "/api/predict.py"
    },
    {
      "src": "/api/predict-batch", 
      "dest": "/api/predict-batch.py"
    },
    {
      "src": "/(.*)",
      "dest": "/$1"
    }
  ],
  "build": {
    "env": {
      "PYTHONPATH": "."
    }
  }
}
\`\`\`

#### Archivo `package.json` (Scripts de Despliegue)
\`\`\`json
{
  "name": "medclassify-ai",
  "scripts": {
    "build": "next build",
    "dev": "next dev",
    "start": "next start",
    "deploy": "vercel --prod",
    "deploy-preview": "vercel"
  }
}
\`\`\`

### 🔧 Comandos de Despliegue

#### Despliegue de Producción
\`\`\`bash
# Despliegue completo a producción
npm run deploy

# O directamente con Vercel CLI
vercel --prod
\`\`\`

#### Despliegue de Preview
\`\`\`bash
# Despliegue de prueba (preview)
npm run deploy-preview

# O directamente
vercel
\`\`\`

#### Verificación del Despliegue
\`\`\`bash
# Verificar estado del despliegue
vercel ls

# Ver logs en tiempo real
vercel logs tu-proyecto.vercel.app
\`\`\`

### 🧪 Testing del Despliegue

#### Script de Prueba Automatizada
\`\`\`bash
# Crear script de prueba
cat > test_deployment.sh << 'EOF'
#!/bin/bash
BASE_URL="https://tu-proyecto.vercel.app"

echo "Testing individual prediction..."
curl -X POST $BASE_URL/api/predict \
  -H "Content-Type: application/json" \
  -d '{"title":"Test cardiac study","abstract":"Analysis of heart function"}' \
  | jq .

echo "Testing batch prediction..."
curl -X POST $BASE_URL/api/predict-batch \
  -H "Content-Type: application/json" \
  -d '{"articles":[{"title":"Brain study","abstract":"Neurological analysis"}]}' \
  | jq .
EOF

chmod +x test_deployment.sh
./test_deployment.sh
\`\`\`

### 📊 Monitoreo y Métricas

#### Dashboard de Vercel
- **URL**: https://vercel.com/dashboard
- **Métricas disponibles**:
  - Requests por minuto
  - Tiempo de respuesta
  - Errores y logs
  - Uso de recursos

#### Logs en Tiempo Real
\`\`\`bash
# Ver logs de la aplicación
vercel logs --follow

# Filtrar logs por función
vercel logs --follow --scope=api/predict.py
\`\`\`

### 🔒 Configuración de Seguridad

#### CORS y Headers
Los endpoints ya incluyen configuración CORS:
\`\`\`python
self.send_header('Access-Control-Allow-Origin', '*')
self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
self.send_header('Access-Control-Allow-Headers', 'Content-Type')
\`\`\`

#### Rate Limiting (Opcional)
\`\`\`bash
# Configurar límites en Vercel
vercel env add RATE_LIMIT_REQUESTS 100
vercel env add RATE_LIMIT_WINDOW 60
\`\`\`

### 🚨 Troubleshooting

#### Problemas Comunes

1. **Error de Python Runtime**:
\`\`\`bash
# Verificar versión de Python en vercel.json
"runtime": "python3.9"
\`\`\`

2. **Timeout en Requests**:
\`\`\`bash
# Optimizar tiempo de procesamiento
# Los endpoints están optimizados para <10s
\`\`\`

3. **Errores de CORS**:
\`\`\`bash
# Verificar headers en las respuestas API
# Ya configurados en el código
\`\`\`

#### Comandos de Diagnóstico
\`\`\`bash
# Verificar configuración
vercel inspect tu-proyecto.vercel.app

# Revisar builds
vercel builds

# Descargar logs
vercel logs tu-proyecto.vercel.app > deployment.log
\`\`\`

### 📱 Interfaz Web

#### URL Principal
- **Aplicación**: https://tu-proyecto.vercel.app
- **Características**:
  - Clasificación en tiempo real
  - Carga de archivos CSV/PDF/TXT
  - Visualización de métricas
  - Análisis de confiabilidad
  - Descarga de resultados

#### Funcionalidades Disponibles
1. **Clasificar Texto**: Entrada manual de título + abstract
2. **Cargar Archivo**: Procesamiento de documentos médicos
3. **Resumen con IA**: Generación automática de resúmenes
4. **Métricas**: Dashboard con estadísticas del sistema

### 🎯 URLs de Ejemplo

Una vez desplegado, las URLs serán:
- **App Principal**: `https://medclassify-ai.vercel.app`
- **API Individual**: `https://medclassify-ai.vercel.app/api/predict`
- **API Lotes**: `https://medclassify-ai.vercel.app/api/predict-batch`

### 📋 Checklist de Despliegue

- [ ] Vercel CLI instalado y configurado
- [ ] Repositorio GitHub conectado
- [ ] Variables de entorno configuradas (si aplica)
- [ ] Tests de endpoints funcionando
- [ ] Interfaz web accesible
- [ ] Documentación actualizada
- [ ] Monitoreo configurado

---

**¡Tu aplicación de clasificación médica está lista para producción en Vercel!** 🚀

## 📊 Evaluación y Predicción

Este repositorio incluye el script `evaluate_and_predict.py` para evaluar el modelo entrenado sobre un archivo CSV y generar las predicciones requeridas por la convocatoria.

### Formato del CSV de entrada
El archivo debe contener las columnas obligatorias:
- `title` - Título del artículo médico
- `abstract` - Resumen/abstract del artículo
- `group` - Etiqueta real del dominio médico

### Ejemplo de CSV de entrada
\`\`\`csv
title,abstract,group
"Efficacy of ACE inhibitors in reducing cardiovascular mortality","This study evaluates the effectiveness of ACE inhibitors in patients with heart failure and reduced ejection fraction...","Cardiovascular"
"Neurobiología del sueño y su importancia","El sueño es un proceso fisiológico fascinante que involucra múltiples estructuras cerebrales y neurotransmisores...","Neurológico"
"Hepatic fibrosis progression markers","Analysis of biomarkers for hepatic fibrosis progression in patients with chronic liver disease and cirrhosis...","Hepatorrenal"
"Breast cancer treatment outcomes","Evaluation of chemotherapy effectiveness in triple-negative breast cancer patients with adjuvant therapy...","Oncológico"
\`\`\`

### Uso del Script de Evaluación

#### 1. Preparación del entorno
\`\`\`bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
\`\`\`

#### 2. Ejecutar evaluación y predicción
\`\`\`bash
python evaluate_and_predict.py --input data/test.csv --model models/best_model.joblib --out-dir outputs
\`\`\`

#### 3. Parámetros del script
- `--input`: Ruta al archivo CSV de entrada (obligatorio)
- `--model`: Ruta al modelo entrenado en formato joblib (obligatorio)  
- `--out-dir`: Directorio de salida para resultados (por defecto: "outputs")

### Salida del Script

El script genera los siguientes archivos en el directorio de salida:

#### 1. `predictions.csv`
Archivo CSV con una columna adicional `group_predicted`:
\`\`\`csv
title,abstract,group,group_predicted
"Efficacy of ACE inhibitors...","This study evaluates...","Cardiovascular","Cardiovascular"
"Neurobiología del sueño...","El sueño es un proceso...","Neurológico","Neurológico"
\`\`\`

#### 2. `metrics.json`
Archivo JSON con métricas de desempeño:
\`\`\`json
{
  "f1_weighted": 0.89,
  "hamming_loss": 0.11,
  "exact_match": 0.85,
  "labels": ["Cardiovascular", "Neurológico", "Hepatorrenal", "Oncológico"],
  "precision_per_label": [0.92, 0.88, 0.85, 0.90],
  "recall_per_label": [0.90, 0.87, 0.83, 0.88],
  "f1_per_label": [0.91, 0.87, 0.84, 0.89]
}
\`\`\`

#### 3. `confusion_matrix.png`
Matriz de confusión visual guardada como imagen PNG.

### Métricas en Consola

Durante la ejecución, el script muestra:

\`\`\`bash
=== Métricas de Desempeño ===
F1 weighted: 0.89
Hamming Loss: 0.11
Exact Match: 0.85

Saved predictions to outputs/predictions.csv
Saved metrics to outputs/metrics.json
Saved confusion matrix to outputs/confusion_matrix.png
\`\`\`

### Ejemplo Completo de Ejecución

\`\`\`bash
# 1. Preparar datos de prueba
mkdir -p data
cat > data/test.csv << 'EOF'
title,abstract,group
"Cardiac arrhythmias in elderly patients","Study of atrial fibrillation management in patients over 65 years old with comorbidities","Cardiovascular"
"Sleep disorders and cognitive function","Analysis of the relationship between sleep quality and memory consolidation in young adults","Neurológico"
"Liver transplant outcomes","Evaluation of post-transplant survival rates and complications in hepatocellular carcinoma patients","Hepatorrenal"
"Chemotherapy resistance mechanisms","Investigation of drug resistance pathways in metastatic colorectal cancer treatment","Oncológico"
EOF

# 2. Ejecutar evaluación
python evaluate_and_predict.py --input data/test.csv --model models/best_model.joblib --out-dir results

# 3. Verificar resultados
ls results/
# predictions.csv  metrics.json  confusion_matrix.png

# 4. Ver métricas
cat results/metrics.json | python -m json.tool
\`\`\`

### 🧪 Tests Automatizados

Para validar que el script funciona correctamente:

\`\`\`bash
# Ejecutar tests unitarios
pytest tests/test_pipeline.py -v

# Ejecutar todos los tests
pytest tests/ -v
\`\`\`

Los tests verifican:
- ✅ Validación de formato CSV (columnas obligatorias)
- ✅ Carga y predicción con modelo válido
- ✅ Generación de archivos de salida
- ✅ Presencia de columna `group_predicted`
- ✅ Cálculo de métricas requeridas
- ✅ Manejo de errores (modelo inexistente, CSV inválido)

### 📋 Requisitos de la Convocatoria

Este script cumple con todos los requisitos especificados:

- ✅ **Carga CSV**: Acepta archivos con columnas `title`, `abstract`, `group`
- ✅ **Predicción**: Genera columna `group_predicted` en la salida
- ✅ **Métrica principal**: Calcula F1-score ponderado (weighted)
- ✅ **Métricas adicionales**: Hamming Loss, Exact Match, precisión/recall por clase
- ✅ **Matriz de confusión**: Genera y guarda visualización
- ✅ **Reproducibilidad**: Script ejecutable con instrucciones claras
- ✅ **Manejo de errores**: Códigos de salida apropiados (0=éxito, 1=error)

### ⚠️ Nota Importante

**"Si no es posible ejecutar la solución, la prueba no será considerada."**

Este script ha sido diseñado para ser completamente ejecutable siguiendo las instrucciones proporcionadas. Asegúrate de:

1. Tener Python 3.8+ instalado
2. Instalar todas las dependencias con `pip install -r requirements.txt`
3. Tener el modelo entrenado disponible en `models/best_model.joblib`
4. Usar el formato CSV exacto especificado


📂 Repositorio GitHub: https://github.com/dmanuelpalacio/MedClassifyAI

📱 WhatsApp: +57 3006101221

**© 2025 MANUEL PALACIO / CAMILA ZAPATA**

**Núcleo Colectivo + Línea Médica Yolombó**

Medellín, Colombia. Todos los derechos reservados.
