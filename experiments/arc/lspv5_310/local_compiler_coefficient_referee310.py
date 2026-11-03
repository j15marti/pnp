#!/usr/bin/env python3
"""REFEREE310: audit the LSPV-1 local truth-table compiler constants.

This is an independent standard-library producer.  It proves the symbolic
six-node bound for one complete blocker, exhausts all 256 three-variable
relations and all entailed clauses, and emits signed weakening certificates
for every false-clause/assignment pair.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import resource
import sys
import time
from collections import Counter
from pathlib import Path

VARS = (1, 2, 3)
ASSIGNMENTS = tuple(range(8))


def canon(clause):
    out = tuple(sorted(set(clause), key=lambda x: (abs(x), x < 0)))
    assert all(-x not in out for x in out)
    assert all(1 <= abs(x) <= 3 or abs(x) >= 4 for x in out)
    return out


def sat_lit(lit, assignment):
    value = bool((assignment >> (abs(lit) - 1)) & 1)
    return value if lit > 0 else not value


def sat_clause(clause, assignment):
    return any(sat_lit(lit, assignment) for lit in clause)


def blocker(assignment):
    return canon((-v if (assignment >> (v - 1)) & 1 else v) for v in VARS)


def all_clauses():
    result = []
    for states in itertools.product((-1, 0, 1), repeat=3):
        # -1 = negative, 0 = absent, 1 = positive
        result.append(canon(s * (i + 1) for i, s in enumerate(states) if s))
    return tuple(sorted(set(result), key=lambda c: (len(c), c)))


CLAUSES = all_clauses()


def resolve(a, b, pivot):
    assert pivot in a and -pivot in b
    raw = (set(a) - {pivot}) | (set(b) - {-pivot})
    if any(-lit in raw for lit in raw):
        return None
    return canon(raw)


def closure_subsumer(sources, target):
    """Return a resolution-derived D subseteq target and its ancestor DAG."""
    known = {canon(c): None for c in sources}
    target_set = set(target)
    for c in sorted(known, key=lambda x: (len(x), x)):
        if set(c) <= target_set:
            return c, known

    changed = True
    while changed:
        changed = False
        items = sorted(known, key=lambda x: (len(x), x))
        additions = []
        for i, a in enumerate(items):
            for b in items[i + 1 :]:
                for pivot in sorted(set(a) & {-x for x in b}, key=lambda x: (abs(x), x)):
                    r = resolve(a, b, pivot)
                    if r is None or r in known or any(r == x[0] for x in additions):
                        continue
                    additions.append((r, a, b, pivot))
        for r, a, b, pivot in additions:
            known[r] = (a, b, pivot)
            changed = True
            if set(r) <= target_set:
                return r, known
    raise AssertionError((sources, target, "resolution subsumption completeness failed"))


def ancestor_nodes(goal, known):
    seen = set()
    order = []

    def visit(c):
        if c in seen or known[c] is None:
            return
        a, b, _ = known[c]
        visit(a)
        visit(b)
        seen.add(c)
        order.append(c)

    visit(goal)
    return order


def gate_slots(out, left, right):
    return (
        canon((-out, left)),
        canon((-out, right)),
        canon((out, -left, -right)),
    )


def weakening_certificate(base, target):
    """Explicit PAID-CLAUSE-WEAKENING352 certificate for base subset target."""
    base, target = canon(base), canon(target)
    assert set(base) <= set(target) and base
    added = tuple(x for x in target if x not in base)
    if not added:
        return {"base": list(base), "target": list(target), "defs": [], "res": [], "cost": 0}

    next_var = 4
    defs = []
    w_chain = []
    if len(added) == 1:
        wlit = -added[0]
    else:
        left, right = -added[0], -added[1]
        out = next_var
        next_var += 1
        slots = gate_slots(out, left, right)
        defs.append({"out": out, "left": left, "right": right, "slots": [list(x) for x in slots]})
        w_chain.append((out, left, right, slots))
        prev = out
        for lit in added[2:]:
            out = next_var
            next_var += 1
            slots = gate_slots(out, prev, -lit)
            defs.append({"out": out, "left": prev, "right": -lit, "slots": [list(x) for x in slots]})
            w_chain.append((out, prev, -lit, slots))
            prev = out
        wlit = prev

    q_records = []
    for lit in base:
        out = next_var
        next_var += 1
        slots = gate_slots(out, -lit, wlit)
        defs.append({"out": out, "left": -lit, "right": wlit, "slots": [list(x) for x in slots]})
        q_records.append((lit, out, slots))

    res = []
    current = base
    for lit, q, slots in q_records:
        parent = slots[0]  # (not q or not lit)
        child = resolve(current, parent, lit)
        assert child is not None
        res.append({"left": list(current), "right": list(parent), "pivot": lit, "out": list(child)})
        current = child
    for lit, q, slots in q_records:
        parent = slots[2]  # (q or lit or not w)
        child = resolve(current, parent, -q)
        assert child is not None
        res.append({"left": list(current), "right": list(parent), "pivot": -q, "out": list(child)})
        current = child

    for out, left, right, slots in reversed(w_chain):
        parent = slots[2]
        child = resolve(current, parent, -out)
        assert child is not None
        res.append({"left": list(current), "right": list(parent), "pivot": -out, "out": list(child)})
        current = child

    assert current == target, (base, target, current)
    expected = 3 * len(base) + 2 * len(added) - 2
    assert len(defs) + len(res) == expected
    return {
        "base": list(base),
        "target": list(target),
        "defs": defs,
        "res": res,
        "cost": expected,
    }


def parse_control(obj):
    if not isinstance(obj, dict) or set(obj) != {"relation_mask", "target"}:
        raise ValueError("schema")
    mask, target = obj["relation_mask"], obj["target"]
    if not isinstance(mask, int) or isinstance(mask, bool) or not 0 <= mask <= 255:
        raise ValueError("mask")
    if not isinstance(target, list) or not all(isinstance(x, int) and not isinstance(x, bool) for x in target):
        raise ValueError("target")
    if any(x == 0 or abs(x) > 3 for x in target):
        raise ValueError("literal")
    if len(set(target)) != len(target) or any(-x in target for x in target):
        raise ValueError("canonical")
    if tuple(target) != canon(target):
        raise ValueError("order")
    return mask, tuple(target)


def main():
    started = time.perf_counter()

    # Exact symbolic blocker audit: every clause false at alpha is a subclause
    # of B_alpha, and widening it to B_alpha costs at most six.
    blocker_certs = []
    blocker_cost_hist = Counter()
    false_pairs = 0
    for clause in CLAUSES:
        if not clause:
            continue
        for alpha in ASSIGNMENTS:
            if sat_clause(clause, alpha):
                continue
            false_pairs += 1
            b = blocker(alpha)
            assert set(clause) <= set(b)
            cert = weakening_certificate(clause, b)
            assert cert["cost"] <= 6
            blocker_cost_hist[cert["cost"]] += 1
            blocker_certs.append({"assignment": alpha, **cert})

    # Exhaust all 256 canonical factors and every entailed non-tautological
    # target.  The resolution closure result is a second, stronger general
    # local compiler: at most 26 closure nodes plus at most 6 paid weakening.
    cases = 0
    sat_relations = 0
    unsat_relations = 0
    cost_hist = Counter()
    max_cost = -1
    worst = []
    for mask in range(256):
        models = tuple(a for a in ASSIGNMENTS if (mask >> a) & 1)
        sources = tuple(blocker(a) for a in ASSIGNMENTS if a not in models)
        if models:
            sat_relations += 1
        else:
            unsat_relations += 1
        for target in CLAUSES:
            if all(sat_clause(target, a) for a in models):
                cases += 1
                subsumer, known = closure_subsumer(sources, target)
                res_nodes = ancestor_nodes(subsumer, known)
                if subsumer and subsumer != target:
                    weak = weakening_certificate(subsumer, target)["cost"]
                else:
                    weak = 0
                cost = len(res_nodes) + weak
                assert cost <= 32
                cost_hist[cost] += 1
                record = {
                    "relation_mask": mask,
                    "models": list(models),
                    "sources": [list(x) for x in sources],
                    "target": list(target),
                    "subsumer": list(subsumer),
                    "resolution_ancestor_nodes": len(res_nodes),
                    "weakening_cost": weak,
                    "total_cost": cost,
                }
                if cost > max_cost:
                    max_cost, worst = cost, [record]
                elif cost == max_cost and len(worst) < 12:
                    worst.append(record)

    # Both-label and malformed controls.
    parity_even = sum(1 for a in ASSIGNMENTS if a.bit_count() % 2 == 0)
    parity_odd = sum(1 for a in ASSIGNMENTS if a.bit_count() % 2 == 1)
    assert (parity_even, parity_odd) == (4, 4)
    malformed = [
        None,
        {},
        {"relation_mask": -1, "target": []},
        {"relation_mask": 256, "target": []},
        {"relation_mask": True, "target": []},
        {"relation_mask": 0, "target": [0]},
        {"relation_mask": 0, "target": [1, 1]},
        {"relation_mask": 0, "target": [1, -1]},
        {"relation_mask": 0, "target": [4]},
        {"relation_mask": 0, "target": [2, 1]},
        {"relation_mask": 0, "target": [], "extra": 1},
    ]
    rejected = 0
    for item in malformed:
        try:
            parse_control(item)
        except ValueError:
            rejected += 1
    assert rejected == len(malformed)
    assert parse_control({"relation_mask": 0, "target": []}) == (0, ())
    assert parse_control({"relation_mask": 255, "target": [1, 2, 3]}) == (255, (1, 2, 3))

    elapsed = time.perf_counter() - started
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    result = {
        "run_id": "LOCAL-COMPILER-COEFFICIENT-REFEREE310",
        "date_pst": "2026-11-03 02:48 PST",
        "calculus": "unchanged source-independent unit-cost Rmix341; audited fragment E=RES+charged two-input signed VARDEF and L3 local Boolean factors",
        "status": {
            "proved": [
                "A complete blocker over <=3 variables needs at most 6 paid E nodes from any false authenticated premise clause.",
                "Each <=3-variable output factor needs at most 48 paid E nodes, improving the proposed 440 coefficient.",
                "Every local implicate has a <=32-node E derivation by resolution subsumption closure plus paid weakening."
            ],
            "restricted": "Only explicit <=3-variable Boolean factors; global XOR, circuit-valued CONVERT and full Rmix341 are not simulated.",
            "open": ["B1", "B2", "B3", "superpolynomial Wbar_Rmix341", "P versus NP"]
        },
        "symbolic_bounds": {
            "single_complete_blocker": 6,
            "complete_blockers_per_factor": 8,
            "factor_translation_coefficient": 48,
            "general_local_implicate_coefficient": 32,
            "prior_valid_but_loose_factor_coefficient": 440
        },
        "finite_audit": {
            "clauses_including_empty": len(CLAUSES),
            "false_clause_assignment_pairs": false_pairs,
            "blocker_cost_histogram": dict(sorted(blocker_cost_hist.items())),
            "relations": 256,
            "sat_relations": sat_relations,
            "unsat_relations": unsat_relations,
            "entailed_clause_cases": cases,
            "observed_max_compiler_cost_on_canonical_relations": max_cost,
            "compiler_cost_histogram": dict(sorted(cost_hist.items())),
            "worst_examples": worst,
            "parity_even_models": parity_even,
            "parity_odd_models": parity_odd,
            "malformed_rejected": rejected,
            "valid_parse_controls": 2
        },
        "blocker_certificates": blocker_certs,
        "work_ledger": {
            "producer_wall_seconds": elapsed,
            "producer_peak_rss_kib_linux": rss,
            "optimizer_discovery_in_W": "excluded",
            "certificate_nodes_in_W": "charged once per distinct inference/definition node",
            "machine_warning": "Host work/RSS are not native FLMV time/space; parsing, policy discovery, serialization and checking remain separate."
        }
    }

    out = Path("results/raw/arc/lspv5_310/local_compiler_coefficient_referee310.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    out.write_text(payload, encoding="utf-8")
    digest = hashlib.sha256(payload.encode()).hexdigest()
    print(json.dumps({
        "status": "PASS",
        "raw": str(out),
        "raw_sha256": digest,
        "false_pairs": false_pairs,
        "entailed_cases": cases,
        "max_blocker_cost": max(blocker_cost_hist),
        "observed_max_canonical_cost": max_cost,
        "malformed_rejected": rejected,
        "wall_seconds": elapsed,
        "peak_rss_kib": rss,
    }, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": repr(exc)}), file=sys.stderr)
        raise
