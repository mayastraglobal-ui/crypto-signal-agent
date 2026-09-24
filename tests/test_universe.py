"""Phase 2 tests: tradable universe - eligibility rules, top 7 / top 10, 2-run hysteresis.

Run:  python -m unittest discover -s tests -v
"""
import json
import os
import sys
import tempfile
import unittest

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import universe as uni  # noqa: E402
from test_data_quality import run_copy  # noqa: E402

U = uni.settings(None)
MARKET = dict(quote="USDT", exclude_meme=["DOGE"], exclude_ai=["FET", "NEAR"],
              exclude_other=["USDC", "WBTC"], exclude_gold=["PAXG"])
ALWAYS = {"BTC", "ETH"}


def good_metrics(**over):
    m = dict(coin="AAA", vol_24h=200e6, vol_7d_avg=180e6, change_24h=2.0, listing_days=400,
             stable_dev_pct=15.0, spread_pct=0.01, depth_bid_usdt=2e6, depth_ask_usdt=2e6)
    m.update(over)
    return m


def elig(**over):
    data_state = over.pop("data_state", "GOOD")
    suspended = over.pop("suspended", False)
    return uni.eligibility(good_metrics(**over), U, 180, data_state, suspended)


class PreFilter(unittest.TestCase):
    def test_lists_leveraged_multiplier_and_volume_floor(self):
        t = lambda s, v=1e9: dict(symbol=s, quote_volume=v, change_pct=0, last=1)
        cands, excl = uni.prefilter([t("BTCUSDT", 2e9), t("DOGEUSDT"), t("NEARUSDT"), t("USDCUSDT"),
                                     t("PAXGUSDT"), t("ETHUPUSDT"), t("1000SATSUSDT"), t("SOLUSDT", 3e9),
                                     t("TINYUSDT", 1e6), t("BTCEUR", 5e9)], MARKET, U)
        self.assertEqual([c["base"] for c in cands], ["SOL", "BTC"])      # sorted by volume
        self.assertIn("meme", excl["DOGE"])
        self.assertIn("AI", excl["NEAR"])
        self.assertIn("stablecoin", excl["USDC"])
        self.assertIn("gold", excl["PAXG"])
        self.assertEqual(excl["ETHUP"], "leveraged token")
        self.assertIn("multiplier", excl["1000SATS"])
        self.assertNotIn("TINY", excl)                                     # below floor: not listed

    def test_pool_always_keeps_btc_eth_and_members(self):
        cands = [dict(base=f"C{i}", quote_volume=1e9 - i) for i in range(30)] + \
                [dict(base="BTC", quote_volume=1), dict(base="MEMBER", quote_volume=2)]
        pool = uni.candidate_pool(cands, ALWAYS | {"MEMBER"}, 20)
        names = [c["base"] for c in pool]
        self.assertEqual(len(names), 20)
        self.assertIn("BTC", names)
        self.assertIn("MEMBER", names)


class Measure(unittest.TestCase):
    def test_measure_spread_depth_volume_stable(self):
        n = 60
        daily = pd.DataFrame({"close": np.linspace(100, 130, n), "volume": 1.0,
                              "quote_volume": [1e6] * (n - 7) + [70e6] * 7})
        bids = [(99.5, 1000.0), (98.0, 1e6)]                 # 98 is outside 1% of the mid
        asks = [(100.5, 2000.0)]
        m = uni.measure(dict(base="X", quote_volume=90e6, change_pct=1.0), daily,
                        book=(99.9, 100.1), depth=(bids, asks), u=U)
        self.assertAlmostEqual(m["spread_pct"], 0.2, places=6)
        self.assertAlmostEqual(m["vol_7d_avg"], 70e6)
        self.assertAlmostEqual(m["depth_bid_usdt"], 99.5 * 1000)
        self.assertAlmostEqual(m["depth_ask_usdt"], 100.5 * 2000)
        self.assertGreater(m["stable_dev_pct"], 2)            # a trending coin is not a stablecoin

    def test_missing_book_and_depth_are_not_guessed(self):
        daily = pd.DataFrame({"close": [1.0] * 10, "volume": [1.0] * 10})
        m = uni.measure(dict(base="X", quote_volume=90e6, change_pct=0), daily, None, None, U)
        self.assertIsNone(m["spread_pct"])
        self.assertIsNone(m["depth_bid_usdt"])
        r = uni.eligibility(dict(m, vol_7d_avg=90e6), U, 5)
        self.assertIn("spread not available", r["flags"])
        self.assertNotIn("spread", r["codes"])


class Eligibility(unittest.TestCase):
    def test_good_coin_passes(self):
        r = elig()
        self.assertTrue(r["ok"], r)
        self.assertEqual(r["reasons"], [])

    def test_each_rule(self):
        cases = {
            "history": dict(listing_days=100),
            "volume_24h": dict(vol_24h=40e6, vol_7d_avg=45e6),
            "volume_7d": dict(vol_7d_avg=30e6),
            "volume_spike": dict(vol_24h=700e6, vol_7d_avg=200e6),
            "big_move": dict(change_24h=-26.0),
            "stablecoin": dict(stable_dev_pct=0.5),
            "spread": dict(spread_pct=0.2),
            "thin_book": dict(depth_ask_usdt=100e3),
            "data_unsafe": dict(data_state="UNSAFE"),
        }
        for code, over in cases.items():
            r = elig(**over)
            self.assertFalse(r["ok"], code)
            self.assertIn(code, r["codes"], (code, r))

    def test_suspended_for_rest_of_day_even_after_calming_down(self):
        r = elig(change_24h=3.0, suspended=True)
        self.assertFalse(r["ok"])
        self.assertIn("big_move", r["codes"])

    def test_degraded_data_is_flag_only(self):
        r = elig(data_state="DEGRADED")
        self.assertTrue(r["ok"])
        self.assertIn("data_degraded", r["flag_codes"])

    def test_wash_volume_is_flag_only(self):
        r = elig(vol_24h=600e6, vol_7d_avg=500e6, depth_bid_usdt=300e3, depth_ask_usdt=300e3)
        self.assertTrue(r["ok"])                               # operator decision: flag only
        self.assertIn("wash_volume", r["flag_codes"])

    def test_suspensions_last_until_end_of_utc_day(self):
        st, sus = uni.update_suspensions(uni.empty_state(), {"PUMP": 30.0, "BTC": 1.0}, U, "2026-09-24")
        self.assertEqual(sus, {"PUMP"})
        st, sus = uni.update_suspensions(st, {"PUMP": 5.0}, U, "2026-09-24")      # calmer, same day
        self.assertEqual(sus, {"PUMP"})
        st, sus = uni.update_suspensions(st, {"PUMP": 5.0}, U, "2026-09-25")      # next UTC day
        self.assertEqual(sus, set())


def names(n, prefix="C"):
    return [f"{prefix}{i}" for i in range(1, n + 1)]


class Membership(unittest.TestCase):
    """Hysteresis rules. Rankings are given directly (best first)."""

    def run_seq(self, rankings, state=None):
        st = state or uni.empty_state()
        out = []
        for r in rankings:
            st, ev, view = uni.update_membership(st, uni.rank(r, ALWAYS), U, ALWAYS)
            out.append((ev, view))
        return st, out

    def test_first_run_takes_top_7_and_next_3_are_research(self):
        _, [(ev, view)] = self.run_seq([["BTC", "ETH"] + names(10)])
        self.assertEqual(view["signal"], ["BTC", "ETH", "C1", "C2", "C3", "C4", "C5"])
        self.assertEqual(view["research_only"], ["C6", "C7", "C8"])
        self.assertEqual(len(view["research"]), 10)
        self.assertTrue(all(e["action"] == "JOIN" for e in ev))

    def test_newcomer_needs_2_runs_and_swaps_with_the_one_pushed_out(self):
        base = ["BTC", "ETH"] + names(8)
        new = ["BTC", "ETH", "NEW"] + names(8)                 # NEW pushes C5 to rank 8
        _, out = self.run_seq([base, new, new])
        ev2, v2 = out[1]
        self.assertNotIn("NEW", v2["signal"])                  # 1 run: not yet
        self.assertEqual(v2["waiting"], {"NEW": 1})
        self.assertIn("C5", v2["signal"])                       # 1 run outside: still a member
        self.assertEqual(v2["leaving"], {"C5": 1})
        self.assertEqual(ev2, [])
        ev3, v3 = out[2]
        self.assertIn("NEW", v3["signal"])
        self.assertNotIn("C5", v3["signal"])
        self.assertEqual(sorted(e["action"] + e["coin"] for e in ev3), ["JOINNEW", "LEAVEC5"])
        self.assertEqual(len(v3["signal"]), 7)

    def test_flicker_never_rotates(self):
        base = ["BTC", "ETH"] + names(8)
        new = ["BTC", "ETH", "NEW"] + names(8)
        _, out = self.run_seq([base, new, base, new, base])
        for ev, view in out[1:]:
            self.assertNotIn("NEW", view["signal"])
            self.assertIn("C5", view["signal"])
            self.assertEqual(ev, [])

    def test_ineligible_member_leaves_at_once_and_slot_waits(self):
        base = ["BTC", "ETH"] + names(8)
        without_c2 = ["BTC", "ETH"] + [c for c in names(8) if c != "C2"]   # C2 broke a rule
        st, out = self.run_seq([base])
        st, ev, view = uni.update_membership(st, uni.rank(without_c2, ALWAYS), U, ALWAYS,
                                             {"C2": ["24h move +30.0%"]})
        self.assertNotIn("C2", view["signal"])
        self.assertEqual(ev[0]["action"], "LEAVE")
        self.assertIn("+30.0%", ev[0]["why"])
        self.assertEqual(view["empty_slots"], 1)               # C6 must first prove itself
        self.assertEqual(view["waiting"], {"C6": 1})
        st, ev, view = uni.update_membership(st, uni.rank(without_c2, ALWAYS), U, ALWAYS)
        self.assertIn("C6", view["signal"])
        self.assertEqual(view["empty_slots"], 0)

    def test_member_back_in_top_after_one_run_stays(self):
        base = ["BTC", "ETH"] + names(8)
        new = ["BTC", "ETH", "NEW"] + names(8)
        st, out = self.run_seq([base, new, base])
        self.assertIn("C5", out[2][1]["signal"])
        self.assertEqual(out[2][1]["leaving"], {})             # streak reset

    def test_btc_returns_immediately_when_eligible_again(self):
        base = ["BTC", "ETH"] + names(8)
        no_btc = ["ETH"] + names(8)
        st, out = self.run_seq([base, no_btc, no_btc, no_btc, base])
        self.assertNotIn("BTC", out[1][1]["signal"])
        self.assertIn("C6", out[3][1]["signal"])               # C6 filled the slot after 2 runs
        ev, view = out[4]
        self.assertIn("BTC", view["signal"])                   # back at once, no waiting
        self.assertEqual(len(view["signal"]), 7)
        self.assertIn("LEAVEC6", [e["action"] + e["coin"] for e in ev])   # worst-ranked made room

    def test_remove_members(self):
        st, _ = self.run_seq([["BTC", "ETH"] + names(8)])
        st, ev = uni.remove_members(st, {"C1": "price data UNSAFE"})
        self.assertNotIn("C1", st["members"])
        self.assertEqual(ev[0]["why"], "price data UNSAFE")


class LogOnlyChanges(unittest.TestCase):
    def test_same_rule_failure_is_logged_once(self):
        st = uni.empty_state()
        st, ev = uni.eligibility_changes(st, {"X": elig(vol_24h=40e6, vol_7d_avg=45e6)})
        self.assertEqual([e["action"] for e in ev], ["EXCLUDED"])
        st, ev = uni.eligibility_changes(st, {"X": elig(vol_24h=41e6, vol_7d_avg=45e6)})  # new number
        self.assertEqual(ev, [])                                                          # same rule
        st, ev = uni.eligibility_changes(st, {"X": elig()})
        self.assertEqual([e["action"] for e in ev], ["ELIGIBLE"])
        st, ev = uni.eligibility_changes(st, {"X": elig()})
        self.assertEqual(ev, [])

    def test_flags_logged_once_and_not_available_never(self):
        wash = dict(vol_24h=600e6, vol_7d_avg=500e6, depth_bid_usdt=300e3, depth_ask_usdt=300e3)
        st, ev = uni.eligibility_changes(uni.empty_state(), {"X": elig(**wash)})
        self.assertEqual([e["action"] for e in ev], ["FLAG"])
        st, ev = uni.eligibility_changes(st, {"X": elig(**wash)})
        self.assertEqual(ev, [])
        st, ev = uni.eligibility_changes(st, {"Y": elig(spread_pct=None)})
        self.assertEqual(ev, [])


class EndToEnd(unittest.TestCase):
    """Several offline runs in a row with scenario files (synthetic data)."""

    def scan(self, tmp, scenario=None):
        args = ["scanner.py", "--offline"]
        if scenario is not None:
            path = os.path.join(tmp, "scenario.json")
            with open(path, "w") as f:
                json.dump(scenario, f)
            args += ["--scenario", path]
        p = run_copy(tmp, *args)
        self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        with open(os.path.join(tmp, "reports", "universe.json")) as f:
            u = json.load(f)
        with open(os.path.join(tmp, "reports", "latest.json")) as f:
            rep = json.load(f)
        return u, rep

    def test_rotation_over_three_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            u1, rep1 = self.scan(tmp)
            self.assertEqual(len(u1["signal"]), 7)
            self.assertEqual(len(u1["research_only"]), 3)
            self.assertEqual(set(rep1["coins_scanned"]), set(u1["signal"]) | set(u1["research_only"]))
            self.assertTrue({"BTC", "ETH"} <= set(u1["signal"]))
            outsider = u1["research_only"][-1]                  # rank 10: jumps to the top
            last_member = u1["signal"][-1]
            boost = {"quote_volume": {outsider: 5e9}}
            u2, _ = self.scan(tmp, boost)
            self.assertEqual(u2["waiting"], {outsider: 1})
            self.assertIn(last_member, u2["signal"])
            u3, rep3 = self.scan(tmp, boost)
            self.assertIn(outsider, u3["signal"])
            self.assertNotIn(last_member, u3["signal"])
            self.assertIn(last_member, u3["research_only"])
            for p in rep3["signals"]:                           # signals only from the signal 7
                self.assertIn(p["coin"], u3["signal"])
            self.assertFalse(os.path.exists(os.path.join(tmp, "memory", "universe_log.md")))  # offline

    def test_exclusions_show_reasons(self):
        with tempfile.TemporaryDirectory() as tmp:
            u, rep = self.scan(tmp, {"depth_usd": {"SOL": 100e3}, "daily_volume_factor": {"ADA": 0.2}})
            why = {c["coin"]: " ".join(c["reasons"]) for c in u["candidates"]}
            self.assertIn("too thin", why["SOL"])
            self.assertIn("spike", why["ADA"])
            self.assertIn("stablecoin", why["FAKEUSD"])
            self.assertIn("±25%", why["PUMP"])
            self.assertIn("180", why["NEWCOIN"])
            self.assertNotIn("SOL", u["signal"] + u["research_only"])
            self.assertIn("DOGE", u["excluded_by_list"])
            self.assertNotIn("SOL", rep["coins_scanned"])


class UniverseLogFile(unittest.TestCase):
    def test_log_is_append_only(self):
        import datetime as dt
        import scanner
        with tempfile.TemporaryDirectory() as tmp:
            old = scanner.MEMORY
            scanner.MEMORY = tmp
            try:
                t = dt.datetime(2026, 9, 24, 18, 7, tzinfo=dt.timezone.utc)
                scanner.write_universe_log([dict(coin="SOL", action="JOIN", why="top 7 for 2 runs")], t)
                scanner.write_universe_log([dict(coin="XRP", action="LEAVE", why="outside top 7")], t)
            finally:
                scanner.MEMORY = old
            with open(os.path.join(tmp, "universe_log.md")) as f:
                text = f.read()
        self.assertEqual(text.count("# Universe log"), 1)
        self.assertLess(text.index("**JOIN** SOL"), text.index("**LEAVE** XRP"))


if __name__ == "__main__":
    unittest.main()
