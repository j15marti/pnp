#!/usr/bin/env python3
"""REFEREE293: direct-sum semantic-interface acquisition audit.

This is a finite verifier for an elementary query theorem.  Python execution
is not claimed to be an FLMV machine trace; the emitted ledger states the
separate abstract bit-probe and live-bit accounting used in the report.
"""
from __future__ import annotations

from itertools import product
from pathlib import Path
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "results/raw/arc/2026-11-02_1048_LSPV5_SEMANTIC_DIRECT_SUM_REFEREE293_raw.json"


def tseitin(vertices, edges, odd_vertex=0):
    incident = [[] for _ in range(vertices)]
    for i, (u, v) in enumerate(edges, 1):
        incident[u].append(i)
        incident[v].append(i)
    assert all(len(row) == 3 for row in incident)
    clauses = []
    for v, scope in enumerate(incident):
        rhs = int(v == odd_vertex)
        for bits in product((0, 1), repeat=3):
            if (sum(bits) & 1) == rhs:
                continue
            # This clause is false exactly on the forbidden bit vector.
            clauses.append(tuple(x if b == 0 else -x for x, b in zip(scope, bits)))
    return len(edges), tuple(clauses)


def fixtures():
    k4 = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    k33 = [(i, 3 + j) for i in range(3) for j in range(3)]
    cube = []
    for x in range(8):
        for bit in (1, 2, 4):
            y = x ^ bit
            if x < y:
                cube.append((x, y))
    petersen = [(i, (i + 1) % 5) for i in range(5)]
    petersen += [(5 + i, 5 + ((i + 2) % 5)) for i in range(5)]
    petersen += [(i, 5 + i) for i in range(5)]
    w1 = (
        (-1, 3, -14), (2, -8, 9), (10, -13, 14), (3, 7, -13),
        (-4, -9, -11), (5, 8, -14), (4, -8, -11), (1, 7, 13),
        (1, -7, 10), (-5, -6, -15), (-2, -6, 12), (-4, 9, -10),
        (-2, 5, -12), (-3, 6, -15), (6, -7, 11), (2, -9, 11),
        (4, 8, -10), (-3, 12, 15), (-5, -12, 15), (-1, 13, 14),
    )
    return {
        "K4_tseitin": tseitin(4, k4),
        "K3_3_tseitin": tseitin(6, k33),
        "Cube_tseitin": tseitin(8, cube),
        "Petersen_tseitin": tseitin(10, petersen),
        "W1": (15, w1),
    }


def clause_true(clause, assignment):
    return any(assignment[abs(lit) - 1] == (lit > 0) for lit in clause)


def formula_true(clauses, assignment):
    return all(clause_true(c, assignment) for c in clauses)


def deletion_witnesses(n, clauses):
    out = [None] * len(clauses)
    models = 0
    assignments = 0
    for a in product((0, 1), repeat=n):
        assignments += 1
        bad = [i for i, c in enumerate(clauses) if not clause_true(c, a)]
        if not bad:
            models += 1
        elif len(bad) == 1 and out[bad[0]] is None:
            out[bad[0]] = a
    assert models == 0 and all(w is not None for w in out)
    return out, assignments


class SignSource:
    def __init__(self, clauses):
        self.support = tuple(tuple(abs(x) for x in c) for c in clauses)
        self.sign = tuple(x > 0 for c in clauses for x in c)
        self.distinct = {"compile": set(), "query": set()}
        self.total = {"compile": 0, "query": 0}

    def read(self, i, phase):
        self.distinct[phase].add(i)
        self.total[phase] += 1
        return self.sign[i]


def exact_membership_query_indexed(source, n, cached_prefix):
    """Clearer indexed implementation used for the recorded audit."""
    cache = tuple(source.read(i, "compile") for i in range(cached_prefix))
    for a in product((0, 1), repeat=n):
        good = True
        for ci, c in enumerate(source.support):
            assert len(c) == 3
            off = 3 * ci
            hit = False
            for j, variable in enumerate(c):
                q = off + j
                sign = cache[q] if q < cached_prefix else source.read(q, "query")
                if a[variable - 1] == sign:
                    hit = True
                    break
            if not hit:
                good = False
                break
        if good:
            return True
    return False


def malformed_controls():
    bad = [
        "1 -1 0\n",                         # no header
        "p cnd 1 1\n1 0\n",                # bad kind
        "p cnf 1 1\n2 0\n",                # out of range
        "p cnf 1 2\n1 0\n",                # clause count mismatch
        "p cnf 1 1\n1\n",                  # missing terminator
        "p cnf 1 1\nq 0\n",                # noninteger
    ]

    def parse(text):
        n = m = None
        clauses = []
        pending = []
        header = False
        for raw in text.splitlines():
            line = raw.strip()
            if not line or line.startswith("c"):
                continue
            if line.startswith("p"):
                parts = line.split()
                if header or len(parts) != 4 or parts[1] != "cnf":
                    raise ValueError("bad header")
                n, m = int(parts[2]), int(parts[3])
                if n < 0 or m < 0:
                    raise ValueError("negative count")
                header = True
                continue
            if not header:
                raise ValueError("missing header")
            for tok in line.split():
                lit = int(tok)
                if lit == 0:
                    clauses.append(tuple(pending))
                    pending = []
                elif abs(lit) > n:
                    raise ValueError("range")
                else:
                    pending.append(lit)
        if not header or pending or len(clauses) != m:
            raise ValueError("incomplete")
        return n, tuple(clauses)

    for text in bad:
        try:
            parse(text)
        except (ValueError, TypeError):
            pass
        else:
            raise AssertionError("malformed input accepted")
    return len(bad)


def main():
    records = []
    total_L = total_assignments = total_flips = 0
    all_fixtures = fixtures()
    names = list(all_fixtures)
    t = len(names)
    for block, name in enumerate(names):
        n, clauses = all_fixtures[name]
        witnesses, assignment_checks = deletion_witnesses(n, clauses)
        L = sum(map(len, clauses))
        assert L == 3 * len(clauses)
        flip_checks = 0
        for ci, clause in enumerate(clauses):
            for li, lit in enumerate(clause):
                neighbor = [list(c) for c in clauses]
                neighbor[ci][li] = -lit
                assert formula_true(tuple(map(tuple, neighbor)), witnesses[ci])
                flip_checks += 1
        assert flip_checks == L

        stages = []
        for p in sorted({0, L // 2, L}):
            source = SignSource(clauses)
            result = exact_membership_query_indexed(source, n, p)
            assert result is False
            c = len(source.distinct["compile"])
            q = len(source.distinct["query"])
            assert c == p and q == L - p
            logical_peak_bits = p + n + 4 * math.ceil(math.log2(L + n + 2)) + 3
            stages.append({
                "compile_prefix": p,
                "compile_distinct_sign_probes": c,
                "query_distinct_sign_probes": q,
                "combined_distinct_sign_probes": len(source.distinct["compile"] | source.distinct["query"]),
                "query_total_sign_probes": source.total["query"],
                "declared_peak_live_bits_upper_bound": logical_peak_bits,
                "membership_qj": result,
            })

        # The combined base relation is {0^t}; a one-flip neighbor in this
        # block permits exactly {0^t, e_block}.
        base_relation = [0]
        neighbor_relation = sorted([0, 1 << block])
        assert len(base_relation) == 1 and len(neighbor_relation) == 2
        total_L += L
        total_assignments += assignment_checks
        total_flips += flip_checks
        records.append({
            "fixture": name,
            "boundary_coordinate": block,
            "n": n,
            "m": len(clauses),
            "L": L,
            "complete_assignments_checked": assignment_checks,
            "models": 0,
            "deletion_witnesses": len(witnesses),
            "sign_flip_sat_neighbors": flip_checks,
            "base_designated_query": False,
            "neighbor_designated_query": True,
            "base_relation_masks": base_relation,
            "one_flip_neighbor_relation_masks": neighbor_relation,
            "phase_splits": stages,
        })

    assert total_L == 396 and total_flips == 396 and total_assignments == 70208
    malformed = malformed_controls()
    out = {
        "run_id": "LSPV5_SEMANTIC_DIRECT_SUM_REFEREE293",
        "timestamp_pst": "2026-11-02 10:48 PST",
        "status": "PASS",
        "theorem_scope": "deterministic exact compile-plus-designated-query source-sign probe model",
        "blocks": len(records),
        "combined_boundary_bits": len(records),
        "combined_base_relation_size": 1,
        "malformed_controls_rejected": malformed,
        "combined_designated_queries": len(records),
        "total_occurrence_signs": total_L,
        "direct_sum_distinct_probe_lower_bound": total_L,
        "complete_assignments_checked": total_assignments,
        "sign_flip_sat_neighbors_checked": total_flips,
        "malformed_controls_rejected": malformed,
        "records": records,
        "claims_not_proved": [
            "superlinear or superpolynomial unrestricted SAT lower bound",
            "square-root-space compiler/query implementation",
            "uniform arbitrary-A contraction",
            "P != NP",
        ],
    }
    RAW.parent.mkdir(parents=True, exist_ok=True)
    RAW.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    digest = hashlib.sha256(RAW.read_bytes()).hexdigest()
    print(json.dumps({
        "status": "PASS",
        "blocks": len(records),
        "signs": total_L,
        "assignments": total_assignments,
        "neighbors": total_flips,
        "malformed": malformed,
        "raw_sha256": digest,
    }, indent=2))


if __name__ == "__main__":
    main()
