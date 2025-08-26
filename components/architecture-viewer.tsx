"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Network, Download, Eye, Layers } from "lucide-react"
import Image from "next/image"

export function ArchitectureViewer() {
  const downloadDiagram = () => {
    const link = document.createElement("a")
    link.href = "/architecture_diagram.png"
    link.download = "medclassify_architecture.png"
    link.click()
  }

  return (
    <Card className="shadow-lg border-0">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-xl flex items-center gap-2">
              <Network className="h-5 w-5 text-blue-600" />
              Diagrama de Arquitectura del Sistema
            </CardTitle>
            <p className="text-sm text-muted-foreground mt-1">
              Pipeline completo de clasificación médica multietiqueta
            </p>
          </div>
          <Button variant="outline" size="sm" onClick={downloadDiagram}>
            <Download className="h-4 w-4 mr-2" />
            Descargar PNG
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Imagen del diagrama */}
          <div className="relative w-full h-96 bg-gray-50 rounded-lg overflow-hidden">
            <Image
              src="/architecture_diagram.png"
              alt="Diagrama de Arquitectura MedClassify AI"
              fill
              className="object-contain"
              priority
            />
          </div>

          {/* Descripción de componentes */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <h4 className="font-semibold text-gray-800 flex items-center gap-2">
                <Layers className="h-4 w-4 text-blue-600" />
                Componentes Principales
              </h4>
              <div className="space-y-3">
                <div className="flex items-center gap-3">
                  <Badge variant="secondary" className="bg-blue-100 text-blue-800">
                    Entrada
                  </Badge>
                  <span className="text-sm">Dataset oficial 3,565 registros</span>
                </div>
                <div className="flex items-center gap-3">
                  <Badge variant="secondary" className="bg-orange-100 text-orange-800">
                    Preproceso
                  </Badge>
                  <span className="text-sm">Limpieza y tokenización médica</span>
                </div>
                <div className="flex items-center gap-3">
                  <Badge variant="secondary" className="bg-green-100 text-green-800">
                    Modelos
                  </Badge>
                  <span className="text-sm">Baseline, Híbrido, Zero-shot</span>
                </div>
                <div className="flex items-center gap-3">
                  <Badge variant="secondary" className="bg-purple-100 text-purple-800">
                    Evaluación
                  </Badge>
                  <span className="text-sm">Métricas multietiqueta completas</span>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h4 className="font-semibold text-gray-800 flex items-center gap-2">
                <Eye className="h-4 w-4 text-green-600" />
                Características Técnicas
              </h4>
              <div className="space-y-3 text-sm">
                <div className="bg-gray-50 p-3 rounded-lg">
                  <p className="font-medium text-gray-800">Pipeline Híbrido</p>
                  <p className="text-gray-600">Combina TF-IDF + BioBERT embeddings para máxima precisión</p>
                </div>
                <div className="bg-gray-50 p-3 rounded-lg">
                  <p className="font-medium text-gray-800">Evaluación Robusta</p>
                  <p className="text-gray-600">F1-Score, Exact Match, Hamming Loss, ROC-AUC por clase</p>
                </div>
                <div className="bg-gray-50 p-3 rounded-lg">
                  <p className="font-medium text-gray-800">Despliegue Completo</p>
                  <p className="text-gray-600">API REST + Dashboard V0 + Vercel hosting</p>
                </div>
              </div>
            </div>
          </div>

          {/* Flujo de datos */}
          <div className="bg-blue-50 p-4 rounded-lg">
            <h4 className="font-semibold text-blue-800 mb-3">🔄 Flujo de Procesamiento</h4>
            <div className="flex flex-wrap items-center gap-2 text-sm">
              <Badge className="bg-blue-600">Título + Abstract</Badge>
              <span>→</span>
              <Badge className="bg-orange-600">Preprocesamiento</Badge>
              <span>→</span>
              <Badge className="bg-green-600">Vectorización</Badge>
              <span>→</span>
              <Badge className="bg-purple-600">Clasificación</Badge>
              <span>→</span>
              <Badge className="bg-red-600">Evaluación</Badge>
              <span>→</span>
              <Badge className="bg-indigo-600">Predicción Final</Badge>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
