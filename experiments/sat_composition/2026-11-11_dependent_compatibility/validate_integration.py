#!/usr/bin/env python3
"""Independent semantic checks of the composition bridge, split into short stages."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path
import random
import time

from affine_table import Interface
from closure_parity import solve_horn_affine
from composition_solver import bijunctive_encoding, solve_affine_tables, solve_cnf_via_selectors
from independent_2sat import decide_independent_2sat

ROOT = Path(__file__).resolve().parent
SEED = 271828


def factor_holds(factor, assignment):
    def parity(mask):
        return sum((assignment >> j) & 1 for j in range(factor.n)
                   if (mask >> j) & 1) % 2
    if any(parity(mask) != rhs for mask, rhs in factor.equations):
        return False
    address = sum(parity(mask) << j for j, mask in enumerate(factor.forms))
    return bool(factor.table[address])


def formula_holds(clauses, assignment):
    return all(any(((assignment >> (abs(lit) - 1)) & 1) == int(lit > 0)
                   for lit in clause) for clause in clauses)


def factor_record(factor):
    return {"n": factor.n, "equations": factor.equations,
            "forms": factor.forms, "table": factor.table}


def check_factors(label, factors, records, old_answer="not_applicable"):
    n = factors[0].n if factors else 0
    expected = any(all(factor_holds(factor, x) for factor in factors)
                   for x in range(1 << n))
    answer = solve_affine_tables(factors)
    assert answer["status"] != "UNRESOLVED", (label, answer)
    assert (answer["status"] == "SAT") == expected, (label, answer, expected)
    if expected:
        assert all(factor_holds(f, answer["witness"]) for f in factors)
    records.append({"label": label, "factors": list(map(factor_record, factors)),
                    "expected": expected, "previous_answer": old_answer,
                    "result": answer})


def baseline():
    cases = json.loads(gzip.decompress((ROOT/'baseline_affine_inputs.json.gz').read_bytes()))
    records = []
    for case in cases:
        factors = [Interface(f["n"], tuple(map(tuple, f["equations"])),
                             tuple(f["forms"]), tuple(f["table"])) for f in case["factors"]]
        check_factors(case["label"], factors, records, case["answer"])
    return {"cases": records, "resolved_previous_gaps": sum(c["answer"] is None for c in cases)}


def tables():
    rng, records = random.Random(SEED), []
    recognition = []
    for arity in range(4):
        for truth in range(1 << (1 << arity)):
            table = tuple(bool((truth >> z) & 1) for z in range(1 << arity))
            support = [z for z, value in enumerate(table) if value]
            majority_closed = all(((a & b) | (b & c) | (a & c)) in support
                                  for a in support for b in support for c in support)
            encoded = bijunctive_encoding(arity, table)
            assert (encoded is not None) == majority_closed
            if encoded is not None:
                assert all(formula_holds(encoded, z) == table[z] for z in range(1 << arity))
            recognition.append({"arity": arity, "table_bits": truth,
                                "bijunctive": majority_closed})
    for case in range(400):
        n = rng.randrange(1, 9)
        factors = [Interface(n, tuple((rng.randrange(1 << n), rng.randrange(2))
                                      for _ in range(rng.randrange(4))), (), (True,))]
        for _ in range(rng.randrange(1, 8)):
            width = rng.randrange(3)
            factors.append(Interface(n, (), tuple(rng.randrange(1 << n) for _ in range(width)),
                                     tuple(bool(rng.randrange(2)) for _ in range(1 << width))))
        check_factors("random_affine_factors_"+str(case), factors, records)
    # Historical ARC228 unary-only observation counterexample.
    check_factors("all_unary_observations_are_retained",
                  [Interface(3, ((7, 1),), (), (True,))] +
                  [Interface(3, (), (1 << j,), (True, False)) for j in range(3)], records)
    # Full three-coordinate relation that is bijunctive but not affine.
    wide = tuple(((z & 1) == 0 or (z & 2)) and ((z & 2) == 0 or (z & 4))
                 for z in range(8))
    check_factors("larger_bijunctive_table", [Interface(3, (), (1, 2, 4), wide)], records)
    unsupported = solve_affine_tables([Interface(3, (), (1, 2, 4), (False,)+(True,)*7)])
    assert unsupported["status"] == "UNRESOLVED"
    return {"cases": records, "table_recognition": recognition,
            "unsupported_table_control": unsupported}


def cnf():
    rng, records = random.Random(SEED), []
    for case in range(160):
        n = rng.randrange(1, 8)
        clauses = [tuple((v+1) * rng.choice((-1, 1)) for v in rng.sample(range(n), min(n, 3)))
                   for _ in range(rng.randrange(1, min(8, 5*n)+1))]
        expected = any(formula_holds(clauses, x) for x in range(1 << n))
        result = solve_cnf_via_selectors(n, clauses, term_cap=10000)
        assert result["status"] != "UNRESOLVED", (case, result)
        assert (result["status"] == "SAT") == expected
        if expected:
            original_model = sum(int(value) << (int(name)-1)
                                 for name,value in result["original_assignment"].items())
            assert formula_holds(clauses, original_model)
        records.append({"label": "random_cnf_"+str(case), "n": n, "clauses": clauses,
                        "expected": expected, "result": result})
    for label, n, clauses, expected in [
        ("empty_formula", 10**9, [], True),
        ("empty_clause", 5, [()], False),
        ("sparse_identifier", 10**9, [(10**9,), (-10**9,)], False),
        ("tautology_and_duplicates", 2, [(1,-1,1), (2,2)], True)]:
        result = solve_cnf_via_selectors(n, clauses)
        assert (result["status"] == "SAT") == expected
        records.append({"label": label, "n": n, "clauses": clauses,
                        "expected": expected, "result": result})
    graph = json.loads((ROOT/'agent_redteam/singleton_fixedpoint_instance.json').read_text())
    started = time.perf_counter()
    hard = solve_horn_affine(graph["variables"], graph["H_clauses"], graph["A_equations"], 100000)
    elapsed = time.perf_counter() - started
    assert hard["status"] == "UNSAT"
    graph_factors = [Interface(graph["variables"], tuple(map(tuple, graph["A_equations"])), (), (True,))]
    for clause in graph["H_clauses"]:
        scope = sorted({abs(lit) for lit in clause})
        local_clause = tuple((scope.index(abs(lit))+1) * (1 if lit > 0 else -1) for lit in clause)
        table = tuple(formula_holds([local_clause], x) for x in range(1 << len(scope)))
        graph_factors.append(Interface(graph["variables"], (), tuple(1 << (i-1) for i in scope), table))
    old_graph_result, old_graph_details = decide_independent_2sat(graph_factors)
    assert old_graph_result is None
    graph_bridge = solve_affine_tables(graph_factors, 100000)
    assert graph_bridge["status"] == "UNSAT"
    seed_controls = []
    for n, clauses in [(2, [(1,2)]), (2, [(1,),(-1,)]), (3, [(1,-2,3),(-1,2)])]:
        result = solve_cnf_via_selectors(n, clauses, strategy="seeds")
        expected = any(formula_holds(clauses,x) for x in range(1 << n))
        assert (result["status"] == "SAT") == expected
        seed_controls.append({"n": n, "clauses": clauses, "result": result})
    seed_bridge = solve_affine_tables([Interface(3, ((7,1),), (), (True,))] +
                                     [Interface(3, (), (1<<i,), (True,False)) for i in range(3)],
                                     strategy="seeds")
    assert seed_bridge["status"] == "UNSAT"
    expansion = []
    for m in range(1, 8):
        anchor = 3*m+1
        clauses, rows = [], []
        for block in range(m):
            variables = [3*block+j+1 for j in range(3)]
            clauses.extend((-a,-b) for a,b in itertools.combinations(variables,2))
            clauses.extend((-a, anchor) for a in variables)
            rows.append((sum(1 << (a-1) for a in variables),1))
        result = solve_horn_affine(anchor, clauses, rows)
        assert result["status"] == "SAT"
        assert result["counters"]["polynomial_stage_sizes"][-1] == 3**m
        expansion.append({"blocks": m, "n": anchor, "clauses": clauses,
                          "equations": rows, "result": result})
    capped = solve_horn_affine(anchor, clauses, rows, term_cap=20)
    assert capped["status"] == "UNRESOLVED"
    return {"cases": records, "singleton_fixedpoint_instance_result": hard,
            "singleton_instance_seconds": elapsed, "flat_expansion": expansion,
            "temporary_cap_control": capped,
            "graph_previous_terminal": old_graph_details,
            "graph_new_bridge": graph_bridge,
            "seed_selector_controls": seed_controls,
            "seed_factor_bridge": seed_bridge}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["baseline", "tables", "cnf"])
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    start = time.perf_counter()
    data = globals()[args.stage]()
    data.update(stage=args.stage, seed=SEED, status="COMPUTATIONAL",
                elapsed_seconds=time.perf_counter()-start,
                limitations="Finite exact checks; universal polynomial SAT controller remains OPEN.",
                source_sha256={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                               for name in ["closure_parity.py", "seed_parity.py", "composition_solver.py",
                                            "affine_table.py", "validate_integration.py"]})
    output = Path(args.out)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(data,indent=2)+"\n")
    print(json.dumps({k:v for k,v in data.items() if k not in
                      {"cases","table_recognition","flat_expansion"}},indent=2))


if __name__ == "__main__":
    main()
