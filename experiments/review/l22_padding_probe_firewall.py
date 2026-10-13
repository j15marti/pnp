#!/usr/bin/env python3
"""Finite audit of legal L22 padding against a block-probe length inference.

The symbolic point proved in the accompanying report is that adjoining
variable-disjoint satisfiable exact-(2,2) components preserves L22 membership
while increasing the canonical byte length.  This script checks the actual
repository compiler, syntax, labels, byte-difference sets, and hostile controls
on bounded instances.  It supplies no asymptotic lower bound.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path

import universal22 as u


RUN_ID = "PADPROBEFW1"
DEADLINE_SECONDS = 25.0
OUT = Path("results/raw/review/2026-10-13_1538_l22_padding_probe_firewall.json")

Y_EDGES = ((0, 2), (0, 3), (0, 5), (1, 2), (1, 3), (1, 4), (2, 3))
N_EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (4, 5))
PAD_SOURCE = [(1, 2, 3)]


def check(condition: bool, label: str, counts: Counter) -> None:
    if not condition:
        raise AssertionError(label)
    counts["assertions"] += 1


def three_colourings(edges: tuple[tuple[int, int], ...]) -> list[tuple[int, ...]]:
    return [c for c in itertools.product(range(3), repeat=6)
            if all(c[a] != c[b] for a, b in edges)]


def base_source(edges: tuple[tuple[int, int], ...]) -> u.CNF:
    cnf, _ = u.properize23(u.colouring_cnf(6, edges))
    return cnf


def offset(cnf: u.CNF, amount: int) -> u.CNF:
    return [tuple((abs(x) + amount) * (1 if x > 0 else -1) for x in c)
            for c in cnf]


def repeated_source(k: int, bad: int | None, y: u.CNF, n: u.CNF) -> u.CNF:
    width = u.check_proper(y)
    assert u.check_proper(n) == width and len(y) == len(n)
    out: u.CNF = []
    for i in range(k):
        out.extend(offset(n if i == bad else y, i * width))
    return out


def append_components(base: u.CNF, base_n: int, component: u.CNF,
                      component_n: int, copies: int) -> u.CNF:
    out = list(base)
    for j in range(copies):
        out.extend(offset(component, base_n + j * component_n))
    return out


def encode(cnf: u.CNF, pretty: bool = False) -> bytes:
    kwargs = {"ensure_ascii": True}
    if pretty:
        kwargs["indent"] = 2
    else:
        kwargs["separators"] = (",", ":")
    return json.dumps(cnf, **kwargs).encode("ascii")


def exact22(cnf: u.CNF) -> bool:
    try:
        n = u.check_proper(cnf)
    except ValueError:
        return False
    counts = Counter(x for c in cnf for x in c)
    return all(counts[x] == counts[-x] == 2 for x in range(1, n + 1))


def sat_bruteforce(cnf: list[tuple[int, ...]]) -> bool:
    n = max((abs(x) for c in cnf for x in c), default=0)
    return any(all(any(bits[abs(x) - 1] == (x > 0) for x in c) for c in cnf)
               for bits in itertools.product((False, True), repeat=n))


def affine_consistent(rows: list[tuple[int, int]]) -> bool:
    pivots: dict[int, tuple[int, int]] = {}
    for mask, rhs in rows:
        while mask:
            p = mask.bit_length() - 1
            if p not in pivots:
                pivots[p] = (mask, rhs)
                break
            mask ^= pivots[p][0]
            rhs ^= pivots[p][1]
        if not mask and rhs:
            return False
    return True


def phase_switch(cnf: u.CNF, flipped: set[int]) -> u.CNF:
    return [tuple(-x if abs(x) in flipped else x for x in c) for c in cnf]


def hostile_controls(counts: Counter) -> None:
    two_sat_yes = [(1, 2), (-1, 2), (1, -2)]
    two_sat_no = two_sat_yes + [(-1, -2)]
    check(sat_bruteforce(two_sat_yes), "2SAT yes", counts)
    check(not sat_bruteforce(two_sat_no), "2SAT no", counts)

    horn_yes = [(-1, 2), (-2, 3), (1,)]
    horn_no = horn_yes + [(-3,)]
    check(sat_bruteforce(horn_yes), "Horn yes", counts)
    check(not sat_bruteforce(horn_no), "Horn no", counts)

    check(affine_consistent([(0b011, 0), (0b110, 1)]), "affine yes", counts)
    check(not affine_consistent([(0b011, 0), (0b011, 1)]), "affine no", counts)

    for n in range(2, 10):
        allowed = {(False, False), (False, True), (True, False)}
        states = {False, True}
        for _ in range(n - 1):
            states = {b for a in states for b in (False, True) if (a, b) in allowed}
        check(bool(states), f"path DP {n}", counts)

    base = [(1, 2), (-1, 2)]
    check(sat_bruteforce(base) == sat_bruteforce(base + [base[0], base[1]]),
          "redundant clauses", counts)
    check(sat_bruteforce(base) == sat_bruteforce(base + [(3, -3)]),
          "tautology padding", counts)

    compact = json.dumps(base, separators=(",", ":"))
    pretty = json.dumps(base, indent=2)
    check(json.loads(compact) == json.loads(pretty), "alternate encoding", counts)
    check(bytes(bytearray(compact.encode())) == compact.encode(), "COPY wrapper", counts)
    check(json.dumps(json.loads(compact), separators=(",", ":")) == compact,
          "INTERP wrapper", counts)
    check((compact + "#dead").startswith(compact), "DEAD wrapper", counts)

    switched = phase_switch(PAD_SOURCE, {1, 3})
    check(sat_bruteforce(PAD_SOURCE) == sat_bruteforce(switched),
          "phase switch", counts)
    permuted = [(3, 1, 2)]
    check(sat_bruteforce(PAD_SOURCE) == sat_bruteforce(permuted),
          "variable permutation", counts)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    started = time.monotonic()
    counts = Counter()
    hostile_controls(counts)

    y_cols = three_colourings(Y_EDGES)
    n_cols = three_colourings(N_EDGES)
    check(len(y_cols) == 24, "Y fingerprint", counts)
    check(len(n_cols) == 0, "N fingerprint", counts)

    y = base_source(Y_EDGES)
    n = base_source(N_EDGES)
    check(len(y) == len(n) == 84, "source clauses", counts)
    check(u.check_proper(y) == u.check_proper(n) == 57, "source variables", counts)

    pad = u.compile22(PAD_SOURCE)
    check(exact22(pad.clauses), "padding exact22", counts)
    check(u.eval_cnf(pad.clauses, u.lift(pad, {1: 1, 2: 0, 3: 0})),
          "padding satisfiable", counts)

    rows = []
    for r in range(1, 4):
        if time.monotonic() - started > DEADLINE_SECONDS:
            raise TimeoutError("cooperative 25-second deadline exceeded")
        good_comp = u.compile22(repeated_source(r, None, y, n))
        bad_comps = [u.compile22(repeated_source(r, i, y, n)) for i in range(r)]
        base_good = encode(good_comp.clauses)
        base_diffs = [
            {j for j, (a, b) in enumerate(zip(base_good, encode(b.clauses))) if a != b}
            for b in bad_comps
        ]
        check(all(base_diffs), f"nonempty diff sets r={r}", counts)
        for i in range(r):
            for j in range(i + 1, r):
                check(base_diffs[i].isdisjoint(base_diffs[j]),
                      f"disjoint r={r} i={i} j={j}", counts)

        for s in (0, 1, 2, 4, 8, 16):
            good = append_components(good_comp.clauses, good_comp.n,
                                     pad.clauses, pad.n, s)
            bads = [append_components(b.clauses, b.n, pad.clauses, pad.n, s)
                    for b in bad_comps]
            check(exact22(good), f"good exact22 r={r} s={s}", counts)
            check(all(exact22(b) for b in bads), f"bad exact22 r={r} s={s}", counts)
            good_bytes = encode(good)
            diff_sets = []
            for i, bad in enumerate(bads):
                bad_bytes = encode(bad)
                check(len(good_bytes) == len(bad_bytes),
                      f"equal lengths r={r} s={s} i={i}", counts)
                diffs = {j for j, (a, b) in enumerate(zip(good_bytes, bad_bytes))
                         if a != b}
                check(diffs == base_diffs[i],
                      f"padding preserves diff set r={r} s={s} i={i}", counts)
                diff_sets.append(diffs)
            for i in range(r):
                for j in range(i + 1, r):
                    check(diff_sets[i].isdisjoint(diff_sets[j]),
                          f"padded disjoint r={r} s={s} i={i} j={j}", counts)

            decoded = json.loads(good_bytes)
            check(encode(decoded) == good_bytes, f"decode/re-encode r={r} s={s}", counts)
            check(json.loads(encode(good, pretty=True)) == decoded,
                  f"pretty alternate r={r} s={s}", counts)

            rows.append({
                "blocks": r,
                "padding_components": s,
                "encoded_bytes": len(good_bytes),
                "target_variables": good_comp.n + s * pad.n,
                "target_clauses": len(good_comp.clauses) + s * len(pad.clauses),
                "certified_required_hits": r,
                "different_bytes_per_bad_block": [len(d) for d in diff_sets],
                "certified_hits_over_bytes": r / len(good_bytes),
            })

    # One fixed hard-looking core can be inflated without increasing its
    # certified number of disjoint sensitive blocks.
    fixed = [row for row in rows if row["blocks"] == 1]
    check(all(row["certified_required_hits"] == 1 for row in fixed),
          "fixed core bound constant", counts)
    check(all(fixed[i]["encoded_bytes"] < fixed[i + 1]["encoded_bytes"]
              for i in range(len(fixed) - 1)),
          "fixed core length increases", counts)
    check(fixed[-1]["certified_hits_over_bytes"] < fixed[0]["certified_hits_over_bytes"],
          "probe density diluted", counts)

    elapsed = time.monotonic() - started
    payload = {
        "run_id": RUN_ID,
        "status": "COMPUTATIONAL",
        "method": "actual graph-colouring/properize23/compile22 pipeline plus legal exact-(2,2) disjoint-union padding",
        "seed": None,
        "padding_component": {
            "source": PAD_SOURCE,
            "target_variables": pad.n,
            "target_clauses": len(pad.clauses),
            "satisfiable": True,
        },
        "counts": dict(counts),
        "rows": rows,
        "elapsed_seconds": elapsed,
        "limitations": [
            "Finite implementation evidence only; the padding lemma is proved symbolically in the report.",
            "The audit preserves the original byte-query adversary on each fixed unpadded core.",
            "It refutes only a total-length or padding-robust inference from that adversary, not the family-specific Omega(N/log N) theorem.",
            "No superpolynomial whole-machine lower bound follows.",
        ],
    }
    semantic = dict(payload)
    semantic.pop("elapsed_seconds")
    payload["semantic_sha256"] = hashlib.sha256(
        json.dumps(semantic, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    payload["script_sha256"] = sha256(Path(__file__))
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

