# 🔐 PRYWATNY PLAN OPERACYJNY GCP & CLOUDFLARE (Tomasz Duda)
## Ściśle poufne — nie przeznaczone do publikacji. Zawiera mapowania kont, projekty, komendy czyszczenia i dane autoryzacyjne.

---

## 🗺️ 1. Pełna Mapa Twoich Kont i Profilów Chmurowych

Masz 4 różne konta Google i ponad 10 powiązanych z nimi projektów. Aby zarządzać nimi bezkonfliktowo i bez ciągłego logowania, używaj profili w Windows PowerShell:

| Nazwa Profilu | Konto Google (E-mail) | ID Projektu GCP | Rola / Przeznaczenie |
| :--- | :--- | :--- | :--- |
| **`profile-tomasz`** | `tomaszc4y@gmail.com` | `coolfon-project` | Prywatna piaskownica (Full trial + GenAI) |
| **`profile-jaison`** | `holisticjson@gmail.com` | `holistic-dashboard-dev` | Agencja Jaison Core, Hermes VM, n8n, Cloud Run |
| **`profile-broker`** | `brokerholistic@gmail.com` | `holistic-broker` | SaaS Holistic Broker (VM, baza wiedzy, n8n) |
| **`profile-laptop`** | `gtrmgroup@gmail.com` | `gtrm-project` | Portfolio Klientów (Coolfon, kurczakujasia, viptransporter) |

---

## 💻 2. Szybka ściągawka PowerShell: Zarządzanie Profilami

Uruchom poniższe komendy (jako One-Liners) tylko raz, aby na stałe skonfigurować wszystkie cztery profile:

```powershell
# Inicjalizacja profili
gcloud config configurations create profile-tomasz
gcloud config configurations create profile-jaison
gcloud config configurations create profile-broker
gcloud config configurations create profile-laptop

# Autoryzacja i powiązanie Profilu Tomasz
gcloud config configurations activate profile-tomasz; gcloud auth login tomaszc4y@gmail.com; gcloud config set project coolfon-project; gcloud auth application-default login

# Autoryzacja i powiązanie Profilu Jaison
gcloud config configurations activate profile-jaison; gcloud auth login holisticjson@gmail.com; gcloud config set project holistic-dashboard-dev; gcloud auth application-default login

# Autoryzacja i powiązanie Profilu Broker
gcloud config configurations activate profile-broker; gcloud auth login brokerholistic@gmail.com; gcloud config set project holistic-broker; gcloud auth application-default login

# Autoryzacja i powiązanie Profilu Laptop
gcloud config configurations activate profile-laptop; gcloud auth login gtrmgroup@gmail.com; gcloud config set project gtrm-project; gcloud auth application-default login
```

### Komenda do przełączania profilu chmurowego w ułamku sekundy:
```powershell
gcloud config configurations activate NAZWA_PROFILU
# Sprawdzenie aktualnie wybranego profilu
gcloud config configurations list
```

---

## 📉 3. Audyt CFO — Czyszczenie i ratowanie budżetów Free Trial

Twoje środki na tradycyjną infrastrukturę (VM, dyski) zbliżają się do końca:
*   **Jaison (`holisticjson@gmail.com`):** Zostało tylko **148,45 zł**.
*   **Broker (`brokerholistic@gmail.com`):** Zostało tylko **86,55 zł** (stan krytyczny).

### Komendy ratunkowe do uruchomienia w PowerShell (Wykonaj je dzisiaj):

```powershell
# 1. Przełącz na profil Jaison
gcloud config configurations activate profile-jaison

# 2. Usuń nieużywany i zbędny dysk hermes-os (30GB) z regionu USA
gcloud compute disks delete hermes-os --zone=us-central1-a --quiet

# 3. Usuń drogi, nieużywany dysk SSD hermes-os-ssd-50gb (50GB) z regionu USA
gcloud compute disks delete hermes-os-ssd-50gb --zone=us-central1-a --quiet

# 4. Usuń niepotrzebne i testowe zasobniki Cloud Storage
gcloud storage rm --recursive gs://holistic_kubelek
gcloud storage rm --recursive gs://771359551342_283819567_us_import_content_with_faq_csv
```

---

## 🌐 4. Krok po kroku: Naprawa certyfikatu SSL `os.jaison.pl` w Cloudflare

Błąd "Waiting for certificate provisioning" w Google Cloud Run występuje dlatego, że Cloudflare ma włączone proxy.

1.  Zaloguj się do konta Cloudflare powiązanego z e-mailem `holisticjson@gmail.com`.
2.  Przejdź do domeny **`jaison.pl`** -> sekcja **DNS -> Records**.
3.  Zlokalizuj rekord typu **A** o nazwie `os` kierujący na adres IP Twojego serwera: `35.210.44.117`.
4.  Kliknij **Edit** przy rekordzie `os`.
5.  Kliknij pomarańczowy suwak, aby zmienić jego status z **Proxied (Pomarańczowa chmurka)** na **DNS Only (Szara chmurka)**.
6.  Kliknij **Save**. Google Cloud pomyślnie zweryfikuje własność domeny i w ciągu kilku godzin wystawi darmowy certyfikat SSL!

---

## 🔑 5. Odzyskiwanie / Reset haseł do Nous Research Hermes Dashboard

Panel na subdomenie `os.jaison.pl` wymaga logowania Username & Password, ponieważ został zbindowany do publicznego adresu IP. Zabezpieczenia te są skonfigurowane bezpośrednio w plikach środowiskowych na Twoim serwerze w chmurze GCP.

### Jak sprawdzić lub zresetować hasło i login?

1.  Zaloguj się na serwer VM `hermes-jaison-core` przez SSH za pomocą PowerShell:
    ```powershell
    gcloud config configurations activate profile-jaison; gcloud compute ssh hermes-jaison-core --zone=europe-west1-b
    ```
2.  Wyświetl plik konfiguracyjny Hermes `.env` na serwerze:
    ```bash
    cat /home/holisticjson/.hermes/.env
    ```
    *   **Zwróć uwagę na zmienne:**
        *   `HERMES_DASHBOARD_BASIC_AUTH_USERNAME` (tutaj zapisany jest Twój login).
        *   `HERMES_DASHBOARD_BASIC_AUTH_PASSWORD` (tutaj zapisane jest Twoje hasło tekstowe).
        *   Jeśli ich tam nie ma, możesz je dopisać, aby wymusić własne dane logowania.
3.  Aby zmienić hasło, otwórz edytor tekstu na serwerze:
    ```bash
    nano /home/holisticjson/.hermes/.env
    ```
    *   Dopisz lub zmień linie:
        ```bash
        HERMES_DASHBOARD_BASIC_AUTH_USERNAME=admin
        HERMES_DASHBOARD_BASIC_AUTH_PASSWORD=WpiszSwojeSilneHaslo123!
        ```
    *   Zapisz plik (`CTRL + O`, potem Enter) i wyjdź z edytora (`CTRL + X`).
4.  Zrestartuj procesy Hermesa, aby załadować nowe dane:
    ```bash
    pm2 restart all
    ```
    Lub, jeśli działa jako usługa systemowa:
    ```bash
    sudo systemctl restart hermes
    ```
5.  Wejdź na `os.jaison.pl` i zaloguj się nowo ustawionymi danymi!

---

## 🌐 6. Procedura Świeżej Instalacji Hermes VM na `coolfon-project`

Ta procedura pozwoli Ci postawić czyste, bezpieczne i super zoptymalizowane środowisko Hermes VM bezpośrednio na Twoim koncie **`tomaszc4y@gmail.com` (projekt `coolfon-project`)**, wykorzystując pełne 1126 zł Free Trial.

### KROK 1: Uruchomienie nowej maszyny VM w chmurze GCP
Wpisz poniższe polecenie w PowerShell jako One-Liner, aby utworzyć maszynę wirtualną o optymalnych parametrach (niski koszt, wysoka wydajność) w najbliższym europejskim regionie:

```powershell
gcloud config configurations activate profile-tomasz; gcloud compute instances create hermes-coolfon-core --zone=europe-west1-b --machine-type=e2-standard-2 --image-family=ubuntu-2204-lts --image-project=ubuntu-os-cloud --boot-disk-size=30GB --boot-disk-type=pd-standard --network-tier=STANDARD --tags=http-server,https-server
```

### KROK 2: Otwarcie portów sieciowych dla ruchu
Musisz otworzyć porty dla paneli i API Hermesa:
```powershell
gcloud compute firewall-rules create allow-hermes-http-https --allow=tcp:80,tcp:443,tcp:8089,tcp:4000 --target-tags=http-server,https-server --description="Allow HTTP HTTPS and Hermes Ports"
```

### KROK 3: Połączenie przez SSH i instalacja podstawowa (Ubuntu)
Połącz się z nową maszyną przez SSH:
```powershell
gcloud compute ssh hermes-coolfon-core --zone=europe-west1-b
```

Po zalogowaniu do Ubuntu, zainstaluj najnowszy pakiet Docker oraz PM2 (jako One-Liners w konsoli Ubuntu):
```bash
sudo apt-get update && sudo apt-get install -y docker.io nodejs npm git && sudo npm install -y pm2 -g
```

### KROK 4: Wgranie Twojego unikalnego kontekstu dewelopera i kluczy
1.  Na nowym serwerze utwórz strukturę folderów:
    ```bash
    mkdir -p /home/holisticjson/.hermes/keys /home/holisticjson/.hermes/knowledge
    ```
2.  Wygeneruj klucz JSON dla konta usługowego (Service Account) w projekcie `coolfon-project` z uprawnieniami **Vertex AI User**.
3.  Zgraj klucz na serwer i zapisz pod ścieżką:  
    `/home/holisticjson/.hermes/keys/coolfon-project-sa.json`
4.  Wgraj swoje pliki wiedzy i skrypty (całą paczkę `.hermes` skopiowaną z obecnego serwera) do `/home/holisticjson/.hermes/`.
5.  Utwórz plik `.env` na serwerze:
    ```bash
    nano /home/holisticjson/.hermes/.env
    ```
    Wklej i dostosuj poniższe dane:
    ```bash
    API_SERVER_ENABLED=true
    GATEWAY_ALLOW_ALL_USERS=true
    API_SERVER_CORS_ORIGINS=*
    
    # Twój nowy projekt i nowy klucz z konta tomaszc4y@gmail.com
    GOOGLE_APPLICATION_CREDENTIALS=/home/holisticjson/.hermes/keys/coolfon-project-sa.json
    VERTEX_PROJECT=coolfon-project
    VERTEX_LOCATION=us-central1
    
    # Zabezpieczenia Basic Auth dla Twojego panelu
    HERMES_DASHBOARD_BASIC_AUTH_USERNAME=admin
    HERMES_DASHBOARD_BASIC_AUTH_PASSWORD=WpiszSwojeSilneHasloTutaj!
    ```

### KROK 5: Mapowanie Domeny w Cloud Run i DNS
W panelu Cloud Run (lub mapowaniu Compute Engine na domenie `os.jaison.pl` w Cloudflare) zmień adres docelowy IP na adres nowej maszyny `hermes-coolfon-core` (znajdziesz go poleceniem `gcloud compute instances describe hermes-coolfon-core --zone=europe-west1-b --format="get(networkInterfaces[0].accessConfigs[0].natIP)"`).

W Cloudflare ustaw chmurkę na **Szary status (DNS Only)**, aby Let's Encrypt pomyślnie wygenerował certyfikat SSL na nowym serwerze!

