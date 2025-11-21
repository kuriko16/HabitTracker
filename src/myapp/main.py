from myapp.adapters.json_storage import JSONStorage
from myapp.business_logic.habit_manager import HabitManager
from myapp.business_logic.xp_system import XPSystem


def main():
    storage = JSONStorage()
    xp = XPSystem()
    manager = HabitManager(storage, xp)

    print("Habit Tracker CLI (Test)")

    while True:
        print("\n1. Add habit")
        print("2. Mark habit as done")
        print("3. Show habits")
        print("4. Show XP")
        print("5. Exit")

        choice = input("Select: ")

        if choice == "1":
            name = input("Name: ")
            desc = input("Description: ")
            freq = input("Frequency: ")
            manager.add_habit(name, desc, freq)

        elif choice == "2":
            name = input("Habit name: ")
            if manager.mark_done(name):
                print("Habit marked as done!")
            else:
                print("Habit not found.")

        elif choice == "3":
            for h in manager.habits:
                print(f"- {h.name} ({h.description}) Done: {h.is_done_today}")

        elif choice == "4":
            print(xp.get_state())

        elif choice == "5":
            break


if __name__ == "__main__":
    main()
