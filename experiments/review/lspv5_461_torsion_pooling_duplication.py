#!/usr/bin/env python3
"""LSPV-5/461 finite controls for the torsion-pooling duplication lemma.

The symbolic lemma is in the report.  This program checks canonical cubic
Tseitin sources, SAT/UNSAT labels, q-fold occurrence duplication, and the
row-erased occurrence histogram over Z/qZ.  It does not optimize Resolution
proofs and does not execute the historical R_mix341 checker.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import resource
import time


def graph_edges(name: str) -> tuple[int, list[tuple[int, int]]]:
    if name == "k4":
        n = 4
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
    elif name == "prism":
        n = 6
        edges = [(0, 1), (1, 2), (2, 0), (3, 4), (4, 5), (5, 3),
                 (0, 3), (1, 4), (2, 5)]
    elif name == "cube":
        n = 8
        edges = []
        for u in range(n):
            for bit in (1, 2, 4):
                v = u ^ bit
                if u < v:
                    edges.append((u, v))
    elif name == "petersen":
        n = 10
        edges = [(i, (i + 1) % 5) for i in range(5)]
        edges += [(i, i + 5) for i in range(5)]
        edges += [(5 + i, 5 + ((i + 2) % 5)) for i in range(5) if i < (i + 2) % 5]
        edges += [(5 + i, 5 + ((i + 2) % 5)) for i in range(5) if i > (i + 2) % 5]
        edges = sorted(set(tuple(sorted(e)) for e in edges))
    else:
        raise ValueError(name)
    assert len(edges) * 2 == 3 * n
    return n, sorted(edges)


def tseitin(nv: int, edges: list[tuple[int, int]], charges: list[int]) -> list[tuple[int, ...]]:
    incident: list[list[int]] = [[] for _ in range(nv)]
    for eid, (u, v) in enumerate(edges, 1):
        incident[u].append(eid)
        incident[v].append(eid)
    clauses: list[tuple[int, ...]] = []
    for v in range(nv):
        ids = sorted(incident[v])
        assert len(ids) == 3
        for bits in itertools.product((0, 1), repeat=3):
            if (sum(bits) & 1) != charges[v]:
                clauses.append(tuple(var if bit == 0 else -var for var, bit in zip(ids, bits)))
    return clauses


def models(nvars: int, clauses: list[tuple[int, ...]]) -> int:
    total = 0
    for mask in range(1 << nvars):
        if all(any(((mask >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause)
               for clause in clauses):
            total += 1
    return total


def duplicate(clauses: list[tuple[int, ...]], q: int) -> list[tuple[int, ...]]:
    return [clause for clause in clauses for _ in range(q)]


def pooled_histogram(clauses: list[tuple[int, ...]], q: int) -> dict[str, int]:
    counts: dict[str, int] = {}
    for clause in clauses:
        key = ",".join(map(str, clause))
        counts[key] = (counts.get(key, 0) + 1) % q
    return {k: v for k, v in counts.items() if v}


def packet(clauses: list[tuple[int, ...]]) -> bytes:
    return ("\n".join(" ".join(map(str, c)) + " 0" for c in clauses) + "\n").encode()


def main() -> None:
    started = time.perf_counter()
    rows = []
    checks = 0
    for graph in ("k4", "prism", "cube", "petersen"):
        nv, edges = graph_edges(graph)
        even = tseitin(nv, edges, [0] * nv)
        odd = tseitin(nv, edges, [1] + [0] * (nv - 1))
        assert len(even) == len(odd) == 4 * nv
        even_models = models(len(edges), even)
        odd_models = models(len(edges), odd)
        assert even_models == 2 ** (len(edges) - nv + 1)
        assert odd_models == 0
        checks += 4
        for q in (2, 3, 5):
            de, do = duplicate(even, q), duplicate(odd, q)
            assert len(de) == len(do) == q * 4 * nv
            assert pooled_histogram(de, q) == {}
            assert pooled_histogram(do, q) == {}
            assert len(packet(de)) == len(packet(do))
            assert models(len(edges), de) == even_models
            assert models(len(edges), do) == 0
            removed = do[:-1]
            assert pooled_histogram(removed, q)
            corrupted = do.copy()
            c = list(corrupted[-1])
            c[0] = -c[0]
            corrupted[-1] = tuple(c)
            assert pooled_histogram(corrupted, q)
            checks += 9
            rows.append({
                "graph": graph,
                "vertices": nv,
                "variables": len(edges),
                "base_clauses": len(even),
                "group_exponent_q": q,
                "duplicated_clauses": len(do),
                "even_models": even_models,
                "odd_models": odd_models,
                "even_pool_support": 0,
                "odd_pool_support": 0,
                "packet_bits_even": 8 * len(packet(de)),
                "packet_bits_odd": 8 * len(packet(do)),
                "odd_packet_sha256": hashlib.sha256(packet(do)).hexdigest(),
                "deletion_control_support": len(pooled_histogram(removed, q)),
                "literal_flip_control_support": len(pooled_histogram(corrupted, q)),
            })
    out = {
        "run": "LSPV-5/461 torsion pooling duplication audit",
        "status": "PROVED/RESTRICTED symbolic lemma; COMPUTATIONAL finite controls",
        "graphs": 4,
        "group_exponents": [2, 3, 5],
        "configurations": len(rows),
        "checks": checks,
        "rows": rows,
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "resolution_optimizer_executed": False,
        "historical_r_mix341_checker_executed": False,
        "topological_isotopy_checker_executed": False,
        "limitation": "Finite controls test labels and torsion pools; Resolution-minimum equality is symbolic.",
    }
    print(json.dumps(out, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
