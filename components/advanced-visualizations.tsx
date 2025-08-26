"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import {
  BarChart3,
  PieChart,
  TrendingUp,
  Download,
  FileSpreadsheet,
  FileText,
  Share2,
  Eye,
  AlertTriangle,
  CheckCircle,
  XCircle,
} from "lucide-react"
import { useState } from "react"

interface VisualizationProps {
  results: {
    cardiovascular: number
    neurologico: number
    hepatorrenal: number
    oncologico: number
    confidence: number
    processingTime: string
    reliability: {
      score: number
      level: string
      factors: Array<{
        factor: string
        score: string
        color: string
      }>
    }
  }
  title: string
  abstract: string
}

export function AdvancedVisualizations({ results, title, abstract }: VisualizationProps) {
  const [activeChart, setActiveChart] = useState("bar")

  const domains = [
    { name: "Cardiovascular", value: results.cardiovascular, color: "bg-red-500" },
    { name: "Neurológico", value: results.neurologico, color: "bg-blue-500" },
    { name: "Hepatorrenal", value: results.hepatorrenal, color: "bg-green-500" },
    { name: "Oncológico", value: results.oncologico, color: "bg-purple-500" },
  ]

  const sortedDomains = [...domains].sort((a, b) => b.value - a.value)
  const primaryDomain = sortedDomains[0]
  const secondaryDomains = sortedDomains.slice(1).filter((d) => d.value > 0.3)

  const exportToCSV = () => {
    const csvData = [
      ["Dominio", "Confianza", "Porcentaje"],
      ...domains.map((d) => [d.name, d.value.toFixed(3), `${(d.value * 100).toFixed(1)}%`]),
      ["", "", ""],
      ["Confiabilidad General", results.confidence.toFixed(3), `${(results.confidence * 100).toFixed(1)}%`],
      [
        "Confiabilidad de Fuente",
        results.reliability.score.toFixed(3),
        `${(results.reliability.score * 100).toFixed(1)}%`,
      ],
      ["Nivel de Confiabilidad", results.reliability.level, ""],
      ["Tiempo de Procesamiento", `${results.processingTime}s`, ""],
    ]

    const csvContent = csvData.map((row) => row.join(",")).join("\n")
    const blob = new Blob([csvContent], { type: "text/csv" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `clasificacion_medica_${new Date().toISOString().split("T")[0]}.csv`
    a.click()
    URL.revokeObjectURL(url)
  }

  const exportToJSON = () => {
    const jsonData = {
      titulo: title,
      resumen: abstract.substring(0, 200) + "...",
      clasificacion: {
        cardiovascular: results.cardiovascular,
        neurologico: results.neurologico,
        hepatorrenal: results.hepatorrenal,
        oncologico: results.oncologico,
      },
      confiabilidad: {
        general: results.confidence,
        fuente: results.reliability.score,
        nivel: results.reliability.level,
        factores: results.reliability.factors,
      },
      metadatos: {
        fecha_analisis: new Date().toISOString(),
        tiempo_procesamiento: `${results.processingTime}s`,
        dominio_principal: primaryDomain.name,
        dominios_secundarios: secondaryDomains.map((d) => d.name),
      },
    }

    const blob = new Blob([JSON.stringify(jsonData, null, 2)], { type: "application/json" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = `clasificacion_medica_${new Date().toISOString().split("T")[0]}.json`
    a.click()
    URL.revokeObjectURL(url)
  }

  const getReliabilityIcon = (level: string) => {
    switch (level) {
      case "Alta":
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case "Media":
        return <AlertTriangle className="h-5 w-5 text-yellow-500" />
      case "Baja":
        return <XCircle className="h-5 w-5 text-red-500" />
      default:
        return <AlertTriangle className="h-5 w-5 text-gray-500" />
    }
  }

  return (
    <div className="space-y-6">
      {/* Export Controls */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Share2 className="h-5 w-5 text-blue-500" />
            Exportar Resultados
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-3">
            <Button onClick={exportToCSV} variant="outline" className="flex items-center gap-2 bg-transparent">
              <FileSpreadsheet className="h-4 w-4" />
              Exportar CSV
            </Button>
            <Button onClick={exportToJSON} variant="outline" className="flex items-center gap-2 bg-transparent">
              <FileText className="h-4 w-4" />
              Exportar JSON
            </Button>
            <Button onClick={() => window.print()} variant="outline" className="flex items-center gap-2">
              <Download className="h-4 w-4" />
              Imprimir Reporte
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Advanced Charts */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="h-5 w-5 text-blue-500" />
              Visualizaciones Avanzadas
            </CardTitle>
            <div className="flex gap-2">
              <Button
                size="sm"
                variant={activeChart === "bar" ? "default" : "outline"}
                onClick={() => setActiveChart("bar")}
              >
                <BarChart3 className="h-4 w-4" />
              </Button>
              <Button
                size="sm"
                variant={activeChart === "pie" ? "default" : "outline"}
                onClick={() => setActiveChart("pie")}
              >
                <PieChart className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          {activeChart === "bar" && (
            <div className="space-y-6">
              <div className="grid gap-4">
                {sortedDomains.map((domain, index) => (
                  <div key={domain.name} className="space-y-2">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className={`w-4 h-4 rounded ${domain.color}`} />
                        <span className="font-medium">{domain.name}</span>
                        {index === 0 && (
                          <Badge variant="secondary" className="text-xs">
                            Principal
                          </Badge>
                        )}
                      </div>
                      <span className="text-sm font-mono">{(domain.value * 100).toFixed(1)}%</span>
                    </div>
                    <Progress value={domain.value * 100} className="h-3" />
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeChart === "pie" && (
            <div className="flex items-center justify-center">
              <div className="relative w-64 h-64">
                <svg viewBox="0 0 100 100" className="w-full h-full transform -rotate-90">
                  {(() => {
                    let cumulativePercentage = 0
                    return sortedDomains.map((domain, index) => {
                      const percentage = domain.value * 100
                      const strokeDasharray = `${percentage} ${100 - percentage}`
                      const strokeDashoffset = -cumulativePercentage
                      cumulativePercentage += percentage

                      const colors = ["#ef4444", "#3b82f6", "#10b981", "#8b5cf6"]

                      return (
                        <circle
                          key={domain.name}
                          cx="50"
                          cy="50"
                          r="15.915"
                          fill="transparent"
                          stroke={colors[index]}
                          strokeWidth="8"
                          strokeDasharray={strokeDasharray}
                          strokeDashoffset={strokeDashoffset}
                          className="transition-all duration-500"
                        />
                      )
                    })
                  })()}
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-800">{(results.confidence * 100).toFixed(0)}%</div>
                    <div className="text-xs text-gray-600">Confianza</div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Detailed Analysis */}
      <Card className="shadow-lg border-0 bg-white/80 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5 text-green-500" />
            Análisis Detallado
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Classification Summary */}
          <div className="p-4 bg-gradient-to-r from-blue-50 to-green-50 rounded-lg border border-blue-200">
            <h3 className="font-semibold text-lg mb-2 flex items-center gap-2">
              <Eye className="h-5 w-5 text-blue-600" />
              Resumen de Clasificación
            </h3>
            <div className="grid md:grid-cols-2 gap-4 text-sm">
              <div>
                <span className="font-medium">Dominio Principal:</span>
                <div className="flex items-center gap-2 mt-1">
                  <div className={`w-3 h-3 rounded ${primaryDomain.color}`} />
                  <span>{primaryDomain.name}</span>
                  <Badge variant="secondary">{(primaryDomain.value * 100).toFixed(1)}%</Badge>
                </div>
              </div>
              <div>
                <span className="font-medium">Confianza General:</span>
                <div className="flex items-center gap-2 mt-1">
                  <Progress value={results.confidence * 100} className="flex-1 h-2" />
                  <span>{(results.confidence * 100).toFixed(1)}%</span>
                </div>
              </div>
              {secondaryDomains.length > 0 && (
                <div className="md:col-span-2">
                  <span className="font-medium">Dominios Secundarios:</span>
                  <div className="flex flex-wrap gap-2 mt-1">
                    {secondaryDomains.map((domain) => (
                      <Badge key={domain.name} variant="outline" className="text-xs">
                        {domain.name}: {(domain.value * 100).toFixed(1)}%
                      </Badge>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Reliability Analysis */}
          <div className="p-4 bg-gradient-to-r from-orange-50 to-red-50 rounded-lg border border-orange-200">
            <h3 className="font-semibold text-lg mb-2 flex items-center gap-2">
              {getReliabilityIcon(results.reliability.level)}
              Análisis de Confiabilidad de la Fuente
            </h3>
            <div className="grid md:grid-cols-2 gap-4 text-sm">
              <div>
                <span className="font-medium">Nivel de Confiabilidad:</span>
                <div className="flex items-center gap-2 mt-1">
                  <Badge
                    variant={
                      results.reliability.level === "Alta"
                        ? "default"
                        : results.reliability.level === "Media"
                          ? "secondary"
                          : "destructive"
                    }
                  >
                    {results.reliability.level}
                  </Badge>
                  <span>{(results.reliability.score * 100).toFixed(1)}%</span>
                </div>
              </div>
              <div>
                <span className="font-medium">Tiempo de Procesamiento:</span>
                <div className="mt-1">
                  <span className="font-mono">{results.processingTime}s</span>
                </div>
              </div>
              <div className="md:col-span-2">
                <span className="font-medium">Factores de Confiabilidad:</span>
                <div className="grid gap-2 mt-2">
                  {results.reliability.factors.map((factor, index) => (
                    <div key={index} className="flex items-center justify-between p-2 bg-white rounded border">
                      <span className="text-sm">{factor.factor}</span>
                      <span className={`text-sm font-medium ${factor.color}`}>{factor.score}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
