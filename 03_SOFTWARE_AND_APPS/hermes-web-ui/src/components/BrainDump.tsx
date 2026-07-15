import { useState } from "react";
import { Skull, X, Paperclip, Send, Link, FileText, Image as ImageIcon } from "lucide-react";
import { Button } from "@/components/ui/button";

export function BrainDump() {
  const [isOpen, setIsOpen] = useState(false);
  const [content, setContent] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async () => {
    if (!content.trim()) return;
    setIsSubmitting(true);
    
    try {
      const response = await fetch("http://127.0.0.1:8085/api/dump", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ content: content, tags: ["ui-zrzut"] }),
      });

      if (!response.ok) {
        throw new Error("Błąd podczas zapisywania zrzutu.");
      }

      setContent("");
      setIsOpen(false);
    } catch (error) {
      console.error("Błąd zapisu do Obsidiana:", error);
      alert("Nie udało się połączyć z API zapisu (Upewnij się, że brain_dump_api.py jest uruchomiony na porcie 8085).");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <>
      {/* Pływający Przycisk */}
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 z-40 flex h-14 w-14 items-center justify-center rounded-full bg-violet-600 text-white shadow-[0_0_20px_-5px_rgba(139,92,246,0.5)] transition-transform hover:scale-110 hover:bg-violet-500 focus:outline-none"
        aria-label="Brain Dump"
        title="Szybki Zrzut Myśli"
      >
        <Skull className="h-6 w-6" />
      </button>

      {/* Modal / Overlay */}
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4">
          <div 
            className="w-full max-w-lg overflow-hidden rounded-xl border border-violet-500/30 bg-background/95 shadow-[0_0_50px_-15px_rgba(139,92,246,0.3)] animate-in fade-in zoom-in-95 duration-200"
          >
            {/* Nagłówek Modal */}
            <div className="flex items-center justify-between border-b border-border/50 bg-violet-500/10 px-4 py-3">
              <div className="flex items-center gap-2">
                <Skull className="h-5 w-5 text-violet-400" />
                <h3 className="font-expanded text-lg font-bold tracking-widest text-violet-100">
                  BRAIN DUMP
                </h3>
              </div>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setIsOpen(false)}
                className="h-8 w-8 text-muted-foreground hover:text-white"
              >
                <X className="h-4 w-4" />
              </Button>
            </div>

            {/* Obszar roboczy */}
            <div className="p-4 flex flex-col gap-4">
              <p className="text-xs text-muted-foreground">
                Zrzucaj luźne pomysły, linki do YT, PDFy, screeny czy inspiracje reklamowe. Wirtualny Zarząd przetworzy je później na Nano-Taski lub wiedzę w Obsidianie.
              </p>
              
              <textarea
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Co Ci chodzi po głowie? Wklej tekst lub link..."
                className="min-h-[120px] w-full resize-none rounded-lg border border-border/50 bg-black/50 p-3 text-sm text-foreground focus:border-violet-500/50 focus:outline-none focus:ring-1 focus:ring-violet-500/50"
                autoFocus
              />

              {/* Akcje / Załączniki */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-1">
                  <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-violet-300" title="Dodaj PDF/Dokument">
                    <FileText className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-violet-300" title="Dodaj Zrzut Ekranu">
                    <ImageIcon className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-violet-300" title="Dodaj Link">
                    <Link className="h-4 w-4" />
                  </Button>
                  <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-violet-300" title="Dodaj Inny Plik">
                    <Paperclip className="h-4 w-4" />
                  </Button>
                </div>
                
                <Button 
                  onClick={handleSubmit} 
                  disabled={!content.trim() || isSubmitting}
                  className="bg-violet-600 hover:bg-violet-500 text-white"
                >
                  {isSubmitting ? (
                    <span className="animate-pulse">Zrzucanie...</span>
                  ) : (
                    <>
                      <Send className="mr-2 h-4 w-4" /> Zrzut do Bazy
                    </>
                  )}
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
