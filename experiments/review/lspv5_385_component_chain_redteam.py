#!/usr/bin/env python3
"""Independent red-team producer for LSPV-1/446.

Builds the complete 8k-clause component formula, witnesses deletion of every
claimed core clause in the COMPLETE source, constructs the q-1 strict
Resolution refutation, and emits a verifier-facing JSON record.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
import resource
import time
from pathlib import Path


def lit_true(lit, assignment):
    return assignment[abs(lit)] == (lit > 0)


def clause_true(clause, assignment):
    return any(lit_true(l, assignment) for l in clause)


def formula_true(formula, assignment, omit=None):
    return all(i == omit or clause_true(c, assignment) for i, c in enumerate(formula))


def forbidden_clause(variables, values):
    return [(-v if bit else v) for v, bit in zip(variables, values)]


def build_component(bits):
    k = len(bits)
    assert k >= 2
    clauses, gates, pads = [], [], []
    next_var, accumulator = k + 1, 1
    for input_var in range(2, k + 1):
        output = next_var
        next_var += 1
        ids = []
        for a, b, z in itertools.product((0, 1), repeat=3):
            if z != (a ^ b):
                ids.append(len(clauses))
                clauses.append(forbidden_clause((accumulator, input_var, output), (a, b, z)))
        gates.append({"a": accumulator, "b": input_var, "o": output, "ids": ids})
        accumulator = output
    for position in range(1, k + 2):
        target = position if position <= k else accumulator
        lit = target if position <= k and bits[position - 1] else -target
        if position == k + 1:
            lit = -target
        p, q = next_var, next_var + 1
        next_var += 2
        ids = []
        for pv, qv in itertools.product((0, 1), repeat=2):
            ids.append(len(clauses))
            clauses.append([lit, -p if pv else p, -q if qv else q])
        pads.append({"target": target, "lit": lit, "p": p, "q": q,
                     "ids": ids, "input": position <= k})

    intended = {v: False for v in range(1, next_var)}
    for i, bit in enumerate(bits, 1):
        intended[i] = bool(bit)
    for gate in gates:
        intended[gate["o"]] = intended[gate["a"]] ^ intended[gate["b"]]

    core = [i for pad in pads for i in pad["ids"]]
    for gate in gates:
        wrong = dict(intended)
        wrong[gate["o"]] = not wrong[gate["o"]]
        active = [i for i in gate["ids"] if not clause_true(clauses[i], wrong)]
        assert len(active) == 1
        gate["active"] = active[0]
        core.append(active[0])

    assert len(clauses) == 8 * k
    assert next_var - 1 == 4 * k + 1
    assert len(core) == len(set(core)) == 5 * k + 3
    assert all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in clauses)
    return {"k": k, "bits": list(bits), "clauses": clauses, "gates": gates,
            "pads": pads, "intended": intended, "core": core,
            "output": accumulator, "max_var": next_var - 1}


def deletion_witness(component, source_id):
    a = dict(component["intended"])
    matching_pad = next((p for p in component["pads"] if source_id in p["ids"]), None)
    if matching_pad is not None:
        if matching_pad["input"]:
            a[matching_pad["target"]] = not a[matching_pad["target"]]
            for gate in component["gates"]:
                a[gate["o"]] = a[gate["a"]] ^ a[gate["b"]]
        clause = component["clauses"][source_id]
        a[matching_pad["p"]] = matching_pad["p"] not in clause
        a[matching_pad["q"]] = matching_pad["q"] not in clause
    else:
        index = next(i for i, g in enumerate(component["gates"]) if g["active"] == source_id)
        gate = component["gates"][index]
        a[gate["o"]] = not a[gate["o"]]
        for later in component["gates"][index + 1:]:
            a[later["o"]] = a[later["a"]] ^ a[later["b"]]
    assert not clause_true(component["clauses"][source_id], a)
    assert formula_true(component["clauses"], a, source_id)
    assert not formula_true(component["clauses"], a)
    return a


def strict_resolution_trace(component):
    formula = component["clauses"]
    derived = []

    def fetch(ref):
        return formula[ref] if ref >= 0 else derived[-ref - 1]["clause"]

    def resolve(left, right, pivot):
        a, b = fetch(left), fetch(right)
        assert pivot in a and -pivot in b
        out = []
        for lit in a + b:
            if lit not in (pivot, -pivot) and lit not in out:
                out.append(lit)
        assert all(-lit not in out for lit in out)
        ref = -len(derived) - 1
        derived.append({"ref": ref, "left": left, "right": right,
                        "pivot": pivot, "clause": out})
        return ref

    def recover(pad):
        i0, i1, i2, i3 = pad["ids"]
        r0 = resolve(i0, i1, pad["q"])
        r1 = resolve(i2, i3, pad["q"])
        r2 = resolve(r0, r1, pad["p"])
        assert fetch(r2) == [pad["lit"]]
        return r2

    values = {}
    for pad in component["pads"]:
        if pad["input"]:
            values[pad["target"]] = recover(pad)
    for gate in component["gates"]:
        la = fetch(values[gate["a"]])[0]
        lb = fetch(values[gate["b"]])[0]
        expected = gate["o"] if (la > 0) ^ (lb > 0) else -gate["o"]
        active = formula[gate["active"]]
        assert sorted(active) == sorted([-la, -lb, expected])
        r0 = resolve(values[gate["a"]], gate["active"], la)
        r1 = resolve(values[gate["b"]], r0, lb)
        assert fetch(r1) == [expected]
        values[gate["o"]] = r1
    negative = recover(component["pads"][-1])
    root = resolve(values[component["output"]], negative, component["output"])
    assert fetch(root) == []
    assert len(derived) == 5 * component["k"] + 2

    sources, seen = set(), set()
    def walk(ref):
        if ref >= 0:
            sources.add(ref)
        elif ref not in seen:
            seen.add(ref)
            node = derived[-ref - 1]
            walk(node["left"]); walk(node["right"])
    walk(root)
    assert sources == set(component["core"])
    return derived


def encode_assignment(assignment):
    return [[v, int(value)] for v, value in sorted(assignment.items())]


def shift_component(component, offset):
    shifted = []
    for clause in component["clauses"]:
        shifted.append([(1 if lit > 0 else -1) * (abs(lit) + offset) for lit in clause])
    assignment = {v + offset: b for v, b in component["intended"].items()}
    return shifted, assignment


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    started = time.perf_counter()
    rng = random.Random(385)
    counters = {"cases": 0, "odd_cases": 0, "deletion_models": 0,
                "resolution_nodes": 0, "clause_tests": 0,
                "component_omission_products": 0, "large_id_cases": 0}
    samples = []

    patterns = []
    for k in range(2, 9):
        patterns.extend(tuple((mask >> i) & 1 for i in range(k)) for mask in range(1 << k))
    for k in (10, 16, 32):
        for _ in range(5):
            bits = [rng.randrange(2) for _ in range(k)]
            if sum(bits) % 2 == 0:
                bits[0] ^= 1
            patterns.append(tuple(bits))

    for bits in patterns:
        component = build_component(bits)
        counters["cases"] += 1
        parity = sum(bits) & 1
        if parity == 0:
            assert formula_true(component["clauses"], component["intended"])
            continue
        counters["odd_cases"] += 1
        assert not formula_true(component["clauses"], component["intended"])
        witnesses = {}
        for sid in component["core"]:
            w = deletion_witness(component, sid)
            counters["deletion_models"] += 1
            counters["clause_tests"] += len(component["clauses"])
            if component["k"] == 5 and len(samples) < 1:
                witnesses[str(sid)] = encode_assignment(w)
        trace = strict_resolution_trace(component)
        counters["resolution_nodes"] += len(trace)
        if component["k"] == 5 and len(samples) < 1:
            samples.append({"component": {k: component[k] for k in
                            ("k", "bits", "clauses", "core", "output", "max_var")},
                            "witnesses": witnesses, "trace": trace})

    # Large sparse identifier control: truth is invariant under injective renaming.
    c = build_component((1, 0, 1, 1))
    mapping = {v: 10**9 + 104729 * v for v in range(1, c["max_var"] + 1)}
    renamed = [[(1 if lit > 0 else -1) * mapping[abs(lit)] for lit in clause]
               for clause in c["clauses"]]
    for sid in c["core"]:
        w = deletion_witness(c, sid)
        rw = {mapping[v]: b for v, b in w.items()}
        assert formula_true(renamed, rw, sid)
        counters["large_id_cases"] += 1

    # Disjoint-component AND / source-subset OR control. If one core clause is
    # omitted in every odd component, the union of the remaining sources is SAT.
    product_components = [build_component((1, 0)),
                          build_component((1, 1, 1)),
                          build_component((1, 0, 0, 0))]
    witness_tables = [{sid: deletion_witness(c, sid) for sid in c["core"]}
                      for c in product_components]
    offsets, total = [], 0
    for c in product_components:
        offsets.append(total)
        total += c["max_var"] + 1000
    for omitted in itertools.product(*(c["core"] for c in product_components)):
        combined_formula, combined_assignment = [], {}
        omitted_global = set()
        base = 0
        for idx, (c, off, sid) in enumerate(zip(product_components, offsets, omitted)):
            sf, _ = shift_component(c, off)
            combined_formula.extend(sf)
            combined_assignment.update({v + off: b for v, b in witness_tables[idx][sid].items()})
            omitted_global.add(base + sid)
            base += len(c["clauses"])
        assert all(i in omitted_global or clause_true(cl, combined_assignment)
                   for i, cl in enumerate(combined_formula))
        counters["component_omission_products"] += 1

    sample_blob = json.dumps(samples, sort_keys=True, separators=(",", ":")).encode()
    result = {
        "run": "LSPV-5/REFEREE385",
        "timestamp_pst": "2026-11-06 04:48 PST",
        "seed": 385,
        "status": "COMPUTATIONAL independent audit supporting PROVED/RESTRICTED theorem",
        "construction": "complete 8k-clause charge-chain proper 3-CNF",
        "tested_k_exhaustive": list(range(2, 9)),
        "tested_k_sampled": [10, 16, 32],
        "counters": counters,
        "sample_sha256": hashlib.sha256(sample_blob).hexdigest(),
        "samples": samples,
        "claims_not_tested": ["historical accepted-byte R_mix341", "global source retraction",
                               "superpolynomial mixed lower bound", "B1", "B2", "B3"],
        "elapsed_seconds": round(time.perf_counter() - started, 6),
        "producer_max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"pass": True, "out": str(out), "counters": counters,
                      "sample_sha256": result["sample_sha256"]}, sort_keys=True))


if __name__ == "__main__":
    main()
