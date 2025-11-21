# src/myapp/business_logic/habit_manager.py
from __future__ import annotations
from dataclasses import asdict
from datetime import datetime
from typing import List, Optional, Dict, Any

from myapp.contracts.habit_contract import HabitContract
from myapp.contracts.storage_interface import IStorage
from myapp.business_logic.xp_system import XPSystem


class HabitManager:
    """
    Kernlogik zur Verwaltung von Habits.
    Verantwortlichkeiten:
    - Erzeugen / Löschen von Habits
    - Markieren als erledigt
    - Persistieren via Storage-Adapter
    - Konversion Contract <-> dict
    """

    def __init__(self, storage: IStorage, xp_system: XPSystem):
        self._storage = storage
        self._xp_system = xp_system
        self._habits: List[HabitContract] = []
        self._next_id = 1
        self.load()

    # ------------------------
    # Hilfsfunktionen
    # ------------------------
    def _now_iso(self) -> str:
        """Aktuellen Zeitstempel als ISO-String."""
        return datetime.utcnow().date().isoformat()

    def _contract_to_dict(self, habit: HabitContract) -> Dict[str, Any]:
        """
        Konvertiert Contract in ein JSON-serialisierbares Dict.
        (Verwendet keine Methoden des Contracts.)
        """
        return {
            "id": habit.id,
            "name": habit.name,
            "description": habit.description,
            "frequency": habit.frequency,
            "is_done_today": habit.is_done_today,
            "created_at": habit.created_at.isoformat() if habit.created_at else None,
            "history": habit.history,
        }

    def _dict_to_contract(self, data: Dict[str, Any]) -> HabitContract:
        """Erzeugt HabitContract aus dict (Datenkonversion)."""
        created = None
        if data.get("created_at"):
            try:
                created = datetime.fromisoformat(data["created_at"])
            except ValueError:
                created = None
        habit = HabitContract(
            id=data.get("id"),
            name=data.get("name", ""),
            description=data.get("description", ""),
            frequency=data.get("frequency", "daily"),
            is_done_today=data.get("is_done_today", False),
            created_at=created,
            history=data.get("history", []) or [],
        )
        return habit

    # ------------------------
    # Persistenz
    # ------------------------
    def load(self) -> None:
        """
        Lädt alle Habits aus dem Storage und befüllt die interne Liste.
        Bestimmt außerdem die nächste freie ID.
        """
        raw = self._storage.load_habits()
        self._habits = [self._dict_to_contract(item) for item in raw]
        # next id bestimmen
        ids = [h.id for h in self._habits if h.id is not None]
        self._next_id = (max(ids) + 1) if ids else 1

    def save(self) -> None:
        """Speichert aktuelle Habits via Adapter (als Liste von dicts)."""
        payload = [self._contract_to_dict(h) for h in self._habits]
        self._storage.save_habits(payload)

    # ------------------------
    # CRUD-Operationen
    # ------------------------
    def add_habit(self, name: str, description: str = "", frequency: str = "daily") -> HabitContract:
        """
        Erstellt ein neues Habit und speichert es.

        Args:
            name (str): Name der Gewohnheit.
            description (str): Kurzbeschreibung.
            frequency (str): Häufigkeit ('daily', 'weekly', ...).

        Returns:
            HabitContract: neu erstelltes Habit-Objekt.
        """
        habit = HabitContract(
            id=self._next_id,
            name=name,
            description=description,
            frequency=frequency,
            is_done_today=False,
            created_at=datetime.utcnow(),
            history=[],
        )
        self._habits.append(habit)
        self._next_id += 1
        self.save()
        return habit

    def delete_habit(self, habit_id: int) -> bool:
        """
        Löscht Habit nach ID.

        Returns:
            bool: True wenn gelöscht, sonst False.
        """
        for idx, h in enumerate(self._habits):
            if h.id == habit_id:
                del self._habits[idx]
                self.save()
                return True
        return False

    def get_all(self) -> List[HabitContract]:
        """Gibt Kopie aller HabitContracts zurück (Leserepräsentation)."""
        return list(self._habits)

    def find_by_name(self, name: str) -> Optional[HabitContract]:
        """Sucht Habit per Name (erste Übereinstimmung)."""
        for h in self._habits:
            if h.name == name:
                return h
        return None

    # ------------------------
    # Business-Operationen
    # ------------------------
    def mark_done(self, habit_id: int, progress_amount: int = 1) -> Optional[Dict[str, int]]:
        """
        Markiert ein Habit als erledigt, fügt History hinzu und berechnet XP.

        Args:
            habit_id (int): ID des Habits.
            progress_amount (int): Multiplikator für XP.

        Returns:
            Optional[Dict[str, int]]: Informationen zu XP/Levelup, None bei Nichterfolg.
        """
        habit = next((h for h in self._habits if h.id == habit_id), None)
        if habit is None:
            return None

        today = self._now_iso()
        # History aktualisieren (kein Duplikat für den Tag)
        if habit.history and habit.history[-1] == today:
            # Bereits für heute markiert
            habit.is_done_today = True
            # Keine weiteren XP vergeben, aber wir könnten ein Flag zurückgeben
            self.save()
            return {"xp_awarded": 0, "level_ups": 0}

        habit.history.append(today)
        habit.is_done_today = True

        # XP berechnen & anwenden
        xp_amount = self._xp_system.calculate_xp(progress_amount)
        # Für dieses Beispiel verwalten wir XP-Werte extern; hier geben wir die XP zurück.
        # Wenn ihr einen globalen Nutzerzustand habt, ruft ihr xp_system.apply_xp(...) hier auf.
        self.save()
        return {"xp_awarded": xp_amount, "level_ups": 0}
