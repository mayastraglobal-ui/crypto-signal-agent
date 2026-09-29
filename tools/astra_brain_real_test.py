import os
from pathlib import Path
from openai import OpenAI

MODEL = "gpt-6-astra"

def main():
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        raise SystemExit("OPENAI_API_KEY is not available.")

    repo = Path(__file__).resolve().parents[1]
    prompt = """You are the Brain of a crypto trading research agent.

THIS IS AN ISOLATED RESEARCH TEST. Do not place trades, generate live signals,
approve strategies, modify files, or claim that any strategy is profitable.

Read the supplied AGENT_PROMPT.md as the authoritative description of the
agent's intended architecture.

Your task:
1. Summarize what this agent is designed to do.
2. Identify the most important missing capabilities for the intended
   self-learning research workflow.
3. Separate responsibilities that belong to deterministic code from
   responsibilities appropriate for the AI Brain.
4. Propose three concrete research/development tasks the Brain should perform
   next, with a clear reason for each.
5. Identify one important risk of allowing an LLM to influence a trading system
   and the corresponding control that should prevent it.

Be precise and evidence-based. If the source does not establish something,
say that it is not established. Do not invent current market data.

Return a concise report with headings:
CURRENT DESIGN
GAPS
DETERMINISTIC CODE VS BRAIN
NEXT THREE TASKS
SAFETY CONTROL
"""

    architecture = (repo / "AGENT_PROMPT.md").read_text(encoding="utf-8")
    response = OpenAI(api_key=key).responses.create(
        model=MODEL,
        input=[
            {"role": "user", "content": prompt},
            {"role": "user", "content": "SOURCE FILE: AGENT_PROMPT.md\n\n" + architecture},
        ],
    )

    out = repo / "reports" / "astra" / "brain-test.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        "# GPT-6 Astra Brain Test\n\n"
        f"- Model: {MODEL}\n"
        "- Test type: isolated architecture/research review\n\n"
        "## Astra Output\n\n"
        + response.output_text.strip()
        + "\n",
        encoding="utf-8",
    )
    print(response.output_text)

if __name__ == "__main__":
    main()
