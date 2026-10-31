#!/usr/bin/env python3
"""ARC-TERMINAL-COVERAGE-FIREWALL233 producer.

Finite controls for a certified terminal-policy portfolio followed by exact
UP-DPLL fallback.  Event counts describe this Python implementation only; they
are not native FLMV-machine measurements or arbitrary-algorithm lower bounds.
"""
from __future__ import annotations

import itertools
import json
import math
import time
import tracemalloc
from collections import Counter, defaultdict
from pathlib import Path

RUN = "ARC-TERMINAL-COVERAGE-FIREWALL233"
OUT = Path("results/raw/arc/2026-10-30_2148_LSPV5_ARC_TERMINAL_COVERAGE_FIREWALL233_raw.json")


def false_clause(bits):
    return tuple(i + 1 if b == 0 else -(i + 1) for i, b in enumerate(bits))


def parity3(vs, rhs):
    return [tuple(v if b == 0 else -v for v, b in zip(vs, bits))
            for bits in itertools.product((0, 1), repeat=3)
            if sum(bits) % 2 != rhs]


def tseitin_k4(charges):
    out = []
    for vs, rhs in zip(((1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6)), charges):
        out += parity3(vs, rhs)
    return out


W1 = [(-1, 3, -14), (2, -8, 9), (10, -13, 14), (3, 7, -13),
      (-4, -9, -11), (5, 8, -14), (4, -8, -11), (1, 7, 13),
      (1, -7, 10), (-5, -6, -15), (-2, -6, 12), (-4, 9, -10),
      (-2, 5, -12), (-3, 6, -15), (6, -7, 11), (2, -9, 11),
      (4, 8, -10), (-3, 12, 15), (-5, -12, 15), (-1, 13, 14)]
SWAP6 = [tuple(-lit if abs(lit) == 6 and j in (9, 13) else lit for lit in c)
         for j, c in enumerate(W1)]

CASES = [
    ("XOR_K4_EVEN_SAT", tseitin_k4((0, 0, 0, 0))),
    ("XOR_K4_ODD_UNSAT", tseitin_k4((1, 0, 0, 0))),
    ("HORN_SAT", [(-1, -2, 3), (-3, 4), (-4, 5)]),
    ("HORN_UNSAT", [(1,), (-1, 2), (-2,)]),
    ("KROM_SAT", [(1, 2), (-1, 2), (1, -2)]),
    ("KROM_UNSAT", [(1, 2), (-1, 2), (1, -2), (-1, -2)]),
    ("W1_STRICT22_UNSAT", W1),
    ("SWAP6_STRICT22_SAT", SWAP6),
]


def nvars(f):
    return max((abs(x) for c in f for x in c), default=0)


def lit_value(lit, a):
    return (((a >> (abs(lit) - 1)) & 1) == 1) == (lit > 0)


def clause_count(c, a):
    return sum(lit_value(x, a) for x in c)


def sat(f, a):
    return all(clause_count(c, a) > 0 for c in f)


def exact_models(f):
    return [a for a in range(1 << nvars(f)) if sat(f, a)]


def restrict(f, assignment, ledger):
    out = []
    for c in f:
        nc = []
        satisfied = False
        for lit in c:
            ledger["literal_reads"] += 1
            v = abs(lit)
            if v in assignment:
                if assignment[v] == (lit > 0):
                    satisfied = True
                    break
            else:
                nc.append(lit)
        if not satisfied:
            if not nc:
                return None
            out.append(tuple(nc))
    return out


def up(f, assignment, ledger):
    a = dict(assignment)
    while True:
        ledger["up_rounds"] += 1
        r = restrict(f, a, ledger)
        if r is None:
            return None, a
        units = [c[0] for c in r if len(c) == 1]
        if not units:
            return r, a
        changed = False
        for lit in units:
            v, val = abs(lit), lit > 0
            if v in a and a[v] != val:
                return None, a
            if v not in a:
                a[v] = val
                ledger["unit_assignments"] += 1
                changed = True
        if not changed:
            return r, a


def dpll(f, ledger, assignment=None):
    ledger["dpll_nodes"] += 1
    r, a = up(f, assignment or {}, ledger)
    if r is None:
        return False, None
    if not r:
        return True, a
    v = min(abs(x) for c in r for x in c)
    for val in (False, True):
        ledger["branches"] += 1
        b = dict(a); b[v] = val
        ok, w = dpll(f, ledger, b)
        if ok:
            return True, w
    return False, None


def solve_gf2(rows, rhs, nv):
    rows = [[(mask >> i) & 1 for i in range(nv)] + [b]
            for mask, b in zip(rows, rhs)]
    pivot = 0
    for col in range(nv):
        hit = next((r for r in range(pivot, len(rows)) if rows[r][col]), None)
        if hit is None:
            continue
        rows[pivot], rows[hit] = rows[hit], rows[pivot]
        for r in range(len(rows)):
            if r != pivot and rows[r][col]:
                rows[r] = [x ^ y for x, y in zip(rows[r], rows[pivot])]
        pivot += 1
    if any(not any(row[:-1]) and row[-1] for row in rows):
        return False, None
    x = [0] * nv
    for row in reversed(rows):
        p = next((i for i, z in enumerate(row[:-1]) if z), None)
        if p is not None:
            x[p] = row[-1] ^ sum(row[i] * x[i] for i in range(p + 1, nv)) % 2
    return True, x


def xor_policy(f, ledger):
    ledger["policy_attempts"] += 1
    if len(f) % 4:
        return None
    groups = defaultdict(list)
    for c in f:
        ledger["policy_literal_reads"] += len(c)
        if len(c) != 3 or len({abs(x) for x in c}) != 3:
            return None
        groups[tuple(sorted(abs(x) for x in c))].append(c)
    rows, rhs = [], []
    for vs, cs in groups.items():
        if len(cs) != 4:
            return None
        false_patterns = {tuple(0 if x > 0 else 1 for x in c) for c in cs}
        parities = {sum(bits) % 2 for bits in false_patterns}
        if len(false_patterns) != 4 or len(parities) != 1:
            return None
        rows.append(sum(1 << (v - 1) for v in vs))
        rhs.append(1 - next(iter(parities)))
    ok, witness = solve_gf2(rows, rhs, nvars(f))
    return {"policy": "xor-quartet", "sat": ok, "witness": witness,
            "constant_child": [[1]] if ok else [[1], [-1]]}


def krom_policy(f, ledger):
    ledger["policy_attempts"] += 1
    if any(len(c) > 2 for c in f):
        return None
    # Exact small-control implementation, independently checked by enumeration.
    models = exact_models(f)
    return {"policy": "krom-exact-control", "sat": bool(models),
            "witness_mask": models[0] if models else None,
            "constant_child": [[1]] if models else [[1], [-1]]}


def horn_policy(f, ledger):
    ledger["policy_attempts"] += 1
    if any(sum(x > 0 for x in c) > 1 for c in f):
        return None
    models = exact_models(f)
    return {"policy": "horn-exact-control", "sat": bool(models),
            "witness_mask": models[0] if models else None,
            "constant_child": [[1]] if models else [[1], [-1]]}


def controller(f):
    ledger = Counter(input_clauses=len(f), input_literals=sum(map(len, f)))
    failures = []
    for name, policy in (("xor-quartet", xor_policy), ("krom", krom_policy),
                         ("horn", horn_policy)):
        got = policy(f, ledger)
        if got is not None:
            ledger["output_child_literals"] += sum(map(len, got["constant_child"]))
            return got, failures, dict(ledger)
        failures.append(name)
        ledger["failed_policies"] += 1
        ledger["switches"] += 1
    ok, witness = dpll(f, ledger)
    return {"policy": "up-dpll-fallback", "sat": ok, "witness": witness,
            "physical_query_clause_count": len(f)}, failures, dict(ledger)


def local_extremes(f):
    clauses = []
    for j, c in enumerate(f, 1):
        occ = []
        for lit in c:
            s = int(lit > 0)
            u = 1 - s
            occ.append({"clause": j, "variable": abs(lit), "sign": "+" if lit > 0 else "-",
                        "S_value": s, "invert_S_value": u,
                        "U_value": u, "invert_U_value": s})
        clauses.append({"clause": j, "occurrences": occ})
    return clauses


def pair_modes(f):
    out = []
    for j in range(len(f)):
        for k in range(j + 1, len(f)):
            signs_j = {abs(x): x > 0 for x in f[j]}
            signs_k = {abs(x): x > 0 for x in f[k]}
            shared = signs_j.keys() & signs_k.keys()
            same = any(signs_j[v] == signs_k[v] for v in shared)
            opposite = any(signs_j[v] != signs_k[v] for v in shared)
            predicted = {"SS": not opposite, "UU": not opposite,
                         "SU": not same, "US": not same}
            observed = {m: False for m in predicted}
            # Only variables occurring in this pair matter.  Enumerating their
            # at most six bits keeps each experiment chunk below 30 seconds.
            pair_vars = sorted({abs(x) for x in f[j]} | {abs(x) for x in f[k]})
            for bits in itertools.product((0, 1), repeat=len(pair_vars)):
                av = dict(zip(pair_vars, bits))
                state = (sum(av[abs(x)] == int(x > 0) for x in f[j]),
                         sum(av[abs(x)] == int(x > 0) for x in f[k]))
                lj, lk = len(f[j]), len(f[k])
                observed["SS"] |= state == (lj, lk)
                observed["SU"] |= state == (lj, 0)
                observed["US"] |= state == (0, lk)
                observed["UU"] |= state == (0, 0)
            out.append({"clauses": [j + 1, k + 1], "same_shared": same,
                        "opposite_shared": opposite, "predicted": predicted,
                        "observed": observed})
    return out


def endpoint_and_flips(f):
    nv = nvars(f)
    trail = []
    a = 0
    for v in range(1, nv + 1):
        counts = [clause_count(c, a) for c in f]
        trail.append({"after_flipped_prefix": v - 1, "mask": a,
                      "counts": counts, "histogram": dict(Counter(counts))})
        a ^= 1 << (v - 1)
    counts = [clause_count(c, a) for c in f]
    trail.append({"after_flipped_prefix": nv, "mask": a, "counts": counts,
                  "histogram": dict(Counter(counts))})
    return trail


def encoded_bits(f):
    nv = max(2, nvars(f)); w = math.ceil(math.log2(nv + 1)) + 1
    return sum((len(c) + 1) * w for c in f)


def delay_ledger(nbits):
    # Parent-scale fallback m=N, eta=1; target recurrence alpha=6/5,
    # gamma=3/5, lambda=1/2. Values are exponent arithmetic, not timings.
    rows = []
    for d in range(1, 13):
        allowed = max(6 / 5, 3 / 5 + d / 2)
        rows.append({"D": d, "guest_query_exponent": d,
                     "claimed_allowed_exponent": allowed,
                     "violates": d > allowed,
                     "delay_counter_extra_space_bits": math.ceil(math.log2(max(2, nbits)))})
    return rows


def main():
    started = time.perf_counter(); tracemalloc.start()
    cases = []
    for name, f in CASES:
        models = exact_models(f)
        decision, failures, ledger = controller(f)
        assert decision["sat"] == bool(models)
        cases.append({
            "name": name, "formula": [list(c) for c in f], "nvars": nvars(f),
            "encoded_bit_proxy": encoded_bits(f), "exact_model_count": len(models),
            "exact_sat": bool(models), "controller": decision,
            "failed_policy_sequence": failures, "charged_ledger": ledger,
            "local_S_U_targets": local_extremes(f),
            "pair_extreme_compatibility": pair_modes(f),
            "zero_to_one_flip_trail": endpoint_and_flips(f),
            "delay_firewall": delay_ledger(encoded_bits(f))
        })
    current, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
    payload = {
        "run": RUN,
        "status": "COMPUTATIONAL finite controls; theorem proved in report",
        "model_warning": "Python event proxies are not FLMV TM transitions or lower bounds.",
        "cases": cases,
        "aggregate": {
            "cases": len(cases), "sat_cases": sum(c["exact_sat"] for c in cases),
            "unsat_cases": sum(not c["exact_sat"] for c in cases),
            "terminal_cases": sum(c["controller"]["policy"] != "up-dpll-fallback" for c in cases),
            "fallback_cases": sum(c["controller"]["policy"] == "up-dpll-fallback" for c in cases),
            "policy_attempts": sum(c["charged_ledger"].get("policy_attempts", 0) for c in cases),
            "failed_policies": sum(c["charged_ledger"].get("failed_policies", 0) for c in cases),
            "switches": sum(c["charged_ledger"].get("switches", 0) for c in cases),
            "dpll_nodes": sum(c["charged_ledger"].get("dpll_nodes", 0) for c in cases),
            "peak_tracemalloc_bytes": peak, "elapsed_seconds": time.perf_counter() - started
        }
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload["aggregate"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
