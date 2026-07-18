# -*- coding: utf-8 -*-
"""
Holistyczny Broker - Deal Sourcing Simulator & Financial ROI Reporter (Blok 13)
Automatycznie generuje luksusowy raport inwestycyjny w estetyce "Quiet Luxury".
"""

import os
import json

def run_deal_sourcing_simulation():
    print("=" * 60)
    print("  [SYSTEM HERMES] INICJALIZACJA SKANERA REAL ESTATE (BLOK 13)  ")
    print("=" * 60)

    # 1. MOCKOWANE DANE WEJŚCIOWE (GUNB RWDZ + ULDK GEOPORTAL + EKW)
    print("\n[1/4] Pobieranie danych z rejestrów państwowych...")
    
    mock_rwdz_data = {
        "organ_kod": "1061",  # Prezydent Miasta Łodzi
        "numer_decyzji": "W-241/2026",
        "data_wplywu": "2026-05-14",
        "status_wniosku": "DECYZJA POZYTYWNA (Prawomocna)",
        "nazwa_zamierzenia": "Budowa budynku mieszkalnego wielorodzinnego z usługami w parterze oraz garażem podziemnym i infrastrukturą techniczną",
        "kategoria_obiektu": "XVII (Budynki mieszkalne wielorodzinne)",
        "inwestor": "REVOLTO PROPERTY LÓDŹ SP. Z O.O. (w likwidacji)",
        "powiat": "m. Łódź",
        "jednostka_ewidencyjna": "106103_9 (Łódź-Śródmieście)",
        "obreb": "S-22",
        "dzialki": "88/14, 88/15"
    }
    print(" >> [GUNB RWDZ] Znaleziono prawomocną decyzję o PnB dla inwestora w likwidacji!")

    mock_uldk_geoportal = {
        "identyfikator_dzialki": "106103_9.0022.88/14",
        "powierzchnia_geometryczna_m2": 4500.0,
        "mpzp_status": "UCHWALONY",
        "mpzp_symbol": "MW/U-12",
        "mpzp_przeznaczenie": "Zabudowa mieszkaniowa wielorodzinna oraz usługi nieuciążliwe",
        "max_wysokosc_m": 15.0,
        "max_intensywność_zabudowy": 1.8,
        "min_powierzchnia_biologicznie_czynna": "25%",
        "media_dostepne": ["woda", "kanalizacja deszczowa i sanitarna", "energia elektryczna", "ciepłociąg miejski"]
    }
    print(" >> [ULDK GEOPORTAL] Pobrano parametry planistyczne i geometrię działek. Powierzchnia: 4500 m2.")

    mock_ekw_data = {
        "numer_kw": "LD1M/00341855/2",
        "dzial_i_wpisy": "Obręb S-22, działki 88/14, 88/15. Sposób korzystania: Tereny zurbanizowane.",
        "dzial_ii_wlasnosc": "REVOLTO PROPERTY LÓDŹ SP. Z O.O. (w likwidacji)",
        "dzial_iii_prawa_roszczenia": "BRAK WPISÓW / WOLNE OD ROSZCZEŃ",
        "dzial_iv_hipoteki": "BRAK WPISÓW / WOLNE OD OBCIĄŻEŃ HIPOTECZNYCH"
    }
    print(" >> [EKW SYSTEM] Zweryfikowano stan prawny księgi wieczystej. Brak obciążeń! Status likwidacji właściciela to unikalna okazja off-market.")

    # 2. KALKULACJE CHŁONNOŚCI I ROI (FINANCIAL ENGINE)
    print("\n[2/4] Uruchamianie Silnika Finansowego (Financial Engine)...")
    
    # Wyliczenie chłonności gruntu (PUM - Powierzchnia Użytkowa Mieszkalna)
    powierzchnia_dzialki = mock_uldk_geoportal["powierzchnia_geometryczna_m2"]
    intensywnosc = mock_uldk_geoportal["max_intensywność_zabudowy"]
    
    # Szacunkowy współczynnik sprawności rzutu budynku (np. 80% powierzchni całkowitej nadziemnej to PUM)
    sprawnosc_rzutu = 0.82
    max_powierzchnia_calkowita = powierzchnia_dzialki * intensywnosc
    szacowany_pum = int(max_powierzchnia_calkowita * sprawnosc_rzutu)
    
    # Parametry kosztowe i przychodowe (Rynek Premium w Łodzi / Śródmieście)
    cena_gruntu = 4500000.0  # Okazyjna cena zakupu
    koszt_budowy_m2_pum = 4600.0  # Stan deweloperski o podwyższonym standardzie
    koszt_budowy_razem = szacowany_pum * koszt_budowy_m2_pum
    
    koszty_soft = 2300000.0  # Projekty, nadzór inwestorski, przyłącza, marketing, obsługa prawna
    calkowity_koszt_inwestycji_tdc = cena_gruntu + koszt_budowy_razem + koszty_soft
    
    cena_sprzedazy_m2_pum = 9800.0  # Średnia cena sprzedaży apartamentów premium w tej lokalizacji
    szacowany_przychod = szacowany_pum * cena_sprzedazy_m2_pum
    
    zysk_netto_przed_tax = szacowany_przychod - calkowity_koszt_inwestycji_tdc
    roi = (zysk_netto_przed_tax / calkowity_koszt_inwestycji_tdc) * 100
    
    # Założenie realizacji projektu w 36 miesięcy (3 lata)
    irr_szacowane = 23.4  # Internal Rate of Return (roczne)

    print(f" >> Wyliczona chłonność (PUM): {szacowany_pum} m2")
    print(f" >> Całkowity koszt projektu (TDC): {calkowity_koszt_inwestycji_tdc:,.2f} PLN")
    print(f" >> Prognozowany przychód: {szacowany_przychod:,.2f} PLN")
    print(f" >> Szacowany zysk przed podatkiem: {zysk_netto_przed_tax:,.2f} PLN")
    print(f" >> ROI: {roi:.2f}% | Szacowane roczne IRR: {irr_szacowane:.2f}%")

    # 3. MATRYCA SCORINGOWA OKAZJI (SCORING MATRIX)
    print("\n[3/4] Wyliczanie scoringu inwestycyjnego na podstawie Matrycy Scoringowej...")
    
    # Wagi dla gruntów deweloperskich z dokumentu architektury:
    # Lokalizacja i dojazd: 20%
    # Cena vs Wartość Rynkowa: 25%
    # Stan prawny (KW, MPZP): 30%
    # Potencjał Yield / PUM: 15%
    # Infrastruktura i media: 10%
    
    oceny_skladnikowe = {
        "lokalizacja": 88,    # Śródmieście Łodzi, świetna komunikacja
        "cena": 96,           # Okazja z likwidacji spółki
        "stan_prawny": 92,     # Prawomocne PnB, czysta KW
        "potencjal_pum": 85,  # Intensywność 1.8 daje świetny PUM
        "media": 90           # Wszystkie media miejskie w drodze
    }
    
    scoring_finalny = (
        0.20 * oceny_skladnikowe["lokalizacja"] +
        0.25 * oceny_skladnikowe["cena"] +
        0.30 * oceny_skladnikowe["stan_prawny"] +
        0.15 * oceny_skladnikowe["potencjal_pum"] +
        0.10 * oceny_skladnikowe["media"]
    )
    
    print(f" >> Finalny Scoring Inwestycyjny gruntu: {scoring_finalny:.2f} / 100 punktów")

    # 4. GENEROWANIE RAPORTU HTML (LUXURY REPORT BUILDER)
    print("\n[4/4] Budowanie luksusowego raportu inwestycyjnego (HTML)...")
    
    html_content = f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RAPORT INWESTYCYJNY OFF-MARKET: ŁÓDŹ - ŚRÓDMIEŚCIE</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
    <style>
        :root {{
            --onyx-black: #0B0F19;
            --slate-grey: #1E293B;
            --emerald-green: #022c22;
            --emerald-light: #064e3b;
            --gold: #D4AF37;
            --gold-hover: #B5952F;
            --white: #F8FAFC;
            --text-muted: #94A3B8;
        }}
        
        body {{
            background-color: var(--onyx-black);
            color: var(--white);
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }}

        header {{
            background: linear-gradient(180deg, var(--emerald-green) 0%, var(--onyx-black) 100%);
            border-bottom: 1px solid rgba(212, 175, 55, 0.2);
            padding: 60px 40px;
            text-align: center;
        }}

        .brand-subtitle {{
            font-family: 'Inter', sans-serif;
            color: var(--gold);
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 3px;
            font-weight: 600;
            margin-bottom: 15px;
        }}

        h1 {{
            font-family: 'Playfair Display', serif;
            font-size: 36px;
            font-weight: 400;
            margin: 0 0 20px 0;
            letter-spacing: 1px;
            color: var(--white);
        }}

        .status-badge {{
            display: inline-block;
            background-color: rgba(212, 175, 55, 0.15);
            color: var(--gold);
            border: 1px solid rgba(212, 175, 55, 0.3);
            padding: 6px 16px;
            border-radius: 30px;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
        }}

        .container {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 40px 20px;
        }}

        .grid-3 {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
            margin-bottom: 40px;
        }}

        /* LUKSUSOWE KARTY METRYK */
        .kpi-card {{
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s ease, border-color 0.3s ease;
        }}

        .kpi-card:hover {{
            transform: translateY(-4px);
            border-color: rgba(212, 175, 55, 0.2);
        }}

        .kpi-title {{
            color: var(--text-muted);
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 10px;
            font-weight: 500;
        }}

        .kpi-val {{
            font-size: 28px;
            font-weight: 700;
            color: var(--white);
            font-family: 'Playfair Display', serif;
        }}

        .kpi-val.gold {{
            color: var(--gold);
            text-shadow: 0 0 10px rgba(212, 175, 55, 0.2);
        }}

        .kpi-desc {{
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 8px;
        }}

        /* SEKCJE SZCZEGÓŁOWE */
        .section-card {{
            background: rgba(30, 41, 59, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.03);
            border-radius: 20px;
            padding: 35px;
            margin-bottom: 40px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.1);
        }}

        .section-title {{
            font-family: 'Playfair Display', serif;
            font-size: 22px;
            border-bottom: 1px solid rgba(212, 175, 55, 0.2);
            padding-bottom: 12px;
            margin-top: 0;
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .section-title span {{
            color: var(--gold);
            font-size: 14px;
            font-family: 'Inter', sans-serif;
            font-weight: 500;
        }}

        /* TABELA PARAMETRÓW */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }}

        th, td {{
            padding: 12px 16px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 13.5px;
        }}

        th {{
            color: var(--text-muted);
            font-weight: 500;
            text-transform: uppercase;
            font-size: 11px;
            letter-spacing: 1px;
        }}

        td.bold {{
            font-weight: 600;
            color: var(--white);
        }}

        td.gold {{
            color: var(--gold);
            font-weight: 600;
        }}

        /* DUE DILIGENCE GAPS */
        .gap-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}

        .gap-item {{
            display: flex;
            align-items: flex-start;
            gap: 12px;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
            font-size: 13px;
        }}

        .gap-item::before {{
            content: '⚠️';
            font-size: 14px;
        }}

        .gap-title {{
            font-weight: 600;
            color: #EF4444;
            margin-bottom: 3px;
        }}

        .gap-desc {{
            color: var(--text-muted);
        }}

        /* CTA BUTTON */
        .cta-container {{
            text-align: center;
            margin: 60px 0;
        }}

        .cta-btn {{
            display: inline-block;
            background: linear-gradient(135deg, var(--gold) 0%, var(--gold-hover) 100%);
            color: var(--onyx-black);
            font-weight: 600;
            font-size: 14px;
            letter-spacing: 1px;
            text-transform: uppercase;
            text-decoration: none;
            padding: 18px 40px;
            border-radius: 40px;
            box-shadow: 0 10px 30px rgba(212, 175, 55, 0.3);
            transition: all 0.3s ease;
        }}

        .cta-btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(212, 175, 55, 0.45);
        }}

        footer {{
            text-align: center;
            padding: 40px;
            color: var(--text-muted);
            font-size: 11px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            letter-spacing: 1px;
        }}
    </style>
</head>
<body>

    <header>
        <div class="brand-subtitle">Holistyczny Broker — Deal Sourcing Intelligence</div>
        <h1>Raport Inwestycyjny Off-Market</h1>
        <div class="status-badge">Kwalifikacja: Klasa A+ (Scoring {scoring_finalny:.1f}%)</div>
    </header>

    <div class="container">

        <!-- GRID 3: GŁÓWNE KPI -->
        <div class="grid-3">
            <div class="kpi-card">
                <div class="kpi-title">Finalny Scoring Terenu</div>
                <div class="kpi-val gold">{scoring_finalny:.2f} / 100</div>
                <div class="kpi-desc">Wysoka ocena wynikająca z posiadania prawomocnego pozwolenia na budowę (PnB) oraz wolnej od roszczeń Księgi Wieczystej.</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Szacowany PUM (Mieszkalny)</div>
                <div class="kpi-val">{szacowany_pum:,} m²</div>
                <div class="kpi-desc">Wyliczony przy intensywności zabudowy 1.8 z MPZP (MW/U) z uwzględnieniem 82% efektywności sprawności rzutu.</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Prognozowana Rentowność (ROI)</div>
                <div class="kpi-val gold">{roi:.1f}%</div>
                <div class="kpi-desc">Prognozowany zysk z przedsięwzięcia: <strong>{zysk_netto_przed_tax:,.2f} PLN</strong> przy szacowanym rocznym <strong>IRR {irr_szacowane}%</strong> (cykl 3-letni).</div>
            </div>
        </div>

        <!-- SPECYFIKACJA GEOPLANISTYCZNA -->
        <div class="section-card">
            <div class="section-title">
                Charakterystyka Geoplanistyczna Działki
                <span>ID: {mock_uldk_geoportal["identyfikator_dzialki"]}</span>
            </div>
            <table>
                <thead>
                    <tr>
                        <th style="width: 35%;">Parametr</th>
                        <th>Wartość z rejestrów (ULDK / RWDZ)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Numer ewidencyjny gruntów</td>
                        <td class="bold">Działki {mock_rwdz_data["dzialki"]} (Obręb S-22 Śródmieście)</td>
                    </tr>
                    <tr>
                        <td>Powierzchnia geometryczna</td>
                        <td class="bold">{powierzchnia_dzialki:,} m²</td>
                    </tr>
                    <tr>
                        <td>Status MPZP</td>
                        <td class="bold">Uchwalony (Symbol: {mock_uldk_geoportal["mpzp_symbol"]})</td>
                    </tr>
                    <tr>
                        <td>Przeznaczenie w planie</td>
                        <td class="bold">{mock_uldk_geoportal["mpzp_przeznaczenie"]}</td>
                    </tr>
                    <tr>
                        <td>Maksymalna intensywność zabudowy</td>
                        <td class="bold">{intensywnosc}</td>
                    </tr>
                    <tr>
                        <td>Dostępność mediów miejskich</td>
                        <td class="gold">{", ".join(mock_uldk_geoportal["media_available" if "media_available" in mock_uldk_geoportal else "media_available" if "media_available" in mock_uldk_geoportal else "media_dostepne"])}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- SPECYFIKACJA FINANSOWA (INVESTMENT MEMORANDUM DCF) -->
        <div class="section-card">
            <div class="section-title">
                Szybka Kalkulacja Kosztów & Przychodów (DCF Model)
                <span>Waluta: PLN</span>
            </div>
            <table>
                <thead>
                    <tr>
                        <th style="width: 50%;">Pozycja Budżetowa</th>
                        <th style="text-align: right;">Kwota</th>
                        <th style="text-align: right; width: 20%;">Wskaźnik / m² PUM</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Koszt zakupu gruntu (off-market)</td>
                        <td class="bold" style="text-align: right;">{cena_gruntu:,.2f}</td>
                        <td style="text-align: right; color: var(--text-muted); font-size: 12px;">{(cena_gruntu/szacowany_pum):,.2f}</td>
                    </tr>
                    <tr>
                        <td>Koszt budowy (generalne wykonawstwo - stan deweloperski)</td>
                        <td class="bold" style="text-align: right;">{koszt_budowy_razem:,.2f}</td>
                        <td style="text-align: right; color: var(--text-muted); font-size: 12px;">{koszt_budowy_m2_pum:,.2f}</td>
                    </tr>
                    <tr>
                        <td>Koszty miękkie (nadzór, projekty, przyłącza miejskie, marketing)</td>
                        <td class="bold" style="text-align: right;">{koszty_soft:,.2f}</td>
                        <td style="text-align: right; color: var(--text-muted); font-size: 12px;">{(koszty_soft/szacowany_pum):,.2f}</td>
                    </tr>
                    <tr style="background: rgba(255,255,255,0.02);">
                        <td class="gold">Całkowity Koszt Inwestycji (TDC)</td>
                        <td class="gold" style="text-align: right;">{calkowity_koszt_inwestycji_tdc:,.2f}</td>
                        <td class="gold" style="text-align: right; font-size: 12px;">{(calkowity_koszt_inwestycji_tdc/szacowany_pum):,.2f}</td>
                    </tr>
                    <tr style="background: rgba(212, 175, 55, 0.05);">
                        <td class="gold">Prognozowany Przychód ze Sprzedaży PUM</td>
                        <td class="gold" style="text-align: right;">{szacowany_przychod:,.2f}</td>
                        <td class="gold" style="text-align: right; font-size: 12px;">{cena_sprzedazy_m2_pum:,.2f}</td>
                    </tr>
                    <tr style="border-top: 2px solid var(--gold);">
                        <td style="font-weight: 700; text-transform: uppercase;">Prognozowany Zysk Netto (Przed Tax)</td>
                        <td style="font-weight: 700; text-align: right; font-size: 18px; color: #10B981;">{zysk_netto_przed_tax:,.2f}</td>
                        <td class="gold" style="text-align: right; font-weight: 700; font-size: 16px;">{roi:.1f}% ROI</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- MATRYCA SCORINGOWA OKAZJI -->
        <div class="section-card">
            <div class="section-title">
                Rozkład Wag Matrycy Scoringowej (Procedura 13)
                <span>Wyliczono ważono</span>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Kryterium Oceny</th>
                        <th style="text-align: center;">Waga Kryterium</th>
                        <th style="text-align: center;">Ocena Cząstkowa</th>
                        <th style="text-align: right;">Wynik Ważony</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="bold">Stan Prawny (KW, Księga wieczysta, brak hipoteki)</td>
                        <td style="text-align: center;">30%</td>
                        <td style="text-align: center;" class="bold">92 / 100</td>
                        <td class="gold" style="text-align: right;">{(0.30 * oceny_skladnikowe["stan_prawny"]):.2f} pkt</td>
                    </tr>
                    <tr>
                        <td class="bold">Cena vs Wartość Rynkowa (Wycena likwidacyjna)</td>
                        <td style="text-align: center;">25%</td>
                        <td style="text-align: center;" class="bold">96 / 100</td>
                        <td class="gold" style="text-align: right;">{(0.25 * oceny_skladnikowe["cena"]):.2f} pkt</td>
                    </tr>
                    <tr>
                        <td class="bold">Lokalizacja i dojazd (Śródmieście, Łódź)</td>
                        <td style="text-align: center;">20%</td>
                        <td style="text-align: center;" class="bold">88 / 100</td>
                        <td class="gold" style="text-align: right;">{(0.20 * oceny_skladnikowe["lokalizacja"]):.2f} pkt</td>
                    </tr>
                    <tr>
                        <td class="bold">Potencjał Yield / PUM (Wysoki wskaźnik intensywności 1.8)</td>
                        <td style="text-align: center;">15%</td>
                        <td style="text-align: center;" class="bold">85 / 100</td>
                        <td class="gold" style="text-align: right;">{(0.15 * oceny_skladnikowe["potencjal_pum"]):.2f} pkt</td>
                    </tr>
                    <tr>
                        <td class="bold">Infrastruktura i media miejskie (Dostępne w drodze)</td>
                        <td style="text-align: center;">10%</td>
                        <td style="text-align: center;" class="bold">90 / 100</td>
                        <td class="gold" style="text-align: right;">{(0.10 * oceny_skladnikowe["media"]):.2f} pkt</td>
                    </tr>
                    <tr style="background: rgba(212, 175, 55, 0.08); border-top: 1px solid var(--gold);">
                        <td style="font-weight: 700; text-transform: uppercase;">Suma Ważona (Ocena Końcowa)</td>
                        <td style="text-align: center; font-weight: 700;">100%</td>
                        <td style="text-align: center; font-weight: 700;">—</td>
                        <td class="gold" style="text-align: right; font-size: 16px; font-weight: 700;">{scoring_finalny:.2f} / 100 pkt</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- SEKCJA: DUE DILIGENCE GAPS -->
        <div class="section-card">
            <div class="section-title">
                Skaner Due Diligence Gaps (Procedura 13C)
                <span>Wymaga weryfikacji przed złożeniem wiążącej oferty</span>
            </div>
            <ul class="gap-list">
                <li class="gap-item">
                    <div>
                        <div class="gap-title">Weryfikacja Przyłączeń Deszczowych (Zlewnia miejska)</div>
                        <div class="gap-desc">MPZP stawia rygorystyczne warunki odprowadzania deszczówki. Konieczne jest pozyskanie warunków technicznych przyłączenia osadnika deszczowego oraz upewnienie się, czy sieć deszczowa ma wolne moce przerobowe w tym kwartale.</div>
                    </div>
                </li>
                <li class="gap-item">
                    <div>
                        <div class="gap-title">Zgoda Syndyka Masy Upadłościowej / Likwidatora</div>
                        <div class="gap-desc">Z uwagi na dopisek "w likwidacji" przy inwestorze w KRS, finalna umowa sprzedaży gruntów wymaga prawomocnej zgody zgromadzenia wspólników lub sędziego-komisarza. Należy natychmiast zweryfikować status postępowania likwidacyjnego.</div>
                    </div>
                </li>
                <li class="gap-item">
                    <div>
                        <div class="gap-title">Potwierdzenie Bezpieczeństwa Ekologicznego (Badanie Gruntu)</div>
                        <div class="gap-desc">Teren historycznie znajdował się w pobliżu dawnych zakładów włókienniczych. Rekomendujemy wykonanie odwiertów geologicznych i badań fizykochemicznych na obecność zanieczyszczeń gruntowo-wodnych (metale ciężkie) w celu wyeliminowania ryzyk rekultywacyjnych.</div>
                    </div>
                </li>
            </ul>
        </div>

        <!-- CTA BUTTON -->
        <div class="cta-container">
            <a href="https://wa.me/48730882961" target="_blank" class="cta-btn">
                📩 Połącz ze Strategiem & Pobierz pełne IM w PDF
            </a>
        </div>

    </div>

    <footer>
        <p>Holistyczny Broker Share Co. | Poufny dokument analityczny B2B. Wszystkie dane objęte klauzulą NDA.</p>
        <p>© 2026 Holistyczny Broker. Wszystkie prawa zastrzeżone.</p>
    </footer>

</body>
</html>
"""
    
    output_path = os.path.join("strona www", "raport_inwestycyjny_dzialka.html")
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"\n >> [SUKCES] Generowanie raportu zakończone! Plik zapisany w: {output_path}")
        print("=" * 60)
    except Exception as e:
        print(f" >> [BŁĄD] Nie udało się zapisać raportu w {output_path}: {e}")
        print("=" * 60)

if __name__ == "__main__":
    run_deal_sourcing_simulation()
