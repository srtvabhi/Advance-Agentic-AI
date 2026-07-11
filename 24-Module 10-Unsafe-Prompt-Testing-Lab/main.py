import sys

from graphs.testing_graph import build_testing_graph


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> None:
    # Entry point for the unsafe prompt testing lab.
    print("Lab 24: Test AI Agents Against Unsafe Prompt Scenarios\n")
    print("This lab runs a built-in prompt safety test suite.\n")

    app = build_testing_graph()
    result = app.invoke(
        {
            "test_suite_name": "Module 10 Unsafe Prompt Test Suite",
            "prompts": [],
            "test_results": [],
            "blocked_count": 0,
            "allowed_count": 0,
            "improvement_plan": "",
            "final_report": "",
        }
    )

    print("--- Test Results ---")
    for item in result["test_results"]:
        print(f"\nPrompt: {item['prompt']}")
        print(f"Decision: {item['decision']}")
        print(f"Reason: {item['reason']}")

    print("\n--- Summary ---")
    print("Blocked:", result["blocked_count"])
    print("Allowed:", result["allowed_count"])
    print("\n--- Improvement Plan ---\n", result["improvement_plan"])
    print("\n--- Final Report ---\n", result["final_report"])


if __name__ == "__main__":
    main()
