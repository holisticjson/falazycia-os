import os
import json
import urllib.request
import pytest
import shutil
import tempfile
from unittest.mock import patch, MagicMock
from streamlit.testing.v1 import AppTest

# Save original functions to avoid recursion when mocking
original_join = os.path.join

class MockUrllibResponse:
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    def getcode(self):
        return 200
    def read(self):
        return b'{"choices": [{"message": {"content": "Mocked Gemini Response Advice"}}]}'

@pytest.fixture
def temp_burnejko_dir():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def test_akademia_mentoring_empty_burnejko_directory(temp_burnejko_dir):
    """Test that the Akademia.pl Mentoring tab does not crash when scratch/burnejko is empty."""
    orig_join = os.path.join
    with patch("app.os.path.join", side_effect=lambda *args: temp_burnejko_dir if any("burnejko" in str(arg) for arg in args) else orig_join(*args)), \
         patch("app.os.path.exists", side_effect=lambda path: temp_burnejko_dir in str(path) or "scratch" in str(path)):
        at = AppTest.from_file("app.py")
        at.session_state.current_page = "🎯 Akademia.pl Mentoring"
        at.run(timeout=30)
        
        # Verify it runs and doesn't crash
        assert at.session_state.current_page == "🎯 Akademia.pl Mentoring"
        
        # Selectbox should render with no options
        selectboxes = at.selectbox
        prompt_selectbox = [sb for sb in selectboxes if "Wybierz" in sb.label][0]
        assert prompt_selectbox.options == []

def test_akademia_mentoring_file_read_error(temp_burnejko_dir):
    """Test that the Akademia.pl Mentoring tab displays an error when a file fails to read."""
    file_path = os.path.join(temp_burnejko_dir, "test_prompt.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Some test prompt content")
        
    orig_join = os.path.join
    with patch("app.os.path.join", side_effect=lambda *args: temp_burnejko_dir if any("burnejko" in str(arg) for arg in args) else orig_join(*args)):
        original_open = open
        def mock_open(file, *args, **kwargs):
            if "test_prompt.md" in str(file):
                raise PermissionError("Access Denied")
            return original_open(file, *args, **kwargs)
            
        with patch("builtins.open", mock_open):
            at = AppTest.from_file("app.py")
            at.session_state.current_page = "🎯 Akademia.pl Mentoring"
            at.run(timeout=30)
            
            selectbox = [sb for sb in at.selectbox if "Wybierz" in sb.label][0]
            assert "test_prompt.md" in selectbox.options
            
            selectbox.set_value("test_prompt.md").run(timeout=30)
            assert len(at.error) > 0
            assert any("Access Denied" in err.value for err in at.error)

def test_akademia_mentoring_successful_generation(temp_burnejko_dir):
    """Test that the Akademia.pl Mentoring successfully sends prompt and handles API response."""
    file_path = os.path.join(temp_burnejko_dir, "test_prompt.md")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("Role: Mentor\nInstructions: Analyze target group.")
        
    orig_join = os.path.join
    with patch("app.os.path.join", side_effect=lambda *args: temp_burnejko_dir if any("burnejko" in str(arg) for arg in args) else orig_join(*args)), \
         patch("urllib.request.urlopen", return_value=MockUrllibResponse()) as mock_urlopen:
        
        at = AppTest.from_file("app.py")
        at.session_state.current_page = "🎯 Akademia.pl Mentoring"
        at.run(timeout=30)
        
        # Select prompt
        selectbox = [sb for sb in at.selectbox if "Wybierz" in sb.label][0]
        selectbox.set_value("test_prompt.md").run(timeout=30)
        
        # Find fresh input widgets and set values
        company_profile_ta = [ta for ta in at.text_area if "Profil firmy" in ta.label][0]
        additional_context_ta = [ta for ta in at.text_area if "Dodatkowy" in ta.label][0]
        target_group_ti = [ti for ti in at.text_input if "Grupa" in ti.label][0]
        marketing_goal_ti = [ti for ti in at.text_input if "Cel" in ti.label][0]
        
        company_profile_ta.set_value("AI Agency")
        additional_context_ta.set_value("Audit this landing page content")
        target_group_ti.set_value("Local Businesses")
        marketing_goal_ti.set_value("Get 10 clients")
        
        # Click button and run
        submit_btn = [btn for btn in at.button if "Uruchom" in btn.label][0]
        submit_btn.click().run(timeout=30)
        
        # Verify urllib.request.urlopen was called
        mock_urlopen.assert_called()
        
        # Verify session state and UI display
        assert at.session_state.mentoring_result == "Mocked Gemini Response Advice"
        markdown_contents = [md.value for md in at.markdown]
        assert any("Mocked Gemini Response Advice" in md for md in markdown_contents)

def test_domena_hosting_new_tabs_rendering():
    """Verify that Domena & Hosting page renders all 4 tabs, including COMED and Alternative Architecture."""
    at = AppTest.from_file("app.py")
    at.session_state.current_page = "Domena & Hosting"
    at.run(timeout=30)
    
    tab_labels = [tab.label for tab in at.tabs]
    assert any("Hosting" in label for label in tab_labels)
    assert any("Poczta" in label for label in tab_labels)
    assert any("COMED" in label for label in tab_labels)
    assert any("Alternatywna" in label for label in tab_labels)
        
    markdown_contents = [md.value for md in at.markdown]
    assert any("COMED" in md for md in markdown_contents)
    assert any("Alternatywna" in md for md in markdown_contents)
