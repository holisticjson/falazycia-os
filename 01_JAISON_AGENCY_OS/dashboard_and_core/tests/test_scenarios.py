import pytest
from unittest.mock import patch, MagicMock
import os
import importlib
import shutil
from fastapi.testclient import TestClient
from streamlit.testing.v1 import AppTest

# Dynamic imports
knowledge_module = importlib.import_module("01_src.knowledge")
query_dual_knowledge_base = knowledge_module.query_dual_knowledge_base
save_idea_to_obsidian_and_gcs = knowledge_module.save_idea_to_obsidian_and_gcs

from webhook_api import app as webhook_app
from brain_dump_api import app as brain_dump_app

webhook_client = TestClient(webhook_app)
bd_client = TestClient(brain_dump_app)

@pytest.fixture
def temp_obsidian_dir(monkeypatch):
    import tempfile
    
    temp_dir = tempfile.mkdtemp()
    monkeypatch.setenv("OBSIDIAN_VAULT_PATH", temp_dir)
    
    # Patch knowledge module OBSIDIAN_DIR
    old_dir = knowledge_module.OBSIDIAN_DIR
    knowledge_module.OBSIDIAN_DIR = temp_dir
    
    # Patch brain_dump_api INBOX_DIR
    import brain_dump_api
    old_inbox = brain_dump_api.INBOX_DIR
    brain_dump_api.INBOX_DIR = os.path.join(temp_dir, "Inbox")
    
    yield temp_dir
    
    knowledge_module.OBSIDIAN_DIR = old_dir
    brain_dump_api.INBOX_DIR = old_inbox
    shutil.rmtree(temp_dir)

@pytest.fixture(autouse=True)
def clean_env():
    # Ensure system environment variables are cleaned before each test
    with patch.dict(os.environ, {}, clear=False):
        if "SYSTEME_IO_WEBHOOK_URL" in os.environ:
            del os.environ["SYSTEME_IO_WEBHOOK_URL"]
        if "SYSTEME_IO_API_KEY" in os.environ:
            del os.environ["SYSTEME_IO_API_KEY"]
        yield

# TC-31: E2E Webhook: Lead received -> saved to Google Sheets -> forwarded to Systeme.io webhook successfully
@patch("requests.post")
@patch("webhook_api.get_sheets_service")
def test_tc31_e2e_lead_webhook_flow(mock_sheets_get, mock_post, monkeypatch):
    monkeypatch.setenv("SYSTEME_IO_WEBHOOK_URL", "https://hook.systeme.io/e2e")
    
    # Mock sheets service append chain
    mock_service = MagicMock()
    mock_sheets_get.return_value = mock_service
    mock_service.spreadsheets.return_value.values.return_value.append.return_value.execute.return_value = {
        "updates": {"updatedCells": 7}
    }
    
    mock_post.return_value.status_code = 200
    
    payload = {
        "project": "broker",
        "name": "E2E Lead",
        "contact": "e2e@example.com",
        "budget": "1M",
        "investment_type": "commercial"
    }
    
    response = webhook_client.post("/api/lead", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    # Verify sheets called
    mock_sheets_get.assert_called_once()
    
    # Verify forwarder called
    mock_post.assert_called_once()
    assert mock_post.call_args[0][0] == "https://hook.systeme.io/e2e"

# TC-32: E2E Knowledge Sync: Save a note via Streamlit knowledge flow -> verify it is written to the local vault -> execute a RAG query containing "notatki" to retrieve it
@patch("google.cloud.storage.Client")
def test_tc32_e2e_knowledge_sync_flow(mock_gcs_client, temp_obsidian_dir):
    # Mock GCS upload to succeed
    mock_bucket = mock_gcs_client.return_value.bucket
    mock_blob = mock_bucket.return_value.blob
    
    # Call save_idea
    res_save = save_idea_to_obsidian_and_gcs("ADHD Focus Strategy", "Use pomodoro timers and clean space", "Streamlit Flow")
    assert res_save["status"] == "success"
    
    # Query with 'notatki' keywords to trigger local search
    res_query = query_dual_knowledge_base("notatki o ADHD pomodoro")
    assert res_query["source"] == "brain_dump"
    assert res_query["matches_count"] == 1
    assert "ADHD Focus Strategy" in res_query["result"]

# TC-33: GCS Sync resilience: Save a note -> mock GCS upload failure -> verify note is still saved locally and function returns success with warning
@patch("google.cloud.storage.Client")
def test_tc33_gcs_sync_resilience(mock_gcs_client, temp_obsidian_dir):
    # Force GCS to fail (e.g. SSL issue or auth issue)
    from google.auth.exceptions import DefaultCredentialsError
    mock_gcs_client.side_effect = DefaultCredentialsError("Missing credentials")
    
    # Save note
    res_save = save_idea_to_obsidian_and_gcs("Local Resilient Note", "This should be saved even without GCP", "Streamlit")
    assert res_save["status"] == "success"
    assert "BRAK AUTORYZACJI GCP" in res_save["message"]
    
    # Check that file actually exists in the local temp directory
    files = os.listdir(temp_obsidian_dir)
    assert len(files) == 1
    assert "Local_Resilient_Note" in files[0]

# TC-34: Malformed webhook request fails immediately before contacting Sheets or Systeme.io
@patch("requests.post")
@patch("webhook_api.get_sheets_service")
def test_tc34_malformed_webhook_fails_early(mock_sheets_get, mock_post):
    payload = {
        "project": "invalid_structure_no_name"
    }
    response = webhook_client.post("/api/lead", json=payload)
    assert response.status_code == 422
    
    # Ensure sheets and systeme.io were not contacted
    mock_sheets_get.assert_not_called()
    mock_post.assert_not_called()

# TC-35: Save a Brain Dump via REST API (/api/dump) -> note created in Inbox -> query with "inbox" retrieves the note content
def test_tc35_brain_dump_api_to_rag(temp_obsidian_dir):
    payload = {
        "content": "This is a raw brainstorm idea for ADHD app",
        "tags": ["adhd", "app"]
    }
    response = bd_client.post("/api/dump", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    # Query with 'inbox' keyword
    res = query_dual_knowledge_base("inbox adhd app")
    assert res["source"] == "brain_dump"
    assert res["matches_count"] == 1
    assert "raw brainstorm idea" in res["result"]

# TC-36: Cloud routing fallback: RAG search directed to GCS with mock SSL error is caught and converted to a user-friendly error message
@patch("google.auth.default")
@patch("requests.post")
def test_tc36_cloud_ssl_error_fallback(mock_post, mock_auth):
    # Mock Auth success
    mock_creds = MagicMock()
    mock_creds.token = "fake-token"
    mock_auth.return_value = (mock_creds, "project-id")
    
    # Mock requests.post to raise SSLError
    import requests
    mock_post.side_effect = requests.exceptions.SSLError("SSL verification failed")
    
    res = query_dual_knowledge_base("Tomasz Duda info")
    assert res["source"] == "gcs"
    assert "Problem z Certyfikatem SSL" in res["result"]

# TC-37: Tryb "One Thing" UI state change doesn't interfere with or delete other session state keys
def test_tc37_one_thing_state_isolation():
    at = AppTest.from_file("app.py")
    at.run()
    at.session_state["some_other_key"] = "important_data"
    
    # Change One Thing
    one_thing_input = [inp for inp in at.text_input if "Moje jedyne zadanie" in inp.label][0]
    one_thing_input.set_value("Nowe zadanie").run()
    
    assert at.session_state["some_other_key"] == "important_data"
    assert at.session_state.one_thing == "Nowe zadanie"

# TC-38: Comprehensive E2E System Scenario: User sets "One Thing", submits a Lead, saves a local note, runs RAG search for that note
@patch("requests.post")
@patch("webhook_api.get_sheets_service")
@patch("google.cloud.storage.Client")
def test_tc38_comprehensive_e2e_scenario(mock_gcs_client, mock_sheets_get, mock_post, temp_obsidian_dir, monkeypatch):
    monkeypatch.setenv("SYSTEME_IO_WEBHOOK_URL", "https://hook.systeme.io/e2e")
    
    # 1. UI: User sets "One Thing"
    at = AppTest.from_file("app.py")
    at.run()
    one_thing_input = [inp for inp in at.text_input if "Moje jedyne zadanie" in inp.label][0]
    one_thing_input.set_value("E2E Integration Test").run()
    assert at.session_state.one_thing == "E2E Integration Test"
    
    # 2. Webhook: Submit Lead
    mock_service = MagicMock()
    mock_sheets_get.return_value = mock_service
    mock_service.spreadsheets.return_value.values.return_value.append.return_value.execute.return_value = {
        "updates": {"updatedCells": 7}
    }
    mock_post.return_value.status_code = 200
    
    lead_payload = {
        "project": "jason",
        "name": "Integration Lead",
        "contact": "integration@test.com",
        "industry": "Marketing",
        "problem": "Automation"
    }
    lead_res = webhook_client.post("/api/lead", json=lead_payload)
    assert lead_res.status_code == 200
    
    # 3. Brain Dump API: Dump a note
    dump_payload = {
        "content": "Secret credentials for the integration test",
        "tags": ["secret"]
    }
    dump_res = bd_client.post("/api/dump", json=dump_payload)
    assert dump_res.status_code == 200
    
    # 4. RAG: Run query matching the dump
    rag_res = query_dual_knowledge_base("notatki secret credentials")
    assert rag_res["source"] == "brain_dump"
    assert rag_res["matches_count"] == 1
    assert "Secret credentials" in rag_res["result"]
