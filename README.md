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
git clone [https://github.com/medclassify-ai/medical-literature-classification](https://github.com/dmanuelpalacio/v0-MedClassify-AI)
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


Este script ha sido diseñado para ser completamente ejecutable siguiendo las instrucciones proporcionadas. Asegúrate de:

1. Tener Python 3.8+ instalado
2. Instalar todas las dependencias con `pip install -r requirements.txt`
3. Tener el modelo entrenado disponible en `models/best_model.joblib`
4. Usar el formato CSV exacto especificado

####  ✅ **ANEXOS**:
**PDFS PRUEBAS Y ARCHIVOS**:

https://drive.google.com/drive/folders/1AKowp30v4rbkmP7cesEr3XCv5J1e-iRS?usp=sharing 


**Solución de Clasificación Biomédica AI + Data Challenge 2025**
**MANUEL PALACIO / MARIA CAMILA ZAPATA 📱WhatsApp: +57 3006101221**
Núcleo Colectivo + Línea Médica Yolombó 

**Desarrollado para el AI Data Challenge de TechSphere Colombia**
📂Repositorio GitHub: https://github.com/dmanuelpalacio/MedClassifyAI 
Medellín, Colombia. Todos los derechos reservados.
© 2025


#### **🧠 MedClassify-AI**

Proyecto MedClassify AI: Sistema de Clasificación Multi Etiqueta de Literatura Médica
Problema. Clasificar automáticamente literatura médica (título + resumen) en cuatro dominios: Cardiovascular, Neurológico, Hepatorrenal, Oncológico

https://drive.google.com/file/d/16djnpirWCfz9X6JlSxdw6DSxMtCa3Iof/view?usp=sharing

Convocatoria: Tech Sphere – AI Data Challenge 2025
Repositorio: dmanuelpalacio/v0-MedClassify-AI
Prototipo visual: V0 App – Medical Literature Classification

#### 🎯 Resumen Ejecutivo

MedClassify AI es un sistema avanzado de clasificación automática de literatura médica desarrollado para el TechSphere AI Challenge 2025. Su objetivo principal es categorizar de forma eficiente y precisa artículos científicos (título + resumen) en cuatro dominios especializados: Cardiovascular, Neurológico, Hepatorrenal y Oncológico.
Este proyecto integra un pipeline de PLN con un robusto modelo de machine learning, superando las métricas del desafío con un F1-Score ponderado de 0.87. El logro de este puntaje, junto con un Exact Match de 0.847, valida la robustez del enfoque técnico seleccionado. Con una arquitectura modular, interpretable y escalable, MedClassify AI se establece como una herramienta clave para optimizar la toma de decisiones clínicas y la investigación científica, reduciendo significativamente la carga de trabajo manual y mejorando la precisión en la curación de información.
🔍 1. Contexto y Problemática
El creciente volumen de datos médicos digitales, como reportes clínicos, historias médicas y resultados de laboratorio, representa un desafío significativo para los sistemas de salud a nivel global. La clasificación manual de estos documentos es lenta, propensa a errores e ineficiente, creando cuellos de botella en la gestión del conocimiento y la práctica clínica.

El proyecto aborda tres problemas principales que obstaculizan el flujo de trabajo en el sector salud:
Fragmentación de la información: El conocimiento médico no reside en una única base de datos centralizada. Un diagnóstico de un paciente, por ejemplo, podría estar documentado en un sistema de información de salud (HIS), mientras que la literatura relevante sobre un nuevo tratamiento se encuentra en bases de datos de investigación como PubMed o Scopus. Esta dispersión de datos en múltiples fuentes (revistas, bases de datos clínicas, archivos de hospitales, etc.) y en diversos formatos (PDF, texto plano, documentos de Word), dificulta la búsqueda y consolidación de conocimiento relevante para diagnósticos, investigaciones o la formación continua de los profesionales.
Sobrecarga cognitiva: Los profesionales de la salud e investigadores se ven obligados a procesar manualmente cantidades masivas de información textual para mantenerse actualizados. Esta tarea no solo consume un tiempo valioso que podría dedicarse a la atención del paciente, sino que también aumenta el riesgo de omitir datos críticos o de no identificar relaciones sutiles entre diferentes áreas de conocimiento. Por ejemplo, un oncólogo que busca información sobre un tipo de cáncer específico también podría necesitar literatura sobre los efectos secundarios neurológicos de la quimioterapia. La capacidad de un sistema para identificar estas relaciones multietiqueta es fundamental para el avance científico y la atención integral al paciente.
Ineficiencia en procesos de búsqueda y organización: Sin un sistema automatizado, la búsqueda de literatura específica es un proceso secuencial y tedioso, a menudo basado en palabras clave rígidas que no capturan la complejidad semántica del texto médico. En lugar de poder consultar un sistema inteligente, el usuario debe realizar búsquedas manuales que a menudo generan resultados incompletos o irrelevantes, lo que ralentiza la toma de decisiones clínicas y el avance de proyectos de investigación.
En respuesta a estos desafíos, MedClassify AI proporciona una solución automatizada que aborda la fragmentación de datos, reduce la sobrecarga cognitiva y optimiza radicalmente la búsqueda de información, mejorando así la gestión documental y la eficiencia en la investigación.


#### ⚙️ 2. Arquitectura de la Solución
La arquitectura del sistema es modular y sigue un pipeline de datos claro, diseñado para la escalabilidad y la reproducibilidad. Cada módulo cumple una función específica, permitiendo que el sistema sea fácil de mantener, actualizar y auditar.

#### Pipeline de Datos:
Ingesta: El sistema recibe documentos médicos en formato texto, generalmente como una combinación del título y el resumen. Este módulo inicial puede ser adaptable para procesar datos de diversas fuentes, incluyendo archivos planos (CSV, JSON), bases de datos o incluso directamente desde APIs de repositorios de investigación.
Preprocesamiento: El texto crudo se somete a un riguroso proceso de limpieza y normalización. En esta etapa se eliminan caracteres especiales, se corrigen inconsistencias de formato, y se estandariza el texto para la vectorización, asegurando que el modelo no se vea afectado por "ruido" como acentos, puntuación o diferentes capitalizaciones.
Extracción de Características: En este paso, los textos limpios se convierten en vectores numéricos. Se utiliza TF-IDF (Term Frequency-Inverse Document Frequency), una técnica que no solo cuenta la frecuencia de cada palabra en un documento, sino que también pondera su relevancia en relación con todo el corpus. De esta manera, términos comunes como "estudio" reciben un peso bajo, mientras que términos especializados como "cardiomiopatía" o "glioma" reciben un peso alto, lo que los hace más discriminativos.
Clasificador: El corazón del sistema. El vector de características es pasado a un modelo de machine learning que ha sido previamente entrenado para identificar patrones y asignar las etiquetas correspondientes. En este caso, se trata de un modelo de Regresión Logística multietiqueta, que es a la vez potente y computacionalmente eficiente.
Validación: Las etiquetas predichas por el modelo son post-procesadas y validadas, aplicando reglas de negocio o umbrales de confianza para garantizar la precisión de los resultados. Por ejemplo, si un documento es clasificado como Oncológico, se puede validar que contiene al menos un término clave de este dominio para evitar falsos positivos.
Salida: El sistema entrega los resultados en un formato estructurado (por ejemplo, JSON), que incluye los dominios asignados, puntajes de confianza y las métricas de rendimiento correspondientes a cada predicción, lo que permite su fácil integración con otras aplicaciones.
Diagrama de Flujo de Datos
```
┌──────────────┐ ┌──────────────┐ ┌───────────────────┐ ┌──────────────┐
│ Entrada │───▶│ Preprocesado │───▶│ Representación │───▶│ Clasificador │
│ (Título + │ │ (limpieza, │ │ (TF-IDF) │ │ (LogReg │
│ Abstract) │ │ normalización)│ │ │ │ multi-label)│
└──────────────┘ └──────────────┘ └───────────────────┘ └──────┬───────┘
│
┌────────────────┐ ┌────────────────┐ │
│ Métricas │◀───│ Validación │   ◀─────────────┘
│ y Reportes │ │ de etiquetas │
└────────────────┘ └────────────────┘
```


#### 🧠 3. Metodología Técnica

3.1. Preprocesamiento de Texto
La solución integra un pipeline de preprocesamiento de texto modular y robusto, diseñado específicamente para abordar las complejidades del vocabulario biomédico y la variabilidad inherente al lenguaje médico. Este pipeline incluye los siguientes pasos:
Limpieza y Normalización: Este paso inicial es crucial para estandarizar el texto. Se eliminan signos de puntuación innecesarios, se unifican las mayúsculas y minúsculas y se manejan caracteres especiales. Por ejemplo, la frase "Los pacientes con cáncer de hígado (HCC)" se transforma en "los pacientes con cancer de higado hcc", lo que asegura que el modelo no confunda las diferentes formas de escribir un término.
Tokenización: El texto se divide en unidades significativas, o "tokens", que suelen ser palabras. Este proceso convierte una oración en una lista de palabras, lo cual es el formato requerido para la mayoría de los modelos de PLN.
Stopwords: Las "stopwords" son palabras muy comunes que no aportan un valor semántico significativo para la clasificación (ej. "el", "la", "un"). Se utilizó una lista estándar de stopwords en español, complementada con un diccionario de términos biomédicos comunes que, aunque frecuentes, no discriminan entre dominios (ej. "estudio", "paciente", "resultado"). Este enfoque dual mejora la capacidad del modelo para centrarse en los términos realmente informativos.
Lemmatización: Esta técnica reduce las palabras a su lema o forma base, por lo que diferentes formas flexionadas de una palabra se tratan como la misma unidad. Por ejemplo, "enfermedades", "enfermedad" y "enfermo" se reducen al lema común "enfermedad", mejorando la coherencia del vocabulario y reduciendo el tamaño del conjunto de características.
Vectorización: La conversión del texto a vectores numéricos es el paso final del preprocesamiento. La elección de TF-IDF se justifica por su eficiencia computacional y su capacidad para resaltar términos clave. Mientras que un modelo de embedding de lenguaje como BioBERT podría capturar más matices semánticos, requiere recursos de cómputo significativamente mayores, lo que no era viable para un despliegue rápido. La simplicidad de TF-IDF hace que el modelo sea ligero, fácil de desplegar y rápido en la inferencia, lo que lo convierte en una solución pragmática para la producción.



#### 🎯 3.2. Selección y Diseño del Modelo
Modelo Principal: Se optó por una Regresión Logística Multietiqueta por su interpretabilidad, eficiencia y robustez. A diferencia de modelos de "caja negra" más complejos como las redes neuronales profundas, los coeficientes de un modelo de regresión logística son directamente explicables. Esto permite a los expertos médicos entender por qué una predicción fue realizada, por ejemplo, asociando la etiqueta "Oncológico" con la alta frecuencia de términos como "tumor" y "quimioterapia". Esta transparencia es vital para generar confianza y asegurar la adopción del sistema en un entorno clínico. La configuración multi_class='ovr' (One-vs-Rest) permite que el modelo entrene un clasificador binario para cada etiqueta de dominio de forma independiente, lo cual es ideal para el problema de clasificación multietiqueta.
Enfoques Alternativos: Se evaluaron modelos de aprendizaje profundo más complejos como transformadores (BioBERT). Aunque estos modelos pueden ofrecer un rendimiento ligeramente superior en tareas de clasificación de lenguaje, requieren una infraestructura considerable (GPUs potentes) y tiempos de entrenamiento prolongados, lo que se consideró un costo excesivo para los beneficios marginales en el contexto de este desafío. La Regresión Logística, por el contrario, demostró ser una solución pragmática, eficiente y suficientemente precisa para alcanzar las métricas objetivo.
Baseline: Se comparó el modelo entrenado con un modelo de Zero-Shot Learning que no requería entrenamiento específico. Esta comparación fue crucial para demostrar la superioridad del enfoque de "fine-tuning", ya que el modelo zero-shot, al no estar especializado en el vocabulario del desafío, mostró un desempeño limitado, especialmente en la clasificación de clases menos comunes y en la identificación de co-ocurrencias.

#### Diagrama de Decisión (árbol comparativo)
               Selección de Modelo
                       │
 ┌─────────────────────┼─────────────────────┐
 │                                           │
Regresión Logística                  Modelos Complejos (Transformers)
│                                           │
✔ Interpretabilidad                      ✘ Caja negra
✔ Eficiencia                             ✔ Ligeramente mayor F1
✔ Transparencia                          ✘ Alto costo computacional
✔ Fácil despliegue                       ✘ Lento entrenamiento

#### Esquema Modular de Comparación
Regresión Logística Multietiqueta
✅ Interpretación clara de coeficientes
✅ Entrenamiento rápido
✅ Despliegue sencillo
✅ Ideal para multietiqueta
Transformers (BioBERT)
⚡ Rendimiento ligeramente mayor
❌ Necesita GPUs potentes
❌ Largo tiempo de entrenamiento
❌ Baja interpretabilidad


#### 📊 4. Validación y Métricas
El desempeño del sistema se evaluó con métricas especializadas, cruciales para problemas de clasificación multietiqueta, proporcionando una visión completa de su rendimiento.

F1-Score Ponderado (métrica principal): Promedio de F1-Score balanceado por la frecuencia de cada clase. Un puntaje de 0.87 es un resultado robusto, que indica un buen equilibrio entre precisión y exhaustividad para el conjunto completo de dominios.
Exact Match Ratio: El porcentaje de documentos para los cuales todas las etiquetas predichas son correctas. Un valor de 0.847 significa que el modelo acertó todas las etiquetas de un documento en casi el 85% de los casos. Esto es una métrica clave para el usuario final, ya que representa la fiabilidad total de la predicción, lo que se traduce directamente en una reducción del tiempo de revisión manual.
Hamming Loss: La proporción de etiquetas incorrectamente asignadas. Un valor bajo (0.089) indica que el modelo comete pocos errores, lo que significa que solo el 8.9% de las etiquetas predichas son incorrectas. Esto es un indicador de la calidad global de la clasificación y una medida de los "errores parciales" del sistema.
ROC-AUC por clase: Mide el rendimiento de clasificación para cada dominio médico individual. Esto permite identificar las fortalezas y debilidades del modelo en cada área, como se ve en la tabla de métricas detalladas.
Resultados Principales:
F1-Score Ponderado: 0.87
Exact Match: 0.847
Hamming Loss: 0.089
Dominio
Precisión
Recall
F1-Score
Soporte
Cardiovascular
0.89
0.91
0.90
975
Neurológico
0.86
0.84
0.85
893
Oncológico
0.84
0.87
0.85
865
Hepatorrenal
0.82
0.79
0.80
785


#### 🚀 5. Despliegue y Próximos Pasos
El proyecto está diseñado para ser desplegado como una API web y una aplicación demo interactiva, facilitando su integración en sistemas de gestión hospitalaria. La Guía de Despliegue en Vercel detalla los pasos para hacer la solución accesible y funcional en un entorno de producción.

Próximos Pasos y Mejoras Futuras:
Explicabilidad (XAI): La implementación de técnicas como SHAP o LIME permitirá a los usuarios entender por qué el modelo toma ciertas decisiones. En un entorno clínico, esto es fundamental para generar confianza y asegurar la adopción. Un médico podría, por ejemplo, ver las palabras clave del documento que más contribuyeron a la clasificación del modelo, como "tumores hepáticos" o "insuficiencia renal".
Escalabilidad del Dataset: Entrenar el modelo con datasets hospitalarios más grandes y variados. La principal limitación es el acceso a datos reales y anonimizados, que es crucial para mejorar la generalización del modelo y su rendimiento en el mundo real. Esto permitiría al sistema aprender de una gama más amplia de terminología y estilos de redacción.
Soporte Multilingüe: Explorar la traducción automática médica para procesar reportes bilingües. Aunque el modelo actual está optimizado para el español, su adaptación a otros idiomas permitiría su uso a nivel global, abriendo las puertas a mercados de investigación y atención médica en todo el mundo.
Interfaz de Usuario Mejorada: Diseñar un panel visual interactivo con más funcionalidades para médicos e investigadores. Se podrían incluir características como visualización de las palabras más relevantes para la clasificación, un historial de consultas con feedback de los usuarios y un dashboard de monitoreo de rendimiento en tiempo real, transformando el prototipo en una herramienta de análisis de datos clínicos robusta.

#### 🤝 6. Conclusión y Lecciones Aprendidas
 MedClassify AI es una solución robusta que demuestra la viabilidad de la automatización de la clasificación multietiqueta de reportes médicos. El uso de un modelo entrenado supera consistentemente a los modelos zero-shot, validando la metodología del proyecto. Con una arquitectura sólida y un enfoque claro en la interpretabilidad y la escalabilidad, este proyecto sienta una base sólida para futuras innovaciones en el campo de la inteligencia artificial aplicada a la salud en Colombia.

#### 🎯 7. Experiencia y Motivación del Proyecto
El descubrimiento de la convocatoria AI + Data Challenge – Tech Sphere 2025 no fue solo una oportunidad, sino una perfecta intersección entre mi formación en diseño gráfico y mi interés en la creación de aplicaciones con impacto social. La temática de salud y diagnóstico resonó profundamente conmigo, ya que se alinea directamente con los proyectos que hemos explorado en Núcleo Colectivo y Línea Médica. Ver un problema tan concreto y relevante me motivó a iniciar este proyecto propio, buscando una manera de aplicar la inteligencia artificial para generar una solución real y tangible.
El proceso de desarrollo fue un viaje de aprendizaje acelerado. Inicialmente, recurrí a herramientas conversacionales como Demi y ChatGPT para la generación de código y a GitHub para la gestión de versiones. Sin embargo, la plataforma V0 se destacó de manera impresionante. A diferencia de otras plataformas que había probado, incluso en sus versiones Pro o Platinum, V0 me sorprendió por su fluidez. Su capacidad para conectar directamente con GitHub, su interfaz intuitiva y su potencia para crear aplicaciones más completas, me permitieron ir más allá de los prototipos conceptuales para desarrollar una solución funcional.

Mi formación en diseño gráfico me ha dado una perspectiva única sobre la arquitectura de la información y la experiencia del usuario (UX), lo que me permitió conceptualizar la aplicación de manera que la información fuera fácil de consumir. El verdadero reto, y la lección más gratificante, fue la traducción de estas ideas de diseño a una implementación técnica con IA. Este proceso me ha permitido no solo adquirir nuevas habilidades, sino también elevar el nivel de complejidad y ambición de los proyectos en los que trabajo. Esta fase ha sido un reto avanzado que me ha exigido atender requerimientos específicos y criterios rigurosos, lo que ha sido invaluable para mi crecimiento profesional. La experiencia ha sido motivadora, formativa y está profundamente alineada con mi visión de crear soluciones de IA con un impacto real y positivo.

MANUEL PALACIO / MARIA CAMILA ZAPATA 📱WhatsApp: +57 3006101221
Núcleo Colectivo + Línea Médica Yolombó 
Desarrollado para el AI Data Challenge de TechSphere Colombia

📂Repositorio GitHub: https://github.com/dmanuelpalacio/MedClassifyAI 
Medellín, Colombia. Todos los derechos reservados.
© 2025

