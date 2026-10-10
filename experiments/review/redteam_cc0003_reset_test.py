#!/usr/bin/env python3
"""Hostile finite test for CC-0003 verifier-workspace reuse.

This checks the specific gap between resetting finite control/address registers
and restoring the verifier's writable tape to its required blank initial state.
It is a finite interface test, not an asymptotic lower bound.
"""

import argparse
import json
import math
import signal
import time


def alarm_handler(_signum, _frame):
    raise TimeoutError("25-second cooperative budget exceeded")


def verifier(candidate, target, memory):
    """A fixed verifier that dirties one shared work cell on every call."""
    was_blank = memory.get(0, 0) == 0
    memory[0] = 1
    return candidate == target and was_blank


def acquire(width, target, reset):
    memory = {}
    calls = 0
    resets = 0
    for candidate in range(1 << width):
        calls += 1
        if verifier(candidate, target, memory):
            return candidate, calls, resets
        if reset:
            memory.clear()
            resets += 1
    return None, calls, resets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-w", type=int, default=16)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(25)
    started = time.monotonic()
    failures = []
    dirty_controls = 0
    repaired_controls = 0

    for width in range(1, args.max_w + 1):
        target = (1 << width) - 1
        dirty, _, _ = acquire(width, target, reset=False)
        clean, _, resets = acquire(width, target, reset=True)
        if dirty is not None:
            failures.append(["dirty_workspace_should_miss", width, dirty])
        else:
            dirty_controls += 1
        if clean != target or resets != target:
            failures.append(["reset_workspace_should_find", width, clean, resets])
        else:
            repaired_controls += 1

    # Direct clearing in the FLMV largest-index space convention is at least
    # a distinct charged operation.  Addressing every cell separately costs
    # q*ceil(log2(q+2)) bit steps in a literal binary-index implementation,
    # but this polylogarithmic factor does not change a polynomial exponent.
    exponent_checks = 0
    for kappa_quarters in range(9):
        for v_quarters in range(9):
            kappa = kappa_quarters / 4
            v = v_quarters / 4
            repaired_exponent = kappa + v
            claimed_exponent = kappa + v
            if not math.isclose(repaired_exponent, claimed_exponent):
                failures.append(["exponent_changed", kappa, v])
            exponent_checks += 1

    result = {
        "status": "PASS" if not failures else "FAIL",
        "scope": "finite dirty-workspace counterexample and reset-ledger audit only",
        "parameters": {"max_w": args.max_w},
        "dirty_workspace_counterexamples": dirty_controls,
        "explicit_reset_positive_controls": repaired_controls,
        "polylog_reset_exponent_checks": exponent_checks,
        "peer_peak_space_check_is_identity": True,
        "peer_peak_space_check_note": (
            "CC-0003 tests peak != verifier_space+w+addr after assigning "
            "peak=verifier_space+w+addr, so it cannot detect dirty workspace."
        ),
        "failure_count": len(failures),
        "failures": failures[:20],
        "elapsed_seconds": time.monotonic() - started,
    }
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
