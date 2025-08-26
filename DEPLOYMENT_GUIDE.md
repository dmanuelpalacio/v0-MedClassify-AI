# 🚀 Guía Completa de Despliegue - MedClassify AI

## Despliegue en Vercel

### Requisitos Previos
- Cuenta en [Vercel](https://vercel.com)
- Node.js 18+ instalado
- Git configurado

### Pasos de Despliegue

#### 1. Preparación del Repositorio
\`\`\`bash
# Clonar el repositorio
git clone https://github.com/medclassify-ai/medical-literature-classification
cd medical-literature-classification

# Verificar archivos de configuración
ls vercel.json package.json requirements.txt
\`\`\`

#### 2. Instalación de Vercel CLI
\`\`\`bash
# Instalar Vercel CLI globalmente
npm install -g vercel

# Verificar instalación
vercel --version
\`\`\`

#### 3. Configuración y Login
\`\`\`bash
# Login en Vercel
vercel login

# Seguir las instrucciones en el navegador
\`\`\`

#### 4. Despliegue Inicial
\`\`\`bash
# Despliegue de preview (desarrollo)
vercel

# Configurar proyecto cuando se solicite:
# - Set up and deploy? [Y/n] Y
# - Which scope? [tu-usuario]
# - Link to existing project? [y/N] N
# - Project name: medclassify-ai
# - Directory: ./
\`\`\`

#### 5. Despliegue a Producción
\`\`\`bash
# Despliegue a producción
vercel --prod

# URL de producción será mostrada
# Ejemplo: https://medclassify-ai.vercel.app
\`\`\`

### Configuración de Dominios Personalizados

#### Agregar Dominio Personalizado
\`\`\`bash
# Agregar dominio desde CLI
vercel domains add medclassify.ai

# O desde el dashboard de Vercel
# 1. Ir a Project Settings
# 2. Domains
# 3. Add Domain
\`\`\`

### Variables de Entorno

#### Configurar Variables (si necesarias)
\`\`\`bash
# Agregar variable de entorno
vercel env add ENVIRONMENT_VARIABLE

# Listar variables
vercel env ls
\`\`\`

### Endpoints API Disponibles

#### 1. Clasificación Individual
**URL**: `https://tu-proyecto.vercel.app/api/predict`
**Método**: POST
**Content-Type**: application/json

\`\`\`bash
curl -X POST https://medclassify-ai.vercel.app/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Efficacy of ACE inhibitors in reducing cardiovascular mortality",
    "abstract": "This randomized controlled trial evaluates the long-term effects of ACE inhibitors on cardiovascular outcomes in patients with hypertension and coronary artery disease."
  }'
\`\`\`

**Respuesta Esperada**:
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

#### 2. Clasificación por Lotes
**URL**: `https://tu-proyecto.vercel.app/api/predict-batch`
**Método**: POST
**Content-Type**: application/json

\`\`\`bash
curl -X POST https://medclassify-ai.vercel.app/api/predict-batch \
  -H "Content-Type: application/json" \
  -d '{
    "articles": [
      {
        "title": "Cardiovascular risk assessment in diabetes",
        "abstract": "Study on cardiovascular complications in diabetic patients..."
      },
      {
        "title": "Neurological manifestations of COVID-19",
        "abstract": "Analysis of neurological symptoms in COVID-19 patients..."
      }
    ]
  }'
\`\`\`

### Monitoreo y Debugging

#### Ver Logs en Tiempo Real
\`\`\`bash
# Logs de funciones
vercel logs https://medclassify-ai.vercel.app

# Logs específicos de una función
vercel logs https://medclassify-ai.vercel.app/api/predict
\`\`\`

#### Inspeccionar Despliegue
\`\`\`bash
# Información detallada del despliegue
vercel inspect https://medclassify-ai.vercel.app

# Lista de despliegues
vercel ls
\`\`\`

### Optimización para Producción

#### 1. Configuración de Cache
\`\`\`json
// vercel.json - headers para cache
{
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        {
          "key": "Cache-Control",
          "value": "s-maxage=60, stale-while-revalidate"
        }
      ]
    }
  ]
}
\`\`\`

#### 2. Límites de Recursos
- **Timeout**: 10 segundos (Hobby), 60 segundos (Pro)
- **Memory**: 1024 MB máximo
- **Payload**: 4.5 MB máximo

### Troubleshooting Común

#### Error: "Module not found"
\`\`\`bash
# Verificar requirements.txt
cat requirements.txt

# Redesplegar
vercel --prod
\`\`\`

#### Error: "Function timeout"
- Optimizar algoritmo de clasificación
- Reducir tamaño del modelo
- Implementar cache

#### Error: "Build failed"
\`\`\`bash
# Ver logs detallados
vercel logs --follow

# Verificar configuración
cat vercel.json
\`\`\`

### Comandos Útiles

\`\`\`bash
# Desarrollo local con Vercel
vercel dev

# Eliminar proyecto
vercel remove medclassify-ai

# Cambiar configuración
vercel project

# Ver información del proyecto
vercel project ls
\`\`\`

### Integración con GitHub

#### Despliegue Automático
1. Conectar repositorio en Vercel Dashboard
2. Configurar branch de producción (main)
3. Habilitar despliegues automáticos

#### Configuración de Webhooks
\`\`\`bash
# Configurar webhook para despliegues
vercel git connect
\`\`\`

### Métricas y Analytics

#### Habilitar Analytics
1. Ir a Project Settings en Vercel
2. Analytics tab
3. Enable Web Analytics

#### Monitoreo de Performance
- Core Web Vitals
- Function execution time
- Error rates

### Costos y Límites

#### Plan Hobby (Gratuito)
- 100 GB-hours de función
- 100 GB de bandwidth
- Dominios personalizados ilimitados

#### Plan Pro
- 1000 GB-hours de función
- 1000 GB de bandwidth
- Soporte prioritario

---

## Despliegue Alternativo: Docker

### Dockerfile
\`\`\`dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
\`\`\`

### Docker Compose
\`\`\`yaml
version: '3.8'
services:
  medclassify:
    build: .
    ports:
      - "8501:8501"
    environment:
      - ENVIRONMENT=production
\`\`\`

---

## Contacto y Soporte

**Desarrollado para el AI Data Challenge de TechSphere Colombia**

- **Repositorio GitHub**: github.com/medclassify-ai
- **WhatsApp**: +57 3006101221
- **© 2025 MANUEL PALACIO / CAMILA ZAPATA**
- **Núcleo Colectivo + Línea Médica Yolombó**
- **Medellín, Colombia. Todos los derechos reservados.**
