import os
import sys
from unittest.mock import patch

# Add project root to path to import scratch/sync_to_gcp.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import scratch.sync_to_gcp as sync_to_gcp

def test_get_newest_brain_dir_success():
    with patch("os.path.exists") as mock_exists, \
         patch("os.listdir") as mock_listdir, \
         patch("os.path.isdir") as mock_isdir, \
         patch("os.path.getmtime") as mock_getmtime:
        
        mock_exists.return_value = True
        mock_listdir.return_value = ["brain1", "brain2", "brain3"]
        mock_isdir.return_value = True
        
        # mock modification times: brain2 is the newest
        parent_path = r"C:\Users\tomas_yq1b9su\.gemini\antigravity\brain"
        mtimes = {
            os.path.join(parent_path, "brain1"): 100,
            os.path.join(parent_path, "brain2"): 300,
            os.path.join(parent_path, "brain3"): 200,
        }
        mock_getmtime.side_effect = lambda path: mtimes.get(path, 0)
        
        conv_id, path = sync_to_gcp.get_newest_brain_dir()
        
        assert conv_id == "brain2"
        assert path == os.path.join(parent_path, "brain2")

def test_get_newest_brain_dir_no_dir():
    with patch("os.path.exists") as mock_exists:
        mock_exists.return_value = False
        conv_id, path = sync_to_gcp.get_newest_brain_dir()
        assert conv_id is None
        assert path is None
