import tkinter as tk
import time
from tkinter import messagebox
import winsound

# Nasz Harmonogram Dnia (w minutach)
SCHEDULE = [
    {"name": "Poranny Rytuał (Wim Hof / Rozciąganie)", "duration": 60},
    {"name": "Telefony: Art Master + CKD (42 675 74 64)", "duration": 15},
    {"name": "Bar Jaś: Canva + Strzałka + Druk", "duration": 60},
    {"name": "Umiejętności Jutra: Skrypt YT", "duration": 60},
    {"name": "GHL: Jasny Motyw + Czcionki", "duration": 60},
    {"name": "Przerwa i odpoczynek (Oczy!)", "duration": 15},
    {"name": "GHL: Copywriting wg Jana Szopy", "duration": 45},
    {"name": "Holistic CEO: Logi z GCP i Deploy", "duration": 60},
    {"name": "Przerwa Obiadowa / Wyjazd", "duration": 60},
    {"name": "Wizyta w CKD: Dentysta (14:00)", "duration": 120},
    {"name": "Koniec na teraz!", "duration": 0}
]

class ADHDTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Holistic System Timer")
        self.root.geometry("350x130")
        
        # Kluczowe: Zawsze na wierzchu!
        self.root.attributes('-topmost', True) 
        self.root.configure(bg="#0B1F33") # Deep Navy (Z Brand Guidelines)
        
        self.current_idx = 0
        self.time_left = SCHEDULE[self.current_idx]["duration"] * 60
        self.running = False
        
        self.task_label = tk.Label(root, text=SCHEDULE[self.current_idx]["name"], font=("Segoe UI", 12, "bold"), fg="#4A90E2", bg="#0B1F33")
        self.task_label.pack(pady=10)
        
        self.time_label = tk.Label(root, text=self.format_time(self.time_left), font=("Segoe UI", 26, "bold"), fg="white", bg="#0B1F33")
        self.time_label.pack()
        
        self.btn_frame = tk.Frame(root, bg="#0B1F33")
        self.btn_frame.pack(pady=5)
        
        self.start_btn = tk.Button(self.btn_frame, text="Start / Pauza", command=self.toggle, bg="#D4AF37", fg="black", font=("Segoe UI", 9, "bold"), relief="flat")
        self.start_btn.pack(side="left", padx=5)
        
        self.next_btn = tk.Button(self.btn_frame, text="Pomiń / Następny", command=self.next_task, bg="#4A90E2", fg="white", font=("Segoe UI", 9, "bold"), relief="flat")
        self.next_btn.pack(side="left", padx=5)
        
        self.update_clock()

    def format_time(self, seconds):
        m, s = divmod(seconds, 60)
        return f"{m:02d}:{s:02d}"
        
    def toggle(self):
        self.running = not self.running
        if self.running:
            self.start_btn.config(text="Pauza", bg="#E63946", fg="white")
        else:
            self.start_btn.config(text="Start", bg="#D4AF37", fg="black")
        
    def next_task(self):
        if self.current_idx < len(SCHEDULE) - 1:
            self.current_idx += 1
            self.time_left = SCHEDULE[self.current_idx]["duration"] * 60
            self.task_label.config(text=SCHEDULE[self.current_idx]["name"])
            self.time_label.config(text=self.format_time(self.time_left))
            self.running = False # Zatrzymuje zegar po zmianie, czekajac na start usera
            self.start_btn.config(text="Start", bg="#D4AF37", fg="black")
            
            # Tryb Przerwy - Zmiana kolorow na ostrzegawczy
            if "Przerwa" in SCHEDULE[self.current_idx]["name"]:
                self.root.configure(bg="#E63946") # Czerwony
                self.task_label.config(bg="#E63946", fg="white")
                self.time_label.config(bg="#E63946", fg="white")
                self.btn_frame.config(bg="#E63946")
                winsound.Beep(1000, 500)
                messagebox.showinfo("Czas na przerwę!", f"Zostaw kod i zacznij: {SCHEDULE[self.current_idx]['name']}")
            # Tryb Pracy - Zmiana kolorow z powrotem
            else:
                self.root.configure(bg="#0B1F33")
                self.task_label.config(bg="#0B1F33", fg="#4A90E2")
                self.time_label.config(bg="#0B1F33", fg="white")
                self.btn_frame.config(bg="#0B1F33")
                winsound.Beep(800, 500)
                messagebox.showinfo("Wracamy do pracy", f"Zaczynamy: {SCHEDULE[self.current_idx]['name']}")
                
    def update_clock(self):
        if self.running and self.time_left > 0:
            self.time_left -= 1
            self.time_label.config(text=self.format_time(self.time_left))
            
            # Przypomnienie na 5 minut przed koncem glownego bloku pracy
            if self.time_left == 5 * 60 and SCHEDULE[self.current_idx]["duration"] > 5:
                winsound.Beep(1200, 300)
                winsound.Beep(1200, 300)
                # Uzywamy root.attributes zeby wymusic na wierzch
                self.root.attributes('-topmost', True)
                messagebox.showwarning("5 Minut", "Uwaga! Zostało 5 minut do końca obecnego bloku. Domknij myśl.")
                
        elif self.running and self.time_left == 0:
            self.running = False
            self.next_task()
            
        self.root.after(1000, self.update_clock)

if __name__ == "__main__":
    root = tk.Tk()
    app = ADHDTimer(root)
    root.mainloop()
