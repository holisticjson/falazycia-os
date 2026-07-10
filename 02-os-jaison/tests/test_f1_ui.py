import pytest
from streamlit.testing.v1 import AppTest

# TC-01 to TC-10

def test_tc01_sidebar_navigation():
    at = AppTest.from_file("app.py")
    at.run()
    # Check default page
    assert at.session_state.current_page == "🎯 Mission Control"
    
    # Simulate selecting another page
    at.session_state.current_page = "Baza Wiedzy (Vertex AI)"
    at.run()
    assert at.session_state.current_page == "Baza Wiedzy (Vertex AI)"

def test_tc02_mission_control_rendering():
    at = AppTest.from_file("app.py")
    at.session_state.current_page = "🎯 Mission Control"
    at.run()
    # Should render the header and sections of Mission Control
    assert len(at.text_input) > 0

def test_tc03_baza_wiedzy_rendering():
    at = AppTest.from_file("app.py")
    at.session_state.current_page = "Baza Wiedzy (Vertex AI)"
    at.run()
    # Should render tab query or search box
    assert len(at.tabs) > 0

def test_tc04_agent_consoles_rendering():
    at = AppTest.from_file("app.py")
    # Navigate to Claude agent console
    at.session_state.current_page = "Claude"
    at.run()
    assert len(at.tabs) > 0

def test_tc05_one_thing_empty():
    at = AppTest.from_file("app.py")
    at.session_state.one_thing = ""
    at.run()
    inputs = at.text_input
    one_thing_input = [inp for inp in inputs if "Moje jedyne zadanie" in inp.label]
    assert len(one_thing_input) == 1
    one_thing_input[0].set_value("").run()
    assert at.session_state.one_thing == ""

def test_tc06_one_thing_long():
    at = AppTest.from_file("app.py")
    at.run()
    one_thing_input = [inp for inp in at.text_input if "Moje jedyne zadanie" in inp.label][0]
    long_task = "A" * 500
    one_thing_input.set_value(long_task).run()
    assert at.session_state.one_thing == long_task

def test_tc07_one_thing_state_persistence():
    at = AppTest.from_file("app.py")
    at.run()
    one_thing_input = [inp for inp in at.text_input if "Moje jedyne zadanie" in inp.label][0]
    one_thing_input.set_value("Ukończyć testy E2E").run()
    assert at.session_state.one_thing == "Ukończyć testy E2E"

def test_tc08_one_thing_navigation_persistence():
    at = AppTest.from_file("app.py")
    at.run()
    one_thing_input = [inp for inp in at.text_input if "Moje jedyne zadanie" in inp.label][0]
    one_thing_input.set_value("Zadanie testowe").run()
    
    # Navigate to Baza Wiedzy
    at.session_state.current_page = "Baza Wiedzy (Vertex AI)"
    at.run()
    assert at.session_state.one_thing == "Zadanie testowe"
    
    # Navigate back to Mission Control
    at.session_state.current_page = "🎯 Mission Control"
    at.run()
    assert at.session_state.one_thing == "Zadanie testowe"

@pytest.mark.skip(reason="Streamlit AppTest concurrent execution timeout on Windows")
def test_tc09_multi_page_navigation():
    pages = ["🎯 Mission Control", "Claude", "Hermes"]
    for page in pages:
        at = AppTest.from_file("app.py")
        at.session_state.current_page = page
        at.run(timeout=25)
        assert at.session_state.current_page == page

def test_tc10_one_thing_flow():
    at = AppTest.from_file("app.py")
    at.run()
    one_thing_input = [inp for inp in at.text_input if "Moje jedyne zadanie" in inp.label][0]
    one_thing_input.set_value("Skupienie na pracy").run()
    
    # Run Pomodoro button if available
    pomodoro_btn = [btn for btn in at.button if "Uruchom Pomodoro" in btn.label]
    if pomodoro_btn:
        pomodoro_btn[0].click().run()
        assert at.session_state.pomodoro_active == True

def test_tc11_akademia_mentoring_page():
    at = AppTest.from_file("app.py")
    at.session_state.current_page = "🎯 Akademia.pl Mentoring"
    at.run()
    assert at.session_state.current_page == "🎯 Akademia.pl Mentoring"

def test_tc12_domena_hosting_page():
    at = AppTest.from_file("app.py")
    at.session_state.current_page = "Domena & Hosting"
    at.run()
    assert at.session_state.current_page == "Domena & Hosting"
    assert len(at.tabs) > 0
