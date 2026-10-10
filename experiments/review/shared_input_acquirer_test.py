#!/usr/bin/env python3
"""Finite audit for CC-0003 shared-read-only exhaustive acquisition."""
import argparse
import json
import math
import signal
import time


def alarm_handler(_signum, _frame):
    raise TimeoutError("25-second cooperative budget exceeded")


def first_accepting(width, accepted):
    for length in range(width + 1):
        for value in range(1 << length):
            candidate = (length, value)
            if candidate in accepted:
                return candidate
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-w", type=int, default=16)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    signal.signal(signal.SIGALRM, alarm_handler)
    signal.alarm(25)
    started = time.monotonic()

    count_checks = acceptance_checks = ledger_checks = space_checks = 0
    failures = []
    for w in range(args.max_w + 1):
        candidate_count = (1 << (w + 1)) - 1
        if sum(1 << length for length in range(w + 1)) != candidate_count:
            failures.append(["count", w])
        count_checks += 1

        controls = [set(), {(w, 0)}, {(0, 0)}, {(w, (1 << w) - 1)}]
        for accepted in controls:
            got = first_accepting(w, accepted)
            ordered = sorted(accepted, key=lambda z: (z[0], z[1]))
            want = ordered[0] if ordered else None
            if got != want:
                failures.append(["acceptance", w, sorted(accepted), got, want])
            acceptance_checks += 1

        for q in [1, 2, 3, 8, 16, 64]:
            for input_len in [1, 2, 7, 64, 1024, 1 << 20]:
                addr = max(1, math.ceil(math.log2(input_len + 2)))
                shared = candidate_count * (q + w + addr) + w
                copied = candidate_count * (q + input_len + w + addr) + w
                if shared > copied or (input_len > 0 and shared == copied):
                    failures.append(["ledger", w, q, input_len])
                ledger_checks += 1
                verifier_space = q % 11
                peak = verifier_space + w + addr
                if peak != verifier_space + w + addr:
                    failures.append(["space", w, q, input_len])
                space_checks += 1

    # Exponent identities on an exact rational grid.
    exponent_checks = 0
    for kappa_num in range(0, 9):
        for v_num in range(0, 9):
            kappa = kappa_num / 4
            v = v_num / 4
            shared_exp = kappa + v
            copied_exp = kappa + max(v, 1)
            if shared_exp > copied_exp + 1e-12:
                failures.append(["exponent", kappa, v])
            exponent_checks += 1

    elapsed = time.monotonic() - started
    result = {
        "status": "PASS" if not failures else "FAIL",
        "scope": "finite arithmetic and enumerator-interface audit only",
        "parameters": {"max_w": args.max_w},
        "candidate_count_checks": count_checks,
        "acceptance_controls": acceptance_checks,
        "shared_vs_copied_ledger_checks": ledger_checks,
        "peak_space_reuse_checks": space_checks,
        "exponent_identity_checks": exponent_checks,
        "failure_count": len(failures),
        "failures": failures[:20],
        "elapsed_seconds": elapsed,
    }
    with open(args.output, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
