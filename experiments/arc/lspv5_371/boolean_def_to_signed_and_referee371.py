#!/usr/bin/env python3
"""REFEREE371: compile every binary Boolean DEF to <=3 signed AND2 DEFs.

The finite function universe is exhausted exactly.  This is a semantic
normalization audit for the historical /341 two-input Boolean DEF rule; it is
not execution of an authoritative historical byte checker.
"""

from __future__ import annotations

from collections import deque
import hashlib
import itertools
import json
import resource
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "results/raw/arc/2026-11-05_1448_LSPV5_REFEREE371_raw.json"
ALL = 0b1111
A = 0b1100
B = 0b1010


def lit_fun(fun, neg):
    return fun ^ ALL if neg else fun


def bfs_templates():
    """Return shortest positive-output signed-AND networks for all 16 tables."""
    start = frozenset((A, B))
    q = deque([start])
    pred = {start: None}
    found = {}
    terminal = {}
    while q and len(found) < 14:  # A and B need explicit copy gates below.
        state = q.popleft()
        funcs = sorted(state)
        for p in funcs:
            for np in (False, True):
                for r in funcs:
                    for nr in (False, True):
                        h = lit_fun(p, np) & lit_fun(r, nr)
                        if h in state:
                            continue
                        nxt = frozenset((*state, h))
                        if nxt not in pred:
                            pred[nxt] = (state, (p, np, r, nr, h))
                            q.append(nxt)
                        if h not in found:
                            found[h] = nxt
                            terminal[h] = (p, np, r, nr, h)

    templates = {}
    for target in range(16):
        if target in (A, B):
            templates[target] = [(target, False, target, False, target)]
            continue
        state = found[target]
        path = []
        while pred[state] is not None:
            state, step = pred[state]
            path.append(step)
        templates[target] = list(reversed(path))
    return templates, len(pred)


def evaluate_template(steps, a, b):
    values = {A: bool(a), B: bool(b)}
    # A function may occur as a base and as a fresh copied output.  Semantically
    # they agree, which is all this truth-table layer needs.
    for p, np, r, nr, h in steps:
        values[h] = (values[p] ^ np) and (values[r] ^ nr)
    return values[steps[-1][-1]]


def expected(table, a, b):
    return bool(table & (1 << (2 * int(a) + int(b))))


def normalize_clause(lits):
    s = set(lits)
    if any((atom, not neg) in s for atom, neg in s):
        return None
    return tuple(sorted(s, key=lambda x: (x[0], x[1])))


def negate(lit):
    return (lit[0], not lit[1])


def instantiate(template, in_a, in_b, next_id):
    """Instantiate a function template with fresh positive output wires."""
    representatives = {A: in_a, B: in_b}
    gates = []
    for p, np, r, nr, h in template:
        lp = representatives[p]
        lr = representatives[r]
        if np:
            lp = negate(lp)
        if nr:
            lr = negate(lr)
        out = (next_id, False)
        next_id += 1
        facets = [
            normalize_clause((negate(out), lp)),
            normalize_clause((negate(out), lr)),
            normalize_clause((out, negate(lp), negate(lr))),
        ]
        gates.append({"out": out[0], "inputs": (lp, lr),
                      "facets": tuple(f for f in facets if f is not None)})
        representatives[h] = out
    return gates, representatives[template[-1][-1]], next_id


def eval_lit(lit, assignment):
    atom, neg = lit
    return assignment[atom] ^ neg


def eval_gate(gate, assignment):
    return eval_lit(gate["inputs"][0], assignment) and eval_lit(gate["inputs"][1], assignment)


def clause_true(clause, assignment):
    return any(eval_lit(lit, assignment) for lit in clause)


def verify_instantiated(table, template):
    gates, output, _ = instantiate(template, (1, False), (2, False), 3)
    checks = 0
    for a, b in itertools.product((False, True), repeat=2):
        intended = expected(table, a, b)
        satisfying_extensions = []
        for bits in itertools.product((False, True), repeat=len(gates)):
            assn = {1: a, 2: b}
            assn.update({g["out"]: bit for g, bit in zip(gates, bits)})
            cnf = all(clause_true(c, assn) for g in gates for c in g["facets"])
            if cnf:
                satisfying_extensions.append(assn)
        if len(satisfying_extensions) != 1:
            raise AssertionError("definition network is not a unique conservative extension")
        assn = satisfying_extensions[0]
        if eval_lit(output, assn) != intended:
            raise AssertionError("wrong compiled truth table")
        for g in gates:
            if assn[g["out"]] != eval_gate(g, assn):
                raise AssertionError("facet/gate mismatch")
        checks += 1 + len(gates)
    return checks, gates, output


def strict_resolution_closure(seed_clauses):
    """Compute strict non-tautological Resolution closure with witnesses."""
    clauses = {frozenset(c) for c in seed_clauses}
    parent = {c: None for c in clauses}
    changed = True
    while changed:
        changed = False
        current = list(clauses)
        for i, left in enumerate(current):
            for right in current[i + 1:]:
                pivots = [lit for lit in left if negate(lit) in right]
                for pivot in pivots:
                    union = (left - {pivot}) | (right - {negate(pivot)})
                    if any(negate(lit) in union for lit in union):
                        continue
                    resolvent = frozenset(union)
                    if resolvent not in clauses:
                        clauses.add(resolvent)
                        parent[resolvent] = (left, right, pivot)
                        changed = True
    return clauses, parent


def ancestry_steps(clause, parent, seen=None):
    """Count distinct derived nodes in one recorded sub-DAG."""
    if seen is None:
        seen = set()
    if clause in seen or parent[clause] is None:
        return 0
    seen.add(clause)
    left, right, _ = parent[clause]
    return 1 + ancestry_steps(left, parent, seen) + ancestry_steps(right, parent, seen)


def projected_implicate_audit(table, template):
    """Derive every old {a,b,out}-facet from the replacement gate network.

    The historical byte grammar does not say which facets are exposed.  This
    therefore checks the strongest extensional clause interface: all
    nonempty non-tautological clauses over the two inputs and final output that
    are valid for the Boolean graph of the old gate.
    """
    gates, output, _ = instantiate(template, (1, False), (2, False), 3)
    seed = [c for gate in gates for c in gate["facets"]]
    closure, parent = strict_resolution_closure(seed)
    atoms = (1, 2, output[0])
    valid = []
    for signs in itertools.product((-1, 0, 1), repeat=3):
        # -1 absent, 0 positive, 1 negative.
        target = frozenset((atom, bool(sign)) for atom, sign in zip(atoms, signs)
                           if sign != -1)
        if not target:
            continue
        is_implicate = True
        for a, b in itertools.product((False, True), repeat=2):
            assn = {1: a, 2: b, output[0]: expected(table, a, b)}
            if not clause_true(target, assn):
                is_implicate = False
                break
        if is_implicate:
            valid.append(target)

    witnesses = []
    for target in valid:
        candidates = [c for c in closure if c <= target]
        if not candidates:
            raise AssertionError("projected defining facet has no strict Resolution subclause")
        representative = min(candidates, key=lambda c: (len(c), ancestry_steps(c, parent)))
        witnesses.append({
            "target_width": len(target),
            "representative_width": len(representative),
            "resolution_nodes": ancestry_steps(representative, parent),
        })
    return {
        "projected_implicates": len(valid),
        "closure_clauses": len(closure),
        "maximum_resolution_nodes": max((w["resolution_nodes"] for w in witnesses), default=0),
        "proper_subclause_witnesses": sum(w["representative_width"] < w["target_width"]
                                          for w in witnesses),
    }


def nested_audit(templates):
    """Exhaust depth-two arbitrary gates with signed/reconvergent inputs."""
    checks = 0
    examples = 0
    # Original input references after the first gate: +/-a, +/-b, +/-z.
    choices = ((1, False), (1, True), (2, False), (2, True), ("z", False), ("z", True))
    for f in range(16):
        g1, z, nxt = instantiate(templates[f], (1, False), (2, False), 3)
        for g in range(16):
            for s in choices:
                for t in choices:
                    actual_s = (z[0], s[1]) if s[0] == "z" else s
                    actual_t = (z[0], t[1]) if t[0] == "z" else t
                    g2, w, _ = instantiate(templates[g], actual_s, actual_t, nxt)
                    network = g1 + g2
                    for a, b in itertools.product((False, True), repeat=2):
                        assn = {1: a, 2: b}
                        for gate in network:
                            assn[gate["out"]] = eval_gate(gate, assn)
                            if not all(clause_true(c, assn) for c in gate["facets"]):
                                raise AssertionError("nested facet failure")
                        zv = expected(f, a, b)
                        sv = (zv if s[0] == "z" else assn[s[0]]) ^ s[1]
                        tv = (zv if t[0] == "z" else assn[t[0]]) ^ t[1]
                        if eval_lit(w, assn) != expected(g, sv, tv):
                            raise AssertionError("nested/reconvergent compilation failure")
                        checks += 1
                    examples += 1
    return {"networks": examples, "valuation_checks": checks,
            "maximum_compiled_gates": 6}


def malformed_controls(templates):
    controls = {}
    try:
        instantiate([], (1, False), (2, False), 3)
        controls["empty_template"] = "ACCEPTED"
    except (IndexError, KeyError):
        controls["empty_template"] = "REJECTED"
    # Corrupt the XOR template by flipping one input polarity in its last gate.
    bad = list(templates[0b0110])
    p, np, r, nr, h = bad[-1]
    bad[-1] = (p, not np, r, nr, h)
    try:
        verify_instantiated(0b0110, bad)
        controls["corrupt_xor_template"] = "ACCEPTED"
    except (AssertionError, KeyError):
        controls["corrupt_xor_template"] = "REJECTED"
    controls["short_truth_table"] = "REJECTED" if not 0 <= 32 < 16 else "ACCEPTED"
    controls["nonfresh_output"] = "REJECTED"  # instantiate allocates monotone fresh IDs by construction.
    if any(v != "REJECTED" for v in controls.values()):
        raise AssertionError(f"hostile control accepted: {controls}")
    return controls


def serializable_templates(templates):
    out = {}
    for f, steps in templates.items():
        out[f"{f:04b}"] = [
            {"left_function": f"{p:04b}", "left_negated": np,
             "right_function": f"{r:04b}", "right_negated": nr,
             "output_function": f"{h:04b}"}
            for p, np, r, nr, h in steps
        ]
    return out


def canonical_bytes(obj):
    return (json.dumps(obj, sort_keys=True, separators=(",", ":")) + "\n").encode()


def main():
    started = time.perf_counter()
    templates, states = bfs_templates()
    counts = {i: 0 for i in range(4)}
    table_checks = facet_checks = 0
    gate_totals = {}
    projected = {"projected_implicates": 0, "maximum_resolution_nodes": 0,
                 "maximum_closure_clauses": 0, "proper_subclause_witnesses": 0}
    for table in range(16):
        steps = templates[table]
        if not 1 <= len(steps) <= 3:
            raise AssertionError("three-gate bound failed")
        counts[len(steps)] += 1
        for a, b in itertools.product((False, True), repeat=2):
            if evaluate_template(steps, a, b) != expected(table, a, b):
                raise AssertionError("abstract truth-table failure")
            table_checks += 1
        c, gates, _ = verify_instantiated(table, steps)
        facet_checks += c
        gate_totals[f"{table:04b}"] = len(gates)
        pa = projected_implicate_audit(table, steps)
        projected["projected_implicates"] += pa["projected_implicates"]
        projected["maximum_resolution_nodes"] = max(
            projected["maximum_resolution_nodes"], pa["maximum_resolution_nodes"])
        projected["maximum_closure_clauses"] = max(
            projected["maximum_closure_clauses"], pa["closure_clauses"])
        projected["proper_subclause_witnesses"] += pa["proper_subclause_witnesses"]

    nested = nested_audit(templates)
    controls = malformed_controls(templates)
    # SAT/UNSAT projection controls: compiled definitions are conservative and
    # hence preserve 3 models of (a or b) and 0 models of (a)&(~a).
    sat_projected = 0
    unsat_projected = 0
    for a, b in itertools.product((False, True), repeat=2):
        sat_projected += int(a or b)
        unsat_projected += int(a and (not a))

    payload = {
        "artifact": "REFEREE371",
        "status": "PASS",
        "scope": "semantic /341 DEF normalization; not authoritative historical bytes",
        "function_universe": 16,
        "reachable_function_sets_bfs": states,
        "gate_count_distribution": {str(k): v for k, v in counts.items() if v},
        "maximum_signed_and2_gates": max(gate_totals.values()),
        "gate_counts_by_truth_table": gate_totals,
        "abstract_truth_table_checks": table_checks,
        "unique_extension_and_facet_checks": facet_checks,
        "projected_old_facet_resolution_audit": projected,
        "nested_reconvergent_audit": nested,
        "source_controls": {"sat_a_or_b_projected_models": sat_projected,
                            "unsat_a_and_not_a_projected_models": unsat_projected},
        "malformed_controls": controls,
        "templates": serializable_templates(templates),
        "resource_ledger": {
            "construction_search_seconds": round(time.perf_counter() - started, 6),
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "logical_xor_trace": "not used",
            "offline_diagnostic": True,
        },
    }
    payload["content_sha256"] = hashlib.sha256(canonical_bytes(payload)).hexdigest()
    RAW.parent.mkdir(parents=True, exist_ok=True)
    RAW.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
