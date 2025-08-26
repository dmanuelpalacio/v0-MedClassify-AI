"use client"

import type React from "react"

import { useState, useCallback } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import {
  Upload,
  FileText,
  Download,
  AlertCircle,
  Link,
  File,
  FileSpreadsheet,
  Brain,
  Shield,
  BookOpen,
} from "lucide-react"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { ClassificationResults } from "./classification-results"

export function FileUpload() {
  const [isDragOver, setIsDragOver] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [isProcessing, setIsProcessing] = useState(false)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [results, setResults] = useState<any>(null)
  const [urlInput, setUrlInput] = useState("")
  const [isUrlProcessing, setIsUrlProcessing] = useState(false)
  const [detailedResults, setDetailedResults] = useState<any>(null)
  const [extractedContent, setExtractedContent] = useState<{ title: string; abstract: string } | null>(null)

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)

    const files = Array.from(e.dataTransfer.files)
    const supportedFile = files.find(
      (file) =>
        file.name.endsWith(".csv") ||
        file.name.endsWith(".pdf") ||
        file.name.endsWith(".txt") ||
        file.name.endsWith(".docx"),
    )

    if (supportedFile) {
      setUploadedFile(supportedFile)
      processFile(supportedFile)
    }
  }, [])

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (
      file &&
      (file.name.endsWith(".csv") ||
        file.name.endsWith(".pdf") ||
        file.name.endsWith(".txt") ||
        file.name.endsWith(".docx"))
    ) {
      setUploadedFile(file)
      processFile(file)
    }
  }

  const processUrl = async (url: string) => {
    setIsUrlProcessing(true)
    setUploadProgress(0)
    setResults(null)
    setDetailedResults(null)

    const processingSteps = [
      "Conectando con la URL...",
      "Extrayendo contenido HTML...",
      "Identificando artículos médicos...",
      "Analizando estructura del documento...",
      "Extrayendo títulos y resúmenes...",
      "Clasificando con IA médica...",
      "Evaluando confiabilidad de fuente...",
      "Generando recomendaciones...",
      "Finalizando análisis...",
    ]

    for (let i = 0; i < processingSteps.length; i++) {
      setUploadProgress((i / processingSteps.length) * 100)
      await new Promise((resolve) => setTimeout(resolve, 800))
    }

    const mockExtractedContent = generateMockContentFromUrl(url)
    setExtractedContent(mockExtractedContent)

    const mockDetailedResults = generateDetailedResults(
      mockExtractedContent.title,
      mockExtractedContent.abstract,
      "URL",
    )

    setDetailedResults(mockDetailedResults)

    // Mock results for URL processing summary
    setResults({
      source: "URL",
      url: url,
      extractedArticles: 1,
      classified: {
        cardiovascular: Math.floor(mockDetailedResults.cardiovascular * 100),
        neurologico: Math.floor(mockDetailedResults.neurologico * 100),
        hepatorrenal: Math.floor(mockDetailedResults.hepatorrenal * 100),
        oncologico: Math.floor(mockDetailedResults.oncologico * 100),
      },
      averageConfidence: mockDetailedResults.confidence,
      processingTime: mockDetailedResults.processingTime,
      reliability: mockDetailedResults.reliability,
    })

    setUploadProgress(100)
    setIsUrlProcessing(false)
  }

  const processFile = async (file: File) => {
    setIsProcessing(true)
    setUploadProgress(0)
    setResults(null)
    setDetailedResults(null)

    const fileExtension = file.name.split(".").pop()?.toLowerCase()

    const processingSteps = [
      "Leyendo archivo...",
      "Extrayendo texto del documento...",
      "Identificando estructura médica...",
      "Segmentando artículos...",
      "Analizando terminología médica...",
      "Clasificando con IA especializada...",
      "Evaluando calidad metodológica...",
      "Generando análisis de confiabilidad...",
      "Creando recomendaciones...",
      "Finalizando procesamiento...",
    ]

    for (let i = 0; i < processingSteps.length; i++) {
      setUploadProgress((i / processingSteps.length) * 100)
      await new Promise((resolve) => setTimeout(resolve, 600))
    }

    const mockExtractedContent = generateMockContentFromFile(file, fileExtension)
    setExtractedContent(mockExtractedContent)

    const mockDetailedResults = generateDetailedResults(
      mockExtractedContent.title,
      mockExtractedContent.abstract,
      "Archivo",
    )

    setDetailedResults(mockDetailedResults)

    const baseArticles = fileExtension === "csv" ? 150 : fileExtension === "pdf" ? 1 : fileExtension === "docx" ? 1 : 5

    setResults({
      source: "Archivo",
      fileType: fileExtension?.toUpperCase(),
      fileName: file.name,
      totalArticles: baseArticles,
      classified: {
        cardiovascular: Math.floor(baseArticles * mockDetailedResults.cardiovascular) + Math.floor(Math.random() * 10),
        neurologico: Math.floor(baseArticles * mockDetailedResults.neurologico) + Math.floor(Math.random() * 8),
        hepatorrenal: Math.floor(baseArticles * mockDetailedResults.hepatorrenal) + Math.floor(Math.random() * 6),
        oncologico: Math.floor(baseArticles * mockDetailedResults.oncologico) + Math.floor(Math.random() * 12),
      },
      averageConfidence: mockDetailedResults.confidence,
      processingTime: mockDetailedResults.processingTime,
      reliability: mockDetailedResults.reliability,
    })

    setUploadProgress(100)
    setIsProcessing(false)
  }

  const generateMockContentFromUrl = (url: string) => {
    const urlPatterns = [
      {
        pattern: /pubmed|ncbi/i,
        title: "Cardiovascular Risk Assessment in Diabetic Patients: A Comprehensive Meta-Analysis",
        abstract:
          "Background: Cardiovascular disease remains the leading cause of mortality in diabetic patients. This meta-analysis evaluates current risk assessment tools and their predictive accuracy. Methods: We systematically reviewed 45 studies involving 125,000 diabetic patients across multiple healthcare systems. Results: Traditional risk calculators showed moderate predictive value (AUC 0.72-0.78), while machine learning approaches demonstrated superior performance (AUC 0.84-0.89). Conclusions: Integration of novel biomarkers and AI-driven assessment tools significantly improves cardiovascular risk prediction in diabetic populations.",
      },
      {
        pattern: /nature|science|cell/i,
        title: "Novel Therapeutic Targets in Alzheimer's Disease: Neuroinflammation and Synaptic Plasticity",
        abstract:
          "Alzheimer's disease (AD) pathogenesis involves complex interactions between amyloid-β plaques, tau tangles, and neuroinflammation. Recent advances in single-cell RNA sequencing have identified microglial activation patterns associated with disease progression. This study presents evidence for targeting specific inflammatory pathways while preserving neuroprotective microglial functions. Our findings suggest that modulating TREM2 signaling and complement cascade activation may offer therapeutic benefits in early-stage AD patients.",
      },
      {
        pattern: /cancer|oncology|tumor/i,
        title: "Immunotherapy Resistance Mechanisms in Advanced Hepatocellular Carcinoma",
        abstract:
          "Hepatocellular carcinoma (HCC) represents a major global health challenge with limited therapeutic options. While immune checkpoint inhibitors have shown promise, resistance mechanisms remain poorly understood. This comprehensive analysis of 200 HCC patients reveals that tumor microenvironment heterogeneity and metabolic reprogramming contribute to immunotherapy resistance. We identify potential biomarkers for patient stratification and combination therapy approaches that may overcome resistance mechanisms.",
      },
    ]

    const matchedPattern = urlPatterns.find((p) => p.pattern.test(url))
    return (
      matchedPattern || {
        title: "Clinical Efficacy of Novel Hepatorenal Syndrome Treatment Protocol",
        abstract:
          "Hepatorenal syndrome (HRS) is a severe complication of advanced liver disease with high mortality rates. This multicenter study evaluates a novel treatment protocol combining terlipressin, albumin, and targeted fluid management. Results from 180 patients demonstrate significant improvement in renal function and 30-day survival rates compared to standard care. The protocol shows particular efficacy in Type-1 HRS patients with preserved cardiac function.",
      }
    )
  }

  const generateMockContentFromFile = (file: File, extension?: string) => {
    const fileBasedContent = {
      pdf: {
        title: "Systematic Review: Precision Medicine Approaches in Cardiovascular Disease Management",
        abstract:
          "This systematic review examines the current state of precision medicine in cardiovascular care, analyzing genomic, proteomic, and metabolomic approaches to personalized treatment. We reviewed 78 studies encompassing 50,000 patients with various cardiovascular conditions. Findings indicate that genetic risk scores combined with traditional risk factors improve prediction accuracy by 15-20%. Pharmacogenomic testing for antiplatelet therapy shows clinical utility in specific populations. Future directions include integration of multi-omics data and artificial intelligence for enhanced clinical decision-making.",
      },
      docx: {
        title: "Neuroplasticity-Based Rehabilitation Strategies for Post-Stroke Recovery",
        abstract:
          "Stroke remains a leading cause of long-term disability worldwide. This comprehensive review explores evidence-based neuroplasticity principles in stroke rehabilitation. We analyzed 120 clinical trials involving 15,000 stroke survivors, examining motor recovery, cognitive rehabilitation, and speech therapy outcomes. Results demonstrate that intensive, task-specific training combined with neuromodulation techniques significantly enhances functional recovery. Virtual reality and brain-computer interfaces show promising results in chronic stroke patients.",
      },
      txt: {
        title: "Emerging Biomarkers in Early Detection of Pancreatic Cancer",
        abstract:
          "Pancreatic ductal adenocarcinoma (PDAC) has a 5-year survival rate below 10%, largely due to late-stage diagnosis. This study investigates novel circulating biomarkers for early detection. We analyzed blood samples from 500 patients including early-stage PDAC, chronic pancreatitis, and healthy controls. A panel combining CA 19-9, circulating tumor DNA, and specific microRNA signatures achieved 85% sensitivity and 92% specificity for early-stage detection. These findings support the development of screening protocols for high-risk populations.",
      },
      csv: {
        title: "Multi-Center Analysis of Treatment Outcomes in Acute Myeloid Leukemia",
        abstract:
          "This large-scale retrospective analysis examines treatment outcomes in 2,500 acute myeloid leukemia (AML) patients across 15 medical centers. We evaluated the impact of cytogenetic risk stratification, age, performance status, and treatment protocols on overall survival and disease-free survival. Results show significant improvements in outcomes with targeted therapies in specific genetic subgroups. Older patients (>65 years) benefit from hypomethylating agents combined with venetoclax. The study provides evidence for personalized treatment approaches based on molecular profiling.",
      },
    }

    return fileBasedContent[extension as keyof typeof fileBasedContent] || fileBasedContent.pdf
  }

  const generateDetailedResults = (title: string, abstract: string, source: string) => {
    const text = (title + " " + abstract).toLowerCase()

    // Enhanced domain detection
    const cardiovascularScore =
      (text.includes("cardiovascular") ? 0.3 : 0) +
      (text.includes("cardiac") || text.includes("heart") ? 0.25 : 0) +
      (text.includes("coronary") || text.includes("artery") ? 0.2 : 0) +
      (text.includes("hypertension") || text.includes("blood pressure") ? 0.15 : 0) +
      Math.random() * 0.1

    const neurologicoScore =
      (text.includes("neurological") || text.includes("neuro") ? 0.3 : 0) +
      (text.includes("brain") || text.includes("neural") ? 0.25 : 0) +
      (text.includes("alzheimer") || text.includes("parkinson") ? 0.2 : 0) +
      (text.includes("stroke") || text.includes("cognitive") ? 0.15 : 0) +
      Math.random() * 0.1

    const hepatorrenalScore =
      (text.includes("hepatorrenal") || text.includes("hepatorenal") ? 0.35 : 0) +
      (text.includes("liver") || text.includes("hepatic") ? 0.2 : 0) +
      (text.includes("kidney") || text.includes("renal") ? 0.2 : 0) +
      (text.includes("dialysis") || text.includes("transplant") ? 0.15 : 0) +
      Math.random() * 0.1

    const oncologicoScore =
      (text.includes("cancer") || text.includes("oncolog") ? 0.3 : 0) +
      (text.includes("tumor") || text.includes("malignant") ? 0.25 : 0) +
      (text.includes("chemotherapy") || text.includes("radiation") ? 0.2 : 0) +
      (text.includes("metastasis") || text.includes("carcinoma") ? 0.15 : 0) +
      Math.random() * 0.1

    // Normalize scores
    const total = cardiovascularScore + neurologicoScore + hepatorrenalScore + oncologicoScore
    const normalizedScores = {
      cardiovascular: total > 0 ? cardiovascularScore / total : 0.25,
      neurologico: total > 0 ? neurologicoScore / total : 0.25,
      hepatorrenal: total > 0 ? hepatorrenalScore / total : 0.25,
      oncologico: total > 0 ? oncologicoScore / total : 0.25,
    }

    // Ensure at least one domain has a reasonable score
    const maxScore = Math.max(...Object.values(normalizedScores))
    if (maxScore < 0.4) {
      const randomDomain = Object.keys(normalizedScores)[Math.floor(Math.random() * 4)] as keyof typeof normalizedScores
      normalizedScores[randomDomain] = 0.6 + Math.random() * 0.3
    }

    // Generate reliability assessment
    const reliability = {
      score: 0.6 + Math.random() * 0.35,
      level: "",
      factors: [
        { factor: "Fuente Identificada", score: "+10%", color: "text-blue-600" },
        {
          factor: source === "URL" ? "Contenido Web Extraído" : "Documento Procesado",
          score: "+15%",
          color: "text-green-600",
        },
        { factor: "Terminología Médica Detectada", score: "+20%", color: "text-green-600" },
        { factor: "Estructura Académica", score: "+10%", color: "text-blue-600" },
      ],
    }

    reliability.level = reliability.score >= 0.8 ? "Alta" : reliability.score >= 0.6 ? "Media" : "Baja"

    return {
      ...normalizedScores,
      confidence: 0.82 + Math.random() * 0.15,
      processingTime: (2.1 + Math.random() * 1.8).toFixed(1),
      reliability,
    }
  }

  const handleUrlSubmit = () => {
    if (urlInput.trim()) {
      processUrl(urlInput.trim())
    }
  }

  const getFileIcon = (fileName: string) => {
    const extension = fileName.split(".").pop()?.toLowerCase()
    switch (extension) {
      case "csv":
        return <FileSpreadsheet className="h-4 w-4" />
      case "pdf":
        return <File className="h-4 w-4 text-red-500" />
      case "docx":
        return <File className="h-4 w-4 text-blue-500" />
      case "txt":
        return <FileText className="h-4 w-4" />
      default:
        return <FileText className="h-4 w-4" />
    }
  }

  const downloadResults = () => {
    const csvContent = `Title,Abstract,Cardiovascular,Neurologico,Hepatorrenal,Oncologico,Primary_Domain,Confidence,Source,Reliability_Level,Processing_Time
"${extractedContent?.title || "Extracted Content"}","${extractedContent?.abstract || "Processed abstract content..."}",${detailedResults?.cardiovascular.toFixed(3) || "0.000"},${detailedResults?.neurologico.toFixed(3) || "0.000"},${detailedResults?.hepatorrenal.toFixed(3) || "0.000"},${detailedResults?.oncologico.toFixed(3) || "0.000"},${getPrimaryDomain()},${detailedResults?.confidence.toFixed(3) || "0.000"},${results.source},${detailedResults?.reliability?.level || "N/A"},${detailedResults?.processingTime || "N/A"}`

    const blob = new Blob([csvContent], { type: "text/csv" })
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `medical_classification_${Date.now()}.csv`
    a.click()
    window.URL.revokeObjectURL(url)
  }

  const getPrimaryDomain = () => {
    if (!detailedResults) return "Unknown"
    const domains = {
      Cardiovascular: detailedResults.cardiovascular,
      Neurológico: detailedResults.neurologico,
      Hepatorrenal: detailedResults.hepatorrenal,
      Oncológico: detailedResults.oncologico,
    }
    return Object.entries(domains).reduce((a, b) =>
      domains[a[0] as keyof typeof domains] > domains[b[0] as keyof typeof domains] ? a : b,
    )[0]
  }

  return (
    <div className="space-y-6">
      <Tabs defaultValue="files" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="files">Cargar Archivos</TabsTrigger>
          <TabsTrigger value="url">Analizar URL</TabsTrigger>
        </TabsList>

        <TabsContent value="files">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="h-5 w-5 text-blue-500" />
                Carga de Documentos Médicos
              </CardTitle>
              <CardDescription>
                Suba archivos CSV, PDF, TXT o DOCX con literatura médica para clasificación automática y análisis de
                confiabilidad
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div
                className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                  isDragOver ? "border-accent bg-accent/5" : "border-border hover:border-accent/50"
                }`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
              >
                <Upload className="h-12 w-12 mx-auto mb-4 text-muted-foreground" />
                <p className="text-lg font-medium mb-2">Arrastre sus archivos aquí</p>
                <p className="text-muted-foreground mb-4">Formatos soportados: CSV, PDF, TXT, DOCX</p>
                <input
                  type="file"
                  accept=".csv,.pdf,.txt,.docx"
                  onChange={handleFileSelect}
                  className="hidden"
                  id="file-upload"
                />
                <Button asChild variant="outline">
                  <label htmlFor="file-upload" className="cursor-pointer">
                    Seleccionar Archivo
                  </label>
                </Button>
              </div>

              {uploadedFile && (
                <div className="mt-4 p-4 bg-muted rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    {getFileIcon(uploadedFile.name)}
                    <span className="font-medium">{uploadedFile.name}</span>
                    <span className="text-sm text-muted-foreground">({(uploadedFile.size / 1024).toFixed(1)} KB)</span>
                  </div>

                  {isProcessing && (
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="flex items-center gap-2">
                          <Brain className="h-4 w-4 text-blue-500" />
                          Procesando con IA médica especializada...
                        </span>
                        <span>{uploadProgress.toFixed(0)}%</span>
                      </div>
                      <Progress value={uploadProgress} />
                    </div>
                  )}
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="url">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Link className="h-5 w-5" />
                Análisis de URL
              </CardTitle>
              <CardDescription>
                Ingrese la URL de un artículo médico, revista científica o repositorio para extraer y clasificar el
                contenido con análisis de confiabilidad
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="url-input">URL del Artículo o Fuente</Label>
                <Input
                  id="url-input"
                  type="url"
                  placeholder="https://pubmed.ncbi.nlm.nih.gov/article/... o https://nature.com/articles/..."
                  value={urlInput}
                  onChange={(e) => setUrlInput(e.target.value)}
                  className="border-gray-200 focus:border-blue-400"
                />
              </div>

              <Button
                onClick={handleUrlSubmit}
                disabled={!urlInput.trim() || isUrlProcessing}
                className="w-full bg-gradient-to-r from-blue-500 to-green-500 hover:from-blue-600 hover:to-green-600"
              >
                {isUrlProcessing ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                    Extrayendo y Analizando con IA...
                  </>
                ) : (
                  <>
                    <Brain className="h-4 w-4 mr-2" />
                    Clasificar y Analizar Confiabilidad
                  </>
                )}
              </Button>

              {isUrlProcessing && (
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="flex items-center gap-2">
                      <Shield className="h-4 w-4 text-orange-500" />
                      Extrayendo contenido y evaluando confiabilidad...
                    </span>
                    <span>{uploadProgress.toFixed(0)}%</span>
                  </div>
                  <Progress value={uploadProgress} />
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>

      {results && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BookOpen className="h-5 w-5 text-green-500" />
              Resultados del Procesamiento
            </CardTitle>
            <CardDescription>
              {results.source === "URL"
                ? `Contenido extraído y analizado de: ${results.url}`
                : `Archivo procesado: ${results.fileName} (${results.fileType})`}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="text-center">
                <p className="text-2xl font-bold text-red-500">{results.classified.cardiovascular}</p>
                <p className="text-sm text-muted-foreground">Cardiovascular</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-blue-500">{results.classified.neurologico}</p>
                <p className="text-sm text-muted-foreground">Neurológico</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-green-500">{results.classified.hepatorrenal}</p>
                <p className="text-sm text-muted-foreground">Hepatorrenal</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-purple-500">{results.classified.oncologico}</p>
                <p className="text-sm text-muted-foreground">Oncológico</p>
              </div>
            </div>

            <Alert className="mb-4">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                {results.source === "URL"
                  ? `Extraído y procesado ${results.extractedArticles} artículo(s) en ${results.processingTime} con confianza promedio de ${(results.averageConfidence * 100).toFixed(1)}%`
                  : `Procesados ${results.totalArticles} artículos en ${results.processingTime} con confianza promedio de ${(results.averageConfidence * 100).toFixed(1)}%`}
                {results.reliability && ` | Confiabilidad de fuente: ${results.reliability.level}`}
              </AlertDescription>
            </Alert>

            <Button onClick={downloadResults} className="w-full">
              <Download className="h-4 w-4 mr-2" />
              Descargar Resultados Detallados CSV
            </Button>
          </CardContent>
        </Card>
      )}

      {detailedResults && extractedContent && (
        <ClassificationResults
          results={detailedResults}
          title={extractedContent.title}
          abstract={extractedContent.abstract}
        />
      )}
    </div>
  )
}
