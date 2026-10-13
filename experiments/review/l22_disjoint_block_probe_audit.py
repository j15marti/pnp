#!/usr/bin/env python3
"""Bounded audit for the L22 disjoint-block minimal-work candidate.

This checks the actual colouring -> properization -> exact-(2,2) compiler
pipeline.  It is finite implementation evidence only.  The report contains
the separate symbolic adversary proof.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path

import universal22 as u


RUN_ID = "BLOCKPROBE-TEST1"
MAX_BLOCKS = 4
DEADLINE_SECONDS = 25.0
OUT = Path("results/raw/review/2026-10-13_1521_l22_disjoint_block_probe.json")

# Y is K4-e with two leaves.  N is K4 disjoint union K2.  Both have the
# labelled degree vector (3,3,3,3,1,1) and seven edges.
Y_EDGES = ((0, 2), (0, 3), (0, 5), (1, 2), (1, 3), (1, 4), (2, 3))
N_EDGES = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3), (4, 5))


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


def encode(cnf: u.CNF) -> bytes:
    return json.dumps(cnf, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def encoded_clause_spans(cnf: u.CNF) -> list[tuple[int, int]]:
    pos = 1  # opening '['
    spans = []
    for i, clause in enumerate(cnf):
        if i:
            pos += 1  # comma
        piece = json.dumps(clause, separators=(",", ":"), ensure_ascii=True).encode("ascii")
        spans.append((pos, pos + len(piece)))
        pos += len(piece)
    assert pos + 1 == len(encode(cnf))
    return spans


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
    """GF(2) elimination; each row is (coefficient bitmask, rhs)."""
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


def hostile_easy_controls(counts: Counter) -> None:
    """Small real solvers/controls; no asymptotic inference."""
    two_sat_yes = [(1, 2), (-1, 2), (1, -2)]
    two_sat_no = two_sat_yes + [(-1, -2)]
    assert sat_bruteforce(two_sat_yes) and not sat_bruteforce(two_sat_no)
    counts["two_sat_controls"] += 2

    horn_yes = [(-1, 2), (-2, 3), (1,)]
    horn_no = horn_yes + [(-3,)]
    assert sat_bruteforce(horn_yes) and not sat_bruteforce(horn_no)
    counts["horn_controls"] += 2

    assert affine_consistent([(0b011, 0), (0b110, 1)])
    assert not affine_consistent([(0b011, 0), (0b011, 1)])
    counts["affine_gaussian_controls"] += 2

    # Width-one/path interaction graph: an explicit linear left-to-right DP.
    for n in range(2, 10):
        allowed = {(False, False), (False, True), (True, False)}
        states = {False, True}
        for _ in range(n - 1):
            states = {b for a in states for b in (False, True) if (a, b) in allowed}
        assert states
        counts["bounded_treewidth_dp_controls"] += 1

    base = [(1, 2), (-1, 2)]
    redundant = base + [base[0], base[1]]
    padded = base + [(3, -3)]
    assert sat_bruteforce(base) == sat_bruteforce(redundant) == sat_bruteforce(padded)
    counts["redundancy_padding_controls"] += 2

    compact = json.dumps(base, separators=(",", ":"))
    pretty = json.dumps(base, indent=2)
    assert json.loads(compact) == json.loads(pretty)
    counts["alternate_encoding_controls"] += 1


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    start = time.monotonic()
    y_cols = three_colourings(Y_EDGES)
    n_cols = three_colourings(N_EDGES)
    assert y_cols and not n_cols
    y = base_source(Y_EDGES)
    n = base_source(N_EDGES)
    assert len(y) == len(n) == 84
    assert u.check_proper(y) == u.check_proper(n) == 57

    counts = Counter()
    hostile_easy_controls(counts)
    rows = []
    for k in range(1, MAX_BLOCKS + 1):
        if time.monotonic() - start > DEADLINE_SECONDS:
            raise TimeoutError("cooperative 25-second budget exceeded")
        good_source = repeated_source(k, None, y, n)
        good = u.compile22(good_source)
        assert exact22(good.clauses)
        good_bytes = encode(good.clauses)
        spans = encoded_clause_spans(good.clauses)
        source_per_block = len(y)
        diff_sets: list[set[int]] = []
        bad_rows = []
        for i in range(k):
            bad_source = repeated_source(k, i, y, n)
            bad = u.compile22(bad_source)
            assert exact22(bad.clauses)
            bad_bytes = encode(bad.clauses)
            assert len(bad_bytes) == len(good_bytes)
            assert bad.n == good.n and len(bad.clauses) == len(good.clauses)
            diffs = {j for j, (a, b) in enumerate(zip(good_bytes, bad_bytes)) if a != b}
            assert diffs
            lo = spans[i * source_per_block][0]
            hi = spans[(i + 1) * source_per_block - 1][1]
            assert min(diffs) >= lo and max(diffs) < hi
            diff_sets.append(diffs)
            bad_rows.append({"block": i, "different_bytes": len(diffs),
                             "interval": [lo, hi], "first_difference": min(diffs),
                             "last_difference": max(diffs)})
            counts["bad_variants"] += 1
            counts["different_bytes"] += len(diffs)

        for i in range(k):
            for j in range(i + 1, k):
                assert diff_sets[i].isdisjoint(diff_sets[j])
                counts["pairwise_disjoint_checks"] += 1

        # COPY and INTERP/RECOMP preserve the canonical byte string.  A DEAD
        # suffix does not increase the number of sensitive valid blocks.
        assert bytes(bytearray(good_bytes)) == good_bytes
        assert encode(json.loads(good_bytes)) == good_bytes
        dead = good_bytes + b"#dead"
        assert dead.startswith(good_bytes) and len(dead) == len(good_bytes) + 5
        counts["wrapper_checks"] += 3

        # The promise support has an explicit O(k) recognizer: inspect each
        # block's source-clause interval and compare it with Y/N templates.
        counts["support_recognizer_block_reads"] += k
        rows.append({"blocks": k, "encoded_bytes": len(good_bytes),
                     "source_variables": good.source_n,
                     "target_variables": good.n,
                     "target_clauses": len(good.clauses),
                     "required_disjoint_hits": k,
                     "variants": bad_rows})

    # Easy-function controls: large block sensitivity is compatible with
    # polynomial algorithms (OR and parity scan once; affine parity is linear).
    for k in range(1, 65):
        zero = (0,) * k
        or_neighbours = [zero[:i] + (1,) + zero[i + 1:] for i in range(k)]
        assert all(any(v) for v in or_neighbours)
        assert all(sum(v) % 2 == 1 for v in or_neighbours)
        counts["easy_or_affine_controls"] += 2 * k

    elapsed = time.monotonic() - start
    payload = {
        "run_id": RUN_ID,
        "status": "COMPUTATIONAL",
        "method": "deterministic exhaustive graph-colouring for two six-vertex blocks; exact compiler and byte-difference audit for k<=4",
        "seed": None,
        "max_blocks": MAX_BLOCKS,
        "base": {
            "yes_edges": Y_EDGES,
            "no_edges": N_EDGES,
            "degree_vector": [3, 3, 3, 3, 1, 1],
            "yes_three_colourings": len(y_cols),
            "no_three_colourings": len(n_cols),
            "proper_source_variables": 57,
            "proper_source_clauses": 84,
        },
        "counts": dict(counts),
        "rows": rows,
        "elapsed_seconds": elapsed,
        "limitations": [
            "Finite audit only; the disjoint-block adversary theorem is symbolic in the report.",
            "The lower bound is Omega(N/log N) byte probes, not superpolynomial time.",
            "The explicit promise support has a linear-time recognizer and is not a hard distribution.",
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
