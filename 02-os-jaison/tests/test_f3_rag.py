import pytest
from unittest.mock import patch, MagicMock
import os
import importlib

# Dynamic import because of digit in folder name "01_src"
knowledge_module = importlib.import_module("01_src.knowledge")
query_dual_knowledge_base = knowledge_module.query_dual_knowledge_base

@pytest.fixture
def temp_obsidian_dir(monkeypatch):
    import tempfile
    import shutil
    
    # Create temp directory
    temp_dir = tempfile.mkdtemp()
    monkeypatch.setenv("OBSIDIAN_VAULT_PATH", temp_dir)
    
    # Also patch OBSIDIAN_DIR in 01_src.knowledge module
    old_dir = knowledge_module.OBSIDIAN_DIR
    knowledge_module.OBSIDIAN_DIR = temp_dir
    
    yield temp_dir
    
    # Restore and cleanup
    knowledge_module.OBSIDIAN_DIR = old_dir
    shutil.rmtree(temp_dir)

# TC-21: Route query containing "brain dump" to local Obsidian search
def test_tc21_route_brain_dump(temp_obsidian_dir):
    with patch.object(knowledge_module, "query_vertex_ai_search") as mock_search:
        res = query_dual_knowledge_base("Show me my brain dump notes")
        assert res["source"] == "brain_dump"
        assert "Wykryto słowo kluczowe" in res["routing_reason"]
        mock_search.assert_not_called()

# TC-22: Route query containing "notatki" to local Obsidian search
def test_tc22_route_notatki(temp_obsidian_dir):
    with patch.object(knowledge_module, "query_vertex_ai_search") as mock_search:
        res = query_dual_knowledge_base("Moje notatki o systemie")
        assert res["source"] == "brain_dump"
        assert "Wykryto słowo kluczowe" in res["routing_reason"]
        mock_search.assert_not_called()

# TC-23: Route standard query to cloud GCS / Vertex AI search
def test_tc23_route_standard_gcs(temp_obsidian_dir):
    with patch.object(knowledge_module, "query_vertex_ai_search") as mock_search:
        mock_search.return_value = "Vertex AI Search Response"
        res = query_dual_knowledge_base("Kto to jest Tomasz Duda?")
        assert res["source"] == "gcs"
        assert "Kierowanie do chmury" in res["routing_reason"]
        assert res["result"] == "Vertex AI Search Response"
        mock_search.assert_called_once_with("Kto to jest Tomasz Duda?")

# TC-24: Empty query routing
def test_tc24_empty_query_routing(temp_obsidian_dir):
    with patch.object(knowledge_module, "query_vertex_ai_search") as mock_search:
        mock_search.return_value = "Brak wyników"
        res = query_dual_knowledge_base("")
        # Empty string doesn't match brain dump keywords, so routes to GCS
        assert res["source"] == "gcs"
        mock_search.assert_called_once_with("")

# TC-25: Multi-word query with mixed keywords routes correctly
def test_tc25_mixed_keywords_routing(temp_obsidian_dir):
    with patch.object(knowledge_module, "query_vertex_ai_search") as mock_search:
        res = query_dual_knowledge_base("Prywatne pliki i pomysł na SaaS")
        assert res["source"] == "brain_dump"
        mock_search.assert_not_called()

# TC-26: Local Obsidian search when directory is empty/missing returns a friendly message
def test_tc26_local_search_empty_dir(temp_obsidian_dir):
    res = query_dual_knowledge_base("notatki")
    assert res["source"] == "brain_dump"
    assert res["files_searched"] == 0
    assert "Nie znaleziono dopasowań w lokalnym Obsidian Vault" in res["result"]

# TC-27: Local Obsidian search with matching files yields correct filename and preview snippet
def test_tc27_local_search_success_verbatim(temp_obsidian_dir):
    # Write a test markdown file
    note_content = "To jest wazny pomysl o SaaS dla lekarzy."
    file_path = os.path.join(temp_obsidian_dir, "note1.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(note_content)
        
    res = query_dual_knowledge_base("pomysl")
    assert res["source"] == "brain_dump"
    assert res["files_searched"] == 1
    assert res["matches_count"] == 1
    assert "note1.md" in res["result"]
    assert "To jest wazny pomysl" in res["result"]

# TC-28: Local Obsidian search with multiple space-separated keywords matches files with all keywords
def test_tc28_local_search_keywords_fallback(temp_obsidian_dir):
    note_content = "Wątek o ADHD w pracy programisty. Skupienie jest kluczowe."
    file_path = os.path.join(temp_obsidian_dir, "note2.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(note_content)
        
    # Query words are scattered and not in this exact order
    res = query_dual_knowledge_base("notatki ADHD skupienie")
    assert res["source"] == "brain_dump"
    assert res["matches_count"] == 1
    assert "note2.md" in res["result"]

# TC-29: Mock GCS / Vertex AI search returns structured answers and snippets
@patch("requests.post")
@patch("google.auth.default")
def test_tc29_vertex_ai_search_snippets(mock_auth, mock_post):
    # Mock google auth credentials
    mock_creds = MagicMock()
    mock_creds.token = "fake-token"
    mock_auth.return_value = (mock_creds, "project-id")
    
    # Mock discovery engine serving config response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "answer": {
            "answerText": "Tomasz Duda to architekt systemów.",
            "steps": [
                {
                    "actions": [
                        {
                            "observation": {
                                "searchResults": [
                                    {
                                        "snippetInfo": [
                                            {"snippet": "Snippet 1 info <b>highlighted</b>"}
                                        ]
                                    }
                                ]
                            }
                        }
                    ]
                }
            ]
        }
    }
    mock_post.return_value = mock_response
    
    res = query_dual_knowledge_base("Kto to jest Tomasz?")
    assert res["source"] == "gcs"
    assert "Tomasz Duda to architekt" in res["result"]
    # Verify snippets were formatted (b tags replaced by **)
    assert "Snippet 1 info **highlighted**" in res["result"]

# TC-30: GCS / Vertex AI search handles authentication/credentials error gracefully
@patch("google.auth.default")
def test_tc30_vertex_ai_auth_error(mock_auth):
    from google.auth.exceptions import DefaultCredentialsError
    mock_auth.side_effect = DefaultCredentialsError("No credentials")
    
    res = query_dual_knowledge_base("Kto to jest Tomasz?")
    assert res["source"] == "gcs"
    assert "Brak kluczy Google Cloud" in res["result"]
