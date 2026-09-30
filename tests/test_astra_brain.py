"""Unit coverage for the GPT-6 Astra research-only integration."""
import datetime as dt
import os
import unittest
from unittest.mock import MagicMock, patch

from engine import brain
from engine.astra_brain import AstraBrain, AstraConfigurationError, AstraResponseError, MODEL


DAILY = """# Daily review
## Summary
- FACT: deterministic facts were supplied.
## Email summary
- lesson: Wait when deterministic evidence is not available.
- tomorrow: Watch the deterministic fact sheet.
"""


class AstraAdapterTests(unittest.TestCase):
    def test_missing_api_key_fails_closed(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(AstraConfigurationError):
                AstraBrain()

    def test_invokes_responses_api_with_the_requested_model(self):
        client = MagicMock()
        client.responses.create.return_value = MagicMock(output_text="# Research")
        result = AstraBrain(client=client, api_key="test-key").run("daily", "facts")
        self.assertEqual(result, "# Research")
        kwargs = client.responses.create.call_args.kwargs
        self.assertEqual(kwargs["model"], MODEL)
        self.assertIn("Task: daily", kwargs["input"])
        self.assertIn("research-only", kwargs["instructions"])

    def test_empty_responses_output_is_rejected(self):
        client = MagicMock()
        client.responses.create.return_value = MagicMock(output_text=" ")
        with self.assertRaises(AstraResponseError):
            AstraBrain(client=client, api_key="test-key").run("daily", "facts")


class AstraGuardTests(unittest.TestCase):
    def review(self, changes, branch="astra/brain-daily"):
        return brain.review(changes, {"strategies.yaml": "strategies: []"},
                            dt.datetime(2026, 9, 30, tzinfo=dt.timezone.utc), branch)

    def test_valid_daily_artifact_is_accepted(self):
        applies, problems, _ = self.review([
            dict(path="reports/astra/daily/2026-09-30.md", status="A", base=None, new=DAILY)])
        self.assertFalse(problems)
        self.assertEqual(applies[0]["path"], "reports/astra/daily/2026-09-30.md")

    def test_prohibited_profit_and_mixed_state_content_is_rejected(self):
        _, problems, _ = self.review([
            dict(path="reports/astra/daily/2026-09-30.md", status="A", base=None,
                 new=DAILY + "\nThis is a guaranteed profit. LIVE and BACKTEST results agree.\n")])
        self.assertTrue(any("profit promise" in p for p in problems))
        self.assertTrue(any("mixes result states" in p for p in problems))

    def test_trading_orders_and_live_approval_content_is_rejected(self):
        _, problems, _ = self.review([
            dict(path="reports/astra/daily/2026-09-30.md", status="A", base=None,
                 new=DAILY + "\nPlace a trade.\nApprove the strategy.\nEntry: 100000.\n")])
        self.assertTrue(any("trading action" in p for p in problems))
        self.assertTrue(any("approval" in p for p in problems))
        self.assertTrue(any("executable order level" in p for p in problems))

    def test_protected_file_is_rejected_as_a_whole(self):
        applies, problems, _ = self.review([
            dict(path="reports/astra/daily/2026-09-30.md", status="A", base=None, new=DAILY),
            dict(path="config.yaml", status="M", base="x", new="changed"),
        ])
        self.assertEqual(applies, [])
        self.assertTrue(any("not allowed" in p for p in problems))

    def test_integration_artifact_requires_daily_email_summary(self):
        _, problems, _ = self.review([
            dict(path="reports/astra/daily-integration.md", status="A", base=None, new="# missing")])
        self.assertTrue(any("Email summary" in p for p in problems))


class AstraWorkflowTests(unittest.TestCase):
    def test_workflow_uses_secret_fact_sheet_runner_and_brain_guard(self):
        with open(".github/workflows/astra-brain.yml", encoding="utf-8") as f:
            workflow = f.read()
        for required in ("ref: astra-brain-test", "OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}",
                         "python brain_pack.py", "python astra_runner.py", "python brain_guard.py",
                         "Save only Brain Guard permitted output"):
            self.assertIn(required, workflow)


if __name__ == "__main__":
    unittest.main()
