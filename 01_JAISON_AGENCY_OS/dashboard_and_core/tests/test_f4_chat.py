# -*- coding: utf-8 -*-
from fastapi.testclient import TestClient
from webhook_api import app

client = TestClient(app)

def test_chat_endpoint_success():
    """
    Testuje poprawne wywołanie endpointu /api/chat z payloadem i oczekuje kodu 200 OK
    oraz obecności 'response' w JSONie.
    """
    payload = {
        "messages": [
            {"role": "user", "text": "Ile kosztuje wdrożenie automatyzacji w waszej agencji?"}
        ]
    }
    
    response = client.post("/api/chat", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0
    # Oczekujemy, że J(AI)SON poda konkretną cenę pakietów
    assert "3 900" in data["response"] or "7 900" in data["response"] or "PLN" in data["response"]

def test_chat_endpoint_empty_payload():
    """
    Testuje obsługę błędnego (pustego) payloadu przez endpoint /api/chat.
    Powinno rzucić 422 Unprocessable Entity z powodu walidacji Pydantic.
    """
    response = client.post("/api/chat", json={})
    assert response.status_code == 422
