# 🔮 Uniwersalny Ekstraktor Wiedzy z Kursów (Wersja Wieloplatformowa)

Ten dokument zawiera instrukcję krok po kroku, jak wyciągnąć **100% wiedzy** z **DOWOLNEGO kursu wideo** (np. Adrian Kilar, Jan Szopa, Akademia Automatyzacji) w pełni automatycznie.

Zaimplementowałem **pełną uniwersalność**! Dashboard Streamlit pozwala teraz wybrać lub utworzyć dowolny folder docelowy w Twojej Bazie Wiedzy, a skrypt przeglądarki i dedykowane rozszerzenie wykrywają wszystkie rodzaje odtwarzaczy wideo!

---

## 🔌 KROK 1: Instalacja Rozszerzenia "Holistic Collector" (Polecane!)

Stworzyłem dla Ciebie **własne, dedykowane rozszerzenie do Chrome**. Pozwala ono na szybkie, wygodne i automatyczne skanowanie całego kursu bez otwierania konsoli deweloperskiej!

### Jak je załadować do Chrome w 30 sekund:
1. Otwórz przeglądarkę Google Chrome.
2. Wpisz w pasku adresu: `chrome://extensions/` i wciśnij **Enter**.
3. W prawym górnym rogu włącz **Tryb dewelopera (Developer mode)**.
4. Kliknij przycisk **Załaduj bez paczki (Load unpacked)** po lewej stronie.
5. Wybierz folder:
   📂 `c:\Aplikacje MVP\Holistic Jason\Holistic_Collector_Extension`
6. **Gotowe!** Rozszerzenie "Holistic Collector" pojawi się na Twojej liście. Przypnij je do paska za pomocą ikony puzzla 🧩.

---

## 📡 KROK 2: Skanowanie kursu za pomocą Rozszerzenia

1. Wejdź na **główną stronę zalogowanego kursu** (np. Jana Szopy na jego platformie lub Adriana Kilara).
2. Kliknij ikonkę **Holistic Collector** 🔮 na pasku przeglądarki.
3. Kliknij fioletowy przycisk: **`🚀 Rozpocznij Skanowanie Kursu`**.
4. W okienku konsoli rozszerzenia zobaczysz postęp na żywo. Po zakończeniu (status zmieni się na zielone "Ukończono!"):
   - Kliknij **`📥 Pobierz plik JSON`** (zapisze plik na dysku)
   - Lub **`📋 Skopiuj JSON do schowka`** (najwygodniejsze!).

*(Uwaga: Gdybyś kiedykolwiek wolał odpalić skan ręcznie bez instalowania rozszerzenia, kod konsolowy JS z KROKU 1.1 wciąż jest dostępny w zakładce "Głęboki Ekstraktor" w Dashboardzie!)*

---

## 📦 KROK 3: Import i Dynamiczne Zapisywanie w Dashboardzie

1. Otwórz swój Dashboard Streamlit i przejdź do zakładki **`Universal Course & Video Transcriber`**.
2. W **lewym panelu (Sidebar)** wybierz lub utwórz folder docelowy w Bazie Wiedzy:
   - Dla Kilara wybierz: **`Adrian Kilar Motion`**.
   - Dla Jana Szopy wybierz lub wpisz: **`Jan Szopa - Akademia Zdalnej Agencji Marketingowej`**.
3. Wejdź w zakładkę **`📦 3. Masowy Import (JSON/Tekst)`**.
4. Wklej skopiowany JSON ze schowka.
5. **Wybierz tryb działania (zobacz poniżej!)** i kliknij **`🚀 Rozpocznij masowy proces`**.

---

## 🔄 WYBÓR TRYBU DZIAŁANIA (JAK UZUPEŁNIĆ ISTNIEJĄCE NOTATKI?):

Dodałem do Twojego Dashboardu **rewolucyjny "Tryb Wzbogacania (Enrich Mode)"**. Pozwala on na uzdatnienie Twoich dotychczasowych notatek o pełne opisy z platformy, bez ponownej syntezy transkrypcji!

### Scenariusz A: Chcę WZBOGACIĆ moje zrobione notatki o pełne opisy (np. dla Adriana Kilara)
Jeśli masz już pliki MD na dysku, ale brakuje w nich szczegółowych promptów i kroków spod filmu:
1. Zeskanuj kurs nowym rozszerzeniem (wyciągnie pełne opisy).
2. Wklej JSON w Dashboardzie w zakładce Masowy Import.
3. Zaznacz checkbox: **`🔄 Tryb Wzbogacania (Enrich Mode)`** (jest domyślnie włączony).
4. Kliknij **`Rozpocznij masowy proces`**.
   - *Jak to działa?* System otworzy plik MD na Twoim dysku, odczyta istniejącą transkrypcję wideo, połączy ją z nowym pełnym opisem z platformy i za pomocą Gemini wygeneruje nową, ultrahaczącą wersję, nadpisując plik. Nie traci żadnych informacji z wideo!

### Scenariusz B: Chcę dodać NOWY kurs od zera (np. Jan Szopa)
Jeśli nie masz jeszcze żadnych notatek na dysku dla tego kursu:
1. Zeskanuj kurs rozszerzeniem.
2. Wskaż nowy folder docelowy w Sidebarze Dashboardu.
3. Wklej JSON w Masowym Imporcie.
4. Pozostaw zaznaczony **`Tryb Wzbogacania`** (zadziała automatycznie jak czysty generator, bo nie znajdzie plików na dysku, i wygeneruje je od zera!).
5. Kliknij **`Rozpocznij masowy proces`**.
