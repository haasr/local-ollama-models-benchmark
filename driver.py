"""
Ollama benchmark driver.

Run:
    python driver.py
"""

from pathlib import Path

from models.ollama_model_test import OllamaModelTest


MODELS = {
    "1": {
        "name": "llama3.2:3b",
        "description": "Llama 3.2 3B",
    },
    "2": {
        "name": "qwen3:4b",
        "description": "Qwen 3 4B",
    },
    "3": {
        "name": "qwen3:8b",
        "description": "Qwen 3 8B",
    },
    "4": {
        "name": "llama3.1:8b",
        "description": "Llama 3.1 8B",
    },
    "5": {
        "name": "gemma3:4b",
        "description": "Gemma 3 4B",
    },
}


RESULTS_DIR = Path(__file__).parent / "results"


def display_menu():
    print()
    print("=" * 60)
    print(" Ollama Local LLM Benchmark")
    print("=" * 60)
    print()
    print("Select the model to test:")
    print()

    for key, model in MODELS.items():
        print(f"  {key}. {model['description']:<25} {model['name']}")

    print()
    print("  Q. Quit")
    print()


def get_model_selection():
    while True:
        display_menu()

        selection = input("Selection: ").strip().lower()

        if selection == "q":
            return None

        if selection in MODELS:
            return MODELS[selection]

        print("\nInvalid selection. Please try again.\n")


def main():
    model = get_model_selection()

    if model is None:
        print("Exiting.")
        return

    print()
    print(f"Selected model: {model['name']}")
    print()

    RESULTS_DIR.mkdir(exist_ok=True)

    benchmark = OllamaModelTest(
        model_name=model["name"],
        results_dir=RESULTS_DIR,
    )

    benchmark.run()


if __name__ == "__main__":
    main()
