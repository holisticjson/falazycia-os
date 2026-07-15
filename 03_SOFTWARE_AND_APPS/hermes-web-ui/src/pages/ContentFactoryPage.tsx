import { useLayoutEffect } from "react";
import { usePageHeader } from "@/contexts/usePageHeader";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Video, Image as ImageIcon, PenTool, Sparkles } from "lucide-react";

export default function ContentFactoryPage() {
  const { setAfterTitle, setTitle } = usePageHeader();

  useLayoutEffect(() => {
    setTitle("Fabryka Treści");
    setAfterTitle(
      <Badge className="border border-fuchsia-400/30 bg-fuchsia-400/10 text-[10px] text-fuchsia-400">
        MARKETING & WIDEO
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
          Zautomatyzowane Centrum Kreacji
        </h2>
        <p className="text-sm text-muted-foreground mt-1 max-w-2xl">
          Dyrektorzy Marketingu i Copywriterzy pracują tu na pełnych obrotach.
          Generuj viralowe hooki, twórz posty i produkuj multimedia z użyciem modeli klasy SOTA (Imagen 3, Veo 3.1).
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {/* Generowanie Wideo */}
        <Card className="bg-card/40 border-border/50 hover:border-fuchsia-400/30 transition-colors">
          <CardHeader className="p-4 pb-2">
            <Video className="h-6 w-6 text-fuchsia-400 mb-2" />
            <CardTitle className="text-lg">Veo 3.1 Studio</CardTitle>
            <CardDescription>Generowanie wideo do rolek i TikToków</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-2">
            <Button className="w-full bg-fuchsia-600 hover:bg-fuchsia-700 text-white">
              <Sparkles className="mr-2 h-4 w-4" /> Nowy Projekt Wideo
            </Button>
          </CardContent>
        </Card>

        {/* Generowanie Grafik */}
        <Card className="bg-card/40 border-border/50 hover:border-sky-400/30 transition-colors">
          <CardHeader className="p-4 pb-2">
            <ImageIcon className="h-6 w-6 text-sky-400 mb-2" />
            <CardTitle className="text-lg">Imagen 3 Studio</CardTitle>
            <CardDescription>Fotorealistyczne grafiki i miniatury</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-2">
            <Button className="w-full bg-sky-600 hover:bg-sky-700 text-white">
              <Sparkles className="mr-2 h-4 w-4" /> Wygeneruj Obraz
            </Button>
          </CardContent>
        </Card>

        {/* Copywriting */}
        <Card className="bg-card/40 border-border/50 hover:border-emerald-400/30 transition-colors">
          <CardHeader className="p-4 pb-2">
            <PenTool className="h-6 w-6 text-emerald-400 mb-2" />
            <CardTitle className="text-lg">Kreator Hooków</CardTitle>
            <CardDescription>Zoptymalizowane skrypty i copy (SOP)</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-2">
            <Button className="w-full bg-emerald-600 hover:bg-emerald-700 text-white">
              <Sparkles className="mr-2 h-4 w-4" /> Napisz Posta
            </Button>
          </CardContent>
        </Card>
      </div>

      <div className="mt-8">
        <h3 className="font-mondwest text-xl mb-4 text-text-secondary tracking-widest">Aktywne Zlecenia (Kanban)</h3>
        <div className="border border-dashed border-border/50 rounded-lg p-8 text-center text-muted-foreground">
          Podpięcie kolejki renderowania i zadań copywriterskich pojawi się tutaj po integracji z backendem.
        </div>
      </div>
    </div>
  );
}
