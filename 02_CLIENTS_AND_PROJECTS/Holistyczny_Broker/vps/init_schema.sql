-- 🏛️ Holistyczny Broker - Baza danych PostgreSQL (v2.0 Schema)
-- Przechowuje leady, zeskrapowane lub zeskanowane działki, dane planistyczne i historie dopasowań.

-- Włączenie obsługi UUID dla unikalnych identyfikatorów
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Tabela Leadów (Leads)
CREATE TABLE IF NOT EXISTS leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    contact VARCHAR(255) NOT NULL,
    budget VARCHAR(100),
    investment_type VARCHAR(100), -- np. MW (Mieszkaniowa), Usługowa, Logistyka
    source VARCHAR(100) NOT NULL,   -- np. "strona główna / Skanuj Potencjał", "dla-biznesu.html", "direct_import"
    status VARCHAR(50) DEFAULT 'new', -- np. 'new', 'nda_sent', 'nda_signed', 'negotiating', 'closed_won', 'closed_lost'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tabela Działek i Ofert (Properties / Parcels)
CREATE TABLE IF NOT EXISTS properties (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    parcel_id VARCHAR(100) UNIQUE NOT NULL, -- identyfikator działki w formacie ULDK np. 106103_9.0022.88/14
    obreb VARCHAR(100),                      -- np. S-22 Śródmieście
    powiat VARCHAR(100) DEFAULT 'm. Łódź',
    area_sqm NUMERIC(12, 2) NOT NULL,       -- powierzchnia działki z Geoportalu
    mpzp_status VARCHAR(50),                -- np. "UCHWALONY", "BRAK"
    mpzp_symbol VARCHAR(50),                -- np. "MW/U-12"
    mpzp_przeznaczenie TEXT,                 -- pełny opis z planu zagospodarowania
    media JSONB,                            -- tablica dostępnych mediów
    rwdz_decision VARCHAR(100),             -- numer prawomocnego pozwolenia na budowę z GUNB RWDZ (jeśli istnieje)
    scoring_value NUMERIC(5, 2),            -- ogólny scoring ważony z matrycy (0-100)
    source_tag VARCHAR(100) NOT NULL,       -- np. "RWDZ_Crawler", "Skan / Agent Kowalski", "Otodom_Scraper"
    raw_data JSONB,                         -- zrzut surowych danych z API
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabela Dopasowań (Matching History)
CREATE TABLE IF NOT EXISTS matching_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
    property_id UUID REFERENCES properties(id) ON DELETE CASCADE,
    match_score NUMERIC(5, 2) NOT NULL,     -- wynik dopasowania w %
    match_reasons TEXT,                      -- uzasadnienie generowane przez LLM
    status VARCHAR(50) DEFAULT 'pending',   -- np. 'pending' (czeka na Telegram), 'approved', 'rejected', 'sent_to_client'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_lead_property_match UNIQUE (lead_id, property_id)
);

-- 4. Tabela Zeskanowanych Dokumentów (Scanned Documents)
CREATE TABLE IF NOT EXISTS scanned_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    file_name VARCHAR(255) NOT NULL,
    gcs_uri VARCHAR(512),                   -- adres pliku na Google Cloud Storage
    extracted_data JSONB,                   -- ustrukturyzowane dane wyciągnięte przez Gemini 2.5 Pro
    validated_status VARCHAR(50),           -- np. "VERIFIED", "DISCREPANCY_FOUND", "PENDING_CHECK"
    discrepancy_desc TEXT,                  -- opis rozbieżności z rejestrem
    source_tag VARCHAR(100),                -- np. "Skan / Agent Nowak"
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Automatyczna aktualizacja updated_at
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_leads_modtime BEFORE UPDATE ON leads FOR EACH ROW EXECUTE PROCEDURE update_modified_column();
CREATE TRIGGER update_properties_modtime BEFORE UPDATE ON properties FOR EACH ROW EXECUTE PROCEDURE update_modified_column();
