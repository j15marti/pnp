#!/usr/bin/env python3
"""REFEREE306: exhaustive width<=3 affine-CNF source-minimum audit.

No external packages.  The experiment enumerates all systems on four variables
with distinct nonzero row supports of width at most three and at most five rows.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import os
import resource
import time

N = 4
ALL_ASSIGNMENTS = range(1 << N)


def parity(x: int, mask: int) -> int:
    return (x & mask).bit_count() & 1


def system_models(rows, n=N):
    return [x for x in range(1 << n) if all(parity(x, m) == b for m, b in rows)]


def wrong_patterns(mask: int, rhs: int, n=N):
    variables = [v for v in range(n) if mask >> v & 1]
    for bits in itertools.product((0, 1), repeat=len(variables)):
        if (sum(bits) & 1) != rhs:
            yield tuple(zip(variables, bits))


def pattern_matches(x: int, pattern) -> bool:
    return all(((x >> v) & 1) == bit for v, bit in pattern)


def canonical_clauses(rows, n=N):
    clauses = []
    for row_index, (mask, rhs) in enumerate(rows):
        for pattern in wrong_patterns(mask, rhs, n):
            # The unique clause falsified by this wrong local pattern.
            clause = tuple((v + 1) if bit == 0 else -(v + 1) for v, bit in pattern)
            clauses.append((row_index, pattern, clause))
    return clauses


def classify(rows):
    models = system_models(rows)
    if models:
        return {"sat": True, "models": len(models), "row_minimal": False,
                "clause_minimal": False, "clause_count": len(canonical_clauses(rows))}
    other_models = []
    projection_ok = True
    for i, row in enumerate(rows):
        others = rows[:i] + rows[i + 1:]
        om = system_models(others)
        other_models.append(om)
        for pat in wrong_patterns(*row):
            if not any(pattern_matches(x, pat) for x in om):
                projection_ok = False
    return {
        "sat": False,
        "models": 0,
        "row_minimal": all(other_models),
        "clause_minimal": projection_ok,
        "clause_count": len(canonical_clauses(rows)),
    }


def dimacs(rows, n=N):
    cls = [c for _, _, c in canonical_clauses(rows, n)]
    lines = [f"p cnf {n} {len(cls)}"]
    lines += [" ".join(map(str, c)) + " 0" for c in cls]
    return "\n".join(lines) + "\n"


def parse_dimacs(text: str):
    lines = text.splitlines()
    if not lines or not lines[0].startswith("p cnf "):
        raise ValueError("missing header")
    parts = lines[0].split()
    if len(parts) != 4:
        raise ValueError("bad header")
    n, m = int(parts[2]), int(parts[3])
    if n < 0 or m < 0 or len(lines) != m + 1:
        raise ValueError("bad counts")
    out = []
    for line in lines[1:]:
        toks = [int(t) for t in line.split()]
        if not toks or toks[-1] != 0 or 0 in toks[:-1]:
            raise ValueError("bad terminator")
        clause = toks[:-1]
        if any(abs(lit) < 1 or abs(lit) > n for lit in clause):
            raise ValueError("literal out of range")
        if len(set(clause)) != len(clause) or any(-lit in clause for lit in clause):
            raise ValueError("noncanonical clause")
        out.append(tuple(clause))
    return n, out


def exact_cost_certificate(rows):
    info = classify(rows)
    if not info["clause_minimal"]:
        raise ValueError("certificate theorem requires clause-minimal UNSAT CNF")
    # Local AND3 aggregation costs sum(clauses(row)-1); XOR all rows costs r-1.
    local = sum((1 << (m.bit_count() - 1)) - 1 for m, _ in rows)
    xor = len(rows) - 1
    assert local + xor == info["clause_count"] - 1
    # Minimal inconsistency implies every row participates in the all-row dependency.
    total_mask = 0
    total_rhs = 0
    for mask, rhs in rows:
        total_mask ^= mask
        total_rhs ^= rhs
    assert total_mask == 0 and total_rhs == 1
    return {"local_and3": local, "xor": xor, "cost": local + xor}


def named_controls():
    unary = [(1, 0), (1, 1)]
    triangle = [(0b011, 0), (0b110, 0), (0b101, 1)]
    row_min_counterexample = [(0b001, 0), (0b010, 0), (0b011, 1)]
    # K4 edges: 01,02,03,12,13,23; one row per vertex.
    k4_masks = [0b000111, 0b011001, 0b101010, 0b110100]
    k4_odd = list(zip(k4_masks, [1, 0, 0, 0]))
    k4_even = list(zip(k4_masks, [0, 0, 0, 0]))
    controls = {
        "unary_contradiction": {"rows": unary, "n": 1},
        "triangle_2xor_odd": {"rows": triangle, "n": 3},
        "row_minimal_not_clause_minimal": {"rows": row_min_counterexample, "n": 2},
        "k4_odd": {"rows": k4_odd, "n": 6},
        "k4_even": {"rows": k4_even, "n": 6},
    }
    result = {}
    for name, d in controls.items():
        rows, n = d["rows"], d["n"]
        models = system_models(rows, n)
        item = {"rows": rows, "variables": n, "models": len(models),
                "clauses": len(canonical_clauses(rows, n))}
        if name not in ("k4_even",):
            # classify uses N=4 only for the exhaustive atlas; named controls need local logic.
            row_min = not models and all(system_models(rows[:i] + rows[i+1:], n)
                                         for i in range(len(rows)))
            clause_min = True
            if not models:
                for i, row in enumerate(rows):
                    om = system_models(rows[:i] + rows[i+1:], n)
                    variables = [v for v in range(n) if row[0] >> v & 1]
                    for bits in itertools.product((0, 1), repeat=len(variables)):
                        if (sum(bits) & 1) != row[1]:
                            pat = tuple(zip(variables, bits))
                            if not any(pattern_matches(x, pat) for x in om):
                                clause_min = False
            item.update(row_minimal=row_min, clause_minimal=clause_min)
        result[name] = item
    result["unary_contradiction"]["exact_cost"] = 1
    result["triangle_2xor_odd"]["exact_cost"] = 5
    result["row_minimal_not_clause_minimal"]["exact_cost"] = 2
    result["k4_odd"]["exact_cost"] = 15
    return result


def run():
    started = time.perf_counter()
    masks = [m for m in range(1, 1 << N) if m.bit_count() <= 3]
    counts = {k: 0 for k in ("systems", "sat", "unsat", "row_minimal", "clause_minimal")}
    rhs_flip_checks = 0
    theorem_checks = 0
    counterexample = None
    by_rows = {}
    for r in range(1, 6):
        rc = {k: 0 for k in counts}
        for supports in itertools.combinations(masks, r):
            for rhs in itertools.product((0, 1), repeat=r):
                rows = list(zip(supports, rhs))
                counts["systems"] += 1; rc["systems"] += 1
                info = classify(rows)
                key = "sat" if info["sat"] else "unsat"
                counts[key] += 1; rc[key] += 1
                if info["row_minimal"]:
                    counts["row_minimal"] += 1; rc["row_minimal"] += 1
                if info["clause_minimal"]:
                    counts["clause_minimal"] += 1; rc["clause_minimal"] += 1
                    assert info["row_minimal"]
                    cert = exact_cost_certificate(rows)
                    assert cert["cost"] == info["clause_count"] - 1
                    theorem_checks += 1
                    for i in range(r):
                        flipped = rows.copy()
                        flipped[i] = (flipped[i][0], 1 - flipped[i][1])
                        assert system_models(flipped)
                        rhs_flip_checks += 1
                if info["row_minimal"] and not info["clause_minimal"] and counterexample is None:
                    counterexample = {"rows": rows, **info}
        by_rows[str(r)] = rc

    assert counterexample is not None
    expected = [(1, 0), (2, 0), (3, 1)]
    assert counterexample["rows"] == expected
    named = named_controls()
    assert named["k4_odd"]["models"] == 0 and named["k4_odd"]["clause_minimal"]
    assert named["k4_even"]["models"] == 8
    assert named["row_minimal_not_clause_minimal"]["row_minimal"]
    assert not named["row_minimal_not_clause_minimal"]["clause_minimal"]

    good = dimacs([(1, 0), (2, 0), (3, 1)])
    n, clauses = parse_dimacs(good)
    assert (n, len(clauses)) == (4, 4)
    malformed = [
        "", "p cnd 2 1\n1 0\n", "p cnf 2\n1 0\n", "p cnf 2 2\n1 0\n",
        "p cnf 2 1\n3 0\n", "p cnf 2 1\n1\n", "p cnf 2 1\n1 0 0\n",
        "p cnf 2 1\n1 -1 0\n", "p cnf 2 1\n1 1 0\n",
    ]
    rejected = 0
    for bad in malformed:
        try:
            parse_dimacs(bad)
        except (ValueError, TypeError):
            rejected += 1
    assert rejected == len(malformed)

    result = {
        "run_id": "AFFINE-CLAUSE-MINIMUM-REFEREE306",
        "status": {"theorem": "PROVED/EXACT", "enumeration": "COMPUTATIONAL",
                   "row_minimal_lemma": "FALSIFIED", "B1": "OPEN", "B2": "OPEN",
                   "B3": "OPEN", "P_vs_NP": "OPEN"},
        "enumeration": {"n": N, "max_rows": 5, "distinct_nonzero_supports": True,
                        "support_width_max": 3, "counts": counts, "by_rows": by_rows,
                        "theorem_checks": theorem_checks, "rhs_flip_checks": rhs_flip_checks},
        "counterexample": counterexample,
        "named_controls": named,
        "malformed": {"tested": len(malformed), "rejected": rejected},
        "resources": {"elapsed_seconds": time.perf_counter() - started,
                      "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      "logical_optimizer_charged_to_W": False},
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":")).encode()
    result["payload_sha256"] = hashlib.sha256(canonical).hexdigest()
    return result


if __name__ == "__main__":
    result = run()
    out = os.environ.get("REF306_OUT", "results/raw/arc/2026-11-02_2250_LSPV5_AFFINE_CLAUSE_MINIMUM_REFEREE306_raw.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps(result, indent=2, sort_keys=True))
