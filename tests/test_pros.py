"""
Phase 18 part C tests: the new building blocks (Fibonacci of the last swing, VWAP anchored at the last swing and the
daily open, volume profile POC / value area, Ichimoku - all from closed candles only) and the idea queue (10 cards
rewritten from freqtrade-strategies, R4, copied into the lab unchanged over the weeks).

Run:  python -m unittest test_pros -v      (from tests/)
"""
import copy
import datetime as dt
import os
import shutil
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np
import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import brain_pack  # noqa: E402
import scanner as sc  # noqa: E402
import test_brain  # noqa: E402
import test_lab  # noqa: E402
import test_robust  # noqa: E402
from engine import bias as BI  # noqa: E402
from engine import brain as B  # noqa: E402
from engine import features as FE  # noqa: E402
from engine import idea_queue as IQ  # noqa: E402
from engine import research_loop as RL  # noqa: E402
from engine import strategy_spec as SS  # noqa: E402

UTC = dt.timezone.utc
NOW = dt.datetime(2026, 9, 27, 2, 0, tzinfo=UTC)
TF1H = sc.TF_MS["1h"]
NEW_COLS = ["fib_dir", "fib_382", "fib_500", "fib_618", "fib_786", "avwap_day", "avwap_swing_high", "avwap_swing_low",
            "ichi_tenkan", "ichi_kijun", "ichi_span_a", "ichi_span_b", "ichi_cloud_top", "ichi_cloud_bottom"]
EXPERIMENTS = test_brain.read(os.path.join(ROOT, "memory", "experiments.md"))


def candles(closes, vol=None, start=1_700_000_000_000):
    c = np.asarray(closes, dtype=float)
    n = len(c)
    ot = start + np.arange(n) * TF1H
    return pd.DataFrame(dict(open_time=ot, open=c, high=c + 0.5, low=c - 0.5, close=c,
                             volume=np.ones(n) if vol is None else np.asarray(vol, float), close_time=ot + TF1H - 1))


class Fibonacci(unittest.TestCase):
    def test_levels_of_the_last_leg(self):
        path = [150, 140, 130, 120, 110, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 190, 185, 180, 175]
        f = FE.compute(candles(path), TF1H)
        hi_i = path.index(200)                                  # the high is KNOWN 3 candles after it
        self.assertTrue(np.isnan(f["fib_dir"].iloc[hi_i + 2]) or f["fib_dir"].iloc[hi_i + 2] == -1)
        row = f.iloc[hi_i + 3]
        H, L = 200.5, 99.5                                      # swing high / low use the candle's high / low
        self.assertEqual(row["fib_dir"], 1.0, "the newest swing is a high: the last leg went up")
        for r, col in ((0.382, "fib_382"), (0.5, "fib_500"), (0.618, "fib_618"), (0.786, "fib_786")):
            self.assertAlmostEqual(row[col], H - r * (H - L))
        down = [100, 110, 120, 130, 140, 150, 140, 130, 120, 110, 100, 90, 80, 85, 90, 95, 100]
        f = FE.compute(candles(down), TF1H)
        row = f.iloc[down.index(80) + 3]
        self.assertEqual(row["fib_dir"], -1.0)
        self.assertAlmostEqual(row["fib_618"], 79.5 + 0.618 * (150.5 - 79.5))


class AnchoredVwap(unittest.TestCase):
    def test_from_the_swing_candle(self):
        rng = np.random.default_rng(4)
        c = 100 + np.cumsum(rng.normal(0, 1, 400))
        v = rng.uniform(1, 5, 400)
        df = candles(c, v)
        f = FE.compute(df, TF1H)
        tp = (df["high"] + df["low"] + df["close"]).to_numpy() / 3
        for kind in ("low", "high"):
            known = np.flatnonzero(f[f"swing_{kind}"].to_numpy())
            for t in (known[3], known[3] + 5, known[-1] + 2):
                if t >= len(df):
                    continue
                p = max(k for k in known if k <= t) - 3        # the swing candle itself (known 3 candles later)
                want = (tp[p:t + 1] * v[p:t + 1]).sum() / v[p:t + 1].sum()
                self.assertAlmostEqual(f[f"avwap_swing_{kind}"].iloc[t], want, places=9, msg=kind)
            self.assertTrue(np.isnan(f[f"avwap_swing_{kind}"].iloc[:known[0]]).all(), "nothing known before the swing")
        np.testing.assert_array_equal(f["avwap_day"].to_numpy(), f["vwap"].to_numpy())


class VolumeProfile(unittest.TestCase):
    def test_small_example(self):
        tp = np.array([1, 2, 2, 3, 3, 3, 4, 10.0])
        v = np.array([1, 1, 1, 1, 1, 5, 1, 1.0])
        poc, vah, val = FE.volume_profile(tp, v, 8, bins=9)
        self.assertTrue(np.isnan(poc[:7]).all())
        self.assertEqual((poc[7], vah[7], val[7]), (3.5, 4.0, 2.0), "fullest bin 3..4; 70% of volume in 2..4")

    def test_matches_a_plain_loop(self):
        rng = np.random.default_rng(2)
        tp = 100 + np.cumsum(rng.normal(0, 1, 300))
        v = rng.uniform(1, 10, 300)
        poc, vah, val = FE.volume_profile(tp, v, 50, chunk=37)          # small chunks: the chunking is exercised
        for t in (49, 120, 299):
            w, wv = tp[t - 49:t + 1], v[t - 49:t + 1]
            lo, width = w.min(), (w.max() - w.min()) / 24
            b = np.clip(np.floor((w - lo) / width), 0, 23).astype(int)
            hist = np.bincount(b, weights=wv, minlength=24)
            self.assertAlmostEqual(poc[t], lo + (hist.argmax() + 0.5) * width)
            order = np.argsort(-hist, kind="stable")
            k = int((np.cumsum(hist[order]) < 0.7 * hist.sum()).sum())
            self.assertAlmostEqual(vah[t], lo + (order[:k + 1].max() + 1) * width)
            self.assertAlmostEqual(val[t], lo + order[:k + 1].min() * width)
            self.assertLessEqual(val[t], poc[t])
            self.assertLessEqual(poc[t], vah[t])


class Ichimoku(unittest.TestCase):
    def test_cloud_is_drawn_from_the_past(self):
        rng = np.random.default_rng(5)
        df = candles(100 + np.cumsum(rng.normal(0, 1, 300)))
        f = FE.compute(df, TF1H)
        h, l = df["high"], df["low"]
        t = 200
        tenkan = (h.iloc[t - 8:t + 1].max() + l.iloc[t - 8:t + 1].min()) / 2
        self.assertAlmostEqual(f["ichi_tenkan"].iloc[t], tenkan)
        self.assertAlmostEqual(f["ichi_span_a"].iloc[t], (f["ichi_tenkan"].iloc[t - 26] + f["ichi_kijun"].iloc[t - 26]) / 2)
        b = (h.iloc[t - 26 - 51:t - 26 + 1].max() + l.iloc[t - 26 - 51:t - 26 + 1].min()) / 2
        self.assertAlmostEqual(f["ichi_span_b"].iloc[t], b)
        self.assertAlmostEqual(f["ichi_cloud_top"].iloc[t], max(f["ichi_span_a"].iloc[t], f["ichi_span_b"].iloc[t]))
        self.assertFalse(any("chikou" in c for c in f.columns), "the chikou span looks into the future - left out")


class NoLookahead(unittest.TestCase):
    """Every new value at candle t uses candles 0..t only, and settles to the same value when history starts later."""

    @classmethod
    def setUpClass(cls):
        cls.df = sc.Synthetic().klines("BTCUSDT", "1h", 3000)
        cls.full = FE.compute(cls.df, TF1H)

    def test_prefix_gives_the_same_values(self):
        for cut in (1000, 2217, 2999):
            f = FE.compute(self.df.iloc[:cut + 1].reset_index(drop=True), TF1H)
            for col in NEW_COLS:
                np.testing.assert_array_equal(f[col].to_numpy(), self.full[col].to_numpy()[:cut + 1], col)
        ns_full = sc.make_namespace(self.df, self.full)
        part = self.df.iloc[:2001].reset_index(drop=True)
        ns_part = sc.make_namespace(part, FE.compute(part, TF1H))
        for fn in ("vp_poc", "vp_vah", "vp_val"):
            np.testing.assert_array_equal(ns_part[fn](100).to_numpy(), ns_full[fn](100).to_numpy()[:2001], fn)

    def test_later_start_settles(self):
        late = self.df.iloc[500:].reset_index(drop=True)
        f = FE.compute(late, TF1H)
        for col in NEW_COLS:
            a, b = f[col].to_numpy()[300:], self.full[col].to_numpy()[800:]
            np.testing.assert_allclose(a, b, rtol=1e-9, err_msg=col)

    def test_building_blocks_are_known_to_the_lab(self):
        for col in NEW_COLS:
            self.assertIn(col, SS.COLUMNS)
        self.assertLessEqual({"vp_poc", "vp_vah", "vp_val"}, SS.FUNCTIONS)
        for rule in ("close > fib_618", "close < vp_val(100)", "close > ichi_cloud_top", "cross_up(close, avwap_swing_low)"):
            self.assertEqual(SS.expr_problems(rule, ["1h"]), [], rule)
        header = test_brain.read(os.path.join(ROOT, "strategies.yaml")).split("\n- id:")[0]
        for name in ("fib_618", "avwap_swing_low", "vp_poc(100)", "ichi_cloud_top", "chikou"):
            self.assertIn(name, header)


QUEUE = IQ.parse(EXPERIMENTS)


class R4Queue(unittest.TestCase):
    """The 10 freqtrade-inspired cards (R4), queued in memory/experiments.md."""

    def test_ten_valid_cards(self):
        self.assertEqual(len(QUEUE), 10)
        self.assertEqual(len({q["key"] for q in QUEUE}), 10)
        self.assertNotIn("&id0", EXPERIMENTS, "no YAML anchors - the card is copied by hand")
        lib = yaml.safe_load(test_brain.read(os.path.join(ROOT, "strategies.yaml")))
        others = {c["id"]: c for c in lib}
        mem = {p: test_brain.read(os.path.join(ROOT, p)) for p in RL.FILES.values()}
        for q in QUEUE:
            c = IQ.ready(q, NOW.date())
            self.assertTrue(q["key"].startswith("R4-"))
            self.assertIn("f3340ce11f5bdf62f598522e64d1f5638eaa13f5/user_data/strategies/", c["source_url"])
            self.assertIn("no code copied", c["source"])
            self.assertEqual(c["parent"], "source: [R4] freqtrade-strategies")
            self.assertEqual(SS.lab_card_problems(c, {k: v for k, v in others.items() if k != c["id"]}, B.rg.LABELS,
                                                  sc.TF_ORDER), [], q["key"])
            self.assertEqual(SS.factory_problems(c, B.LOSS_TAGS), [], q["key"])
            self.assertEqual(RL.parent_exists_problems(c, mem, B.LOSS_TAGS), [], q["key"])
            self.assertIsNone(SS.special(c), "no SMC / 5m ingredient - no control twin needed")
        self.assertEqual(sum(q["card"]["factory"] == "literature" for q in QUEUE), 10)

    def test_cards_run_and_pass_the_bias_check(self):
        tfs = ["4h", "1h", "30m", "15m"]
        feed = sc.Synthetic()
        data, quality = {}, {}
        for tf in ["1w", "1d"] + tfs:
            raw = feed.klines("BTCUSDT", tf, 1000 if tf == "1w" else 4000)
            df, rep = test_robust.dq.check_candles(raw, sc.TF_MS[tf], int(raw["close_time"].max()) + 1,
                                                   test_robust.dq.settings(test_robust.CFG.get("data_quality")))
            data[("BTCUSDT", tf)], quality[("BTC", tf)] = df, rep
        cards, _, _ = SS.load([IQ.ready(q, NOW.date()) for q in QUEUE], B.rg.LABELS, sc.TF_ORDER)
        self.assertEqual(len(cards), 10)
        btc = sc.btc_frames(data, "USDT", tfs)
        full = sc.prepare_coin("BTCUSDT", "BTC", data, quality, tfs, test_robust.CFG, None, btc)
        fired = 0
        for s in cards:
            for tf in s["timeframes"]:
                L, S, XL, XS, cols = sc.strategy_signals(s, tf, full["frames"][tf], test_robust.CFG)
                fired += int(L.sum() + S.sum())
        self.assertGreater(fired, 0, "the rules are not dead on arrival")
        res = BI.check_coin("BTCUSDT", "BTC", data, quality, tfs, test_robust.CFG, None, btc, full, cards,
                            sc.prepare_coin, sc.eval_rules, sc.level_array, SS.columns_needed,
                            BI.settings(dict(lookahead_cuts=3)))
        self.assertEqual(res["findings"], {})
        self.assertEqual(len(res["checked"]), 10)

    def test_copy_must_be_unchanged(self):
        q = QUEUE[0]
        self.assertEqual(IQ.copy_problems(IQ.ready(q, NOW.date()), QUEUE), [])
        bad = copy.deepcopy(IQ.ready(q, NOW.date()))
        bad["params"]["lo"] = 25
        self.assertIn("copy it unchanged", IQ.copy_problems(bad, QUEUE)[0])
        self.assertIn("params", IQ.copy_problems(bad, QUEUE)[0])
        self.assertEqual(IQ.copy_problems(dict(id="other", version="1.0"), QUEUE), [])
        self.assertEqual(IQ.pending(QUEUE, [q["card"]])[0]["key"], QUEUE[1]["key"])

    def test_guard_accepts_the_copy_and_refuses_a_change(self):
        main = {SB: test_brain.read(os.path.join(ROOT, SB)) for SB in (SS.LIBRARY_FILE,) + tuple(RL.FILES.values())}
        main[SS.LAB_FILE] = test_lab.LAB_HEAD
        good = IQ.ready(QUEUE[0], NOW.date())
        _, probs, _ = B.review([test_lab.lab_change([good])], main, NOW, "claude/brain-weekly")
        self.assertEqual(probs, [])
        bad = copy.deepcopy(good)
        bad["timeframes"] = ["1h"]
        _, probs, _ = B.review([test_lab.lab_change([bad])], main, NOW, "claude/brain-weekly")
        self.assertTrue(any("copy it unchanged" in p for p in probs), probs)

    def test_weekly_fact_sheet_offers_the_next_within_the_quota(self):
        tmp = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tmp, True)
        os.makedirs(os.path.join(tmp, "memory"))
        for name in ("config.yaml", "strategies.yaml"):
            shutil.copy(os.path.join(ROOT, name), tmp)
        shutil.copy(os.path.join(ROOT, "memory", "experiments.md"), os.path.join(tmp, "memory"))
        lab = os.path.join(tmp, SS.LAB_FILE)
        with open(lab, "w") as f:
            f.write(test_lab.LAB_HEAD)
        with mock.patch.object(brain_pack, "ROOT", tmp), mock.patch.object(brain_pack, "MEMORY", os.path.join(tmp, "memory")):
            text = "\n".join(brain_pack.queue_lines(NOW))
            self.assertIn("- 0 of 10 queued cards are in the lab; 10 waiting", text)
            self.assertEqual(text.count("- NEXT: "), 2, "literature quota: 2 a week")
            self.assertIn("- NEXT: R4-BBRSI@1.0", text)
            pasted = yaml.safe_load(text.split("```yaml\n")[1].split("\n```")[0])[0]
            self.assertEqual(pasted, IQ.ready(QUEUE[0], NOW.date()))
            with open(lab, "a") as f:                                   # two literature cards added this week
                f.write(test_lab.dump([IQ.ready(QUEUE[0], NOW.date()), IQ.ready(QUEUE[1], NOW.date())]))
            text = "\n".join(brain_pack.queue_lines(NOW))
            self.assertIn("- 2 of 10 queued cards are in the lab; 8 waiting", text)
            self.assertIn("nothing to add now: the literature quota", text)
            later = "\n".join(brain_pack.queue_lines(NOW + dt.timedelta(days=7)))
            self.assertIn("- NEXT: R4-HLHB@1.0", later)

    def test_task_and_sources(self):
        self.assertIn("idea queue", test_brain.read(os.path.join(ROOT, "tasks", "weekly_research.md")).lower())
        from engine import curriculum as CU
        self.assertIn("R4", CU.studied(test_brain.read(os.path.join(ROOT, "memory", "research_sources.md"))))


if __name__ == "__main__":
    unittest.main()
