# src/myapp/business_logic/xp_system.py
from __future__ import annotations
from typing import Tuple


class XPSystem:
    """
    Verantwortlich für XP-Berechnung und Levellogik.
    Diese Klasse hält keinen persistenten Zustand (außer per Aufrufer).
    """

    BASE_XP_PER_ACTION: int = 10
    XP_PER_LEVEL: int = 100

    def calculate_xp(self, progress_amount: int = 1) -> int:
        """
        Berechnet die XP für eine gegebene Aktion / Fortschrittseinheit.

        Args:
            progress_amount (int): Multiplikator für XP (z. B. 1 für einfache Aktion).

        Returns:
            int: Anzahl der zu vergebenden XP.
        """
        return self.BASE_XP_PER_ACTION * max(1, progress_amount)

    def apply_xp(self, current_xp: int, delta_xp: int) -> Tuple[int, int]:
        """
        Wendet XP an und berechnet neuen Level-Status.

        Args:
            current_xp (int): Aktuelle XP des Nutzers.
            delta_xp (int): Hinzugefügte XP.

        Returns:
            Tuple[int, int]: (new_xp_remainder, new_level_increment)
            - new_xp_remainder: verbleibende XP nach Levelup-Abzug
            - new_level_increment: wie oft Level hochgegangen
        """
        total = current_xp + delta_xp
        level_ups = 0
        while total >= self.XP_PER_LEVEL:
            total -= self.XP_PER_LEVEL
            level_ups += 1
        return total, level_ups
