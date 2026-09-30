"""GPT-6 Astra adapter for TradeSentry's research Brain.

This module deliberately contains no market, risk, strategy, or file-writing
logic.  The caller supplies deterministic context and validates any returned
text with the existing Brain Guard.
"""
import os
from importlib import import_module

MODEL = "gpt-6-astra"


class AstraConfigurationError(RuntimeError):
    """Raised when the Astra credential is unavailable."""


class AstraResponseError(RuntimeError):
    """Raised when Astra does not return usable text."""


class AstraBrain:
    """Research-only adapter using the official OpenAI Responses API."""

    def __init__(self, client=None, api_key=None):
        key = api_key if api_key is not None else os.environ.get("OPENAI_API_KEY")
        if not key:
            raise AstraConfigurationError("OPENAI_API_KEY is not configured")
        # Import only when a real client is needed.  This keeps deterministic
        # unit tests offline while production uses the official SDK installed
        # from requirements.txt.
        self._client = client or import_module("openai").OpenAI(api_key=key)

    def run(self, task: str, context: str) -> str:
        if not task or not context:
            raise ValueError("task and context are required")
        response = self._client.responses.create(
            model=MODEL,
            instructions=(
                "You are GPT-6 Astra, TradeSentry's research-only Brain. "
                "Use only supplied deterministic facts for prices, statistics, "
                "regimes, signals, and outcomes. Never trade, approve a strategy, "
                "change risk, configuration, workflows, engine calculations, or "
                "Brain Guard. If information is missing, say 'not available'."
            ),
            input=f"Task: {task}\n\n{context}",
        )
        text = getattr(response, "output_text", None)
        if not isinstance(text, str) or not text.strip():
            raise AstraResponseError("Astra returned empty output")
        return text.strip()
