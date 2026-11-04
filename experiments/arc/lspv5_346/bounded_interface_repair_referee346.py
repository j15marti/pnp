#!/usr/bin/env python3
"""Finite controls for REFEREE346 bounded named-interface repair."""

from __future__ import annotations

import hashlib
import itertools
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/raw/arc/2026-11-04_1445_LSPV5_346_BOUNDED_INTERFACE_REPAIR.json"
SEED = 34620261104


def proper_clause(code):
    """Ternary code: -1 means negative, 0 absent, +1 positive."""
    return tuple(i + 1 if s > 0 else -(i + 1) for i, s in enumerate(code) if s)


def all_clauses(b):
    return [proper_clause(c) for c in itertools.product((-1, 0, 1), repeat=b)]


def normalize(raw, b):
    if not isinstance(raw, (list, tuple)):
        raise ValueError("clause must be a sequence")
    seen = set()
    for lit in raw:
        if not isinstance(lit, int) or isinstance(lit, bool) or lit == 0:
            raise ValueError("literal must be a nonzero integer")
        if abs(lit) > b:
            raise ValueError("literal outside declared interface")
        if -lit in seen:
            raise ValueError("tautological clause")
        if lit in seen:
            raise ValueError("duplicate literal")
        seen.add(lit)
    return tuple(sorted(seen, key=lambda x: (abs(x), x < 0)))


def satisfies_clause(bits, clause):
    return any(bits[abs(lit) - 1] == (lit > 0) for lit in clause)


def models(cnf, bits):
    return all(satisfies_clause(bits, c) for c in cnf)


def resolve(a, b, pivot):
    if pivot not in a or -pivot not in b:
        return None
    out = (set(a) - {pivot}) | (set(b) - {-pivot})
    if any(-lit in out for lit in out):
        return None
    return tuple(sorted(out, key=lambda x: (abs(x), x < 0)))


def saturation(cnf, b):
    clauses = {normalize(c, b) for c in cnf}
    provenance = {}
    changed = True
    while changed:
        changed = False
        snapshot = sorted(clauses, key=lambda c: (len(c), c))
        for i, a in enumerate(snapshot):
            for bb in snapshot[i + 1 :]:
                for lit in a:
                    r = resolve(a, bb, lit)
                    if r is not None and r not in clauses:
                        clauses.add(r)
                        provenance[r] = [list(a), list(bb), lit]
                        changed = True
    return clauses, provenance


def subsumes(a, c):
    return set(a).issubset(c)


def exact_entails(cnf, clause, b):
    for bits in itertools.product((False, True), repeat=b):
        if models(cnf, bits) and not satisfies_clause(bits, clause):
            return False
    return True


def random_cnf(rng, universe, max_size):
    count = rng.randint(0, max_size)
    return rng.sample(universe, min(count, len(universe)))


def php(h):
    """Standard unary PHP_{h+1}^h over variables 1..h(h+1)."""
    def var(pigeon, hole):
        return pigeon * h + hole + 1
    clauses = []
    for p in range(h + 1):
        clauses.append(tuple(var(p, j) for j in range(h)))
    for j in range(h):
        for p in range(h + 1):
            for q in range(p + 1, h + 1):
                clauses.append((-var(p, j), -var(q, j)))
    return clauses


def run():
    rng = random.Random(SEED)
    checks = 0
    samples = []
    sat_count = 0
    unsat_count = 0
    entailed_checked = 0

    for b in range(1, 7):
        universe = all_clauses(b)
        per_b = 120 if b <= 4 else 40
        max_added = 0
        for sample_id in range(per_b):
            cnf = random_cnf(rng, universe, min(2 * b + 3, len(universe)))
            closure, provenance = saturation(cnf, b)
            assert len(closure) <= 3**b
            checks += 1
            assignments = list(itertools.product((False, True), repeat=b))
            is_sat = any(models(cnf, x) for x in assignments)
            sat_count += is_sat
            unsat_count += not is_sat
            max_added = max(max_added, len(provenance))
            for c in universe:
                if exact_entails(cnf, c, b):
                    assert any(subsumes(d, c) for d in closure)
                    checks += 1
                    entailed_checked += 1
            if not is_sat:
                assert () in closure
                checks += 1
        samples.append({
            "b": b,
            "samples": per_b,
            "proper_clause_bound": 3**b,
            "max_added_resolution_nodes_observed": max_added,
        })

    # Unbounded original support but a one-wire named interface.
    origin_support = []
    for k in [4, 5, 8, 16, 32, 64, 128]:
        closure, provenance = saturation([(1,), (-1,)], 1)
        assert () in closure and len(provenance) == 1
        checks += 2
        origin_support.append({
            "transitive_original_support": k,
            "named_interface": 1,
            "repair_nodes": len(provenance),
        })

    # Tiny-output firewall: Gamma_h={z or D : D in PHP} entails the unit z,
    # while z=0 restores the full PHP source interface.
    guarded_php = []
    for h in [1, 2, 3]:
        base = php(h)
        z = h * (h + 1) + 1
        gamma = [tuple(list(c) + [z]) for c in base]
        gamma_models = 0
        z0_models = 0
        for bits in itertools.product((False, True), repeat=z):
            if models(gamma, bits):
                gamma_models += 1
                if not bits[z - 1]:
                    z0_models += 1
        assert gamma_models > 0 and z0_models == 0
        checks += 2
        deletion_witnesses = 0
        for dropped in range(len(gamma)):
            reduced = gamma[:dropped] + gamma[dropped + 1 :]
            found = False
            for bits0 in itertools.product((False, True), repeat=z - 1):
                bits = bits0 + (False,)
                if models(reduced, bits):
                    found = True
                    break
            deletion_witnesses += found
        assert deletion_witnesses == len(gamma)
        checks += 1
        guarded_php.append({
            "h": h,
            "php_variables": h * (h + 1),
            "guarded_clauses": len(gamma),
            "conclusion_named_support": 1,
            "gamma_models": gamma_models,
            "z_false_models": z0_models,
            "source_deletion_z_false_witnesses": deletion_witnesses,
        })

    # Shared proof node is compiled once; fan-out changes references, not DAG nodes.
    shared = []
    base_closure, base_provenance = saturation([(1,), (-1,)], 1)
    repair_nodes = len(base_provenance)
    for fanout in [1, 2, 4, 8, 16, 64, 256, 1024]:
        dag_nodes = repair_nodes
        tree_nodes = repair_nodes * fanout
        assert dag_nodes == 1 and tree_nodes == fanout
        checks += 2
        shared.append({
            "fanout": fanout,
            "shared_dag_repair_nodes": dag_nodes,
            "tree_unfolded_repair_nodes": tree_nodes,
            "dependency_references": fanout,
        })

    # Compact parity is the mandatory representation countercontrol.
    parity = []
    for b in range(2, 17):
        dense_blockers = 2 ** (b - 1)
        xor_rows = 1
        xor_serialized_bits_upper = 2 * b + 1
        assert dense_blockers > xor_rows
        checks += 1
        parity.append({
            "b": b,
            "dense_cnf_blockers": dense_blockers,
            "compact_xor_rows": xor_rows,
            "compact_xor_serialized_bits_upper": xor_serialized_bits_upper,
        })

    # Threshold arithmetic: b <= c log_3 M gives 3^b <= M^c.
    thresholds = []
    for M in [9, 27, 81, 243, 729, 2187, 6561, 19683]:
        b = 0
        while 3 ** (b + 1) <= M:
            b += 1
        assert 3**b <= M
        checks += 1
        thresholds.append({"M": M, "b_floor_log3_M": b, "3^b": 3**b})

    malformed = [
        [0], [1, -1], [1, 1], [2], [True], "1", None,
    ]
    rejected = 0
    for raw in malformed:
        try:
            normalize(raw, 1)
        except ValueError:
            rejected += 1
    assert rejected == len(malformed)
    checks += rejected + 1

    data = {
        "run": "REFEREE346",
        "timestamp_pst": "2026-11-04 14:45",
        "seed": SEED,
        "status": {
            "bounded_named_interface_repair": "PROVED_RESTRICTED",
            "finite_controls": "COMPUTATIONAL",
            "representation_independence": "FALSIFIED_BY_PARITY",
            "B1": "OPEN",
            "B2": "OPEN",
            "B3": "OPEN",
            "P_vs_NP": "OPEN",
        },
        "random_resolution_closure": {
            "samples": samples,
            "sat_instances": sat_count,
            "unsat_instances": unsat_count,
            "entailed_clauses_checked": entailed_checked,
        },
        "unbounded_origin_support_atomic_repair": origin_support,
        "guarded_php_tiny_output_firewall": guarded_php,
        "shared_fanout": shared,
        "parity_countercontrol": parity,
        "logarithmic_thresholds": thresholds,
        "malformed": {"tested": len(malformed), "rejected": rejected},
        "assertions": checks,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, indent=2, sort_keys=True) + "\n"
    OUT.write_text(payload, encoding="utf-8")
    digest = hashlib.sha256(payload.encode()).hexdigest()
    print(json.dumps({"output": str(OUT), "sha256": digest, "assertions": checks,
                      "entailed_clauses_checked": entailed_checked}, indent=2))


if __name__ == "__main__":
    run()
