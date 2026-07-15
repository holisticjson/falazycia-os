import { useLayoutEffect } from "react";
import { usePageHeader } from "@/contexts/usePageHeader";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Receipt, Wallet, FileSpreadsheet, Send } from "lucide-react";

export default function FinancePage() {
  const { setAfterTitle, setTitle } = usePageHeader();

  useLayoutEffect(() => {
    setTitle("Wydział Finansowy");
    setAfterTitle(
      <Badge className="border border-emerald-400/30 bg-emerald-400/10 text-[10px] text-emerald-400">
        FAKTUROWNIA & KSeF
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
          Moduł Finansów i Automatyzacji
        </h2>
        <p className="text-sm text-muted-foreground mt-1 max-w-2xl">
          Integracja z API Fakturowni oraz pełna zgodność z KSeF. Asystent CFO analizuje koszty stałe i przypomina o płatnościach.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {/* KSeF Dashboard */}
        <Card className="bg-card/40 border-border/50 hover:border-emerald-400/30 transition-colors">
          <CardHeader className="p-4 pb-2">
            <Receipt className="h-6 w-6 text-emerald-400 mb-2" />
            <CardTitle className="text-lg">Faktury KSeF</CardTitle>
            <CardDescription>Pobieranie faktur kosztowych i eksport do księgowości</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-2">
            <Button className="w-full bg-emerald-600 hover:bg-emerald-700 text-white">
              Synchronizuj z KSeF
            </Button>
          </CardContent>
        </Card>

        {/* Fakturownia */}
        <Card className="bg-card/40 border-border/50 hover:border-emerald-400/30 transition-colors">
          <CardHeader className="p-4 pb-2">
            <FileSpreadsheet className="h-6 w-6 text-emerald-400 mb-2" />
            <CardTitle className="text-lg">Fakturownia</CardTitle>
            <CardDescription>Wystawianie faktur dla klientów B2B</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-2">
            <Button className="w-full bg-emerald-600 hover:bg-emerald-700 text-white">
              <Send className="mr-2 h-4 w-4" /> Wystaw Fakturę
            </Button>
          </CardContent>
        </Card>

        {/* Koszty stałe */}
        <Card className="bg-card/40 border-border/50 hover:border-emerald-400/30 transition-colors">
          <CardHeader className="p-4 pb-2">
            <Wallet className="h-6 w-6 text-emerald-400 mb-2" />
            <CardTitle className="text-lg">Koszty Operacyjne</CardTitle>
            <CardDescription>Śledzenie subskrypcji AI i infrastruktury (GCP, API)</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-2">
            <Button variant="outline" className="w-full border-emerald-500/30 text-emerald-400 hover:bg-emerald-900/20">
              Analizuj Koszty
            </Button>
          </CardContent>
        </Card>
      </div>

      <div className="mt-8">
        <h3 className="font-mondwest text-xl mb-4 text-text-secondary tracking-widest">Powiadomienia Finansowe (CFO Agent)</h3>
        <div className="border border-dashed border-border/50 rounded-lg p-8 text-center text-muted-foreground">
          Podsumowanie miesięczne oraz alerty o nadchodzących płatnościach ZUS/VAT pojawią się tutaj.
        </div>
      </div>
    </div>
  );
}
