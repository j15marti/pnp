#!/usr/bin/env python3
"""Exact finite controls for ACQUISITION-QUERY-EXPONENT-REFEREE243.

Standard library only, deterministic, no solver oracle.  Each invocation is
designed to finish in under 30 seconds.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
import time
import tracemalloc
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "results/raw/arc/2026-10-31_0748_LSPV5_ACQUISITION_QUERY_EXPONENT_REFEREE243_raw.json"
SUMMARY = ROOT / "results/summaries/arc/2026-10-31_0748_LSPV5_ACQUISITION_QUERY_EXPONENT_REFEREE243_summary.json"


class CNFBuilder:
    def __init__(self):
        self.nvars = 0
        self.clauses: list[tuple[int, int, int]] = []

    def var(self) -> int:
        self.nvars += 1
        return self.nvars

    def add3(self, a: int, b: int, c: int) -> None:
        assert len({abs(a), abs(b), abs(c)}) == 3
        self.clauses.append((a, b, c))

    def add2(self, a: int, b: int) -> None:
        assert abs(a) != abs(b)
        p = self.var()
        self.add3(a, b, p)
        self.add3(a, b, -p)

    def force(self, lit: int) -> None:
        u, v = self.var(), self.var()
        self.add3(lit, u, v)
        self.add3(lit, u, -v)
        self.add3(lit, -u, v)
        self.add3(lit, -u, -v)

    def eq_or(self, z: int, a: int, b: int) -> None:
        self.add2(-a, z)
        self.add2(-b, z)
        self.add3(a, b, -z)

    def eq_and(self, z: int, a: int, b: int) -> None:
        self.add2(a, -z)
        self.add2(b, -z)
        self.add3(-a, -b, z)

    def dimacs(self) -> str:
        body = "".join(" ".join(map(str, c)) + " 0\n" for c in self.clauses)
        return f"p cnf {self.nvars} {len(self.clauses)}\n" + body


def graphs(kind: str, q: int) -> list[tuple[int, int]]:
    if kind == "cycle":
        return [(i, (i + 1) % q) for i in range(q)]
    if kind == "complete":
        return [(i, j) for i in range(q) for j in range(i + 1, q)]
    if kind == "path":
        return [(i, i + 1) for i in range(q - 1)]
    raise ValueError(kind)


def tau_known(kind: str, q: int) -> int:
    if kind == "cycle":
        return (q + 1) // 2
    if kind == "complete":
        return q - 1
    if kind == "path":
        return q // 2
    raise ValueError(kind)


def source_gate276(kind: str, q: int, unsat: bool) -> tuple[str, list[tuple[int, int, int]], int]:
    edges = graphs(kind, q)
    b = CNFBuilder()
    x = [b.var() for _ in range(q)]
    r = q + 1
    for u, v in edges:
        for _ in range(r):
            z = b.var()
            b.add3(x[u], x[v], z)
    a, bb, c = b.var(), b.var(), b.var()
    if not unsat:
        b.add3(a, bb, c)
    else:
        for vals in itertools.product((0, 1), repeat=3):
            lits = tuple(var if val == 0 else -var for var, val in zip((a, bb, c), vals))
            b.add3(*lits)
    return b.dimacs(), b.clauses, b.nvars


def vertex_cover_query(kind: str, q: int, t: int) -> tuple[str, dict]:
    """Proper-3CNF Tseitin encoding of VC(G)<=t using a bitonic network."""
    edges = graphs(kind, q)
    b = CNFBuilder()
    inputs = [b.var() for _ in range(q)]
    for u, v in edges:
        b.add2(inputs[u], inputs[v])
    p = 1
    while p < q:
        p *= 2
    wires = inputs[:]
    for _ in range(p - q):
        z = b.var()
        b.force(-z)
        wires.append(z)
    comparators = 0
    k = 2
    while k <= p:
        j = k // 2
        while j:
            nxt = wires[:]
            for i in range(p):
                mate = i ^ j
                if mate > i:
                    hi, lo = b.var(), b.var()
                    b.eq_or(hi, wires[i], wires[mate])
                    b.eq_and(lo, wires[i], wires[mate])
                    ascending = (i & k) == 0
                    if ascending:
                        nxt[i], nxt[mate] = lo, hi
                    else:
                        nxt[i], nxt[mate] = hi, lo
                    comparators += 1
            wires = nxt
            j //= 2
        k *= 2
    if t < q:
        b.force(-wires[p - t - 1])
    meta = {"variables": b.nvars, "clauses": len(b.clauses), "comparators": comparators, "padded_wires": p}
    return b.dimacs(), meta


def min_vertex_cover(q: int, edges: list[tuple[int, int]]) -> int:
    for k in range(q + 1):
        for s in itertools.combinations(range(q), k):
            ss = set(s)
            if all(u in ss or v in ss for u, v in edges):
                return k
    raise AssertionError


def min_hitting(clauses: list[tuple[int, int, int]], nvars: int, cap: int) -> int:
    sets = [set(map(abs, c)) for c in clauses]
    universe = range(1, nvars + 1)
    for k in range(cap + 1):
        for s in itertools.combinations(universe, k):
            ss = set(s)
            if all(ss & c for c in sets):
                return k
    raise AssertionError("no hitting set under cap")


def fwht(a: list[int]) -> list[int]:
    a = a[:]
    h = 1
    while h < len(a):
        for i in range(0, len(a), 2 * h):
            for j in range(i, i + h):
                x, y = a[j], a[j + h]
                a[j], a[j + h] = x + y, x - y
        h *= 2
    return a


def bent_rows() -> tuple[list[dict], int]:
    rows, checks = [], 0
    for r in range(2, 7):
        n = 2 * r
        size = 1 << n
        for d in range(2, r + 1):
            signs = []
            zeros = 0
            for z in range(size):
                x = z & ((1 << r) - 1)
                y = z >> r
                dot = (x & y).bit_count() & 1
                mon = 1
                for i in range(d):
                    mon &= (y >> i) & 1
                f = dot ^ mon
                signs.append(1 if f == 0 else -1)
                zeros += f == 0
            w = fwht(signs)
            assert all(abs(v) == (1 << r) for v in w)
            assert w[0] == (1 << r)
            assert zeros == (1 << (2 * r - 1)) + (1 << (r - 1))
            bias_num = max(abs(v) for v in w[1:])
            bias_den = 2 * zeros
            assert bias_num * (2**r + 1) == bias_den
            one_count = size - zeros
            assert 2 * one_count == (1 << (2 * r)) - (1 << r)
            rows.append({
                "r": r, "degree": d, "ambient_points": size,
                "zero_set_size": zeros, "walsh_abs": 1 << r,
                "linear_bias": f"1/{2**r + 1}",
                "nonlinear_gap": f"{one_count}/{size}",
            })
            checks += len(w) + size + 4
    return rows, checks


def h7_h8_controls() -> tuple[dict, int]:
    patterns = list(itertools.product((0, 1), repeat=3))
    def clause_false_at(p):
        return tuple((i + 1) if bit == 0 else -(i + 1) for i, bit in enumerate(p))
    h8 = [clause_false_at(p) for p in patterns]
    h7 = [c for p, c in zip(patterns, h8) if p != (1, 0, 1)]
    checks = 0
    out = {}

    def dpll(cnf):
        nodes = probes = 0
        def rec(assign):
            nonlocal nodes, probes
            nodes += 1
            while True:
                unit = None
                all_sat = True
                for c in cnf:
                    sat = False; undec = []
                    for lit in c:
                        probes += 1
                        v = abs(lit)
                        if v not in assign: undec.append(lit)
                        elif assign[v] == (lit > 0): sat = True; break
                    if sat: continue
                    all_sat = False
                    if not undec: return False
                    if len(undec) == 1: unit = undec[0]; break
                if all_sat: return True
                if unit is None: break
                v, val = abs(unit), unit > 0
                if v in assign and assign[v] != val: return False
                assign[v] = val
            scores = {v: 0 for v in (1, 2, 3) if v not in assign}
            for c in cnf:
                for lit in c:
                    if abs(lit) in scores: scores[abs(lit)] += 1
            v = max(scores, key=scores.get)
            return rec({**assign, v: False}) or rec({**assign, v: True})
        label = rec({})
        return {"label": "SAT" if label else "UNSAT", "states": nodes, "literal_probes": probes}

    for name, cnf in (("H7_unique_middle_SAT", h7), ("H8_UNSAT", h8)):
        models = []
        counts = []
        for a in patterns:
            tc = [sum(((a[abs(l)-1] == 1) if l > 0 else (a[abs(l)-1] == 0)) for l in c) for c in cnf]
            counts.append(tc)
            if all(x > 0 for x in tc):
                models.append(a)
            checks += len(cnf)
        pair_modes = 0
        for i, c1 in enumerate(cnf):
            for j, c2 in enumerate(cnf):
                if i == j:
                    continue
                for e1 in ("S", "U"):
                    for e2 in ("S", "U"):
                        req = {}
                        ok = True
                        for c, e in ((c1, e1), (c2, e2)):
                            for lit in c:
                                value = (lit > 0) if e == "S" else (lit < 0)
                                v = abs(lit)
                                if v in req and req[v] != value:
                                    ok = False
                                req[v] = value
                        brute = False
                        for a in patterns:
                            def extreme(c, e):
                                vals = [((a[abs(l)-1] == 1) if l > 0 else (a[abs(l)-1] == 0)) for l in c]
                                return all(vals) if e == "S" else not any(vals)
                            brute |= extreme(c1, e1) and extreme(c2, e2)
                        assert ok == brute
                        pair_modes += 1
                        checks += 1
        out[name] = {"clauses": cnf, "models": models, "truth_counts": counts, "pair_modes": pair_modes,
                     "up_dpll": dpll(cnf)}
    assert out["H7_unique_middle_SAT"]["models"] == [(1, 0, 1)]
    assert out["H8_UNSAT"]["models"] == []
    return out, checks


def main() -> None:
    started = time.perf_counter()
    tracemalloc.start()
    assertions = 0

    bent, c = bent_rows()
    assertions += c

    graph_rows = []
    for kind in ("cycle", "complete"):
        q_values = (4, 8, 16, 32, 64, 128, 256) if kind == "cycle" else (4, 8, 16, 32, 64)
        for q in q_values:
            tau = tau_known(kind, q)
            sat_src, sat_clauses, sat_nv = source_gate276(kind, q, False)
            unsat_src, unsat_clauses, unsat_nv = source_gate276(kind, q, True)
            query_yes, meta_yes = vertex_cover_query(kind, q, tau)
            query_no, meta_no = vertex_cover_query(kind, q, tau - 1)
            N = max(len(sat_src), len(unsat_src))
            M = max(len(query_yes), len(query_no))
            assert M > 0 and N > 0
            if q <= 8:
                exact_tau = min_vertex_cover(q, graphs(kind, q))
                assert exact_tau == tau
                assertions += 1
            if q <= 5:
                bh_sat = min_hitting(sat_clauses, sat_nv, tau + 1)
                bh_unsat = min_hitting(unsat_clauses, unsat_nv, tau + 1)
                assert bh_sat == bh_unsat == tau + 1
                assertions += 2
            graph_rows.append({
                "kind": kind, "q": q, "edges": len(graphs(kind, q)), "tau": tau,
                "source_sat_chars": len(sat_src), "source_unsat_chars": len(unsat_src),
                "query_tau_chars": len(query_yes), "query_tau_minus_1_chars": len(query_no),
                "source_N": N, "query_M": M,
                "finite_log_exponent": math.log(M) / math.log(N),
                "query_tau_meta": meta_yes, "query_tau_minus_1_meta": meta_no,
                "expected_asymptotic_query_exponent": "1/2+o(1)" if kind == "cycle" else "2/3+o(1)",
                "source_labels": {"positive_guard": "SAT", "eight_guard": "UNSAT"},
                "backdoor_size": tau + 1,
            })
            assertions += 8

    controls, c = h7_h8_controls()
    assertions += c

    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    elapsed = time.perf_counter() - started

    result = {
        "run_id": "ACQUISITION-QUERY-EXPONENT-REFEREE243",
        "timestamp_pdt": "2026-10-31T07:48:00-07:00",
        "deterministic": True,
        "random_seed": None,
        "status": {"general_lemmas": "PROVED/EXACT restricted", "finite_controls": "COMPUTATIONAL", "universal_arc": "OPEN", "p_vs_np": "OPEN"},
        "theorems_tested": {
            "query_exponent_firewall": "A compulsory ordinary-SAT acquisition query of length N^(c+o(1)) to a DELAY-wrapped arbitrary A contributes exponent cK; if c>lambda it cannot uniformly satisfy max(alpha,gamma+lambda K).",
            "bent_degree_firewall": "For every r>=d>=2, f(x,y)=x.y XOR product_{i<=d} y_i is degree d and bent; uniform f=0 has linear bias 1/(2^r+1) but f distinguishes it from uniform by (1-2^-r)/2.",
        },
        "graph_acquisition_rows": graph_rows,
        "bent_degree_rows": bent,
        "original_clause_controls": controls,
        "producer_assertion_units": assertions,
        "runtime_seconds": elapsed,
        "python_peak_tracemalloc_bytes": peak,
        "limitations": [
            "DIMACS character counts and Python operations are not native FLMV transitions.",
            "The Vertex-Cover query is one explicit bitonic-network reduction, not a lower bound on every acquisition algorithm.",
            "The bent distributions are not identified with the CHMY easy-source ensemble and do not construct a SAT transformation.",
        ],
    }
    RAW.parent.mkdir(parents=True, exist_ok=True)
    SUMMARY.parent.mkdir(parents=True, exist_ok=True)
    RAW.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    raw_hash = hashlib.sha256(RAW.read_bytes()).hexdigest()
    summary = {
        "run_id": result["run_id"], "raw_sha256": raw_hash,
        "producer_assertion_units": assertions, "graph_rows": len(graph_rows),
        "bent_rows": len(bent), "runtime_seconds": elapsed,
        "max_finite_query_exponent": max(x["finite_log_exponent"] for x in graph_rows),
        "min_finite_query_exponent": min(x["finite_log_exponent"] for x in graph_rows),
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
