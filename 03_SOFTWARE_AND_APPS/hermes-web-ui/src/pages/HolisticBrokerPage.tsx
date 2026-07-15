import { useLayoutEffect } from "react";
import { usePageHeader } from "@/contexts/usePageHeader";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Building2, Home, Search, Target } from "lucide-react";

export default function HolisticBrokerPage() {
  const { setAfterTitle, setTitle } = usePageHeader();

  useLayoutEffect(() => {
    setTitle("Holistic Broker");
    setAfterTitle(
      <Badge className="border border-amber-400/30 bg-amber-400/10 text-[10px] text-amber-400">
        AI REAL ESTATE
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
          Oddział Nieruchomości
        </h2>
        <p className="text-sm text-muted-foreground mt-1 max-w-2xl">
          Niezależny system wspierający markę holistycznybroker.pl. Skupia się na analizie off-market, 
          generowaniu ofert dla deweloperów oraz inteligentnym matchowaniu inwestorów z nieruchomościami.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card className="bg-card/40 border-border/50 hover:border-amber-400/30 transition-colors">
          <CardHeader className="p-4 pb-2">
            <Search className="h-6 w-6 text-amber-400 mb-2" />
            <CardTitle className="text-lg">Skaner Off-Market</CardTitle>
            <CardDescription>Analiza rynku w poszukiwaniu okazji inwestycyjnych (Flip/Wynajem)</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-2">
            <Button className="w-full bg-amber-600 hover:bg-amber-700 text-white">
              Skanuj Rynek
            </Button>
          </CardContent>
        </Card>

        <Card className="bg-card/40 border-border/50 hover:border-amber-400/30 transition-colors">
          <CardHeader className="p-4 pb-2">
            <Building2 className="h-6 w-6 text-amber-400 mb-2" />
            <CardTitle className="text-lg">Oferty Deweloperskie</CardTitle>
            <CardDescription>Generowanie spersonalizowanych pakietów (Hormozi methodology)</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-2">
            <Button className="w-full bg-amber-600 hover:bg-amber-700 text-white">
              Kreator Ofert
            </Button>
          </CardContent>
        </Card>

        <Card className="bg-card/40 border-border/50 hover:border-amber-400/30 transition-colors">
          <CardHeader className="p-4 pb-2">
            <Target className="h-6 w-6 text-amber-400 mb-2" />
            <CardTitle className="text-lg">Baza Inwestorów</CardTitle>
            <CardDescription>CRM dla klientów premium i inteligentny match-making</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-2">
            <Button className="w-full bg-amber-600 hover:bg-amber-700 text-white">
              Otwórz CRM
            </Button>
          </CardContent>
        </Card>
      </div>

      <div className="mt-8">
        <h3 className="font-mondwest text-xl mb-4 text-text-secondary tracking-widest">Ostatnie Transakcje / Leady</h3>
        <div className="border border-dashed border-border/50 rounded-lg p-8 text-center text-muted-foreground">
          Brak danych. Trwa synchronizacja z backendem Hermes.
        </div>
      </div>
    </div>
  );
}
