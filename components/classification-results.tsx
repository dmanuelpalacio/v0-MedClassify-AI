"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Button } from "@/components/ui/button"
import { Separator } from "@/components/ui/separator"
import {
  Heart,
  Brain,
  Clover as Liver,
  Target,
  CheckCircle,
  Clock,
  TrendingUp,
  Shield,
  AlertTriangle,
  Award,
  BarChart3,
  EyeOff,
  FileText,
  ExternalLink,
  BookOpen,
  Download,
  Lightbulb,
  Search,
  Star,
  Users,
  FileDown,
} from "lucide-react"
import { AdvancedVisualizations } from "./advanced-visualizations"
import { useState } from "react"

interface ClassificationResultsProps {
  results: {
    cardiovascular: number
    neurologico: number
    hepatorrenal: number
    oncologico: number
    confidence: number
    processingTime?: string
    reliability?: {
      score: number
      level: string
      factors: Array<{
        factor: string
        score: string
        color: string
      }>
    }
  }
  title?: string
  abstract?: string
}

export function ClassificationResults({ results, title = "", abstract = "" }: ClassificationResultsProps) {
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [isGeneratingPDF, setIsGeneratingPDF] = useState(false)

  const domains = [
    {
      name: "Cardiovascular",
      score: results.cardiovascular,
      icon: Heart,
      color: "text-red-500",
      bgColor: "bg-red-50",
      progressColor: "bg-red-500",
      description: "Enfermedades del corazón y sistema circulatorio",
    },
    {
      name: "Neurológico",
      score: results.neurologico,
      icon: Brain,
      color: "text-blue-500",
      bgColor: "bg-blue-50",
      progressColor: "bg-blue-500",
      description: "Trastornos del sistema nervioso",
    },
    {
      name: "Hepatorrenal",
      score: results.hepatorrenal,
      icon: Liver,
      color: "text-green-500",
      bgColor: "bg-green-50",
      progressColor: "bg-green-500",
      description: "Enfermedades hepáticas y renales",
    },
    {
      name: "Oncológico",
      score: results.oncologico,
      icon: Target,
      color: "text-purple-500",
      bgColor: "bg-purple-50",
      progressColor: "bg-purple-500",
      description: "Cáncer y tumores malignos",
    },
  ]

  const primaryDomain = domains.reduce((prev, current) => (prev.score > current.score ? prev : current))
  const secondaryDomains = domains.filter((d) => d.score > 0.3 && d.name !== primaryDomain.name)

  const generateSummary = () => {
    const keyTerms = extractKeyTerms(title + " " + abstract)

    return {
      executiveSummary: `Este artículo se clasifica principalmente en el dominio ${primaryDomain.name.toLowerCase()} con una confianza del ${(primaryDomain.score * 100).toFixed(1)}%. El análisis identifica elementos clave relacionados con ${primaryDomain.description.toLowerCase()}.`,
      keyFindings: [
        `Dominio principal: ${primaryDomain.name} (${(primaryDomain.score * 100).toFixed(1)}% confianza)`,
        `Confiabilidad de la fuente: ${results.reliability?.level || "No evaluada"}`,
        `Términos clave identificados: ${keyTerms.slice(0, 3).join(", ")}`,
        `Tiempo de procesamiento: ${results.processingTime || "N/A"}s`,
      ],
      clinicalRelevance: getClinicalRelevance(primaryDomain.name),
      methodologyAssessment: getMethodologyAssessment(abstract),
    }
  }

  const extractKeyTerms = (text: string) => {
    const medicalTerms = [
      "cardiovascular",
      "cardiac",
      "heart",
      "coronary",
      "hypertension",
      "arrhythmia",
      "neurological",
      "brain",
      "neural",
      "cognitive",
      "alzheimer",
      "parkinson",
      "hepatorrenal",
      "liver",
      "kidney",
      "renal",
      "hepatic",
      "dialysis",
      "oncological",
      "cancer",
      "tumor",
      "malignant",
      "chemotherapy",
      "radiation",
    ]

    return medicalTerms.filter((term) => text.toLowerCase().includes(term)).slice(0, 5)
  }

  const getClinicalRelevance = (domain: string) => {
    const relevanceMap = {
      Cardiovascular: "Alto impacto en práctica cardiológica y medicina preventiva",
      Neurológico: "Relevante para neurología, psiquiatría y medicina geriátrica",
      Hepatorrenal: "Aplicable en nefrología, hepatología y medicina interna",
      Oncológico: "Crítico para oncología, hematología y cuidados paliativos",
    }
    return relevanceMap[domain] || "Relevancia clínica por determinar"
  }

  const getMethodologyAssessment = (abstract: string) => {
    const hasRandomized = abstract.toLowerCase().includes("randomized") || abstract.toLowerCase().includes("rct")
    const hasControlled = abstract.toLowerCase().includes("controlled") || abstract.toLowerCase().includes("control")
    const hasMetaAnalysis =
      abstract.toLowerCase().includes("meta-analysis") || abstract.toLowerCase().includes("systematic")

    if (hasMetaAnalysis) return "Meta-análisis o revisión sistemática - Evidencia de alto nivel"
    if (hasRandomized && hasControlled) return "Ensayo clínico randomizado controlado - Evidencia robusta"
    if (hasControlled) return "Estudio controlado - Evidencia moderada"
    return "Metodología por evaluar - Revisar diseño del estudio"
  }

  const generateRelatedStudies = (domain: string) => {
    const studyRecommendations = {
      Cardiovascular: [
        {
          title: "ASCVD Risk Calculator Validation Studies",
          journal: "Circulation",
          relevance: "Herramientas de evaluación de riesgo cardiovascular",
          url: "https://www.ahajournals.org/journal/circ",
          impact: "Alto",
        },
        {
          title: "Heart Failure Guidelines - ESC/AHA",
          journal: "European Heart Journal",
          relevance: "Guías clínicas actualizadas en cardiología",
          url: "https://academic.oup.com/eurheartj",
          impact: "Muy Alto",
        },
        {
          title: "Precision Medicine in Cardiology",
          journal: "Nature Reviews Cardiology",
          relevance: "Medicina personalizada cardiovascular",
          url: "https://www.nature.com/nrcardio/",
          impact: "Alto",
        },
      ],
      Neurológico: [
        {
          title: "Alzheimer Disease Biomarkers",
          journal: "Nature Reviews Neurology",
          relevance: "Biomarcadores en enfermedades neurodegenerativas",
          url: "https://www.nature.com/nrneurol/",
          impact: "Muy Alto",
        },
        {
          title: "Stroke Prevention Guidelines",
          journal: "The Lancet Neurology",
          relevance: "Prevención y tratamiento del ictus",
          url: "https://www.thelancet.com/journals/laneur",
          impact: "Alto",
        },
        {
          title: "Neuroplasticity and Rehabilitation",
          journal: "Brain",
          relevance: "Rehabilitación neurológica basada en evidencia",
          url: "https://academic.oup.com/brain",
          impact: "Alto",
        },
      ],
      Hepatorrenal: [
        {
          title: "Chronic Kidney Disease Guidelines",
          journal: "Kidney International",
          relevance: "Manejo integral de enfermedad renal crónica",
          url: "https://www.kidney-international.org/",
          impact: "Muy Alto",
        },
        {
          title: "NASH Treatment Advances",
          journal: "Hepatology",
          relevance: "Tratamientos emergentes en hepatología",
          url: "https://aasldpubs.onlinelibrary.wiley.com/journal/15273350",
          impact: "Alto",
        },
        {
          title: "Liver Transplantation Outcomes",
          journal: "Liver Transplantation",
          relevance: "Resultados en trasplante hepático",
          url: "https://aasldpubs.onlinelibrary.wiley.com/journal/15276473",
          impact: "Alto",
        },
      ],
      Oncológico: [
        {
          title: "Immunotherapy Advances",
          journal: "Nature Cancer",
          relevance: "Inmunoterapia en diferentes tipos de cáncer",
          url: "https://www.nature.com/natcancer/",
          impact: "Muy Alto",
        },
        {
          title: "Precision Oncology Trials",
          journal: "Journal of Clinical Oncology",
          relevance: "Medicina de precisión en oncología",
          url: "https://ascopubs.org/journal/jco",
          impact: "Muy Alto",
        },
        {
          title: "Cancer Survivorship Care",
          journal: "The Lancet Oncology",
          relevance: "Cuidados de supervivencia en cáncer",
          url: "https://www.thelancet.com/journals/lanonc",
          impact: "Alto",
        },
      ],
    }

    return studyRecommendations[domain] || []
  }

  const summary = generateSummary()
  const relatedStudies = generateRelatedStudies(primaryDomain.name)

  const getReliabilityStyle = (level: string) => {
    switch (level) {
      case "Alta":
        return { bg: "bg-green-50", border: "border-green-200", text: "text-green-800", icon: "text-green-600" }
      case "Media":
        return { bg: "bg-yellow-50", border: "border-yellow-200", text: "text-yellow-800", icon: "text-yellow-600" }
      default:
        return { bg: "bg-red-50", border: "border-red-200", text: "text-red-800", icon: "text-red-600" }
    }
  }

  const exportResults = async (format: "csv" | "json" | "pdf") => {
    const exportData = {
      title,
      abstract,
      classification: domains.map((d) => ({ domain: d.name, confidence: d.score })),
      primaryDomain: primaryDomain.name,
      reliability: results.reliability,
      summary,
      relatedStudies,
      timestamp: new Date().toISOString(),
    }

    if (format === "pdf") {
      setIsGeneratingPDF(true)
      try {
        await generateComprehensivePDF(exportData)
      } catch (error) {
        console.error("Error generating PDF:", error)
      } finally {
        setIsGeneratingPDF(false)
      }
      return
    }

    if (format === "csv") {
      const csvContent = [
        "Dominio,Confianza",
        ...domains.map((d) => `${d.name},${d.score.toFixed(3)}`),
        "",
        `Dominio Principal,${primaryDomain.name}`,
        `Confiabilidad,${results.reliability?.level || "N/A"}`,
        `Tiempo de Procesamiento,${results.processingTime || "N/A"}s`,
      ].join("\n")

      const blob = new Blob([csvContent], { type: "text/csv" })
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `clasificacion_medica_${Date.now()}.csv`
      a.click()
    } else if (format === "json") {
      const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: "application/json" })
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `clasificacion_medica_${Date.now()}.json`
      a.click()
    }
  }

  const generateComprehensivePDF = async (data: any) => {
    const htmlContent = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <title>Reporte de Clasificación Médica - MedClassify AI</title>
        <style>
          body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; color: #333; }
          .header { background: linear-gradient(135deg, #3b82f6, #10b981); color: white; padding: 30px; border-radius: 10px; margin-bottom: 30px; }
          .header h1 { margin: 0; font-size: 28px; }
          .header p { margin: 5px 0 0 0; opacity: 0.9; }
          .section { margin-bottom: 30px; }
          .card { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
          .primary-domain { background: linear-gradient(135deg, #ecfdf5, #f0fdf4); border-left: 4px solid #10b981; }
          .reliability-high { background: linear-gradient(135deg, #ecfdf5, #f0fdf4); border-left: 4px solid #10b981; }
          .reliability-medium { background: linear-gradient(135deg, #fffbeb, #fefce8); border-left: 4px solid #f59e0b; }
          .reliability-low { background: linear-gradient(135deg, #fef2f2, #fef2f2); border-left: 4px solid #ef4444; }
          .domain-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0; }
          .domain-item { background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 15px; }
          .progress-bar { background: #e2e8f0; height: 8px; border-radius: 4px; overflow: hidden; margin: 10px 0; }
          .progress-fill { height: 100%; border-radius: 4px; }
          .cardiovascular { background: #ef4444; }
          .neurologico { background: #3b82f6; }
          .hepatorrenal { background: #10b981; }
          .oncologico { background: #8b5cf6; }
          .study-item { background: white; border: 1px solid #e2e8f0; border-radius: 6px; padding: 15px; margin: 10px 0; }
          .badge { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 500; }
          .badge-high { background: #dcfce7; color: #166534; }
          .badge-medium { background: #fef3c7; color: #92400e; }
          .badge-low { background: #fee2e2; color: #991b1b; }
          .key-findings { background: #eff6ff; border-left: 4px solid #3b82f6; padding: 15px; margin: 15px 0; }
          .footer { text-align: center; margin-top: 40px; padding: 20px; background: #f8fafc; border-radius: 8px; }
          .timestamp { color: #6b7280; font-size: 12px; }
          h2 { color: #1f2937; border-bottom: 2px solid #e5e7eb; padding-bottom: 10px; }
          h3 { color: #374151; margin-top: 25px; }
          .metadata { background: #f1f5f9; padding: 15px; border-radius: 6px; margin: 15px 0; }
          .abstract-section { background: #fafafa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #6366f1; }
        </style>
      </head>
      <body>
        <div class="header">
          <h1>🧠 MedClassify AI - Reporte de Análisis</h1>
          <p>Sistema de Clasificación de Literatura Médica | TechSphere AI Challenge 2025</p>
          <p class="timestamp">Generado el: ${new Date().toLocaleString("es-ES")}</p>
        </div>

        <div class="section">
          <h2>📄 Información del Artículo</h2>
          <div class="metadata">
            <h3>Título:</h3>
            <p><strong>${data.title || "No especificado"}</strong></p>
          </div>
          ${
            data.abstract
              ? `
            <div class="abstract-section">
              <h3>Resumen (Abstract):</h3>
              <p style="line-height: 1.6;">${data.abstract}</p>
            </div>
          `
              : ""
          }
        </div>

        <div class="section">
          <h2>🎯 Resultado de Clasificación Principal</h2>
          <div class="card primary-domain">
            <h3>Dominio Principal: ${data.primaryDomain}</h3>
            <p><strong>Confianza:</strong> ${(domains.find((d) => d.name === data.primaryDomain)?.score * 100 || 0).toFixed(1)}%</p>
            <p><strong>Descripción:</strong> ${domains.find((d) => d.name === data.primaryDomain)?.description || ""}</p>
            <p><strong>Tiempo de procesamiento:</strong> ${results.processingTime || "N/A"}s</p>
          </div>
        </div>

        <div class="section">
          <h2>📊 Análisis Detallado por Dominios</h2>
          <div class="domain-grid">
            ${domains
              .map(
                (domain) => `
              <div class="domain-item">
                <h4>${domain.name}</h4>
                <div class="progress-bar">
                  <div class="progress-fill ${domain.name.toLowerCase()}" style="width: ${domain.score * 100}%"></div>
                </div>
                <p><strong>${(domain.score * 100).toFixed(1)}%</strong> de confianza</p>
                <p style="font-size: 12px; color: #6b7280;">${domain.description}</p>
              </div>
            `,
              )
              .join("")}
          </div>
        </div>

        ${
          data.reliability
            ? `
          <div class="section">
            <h2>🛡️ Análisis de Confiabilidad de la Fuente</h2>
            <div class="card reliability-${data.reliability.level.toLowerCase()}">
              <h3>Nivel de Confiabilidad: ${data.reliability.level}</h3>
              <p><strong>Puntuación:</strong> ${(data.reliability.score * 100).toFixed(0)}%</p>
              
              <h4>Factores Evaluados:</h4>
              <ul>
                ${data.reliability.factors
                  .map(
                    (factor) => `
                  <li><strong>${factor.factor}:</strong> ${factor.score}</li>
                `,
                  )
                  .join("")}
              </ul>
              
              <div class="key-findings">
                <h4>Interpretación:</h4>
                <p>${
                  data.reliability.level === "Alta"
                    ? "Esta fuente presenta características de alta confiabilidad académica y científica."
                    : data.reliability.level === "Media"
                      ? "Esta fuente presenta confiabilidad moderada. Considere verificar con fuentes adicionales."
                      : "Esta fuente requiere verificación adicional antes de ser considerada para decisiones clínicas."
                }</p>
              </div>
            </div>
          </div>
        `
            : ""
        }

        <div class="section">
          <h2>📋 Resumen Ejecutivo</h2>
          <div class="card">
            <div class="key-findings">
              <p><strong>${data.summary.executiveSummary}</strong></p>
            </div>
            
            <h3>Hallazgos Clave:</h3>
            <ul>
              ${data.summary.keyFindings.map((finding) => `<li>${finding}</li>`).join("")}
            </ul>
            
            <h3>Relevancia Clínica:</h3>
            <p>${data.summary.clinicalRelevance}</p>
            
            <h3>Evaluación Metodológica:</h3>
            <p>${data.summary.methodologyAssessment}</p>
          </div>
        </div>

        <div class="section">
          <h2>📚 Estudios Relacionados y Recomendaciones</h2>
          <p>Basado en la clasificación en <strong>${data.primaryDomain}</strong>, se recomiendan los siguientes estudios:</p>
          
          ${data.relatedStudies
            .map(
              (study) => `
            <div class="study-item">
              <h4>${study.title}</h4>
              <p><strong>Revista:</strong> ${study.journal}</p>
              <p><strong>Relevancia:</strong> ${study.relevance}</p>
              <p><strong>Impacto:</strong> <span class="badge badge-${study.impact === "Muy Alto" ? "high" : study.impact === "Alto" ? "medium" : "low"}">${study.impact}</span></p>
              <p><strong>URL:</strong> <a href="${study.url}" target="_blank">${study.url}</a></p>
            </div>
          `,
            )
            .join("")}
        </div>

        <div class="section">
          <h2>🔍 Términos Clave para Búsquedas Adicionales</h2>
          <div class="card">
            <p><strong>Términos recomendados:</strong></p>
            <p>${extractKeyTerms(data.title + " " + data.abstract).join(", ")}</p>
            <p style="margin-top: 15px; font-size: 14px; color: #6b7280;">
              Utilice estos términos para búsquedas adicionales en PubMed, Cochrane Library, o bases de datos especializadas.
            </p>
          </div>
        </div>

        <div class="footer">
          <p><strong>MedClassify AI</strong> - Sistema de Clasificación de Literatura Médica</p>
          <p>TechSphere AI Challenge 2025</p>
          <p class="timestamp">Reporte generado automáticamente el ${new Date().toLocaleString("es-ES")}</p>
        </div>
      </body>
      </html>
    `

    const printWindow = window.open("", "_blank")
    if (printWindow) {
      printWindow.document.write(htmlContent)
      printWindow.document.close()

      setTimeout(() => {
        printWindow.print()
        printWindow.close()
      }, 1000)
    }
  }

  return (
    <div className="space-y-6 animate-in fade-in-50 duration-500">
      <Card className="border-0 shadow-lg bg-gradient-to-br from-blue-50 to-green-50">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="p-2 bg-green-100 rounded-lg">
                <CheckCircle className="h-5 w-5 text-green-600" />
              </div>
              <CardTitle className="text-lg text-gray-800">Análisis Completo de Literatura Médica</CardTitle>
            </div>
            <div className="flex items-center gap-3">
              {results.processingTime && (
                <div className="flex items-center gap-1 text-sm text-gray-600">
                  <Clock className="h-4 w-4" />
                  <span>{results.processingTime}s</span>
                </div>
              )}
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => exportResults("csv")}
                  className="flex items-center gap-2"
                >
                  <Download className="h-4 w-4" />
                  CSV
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => exportResults("json")}
                  className="flex items-center gap-2"
                >
                  <Download className="h-4 w-4" />
                  JSON
                </Button>
                <Button
                  variant="default"
                  size="sm"
                  onClick={() => exportResults("pdf")}
                  disabled={isGeneratingPDF}
                  className="flex items-center gap-2 bg-gradient-to-r from-red-500 to-orange-500 hover:from-red-600 hover:to-orange-600"
                >
                  {isGeneratingPDF ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white" />
                      Generando...
                    </>
                  ) : (
                    <>
                      <FileDown className="h-4 w-4" />
                      PDF Completo
                    </>
                  )}
                </Button>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowAdvanced(!showAdvanced)}
                className="flex items-center gap-2"
              >
                {showAdvanced ? (
                  <>
                    <EyeOff className="h-4 w-4" />
                    Ocultar Avanzado
                  </>
                ) : (
                  <>
                    <BarChart3 className="h-4 w-4" />
                    Ver Avanzado
                  </>
                )}
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="mb-6 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg border border-blue-200">
            <h3 className="font-semibold text-blue-800 mb-2 flex items-center gap-2">
              <FileText className="h-5 w-5" />
              Resumen del Análisis Integral
            </h3>
            <p className="text-sm text-blue-700 leading-relaxed mb-3">{summary.executiveSummary}</p>
            <div className="grid md:grid-cols-3 gap-4 text-sm">
              <div className="bg-white/60 p-3 rounded-lg">
                <p className="font-medium text-gray-800">Dominio Principal</p>
                <p className="text-blue-600">{primaryDomain.name}</p>
              </div>
              <div className="bg-white/60 p-3 rounded-lg">
                <p className="font-medium text-gray-800">Confiabilidad</p>
                <p className="text-blue-600">{results.reliability?.level || "No evaluada"}</p>
              </div>
              <div className="bg-white/60 p-3 rounded-lg">
                <p className="font-medium text-gray-800">Estudios Relacionados</p>
                <p className="text-blue-600">{relatedStudies.length} recomendaciones</p>
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <p className="text-sm text-gray-600 mb-1">Dominio Principal</p>
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg ${primaryDomain.bgColor}`}>
                  <primaryDomain.icon className={`h-6 w-6 ${primaryDomain.color}`} />
                </div>
                <div>
                  <p className="text-xl font-bold text-gray-800">{primaryDomain.name}</p>
                  <p className="text-sm text-gray-600">{primaryDomain.description}</p>
                </div>
              </div>
              <Badge variant="secondary" className="mt-2 text-lg px-3 py-1 bg-white/80">
                {(primaryDomain.score * 100).toFixed(1)}% confianza
              </Badge>
            </div>

            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-sm mb-2">
                  <span className="text-gray-600">Confianza del Modelo</span>
                  <span className="font-semibold text-gray-800">{(results.confidence * 100).toFixed(1)}%</span>
                </div>
                <Progress value={results.confidence * 100} className="h-3" />
              </div>

              {secondaryDomains.length > 0 && (
                <div>
                  <p className="text-sm text-gray-600 mb-2">Dominios Secundarios</p>
                  <div className="flex flex-wrap gap-2">
                    {secondaryDomains.map((domain) => (
                      <Badge key={domain.name} variant="outline" className="text-xs">
                        {domain.name} ({(domain.score * 100).toFixed(0)}%)
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
        <CardHeader>
          <div className="flex items-center gap-2">
            <FileText className="h-5 w-5 text-blue-500" />
            <CardTitle>Resumen Ejecutivo y Análisis Profundo</CardTitle>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
            <h4 className="font-semibold text-blue-800 mb-2">Resumen Ejecutivo</h4>
            <p className="text-sm text-blue-700 leading-relaxed">{summary.executiveSummary}</p>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h4 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <Lightbulb className="h-4 w-4 text-yellow-500" />
                Hallazgos Clave
              </h4>
              <ul className="space-y-2">
                {summary.keyFindings.map((finding, index) => (
                  <li key={index} className="flex items-start gap-2 text-sm">
                    <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0" />
                    <span className="text-gray-700">{finding}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div>
              <h4 className="font-semibold text-gray-800 mb-3 flex items-center gap-2">
                <Users className="h-4 w-4 text-green-500" />
                Relevancia Clínica
              </h4>
              <p className="text-sm text-gray-700 mb-4">{summary.clinicalRelevance}</p>

              <h4 className="font-semibold text-gray-800 mb-2 flex items-center gap-2">
                <BarChart3 className="h-4 w-4 text-purple-500" />
                Evaluación Metodológica
              </h4>
              <p className="text-sm text-gray-700">{summary.methodologyAssessment}</p>
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
        <CardHeader>
          <div className="flex items-center gap-2">
            <BookOpen className="h-5 w-5 text-green-500" />
            <CardTitle>Estudios Relacionados y Recomendaciones</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <p className="text-sm text-gray-600 mb-4">
              Basado en la clasificación en <strong>{primaryDomain.name}</strong>, se recomiendan los siguientes
              estudios y recursos:
            </p>

            <div className="grid gap-4">
              {relatedStudies.map((study, index) => (
                <div key={index} className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <h4 className="font-semibold text-gray-800">{study.title}</h4>
                        <Badge
                          variant="outline"
                          className={`text-xs ${
                            study.impact === "Muy Alto"
                              ? "bg-green-100 text-green-800"
                              : study.impact === "Alto"
                                ? "bg-blue-100 text-blue-800"
                                : "bg-gray-100 text-gray-600"
                          }`}
                        >
                          <Star className="h-3 w-3 mr-1" />
                          {study.impact}
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-600 mb-2">{study.journal}</p>
                      <p className="text-sm text-gray-700">{study.relevance}</p>
                    </div>
                    <Button
                      variant="outline"
                      size="sm"
                      className="flex items-center gap-2 bg-transparent"
                      onClick={() => window.open(study.url, "_blank")}
                    >
                      <ExternalLink className="h-4 w-4" />
                      Ver
                    </Button>
                  </div>
                </div>
              ))}
            </div>

            <Separator />

            <div className="p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-lg border border-purple-200">
              <h4 className="font-semibold text-purple-800 mb-2 flex items-center gap-2">
                <Search className="h-4 w-4" />
                Búsquedas Recomendadas
              </h4>
              <div className="flex flex-wrap gap-2">
                {extractKeyTerms(title + " " + abstract).map((term, index) => (
                  <Badge key={index} variant="secondary" className="bg-purple-100 text-purple-800">
                    {term}
                  </Badge>
                ))}
              </div>
              <p className="text-sm text-purple-700 mt-2">
                Utilice estos términos para búsquedas adicionales en PubMed, Cochrane Library, o bases de datos
                especializadas.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {showAdvanced && results.reliability && (
        <AdvancedVisualizations results={results} title={title} abstract={abstract} />
      )}

      {results.reliability && (
        <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
          <CardHeader>
            <div className="flex items-center gap-2">
              <Shield className="h-5 w-5 text-orange-500" />
              <CardTitle>Análisis de Confiabilidad de la Fuente</CardTitle>
            </div>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div
                  className={`p-4 rounded-xl border ${getReliabilityStyle(results.reliability.level).bg} ${getReliabilityStyle(results.reliability.level).border}`}
                >
                  <div className="flex items-center gap-3 mb-2">
                    <div className="p-2 bg-white rounded-lg shadow-sm">
                      {results.reliability.level === "Alta" ? (
                        <Award className={`h-5 w-5 ${getReliabilityStyle(results.reliability.level).icon}`} />
                      ) : results.reliability.level === "Media" ? (
                        <Shield className={`h-5 w-5 ${getReliabilityStyle(results.reliability.level).icon}`} />
                      ) : (
                        <AlertTriangle className={`h-5 w-5 ${getReliabilityStyle(results.reliability.level).icon}`} />
                      )}
                    </div>
                    <div>
                      <p className={`font-semibold ${getReliabilityStyle(results.reliability.level).text}`}>
                        Confiabilidad {results.reliability.level}
                      </p>
                      <p className="text-sm text-gray-600">
                        Puntuación: {(results.reliability.score * 100).toFixed(0)}%
                      </p>
                    </div>
                  </div>
                  <Progress value={results.reliability.score * 100} className="h-3" />
                </div>

                <div className="text-sm text-gray-600">
                  <p className="font-medium mb-2">Interpretación:</p>
                  {results.reliability.level === "Alta" && (
                    <p>Esta fuente presenta características de alta confiabilidad académica y científica.</p>
                  )}
                  {results.reliability.level === "Media" && (
                    <p>Esta fuente presenta confiabilidad moderada. Considere verificar con fuentes adicionales.</p>
                  )}
                  {results.reliability.level === "Baja" && (
                    <p>
                      Esta fuente requiere verificación adicional antes de ser considerada para decisiones clínicas.
                    </p>
                  )}
                </div>
              </div>

              <div>
                <p className="font-medium text-gray-800 mb-3">Factores de Confiabilidad</p>
                <div className="space-y-2">
                  {results.reliability.factors.map((factor, index) => (
                    <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded-lg">
                      <span className="text-sm text-gray-700">{factor.factor}</span>
                      <Badge variant="outline" className={`text-xs ${factor.color}`}>
                        {factor.score}
                      </Badge>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
        <CardHeader>
          <div className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5 text-blue-500" />
            <CardTitle>Análisis Detallado por Dominio</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid gap-6">
            {domains
              .sort((a, b) => b.score - a.score)
              .map((domain, index) => {
                const Icon = domain.icon
                const isHighConfidence = domain.score > 0.5
                const isMediumConfidence = domain.score > 0.25

                return (
                  <div
                    key={domain.name}
                    className={`p-4 rounded-xl border transition-all duration-300 hover:shadow-md ${
                      isHighConfidence
                        ? "border-green-200 bg-green-50/50"
                        : isMediumConfidence
                          ? "border-yellow-200 bg-yellow-50/50"
                          : "border-gray-200 bg-gray-50/50"
                    }`}
                  >
                    <div className="flex items-center gap-4">
                      <div className="flex items-center gap-3">
                        <div className="relative">
                          <div className={`p-3 rounded-xl ${domain.bgColor} shadow-sm`}>
                            <Icon className={`h-6 w-6 ${domain.color}`} />
                          </div>
                          {index === 0 && (
                            <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full flex items-center justify-center">
                              <CheckCircle className="h-3 w-3 text-white" />
                            </div>
                          )}
                        </div>
                        <div>
                          <div className="flex items-center gap-2 mb-1">
                            <span className="font-semibold text-gray-800">{domain.name}</span>
                            {isHighConfidence && (
                              <Badge variant="secondary" className="text-xs bg-green-100 text-green-800">
                                Alta
                              </Badge>
                            )}
                            {isMediumConfidence && !isHighConfidence && (
                              <Badge variant="secondary" className="text-xs bg-yellow-100 text-yellow-800">
                                Media
                              </Badge>
                            )}
                            {!isMediumConfidence && (
                              <Badge variant="secondary" className="text-xs bg-gray-100 text-gray-600">
                                Baja
                              </Badge>
                            )}
                          </div>
                          <p className="text-sm text-gray-600">{domain.description}</p>
                        </div>
                      </div>

                      <div className="flex-1 ml-auto max-w-xs">
                        <div className="flex justify-between items-center mb-2">
                          <span className="text-sm text-gray-600">Confianza</span>
                          <span className="text-lg font-bold text-gray-800">{(domain.score * 100).toFixed(1)}%</span>
                        </div>
                        <div className="relative">
                          <Progress value={domain.score * 100} className="h-3" />
                          <div
                            className={`absolute top-0 left-0 h-3 rounded-full transition-all duration-1000 ${domain.progressColor}`}
                            style={{ width: `${domain.score * 100}%` }}
                          />
                        </div>
                      </div>
                    </div>
                  </div>
                )
              })}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
