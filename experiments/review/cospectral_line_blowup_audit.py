#!/usr/bin/env python3
"""COSPECBLOW1: bounded audit of a cospectral balanced 3-colouring source.

The two graph6 strings are entries 3138 and 3576 (one-based) in the
authors' cubic_graph16.g6 file for Yan--Wang, arXiv:2112.06112.  Their line
graphs are a 3-colourable / non-3-colourable cospectral pair.  Independent-
set blow-up supplies a growing connected regular pair.  This script audits
the exact identities and then looks for a polynomial promise-support leak.

Each --stage is designed to finish within 25 seconds.  No finite result is
used as an asymptotic lower bound.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from itertools import combinations, product
import hashlib
import json
from pathlib import Path
import random
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import universal22 as u
import image22_decoder_audit as image22

RUN_ID = "COSPECBLOW1"
SEED = 20261013
G6_YES = "O??CA?oB@PR?`_T?CWAA_"   # source cubic graph is 3-edge-colourable
G6_NO = "O??CA?oIC`B_@cX?OWAQ?"    # source cubic graph is not 3-edge-colourable
SOURCE_FILE_BLOB = "4012b66db46b56dfc9d0a4fba448ee32f7d909bc"
GRAPHLET_YES = 877
GRAPHLET_NO = 873


def parse_graph6(text: str) -> tuple[int, list[tuple[int, int]]]:
    if not text or text[0] == "~":
        raise ValueError("Only the small graph6 format is used here")
    n = ord(text[0]) - 63
    bits: list[int] = []
    for ch in text[1:]:
        x = ord(ch) - 63
        bits.extend((x >> k) & 1 for k in range(5, -1, -1))
    need = n * (n - 1) // 2
    if len(bits) < need:
        raise ValueError("Truncated graph6 string")
    edges: list[tuple[int, int]] = []
    p = 0
    for j in range(1, n):
        for i in range(j):
            if bits[p]:
                edges.append((i, j))
            p += 1
    return n, edges


def adjacency(n: int, edges: list[tuple[int, int]]) -> list[set[int]]:
    a = [set() for _ in range(n)]
    for x, y in edges:
        if x == y or not (0 <= x < n and 0 <= y < n):
            raise ValueError("Not a simple graph")
        a[x].add(y)
        a[y].add(x)
    if sum(map(len, a)) != 2 * len(set(tuple(sorted(e)) for e in edges)):
        raise ValueError("Duplicate edge")
    return a


def connected(a: list[set[int]]) -> bool:
    if not a:
        return False
    seen = {0}
    stack = [0]
    while stack:
        v = stack.pop()
        for w in a[v] - seen:
            seen.add(w)
            stack.append(w)
    return len(seen) == len(a)


def line_graph(n: int, edges: list[tuple[int, int]]) -> tuple[int, list[tuple[int, int]]]:
    del n
    out = []
    endpoint = [set(e) for e in edges]
    for i in range(len(edges)):
        for j in range(i):
            if endpoint[i] & endpoint[j]:
                out.append((j, i))
    return len(edges), out


def blowup(n: int, edges: list[tuple[int, int]], r: int) -> tuple[int, list[tuple[int, int]]]:
    if r < 1:
        raise ValueError("Positive blow-up required")
    out = []
    for x, y in edges:
        for i in range(r):
            for j in range(r):
                out.append((x * r + i, y * r + j))
    return n * r, out


def permute_graph(n: int, edges: list[tuple[int, int]], rng: random.Random) -> tuple[int, list[tuple[int, int]]]:
    p = list(range(n))
    rng.shuffle(p)
    return n, [tuple(sorted((p[x], p[y]))) for x, y in edges]


def three_colour(a: list[set[int]]) -> list[int] | None:
    n = len(a)
    colour = [-1] * n

    def search(done: int) -> bool:
        if done == n:
            return True
        uncoloured = [v for v in range(n) if colour[v] < 0]
        v = max(uncoloured, key=lambda x: (len({colour[w] for w in a[x] if colour[w] >= 0}), len(a[x]), -x))
        forbidden = {colour[w] for w in a[v] if colour[w] >= 0}
        for c in range(3):
            if c in forbidden:
                continue
            colour[v] = c
            if search(done + 1):
                return True
        colour[v] = -1
        return False

    return colour if search(0) else None


def matmul(x: list[list[int]], y: list[list[int]]) -> list[list[int]]:
    n = len(x)
    out = [[0] * n for _ in range(n)]
    for i, row in enumerate(x):
        for k, z in enumerate(row):
            if z:
                yk = y[k]
                for j in range(n):
                    out[i][j] += z * yk[j]
    return out


def power_traces(a: list[set[int]]) -> list[int]:
    n = len(a)
    base = [[int(j in a[i]) for j in range(n)] for i in range(n)]
    power = [row[:] for row in base]
    traces = []
    for _ in range(1, n + 1):
        traces.append(sum(power[i][i] for i in range(n)))
        power = matmul(power, base)
    return traces


def one_wl_cell_sizes(a: list[set[int]]) -> list[int]:
    colours = [0] * len(a)
    while True:
        keys = [(colours[v], tuple(sorted(colours[w] for w in a[v]))) for v in range(len(a))]
        names = {key: i for i, key in enumerate(sorted(set(keys)))}
        nxt = [names[key] for key in keys]
        if nxt == colours:
            break
        colours = nxt
    return sorted(Counter(colours).values())


def false_twin_quotient(a: list[set[int]]) -> tuple[list[list[int]], list[set[int]]]:
    groups: dict[tuple[int, ...], list[int]] = defaultdict(list)
    for v in range(len(a)):
        groups[tuple(sorted(a[v]))].append(v)
    classes = list(groups.values())
    owner = {}
    for i, cls in enumerate(classes):
        for v in cls:
            owner[v] = i
    q = [set() for _ in classes]
    for v in range(len(a)):
        for w in a[v]:
            if owner[v] != owner[w]:
                q[owner[v]].add(owner[w])
    return classes, q


def graphlet7_count(a: list[set[int]]) -> int:
    """Count induced 7-sets with degree multiset 0,2,2,2,2,2,2."""
    total = 0
    for ss in combinations(range(len(a)), 7):
        S = set(ss)
        degrees = sorted(len(a[v] & S) for v in ss)
        if degrees == [0, 2, 2, 2, 2, 2, 2]:
            total += 1
    return total


def promise_classifier(n: int, edges: list[tuple[int, int]]) -> str:
    a = adjacency(n, edges)
    classes, q = false_twin_quotient(a)
    if len(q) != 24 or len(set(map(len, classes))) != 1:
        return "OFF_PROMISE"
    f = graphlet7_count(q)
    if f == GRAPHLET_YES:
        return "YES"
    if f == GRAPHLET_NO:
        return "NO"
    return "OFF_PROMISE"


def exact22(comp: u.Compiled) -> bool:
    counts = Counter(l for c in comp.clauses for l in c)
    return all(counts[x] == 2 and counts[-x] == 2 for x in range(1, comp.n + 1))


def run_base(check, rng: random.Random) -> dict:
    cubic = [parse_graph6(G6_YES), parse_graph6(G6_NO)]
    lines = [line_graph(*g) for g in cubic]
    labels = ["YES", "NO"]
    base_rows = []
    for label, (n, e), (ln, le) in zip(labels, cubic, lines):
        a = adjacency(n, e)
        la = adjacency(ln, le)
        check(n == 16 and len(e) == 24 and set(map(len, a)) == {3}, "cubic_counts")
        check(connected(a), "cubic_connected")
        check(ln == 24 and len(le) == 48 and set(map(len, la)) == {4}, "line_counts")
        check(connected(la), "line_connected")
        colouring = three_colour(la)
        check((colouring is not None) == (label == "YES"), "line_chromatic_label")
        base_rows.append({"label": label, "three_colourable": colouring is not None})
    traces = [power_traces(adjacency(*g)) for g in lines]
    check(traces[0] == traces[1], "line_exact_power_traces")
    fingerprints = [graphlet7_count(adjacency(*g)) for g in lines]
    check(fingerprints == [GRAPHLET_YES, GRAPHLET_NO], "graphlet7_fingerprint")

    rows = []
    # Four logarithmically spaced sizes and one independent relabelling per
    # side keep this stage below the 25-second cooperative budget.
    for r in (1, 2, 4, 8):
        for label, base in zip(labels, lines):
            bn, be = blowup(*base, r)
            a = adjacency(bn, be)
            check(bn == 24 * r and len(be) == 48 * r * r, "blowup_counts")
            check(set(map(len, a)) == {4 * r}, "blowup_regular")
            check(connected(a), "blowup_connected")
            check(one_wl_cell_sizes(a) == [24 * r], "one_wl_single_cell")
            classes, q = false_twin_quotient(a)
            check(len(q) == 24 and set(map(len, classes)) == {r}, "twin_quotient_shape")
            check(graphlet7_count(q) == (GRAPHLET_YES if label == "YES" else GRAPHLET_NO),
                  "quotient_fingerprint")
            check(promise_classifier(bn, be) == label, "promise_classifier")
            for _ in range(1):
                pn, pe = permute_graph(bn, be, rng)
                check(promise_classifier(pn, pe) == label, "relabel_invariance")
            rows.append({"r": r, "label": label, "vertices": bn, "edges": len(be),
                         "degree": 4 * r, "wl_cells": [24 * r],
                         "quotient_graphlet7": GRAPHLET_YES if label == "YES" else GRAPHLET_NO})
    check(promise_classifier(5, [(i, i + 1) for i in range(4)]) == "OFF_PROMISE", "off_promise_path")
    check(promise_classifier(5, [(i, (i + 1) % 5) for i in range(5)]) == "OFF_PROMISE", "off_promise_cycle")
    return {"source_blob": SOURCE_FILE_BLOB, "base": base_rows,
            "line_power_traces": traces[0], "graphlet7": fingerprints,
            "blowups": rows,
            "symbolic_identities": {
                "line_spectrum": "Spec(L(G))={lambda+1:lambda in Spec(G)} union {-2}^8 for cubic order 16",
                "blowup_spectrum": "Spec(B_r(K))={r*mu:mu in Spec(K)} union {0}^{24(r-1)}",
                "chromatic": "chi(B_r(K))=chi(K)"
            }}


def run_target(check, label: str) -> dict:
    source = parse_graph6(G6_YES if label == "YES" else G6_NO)
    ln, le = line_graph(*source)
    colour = three_colour(adjacency(ln, le))
    check((colour is not None) == (label == "YES"), "source_label")
    raw = u.colouring_cnf(ln, le)
    proper, pmap = u.properize23(raw)
    comp = u.compile22(proper)
    check(comp.n == 1008 * ln + 1188 * len(le), "target_variable_formula")
    check(len(comp.clauses) == 1344 * ln + 1584 * len(le), "target_clause_formula")
    check(u.check_proper(comp.clauses) == comp.n, "target_proper_distinct")
    check(exact22(comp), "target_exact_signed_occurrences")
    encoded = image22.encode(comp.clauses)
    decoded = image22.decode_image(encoded)
    check(decoded is not None and decoded.balanced == comp.balanced, "ordered_decoder_roundtrip")
    check(image22.decode_image(bytes(bytearray(encoded))) is not None, "copy_wrapper")
    check(image22.decode_image(encoded + b" ") is None, "byte_padding_rejected")
    swapped = list(comp.clauses)
    mb = len(comp.balanced)
    swapped[mb], swapped[mb + 1] = swapped[mb + 1], swapped[mb]
    check(image22.decode_image(image22.encode(swapped)) is None, "clause_order_scope")
    duplicated = list(comp.clauses) + [comp.clauses[0]]
    try:
        u.check_proper(duplicated)
        duplicate_rejected = False
    except ValueError:
        duplicate_rejected = True
    check(duplicate_rejected, "duplicate_clause_rejected")
    if colour is not None:
        values = {3 * v + k + 1: int(colour[v] == k) for v in range(ln) for k in range(3)}
        pv = {x: values[y] if y else 0 for x, y in pmap.items()}
        check(u.eval_cnf(raw, values), "yes_graph_witness")
        check(u.eval_cnf(proper, pv), "yes_proper_witness")
        check(u.eval_cnf(comp.clauses, u.lift(comp, pv)), "yes_target_witness")
    return {"label": label, "source_vertices": ln, "source_edges": len(le),
            "source_clauses": len(raw), "proper_clauses": len(proper),
            "target_variables": comp.n, "target_clauses": len(comp.clauses),
            "encoded_bytes": len(encoded), "ordered_decoder": True,
            "three_colourable": colour is not None}


def brute_sat(cnf: u.CNF) -> bool:
    n = max(abs(l) for c in cnf for l in c)
    return any(u.eval_cnf(cnf, dict(enumerate(bits, 1))) for bits in product((0, 1), repeat=n))


def run_easy(check) -> dict:
    two, _ = u.properize23([(1, 2), (-1, 2)])
    affine = [tuple((j + 1) * (1 if b[j] == 0 else -1) for j in range(3))
              for b in product((0, 1), repeat=3) if sum(b) % 2]
    cases = {
        "horn": [(1, -2, -3), (-1, 2, -3), (-1, -2, 3)],
        "two_sat": two,
        "affine_tseitin": affine,
        "bounded_treewidth_chain": [(1, 2, 3), (-2, 3, 4), (-3, 4, 5)],
        "independent_product": [(1, 2, 3), (4, 5, 6)],
        "transparent_padding": [(1, 2, 3)] + u.pad7(1, 4),
    }
    rows = []
    for name, formula in cases.items():
        sat = brute_sat(formula)
        comp = u.compile22(formula)
        check(exact22(comp), "easy_exact22")
        check(u.check_proper(comp.clauses) == comp.n, "easy_proper")
        check(any(u.eval_cnf(comp.clauses, u.lift(comp, dict(enumerate(bits, 1))))
                  for bits in product((0, 1), repeat=comp.source_n)) == sat,
              "easy_semantics")
        rows.append({"case": name, "satisfiable": sat, "target_n": comp.n,
                     "target_m": len(comp.clauses),
                     "claimed_hard": False})
    return {"cases": rows,
            "note": "These are finite hostile controls only; each retains its known direct shortcut."}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=("base", "target-yes", "target-no", "easy"), required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    start = time.monotonic()
    deadline = start + 25.0
    checks: Counter[str] = Counter()

    def check(condition: bool, group: str) -> None:
        if time.monotonic() > deadline:
            raise TimeoutError("25-second cooperative budget exceeded")
        checks[group] += 1
        if not condition:
            raise AssertionError((group, checks[group]))

    result = {"run_id": RUN_ID, "stage": args.stage, "seed": SEED, "status": "RUNNING"}
    try:
        rng = random.Random(SEED)
        if args.stage == "base":
            data = run_base(check, rng)
        elif args.stage == "target-yes":
            data = run_target(check, "YES")
        elif args.stage == "target-no":
            data = run_target(check, "NO")
        else:
            data = run_easy(check)
        result.update(status="COMPUTATIONAL", all_checks_passed=True, data=data)
    except Exception as exc:
        result.update(status="FAILED_TEST", all_checks_passed=False, error=repr(exc))
        raise
    finally:
        result.update(assertions=sum(checks.values()), checks_by_group=dict(checks),
                      elapsed_seconds=time.monotonic() - start,
                      script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: result[k] for k in
                      ("stage", "status", "all_checks_passed", "assertions", "elapsed_seconds")},
                     sort_keys=True))


if __name__ == "__main__":
    main()
