#!/usr/bin/env python3
"""Independent audit of the compact q=3 one-hot running-sum encoding.

This reconstructs the exact clause template stated in LSPV-3/530:
18 forbidden transition triples and one output ALO per running state,
plus a final unit. It does not implement or execute historical R_mix341.
"""

from __future__ import annotations

import itertools
import json
import resource
import time


def bits(mask: int) -> tuple[bool, bool, bool]:
    return tuple(bool(mask & (1 << i)) for i in range(3))  # type: ignore[return-value]


def onehot_mask(value: int) -> int:
    return 1 << value


def transition_satisfies(cur: int, inp: int, out: int, sign: int, drop=None) -> bool:
    """Evaluate 18 negative wrong-sum clauses plus output ALO.

    cur and inp are bit masks for three indicators. For the first transition,
    the caller maps the first input residue through its sign before passing it.
    """
    cb, ib, ob = bits(cur), bits(inp), bits(out)
    clause_index = 0
    for s, a, n in itertools.product(range(3), repeat=3):
        if n == (s + sign * a) % 3:
            continue
        if drop != ("wrong", clause_index):
            if cb[s] and ib[a] and ob[n]:
                return False
        clause_index += 1
    if drop != ("alo", 0) and not any(ob):
        return False
    return True


def chain_extensions(values, signs, target, drop=None):
    """Return all Boolean state-mask extensions satisfying the chain."""
    b = len(values)
    assert b >= 2 and len(signs) == b
    extensions = []
    for states in itertools.product(range(8), repeat=b - 1):
        cur0 = onehot_mask((signs[0] * values[0]) % 3)
        if not transition_satisfies(
            cur0,
            onehot_mask(values[1]),
            states[0],
            signs[1],
            drop if drop and drop[0] == 0 else None,
        ):
            continue
        ok = True
        for j in range(1, b - 1):
            local_drop = drop[1] if drop and drop[0] == j else None
            if not transition_satisfies(
                states[j - 1],
                onehot_mask(values[j + 1]),
                states[j],
                signs[j + 1],
                local_drop,
            ):
                ok = False
                break
        if ok and bits(states[-1])[target]:
            extensions.append(states)
    return extensions


def main():
    started = time.perf_counter()
    stage_checks = 0
    # Exact local semantics under promised one-hot current and input groups.
    for sign in (-1, 1):
        for s, a in itertools.product(range(3), repeat=2):
            sats = []
            for out in range(8):
                stage_checks += 1
                if transition_satisfies(onehot_mask(s), onehot_mask(a), out, sign):
                    sats.append(out)
            expected = onehot_mask((s + sign * a) % 3)
            assert sats == [expected], (sign, s, a, sats, expected)

    chain_cases = 0
    accepted = 0
    rejected = 0
    # Full Boolean auxiliary-state enumeration, not merely one-hot state tuples.
    for b in range(2, 6):
        for sign_style in (0, 1):
            signs = tuple(-1 if sign_style and i % 2 else 1 for i in range(b))
            for target in range(3):
                for values in itertools.product(range(3), repeat=b):
                    exts = chain_extensions(values, signs, target)
                    valid = sum(e * a for e, a in zip(signs, values)) % 3 == target
                    assert len(exts) == (1 if valid else 0), (b, signs, target, values, exts)
                    if valid:
                        accepted += 1
                        expected_states = []
                        running = (signs[0] * values[0]) % 3
                        for j in range(1, b):
                            running = (running + signs[j] * values[j]) % 3
                            expected_states.append(onehot_mask(running))
                        assert exts[0] == tuple(expected_states)
                    else:
                        rejected += 1
                    chain_cases += 1

    # Hostile deletions: each category has an explicit wrong-boundary witness.
    hostile = {}
    for category in ("alo", "wrong"):
        witness = None
        for b in range(3, 5):
            signs = (1,) * b
            for target in range(3):
                for values in itertools.product(range(3), repeat=b):
                    if sum(values) % 3 == target:
                        continue
                    max_index = 1 if category == "alo" else 18
                    for stage in range(b - 1):
                        for idx in range(max_index):
                            exts = chain_extensions(values, signs, target, (stage, (category, idx)))
                            if exts:
                                witness = {
                                    "b": b,
                                    "target": target,
                                    "values": values,
                                    "deleted_stage": stage,
                                    "deleted_facet": [category, idx],
                                    "state_masks": exts[0],
                                }
                                break
                        if witness:
                            break
                    if witness:
                        break
                if witness:
                    break
            if witness:
                break
        assert witness is not None, category
        hostile[category] = witness

    result = {
        "status": "PASS",
        "scope": "independent semantics of 18 wrong-sum clauses + output ALO per q=3 stage; no historical-checker claim",
        "stage_assignment_checks": stage_checks,
        "full_boolean_chain_cases": chain_cases,
        "accepted_unique_extensions": accepted,
        "rejected_wrong_boundary_tuples": rejected,
        "hostile_single_facet_deletion_witnesses": hostile,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
