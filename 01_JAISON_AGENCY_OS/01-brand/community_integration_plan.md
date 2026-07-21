# 🧠 ADHD4Life Community Integration Plan

> **Data**: 28 maja 2026 | **Status**: Sprint Nocny (Fase Deployment)

---

## I. WIZJA OGÓLNA

Społeczność **ADHD4Life** to ekosystem osób neuroróżnorodnych (ADHD, ASD, disleksja, itd.), którzy walczą z „chaosem poznawczym" i szukają systemów, które rzeczywiście funkcjonują. Nasz dashboard Streamlit (`os.holisticjson.pl`) stanie się **centralnym hubu** dla:

1. **Community Digest** – cotygodniowe streszczania z kanałów (Discord, Telegram, Slack)
2. **Resource Library** – biblioteka ADHD-friendly (kursy, archiwa, prompty, narzędzia)
3. **Onboarding Bota** – asystent powitający nowych członków + quiz kwalifikacyjny

---

## II. ARCHITEKTURA INTEGRACJI

### A. DATA FLOW (Przepływ Danych)

```
Kanały Społeczności (Discord/Telegram/Slack)
    ↓
[Hermes Agent] – bot zbierający wiadomości
    ↓
Local Database (~/.hermes/community/) – przechowywanie Raw Messages
    ↓
LLM Pipeline (Summarization + Tagging)
    ↓
Streamlit Dashboard (Rendered Community Hub)
    ↓
✅ Community Digest (dostępny dla wszystkich)
```

### B. Moduły Dashboardu (Nowe)

#### **Moduł 1: Community Digest** (📰)
- **Co**: Cotygodniowe streszczenia wiadomości z kanałów
- **Gdzie**: `os.holisticjson.pl/community`
- **Jak**:
  1. Hermes bot zbiera wszystkie wiadomości z Discord → JSON
  2. Gemini 2.0 Flash streścza (max 500 tokens) wg szablonu:
     - **Top Announcements** (sticky posts)
     - **Hot Topics** (3-5 najczęstszych tematów)
     - **New Resources** (linki, pliki, artykuły)
     - **Member Milestones** (osiągnięcia członków)
  3. Renderowanie w Streamlit jako interaktywne karty
- **Automatyzacja**: Cronjob co poniedziałek o 9:00 UTC

#### **Moduł 2: Resource Library** (📚)
- **Co**: Centralna biblioteka wszystkich zasobów
- **Kategorie**:
  - 📖 Kursy (YouTube, Udemy, własne)
  - 🔬 Prompty AI (ChatGPT, Gemini, Cursor)
  - 🛠️ Narzędzia (productivity, automation, LLM)
  - 📝 Archiwa (artykuły, case studies, research)
  - 🎧 Podcasty + Transkrypcje
- **Wyszukiwanie**: Full-text search (FTS) po tagach ADHD
- **Rekomendacje**: "Dla Ciebie" na podstawie profilu użytkownika

#### **Moduł 3: Onboarding Bot** (🤖)
- **Trigger**: Nowy user wchodzi na dashboard
- **Flow**:
  1. Powitanie + historia Holistic JSON (ze źródła `o_mnie.md`)
  2. Quiz: "Co Cię tu sprowadza?" (5 pytań multiple choice)
  3. Automatyczne tagi (np. `founder`, `newbie`, `mentor`)
  4. Rekomendacja startowych zasobów
  5. Zaproszenie na Discord + przypomnienie o zasadach
- **Lokalizacja**: Sidebar Streamlit (co session)

---

## III. IMPLEMENTACJA (KAMIENIE MILOWE)

### FAZA 1: Infrastruktura (Tydzień 1)
- [ ] Utworzyć folder `~/.hermes/community/` (raw messages)
- [ ] Stworzyć skrypt `collect_discord_messages.py` (Hermes Tool)
- [ ] Zdefiniować schema JSON dla Community Digest
- [ ] Ustawić first cronjob (test run)

### FAZA 2: LLM Pipeline (Tydzień 2)
- [ ] Integracja Gemini 2.0 do streszczania
- [ ] Template dla Community Digest (markdown format)
- [ ] Error handling + Retry logic (Exponential Backoff)
- [ ] Walidacja outputu (length, tone, no_hallucinations)

### FAZA 3: Streamlit UI (Tydzień 3)
- [ ] Nowa strona `/community` w app.py
- [ ] Komponent DigestCard (responsive, ADHD-friendly)
- [ ] Resource Library (tabelka, filtry, search)
- [ ] Onboarding Modal (przy first visit)

### FAZA 4: Polish + Monitoring (Tydzień 4)
- [ ] A/B testing (digest frequency, length)
- [ ] Analytics (co czytają, co ignorują)
- [ ] Feedback form z community
- [ ] Iteracyjne ulepszenia

---

## IV. KANAŁY INTEGRACJI

### Discord Server (ADHD4Life Guild)
- **Bot Token**: Przechowywany w Hermes Secrets (~/.hermes/config/secrets.toml)
- **Channels to Track**:
  - `#announcements` – sticky posts (priority)
  - `#resource-sharing` – artykuły, kursy
  - `#wins` – member achievements
  - `#help` – Q&A (zbieramy FAQ)
- **Permissions**: Read-only (bot nie pisze na chacie)

### Telegram Community
- **Group ID**: Z memory (`-1001234567890`)
- **Metoda**: Hermes Telegram integration
- **Flow**: Message → Hermes bot → Local DB

### Slack Workspace (opcjonalnie)
- **Token**: OAuth2 (jeśli będzie potrzebne)
- **Channels**: TBD

---

## V. ADHD-FRIENDLY UX DESIGN

### Zasady Projektowania
1. **Zero Cognitive Load**:
   - Max 3 sekcje widoczne jednocześnie
   - Jasne piktogramy + krótkie nagłówki
   - Brak ścian tekstu (max 2-3 zdania per karta)

2. **Quick Capture**:
   - Przycisk "📌 Save for Later" na każdej karcie
   - Saved items trafią do osobistego Kanban
   - Exportable do Notion/Obsidian

3. **Accessibility**:
   - Dark mode domyślnie
   - Fonty: Atkinson Hyperlegible (wylegalizowana czcionka)
   - Keyboard navigation pełna
   - Screen reader compatible

4. **Personalizacja**:
   - Filter po tagach (`#automation`, `#mental-health`, `#productivity`)
   - "For You" rekomendacje
   - Moje saved items (persist w JSON)

---

## VI. DATA & PRIVACY

### Bezpieczeństwo
- **No PII**: Nie przechowujemy imion/emails (tylko user_id)
- **Encryption**: Messages at rest (jeśli dane wrażliwe)
- **GDPR Ready**: Opcja delete dla użytkownika
- **Open Source**: Community może audytować kod

### Retention Policy
- Raw Discord messages: 30 dni
- Digests: 1 rok archiwum
- Personal data (saved items): 6 miesięcy po deletion

---

## VII. METRYKI SUKCESU

| Metryka | Target | Tracking |
|---------|--------|----------|
| Weekly Active Users (WAU) | 50+ | Google Analytics |
| Avg Time on Community Hub | 5+ min | Streamlit session tracking |
| Resource Downloads/Week | 100+ | Download counter |
| Community Digest Open Rate | 70%+ | Email/Telegram analytics |
| NPS Score (Community) | 8+/10 | Quarterly survey |

---

## VIII. TIMELINE DEPLOYMENT

```
[Teraz]
┌─ Dzisiaj: Plan napisany ✅
├─ Tydzień 1: Infrastruktura live
├─ Tydzień 2: LLM pipeline live
├─ Tydzień 3: Dashboard live (beta)
├─ Tydzień 4: Public launch + monitoring
└─ Miesiąc 2: Community feedback loop + iterations
```

---

## IX. PLIKI DO STWORZENIA

```
~/.hermes/community/
├── config/
│   ├── channels.yaml          # Discord/Telegram channel mappings
│   ├── tags.yaml              # ADHD-related tags taxonomy
│   └── templates/
│       └── digest_template.md # Szablon streszczenia
├── scripts/
│   ├── collect_discord_messages.py
│   ├── summarize_digest.py
│   ├── onboarding_flow.py
│   └── push_to_dashboard.py
├── raw_messages/
│   ├── discord/
│   │   ├── 2026-05-28_announcements.json
│   │   └── 2026-05-28_resource_sharing.json
│   └── telegram/
├── processed/
│   └── digests/
│       └── 2026-05-28_community_digest.json
└── README.md
```

---

## X. NEXT STEPS (PRIORITY ZERO)

1. **Confirm Discord Bot Permissions** – Czy bot ma dostęp do wszystkich kanałów?
2. **Setup Secrets** – Przechowywanie API keys bezpiecznie
3. **Create First Test Digest** – Ręcznie, aby zvalidować template
4. **Deploy Cronjob** – Hermes cronjob system
5. **Notify Community** – Announcement na Discord: "Community Hub Coming Soon!"

---

## XI. NOTES

- **Owner**: Holistic JSON
- **Contributors**: [TBD – Community Mods]
- **Last Updated**: 28 maja 2026, 21:45 UTC
- **Version**: 1.0 (Deployment-Ready)
