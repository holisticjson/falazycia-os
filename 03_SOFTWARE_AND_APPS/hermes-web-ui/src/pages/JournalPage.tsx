import { useLayoutEffect } from "react";
import { usePageHeader } from "@/contexts/usePageHeader";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Sparkles, Trophy, Target, Flame, Activity } from "lucide-react";

const COMPLETED_TASKS = [
  { id: 1, title: "Wysłano maile z ofertą off-market", dopamine: 25, time: "10:30" },
  { id: 2, title: "Opublikowano nowy wpis na bloga", dopamine: 40, time: "12:15" },
  { id: 3, title: "Zsynchronizowano faktury KSeF", dopamine: 15, time: "14:00" },
  { id: 4, title: "Podpięto Kanban pod backend", dopamine: 50, time: "Wczoraj" },
];

export default function JournalPage() {
  const { setAfterTitle, setTitle } = usePageHeader();

  useLayoutEffect(() => {
    setTitle("Dopamine Journal");
    setAfterTitle(
      <Badge className="border border-yellow-400/30 bg-yellow-400/10 text-[10px] text-yellow-400">
        MOTYWACJA
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
          <Sparkles className="h-6 w-6 text-yellow-400" />
          Dziennik Dopaminowy
        </h2>
        <p className="text-sm text-muted-foreground mt-1 max-w-3xl">
          Wizualizacja Twoich osiągnięć. Gamifikacja codziennych zadań pomaga utrzymać motywację przy ADHD.
          Wykonuj mikro-kroki na tablicy Kanban, by zbierać punkty dopaminy.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-4">
        {/* Statystyki */}
        <Card className="bg-card/40 border-border/50">
          <CardHeader className="p-4 pb-2">
            <Trophy className="h-6 w-6 text-yellow-400 mb-2" />
            <CardTitle className="text-lg">Punkty Dopaminy</CardTitle>
          </CardHeader>
          <CardContent className="p-4 pt-2">
            <div className="text-4xl font-bold text-yellow-400">130</div>
            <p className="text-xs text-muted-foreground mt-1">Zebrane w tym tygodniu</p>
          </CardContent>
        </Card>

        <Card className="bg-card/40 border-border/50">
          <CardHeader className="p-4 pb-2">
            <Flame className="h-6 w-6 text-orange-400 mb-2" />
            <CardTitle className="text-lg">Streak (Passa)</CardTitle>
          </CardHeader>
          <CardContent className="p-4 pt-2">
            <div className="text-4xl font-bold text-orange-400">4 Dni</div>
            <p className="text-xs text-muted-foreground mt-1">Utrzymuj rutynę pracy</p>
          </CardContent>
        </Card>

        <Card className="bg-card/40 border-border/50">
          <CardHeader className="p-4 pb-2">
            <Target className="h-6 w-6 text-sky-400 mb-2" />
            <CardTitle className="text-lg">Zrobione Dzisiaj</CardTitle>
          </CardHeader>
          <CardContent className="p-4 pt-2">
            <div className="text-4xl font-bold text-sky-400">3</div>
            <p className="text-xs text-muted-foreground mt-1">Ukończone nano-taski</p>
          </CardContent>
        </Card>

        <Card className="bg-card/40 border-border/50">
          <CardHeader className="p-4 pb-2">
            <Activity className="h-6 w-6 text-emerald-400 mb-2" />
            <CardTitle className="text-lg">Status Agencji</CardTitle>
          </CardHeader>
          <CardContent className="p-4 pt-2">
            <div className="text-2xl font-bold text-emerald-400">Zdrowa</div>
            <p className="text-xs text-muted-foreground mt-1">Praca zespołowa (Swarm)</p>
          </CardContent>
        </Card>
      </div>

      <div className="mt-8">
        <h3 className="font-mondwest text-xl mb-4 text-text-secondary tracking-widest">Historia Sukcesów</h3>
        <div className="flex flex-col gap-3">
          {COMPLETED_TASKS.map(task => (
            <Card key={task.id} className="bg-card/40 border-border/50 flex flex-row items-center justify-between p-4">
              <div className="flex items-center gap-3">
                <Badge className="bg-yellow-400/10 border-yellow-400/20 text-yellow-400 tabular-nums min-w-[3rem] justify-center">
                  +{task.dopamine}
                </Badge>
                <span className="text-sm font-medium">{task.title}</span>
              </div>
              <span className="text-xs text-muted-foreground">{task.time}</span>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
