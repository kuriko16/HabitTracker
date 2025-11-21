# src/myapp/contracts/storage_interface.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class IStorage(ABC):
    """
    Interface für persistente Speicheradapter.
    Alle Adapter sollen diese Methoden implementieren.
    """

    @abstractmethod
    def load_habits(self) -> List[Dict[str, Any]]:
        """Lädt eine Liste von Habit-Dictionaries aus dem Speicher."""
        raise NotImplementedError

    @abstractmethod
    def save_habits(self, habits: List[Dict[str, Any]]) -> None:
        """Speichert eine Liste von Habit-Dictionaries im Speicher."""
        raise NotImplementedError
