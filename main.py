"""
main.py - Entry point for the NL2SQL system.
Run: python main.py
"""
import json
from app.NL2sql import process_question
from app.config import GROQ_API_KEY


def print_result(result: dict):
    """Pretty print the pipeline result."""
    print("\n" + "="*60)
    if result["intent"]:
        print("📊 INTENT EXTRACTED:")
        print(json.dumps(result["intent"], indent=2))

    if result["sql"]:
        print("\n🗄️  GENERATED SQL:")
        print("-" * 40)
        print(result["sql"])
        print("-" * 40)

    if result["validation"]:
        status = "✅ VALID" if result["validation"]["is_valid"] else "❌ INVALID"
        print(f"\n🔎 VALIDATION: {status}")
        if result["validation"]["errors"]:
            for err in result["validation"]["errors"]:
                print(f"   - {err}")

    print(f"\n📌 STATUS: {result['message']}")
    print(f"   Attempts: {result['attempts']}")
    print("="*60)


def main():
    if not GROQ_API_KEY:
        print("❌ ERROR: GEMINI_API_KEY not set in .env file.")
        print("   Create a .env file with: GEMINI_API_KEY=your_key_here")
        return

    print("="*60)
    print("   🤖 NL2SQL — Natural Language to SQL Query System")
    print("="*60)
    print("Type your question in plain English. Type 'exit' to quit.\n")

    while True:
        try:
            question = input("❓ Your question: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not question:
            continue
        if question.lower() in ("exit", "quit", "q"):
            print("Goodbye!")
            break

        result = process_question(question)
        print_result(result)


if __name__ == "__main__":
    main()