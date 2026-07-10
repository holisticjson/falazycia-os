import sys
import os
import runpy

# Dodajemy foldery 01_src i 01_src/agents do ścieżki Pythona, aby działały importy lokalne i modułowe
src_path = os.path.join(os.path.dirname(__file__), '01_src')
agents_path = os.path.join(src_path, 'agents')

if src_path not in sys.path:
    sys.path.insert(0, src_path)
if agents_path not in sys.path:
    sys.path.insert(0, agents_path)

# Ścieżka do właściwego pliku po refaktoryzacji
target_script = os.path.join(agents_path, 'holistic_ceo.py')

# Uruchamiamy właściwy skrypt wewnątrz Streamlit
runpy.run_path(target_script, run_name="__main__")
