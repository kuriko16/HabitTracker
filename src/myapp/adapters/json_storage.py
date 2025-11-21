# src/myapp/adapters/json_storage.py
from __future__ import annotations
import json
from pathlib import Path
from typing import List, Dict, Any
from myapp.contracts.storage_interface import IStorage


class JSONStorage(IStorage):
    """
    Einfacher JSON-Adapter, der Habit-Daten als Liste von Dicts speichert.
    Der Adapter arbeitet mit rohen Dicts; die Konversion dataclass <-> dict
    erfolgt im HabitManager.
    """

    def __init__(self, path: str | Path = "data/habits.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def load_habits(self) -> List[Dict[str, Any]]:
        """Lädt habit-Objekte als Liste von Dictionaries."""
        try:
            with self.path.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
            return data.get("habits", [])
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            # Im Fehlerfall leere Liste zurückgeben (robust gegenüber defekten Dateien)
            return []

    def save_habits(self, habits: List[Dict[str, Any]]) -> None:
        """Schreibt die Liste von Habit-Dictionaries in die JSON-Datei."""
        payload = {"habits": habits}
        with self.path.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
