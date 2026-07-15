# Walkthrough — Programowe wnioski o podwyższenie limitów GCP

## Co zostało zrobione

Stworzono narzędzie [`request_quota.py`](file:///c:/Aplikacje%20MVP/Vojsik%20AI/request_quota.py) do programowego składania wniosków o podwyższenie limitów API Vertex AI (Gemini) w Google Cloud Platform bez potrzeby wchodzenia do konsoli webowej.

---

## Wyniki wykonania (2026-07-08, projekt: `gtrm-project`)

### RPM (Requests Per Minute) — 8/8 wniosków wysłanych

| Model (base_model ID) | Region | Preference ID | Status |
|---|---|---|---|
| `gemini-2.5-flash-preview-04-17` | us-central1 | `gtrm-gencntrequest-1783525019` | Oczekuje |
| `gemini-2.5-flash-preview-04-17` | europe-west3 | `gtrm-gencntrequest-1783525027` | Oczekuje |
| `gemini-2.5-pro-preview-06-05` | us-central1 | `gtrm-gencntrequest-1783525034` | Oczekuje |
| `gemini-2.5-pro-preview-06-05` | europe-west3 | `gtrm-gencntrequest-1783525042` | Oczekuje |
| `gemini-2.0-flash-001` | us-central1 | `gtrm-gencntrequest-1783525049` | Oczekuje |
| `gemini-2.0-flash-001` | europe-west3 | `gtrm-gencntrequest-1783525056` | Oczekuje |
| `gemini-2.0-flash-lite-001` | us-central1 | `gtrm-gencntrequest-1783525062` | Oczekuje |
| `gemini-2.0-flash-lite-001` | europe-west3 | `gtrm-gencntrequest-1783525069` | Oczekuje |

> **`granted: 0`** oznacza że wniosek jest przyjęty i czeka na automatyczną lub manualną weryfikację przez Google. Czas oczekiwania: zazwyczaj kilka minut do 2 dni roboczych.

### TPM (Tokens Per Minute) — nie wymagały podwyższenia

Limity tokenów na `gtrm-project` (płatne konto org) są już na poziomie ~4 000 000 TPM — znacznie powyżej żądanych 500 000. Błąd `FAILED_PRECONDITION: decreases quota` potwierdza to.

---

## Jak śledzić status wniosków

```
https://console.cloud.google.com/iam-admin/quotas?project=gtrm-project
```

Lub przez terminal:

```bash
python "C:\Aplikacje MVP\Vojsik AI\request_quota.py" --list
```

---

## Konfiguracja gcloud (jednorazowa, już wykonana)

```bash
gcloud config set account gtrmgroup@gmail.com
gcloud config set project gtrm-project
gcloud auth application-default set-quota-project gtrm-project
```

AntiGravity IDE i wszystkie skrypty Python używające ADC automatycznie korzystają teraz z `gtrm-project`.

---

## Jak złożyć nowe wnioski w przyszłości

```bash
# Tylko dla konkretnych modeli i regionów:
python "C:\Aplikacje MVP\Vojsik AI\request_quota.py" \
  --models gemini-2.5-flash gemini-2.5-pro \
  --rpm 120 \
  --regions us-central1

# Dry-run (bez wysyłania):
python "C:\Aplikacje MVP\Vojsik AI\request_quota.py" --dry-run

# Sprawdzenie statusu istniejących preferencji:
python "C:\Aplikacje MVP\Vojsik AI\request_quota.py" --list
```

---

## Dlaczego błąd 429 NIE jest spowodowany porą dnia

Błąd `HTTP 429 Resource Exhausted` to twarde ograniczenie na poziomie projektu GCP — nie ma związku z:
- godziną dnia
- przeciążeniem sieci Google
- liczbą aktywnych użytkowników globalnie

Domyślny limit dla nowych projektów to 1–5 RPM na model — zbyt mało dla równoległych procesów agentowych.
