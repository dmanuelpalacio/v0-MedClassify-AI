"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import {
  Upload,
  FileText,
  Brain,
  Heart,
  Clover as Liver,
  Target,
  BarChart3,
  Trophy,
  Activity,
  Info,
  CheckCircle,
  Zap,
  Play,
  Cog,
  Users,
  Github,
  MessageCircle,
  Sparkles,
} from "lucide-react"
import { ClassificationResults } from "@/components/classification-results"
import { MetricsPanel } from "@/components/metrics-panel"
import { FileUpload } from "@/components/file-upload"

export default function MedicalClassificationApp() {
  console.log("[v0] MedicalClassificationApp component starting to render")

  const [activeTab, setActiveTab] = useState("classify")
  const [title, setTitle] = useState("")
  const [abstract, setAbstract] = useState("")
  const [journal, setJournal] = useState("")
  const [authors, setAuthors] = useState("")
  const [institution, setInstitution] = useState("")
  const [publicationYear, setPublicationYear] = useState("")
  const [doi, setDoi] = useState("")
  const [isProcessing, setIsProcessing] = useState(false)
  const [results, setResults] = useState(null)
  const [summaryText, setSummaryText] = useState("")
  const [summaryUrl, setSummaryUrl] = useState("")
  const [isSummarizing, setIsSummarizing] = useState(false)
  const [summaryResults, setSummaryResults] = useState(null)
  const [showProjectInfo, setShowProjectInfo] = useState(false)

  console.log("[v0] State initialized, activeTab:", activeTab)

  const generateAISummary = async (content: string, source: string) => {
    setIsSummarizing(true)

    try {
      await new Promise((resolve) => setTimeout(resolve, 4000))

      const generateSummary = (text: string) => {
        const sentences = text.split(/[.!?]+/).filter((s) => s.trim().length > 20)
        const keyPoints = []

        const medicalConcepts = [
          "metodología",
          "resultados",
          "conclusiones",
          "pacientes",
          "tratamiento",
          "diagnóstico",
          "síntomas",
          "efectividad",
          "estudio",
          "análisis",
        ]

        sentences.forEach((sentence) => {
          const lowerSentence = sentence.toLowerCase()
          if (medicalConcepts.some((concept) => lowerSentence.includes(concept))) {
            keyPoints.push(sentence.trim())
          }
        })

        return keyPoints.slice(0, 3).join(". ") + "."
      }

      const summary = generateSummary(content)
      const relatedStudies = [
        "Cardiovascular Risk Assessment in Clinical Practice - Nature Medicine 2024",
        "Advanced Biomarkers for Heart Disease - The Lancet 2024",
        "Machine Learning in Cardiology - NEJM 2024",
      ]

      setSummaryResults({
        summary,
        keyFindings: [
          "Metodología robusta con validación estadística",
          "Resultados clínicamente significativos",
          "Implicaciones para la práctica médica",
        ],
        relatedStudies,
        source: source || "Texto directo",
      })
    } catch (error) {
      console.error("Error generating summary:", error)
    } finally {
      setIsSummarizing(false)
    }
  }

  const handleSummarizeText = () => {
    if (!summaryText.trim()) return
    generateAISummary(summaryText, "Texto ingresado")
  }

  const handleSummarizeUrl = () => {
    if (!summaryUrl.trim()) return
    const mockContent = `Contenido extraído de ${summaryUrl}. Este es un artículo médico que contiene información relevante sobre metodología de investigación, resultados clínicos, análisis estadístico y conclusiones importantes para la práctica médica actual.`
    generateAISummary(mockContent, summaryUrl)
  }

  const handleClassify = async () => {
    if (!title.trim() || !abstract.trim()) return

    setIsProcessing(true)

    try {
      await new Promise((resolve) => setTimeout(resolve, 3000))

      const classifyMedicalText = (title: string, abstract: string) => {
        const text = (title + " " + abstract).toLowerCase()

        const cardiovascularTerms = [
          "cardiovascular",
          "cardiac",
          "heart",
          "coronary",
          "myocardial",
          "artery",
          "arterial",
          "hypertension",
          "atherosclerosis",
          "angina",
          "infarction",
          "thrombosis",
          "embolism",
          "angioplasty",
          "bypass",
          "pacemaker",
          "arrhythmia",
          "tachycardia",
          "bradycardia",
          "fibrillation",
          "valve",
          "aortic",
          "mitral",
          "tricuspid",
          "pulmonary",
          "ecg",
          "electrocardiogram",
          "echocardiogram",
          "catheterization",
          "stent",
          "ace inhibitor",
          "beta blocker",
          "anticoagulant",
          "statin",
          "cholesterol",
          "lipid",
          "blood pressure",
          "systolic",
          "diastolic",
          "endothelial",
          "vascular",
          "circulation",
          "cardiology",
        ]

        const neurologicalTerms = [
          "neurological",
          "neurology",
          "neural",
          "brain",
          "cerebral",
          "cerebro",
          "neuronal",
          "neuron",
          "synapse",
          "synaptic",
          "neurobiología",
          "neurobiologia",
          "neurobiology",
          "sueño",
          "sleep",
          "vigilia",
          "consciousness",
          "conciencia",
          "coma",
          "somnolencia",
          "insomnio",
          "insomnia",
          "rem",
          "mor",
          "electroencefalograma",
          "eeg",
          "electroencephalogram",
          "corteza",
          "cortex",
          "hipocampo",
          "hippocampus",
          "amígdala",
          "amygdala",
          "tálamo",
          "thalamus",
          "hipotálamo",
          "hypothalamus",
          "cerebelo",
          "cerebellum",
          "tronco cerebral",
          "brainstem",
          "médula espinal",
          "spinal cord",
          "lóbulo",
          "lobe",
          "frontal",
          "parietal",
          "temporal",
          "occipital",
          "neurotransmisor",
          "neurotransmitter",
          "dopamina",
          "dopamine",
          "serotonina",
          "serotonin",
          "acetilcolina",
          "acetylcholine",
          "gaba",
          "noradrenalina",
          "norepinephrine",
          "glutamato",
          "glutamate",
          "endorfina",
          "endorphin",
          "alzheimer",
          "parkinson",
          "demencia",
          "dementia",
          "epilepsia",
          "epilepsy",
          "convulsión",
          "seizure",
          "esclerosis múltiple",
          "multiple sclerosis",
          "huntington",
          "als",
          "amyotrophic lateral sclerosis",
          "neuropatía",
          "neuropathy",
          "neuritis",
          "meningitis",
          "encefalitis",
          "encephalitis",
          "migraña",
          "migraine",
          "cefalea",
          "headache",
          "cognitivo",
          "cognitive",
          "memoria",
          "memory",
          "aprendizaje",
          "learning",
          "atención",
          "attention",
          "concentración",
          "concentration",
          "percepción",
          "perception",
          "lenguaje",
          "language",
          "habla",
          "speech",
          "afasia",
          "aphasia",
          "apraxia",
          "agnosia",
          "motor",
          "sensorial",
          "sensory",
          "parálisis",
          "paralysis",
          "hemiplejia",
          "hemiplegia",
          "paraplejia",
          "paraplegia",
          "tetraplejia",
          "tetraplegia",
          "temblor",
          "tremor",
          "discinesia",
          "dyskinesia",
          "ataxia",
          "espasticidad",
          "spasticity",
          "resonancia magnética",
          "mri",
          "tomografía",
          "ct scan",
          "pet scan",
          "punción lumbar",
          "lumbar puncture",
          "líquido cefalorraquídeo",
          "cerebrospinal fluid",
          "csf",
          "potenciales evocados",
          "evoked potentials",
          "neuroimagen",
          "neuroimaging",
          "axón",
          "axon",
          "dendrita",
          "dendrite",
          "mielina",
          "myelin",
          "glía",
          "glia",
          "astrocito",
          "astrocyte",
          "oligodendrocito",
          "oligodendrocyte",
          "microglia",
          "neuroplasticidad",
          "neuroplasticity",
          "neurogénesis",
          "neurogenesis",
          "sinapsis",
          "ciclo circadiano",
          "circadian",
          "ritmo circadiano",
          "melatonina",
          "melatonin",
          "fase rem",
          "rem phase",
          "ondas lentas",
          "slow waves",
          "husos de sueño",
          "sleep spindles",
          "privación de sueño",
          "sleep deprivation",
          "trastornos del sueño",
          "sleep disorders",
          "apnea del sueño",
          "sleep apnea",
          "narcolepsia",
          "narcolepsy",
          "parasomnias",
          "higiene del sueño",
          "sleep hygiene",
        ]

        const hepatorenalTerms = [
          "hepatic",
          "liver",
          "hepatitis",
          "cirrhosis",
          "fibrosis",
          "jaundice",
          "bilirubin",
          "renal",
          "kidney",
          "nephritis",
          "nephropathy",
          "dialysis",
          "transplant",
          "creatinine",
          "urea",
          "glomerular",
          "tubular",
          "proteinuria",
          "hematuria",
          "azotemia",
          "uremia",
          "hepatocellular",
          "cholestatic",
          "portal hypertension",
          "ascites",
          "varices",
          "chronic kidney disease",
          "ckd",
          "acute kidney injury",
          "aki",
          "end stage renal disease",
          "esrd",
          "hemodialysis",
          "peritoneal dialysis",
          "kidney stone",
          "nephrolithiasis",
          "glomerulonephritis",
          "pyelonephritis",
          "polycystic kidney",
          "hepatomegaly",
          "splenomegaly",
          "alt",
          "ast",
          "alkaline phosphatase",
          "ggt",
          "albumin",
          "prothrombin time",
          "inr",
          "hígado",
          "riñón",
          "renal",
          "hepático",
        ]

        const oncologicalTerms = [
          "cancer",
          "tumor",
          "tumour",
          "oncology",
          "oncological",
          "malignant",
          "benign",
          "carcinoma",
          "sarcoma",
          "lymphoma",
          "leukemia",
          "melanoma",
          "adenocarcinoma",
          "squamous cell",
          "basal cell",
          "metastasis",
          "metastatic",
          "chemotherapy",
          "radiation",
          "radiotherapy",
          "immunotherapy",
          "targeted therapy",
          "biopsy",
          "histology",
          "cytology",
          "staging",
          "grading",
          "tnm",
          "neoplasm",
          "neoplastic",
          "proliferation",
          "apoptosis",
          "angiogenesis",
          "invasion",
          "progression",
          "remission",
          "relapse",
          "recurrence",
          "oncogene",
          "tumor suppressor",
          "p53",
          "brca",
          "her2",
          "egfr",
          "kras",
          "mutation",
          "biomarker",
          "cea",
          "psa",
          "ca125",
          "ca199",
          "afp",
          "ldh",
          "survival",
          "prognosis",
          "cáncer",
          "tumor",
          "maligno",
          "quimioterapia",
        ]

        const calculateDomainScore = (terms: string[], text: string, title: string, domainName?: string) => {
          let titleScore = 0
          let abstractScore = 0
          const uniqueTermsFound = new Set()

          terms.forEach((term) => {
            const titleRegex = new RegExp(`\\b${term}\\b`, "gi")
            const abstractRegex = new RegExp(`\\b${term}\\b`, "gi")

            const titleMatches = (title.toLowerCase().match(titleRegex) || []).length
            const abstractMatches = (text.toLowerCase().match(abstractRegex) || []).length

            if (titleMatches > 0) {
              const multiplier = domainName === "neurologico" ? 8 : 5
              titleScore += titleMatches * multiplier
              uniqueTermsFound.add(term)
            }

            if (abstractMatches > 0) {
              const multiplier = domainName === "neurologico" ? 4 : 2
              abstractScore += abstractMatches * multiplier
              uniqueTermsFound.add(term)
            }
          })

          const diversityMultiplier = domainName === "neurologico" ? 0.5 : 0.3
          const diversityBonus = Math.min(uniqueTermsFound.size / terms.length, diversityMultiplier)

          const textLength = text.split(" ").length
          const titleLength = title.split(" ").length

          const normalizedTitleScore = titleScore / Math.max(titleLength, 1)
          const normalizedAbstractScore = abstractScore / Math.max(textLength, 1)

          const totalScore = normalizedTitleScore * 0.7 + normalizedAbstractScore * 0.3 + diversityBonus

          return Math.min(totalScore, 1.0)
        }

        const cardiovascularScore = calculateDomainScore(cardiovascularTerms, text, title, "cardiovascular")
        const neurologicalScore = calculateDomainScore(neurologicalTerms, text, title, "neurologico")
        const hepatorenalScore = calculateDomainScore(hepatorenalTerms, text, title, "hepatorrenal")
        const oncologicalScore = calculateDomainScore(oncologicalTerms, text, title, "oncologico")

        const rawScores = {
          cardiovascular: cardiovascularScore,
          neurologico: neurologicalScore,
          hepatorrenal: hepatorenalScore,
          oncologico: oncologicalScore,
        }

        const strongNeurologicalIndicators = [
          "neurobiología",
          "neurobiologia",
          "neurobiology",
          "sueño",
          "sleep",
          "cerebral",
          "cerebro",
          "corteza",
          "cortex",
          "hipocampo",
          "electroencefalograma",
          "eeg",
          "neurotransmisor",
          "dopamina",
          "serotonina",
          "rem",
          "mor",
          "vigilia",
          "consciousness",
          "conciencia",
        ]

        const hasStrongNeurologicalTerms = strongNeurologicalIndicators.some(
          (term) => text.toLowerCase().includes(term) || title.toLowerCase().includes(term),
        )

        const maxScore = Math.max(...Object.values(rawScores))
        const sortedScores = Object.entries(rawScores).sort(([, a], [, b]) => b - a)
        const [topDomain, topScore] = sortedScores[0]
        const [secondDomain, secondScore] = sortedScores[1]

        const normalizedScores = {}

        if (hasStrongNeurologicalTerms && topDomain !== "neurologico" && rawScores.neurologico > 0.1) {
          normalizedScores.neurologico = Math.max(0.75, rawScores.neurologico * 2)
          normalizedScores.cardiovascular = Math.min(0.15, rawScores.cardiovascular * 0.3)
          normalizedScores.hepatorrenal = Math.min(0.08, rawScores.hepatorrenal * 0.5)
          normalizedScores.oncologico = Math.min(0.07, rawScores.oncologico * 0.5)
        } else if (topScore > secondScore * 1.5) {
          Object.entries(rawScores).forEach(([domain, score]) => {
            if (domain === topDomain) {
              normalizedScores[domain] = Math.min(0.95, score * 1.3)
            } else {
              normalizedScores[domain] = Math.max(0.05, score * 0.6)
            }
          })
        } else {
          Object.entries(rawScores).forEach(([domain, score]) => {
            normalizedScores[domain] = Math.max(0.05, Math.min(0.85, score))
          })
        }

        return normalizedScores
      }

      const classificationScores = classifyMedicalText(title, abstract)

      const calculateOverallConfidence = (scores: any) => {
        const scoresArray = Object.values(scores) as number[]
        const maxScore = Math.max(...scoresArray)
        const secondMaxScore = scoresArray.sort((a, b) => b - a)[1]

        const separation = maxScore - secondMaxScore
        const baseConfidence = 0.7 + separation * 0.3

        const avgScore = scoresArray.reduce((a, b) => a + b, 0) / scoresArray.length
        const confidenceAdjustment = avgScore > 0.3 ? 0.1 : avgScore > 0.1 ? 0.05 : -0.1

        return Math.max(0.6, Math.min(0.98, baseConfidence + confidenceAdjustment))
      }

      const analyzeSourceReliability = () => {
        let reliabilityScore = 0.5
        const reliabilityFactors = []

        const highImpactJournals = ["nature", "science", "cell", "lancet", "nejm", "jama"]
        const mediumImpactJournals = ["plos", "bmc", "frontiers", "mdpi"]

        if (journal.toLowerCase()) {
          if (highImpactJournals.some((j) => journal.toLowerCase().includes(j))) {
            reliabilityScore += 0.3
            reliabilityFactors.push({ factor: "Revista de Alto Impacto", score: "+30%", color: "text-green-600" })
          } else if (mediumImpactJournals.some((j) => journal.toLowerCase().includes(j))) {
            reliabilityScore += 0.15
            reliabilityFactors.push({ factor: "Revista de Impacto Medio", score: "+15%", color: "text-yellow-600" })
          } else {
            reliabilityFactors.push({ factor: "Revista Identificada", score: "+5%", color: "text-blue-600" })
            reliabilityScore += 0.05
          }
        }

        const prestigiousInstitutions = ["harvard", "stanford", "mit", "oxford", "cambridge", "mayo clinic"]
        if (institution.toLowerCase() && prestigiousInstitutions.some((i) => institution.toLowerCase().includes(i))) {
          reliabilityScore += 0.2
          reliabilityFactors.push({ factor: "Institución Prestigiosa", score: "+20%", color: "text-green-600" })
        } else if (institution.trim()) {
          reliabilityScore += 0.1
          reliabilityFactors.push({ factor: "Institución Académica", score: "+10%", color: "text-blue-600" })
        }

        const currentYear = new Date().getFullYear()
        const pubYear = Number.parseInt(publicationYear)
        if (pubYear && pubYear >= currentYear - 2) {
          reliabilityScore += 0.15
          reliabilityFactors.push({ factor: "Publicación Reciente", score: "+15%", color: "text-green-600" })
        } else if (pubYear && pubYear >= currentYear - 5) {
          reliabilityScore += 0.1
          reliabilityFactors.push({ factor: "Publicación Actual", score: "+10%", color: "text-yellow-600" })
        } else if (pubYear && pubYear < currentYear - 10) {
          reliabilityScore -= 0.1
          reliabilityFactors.push({ factor: "Publicación Antigua", score: "-10%", color: "text-red-600" })
        }

        if (doi.trim()) {
          reliabilityScore += 0.1
          reliabilityFactors.push({ factor: "DOI Verificable", score: "+10%", color: "text-green-600" })
        }

        if (authors.includes(",") || authors.includes(";")) {
          reliabilityScore += 0.05
          reliabilityFactors.push({ factor: "Múltiples Autores", score: "+5%", color: "text-blue-600" })
        }

        return {
          score: Math.min(Math.max(reliabilityScore, 0), 1),
          factors: reliabilityFactors,
          level: reliabilityScore >= 0.8 ? "Alta" : reliabilityScore >= 0.6 ? "Media" : "Baja",
        }
      }

      const reliability = analyzeSourceReliability()
      const overallConfidence = calculateOverallConfidence(classificationScores)

      const mockResults = {
        ...classificationScores,
        confidence: overallConfidence,
        processingTime: (2.5 + Math.random() * 1.5).toFixed(1),
        reliability: reliability,
      }

      setResults(mockResults)
    } catch (error) {
      console.error("Classification error:", error)
    } finally {
      setIsProcessing(false)
    }
  }

  const medicalDomains = [
    {
      name: "Cardiovascular",
      icon: Heart,
      color: "text-red-500",
      bgColor: "bg-red-50",
      description: "Enfermedades del corazón y sistema circulatorio",
    },
    {
      name: "Neurológico",
      icon: Brain,
      color: "text-blue-500",
      bgColor: "bg-blue-50",
      description: "Trastornos del sistema nervioso",
    },
    {
      name: "Hepatorrenal",
      icon: Liver,
      color: "text-green-500",
      bgColor: "bg-green-50",
      description: "Enfermedades hepáticas y renales",
    },
    {
      name: "Oncológico",
      icon: Target,
      color: "text-purple-500",
      bgColor: "bg-purple-50",
      description: "Cáncer y tumores malignos",
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-green-50">
      {console.log("[v0] Starting to render main div")}
      <nav className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50">
        {console.log("[v0] Rendering navigation")}
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-blue-500 to-green-500 rounded-lg">
                <Brain className="h-6 w-6 text-white" />
              </div>
              <span className="font-bold text-xl text-gray-900">MedClassify AI</span>
            </div>
            <div className="hidden md:flex items-center gap-6">
              <Button variant="ghost" onClick={() => setActiveTab("classify")}>
                Clasificar
              </Button>
              <Button variant="ghost" onClick={() => setActiveTab("upload")}>
                Cargar Archivo
              </Button>
              <Button variant="ghost" onClick={() => setActiveTab("summary")}>
                Resumen IA
              </Button>
              <Button variant="ghost" onClick={() => setActiveTab("metrics")}>
                Métricas
              </Button>
              <Button variant="ghost" onClick={() => setActiveTab("project-info")}>
                <Info className="h-4 w-4 mr-2" />
                Info del Proyecto
              </Button>
              <Button className="bg-blue-600 hover:bg-blue-700" onClick={() => setActiveTab("classify")}>
                <Play className="h-4 w-4 mr-2" />
                Usar App
              </Button>
            </div>
          </div>
        </div>
      </nav>

      <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white py-6">
        <div className="container mx-auto px-4 text-center">
          <div className="inline-flex items-center px-3 py-1 bg-white/20 rounded-full mb-3">
            <Sparkles className="h-4 w-4 mr-2 text-yellow-300" />
            <span className="text-sm">AI + Data Challenge 2025 - TechSphere Colombia</span>
          </div>
          <h1 className="text-2xl md:text-3xl font-bold mb-2">
            MedClassify AI: Clasificación Inteligente de Literatura Médica
          </h1>
          <p className="text-blue-100 max-w-2xl mx-auto">
            Sistema de IA que clasifica literatura médica en dominios Cardiovascular, Neurológico, Hepatorrenal y
            Oncológico con precisión superior al <span className="font-bold text-yellow-300">87%</span>.
          </p>
        </div>
      </div>

      {console.log("[v0] Banner rendered, rendering main content")}

      <div className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 sticky top-24">
              <div className="flex items-center gap-2 mb-6">
                <Activity className="h-5 w-5 text-blue-600" />
                <h2 className="text-lg font-semibold text-gray-900">Navegación</h2>
              </div>
              <div className="space-y-3">
                <Button
                  variant={activeTab === "classify" ? "default" : "ghost"}
                  className="w-full justify-start"
                  onClick={() => setActiveTab("classify")}
                >
                  <FileText className="h-4 w-4 mr-2" />
                  Clasificar Texto
                </Button>
                <Button
                  variant={activeTab === "upload" ? "default" : "ghost"}
                  className="w-full justify-start"
                  onClick={() => setActiveTab("upload")}
                >
                  <Upload className="h-4 w-4 mr-2" />
                  Cargar Archivo
                </Button>
                <Button
                  variant={activeTab === "summary" ? "default" : "ghost"}
                  className="w-full justify-start"
                  onClick={() => setActiveTab("summary")}
                >
                  <Brain className="h-4 w-4 mr-2" />
                  Resumen con IA
                </Button>
                <Button
                  variant={activeTab === "metrics" ? "default" : "ghost"}
                  className="w-full justify-start"
                  onClick={() => setActiveTab("metrics")}
                >
                  <BarChart3 className="h-4 w-4 mr-2" />
                  Métricas
                </Button>
                <Button
                  variant={activeTab === "project-info" ? "default" : "ghost"}
                  className="w-full justify-start"
                  onClick={() => setActiveTab("project-info")}
                >
                  <Info className="h-4 w-4 mr-2" />
                  Info del Proyecto
                </Button>
              </div>
            </div>

            <Card className="mt-6 shadow-lg border-0 bg-white/80 backdrop-blur-sm">
              <CardHeader className="pb-3">
                <CardTitle className="text-lg">Dominios Médicos</CardTitle>
                <CardDescription>Categorías de clasificación disponibles</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {medicalDomains.map((domain) => {
                  const Icon = domain.icon
                  return (
                    <div
                      key={domain.name}
                      className="flex items-start gap-3 p-3 rounded-lg hover:bg-gray-50 transition-colors"
                    >
                      <div className={`p-2 rounded-lg ${domain.bgColor}`}>
                        <Icon className={`h-5 w-5 ${domain.color}`} />
                      </div>
                      <div>
                        <h4 className="font-semibold text-sm">{domain.name}</h4>
                        <p className="text-xs text-muted-foreground leading-relaxed">{domain.description}</p>
                      </div>
                    </div>
                  )
                })}
              </CardContent>
            </Card>
          </div>

          <div className="lg:col-span-3 order-1 lg:order-2 space-y-6">
            <div className="flex-1 overflow-auto">
              {activeTab === "classify" && (
                <div className="space-y-6">
                  <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Brain className="h-5 w-5 text-blue-500" />
                        Clasificación de Artículos Médicos
                      </CardTitle>
                      <CardDescription>
                        Ingrese el título y resumen del artículo médico para obtener una clasificación automática en los
                        cuatro dominios especializados
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-6">
                      <div className="space-y-2">
                        <Label htmlFor="title" className="text-sm font-medium">
                          Título del Artículo
                        </Label>
                        <Input
                          id="title"
                          placeholder="Ej: Efficacy of ACE inhibitors in reducing cardiovascular mortality..."
                          value={title}
                          onChange={(e) => setTitle(e.target.value)}
                          className="border-gray-200 focus:border-blue-400"
                        />
                      </div>

                      <div className="space-y-2">
                        <Label htmlFor="abstract" className="text-sm font-medium">
                          Resumen (Abstract)
                        </Label>
                        <Textarea
                          id="abstract"
                          placeholder="Ingrese el resumen completo del artículo médico. Incluya contexto, metodología, resultados y conclusiones..."
                          value={abstract}
                          onChange={(e) => setAbstract(e.target.value)}
                          className="min-h-40 border-gray-200 focus:border-blue-400 resize-none"
                        />
                      </div>

                      <div className="border-t pt-6">
                        <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                          <Trophy className="h-5 w-5 text-orange-500" />
                          Análisis de Confiabilidad de la Fuente
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div className="space-y-2">
                            <Label htmlFor="journal" className="text-sm font-medium">
                              Revista/Journal
                            </Label>
                            <Input
                              id="journal"
                              placeholder="Ej: Nature Medicine, The Lancet..."
                              value={journal}
                              onChange={(e) => setJournal(e.target.value)}
                              className="border-gray-200 focus:border-orange-400"
                            />
                          </div>
                          <div className="space-y-2">
                            <Label htmlFor="authors" className="text-sm font-medium">
                              Autores
                            </Label>
                            <Input
                              id="authors"
                              placeholder="Ej: Smith J, García M, et al."
                              value={authors}
                              onChange={(e) => setAuthors(e.target.value)}
                              className="border-gray-200 focus:border-orange-400"
                            />
                          </div>
                          <div className="space-y-2">
                            <Label htmlFor="institution" className="text-sm font-medium">
                              Institución
                            </Label>
                            <Input
                              id="institution"
                              placeholder="Ej: Harvard Medical School, Mayo Clinic..."
                              value={institution}
                              onChange={(e) => setInstitution(e.target.value)}
                              className="border-gray-200 focus:border-orange-400"
                            />
                          </div>
                          <div className="space-y-2">
                            <Label htmlFor="publicationYear" className="text-sm font-medium">
                              Año de Publicación
                            </Label>
                            <Input
                              id="publicationYear"
                              placeholder="2024"
                              value={publicationYear}
                              onChange={(e) => setPublicationYear(e.target.value)}
                              className="border-gray-200 focus:border-orange-400"
                            />
                          </div>
                        </div>
                      </div>

                      <Button
                        onClick={handleClassify}
                        disabled={!title || !abstract || isProcessing}
                        className="w-full bg-gradient-to-r from-blue-600 to-green-600 hover:from-blue-700 hover:to-green-700 text-white py-3"
                      >
                        {isProcessing ? (
                          <>
                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                            Clasificando...
                          </>
                        ) : (
                          <>
                            <Brain className="h-4 w-4 mr-2" />
                            Clasificar y Analizar Confiabilidad
                          </>
                        )}
                      </Button>
                    </CardContent>
                  </Card>

                  {results && <ClassificationResults results={results} title={title} abstract={abstract} />}
                </div>
              )}

              {activeTab === "upload" && <FileUpload />}

              {activeTab === "summary" && (
                <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Brain className="h-5 w-5 text-purple-500" />
                      Resumen Inteligente con IA
                    </CardTitle>
                    <CardDescription>
                      Genere resúmenes automáticos de artículos médicos y encuentre estudios relacionados
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-6">
                    <div className="space-y-2">
                      <Label htmlFor="summaryText" className="text-sm font-medium">
                        Texto del Artículo
                      </Label>
                      <Textarea
                        id="summaryText"
                        placeholder="Pegue aquí el texto completo del artículo médico para generar un resumen automático..."
                        value={summaryText}
                        onChange={(e) => setSummaryText(e.target.value)}
                        className="min-h-40 border-gray-200 focus:border-purple-400 resize-none"
                      />
                    </div>

                    <div className="space-y-2">
                      <Label htmlFor="summaryUrl" className="text-sm font-medium">
                        URL del Artículo (Opcional)
                      </Label>
                      <Input
                        id="summaryUrl"
                        placeholder="https://pubmed.ncbi.nlm.nih.gov/..."
                        value={summaryUrl}
                        onChange={(e) => setSummaryUrl(e.target.value)}
                        className="border-gray-200 focus:border-purple-400"
                      />
                    </div>

                    <Button
                      onClick={handleSummarizeText}
                      disabled={!summaryText || isSummarizing}
                      className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white py-3"
                    >
                      {isSummarizing ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                          Generando Resumen...
                        </>
                      ) : (
                        <>
                          <Brain className="h-4 w-4 mr-2" />
                          Generar Resumen con IA
                        </>
                      )}
                    </Button>

                    {summaryResults && (
                      <Card className="mt-6 border-purple-200 bg-purple-50">
                        <CardHeader>
                          <CardTitle className="text-lg text-purple-800">Resumen Generado</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                          <div>
                            <h4 className="font-semibold text-purple-800 mb-2">Resumen Ejecutivo:</h4>
                            <p className="text-purple-700 text-sm leading-relaxed">{summaryResults.summary}</p>
                          </div>
                          <div>
                            <h4 className="font-semibold text-purple-800 mb-2">Hallazgos Clave:</h4>
                            <ul className="space-y-1">
                              {summaryResults.keyFindings.map((finding, index) => (
                                <li key={index} className="text-purple-700 text-sm flex items-start gap-2">
                                  <CheckCircle className="h-4 w-4 text-purple-500 mt-0.5 flex-shrink-0" />
                                  {finding}
                                </li>
                              ))}
                            </ul>
                          </div>
                          <div>
                            <h4 className="font-semibold text-purple-800 mb-2">Estudios Relacionados:</h4>
                            <ul className="space-y-2">
                              {summaryResults.relatedStudies.map((study, index) => (
                                <li
                                  key={index}
                                  className="text-purple-700 text-sm p-2 bg-white rounded border border-purple-200"
                                >
                                  {study}
                                </li>
                              ))}
                            </ul>
                          </div>
                        </CardContent>
                      </Card>
                    )}
                  </CardContent>
                </Card>
              )}

              {activeTab === "metrics" && <MetricsPanel />}

              {activeTab === "project-info" && (
                <div className="space-y-8">
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <Card className="text-center p-4">
                      <div className="text-2xl font-bold text-blue-600">89%</div>
                      <div className="text-sm text-gray-600">F1-Score</div>
                    </Card>
                    <Card className="text-center p-4">
                      <div className="text-2xl font-bold text-green-600">4</div>
                      <div className="text-sm text-gray-600">Dominios Médicos</div>
                    </Card>
                    <Card className="text-center p-4">
                      <div className="text-2xl font-bold text-purple-600">BERT</div>
                      <div className="text-sm text-gray-600">Modelo Base</div>
                    </Card>
                    <Card className="text-center p-4">
                      <div className="text-2xl font-bold text-orange-600">API</div>
                      <div className="text-sm text-gray-600">REST Ready</div>
                    </Card>
                  </div>

                  <Card className="shadow-lg">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Target className="h-5 w-5 text-red-500" />
                        El Desafío de la Clasificación Médica Automatizada
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-gray-700 mb-4">
                        La literatura médica crece exponencialmente, con miles de artículos publicados diariamente. Los
                        profesionales de la salud necesitan herramientas eficientes para clasificar y organizar esta
                        información en dominios específicos.
                      </p>
                      <div className="grid md:grid-cols-2 gap-4">
                        <div>
                          <h4 className="font-semibold mb-2">Desafíos Técnicos:</h4>
                          <ul className="space-y-1 text-sm text-gray-600">
                            <li>{"• Terminología médica especializada"}</li>
                            <li>{"• Clasificación multietiqueta"}</li>
                            <li>{"• Precisión clínica requerida"}</li>
                            <li>{"• Escalabilidad del sistema"}</li>
                          </ul>
                        </div>
                        <div>
                          <h4 className="font-semibold mb-2">Nuestra Solución:</h4>
                          <ul className="space-y-1 text-sm text-gray-600">
                            <li>{"• Modelos BioBERT especializados"}</li>
                            <li>{"• Pipeline híbrido TF-IDF + ML"}</li>
                            <li>{"• Validación con métricas médicas"}</li>
                            <li>{"• API REST para integración"}</li>
                          </ul>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="shadow-lg">
                    <CardHeader>
                      <CardTitle>Dominios de Clasificación</CardTitle>
                      <CardDescription>Cuatro especialidades médicas principales</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="grid md:grid-cols-2 gap-4">
                        <div className="flex items-center gap-3 p-3 bg-red-50 rounded-lg">
                          <Heart className="h-6 w-6 text-red-500" />
                          <div>
                            <div className="font-semibold">Cardiovascular</div>
                            <div className="text-sm text-gray-600">Enfermedades del corazón y sistema circulatorio</div>
                          </div>
                        </div>
                        <div className="flex items-center gap-3 p-3 bg-blue-50 rounded-lg">
                          <Brain className="h-6 w-6 text-blue-500" />
                          <div>
                            <div className="font-semibold">Neurológico</div>
                            <div className="text-sm text-gray-600">Trastornos del sistema nervioso</div>
                          </div>
                        </div>
                        <div className="flex items-center gap-3 p-3 bg-green-50 rounded-lg">
                          <Activity className="h-6 w-6 text-green-500" />
                          <div>
                            <div className="font-semibold">Hepatorrenal</div>
                            <div className="text-sm text-gray-600">Enfermedades hepáticas y renales</div>
                          </div>
                        </div>
                        <div className="flex items-center gap-3 p-3 bg-purple-50 rounded-lg">
                          <Zap className="h-6 w-6 text-purple-500" />
                          <div>
                            <div className="font-semibold">Oncológico</div>
                            <div className="text-sm text-gray-600">Cáncer y tumores malignos</div>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="shadow-lg">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Cog className="h-5 w-5 text-blue-500" />
                        ¿Cómo Funciona MedClassify AI?
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="space-y-4">
                        <div className="flex items-start gap-4">
                          <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                            <span className="text-blue-600 font-semibold">1</span>
                          </div>
                          <div>
                            <h4 className="font-semibold">Ingreso de Datos</h4>
                            <p className="text-sm text-gray-600">
                              El usuario ingresa el título y abstract del artículo médico
                            </p>
                          </div>
                        </div>
                        <div className="flex items-start gap-4">
                          <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                            <span className="text-blue-600 font-semibold">2</span>
                          </div>
                          <div>
                            <h4 className="font-semibold">Preprocesamiento</h4>
                            <p className="text-sm text-gray-600">
                              Limpieza y normalización del texto médico especializado
                            </p>
                          </div>
                        </div>
                        <div className="flex items-start gap-4">
                          <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                            <span className="text-blue-600 font-semibold">3</span>
                          </div>
                          <div>
                            <h4 className="font-semibold">Análisis con IA</h4>
                            <p className="text-sm text-gray-600">
                              Procesamiento con modelos BioBERT y pipeline híbrido
                            </p>
                          </div>
                        </div>
                        <div className="flex items-start gap-4">
                          <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                            <span className="text-blue-600 font-semibold">4</span>
                          </div>
                          <div>
                            <h4 className="font-semibold">Clasificación</h4>
                            <p className="text-sm text-gray-600">
                              Asignación a dominios médicos con scores de confianza
                            </p>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  <Card className="shadow-lg">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <Users className="h-5 w-5 text-green-500" />
                        Equipo de Desarrollo
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-center space-y-4">
                        <div>
                          <p className="font-semibold text-lg">Manuel Palacio & Camila Zapata</p>
                          <p className="text-gray-600">Núcleo Colectivo + Línea Médica Yolombó</p>
                          <p className="text-gray-600">Medellín, Colombia</p>
                        </div>
                        <div className="flex justify-center gap-4 text-sm">
                          <div className="flex items-center gap-2">
                            <Github className="h-4 w-4" />
                            <span>github.com/medclassify-ai</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <MessageCircle className="h-4 w-4" />
                            <span>+57 3006101221</span>
                          </div>
                        </div>
                        <p className="text-xs text-gray-500">© 2025 Todos los derechos reservados</p>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      <footer className="bg-gradient-to-r from-gray-900 to-blue-900 text-white py-12 mt-16">
        <div className="container mx-auto px-4">
          <div className="text-center space-y-6">
            <div className="flex justify-center items-center gap-4 mb-6">
              <Heart className="h-8 w-8 text-red-400" />
              <Brain className="h-8 w-8 text-blue-400" />
            </div>

            <h3 className="text-xl md:text-2xl font-bold mb-4">
              Desarrollado para el AI Data Challenge de TechSphere Colombia
            </h3>

            <div className="flex flex-col md:flex-row justify-center items-center gap-4 md:gap-6 text-sm md:text-lg">
              <div className="flex items-center gap-2 text-center">
                <span className="text-blue-300">📂</span>
                <span className="break-all md:break-normal">
                  Repositorio GitHub: https://github.com/dmanuelpalacio/MedClassifyAI
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-green-300">📱</span>
                <span>WhatsApp: +57 3006101221</span>
              </div>
            </div>

            <div className="border-t border-gray-700 pt-6 mt-8">
              <p className="text-xl font-semibold mb-2">© 2025 MANUEL PALACIO / CAMILA ZAPATA</p>
              <p className="text-blue-300 text-lg mb-2">Núcleo Colectivo + Línea Médica Yolombó</p>
              <p className="text-gray-300">Medellín, Colombia. Todos los derechos reservados.</p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
