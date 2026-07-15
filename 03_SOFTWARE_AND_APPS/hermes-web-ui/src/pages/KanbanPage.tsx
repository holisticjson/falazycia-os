import { useEffect, useLayoutEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { usePageHeader } from "@/contexts/usePageHeader";
import { api, SessionInfo } from "@/lib/api";
import { BrainCircuit, CheckCircle2, CircleDot, Clock, Zap } from "lucide-react";
import { cn } from "@/lib/utils";

// Mock nano-tasks derived from SOPs
interface NanoTask {
  id: string;
  title: string;
  description: string;
  agent: string;
  status: "todo" | "in-progress" | "done";
  reward: number;
}

const MOCK_TASKS: NanoTask[] = [
  {
    id: "task-1",
    title: "Rozbij projekt na mikro-kroki",
    description: "Analiza procedury SOP Dyrektora Marketingu.",
    agent: "Planner-01",
    status: "todo",
    reward: 10,
  },
  {
    id: "task-2",
    title: "Wygeneruj grafiki do posta (Imagen 3)",
    description: "Uruchom generator obrazów na podstawie promptu wizualnego.",
    agent: "Dyrektor Kreatywny",
    status: "todo",
    reward: 15,
  },
];

export default function KanbanPage() {
  const { setAfterTitle, setTitle } = usePageHeader();
  const [activeSessions, setActiveSessions] = useState<SessionInfo[]>([]);
  const [loading, setLoading] = useState(true);

  useLayoutEffect(() => {
    setTitle("ADHD Kanban");
    setAfterTitle(
      <Badge className="border border-warning/30 bg-warning/10 text-[10px] text-warning">
        NANO-TASKS
      </Badge>
    );
    return () => {
      setTitle(null);
      setAfterTitle(null);
    };
  }, [setAfterTitle, setTitle]);

  useEffect(() => {
    // Fetch real sessions to populate "In Progress" with active agent thoughts
    api
      .getSessions(20)
      .then((res) => {
        setActiveSessions(res.sessions.filter((s) => s.is_active));
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const todoTasks = MOCK_TASKS.filter((t) => t.status === "todo");
  // Map active sessions to "In Progress" tasks
  const inProgressTasks: NanoTask[] = activeSessions.map((s) => ({
    id: s.id,
    title: s.title || "Agent wykonuje zadanie...",
    description: s.preview || "Przetwarzanie danych",
    agent: (s.model || "Hermes Agent").split("/").pop() || "Agent",
    status: "in-progress",
    reward: 25,
  }));

  const doneTasks = MOCK_TASKS.filter((t) => t.status === "done");

  return (
    <div className="flex h-full min-h-0 flex-col gap-5 p-4">
      <div className="mb-2">
        <h2 className="font-expanded text-2xl font-bold tracking-[0.04em] text-midground blend-lighter">
          Proceduralizacja zadań
        </h2>
        <p className="text-sm text-muted-foreground mt-1">
          Złożone procedury (SOP z Obsidiana) przeżute na mikro-kroki, by omijać paraliż zadaniowy.
        </p>
      </div>

      <div className="grid h-full grid-cols-1 gap-6 md:grid-cols-3">
        {/* TODO COLUMN */}
        <div className="flex flex-col gap-3">
          <div className="flex items-center justify-between border-b border-border pb-2">
            <h3 className="font-mondwest text-lg uppercase text-text-secondary tracking-widest flex items-center gap-2">
              <CircleDot className="h-4 w-4 text-sky-400" /> Do zrobienia
            </h3>
            <Badge variant="outline" className="text-xs">
              {todoTasks.length}
            </Badge>
          </div>
          <div className="flex flex-col gap-3 overflow-y-auto pr-2 pb-10">
            {todoTasks.map((task) => (
              <Card key={task.id} className="bg-card/40 border-border/50 hover:border-sky-400/30 transition-colors">
                <CardHeader className="p-4 pb-2">
                  <div className="flex justify-between items-start">
                    <Badge className="bg-sky-400/10 text-sky-300 border-sky-400/20 text-[10px]">
                      {task.agent}
                    </Badge>
                    <span className="flex items-center text-[10px] text-warning/80 font-mono">
                      +{task.reward} dopamine
                    </span>
                  </div>
                  <CardTitle className="text-sm mt-2 leading-tight">{task.title}</CardTitle>
                </CardHeader>
                <CardContent className="p-4 pt-1 text-xs text-muted-foreground">
                  {task.description}
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* IN PROGRESS COLUMN */}
        <div className="flex flex-col gap-3">
          <div className="flex items-center justify-between border-b border-border pb-2">
            <h3 className="font-mondwest text-lg uppercase text-text-secondary tracking-widest flex items-center gap-2">
              <Zap className="h-4 w-4 text-warning" /> W trakcie
            </h3>
            <Badge variant="outline" className="text-xs">
              {inProgressTasks.length}
            </Badge>
          </div>
          <div className="flex flex-col gap-3 overflow-y-auto pr-2 pb-10">
            {loading ? (
              <div className="text-xs text-muted-foreground text-center py-4 flex items-center justify-center gap-2">
                <Clock className="h-4 w-4 animate-spin" /> Ładowanie eventów...
              </div>
            ) : inProgressTasks.length === 0 ? (
              <div className="text-xs text-muted-foreground text-center py-4 border border-dashed border-border/50 rounded-lg">
                Agenci w stanie spoczynku
              </div>
            ) : (
              inProgressTasks.map((task) => (
                <Card key={task.id} className="bg-warning/5 border-warning/30 shadow-[0_0_15px_-5px_rgba(255,189,56,0.2)]">
                  <span className="pointer-events-none absolute left-0 top-0 bottom-0 w-1 bg-warning/50 rounded-l-md" />
                  <CardHeader className="p-4 pb-2">
                    <div className="flex justify-between items-start">
                      <Badge className="bg-warning/20 text-warning border-warning/30 text-[10px] animate-pulse">
                        <BrainCircuit className="h-3 w-3 mr-1 inline-block" />
                        {task.agent}
                      </Badge>
                      <span className="flex items-center text-[10px] text-warning/80 font-mono">
                        +{task.reward} dopamine
                      </span>
                    </div>
                    <CardTitle className="text-sm mt-2 leading-tight text-midground">{task.title}</CardTitle>
                  </CardHeader>
                  <CardContent className="p-4 pt-1 text-xs text-muted-foreground">
                    {task.description}
                  </CardContent>
                </Card>
              ))
            )}
          </div>
        </div>

        {/* DONE COLUMN */}
        <div className="flex flex-col gap-3">
          <div className="flex items-center justify-between border-b border-border pb-2">
            <h3 className="font-mondwest text-lg uppercase text-text-secondary tracking-widest flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-emerald-400" /> Zrobione
            </h3>
            <Badge variant="outline" className="text-xs">
              {doneTasks.length}
            </Badge>
          </div>
          <div className="flex flex-col gap-3 overflow-y-auto pr-2 pb-10">
            {doneTasks.length === 0 ? (
              <div className="text-xs text-muted-foreground text-center py-4 border border-dashed border-border/50 rounded-lg">
                Brak ukończonych mikro-kroków
              </div>
            ) : (
              doneTasks.map((task) => (
                <Card key={task.id} className="bg-emerald-900/10 border-emerald-500/20 opacity-70">
                  <CardHeader className="p-4 pb-2">
                    <div className="flex justify-between items-start">
                      <Badge className="bg-emerald-500/10 text-emerald-300 border-emerald-500/20 text-[10px] line-through">
                        {task.agent}
                      </Badge>
                    </div>
                    <CardTitle className="text-sm mt-2 leading-tight line-through text-muted-foreground">
                      {task.title}
                    </CardTitle>
                  </CardHeader>
                </Card>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
