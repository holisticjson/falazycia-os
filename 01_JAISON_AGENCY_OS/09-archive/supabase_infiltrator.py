"""
🛰️ Supabase Infiltrator & Schema Inspector — J(AI)SON Integration Utility
======================================================================
Ten skrypt umożliwia automatyczne połączenie z bazą Supabase Twojego projektu Content Box,
odczytanie struktury tabel (schema) oraz zrzucenie pomysłów na posty, kalendarza i danych do Twojego lokalnego panelu J(AI)SON.

Wymagania: pip install supabase python-dotenv
Użycie:
  python 02-os-jaison/integrations/supabase_infiltrator.py --test-connection
  python 02-os-jaison/integrations/supabase_infiltrator.py --export-schema
  python 02-os-jaison/integrations/supabase_infiltrator.py --fetch-content
"""

import os
import sys
import argparse
from pathlib import Path

# Załaduj zmienne środowiskowe z głównego pliku .env
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).resolve().parents[2] / ".env"
    load_dotenv(dotenv_path=env_path)
except ImportError:
    pass

try:
    from supabase import create_client, Client
except ImportError:
    print("⚡ Instalowanie wymaganej biblioteki supabase-py...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "supabase", "python-dotenv"])
    from supabase import create_client, Client


def get_credentials() -> tuple[str, str]:
    """Pobiera poświadczenia do Supabase ze zmiennych środowiskowych."""
    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_KEY", "")
    
    # Przykładowe/zastępcze dane jeśli nie zostały jeszcze zdefiniowane w .env
    if not url or not key:
        print("⚠️ Brak kluczy SUPABASE_URL i SUPABASE_KEY w pliku .env!")
        print("👉 Dodaj je do swojego pliku .env w następujący sposób:")
        print("   SUPABASE_URL=https://twoj-projekt.supabase.co")
        print("   SUPABASE_KEY=twoj-klucz-service-role-lub-anon")
        print("\n[!] W celach demonstracyjnych skrypt spróbuje teraz pobrać parametry interaktywnie...")
        
        # Fallback na interaktywne zapytanie w konsoli
        url = input("Wprowadź Supabase URL: ").strip()
        key = input("Wprowadź Supabase Key (Service Role lub Anon): ").strip()
        
    return url, key


def test_supabase_connection() -> Client | None:
    """Testuje połączenie z bazą danych Supabase."""
    url, key = get_credentials()
    if not url or not key:
        print("❌ Nie można przetestować połączenia bez poprawnych danych uwierzytelniających.")
        return None
        
    print(f"🔗 Łączenie z Supabase pod adresem: {url}...")
    try:
        client = create_client(url, key)
        print("✅ Połączenie zintegrowane pomyślnie z klientem Supabase!")
        return client
    except Exception as e:
        print(f"❌ Krytyczny błąd połączenia: {str(e)}")
        return None


def export_database_schema(client: Client):
    """Infiltruje strukturę bazy danych i wyświetla dostępne tabele."""
    print("\n🔍 INFILTRACJA STRUKTURY BAZY DANYCH SUPABASE...")
    
    # Tradycyjne tabele w Content Box (posts, campaigns, user_profiles, content_ideas, calendar_events)
    target_tables = ["posts", "campaigns", "user_profiles", "content_ideas", "calendar_events", "schedules"]
    found_tables = []
    
    for table in target_tables:
        try:
            # Próbujemy pobrać 1 wiersz z danej tabeli w celu weryfikacji jej istnienia
            res = client.table(table).select("*").limit(1).execute()
            print(f"  👉 Tabela '{table}': [WYKRYTA] - Zawiera dane.")
            found_tables.append(table)
        except Exception as e:
            # Jeśli tabela nie istnieje, Supabase wyrzuci błąd
            if "does not exist" in str(e).lower() or "404" in str(e):
                print(f"  ❌ Tabela '{table}': [NIE ISTNIEJE]")
            else:
                # Tabela istnieje, ale np. jest pusta lub brak uprawnień
                print(f"  ⚠️ Tabela '{table}': [ZABLOKOWANA LUB PUSTA] - (Szczegóły: {str(e)[:60]}...)")
                found_tables.append(table)
                
    if not found_tables:
        print("\n⚠️ Nie wykryto standardowych tabel Content Box. Prawdopodobnie Twoja baza używa innych nazw.")
        print("💡 Sugestia: Możesz uruchomić zapytanie SQL bezpośrednio w konsoli Supabase, aby pobrać listę tabel.")
    else:
        print(f"\n🎉 Pomyślnie zmapowano tabele: {', '.join(found_tables)}")


def fetch_and_dump_content(client: Client):
    """Pobiera pomysły na posty oraz zaplanowane posty z Supabase."""
    print("\n📥 POBIERANIE TREŚCI MARKETINGOWYCH Z SUPABASE...")
    
    # 1. Pobieranie Pomysłów na Posty (Content Ideas)
    try:
        ideas_res = client.table("content_ideas").select("*").limit(10).execute()
        ideas = ideas_res.data
        print(f"  ✅ Pobrano {len(ideas)} pomysłów na treści z tabeli 'content_ideas'.")
        for i, idea in enumerate(ideas, 1):
            title = idea.get("title", idea.get("topic", "Bez tytułu"))
            platform = idea.get("platform", "Wszystkie")
            print(f"    [{i}] {title} ({platform})")
    except Exception as e:
        print(f"  ❌ Nie udało się pobrać danych z 'content_ideas': {str(e)}")

    # 2. Pobieranie Kalendarza i Zaplanowanych Postów
    try:
        posts_res = client.table("posts").select("*").limit(10).execute()
        posts = posts_res.data
        print(f"  ✅ Pobrano {len(posts)} zaplanowanych postów z tabeli 'posts'.")
        for i, post in enumerate(posts, 1):
            content = post.get("content", post.get("text", "Pusta treść"))[:60]
            status = post.get("status", "Nieznany")
            print(f"    [{i}] Status: {status} | Treść: {content}...")
    except Exception as e:
        print(f"  ❌ Nie udało się pobrać danych z 'posts': {str(e)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Supabase Infiltrator CLI")
    parser.add_argument("--test-connection", action="store_true", help="Testuje połączenie z bazą danych")
    parser.add_argument("--export-schema", action="store_true", help="Mapuje tabele bazy danych")
    parser.add_argument("--fetch-content", action="store_true", help="Pobiera pomysły i kalendarz postów")
    
    args = parser.parse_args()
    
    # Domyślnie jeśli nie podano flag, wykonaj wszystkie kroki
    if not (args.test_connection or args.export_schema or args.fetch_content):
        args.test_connection = True
        args.export_schema = True
        args.fetch_content = True
        
    client = test_supabase_connection()
    if client:
        if args.export_schema:
            export_database_schema(client)
        if args.fetch_content:
            fetch_and_dump_content(client)
    else:
        sys.exit(1)
