import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os

from webhook_api import app

client = TestClient(app)

@pytest.fixture
def mock_sheets_service():
    with patch("webhook_api.get_sheets_service") as mock_get:
        mock_service = MagicMock()
        mock_get.return_value = mock_service
        # Mock sheets append API chain
        mock_append = mock_service.spreadsheets.return_value.values.return_value.append
        mock_append.return_value.execute.return_value = {
            "updates": {
                "updatedCells": 7
            }
        }
        yield mock_service

@pytest.fixture(autouse=True)
def clean_env():
    # Ensure system environment variables are cleaned before each test
    with patch.dict(os.environ, {}, clear=False):
        if "SYSTEME_IO_WEBHOOK_URL" in os.environ:
            del os.environ["SYSTEME_IO_WEBHOOK_URL"]
        if "SYSTEME_IO_API_KEY" in os.environ:
            del os.environ["SYSTEME_IO_API_KEY"]
        yield

# TC-11: Submitting lead with project "broker" writes to "Leady_Broker!A:G"
def test_tc11_broker_lead_sheets_range(mock_sheets_service):
    payload = {
        "project": "broker",
        "name": "Jan Kowalski",
        "contact": "jan@kowalski.pl",
        "budget": "500k",
        "investment_type": "mieszkanie",
        "source": "Landing Page"
    }
    response = client.post("/api/lead", json=payload)
    assert response.status_code == 200
    
    # Check sheet range was correct
    append_mock = mock_sheets_service.spreadsheets.return_value.values.return_value.append
    kwargs = append_mock.call_args[1]
    assert kwargs["range"] == "Leady_Broker!A:G"

# TC-12: Submitting lead with project "jason" writes to "Leady_Jason_B2B!A:G"
def test_tc12_jason_lead_sheets_range(mock_sheets_service):
    payload = {
        "project": "jason",
        "name": "Maria Nowak",
        "contact": "maria@nowak.pl",
        "industry": "IT",
        "problem": "Brak klientów",
        "source": "Cold Mail"
    }
    response = client.post("/api/lead", json=payload)
    assert response.status_code == 200
    
    # Check sheet range was correct
    append_mock = mock_sheets_service.spreadsheets.return_value.values.return_value.append
    kwargs = append_mock.call_args[1]
    assert kwargs["range"] == "Leady_Jason_B2B!A:G"

# TC-13: Missing required fields in Lead payload raises 422 ValidationError
def test_tc13_missing_required_fields(mock_sheets_service):
    # 'project' and 'name' are missing, contact is present
    payload = {
        "contact": "test@example.com"
    }
    response = client.post("/api/lead", json=payload)
    assert response.status_code == 422

# TC-14: Submitting lead with empty contact string (Pydantic validation checks)
def test_tc14_empty_contact_field(mock_sheets_service):
    payload = {
        "project": "jason",
        "name": "Anna",
        "contact": "" # empty contact
    }
    response = client.post("/api/lead", json=payload)
    # Pydantic allows empty string for string field by default, so it passes FastAPI validation but we verify behavior
    assert response.status_code == 200

# TC-15: Forwarding when only SYSTEME_IO_WEBHOOK_URL is set
@patch("requests.post")
def test_tc15_forward_webhook_only(mock_post, mock_sheets_service, monkeypatch):
    monkeypatch.setenv("SYSTEME_IO_WEBHOOK_URL", "https://hook.systeme.io/lead123")
    
    payload = {
        "project": "broker",
        "name": "Adam",
        "contact": "adam@gmail.com",
        "source": "Facebook"
    }
    mock_post.return_value.status_code = 200
    
    response = client.post("/api/lead", json=payload)
    assert response.status_code == 200
    
    # Verify requests.post was called once (for the webhook)
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert args[0] == "https://hook.systeme.io/lead123"
    assert kwargs["json"]["name"] == "Adam"

# TC-16: Forwarding when only SYSTEME_IO_API_KEY is set
@patch("requests.post")
def test_tc16_forward_api_only(mock_post, mock_sheets_service, monkeypatch):
    monkeypatch.setenv("SYSTEME_IO_API_KEY", "secret-api-key")
    
    payload = {
        "project": "jason",
        "name": "Ewa",
        "contact": "ewa@gmail.com",
        "source": "Instagram"
    }
    mock_post.return_value.status_code = 201
    
    response = client.post("/api/lead", json=payload)
    assert response.status_code == 200
    
    # Verify requests.post was called once (for the API)
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert args[0] == "https://api.systeme.io/api/v2/contacts"
    assert kwargs["headers"]["Authorization"] == "Bearer secret-api-key"

# TC-17: Forwarding when BOTH SYSTEME_IO_WEBHOOK_URL and SYSTEME_IO_API_KEY are set
@patch("requests.post")
def test_tc17_forward_both(mock_post, mock_sheets_service, monkeypatch):
    monkeypatch.setenv("SYSTEME_IO_WEBHOOK_URL", "https://hook.systeme.io/lead123")
    monkeypatch.setenv("SYSTEME_IO_API_KEY", "secret-api-key")
    
    payload = {
        "project": "jason",
        "name": "Piotr",
        "contact": "piotr@gmail.com",
        "source": "API"
    }
    mock_post.return_value.status_code = 200
    
    response = client.post("/api/lead", json=payload)
    assert response.status_code == 200
    
    # Verify requests.post was called twice (once for webhook, once for API)
    assert mock_post.call_count == 2
    called_urls = [call[0][0] for call in mock_post.call_args_list]
    assert "https://hook.systeme.io/lead123" in called_urls
    assert "https://api.systeme.io/api/v2/contacts" in called_urls

# TC-18: Forwarding when NEITHER is set
@patch("requests.post")
def test_tc18_forward_neither(mock_post, mock_sheets_service):
    payload = {
        "project": "jason",
        "name": "Olek",
        "contact": "olek@gmail.com",
        "source": "Referral"
    }
    response = client.post("/api/lead", json=payload)
    assert response.status_code == 200
    # Verify no post requests were sent
    mock_post.assert_not_called()

# TC-19: Webhook works successfully under normal mock conditions
def test_tc19_webhook_success_flow(mock_sheets_service):
    payload = {
        "project": "broker",
        "name": "Stefan",
        "contact": "stefan@wp.pl"
    }
    response = client.post("/api/lead", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["updatedCells"] == 7

# TC-20: Webhook handles Google Sheets API errors gracefully by using non-blocking fallback and returning 200 Success
def test_tc20_sheets_api_failure_graceful(mock_sheets_service):
    # Make append execute call raise an Exception
    append_mock = mock_sheets_service.spreadsheets.return_value.values.return_value.append
    append_mock.return_value.execute.side_effect = Exception("Google API is down")
    
    payload = {
        "project": "broker",
        "name": "Kryspin",
        "contact": "kryspin@o2.pl"
    }
    response = client.post("/api/lead", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert response.json()["sheets_synced"] is False
    assert response.json()["updatedCells"] == 0
