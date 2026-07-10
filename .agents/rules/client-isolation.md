# Standard Izolacji i Struktury Klienta (Client Isolation & Structure Standard)

Wszyscy klienci zewnętrzni w folderze `04-clients/` muszą posiadać absolutnie zunifikowaną strukturę folderów opartą na szablonie `_client-template`. Ta struktura zapobiega wyciekom danych autoryzacyjnych, chaosowi w plikach projektowych oraz ułatwia automatyzację procesów przez agentów AI.

## Struktura Katalogu Klienta
Każdy katalog klienta `04-clients/<nazwa_klienta>/` musi posiadać podkatalogi:

```text
├── 00-admin/         # Dane rejestracyjne, umowy, faktury, dostępy, credentials (np. api_keys, ftp)
├── 01-brand/         # Brandbook, pozycjonowanie, tone of voice, persony, strategia marketingowa
├── 02-website/       # Audyty SEO, kod źródłowy stron www, backupy baz danych, konfiguracja domen
├── 03-social/        # Kalendarze publikacji, prompty postów, scenariusze wideo, teksty copywritingu
├── 04-assets/        # Logotypy, grafiki, surowe wideo, zdjęcia, b-roll, fonty firmowe
├── 05-automation/    # Schematy n8n, webhooki, skrypty integracyjne, konfiguracja CRM
├── 06-crm/           # Dane leadów, listy mailingowe, notatki ze spotkań handlowych
├── 07-deploy/        # Instrukcje wdrożenia na hosting (FTP, Cloud Run), konfiguracja DNS
├── 08-reports/       # Raporty z kampanii, analityka GA4, case studies, wyniki optymalizacji
└── 09-archive/       # Stare pomysły, nieaktywne podstrony, odrzucone wersje kreacji
```

## Zasady Bezwzględnego Przestrzegania (Isolation Principles)
1. **Całkowita Izolacja:** Agenci AI mają kategoryczny zakaz mieszania plików lub danych między klientami. Pliki klienta `A` nie mogą być pod żadnym pozorem kopiowane, odwoływane lub linkowane w katalogu klienta `B`.
2. **Kwalifikacja do _client-template:** Przed rozpoczęciem jakichkolwiek prac dla nowego klienta, agent AI musi skopiować strukturę `04-clients/_client-template/` do nowo utworzonego folderu klienta.
3. **Zasada Poufności (Credentials):** Wszelkie klucze API, loginy FTP i hasła mogą znajdować się wyłącznie w plikach konfiguracyjnych wewnątrz podkatalogu `00-admin/`. Niedozwolone jest umieszczanie surowych kluczy w kodzie źródłowym stron lub skryptach automatyzacji.
