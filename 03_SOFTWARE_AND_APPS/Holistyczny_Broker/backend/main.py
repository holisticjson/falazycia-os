import os
import httpx
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="Holistyczny Broker - Lead API Backend", 
    description="Centralny, bezpieczny endpoint dla leadów w architekturze Zero-Data-Leakage.",
    version="2.0.0"
)

# Konfiguracja CORS (Cross-Origin Resource Sharing)
# Pozwala przeglądarkom użytkowników na bezpieczne wysyłanie zapytań ze strony na Cloud Run
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # W produkcji można ograniczyć do ["https://holistycznybroker.pl", "https://www.holistycznybroker.pl"]
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

class LeadPayload(BaseModel):
    project: str = Field(default="broker")
    name: str
    contact: str
    budget: Optional[str] = None
    investment_type: Optional[str] = None
    source: str

@app.post("/api/lead", status_code=status.HTTP_201_CREATED)
async def create_lead(payload: LeadPayload):
    """
    Odbiera dane formularza w formacie JSON i bezpiecznie przekazuje je dalej.
    Brak jakichkolwiek kluczy dostępu i tokenów na froncie zabezpiecza nas przed wyciekiem.
    """
    lead_data = payload.dict()
    print(f"[LEAD RECEIVER] Otrzymano nowego leada: {lead_data}")
    
    # Adres centralnego webhooka (np. Make.com, n8n lub system CRM) pobierany bezpiecznie z konfiguracji chmurowej
    webhook_url = os.getenv("LEAD_WEBHOOK_URL")
    
    if webhook_url:
        print(f"[LEAD SENDER] Przekazywanie leada do centralnego n8n/Make: {webhook_url}")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(webhook_url, json=lead_data, timeout=10.0)
                if response.status_code in [200, 201, 202]:
                    print("[LEAD SENDER] Lead pomyślnie dostarczony do systemu CRM.")
                    return {"status": "success", "message": "Lead received and synchronized with CRM."}
                else:
                    print(f"[LEAD SENDER] CRM zwrócił nieoczekiwany kod statusu: {response.status_code}")
                    # Zwracamy success dla frontendu, żeby nie blokować użytkownika na stronie
                    return {"status": "success", "message": "Lead received locally (CRM sync pending)."}
        except Exception as e:
            print(f"[LEAD SENDER] Wyjątek podczas wysyłania do CRM: {str(e)}")
            return {"status": "success", "message": "Lead received locally (CRM connection timeout)."}
    
    # Fallback, jeśli webhook nie jest jeszcze podłączony pod zmienną środowiskową
    print("[LEAD SENDER] Brak skonfigurowanej zmiennej LEAD_WEBHOOK_URL. Lead zapisany wyłącznie w logach kontenera.")
    return {"status": "success", "message": "Lead received locally on server (no webhook configured)."}

@app.get("/health")
def health_check():
    """
    Endpoint używany przez Google Cloud Run do automatycznego monitorowania żywotności kontenera (Liveness Probe).
    """
    return {"status": "healthy", "service": "holistyczny-broker-backend"}

# Montowanie obsługi plików statycznych na samym końcu, aby obsłużyć cały frontend pod ścieżką /
# Parametr html=True sprawia, że FastAPI automatycznie serwuje index.html jako główną stronę "/"
# oraz poprawnie mapuje ścieżki do innych plików HTML (np. /blog -> /blog.html)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
