import { useLayoutEffect, useState, useEffect } from "react";
import { usePageHeader } from "@/contexts/usePageHeader";
import { Button } from "@/components/ui/button";
import { Moon, Play, Square, Pause, Wind } from "lucide-react";

export default function ZenPage() {
  const { setAfterTitle, setTitle } = usePageHeader();
  const [timeLeft, setTimeLeft] = useState(25 * 60); // 25 minut (Pomodoro)
  const [isActive, setIsActive] = useState(false);
  const [task, setTask] = useState("");

  useLayoutEffect(() => {
    setTitle("SOS Sanctuary");
    setAfterTitle(null);
    return () => {
      setTitle(null);
    };
  }, [setAfterTitle, setTitle]);

  useEffect(() => {
    let interval: ReturnType<typeof setInterval> | null = null;
    if (isActive && timeLeft > 0) {
      interval = setInterval(() => {
        setTimeLeft((time) => time - 1);
      }, 1000);
    } else if (timeLeft === 0) {
      setIsActive(false);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isActive, timeLeft]);

  const toggleTimer = () => setIsActive(!isActive);
  const resetTimer = () => {
    setIsActive(false);
    setTimeLeft(25 * 60);
  };

  const minutes = Math.floor(timeLeft / 60).toString().padStart(2, "0");
  const seconds = (timeLeft % 60).toString().padStart(2, "0");

  return (
    <div className="flex h-full flex-col items-center justify-center p-4 bg-background transition-colors duration-1000 relative overflow-hidden">
      {/* Tło przypominające oddychanie w Zen Mode */}
      <div className={`absolute inset-0 bg-gradient-to-b from-indigo-900/10 to-background z-0 transition-opacity duration-[4000ms] ${isActive ? 'opacity-100' : 'opacity-20'}`} />
      
      <div className="z-10 flex flex-col items-center w-full max-w-md gap-8 text-center">
        <Wind className="h-12 w-12 text-indigo-400 mb-2 opacity-50" />
        
        <div>
          <h2 className="font-expanded text-3xl font-bold tracking-widest text-midground blend-lighter">
            Tryb Skupienia
          </h2>
          <p className="text-sm text-muted-foreground mt-2">
            Zignoruj szum. Skup się tylko na jednym zadaniu naraz.
          </p>
        </div>

        <input
          type="text"
          placeholder="Wpisz jedno główne zadanie na teraz..."
          value={task}
          onChange={(e) => setTask(e.target.value)}
          className="w-full bg-transparent border-b-2 border-indigo-400/30 text-center text-xl p-2 outline-none focus:border-indigo-400 transition-colors placeholder:text-muted-foreground/30 text-foreground"
        />

        <div className="text-8xl font-mono tabular-nums tracking-tight text-indigo-100/90 font-light drop-shadow-2xl">
          {minutes}:{seconds}
        </div>

        <div className="flex items-center gap-4">
          <Button
            onClick={toggleTimer}
            className="h-16 w-32 rounded-full text-lg bg-indigo-600 hover:bg-indigo-700 text-white"
          >
            {isActive ? (
              <><Pause className="mr-2 h-5 w-5" /> Pauza</>
            ) : (
              <><Play className="mr-2 h-5 w-5 fill-current" /> Start</>
            )}
          </Button>
          <Button
            onClick={resetTimer}
            variant="outline"
            className="h-16 w-16 rounded-full border-indigo-500/30 text-indigo-300 hover:bg-indigo-900/20 p-0"
          >
            <Square className="h-5 w-5" />
          </Button>
        </div>
      </div>
      
      <div className="absolute bottom-8 text-xs text-muted-foreground/50 z-10 flex items-center gap-2">
        <Moon className="h-3 w-3" /> Zablokowano wszystkie powiadomienia innych Agentów
      </div>
    </div>
  );
}
