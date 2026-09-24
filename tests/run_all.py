#!/usr/bin/env python3
"""Run every test file, several at a time (one process each), slowest first.

Same tests as `python -m unittest discover -s tests` - only faster: the end-to-end tests run the whole
scanner offline and take most of the time, so they run in parallel on the machine's CPUs.
Files in the same GROUP run in one process, so they can share one offline scanner run
(tests/test_data_quality.py -> shared_offline_run).

Run:  python tests/run_all.py            (exit code 0 = everything passed)
"""
import glob
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
# slowest first (measured); files not listed run afterwards, one process each
GROUPS = [["test_universe"], ["test_research"], ["test_data_quality"], ["test_regime"], ["test_positions"],
          ["test_features", "test_smc", "test_timeframes", "test_strategy_spec"]]


def run(group):
    t = time.time()
    p = subprocess.run([sys.executable, "-m", "unittest", "-v", *group], cwd=HERE, capture_output=True, text=True)
    return group, p.returncode, p.stdout + p.stderr, time.time() - t


def main():
    found = sorted(os.path.basename(f)[:-3] for f in glob.glob(os.path.join(HERE, "test_*.py")))
    listed = {m for g in GROUPS for m in g}
    missing = listed - set(found)
    if missing:
        sys.exit(f"run_all.py lists test files that do not exist: {sorted(missing)}")
    groups = GROUPS + [[m] for m in found if m not in listed]
    workers = max(2, min(len(groups), os.cpu_count() or 2))
    start, failed = time.time(), []
    with ThreadPoolExecutor(workers) as pool:
        for group, code, out, secs in pool.map(run, groups):
            status = "OK" if code == 0 else "FAILED"
            print(f"\n===== {' + '.join(group)}: {status} ({secs:.0f} s) =====")
            print(out.rstrip())
            if code != 0:
                failed.append(" + ".join(group))
    print(f"\n===== {len(groups)} groups, {len(found)} test files in {time.time() - start:.0f} s on {workers} "
          f"processes: {'ALL PASSED' if not failed else 'FAILED: ' + ', '.join(failed)} =====")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
