# ⚙️ INSTRUKCJA AUTOMATYZACJI GCP, VERTEX AI, HERMES OS & STREAMLIT DASHBOARD
## Pełny Przewodnik Krok po Kroku (CLI / Console) dla Projektu "Fala Życia"

---

## 🎯 EXECUTIVE SUMMARY & ODPOWIEDZI NA PYTANIA STRATEGICZNE

### 1. Czy można stworzyć nowy projekt w GCP na koncie `holisticjason@gmail.com`?
**TAK!** Jedno konto Google (`holisticjason@gmail.com`) i jedno konto rozliczeniowe (Billing Account z darmowymi kredytami $300) mogą obsługiwać **wiele osobnych projektów GCP**. 
- Tworzymy projekt o identyfikatorze: **`falazycia-os`**.
- Podpinamy pod niego aktywne konto bilingowe.
- Zyskujemy 100% czystej separacji zasobów (logi, zasobniki, bazy) bez konieczności ponownego wpisywania nowej karty bilingowej!

---

### 2. Czy warto sklonować Dashboard Streamlit i uruchomić Hermes Agentic OS na Maszynie VM?
**TAK, BARDZO WARTO!**
- **Sklonowany Dashboard Streamlit ("Fala Życia OS"):** Daje Anii, Monice i Tomkowi elegancki, dedykowany panel dowodzenia do podglądu statusu botów WhatsApp/Discord, kalendarzy Cal.com, bazy badań klinicznych i lejków partnerów.
- **Hermes Agentic OS na VM (GCP Compute Engine):** Działa jako suwerenny silnik orkiestracyjny 24/7.
- **Mostek MCP (Model Context Protocol):** Wystawiamy funkcje Streamlita i Hermes jako natywne serwery MCP. Dzięki temu Ty i Partnerzy możecie wydawać polecenia agentom z poziomu **Discorda**, **WhatsAppa** lub **Panelu Web**!

---

## 🛠️ INSTRUKCJA KROK PO KROKU: SKRYPTY GCLOUD (POWERSHELL ONE-LINERS)

Wszystkie komendy są sformatowane jako ciągłe polecenia PowerShell (One-Liners), całkowicie wolne od linuxowych ukośników `\`.

### Krok 1: Tworzenie Nowego Projektu GCP i Podpięcie Bilingu

Run w konsoli gcloud:
```powershell
gcloud projects create falazycia-os --name="Fala Życia OS" --set-as-default
```

Pobranie ID konta bilingowego:
```powershell
gcloud billing accounts list --format="json(name, displayName)"
```

Podpięcie konta bilingowego pod nowy projekt (`ACCOUNT_ID` zastąp swoim identyfikatorem konta):
```powershell
gcloud billing projects link falazycia-os --billing-account=ACCOUNT_ID
```

---

### Krok 2: Włączenie Kluczowych API dla Agencji i Agentów

Włączamy wszystkie niezbędne usługi jednym poleceniem:
```powershell
gcloud services enable run.googleapis.com compute.googleapis.com storage.googleapis.com aiplatform.googleapis.com discoveryengine.googleapis.com iam.googleapis.com cloudresourcemanager.googleapis.com --project=falazycia-os
```

---

### Krok 3: Tworzenie Konta Serwisowego (Service Account) i Klucza JSON dla Agentów

Tworzymy konto serwisowe dla Antigravity i agentów:
```powershell
gcloud iam service-accounts create jaison-agent-falazycia --display-name="Jaison Agent Fala Życia" --project=falazycia-os
```

Nadajemy uprawnienia zarządcze (Cloud Run, Cloud Storage, Vertex AI, Compute Engine):
```powershell
gcloud projects add-iam-policy-binding falazycia-os --member="serviceAccount:jaison-agent-falazycia@falazycia-os.iam.gserviceaccount.com" --role="roles/run.admin"
gcloud projects add-iam-policy-binding falazycia-os --member="serviceAccount:jaison-agent-falazycia@falazycia-os.iam.gserviceaccount.com" --role="roles/storage.admin"
gcloud projects add-iam-policy-binding falazycia-os --member="serviceAccount:jaison-agent-falazycia@falazycia-os.iam.gserviceaccount.com" --role="roles/aiplatform.user"
gcloud projects add-iam-policy-binding falazycia-os --member="serviceAccount:jaison-agent-falazycia@falazycia-os.iam.gserviceaccount.com" --role="roles/compute.admin"
```

Generujemy plik klucza JSON dla agenta:
```powershell
gcloud iam service-accounts keys create "C:\Aplikacje MVP\02_CLIENTS_AND_PROJECTS\lifewave\gcp-service-account-key.json" --iam-account=jaison-agent-falazycia@falazycia-os.iam.gserviceaccount.com --project=falazycia-os
```

---

### Krok 4: Tworzenie Zasobnika Cloud Storage (GCS) dla Assetów Wideo i Plików

Tworzymy zasobnik na materiały wideo, transkrypcje i e-booki:
```powershell
gcloud storage buckets create gs://falazycia-assets-bucket --project=falazycia-os --location=europe-west3
```

---

### Krok 5: Tworzenie Maszyny Wirtualnej (VM) pod Hermes Agentic OS & Dashboard Streamlit

Tworzymy lekką maszynę wirtualną w regionie europejskim:
```powershell
gcloud compute instances create falazycia-hermes-vm --project=falazycia-os --zone=europe-west3-c --machine-type=e2-small --image-family=ubuntu-2204-lts --image-project=ubuntu-os-cloud --boot-disk-size=30GB
```

---

## 🌐 INTEGRACJA CLOUDFLARE & GOOGLE SEARCH CONSOLE

1. **Cloudflare:**
   - Podpinamy domenę **`fala-zycia.pl`** pod Twoje konto Cloudflare (`holisticjason@gmail.com`).
   - Ustawiamy rekordy CNAME dla subdomen:
     - `swiatynia.fala-zycia.pl` ➔ CNAME kierujący na Cloud Run / GitHub Pages dla Ani.
     - `monika.fala-zycia.pl` ➔ CNAME kierujący na Cloud Run dla Moniki.
     - `x2o.fala-zycia.pl` ➔ CNAME kierujący na Cloud Run dla Tomasza.
     - `dashboard.fala-zycia.pl` ➔ CNAME kierujący na maszynę VM / Cloud Run ze Streamlit Dashboardem.

2. **Google Search Console:**
   - Dodajemy domenę `fala-zycia.pl` w Google Search Console (weryfikacja rekordem TXT w Cloudflare).
   - Przesyłamy mapę witryny `sitemap.xml` dla szybkiego indeksowania w Google i wyszukiwarkach LLM (GEO/AEO).
