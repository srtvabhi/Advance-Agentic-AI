import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


LABS = {
    "1": {
        "title": "Design an enterprise-grade agent architecture",
        "folder": "enterprise_architecture",
    },
    "2": {
        "title": "Build a stateful agent workflow design",
        "folder": "stateful_workflow",
    },
    "3": {
        "title": "Create an AI planning and execution pipeline",
        "folder": "planning_pipeline",
    },
}


def show_menu() -> None:
    print("Module-1 Lab: Advanced Agentic AI Architecture Patterns\n")
    for key, lab in LABS.items():
        print(f"{key}. {lab['title']}")
    print("q. Quit")


def run_lab(choice: str) -> None:
    lab = LABS[choice]
    lab_folder = BASE_DIR / lab["folder"]
    print(f"\nStarting: {lab['title']}\n")
    subprocess.run([sys.executable, "main.py"], cwd=lab_folder, check=True)


def main() -> None:
    while True:
        show_menu()
        choice = input("\nSelect lab objective: ").strip().lower()

        if choice in {"q", "quit", "exit"}:
            print("Goodbye.")
            break

        if choice not in LABS:
            print("Invalid choice. Please select 1, 2, 3, or q.\n")
            continue

        run_lab(choice)
        print("\nReturned to Module-1 menu.\n")


if __name__ == "__main__":
    main()
