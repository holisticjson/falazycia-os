"""
================================================================================
  SEATS.AERO API WRAPPER & LIVE SEARCH SERVICE (DLA FALA ŻYCIA AGENT 2.0)
================================================================================
  Pozwala na wykonywanie zapytania w czasie rzeczywistym o dostępność lotów
  za punkty w klasie biznes/pierwszej (Star Alliance, Oneworld, SkyTeam).
================================================================================
"""

import os
import json
import urllib.request
import urllib.parse

SEATS_AERO_API_KEY = os.getenv("SEATS_AERO_API_KEY", "")
BASE_URL = "https://seats.aero/partnerapi"

def search_award_availability(origin, destination, cabin="business", start_date=None, end_date=None):
    """
    Wyszukuje dostępność lotów za punkty przez Seats.aero Partner API.
    
    Parametry:
      - origin: Trzyliterowy kod lotniska wylotu (np. 'WAW', 'VIE', 'FRA', 'MUC')
      - destination: Trzyliterowy kod lotniska docelowego (np. 'TYO', 'BKK', 'DOH', 'JFK')
      - cabin: 'business' | 'first' | 'economy'
      - start_date / end_date: YYYY-MM-DD
    """
    if not SEATS_AERO_API_KEY:
        return {
            "status": "demo_mode",
            "message": "Brak SEATS_AERO_API_KEY w środowisku. Zwracam przykładowy wynik na żywo.",
            "results": [
                {
                    "route": f"{origin} -> {destination}",
                    "date": start_date or "2026-11-14",
                    "airline": "Qatar Airways",
                    "cabin": "Business (Qsuite)",
                    "program": "Qatar Airways Privilege Club (Avios)",
                    "points_required": 75000,
                    "taxes_cash_pln": 1120,
                    "seats_available": 2,
                    "booking_url": f"https://seats.aero/search?origin={origin}&destination={destination}"
                }
            ]
        }

    params = {
        "origin": origin,
        "destination": destination,
        "cabin": cabin
    }
    if start_date: params["start_date"] = start_date
    if end_date: params["end_date"] = end_date

    url = f"{BASE_URL}/search?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Partner-Authorization": SEATS_AERO_API_KEY,
        "Accept": "application/json"
    })

    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "error": str(e)}

if __name__ == "__main__":
    print("🔎 Testowe wywołanie skanera Seats.aero...")
    res = search_award_availability("WAW", "TYO", cabin="business")
    print(json.dumps(res, indent=2, ensure_ascii=False))
