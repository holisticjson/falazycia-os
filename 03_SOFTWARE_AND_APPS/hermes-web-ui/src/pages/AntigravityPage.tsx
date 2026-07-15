import { useLayoutEffect } from "react";
import { usePageHeader } from "@/contexts/usePageHeader";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Code2, Terminal, Database, Webhook, Zap, Fingerprint } from "lucide-react";

export default function AntigravityPage() {
  const { setAfterTitle, setTitle } = usePageHeader();

  useLayoutEffect(() => {
    setTitle("Antigravity Core");
    setAfterTitle(
      <Badge className="border border-primary/30 bg-primary/10 text-[10px] text-primary">
        BUILDER AGENT
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
        <h2 className="font-expanded text-2xl font-bold tracking-[0.04em] text-midground blend-lighter flex items-center gap-2">
          <Terminal className="h-6 w-6 text-primary" />
          Antigravity Workspace
        </h2>
        <p className="text-sm text-muted-foreground mt-1 max-w-3xl">
          Główny interfejs wykonawczy Agenta Budowniczego. Z tego poziomu (lub zdalnie przez Telegram)
          możesz zrzucić mi zadania kodowania, architektury i wdrażania zmian na serwerach, mając pełen dostęp
          do historii naszych konwersacji, załadowanych umiejętności (Skills) oraz kontekstu.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        {/* Sekcja: Zdalny Dostęp i Tożsamość */}
        <Card className="bg-card/40 border-border/50 hover:border-primary/30 transition-colors">
          <CardHeader className="p-4 pb-2">
            <Fingerprint className="h-6 w-6 text-primary mb-2" />
            <CardTitle className="text-lg">Tożsamość & Kontekst</CardTitle>
            <CardDescription>Aktywne sesje i permanentny dostęp</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-2 flex flex-col gap-3">
            <div className="flex items-center justify-between text-xs">
              <span className="text-muted-foreground">Konto Hermes:</span>
              <Badge variant="outline" className="text-emerald-400 border-emerald-400/30">Zalogowano (Admin)</Badge>
            </div>
            <div className="flex items-center justify-between text-xs">
              <span className="text-muted-foreground">Pamięć długa (Obsidian):</span>
              <Badge variant="outline" className="text-sky-400 border-sky-400/30">Zsynchronizowano</Badge>
            </div>
            <Button variant="outline" className="w-full text-xs mt-2 border-primary/20 hover:bg-primary/10">
              <Database className="mr-2 h-3 w-3" /> Przeglądaj Historię
            </Button>
          </CardContent>
        </Card>

        {/* Sekcja: Wykonawstwo i Skills */}
        <Card className="bg-card/40 border-border/50 hover:border-primary/30 transition-colors">
          <CardHeader className="p-4 pb-2">
            <Code2 className="h-6 w-6 text-primary mb-2" />
            <CardTitle className="text-lg">Aktywne Skille</CardTitle>
            <CardDescription>Narzędzia, do których Antigravity ma dostęp</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-2">
            <div className="flex flex-wrap gap-2">
              <Badge className="bg-primary/10 border-primary/20 text-[10px]">Terminal / Shell</Badge>
              <Badge className="bg-primary/10 border-primary/20 text-[10px]">Pliki lokalne (FS)</Badge>
              <Badge className="bg-primary/10 border-primary/20 text-[10px]">Git / GitHub</Badge>
              <Badge className="bg-primary/10 border-primary/20 text-[10px]">MCP Obsidian Vault</Badge>
              <Badge className="bg-primary/10 border-primary/20 text-[10px]">MCP Web Search</Badge>
            </div>
            <Button className="w-full bg-primary/20 hover:bg-primary/30 text-primary mt-4 border border-primary/30 text-xs">
              <Zap className="mr-2 h-3 w-3" /> Zarządzaj Skilami
            </Button>
          </CardContent>
        </Card>

        {/* Sekcja: Telegram Bot */}
        <Card className="bg-card/40 border-border/50 hover:border-primary/30 transition-colors">
          <CardHeader className="p-4 pb-2">
            <Webhook className="h-6 w-6 text-primary mb-2" />
            <CardTitle className="text-lg">Telegram Bridge</CardTitle>
            <CardDescription>Nasłuchiwanie poleceń z telefonu</CardDescription>
          </CardHeader>
          <CardContent className="p-4 pt-2 flex flex-col gap-3">
            <div className="flex items-center justify-between text-xs">
              <span className="text-muted-foreground">Orkiestrator Jason (Bot):</span>
              <Badge variant="outline" className="text-emerald-400 border-emerald-400/30">Aktywny</Badge>
            </div>
            <div className="flex items-center justify-between text-xs">
              <span className="text-muted-foreground">Kierowanie (Routing):</span>
              <Badge variant="outline" className="text-muted-foreground border-border/50">Jason ➔ Antigravity</Badge>
            </div>
            <div className="text-[10px] text-muted-foreground mt-2 border border-border/50 bg-background/50 p-2 rounded">
              Wiadomości na Telegramie oddelegowane do zadań technicznych trafiają bezpośrednio na tę tablicę.
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="mt-8 flex flex-col h-full min-h-[300px]">
        <h3 className="font-mondwest text-xl mb-4 text-text-secondary tracking-widest flex items-center gap-2">
          <Terminal className="h-4 w-4" /> Dziennik Operacyjny (Zdalny Terminal)
        </h3>
        <div className="flex-1 border border-border/50 bg-black/60 rounded-lg p-4 font-mono text-xs text-primary/80 overflow-y-auto">
          <div className="mb-2 text-muted-foreground"># Antigravity Remote Execution Runtime (A-RER) v2.0</div>
          <div className="mb-4 text-muted-foreground"># Logowanie z uprawnieniami administratora pomyślne. Telegram bot webhook podłączony.</div>
          <div><span className="text-emerald-400">system:</span> Oczekiwanie na polecenia ze zdalnego interfejsu lub Telegrama...</div>
        </div>
      </div>
    </div>
  );
}
