#!/usr/bin/env python3
"""Independent end-to-end controller validation, with compact reproducible records."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import random
import subprocess
import sys
import time

from controller import compact_result, lower_small_affine, solve_auto, solve_cnf


ROOT = Path(__file__).resolve().parent


def clause_truth(clause, assignment):
    return any(bool((assignment >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause)


def source_truth(n, clauses, equations):
    return any(all(clause_truth(c, value) for c in clauses)
               and all(sum((value >> j) & 1 for j in range(n) if (mask >> j) & 1) % 2 == rhs
                       for mask, rhs in equations)
               for value in range(1 << n))


def check_answer(answer, n, clauses, equations, expected, allow_unresolved=False):
    assert answer["status"] in ("SAT", "UNSAT", "UNRESOLVED")
    if answer["status"] == "UNRESOLVED":
        assert allow_unresolved
        assert answer["witness"] is None
        return
    assert (answer["status"] == "SAT") == expected
    if answer["status"] == "SAT":
        witness = answer["witness"]
        assert isinstance(witness, int) and 0 <= witness < (1 << n)
        assert all(clause_truth(c, witness) for c in clauses)
        assert all(sum((witness >> j) & 1 for j in range(n) if (mask >> j) & 1) % 2 == rhs
                   for mask, rhs in equations)
        assert answer["original_witness_checks"] == {"clauses": len(clauses), "affine_rows": len(equations)}
    counters = answer["counters"]
    assert counters["backend_calls"] == counters["affine_terminal_calls"] + counters["frozen_backend_calls"]
    assert counters["backend_calls"] <= 4 * counters["bags"]


def record(answer, small=True):
    output = {"result": compact_result(answer)}
    if small:
        output["decomposition"] = answer["decomposition"]
    else:
        encoded = json.dumps(answer["decomposition"], sort_keys=True).encode()
        output["decomposition_summary"] = {
            "bags": len(answer["decomposition"]["bags"]),
            "edges": len(answer["decomposition"]["edges"]),
            "sha256": hashlib.sha256(encoded).hexdigest(),
        }
    return output


def random_mixed(seed):
    rng = random.Random(seed)
    cases = []
    for mode in ("2cnf", "horn"):
        for trial in range(80):
            n = rng.randrange(0, 8)
            clauses = []
            for _ in range(rng.randrange(0, 11)):
                if not n:
                    clause = ()
                elif mode == "2cnf":
                    clause = tuple((rng.randrange(n) + 1) * rng.choice((-1, 1))
                                   for _ in range(rng.choices((0, 1, 2), (1, 2, 8))[0]))
                else:
                    variables = rng.sample(range(1, n + 1), rng.randrange(min(n, 5) + 1))
                    clause = [-v for v in variables]
                    if clause and rng.randrange(2):
                        clause[rng.randrange(len(clause))] *= -1
                    clause = tuple(clause)
                clauses.append(clause)
            equations = [(rng.randrange(1 << n), rng.randrange(2)) for _ in range(rng.randrange(5))]
            expected = source_truth(n, clauses, equations)
            for strategy in ("polynomial", "seeds"):
                answer = solve_auto(n, clauses, equations, mode=mode, strategy=strategy)
                check_answer(answer, n, clauses, equations, expected)
                cases.append(dict(label="random_mixed", n=n, clauses=clauses, equations=equations,
                                  mode=mode, strategy=strategy, expected=expected, **record(answer)))
            if trial < 12:
                for strategy in ("polynomial", "seeds"):
                    cap = (0, 1, 3)[trial % 3]
                    answer = solve_auto(n, clauses, equations, mode=mode, strategy=strategy,
                                        candidate_cap=trial % 3, term_cap=cap, seed_cap=cap)
                    check_answer(answer, n, clauses, equations, expected, allow_unresolved=True)
                    cases.append(dict(label="random_capped", n=n, clauses=clauses, equations=equations,
                                      mode=mode, strategy=strategy, cap=cap, expected=expected, **record(answer)))
    # These remain nonunit and retain a ternary affine row after wrapper lowering.
    clauses = [(-1, -2), (-1, -3), (-2, -3)]
    for mode, rhs in (("2cnf", 0), ("horn", 1)):
        for strategy in ("polynomial", "seeds"):
            equations = [(7, rhs)]
            answer = solve_auto(3, clauses, equations, mode=mode, strategy=strategy,
                                term_cap=0, seed_cap=0)
            assert answer["status"] == "UNRESOLVED"
            check_answer(answer, 3, clauses, equations, True, allow_unresolved=True)
            cases.append(dict(label="genuine_zero_budget_unknown", n=3, clauses=clauses,
                              equations=equations, mode=mode, strategy=strategy, expected=True, **record(answer)))
    return cases


def lowering_cases():
    cases = []
    # Every <=2-support row on three variables, including constants, both rhs values.
    for mode in ("2cnf", "horn"):
        for mask in range(8):
            if mask.bit_count() > 2:
                continue
            for rhs in (0, 1):
                clauses, remaining, metadata = lower_small_affine(3, [], [(mask, rhs)], mode)
                for assignment in range(8):
                    original = sum((assignment >> j) & 1 for j in range(3) if (mask >> j) & 1) % 2 == rhs
                    transformed = all(clause_truth(c, assignment) for c in clauses) and all(
                        sum((assignment >> j) & 1 for j in range(3) if (m >> j) & 1) % 2 == b
                        for m, b in remaining)
                    assert original == transformed
                if mode == "horn":
                    assert all(sum(lit > 0 for lit in c) <= 1 for c in clauses)
                    assert bool(remaining) == (mask.bit_count() == 2 and rhs == 1)
                else:
                    assert not remaining and all(len(c) <= 2 for c in clauses)
                cases.append({"label": "lowering_semantics", "mode": mode, "mask": mask, "rhs": rhs,
                              "compiled_clauses": clauses, "remaining_rows": remaining, "metadata": metadata})
    all_rows = [(mask, rhs) for mask in range(4) for rhs in (0, 1)]
    systems = [()] + [(row,) for row in all_rows] + list(itertools.combinations_with_replacement(all_rows, 2))
    for rows in systems:
        # A genuine nonunit Horn clause makes the wrapper execute its lowering path.
        clauses = [(-1, -2)]
        expected = source_truth(2, clauses, rows)
        for mode in ("2cnf", "horn"):
            for strategy in ("polynomial", "seeds"):
                answer = solve_auto(2, clauses, rows, mode=mode, strategy=strategy)
                check_answer(answer, 2, clauses, rows, expected)
                cases.append(dict(label="combined_lowarity_system", n=2, clauses=clauses, equations=rows,
                                  mode=mode, strategy=strategy, expected=expected, **record(answer)))
    # Regression: lowering equality must not hide an originally pure affine input.
    for mode in ("2cnf", "horn"):
        for strategy in ("polynomial", "seeds"):
            rows = [(3, 0), (7, 0)]
            answer = solve_auto(3, [], rows, mode=mode, strategy=strategy, term_cap=0, seed_cap=0)
            check_answer(answer, 3, [], rows, True)
            assert answer["counters"]["affine_terminal_calls"] == 1
            assert answer["counters"]["frozen_backend_calls"] == 0
            assert answer["preprocessing"]["path"] == "original_unit_affine_terminal"
            cases.append(dict(label="prelowering_affine_regression", n=3, clauses=[], equations=rows,
                              mode=mode, strategy=strategy, expected=True, **record(answer)))
    return cases


def selector_cases(seed):
    rng = random.Random(seed + 1)
    sources = [(0, []), (0, [()]), (6, [(1, 2, 3, 4, 5, 6)]),
               (2, [(1,), (-1,)]), (2, [(1, -1), (2, 2)])]
    for _ in range(40):
        n = rng.randrange(1, 7)
        clauses = []
        for _ in range(rng.randrange(7)):
            length = rng.choices(tuple(range(min(n, 4) + 1)),
                                 tuple(1 if k == 0 else 4 for k in range(min(n, 4) + 1)))[0]
            variables = rng.sample(range(1, n + 1), length)
            clauses.append(tuple(v * rng.choice((-1, 1)) for v in variables))
        sources.append((n, clauses))
    cases = []
    for n, clauses in sources:
        expected = source_truth(n, clauses, [])
        for strategy in ("polynomial", "seeds"):
            answer = solve_cnf(n, clauses, strategy=strategy, term_cap=100000, seed_cap=5000)
            if answer["status"] == "UNRESOLVED":
                assert strategy == "seeds"
            else:
                assert (answer["status"] == "SAT") == expected
                if expected:
                    assignment = answer["original_assignment"]
                    assert all(any(assignment[str(abs(lit))] == (lit > 0) for lit in clause) for clause in clauses)
                    assert answer["original_cnf_clause_checks"] == len(clauses)
            cases.append(dict(label="selector_frontend", n=n, clauses=clauses,
                              strategy=strategy, expected=expected, **record(answer)))
    huge = 10**9
    for clauses, expected in (([(huge,), (-huge, 5)], True), ([(huge,), (-huge,)], False)):
        for strategy in ("polynomial", "seeds"):
            answer = solve_cnf(huge, clauses, strategy=strategy)
            assert (answer["status"] == "SAT") == expected
            assert answer["selector_bridge"]["encoded_variables"] < 10
            if expected:
                assert all(any(answer["original_assignment"][str(abs(lit))] == (lit > 0)
                               for lit in clause) for clause in clauses)
                assert answer["witness"].bit_length() <= 2
            cases.append(dict(label="sparse_identifier_selector", n=huge, clauses=clauses,
                              strategy=strategy, expected=expected, **record(answer)))
    return cases


def anchor_instance(triples, anchors):
    clauses, rows = [], []
    for j in range(triples):
        group = [anchors + 3 * j + i + 1 for i in range(3)]
        clauses.extend((-a, -b) for a, b in itertools.combinations(group, 2))
        clauses.extend((-v, a + 1) for v in group for a in range(anchors))
        rows.append((sum(1 << (v - 1) for v in group), 1))
    return anchors + 3 * triples, clauses, rows


def structured_cases():
    cases = []
    for anchors, mode in ((1, "horn"), (2, "2cnf")):
        n, clauses, rows = anchor_instance(200, anchors)
        for strategy in ("polynomial", "seeds"):
            answer = solve_auto(n, clauses, rows, mode=mode, strategy=strategy,
                                term_cap=20, seed_cap=20)
            check_answer(answer, n, clauses, rows, True)
            assert answer["counters"]["max_local_affine_rank"] <= 1
            assert answer["counters"]["max_separator_size"] == anchors
            assert answer["counters"]["max_bag_variables"] <= anchors + 3
            cases.append(dict(label="automatic_anchor_family", generator={"triples": 200, "anchors": anchors},
                              n=n, clause_count=len(clauses), affine_rank=200, mode=mode,
                              strategy=strategy, term_cap=20, seed_cap=20, **record(answer, small=False)))
    data = json.loads((ROOT / "agent_redteam" / "mycielski_instance.json").read_text())
    # Independently enumerate graph colorings with vertex zero fixed to color zero.
    # Any coloring can be permuted to this condition, so the reduction is exact.
    attempts = 0
    for rest in itertools.product(range(3), repeat=data["graph_vertices"] - 1):
        colors = (0, *rest)
        attempts += 1
        assert not all(colors[a] != colors[b] for a, b in data["graph_edges"])
    for mode in ("2cnf", "horn"):
        answer = solve_auto(data["variables"], data["H_clauses"], data["A_equations"], mode=mode)
        assert answer["status"] == "UNSAT"
        cases.append(dict(label="automatic_mycielski_unsat", source="agent_redteam/mycielski_instance.json",
                          independent_color_assignments_checked=attempts, mode=mode, **record(answer, small=False)))
    return cases


def invalid_cases():
    inputs = [
        (-1, [], [], {}), (True, [], [], {}), (1, [(2,)], [], {}),
        (1, [(0,)], [], {}), (1, [], [(2, 0)], {}), (1, [], [(1, 2)], {}),
        (3, [(1, 2, 3)], [], {"mode": "2cnf"}),
        (2, [(1, 2)], [], {"mode": "horn"}),
        (0, [], [], {"mode": "horn", "max_separator": 2}),
        (0, [], [], {"candidate_cap": -1}), (0, [], [], {"max_splits": -1}),
        (0, [], [], {"term_cap": -1}),
    ]
    cases = []
    for n, clauses, equations, options in inputs:
        try:
            solve_auto(n, clauses, equations, **options)
        except ValueError as error:
            cases.append({"n": n, "clauses": clauses, "equations": equations,
                          "options": options, "rejected": str(error)})
        else:
            raise AssertionError("Malformed input was accepted")
    return cases


def cli_cases():
    # Optional smoke stage, selected after the parent creates the final examples.
    cases = []
    jobs = []
    candidates = sorted((ROOT / "examples").glob("*"))
    for path in candidates:
        if path.suffix == ".cnf":
            mode = "cnf"
        elif path.suffix == ".json":
            data = json.loads(path.read_text())
            mode = data.get("mode", "horn" if "horn" in path.stem else "2cnf")
            if mode not in ("horn", "2cnf") or not {"n", "clauses"} <= set(data):
                continue
        else:
            continue
        jobs.append((path, mode, [], None))
    extra = [
        ("affine_only.json", "2cnf", ["--term-cap", "0", "--seed-cap", "0"], "SAT"),
        ("one_anchor_20.json", "horn", ["--strategy", "seeds", "--seed-cap", "20"], "SAT"),
        ("three_anchors_balanced_8.json", "2cnf", ["--term-cap", "20"], "UNRESOLVED"),
    ]
    for filename, mode, options, expected_status in extra:
        path = ROOT / "examples" / filename
        if path.is_file():
            jobs.append((path, mode, options, expected_status))
    for path, mode, options, expected_status in jobs:
        done = subprocess.run([sys.executable, str(ROOT / "controller.py"), mode, str(path), *options],
                              capture_output=True, text=True, check=True, timeout=30)
        result = json.loads(done.stdout)
        assert result["status"] in ("SAT", "UNSAT", "UNRESOLVED")
        if expected_status is not None:
            assert result["status"] == expected_status
        if path.suffix == ".json" and result["status"] == "SAT":
            data = json.loads(path.read_text())
            check_answer(result, data["n"], data["clauses"], data["equations"], True)
        cases.append({"input": str(path.relative_to(ROOT)), "mode": mode,
                      "options": options, "expected_status": expected_status, "result": result})
    if not cases:
        raise ValueError("No final CLI examples have been created yet")
    return cases


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("all", "random", "lowering", "selector", "structured", "invalid", "cli"), default="all", nargs="?")
    parser.add_argument("--seed", type=int, default=20261112)
    parser.add_argument("--out", default=str(ROOT / "results" / "controller_validation.json"))
    args = parser.parse_args()
    started = time.perf_counter()
    builders = {"random": lambda: random_mixed(args.seed), "lowering": lowering_cases,
                "selector": lambda: selector_cases(args.seed), "structured": structured_cases,
                "invalid": invalid_cases, "cli": cli_cases}
    chosen = tuple(key for key in builders if key != "cli") if args.stage == "all" else (args.stage,)
    sections = {}
    for stage in chosen:
        mark = time.perf_counter()
        cases = builders[stage]()
        sections[stage] = {"cases": cases, "case_count": len(cases), "elapsed_seconds": time.perf_counter() - mark}
        print(json.dumps({"stage": stage, "cases": len(cases), "elapsed_seconds": sections[stage]["elapsed_seconds"], "failures": 0}), flush=True)
    output = {"status": "COMPUTATIONAL", "seed": args.seed, "failures": 0,
              "case_count": sum(section["case_count"] for section in sections.values()),
              "elapsed_seconds": time.perf_counter() - started, "sections": sections,
              "source_sha256": {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
                                for name in ("controller.py", "separator_decomp.py", "factored_solver.py", "verify_controller.py")},
              "limitation": "Finite exact comparisons and explicitly capped controls; no all-input polynomial-time claim."}
    destination = Path(args.out)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps({key: value for key, value in output.items() if key != "sections"}), flush=True)


if __name__ == "__main__":
    main()
