#!/usr/bin/env python3
"""NAMED-FRONTIER-COMPOSITION132 finite red-team audit.

Independently rebuilds the restricted scoped named-interface join and tests it
on STRICT-SUBJOIN-STATUS131.  It compares fixed, union-optimal, and
product-optimal event-block schedules, including a two-level run.  This is a
restricted algorithm experiment, not an all-input ARC contraction.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from math import isqrt
import hashlib
import json


Event = tuple[str, object]


def scan(events: tuple[Event, ...]):
    active: set[int] = set()
    opened: set[int] = set()
    cuts = [tuple()]
    clauses: list[tuple[int, int, int]] = []
    width = 0
    for op, arg in events:
        if op == "O":
            v = int(arg)
            assert v > 0 and v not in opened
            opened.add(v); active.add(v)
        elif op == "C":
            clause = tuple(arg)
            assert len(clause) == 3 and len({abs(x) for x in clause}) == 3
            assert all(abs(x) in active for x in clause)
            clauses.append(clause)
        elif op == "D":
            v = int(arg)
            assert v in active
            active.remove(v)
        else:
            raise AssertionError(op)
        cuts.append(tuple(sorted(active)))
        width = max(width, len(active))
    assert not active
    return cuts, width, clauses, len(opened)


def build_stream(clauses):
    first, last = {}, {}
    for i, clause in enumerate(clauses):
        for lit in clause:
            v = abs(lit)
            first.setdefault(v, i); last[v] = i
    out: list[Event] = []
    for i, clause in enumerate(clauses):
        for v in sorted(v for v in first if first[v] == i):
            out.append(("O", v))
        out.append(("C", tuple(clause)))
        for v in sorted((v for v in last if last[v] == i), reverse=True):
            out.append(("D", v))
    ans = tuple(out); scan(ans); return ans


def encode_bits(events):
    _, _, clauses, n = scan(events)
    m = len(clauses)
    word = (64 * (n + m + 1) - 1).bit_length()
    return (2 + 4 * n + 4 * m) * word


def dpll(clauses):
    def go(cs):
        while True:
            if not cs: return True
            if any(not c for c in cs): return False
            unit = next((c[0] for c in cs if len(c) == 1), None)
            if unit is None: break
            cs = tuple(tuple(z for z in c if z != -unit) for c in cs if unit not in c)
        lit = cs[0][0]
        for chosen in (lit, -lit):
            rem = tuple(tuple(z for z in c if z != -chosen) for c in cs if chosen not in c)
            if go(rem): return True
        return False
    return go(tuple(map(tuple, clauses)))


def pin(out, v, bit, next_id):
    a, b = next_id, next_id + 1
    out.extend((("O", a), ("O", b)))
    z = v if bit else -v
    for sa, sb in product((1, -1), repeat=2):
        out.append(("C", (z, sa * a, sb * b)))
    out.extend((("D", b), ("D", a)))
    return next_id + 2


def make_child(block, left, right, left_bits, right_bits):
    mapping: dict[int, int] = {}
    out: list[Event] = []
    next_id = 1
    alive: set[int] = set()
    right_set = set(right)

    def local(v):
        nonlocal next_id
        if v not in mapping:
            mapping[v] = next_id; next_id += 1
        return mapping[v]

    for v in left:
        out.append(("O", local(v))); alive.add(v)
    for v, bit in zip(left, left_bits):
        next_id = pin(out, local(v), bit, next_id)
    for op, arg in block:
        if op == "O":
            v = int(arg); out.append(("O", local(v))); alive.add(v)
        elif op == "C":
            out.append(("C", tuple(local(abs(x)) if x > 0 else -local(abs(x)) for x in arg)))
        else:
            v = int(arg)
            if v not in right_set:
                out.append(("D", local(v))); alive.remove(v)
    assert alive == right_set
    for v, bit in zip(right, right_bits):
        next_id = pin(out, local(v), bit, next_id)
    for v in sorted(right, reverse=True):
        out.append(("D", local(v)))
    child = tuple(out); scan(child); return child


def fixed_path(length, block_max):
    return tuple(range(0, length, block_max)) + (length,)


def optimal_path(cuts, block_max, mode):
    """Exact shortest path for sum of union or product assignment counts."""
    length = len(cuts) - 1
    inf = 10**100
    dp = [inf] * (length + 1); prev = [-1] * (length + 1)
    dp[0] = 0
    for j in range(1, length + 1):
        for i in range(max(0, j - block_max), j):
            if mode == "union": exponent = len(set(cuts[i]) | set(cuts[j]))
            elif mode == "product": exponent = len(cuts[i]) + len(cuts[j])
            else: raise ValueError(mode)
            val = dp[i] + (1 << exponent)
            if val < dp[j]: dp[j], prev[j] = val, i
    path = [length]
    while path[-1]: path.append(prev[path[-1]])
    path.reverse()
    return tuple(path), dp[length]


def schedule(events, mode):
    cuts, _, _, _ = scan(events)
    b = max(1, isqrt(len(events)))
    if mode == "fixed":
        path = fixed_path(len(events), b)
    else:
        path, _ = optimal_path(cuts, b, mode)
    union_cost = sum(1 << len(set(cuts[i]) | set(cuts[j])) for i, j in zip(path, path[1:]))
    product_cost = sum(1 << (len(cuts[i]) + len(cuts[j])) for i, j in zip(path, path[1:]))
    return path, union_cost, product_cost


@dataclass
class Stats:
    generated: int = 0
    consistent: int = 0
    incompatible: int = 0
    cache_hits: int = 0
    solver_calls: int = 0
    generated_bits: int = 0
    peak_child_bits: int = 0
    peak_width: int = 0
    planner_edges: int = 0


class Solver:
    def __init__(self, mode):
        self.mode = mode; self.stats = Stats(); self.memo = {}

    def solve(self, events, depth):
        cuts, width, clauses, _ = scan(events)
        self.stats.peak_width = max(self.stats.peak_width, width)
        if depth == 0 or len(events) <= 5:
            self.stats.solver_calls += 1
            return dpll(clauses)
        path, _, _ = schedule(events, self.mode)
        b = max(1, isqrt(len(events)))
        self.stats.planner_edges += sum(min(j, b) for j in range(1, len(events) + 1)) if self.mode != "fixed" else len(path)-1
        reachable = {()}
        for low, high in zip(path, path[1:]):
            left, right = cuts[low], cuts[high]
            future = set(); common = set(left) & set(right)
            for ua in reachable:
                for vb in product((0, 1), repeat=len(right)):
                    self.stats.generated += 1
                    if any(ua[left.index(v)] != vb[right.index(v)] for v in common):
                        self.stats.incompatible += 1; continue
                    self.stats.consistent += 1
                    child = make_child(events[low:high], left, right, ua, vb)
                    cbits = encode_bits(child)
                    self.stats.generated_bits += cbits
                    self.stats.peak_child_bits = max(self.stats.peak_child_bits, cbits)
                    if child in self.memo:
                        self.stats.cache_hits += 1
                        sat = self.memo[child]
                    else:
                        self.stats.solver_calls += 1
                        sat = self.solve(child, depth - 1) if depth > 1 else dpll(scan(child)[2])
                        self.memo[child] = sat
                    if sat: future.add(tuple(vb))
            reachable = future
            if not reachable: return False
        return () in reachable


def exact_one_cnf(lits):
    """Five proper clauses forbid Hamming weights 0,2,3 of three literals."""
    out = []
    for row in product((0, 1), repeat=3):
        if sum(row) == 1: continue
        clause = tuple(lit if bit == 0 else -lit for lit, bit in zip(lits, row))
        out.append(clause)
    return out


def strict_pair(signed):
    triples = ((1,2,3),(1,2,4),(1,3,4),(2,3,4))
    if signed: triples = triples[:3] + ((-2,3,4),)
    return [c for t in triples for c in exact_one_cnf(t)]


def status_only_blocks(events, path):
    """Whether every unpinned event block is locally satisfiable."""
    return [dpll([arg for op, arg in events[i:j] if op == "C"]) for i,j in zip(path,path[1:])]


def k4_tseitin(charge):
    # K4 edges: 12,13,14,23,24,34. Vertex parities use exact XOR CNF.
    inc = ((1,2,3),(1,4,5),(2,4,6),(3,5,6))
    clauses = []
    for v, vars3 in enumerate(inc):
        bit = charge[v]
        for row in product((0,1), repeat=3):
            if (sum(row) & 1) == bit: continue
            clauses.append(tuple(x if b == 0 else -x for x,b in zip(vars3,row)))
    return clauses


def affine_label_k4(charge):
    # Sum of all vertex equations cancels each edge twice.
    return (sum(charge) & 1) == 0


def main():
    rows = []
    checks = 0
    # Exhaustively verify the five-clause exact-one compiler itself.
    for signed_lits in ((1, 2, 3), (-1, 2, 3)):
        compiled = exact_one_cnf(signed_lits)
        for bits in product((0, 1), repeat=3):
            value = {i + 1: bits[i] for i in range(3)}
            sat = all(any(value[abs(l)] == (1 if l > 0 else 0) for l in c) for c in compiled)
            target = sum(value[abs(l)] if l > 0 else 1 - value[abs(l)] for l in signed_lits) == 1
            assert sat == target; checks += 1
    for signed, expected in ((False, False), (True, True)):
        clauses = strict_pair(signed)
        stream = build_stream(clauses)
        assert dpll(clauses) is expected; checks += 1
        for mode in ("fixed", "union", "product"):
            path, uc, pc = schedule(stream, mode)
            cuts = scan(stream)[0]
            for i, j in zip(path, path[1:]):
                brute = 0
                for ua in product((0, 1), repeat=len(cuts[i])):
                    for vb in product((0, 1), repeat=len(cuts[j])):
                        if all(ua[cuts[i].index(v)] == vb[cuts[j].index(v)]
                               for v in set(cuts[i]) & set(cuts[j])):
                            brute += 1
                assert brute == 1 << len(set(cuts[i]) | set(cuts[j])); checks += 1
            local = status_only_blocks(stream, path)
            assert all(local); checks += 1
            solver = Solver(mode); got = solver.solve(stream, 2)
            assert got is expected; checks += 1
            rows.append({
                "case": "signed-SAT" if signed else "positive-UNSAT",
                "mode": mode, "label": got, "source_bits": encode_bits(stream),
                "source_events": len(stream), "source_width": scan(stream)[1],
                "path": path, "union_schedule_cost": uc, "product_schedule_cost": pc,
                "status_only_vector": local, "stats": vars(solver.stats),
            })

    affine_rows = []
    for name, charge in (("affine-SAT", (0,0,0,0)), ("affine-UNSAT", (1,0,0,0))):
        clauses = k4_tseitin(charge); stream = build_stream(clauses)
        expected = affine_label_k4(charge)
        assert dpll(clauses) is expected; checks += 1
        solver = Solver("union"); got = solver.solve(stream, 1)
        assert got is expected; checks += 1
        path, uc, pc = schedule(stream, "union")
        affine_rows.append({"case":name,"label":got,"affine_direct_label":expected,
            "source_bits":encode_bits(stream),"source_width":scan(stream)[1],
            "path":path,"union_schedule_cost":uc,"product_schedule_cost":pc,
            "scoped_stats":vars(solver.stats)})

    # Exact identity used by the overlap-aware scheduler.
    for row in rows + affine_rows:
        assert row["union_schedule_cost"] <= row["product_schedule_cost"]
        checks += 1

    result = {
        "run_id":"NAMED-FRONTIER-COMPOSITION132",
        "status":"COMPUTATIONAL finite audit; symbolic restricted theorem in report",
        "checks":checks,"seed":None,"exhaustive":True,
        "strict_pair":rows,"affine_controls":affine_rows,
        "limitations":[
            "The source must already be a valid closed scoped proper-3CNF event stream.",
            "Named-boundary enumeration is a restricted algorithm, not a necessary action of arbitrary SAT deciders.",
            "Finite child sizes and call counts do not prove an asymptotic ARC contraction.",
        ],
    }
    raw = json.dumps(result, sort_keys=True, indent=2) + "\n"
    result["prehash_sha256"] = hashlib.sha256(raw.encode()).hexdigest()
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
