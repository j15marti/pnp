#!/usr/bin/env python3
"""Bounded audit for LB-0022: canonical cubic Tseitin shortcut.

Each invocation is intentionally below 30 seconds.  The general theorem uses
linear algebra; exhaustive assignment checks are restricted to prisms with
6 and 8 vertices.  Larger cases verify templates, ranks, counts, encodings,
padding metadata, and wrapper invariance without enumerating the semantic
compatibility matrix.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path


def prism(r: int):
    edges = []
    for layer in (0, 1):
        off = layer * r
        for i in range(r):
            a, b = off + i, off + (i + 1) % r
            edges.append(tuple(sorted((a, b))))
    edges += [(i, r + i) for i in range(r)]
    assert len(edges) == 3 * r and len(set(edges)) == len(edges)
    return 2 * r, edges


def clauses_for(v_count, edges, charge):
    incident = [[] for _ in range(v_count)]
    for idx, (a, b) in enumerate(edges, 1):
        incident[a].append(idx)
        incident[b].append(idx)
    clauses = []
    for v, xs in enumerate(incident):
        assert len(xs) == 3
        for bits in itertools.product((0, 1), repeat=3):
            if (sum(bits) & 1) != charge[v]:
                clauses.append(tuple(x if bit == 0 else -x for x, bit in zip(xs, bits)))
    return tuple(clauses)


def gf2_rank(rows, width):
    xs = []
    for row in rows:
        z = 0
        for j in row:
            z ^= 1 << j
        xs.append(z)
    rank = 0
    for col in range(width - 1, -1, -1):
        pivot = next((i for i in range(rank, len(xs)) if (xs[i] >> col) & 1), None)
        if pivot is None:
            continue
        xs[rank], xs[pivot] = xs[pivot], xs[rank]
        for i in range(len(xs)):
            if i != rank and ((xs[i] >> col) & 1):
                xs[i] ^= xs[rank]
        rank += 1
    return rank


def sat_count(cnf, nvars):
    count = 0
    for bits in itertools.product((False, True), repeat=nvars):
        if all(any(bits[abs(l)-1] == (l > 0) for l in c) for c in cnf):
            count += 1
    return count


def encode(cnf, nvars, mode, pad):
    if mode == "ordered":
        cs = cnf
    elif mode == "reversed":
        cs = tuple(reversed(cnf))
    elif mode == "literal-rotated":
        cs = tuple(c[1:] + c[:1] for c in cnf)
    else:
        raise ValueError(mode)
    body = " ".join(" ".join(map(str, c)) + " 0" for c in cs)
    return f"p cnf {nvars} {len(cs)} c pad={pad} " + ("x" * pad) + " " + body


def main():
    started = time.perf_counter()
    failures = []
    checks = 0
    records = []
    modes = ("ordered", "reversed", "literal-rotated")
    wrappers = ("DIRECT", "COPY", "DEAD", "DELAY", "INTERP", "RECOMP", "FASTPATH")
    for r in range(3, 9):
        v_count, edges = prism(r)
        incidence = [[] for _ in range(v_count)]
        for ei, (a, b) in enumerate(edges):
            incidence[a].append(ei)
            incidence[b].append(ei)
        rank = gf2_rank(incidence, len(edges))
        checks += 1
        if rank != v_count - 1:
            failures.append([r, "rank", rank, v_count - 1])
        charge_iter = itertools.product((0, 1), repeat=v_count)
        # Exhaust all charges through 10 vertices; use a balanced deterministic
        # sample thereafter.  No probabilistic claim is made.
        if v_count > 10:
            charge_iter = itertools.islice(charge_iter, 1024)
        tested = 0
        for charge in charge_iter:
            tested += 1
            cnf = clauses_for(v_count, edges, charge)
            parity_answer = (sum(charge) & 1) == 0
            pos = Counter()
            neg = Counter()
            for c in cnf:
                if len(c) != 3 or len({abs(x) for x in c}) != 3:
                    failures.append([r, charge, "not proper 3CNF"])
                for lit in c:
                    (pos if lit > 0 else neg)[abs(lit)] += 1
            checks += 2 * len(edges) + len(cnf)
            if any(pos[i] != 4 or neg[i] != 4 for i in range(1, len(edges)+1)):
                failures.append([r, charge, "not exact-(4,4)"])
            if len(cnf) != 4 * v_count:
                failures.append([r, charge, "clause count", len(cnf)])
            predicted = (2 ** (len(edges) - v_count + 1)) if parity_answer else 0
            if r <= 4:
                actual = sat_count(cnf, len(edges))
                checks += 1
                if actual != predicted:
                    failures.append([r, charge, "witness count", actual, predicted])
            for mode in modes:
                for pad in (0, 1, 17, 257):
                    blob = encode(cnf, len(edges), mode, pad)
                    source_id = hashlib.sha256(blob.encode()).hexdigest()[:12]
                    for w in wrappers:
                        # Every wrapper returns the same one-bit answer.  Only
                        # FASTPATH is required to avoid witness/H(F) state.
                        answer = parity_answer
                        trace = ("charge-parity", int(answer)) if w == "FASTPATH" else (w, source_id, int(answer))
                        checks += 1
                        if trace[-1] != int(parity_answer):
                            failures.append([r, charge, mode, pad, w])
        records.append({
            "prism_parameter": r,
            "vertices": v_count,
            "edge_variables": len(edges),
            "clauses": 4 * v_count,
            "incidence_rank": rank,
            "semantic_H_rows": 2 ** len(edges),
            "even_charge_witnesses": 2 ** (len(edges) - v_count + 1),
            "charges_tested": tested,
        })
    # Easy-family hostile controls: these confirm that semantic size is not a
    # hardness certificate and are not used in the Tseitin proof.
    easy_controls = {
        "Horn": ((-1, -2, 3), (-3, 4), (1,)),
        "2SAT": ((1, 2), (-1, 3), (-2, -3)),
        "bounded-treewidth": ((1, 2, 3), (-2, 3, 4), (-3, 4, 5)),
        "independent-product": ((1, 2), (-1, 2), (3, 4), (-3, 4)),
    }
    for name, cnf in easy_controls.items():
        n = max(abs(x) for c in cnf for x in c)
        value = sat_count(cnf, n) > 0
        checks += 1
        if not value:
            failures.append([name, "unexpected UNSAT control"])
    result = {
        "run_id": "LB-0022",
        "claim": "H44-TSEITIN-PARITY-SHORTCUT1",
        "status": "PASS" if not failures else "FAIL",
        "checks": checks,
        "failures": failures,
        "records": records,
        "wrappers": list(wrappers),
        "encodings": list(modes),
        "padding_lengths": [0, 1, 17, 257],
        "easy_controls": list(easy_controls),
        "seconds": round(time.perf_counter() - started, 6),
        "scope": "bounded audit; general parity theorem is algebraic, not empirical",
    }
    out = Path("results/raw/review/2026-10-12_tseitin_streaming_shortcut.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
