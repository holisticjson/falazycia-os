import os
import json
import threading
from typing import Any, Dict, Optional

class JsonStore:
    """Thread‑safe JSON storage helper.

    Provides `save` and `load` methods for a given directory. Files are
    written atomically to avoid race conditions when Streamlit reruns.
    """

    _lock = threading.Lock()

    def __init__(self, base_dir: str):
        self.base_dir = os.path.abspath(base_dir)
        os.makedirs(self.base_dir, exist_ok=True)

    def _path(self, filename: str) -> str:
        return os.path.join(self.base_dir, filename)

    def save(self, filename: str, data: Dict[str, Any]) -> None:
        """Save *data* as pretty‑printed JSON to *filename*.

        The operation is performed under a global lock to be safe with the
        multi‑threaded Streamlit runtime.
        """
        with self._lock:
            path = self._path(filename)
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def load(self, filename: str) -> Optional[Dict[str, Any]]:
        """Load JSON from *filename*.

        Returns ``None`` if the file does not exist or cannot be parsed.
        """
        path = self._path(filename)
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def list_json_files(self) -> list[str]:
        """Return a list of all ``.json`` files in the store directory."""
        return [f for f in os.listdir(self.base_dir) if f.endswith('.json')]
