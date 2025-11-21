# src/myapp/dummies/mock_storage.py
from typing import List, Dict, Any
from myapp.contracts.storage_interface import IStorage


class MockStorage(IStorage):
    """In-Memory Storage für Tests; verliert Daten beim Beenden."""

    def __init__(self, initial: List[Dict[str, Any]] | None = None):
        self._data = initial or []

    def load_habits(self) -> List[Dict[str, Any]]:
        return list(self._data)

    def save_habits(self, habits: List[Dict[str, Any]]) -> None:
        # flache Kopie speichern
        self._data = [dict(h) for h in habits]
