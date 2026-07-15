import { useLayoutEffect } from "react";
import { usePageHeader } from "@/contexts/usePageHeader";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Scale, FileText, ShieldAlert, Cpu } from "lucide-react";

export default function LegalDepartmentPage() {
  const { setAfterTitle, setTitle } = usePageHeader();

  useLayoutEffect(() => {
    setTitle("Dział Prawny");
    setAfterTitle(
      <Badge className="border border-indigo-400/30 bg-indigo-400/10 text-[10px] text-indigo-400">
        SMART ROUTING (GCP)
      </Badge>
    );
    return () => {
      setTitle(null);
      setAfterTitle(null);
    };
  }, [setAfterTitle, setTitle]);

  return (
    <div className="flex h-full min-h-0 flex-col gap-5 p-4 overflow-y-auto">
      <div className="mb-2">
        <h2 className="font-expanded text-2xl font-bold tracking-[0.04em] text-midground blend-lighter">
          Zautomatyzowany Radca Prawny
        </h2>
        <p className="text-sm text-muted-foreground mt-1 max-w-2xl">
          Wykorzystuje modele długiego kontekstu (Llama 3 / Gemma 2 via Vertex AI Model Garden) do analizy umów najmu, NDA oraz wyłapywania potencjalnych haczyków prawnych.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card className="bg-card/40 border-border/50 hover:border-indigo-400/30 transition-colors">
          <CardHeader className="p-4 pb-2">
            <FileText className="h-6 w-6 text-indigo-400 mb-2" />
            <CardTitle className="text-lg">Analiza Umowy</CardTitle>
            <CardDescription>Załaduj PDF/DOCX do analizy na obecność ukrytych klauzul</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-2">
            <Button className="w-full bg-indigo-600 hover:bg-indigo-700 text-white">
              Wgraj Dokument
            </Button>
          </CardContent>
        </Card>

        <Card className="bg-card/40 border-border/50 hover:border-indigo-400/30 transition-colors">
          <CardHeader className="p-4 pb-2">
            <ShieldAlert className="h-6 w-6 text-indigo-400 mb-2" />
            <CardTitle className="text-lg">Kreator NDA</CardTitle>
            <CardDescription>Generowanie bezpiecznych umów o poufności z szablonów</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-2">
            <Button className="w-full bg-indigo-600 hover:bg-indigo-700 text-white">
              Stwórz NDA
            </Button>
          </CardContent>
        </Card>

        <Card className="bg-card/40 border-border/50 hover:border-indigo-400/30 transition-colors">
          <CardHeader className="p-4 pb-2">
            <Cpu className="h-6 w-6 text-indigo-400 mb-2" />
            <CardTitle className="text-lg">Smart Routing</CardTitle>
            <CardDescription>Aktywny model: Llama 3 70B (Vertex AI)</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-2 flex items-center justify-between">
            <span className="text-xs text-muted-foreground">Oczekujące zadania: 0</span>
            <Badge variant="outline" className="text-emerald-400 border-emerald-400/30">Online</Badge>
          </CardContent>
        </Card>
      </div>

      <div className="mt-8">
        <h3 className="font-mondwest text-xl mb-4 text-text-secondary tracking-widest">Ostatnie Analizy</h3>
        <div className="border border-dashed border-border/50 rounded-lg p-8 text-center text-muted-foreground">
          Historia analizowanych dokumentów pojawi się tutaj.
        </div>
      </div>
    </div>
  );
}
