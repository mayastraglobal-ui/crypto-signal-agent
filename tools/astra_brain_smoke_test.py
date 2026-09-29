import os
from openai import OpenAI

MODEL = "gpt-6-astra"

def main():
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise SystemExit("OPENAI_API_KEY is not available to this workflow.")

    client = OpenAI(api_key=key)
    response = client.responses.create(
        model=MODEL,
        input=(
            "You are the research Brain of a crypto trading research agent. "
            "This is a smoke test only. Do not propose trades or modify files. "
            "Reply with exactly three short lines: READY, your model name, and "
            "one sentence confirming that you can reason over research tasks."
        ),
    )
    print(response.output_text)

if __name__ == "__main__":
    main()
