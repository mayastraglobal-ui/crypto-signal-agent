"""Small, side-effect-free interface for research-Brain providers.

Providers receive already-prepared context and return text.  They do not get a
repository path, trading-engine objects, or file-writing capabilities.
"""
from typing import Protocol


class BrainProvider(Protocol):
    """A research-only model provider."""

    def run(self, task: str, context: str) -> str:
        """Return the model's proposed task artifact as text."""
