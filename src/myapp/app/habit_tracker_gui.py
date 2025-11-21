import customtkinter as ctk
from typing import Callable, List

class HabitTrackerGUI(ctk.CTk):
    def __init__(self, manager):
        super().__init__()
        self.title("Habit Tracker")
        self.geometry("600x500")
        self.manager = manager

        self.habit_listbox = ctk.CTkTextbox(self, width=400, height=300)
        self.habit_listbox.pack(pady=20)

        self.refresh_button = ctk.CTkButton(self, text="Refresh", command=self.refresh)
        self.refresh_button.pack(pady=5)

        self.add_button = ctk.CTkButton(self, text="Add Habit", command=self.open_add_window)
        self.add_button.pack(pady=5)

        self.mark_button = ctk.CTkButton(self, text="Mark Done", command=self.mark_done)
        self.mark_button.pack(pady=5)

        self.refresh()

    def refresh(self):
        self.habit_listbox.delete("0.0", "end")
        for habit in self.manager.get_all():
            line = f"ID {habit.id} | {habit.name} | Done today: {habit.is_done_today}\n"
            self.habit_listbox.insert("end", line)

    def open_add_window(self):
        win = ctk.CTkToplevel(self)
        win.title("Add Habit")

        name_entry = ctk.CTkEntry(win, placeholder_text="Name")
        name_entry.pack(pady=10)

        desc_entry = ctk.CTkEntry(win, placeholder_text="Description")
        desc_entry.pack(pady=10)

        freq_entry = ctk.CTkEntry(win, placeholder_text="Frequency (daily/weekly)")
        freq_entry.pack(pady=10)

        def save():
            name = name_entry.get()
            desc = desc_entry.get()
            freq = freq_entry.get() or "daily"
            self.manager.add_habit(name, desc, freq)
            self.refresh()
            win.destroy()

        save_button = ctk.CTkButton(win, text="Save", command=save)
        save_button.pack(pady=10)

    def mark_done(self):
        win = ctk.CTkToplevel(self)
        win.title("Mark Habit Done")

        id_entry = ctk.CTkEntry(win, placeholder_text="Habit ID")
        id_entry.pack(pady=10)

        def submit():
            try:
                habit_id = int(id_entry.get())
                self.manager.mark_done(habit_id)
                self.refresh()
                win.destroy()
            except ValueError:
                pass

        mark_button = ctk.CTkButton(win, text="Mark Done", command=submit)
        mark_button.pack(pady=10)


# nur mal ein Beispiel wie es ausschauen könnte
# from myapp.business_logic.habit_manager import HabitManager
# from myapp.business_logic.xp_system import XPSystem
# from myapp.adapters.json_storage import JSONStorage
#
# if __name__ == "__main__":
#     ctk.set_appearance_mode("dark")
#     storage = JSONStorage()
#     xp = XPSystem()
#     manager = HabitManager(storage, xp)
#     app = HabitTrackerGUI(manager)
#     app.mainloop()
