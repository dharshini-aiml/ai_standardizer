import argparse
import os
from app.services.ai_service import AIService


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", help="Prompt to send", default=None)
    args = parser.parse_args()

    svc = AIService()

    try:
        resp = svc.generate(args.prompt or "Respond with 'pong' if available.")
        print("-- Provider: Gemini")
        print("-- Response:\n", resp)
    except Exception as e:
        print("LLM test failed:", str(e))


if __name__ == "__main__":
    main()