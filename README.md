... existing code ...

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

... existing code ...
\`\`\`

```python file="" isHidden
