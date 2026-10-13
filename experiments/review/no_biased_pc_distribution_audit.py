#!/usr/bin/env python3
"""Finite controls for the NO-biased graph-colouring PC distribution firewall."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import time
from pathlib import Path


def circulant_six_regular(n: int) -> set[tuple[int, int]]:
    assert n >= 8
    edges: set[tuple[int, int]] = set()
    for v in range(n):
        for step in (1, 2, 3):
            w = (v + step) % n
            edges.add(tuple(sorted((v, w))))
    assert all(sum(v in e for e in edges) == 6 for v in range(n))
    return edges


def switch_randomize(edges: set[tuple[int, int]], n: int, rng: random.Random) -> set[tuple[int, int]]:
    edges = set(edges)
    for _ in range(80 * n):
        e1, e2 = rng.sample(tuple(edges), 2)
        a, b = e1
        c, d = e2
        if len({a, b, c, d}) < 4:
            continue
        if rng.randrange(2):
            c, d = d, c
        f1, f2 = tuple(sorted((a, d))), tuple(sorted((c, b)))
        if f1 == f2 or f1 in edges or f2 in edges:
            continue
        edges.remove(e1)
        edges.remove(e2)
        edges.add(f1)
        edges.add(f2)
    assert len(edges) == 3 * n
    assert all(sum(v in e for e in edges) == 6 for v in range(n))
    return edges


def three_colourable(n: int, edges: set[tuple[int, int]]) -> bool:
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    colour = [-1] * n

    def search(done: int) -> bool:
        if done == n:
            return True
        uncoloured = [v for v in range(n) if colour[v] < 0]
        v = max(uncoloured, key=lambda x: (len({colour[w] for w in adj[x] if colour[w] >= 0}), len(adj[x])))
        forbidden = {colour[w] for w in adj[v] if colour[w] >= 0}
        for c in range(3):
            if c in forbidden:
                continue
            colour[v] = c
            if search(done + 1):
                return True
            colour[v] = -1
        return False

    return search(0)


def complete_tripartite(parts: int = 1) -> tuple[int, set[tuple[int, int]]]:
    n = 9 * parts
    edges: set[tuple[int, int]] = set()
    for block in range(parts):
        off = 9 * block
        groups = [range(off, off + 3), range(off + 3, off + 6), range(off + 6, off + 9)]
        for i in range(3):
            for j in range(i + 1, 3):
                for a in groups[i]:
                    for b in groups[j]:
                        edges.add((a, b))
    return n, edges


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--seed", type=int, default=220336)
    args = ap.parse_args()
    start = time.perf_counter()
    rng = random.Random(args.seed)
    assertions = 0
    failures: list[dict[str, object]] = []

    rows = []
    for n in (8, 10, 12, 14, 16, 18):
        sat = 0
        trials = 32
        for _ in range(trials):
            edges = switch_randomize(circulant_six_regular(n), n, rng)
            assertions += 3
            if len(edges) != 3 * n:
                failures.append({"type": "edge_count", "n": n})
            if any(sum(v in e for e in edges) != 6 for v in range(n)):
                failures.append({"type": "degree", "n": n})
            sat += int(three_colourable(n, edges))
        rows.append({
            "vertices": n,
            "finite_nonuniform_trials": trials,
            "three_colourable": sat,
            "constant_reject_correct": trials - sat,
            "compiled_variables_formula": 4572 * n,
            "compiled_clauses_formula": 6096 * n,
            "source_theorem_regime_certified": False,
        })

    yes_controls = []
    for parts in (1, 2, 3):
        n, edges = complete_tripartite(parts)
        ok = three_colourable(n, edges)
        assertions += 3
        if not ok:
            failures.append({"type": "yes_control_rejected", "parts": parts})
        if len(edges) != 3 * n or any(sum(v in e for e in edges) != 6 for v in range(n)):
            failures.append({"type": "yes_control_not_six_regular", "parts": parts})
        yes_controls.append({"family": f"{parts} disjoint K_3,3,3", "vertices": n, "six_regular": True, "three_colourable": ok})

    # Corollary 6.2 assumes 6 d^3 <= log n.  Record both common log conventions.
    d = 6
    exponent = 6 * d**3
    threshold = {
        "d": d,
        "required_log_n_at_least": exponent,
        "if_natural_log_log10_n_at_least": exponent / math.log(10),
        "if_base2_log_log10_n_at_least": exponent * math.log10(2),
    }
    theorem = {
        "source": "Conneryd--de Rezende--Nordstrom--Pang--Risse, Corollary 6.2",
        "source_claim": "for fixed d>=6 in its regime, random d-regular graphs are a.a.s. non-3-colourable and require high PC degree over any field",
        "pushforward_identity": "Pr[K_G in L22] = Pr[G is 3-colourable] = o(1)",
        "constant_reject_error": "o(1) on the pushforward distribution",
        "scope": "distributional decision firewall only; constant reject is not an exact full-L22 decider",
    }
    digest_payload = json.dumps({"rows": rows, "yes_controls": yes_controls, "threshold": threshold, "theorem": theorem}, sort_keys=True).encode()
    result = {
        "status": "PASS" if not failures else "FAIL",
        "classification": "COMPUTATIONAL finite controls plus a separate source-theorem corollary",
        "seed": args.seed,
        "assertions": assertions,
        "failures": failures,
        "randomized_six_regular_controls": rows,
        "explicit_yes_controls": yes_controls,
        "source_regime_threshold": threshold,
        "symbolic_firewall": theorem,
        "semantic_sha256": hashlib.sha256(digest_payload).hexdigest(),
        "elapsed_seconds": round(time.perf_counter() - start, 6),
        "limitations": [
            "The switched finite graphs are controls, not certified uniform random-regular samples.",
            "No asymptotic claim is inferred from finite trials.",
            "The constant rejector is not a total exact L22 decider.",
            "The result blocks an average-case-decision inference, not the verified PC/PCR lower bound.",
        ],
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
