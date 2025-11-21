# src/myapp/contracts/habit_contract.py
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class HabitContract:
    """
    Datenmodell (Contract) für eine Gewohnheit (Habit).
    Dieses Contract definiert ausschließlich die Datenstruktur.
    Logik (Speichern, Serialisieren, Verhalten) gehört in den HabitManager.
    """
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    frequency: str = "daily"  # z. B. 'daily', 'weekly', oder ein Zahlstring
    is_done_today: bool = False
    created_at: Optional[datetime] = None
    history: List[str] = field(default_factory=list)
    