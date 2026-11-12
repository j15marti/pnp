"""Independent bounded verification of the factored SAT controller.

Checks complete subtree message semantics against brute force on small inputs,
invalid decomposition rejection, capped unknown states, and large separator cases.
No external dependencies. Intended runtime is below 30 seconds.
"""

from pathlib import Path
import hashlib
import itertools
import json
import random
import sys
import time

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "factored_solver.py"
sys.path.insert(0, str(SOURCE.parent))
from factored_solver import solve_decomposed


def satisfies(value, clauses, equations):
    return all(any(bool((value >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause)
               for clause in clauses) and all(((mask & value).bit_count() & 1) == bit
                                             for mask, bit in equations)


def brute_models(n, clauses, equations):
    return [x for x in range(1 << n) if satisfies(x, clauses, equations)]


def verify_case(n, clauses, equations, decomposition, mode="2cnf", strategy="polynomial",
                capped=False, **caps):
    answer = solve_decomposed(n, clauses, equations, decomposition, mode=mode,
                              strategy=strategy, **caps)
    models = brute_models(n, clauses, equations)
    status = answer["status"]
    if status == "SAT":
        assert satisfies(answer["witness"], clauses, equations)
        assert models
    elif status == "UNSAT":
        assert not models
    else:
        assert status == "UNRESOLVED" and capped

    # Independently enumerate the ORIGINAL factors owned by each entire subtree.
    entries = answer["bag_results"]
    children = [[] for _ in entries]
    for index, entry in enumerate(entries):
        if entry["parent"] is not None:
            children[entry["parent"]].append(index)
    checks = 0
    for index, entry in enumerate(entries):
        subtree = []
        stack = [index]
        while stack:
            node = stack.pop()
            subtree.append(node)
            stack.extend(children[node])
        cs = [clauses[i] for node in subtree for i in entries[node]["assigned_clause_indices"]]
        eqs = [equations[i] for node in subtree for i in entries[node]["assigned_equation_indices"]]
        submodels = brute_models(n, cs, eqs)
        for state in entry["states"]:
            assignment = state["assignment"]
            exists = any(all(((point >> variable) & 1) == ((assignment >> j) & 1)
                             for j, variable in enumerate(entry["separator"]))
                         for point in submodels)
            if state["status"] == "SAT":
                assert exists
            elif state["status"] == "UNSAT":
                assert not exists
            else:
                assert capped
            checks += 1
    return answer, checks


def anchor_case(m, anchors):
    n = anchors + 3 * m
    clauses, equations, bags = [], [], []
    for i in range(m):
        variables = [anchors + 3 * i + j for j in range(3)]
        bags.append(list(range(anchors)) + variables)
        equations.append((sum(1 << v for v in variables), 1))
        clauses.extend((-(a + 1), -(b + 1)) for a, b in itertools.combinations(variables, 2))
        clauses.extend((-(v + 1), a + 1) for v in variables for a in range(anchors))
    return n, clauses, equations, {"bags": bags, "edges": [[0, i] for i in range(1, m)]}


def connected_after_deleting(n, clauses, equations, deleted):
    adjacency = [set() for _ in range(n)]
    scopes = [{abs(lit) - 1 for lit in clause} for clause in clauses]
    scopes += [{v for v in range(n) if (mask >> v) & 1} for mask, _ in equations]
    for scope in scopes:
        for a, b in itertools.combinations(scope, 2):
            adjacency[a].add(b)
            adjacency[b].add(a)
    remaining = set(range(n)) - set(deleted)
    if not remaining:
        return True
    reached = {next(iter(remaining))}
    stack = list(reached)
    while stack:
        for neighbor in adjacency[stack.pop()] & remaining:
            if neighbor not in reached:
                reached.add(neighbor)
                stack.append(neighbor)
    return reached == remaining


def main():
    started = time.perf_counter()
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    cases = messages = 0
    controls = []

    explicit = [
        (4, [], [(5, 0), (6, 0), (9, 0), (10, 1)],
         {"bags": [[0, 1, 2], [0, 1, 3]], "edges": [[0, 1]]}, "two_bit_equality_disequality"),
        (4, [(-3, 1), (-4, 2), (-1,), (-2,)], [(12, 1)],
         {"bags": [[0, 1], [3, 1, 2, 0]], "edges": [[0, 1]]}, "positive_binary_child_unsat"),
        (4, [(-3, 1), (-4, 2), (-1,)], [(12, 1)],
         {"bags": [[0, 1], [3, 1, 2, 0]], "edges": [[0, 1]]}, "positive_binary_child_sat_lift"),
        (8, [(-8, 4), (1, 4), (-7, -8)], [(137, 1), (72, 0)],
         {"bags": [[7, 0, 3], [6, 3, 7]], "edges": [[1, 0]]}, "shifted_unsorted_labels"),
        (4, [(1,), (-3,)], [(3, 1), (12, 0)],
         {"bags": [[0, 1], [2, 3]], "edges": []}, "forest_components"),
        (0, [], [], {"bags": [[]], "edges": []}, "empty_sat"),
        (0, [()], [], {"bags": [[]], "edges": []}, "empty_clause_unsat"),
        (0, [], [(0, 1)], {"bags": [], "edges": []}, "constant_without_bags_unsat"),
        (3, [(1,), (1,)], [(3, 1), (3, 1)],
         {"bags": [[0, 1], [1, 2]], "edges": [[0, 1]]}, "duplicate_constraints"),
    ]
    for n, cs, eqs, dec, label in explicit:
        outcomes = []
        for strategy in ("polynomial", "seeds"):
            answer, checked = verify_case(n, cs, eqs, dec, strategy=strategy)
            cases += 1
            messages += checked
            outcomes.append(answer["status"])
        controls.append({"label": label, "statuses": outcomes})

    rng = random.Random(41729)
    for mode, n, bags, samples in [
        ("2cnf", 5, [[0, 1, 2], [1, 2, 3], [2, 3, 4]], 160),
        ("horn", 7, [[0, 1, 2], [2, 3, 4], [4, 5, 6]], 100),
    ]:
        dec = {"bags": bags, "edges": [[0, 1], [1, 2]]}
        for _ in range(samples):
            cs, eqs = [], []
            for bag in bags:
                for _ in range(rng.randrange(5)):
                    width = rng.randrange(1, 3 if mode == "2cnf" else 4)
                    scope = rng.sample(bag, width)
                    if mode == "2cnf":
                        cs.append(tuple((v + 1) * rng.choice((-1, 1)) for v in scope))
                    else:
                        positive = rng.choice([None, *scope])
                        cs.append(tuple(v + 1 if v == positive else -(v + 1) for v in scope))
                for _ in range(rng.randrange(3)):
                    mask = sum(1 << v for v in bag if rng.randrange(2))
                    eqs.append((mask, rng.randrange(2)))
            for strategy in ("polynomial", "seeds"):
                _, checked = verify_case(n, cs, eqs, dec, mode, strategy)
                cases += 1
                messages += checked

    # UNKNOWN boundary states must stay possible and must not acquire witnesses.
    unknown_answer, checked = verify_case(3, [(-2, -3)], [(6, 0)],
        {"bags": [[0], [0, 1, 2]], "edges": [[0, 1]]},
        strategy="seeds", seed_cap=0, capped=True)
    assert unknown_answer["status"] == "UNRESOLVED"
    assert all(state["status"] == "UNRESOLVED"
               for state in unknown_answer["bag_results"][1]["states"])
    assert not unknown_answer["bag_results"][0]["possible_child_message_clauses_local"]
    cases += 1
    messages += checked
    downgraded_answer, checked = verify_case(3, [(-2, -3)], [(6, 0)],
        {"bags": [[0], [0, 1, 2]], "edges": [[0, 1]]},
        strategy="polynomial", term_cap=0, capped=True)
    downgraded_root = downgraded_answer["bag_results"][0]["states"][0]
    assert downgraded_root["backend"]["status"] == "SAT"
    assert downgraded_root["status"] == "UNRESOLVED"
    assert downgraded_root["reason"] == "local_model_selects_unresolved_child_state"
    assert downgraded_answer["status"] == "UNRESOLVED"
    assert downgraded_root["local_witness"] is None
    cases += 1
    messages += checked
    for _ in range(40):
        cs = [(rng.choice((-1, 1)) * (rng.choice([0, 1, 2]) + 1),)
              for _ in range(rng.randrange(3))]
        eqs = [(rng.randrange(8), rng.randrange(2)) for _ in range(rng.randrange(3))]
        _, checked = verify_case(3, cs, eqs, {"bags": [[0], [0, 1, 2]], "edges": [[0, 1]]},
                                 strategy="seeds", seed_cap=rng.randrange(3), capped=True)
        cases += 1
        messages += checked

    invalid = [
        (3, [], [], {"bags": [[0, 1], [1, 2], [0, 2]], "edges": [[0, 1], [1, 2]]}, "running_intersection"),
        (2, [], [], {"bags": [[0, 1]] * 3, "edges": [[0, 1], [1, 2], [2, 0]]}, "cycle"),
        (3, [], [(5, 1)], {"bags": [[0, 1], [1, 2]], "edges": [[0, 1]]}, "uncovered_parity_row"),
        (3, [(1, 3)], [], {"bags": [[0, 1], [1, 2]], "edges": [[0, 1]]}, "uncovered_clause"),
        (2, [], [], {"bags": [[0, 1], [0, 1]], "edges": [[0, 1], [1, 0]]}, "duplicate_edge"),
        (2, [], [], {"bags": [[0, 0, 1]], "edges": []}, "duplicate_bag_label"),
        (2, [], [], {"bags": [[0, 2]], "edges": []}, "out_of_range_label"),
        (3, [], [], {"bags": [[0, 1, 2], [0, 1, 2]], "edges": [[0, 1]]}, "adhesion_three"),
        (1, [], [], {"bags": [[0], [0]], "edges": []}, "shared_variable_across_forest"),
        (1, [], [], {"bags": [[0]], "edges": [[0, 0]]}, "self_edge"),
    ]
    rejected = []
    for n, cs, eqs, dec, label in invalid:
        try:
            solve_decomposed(n, cs, eqs, dec)
        except ValueError:
            rejected.append(label)
        else:
            raise AssertionError(f"Invalid decomposition accepted: {label}")
    try:
        solve_decomposed(2, [], [], {"bags": [[0, 1], [0, 1]], "edges": [[0, 1]]}, mode="horn")
    except ValueError:
        rejected.append("horn_binary_adhesion")
    else:
        raise AssertionError("Horn mode accepted unsupported binary adhesion")

    large = []
    for anchors, mode in [(1, "horn"), (2, "2cnf")]:
        n, cs, eqs, dec = anchor_case(80, anchors)
        answer = solve_decomposed(n, cs, eqs, dec, mode=mode, term_cap=1000)
        assert answer["status"] == "SAT" and satisfies(answer["witness"], cs, eqs)
        large.append({"anchors": anchors, "triples": 80, "variables": n,
                      "status": answer["status"], "counters": answer["counters"]})
    n, cs, eqs, dec = anchor_case(5, 2)
    assert all(connected_after_deleting(n, cs, eqs, [v]) for v in range(n))
    assert not connected_after_deleting(n, cs, eqs, [0, 1])

    instance = json.loads((HERE / "mycielski_instance.json").read_text())
    graph = solve_decomposed(instance["variables"], instance["H_clauses"], instance["A_equations"],
                             {"bags": [list(range(instance["variables"]))], "edges": []},
                             term_cap=100000)
    assert graph["status"] == "UNSAT"
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == source_hash
    report = {"status": "all assertions passed", "runtime_seconds": time.perf_counter() - started,
              "source_sha256": source_hash, "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "small_and_capped_cases": cases, "subtree_message_checks": messages,
              "explicit_controls": controls, "invalid_cases_rejected": rejected,
              "unknown_child_control": unknown_answer, "unknown_child_parent_downgrade": downgraded_answer,
              "large_anchor_controls": large,
              "two_anchor_graph_has_no_articulation": True,
              "mycielski_terminal_status": graph["status"], "mycielski_counters": graph["counters"],
              "scope": "Exact restricted decomposition and cap semantics verified; no unrestricted polynomial bound."}
    (HERE / "factored_audit.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ("unknown_child_control", "unknown_child_parent_downgrade",
                                     "large_anchor_controls", "mycielski_counters")}, indent=2))


if __name__ == "__main__":
    main()
