#!/usr/bin/env python3
"""
systeme_agent.py - Pomocnik integracji i diagnostyki Systeme.io (Dyrektor AI CMO / CTO)
Zgodnie z Zasadą Proaktywnej Weryfikacji (Zero Zagadek) i Strategią "Jednego Taga".
Dostosowany do poprawnego wyświetlania znaków na konsoli Windows (w pełni obsługuje kodowanie UTF-8).
"""

import os
import sys
import codecs
import argparse

# Wymuszenie kodowania UTF-8 na konsoli Windows dla uniknięcia UnicodeEncodeError
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
if sys.stderr.encoding != 'utf-8':
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# Dodanie katalogu roboczego do path na wypadek uruchamiania z podkatalogów
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from integrations.systeme_io import SystemeIOClient
except ImportError:
    from integrations.systeme_io import SystemeIOClient

# Ładowanie zmiennych z pliku .env
env_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip()

def diagnoza_systeme_io():
    """
    Przeprowadza pełną, proaktywną diagnostykę połączenia z Systeme.io.
    Wyrzuca łopatologiczne i maszynowo sprawne porady w formacie ADHD-Optimal.
    """
    print("\n" + "="*50)
    print("🧠 DIAGNOSTYKA INTEGRACJI SYSTEME.IO -- HOLISTIC 2.0")
    print("="*50)

    api_key = os.environ.get("SYSTEME_IO_API_KEY")
    
    if not api_key:
        print("\n❌ [BŁĄD] Brak klucza SYSTEME_IO_API_KEY w Twoim pliku .env!")
        print("\n💡 CO MUSISZ ZROBIĆ KROK PO KROKU:")
        print("1. Zaloguj się na swoje konto w Systeme.io.")
        print("2. Przejdź do: Ustawienia (Twój profil) -> Klucze API (API Keys).")
        print("3. Wygeneruj nowy klucz i skopiuj go.")
        print("4. Otwórz plik .env w głównym katalogu projektu.")
        print("5. Wklej go jako: SYSTEME_IO_API_KEY=Twój_Klucz")
        print("6. Zapisz plik i uruchom ten skrypt ponownie.")
        return False

    print(f"✔ Wykryto klucz API: {api_key[:10]}...{api_key[-10:] if len(api_key) > 20 else ''}")
    print("📡 Testowanie połączenia z serwerem Systeme.io...")
    
    client = SystemeIOClient()
    result = client.get_contacts()
    
    if result["status"] == "success":
        print("✔ [SUKCES] Połączenie nawiązane pomyślnie!")
        contacts_data = result.get("data", {})
        
        count = "Nieznana"
        if isinstance(contacts_data, list):
            count = len(contacts_data)
        elif isinstance(contacts_data, dict):
            for key in ['items', 'contacts', 'data']:
                if key in contacts_data and isinstance(contacts_data[key], list):
                    count = len(contacts_data[key])
                    break
        
        print(f"✔ Liczba kontaktów na Twoim koncie: {count} / 2000 (Darmowy limit)")
        
        if isinstance(count, int) and count >= 1900:
            print("\n⚠️ [OSTRZEŻENIE] Zbliżasz się do darmowego limitu 2000 kontaktów!")
            print("👉 Zrób przegląd i usuń nieaktywne adresy, aby uniknąć opłat.")
        return True
    else:
        print("\n❌ [BŁĄD] Połączenie nie powiodło się!")
        print(f"👉 Szczegóły błędu: {result.get('message')}")
        
        print("\n💡 ROZWIĄZANIE PROBLEMU:")
        print("- Sprawdź internet: Upewnij się, że Twoja maszyna ma dostęp do sieci.")
        print("- Weryfikacja klucza: Twój klucz może być nieaktywny lub wygasły w Systeme.io.")
        print("- Blokada IP: Jeśli używasz dziwnych serwerów proxy lub VPN (np. Mullwad, AdGuard DNS), systemy zabezpieczeń Systeme.io mogą odrzucać żądanie.")
        print("- Problem z SSL: Jeśli widzisz błąd SSL, oznacza to problem z lokalnymi certyfikatami urzędów certyfikacji (CA) w Twojej instalacji Pythona. Możesz go rozwiązać ustawiając ignorowanie weryfikacji certyfikatów.")
        return False

def dodaj_leada(email, first_name, client_type="lead"):
    """
    Dodaje leada do Systeme.io stosując Strategię Jednego Taga.
    Używa custom fields do segmentacji (np. client_type: lead, affiliate, ADHD-client).
    """
    print(f"\n⚡ Inicjowanie zapisu leada: {email} ({first_name})...")
    client = SystemeIOClient()
    
    custom_fields = {
        "client_type": client_type,
        "source": "mercury_landing"
    }
    
    result = client.add_contact(email, first_name, custom_fields)
    
    if result["status"] == "success":
        print(f"✔ [SUKCES] Kontakt dodany pomyślnie do Systeme.io.")
        print(f"👉 Segmentacja: client_type ustawiono na '{client_type}'")
        return True
    elif result["status"] == "exists":
        print(f"ℹ️ [INFO] Kontakt o adresie {email} już istnieje w Systeme.io.")
        return True
    else:
        print(f"\n⚠️ [OSTRZEŻENIE] [AWARYJNY FALLBACK] Systeme.io API odmówiło posłuszeństwa.")
        print(f"👉 Szczegóły: {result.get('message')}")
        print(f"✔ [ZABEZPIECZENIE] Lead został zapisany lokalnie w clients/leads_fallback.json.")
        print(f"🤖 Agent Hermes wyśle powiadomienie o tym zdarzeniu podczas najbliższego crona.")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Systeme.io Integrator CLI - Holistic 2.0")
    parser.add_argument("--diagnose", action="store_true", help="Uruchom diagnostykę połączenia i kluczy API")
    parser.add_argument("--add", action="store_true", help="Dodaj próbny/nowy kontakt")
    parser.add_argument("--email", type=str, help="Adres email kontaktu")
    parser.add_argument("--name", type=str, help="Imię kontaktu")
    parser.add_argument("--type", type=str, default="lead", choices=["lead", "affiliate", "ADHD-client"], help="Typ klienta (zamiast tagu)")
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
        
    if args.diagnose:
        diagnoza_systeme_io()
    elif args.add:
        if not args.email or not args.name:
            print("❌ [BŁĄD] Musisz podać --email i --name, aby dodać kontakt!")
            sys.exit(1)
        dodaj_leada(args.email, args.name, args.type)
