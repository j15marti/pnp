#!/usr/bin/env python3
"""Exact tree-decomposition dynamic programming for mixed Boolean/affine factors.

The supplied decomposition is a FOREST of explicit bags. Every original factor is
assigned once to its first containing bag. Messages have at most two variables for
2-CNF, or one variable for Horn CNF, so they can be encoded as clauses in the same
local tractable language. Affine equations remain local to their assigned bags.

Capped backends use three values. A child state is allowed unless proved UNSAT.
SAT of this relaxation certifies a parent state only when the selected states of
every child are themselves SAT. Unknown child states are never silently forbidden.

The implementation is ordinary exact decomposition DP with explicit cap semantics;
no historical novelty or all-input polynomial decomposition theorem is claimed.
"""
from __future__ import annotations


def _bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def _valid_cap(value):
    return value is None or (isinstance(value, int) and not isinstance(value, bool) and value >= 0)


def _coefficient_rank(masks, counters):
    rows = {}
    for mask in masks:
        while mask:
            pivot = mask.bit_length() - 1
            counters["local_rank_pivot_tests"] += 1
            if pivot not in rows:
                rows[pivot] = mask
                break
            mask ^= rows[pivot]
            counters["local_rank_row_additions"] += 1
    return len(rows)


def _try_unit_affine(n, clauses, equations, outer_counters):
    """Recognize a constant contradiction or a unit-clause/affine query.

    Gaussian elimination is a polynomial terminal, independent of expansion and
    seed-search caps. Return None when a genuine nonunit clause remains.
    """
    outer_counters["unit_affine_recognition_calls"] += 1
    units = []
    nonunit = False
    empty = False
    measured = {"terminal": "unit_affine", "recognition_clauses": 0,
                "recognition_literal_visits": 0, "input_affine_rows": len(equations),
                "unit_rows": 0, "gaussian_input_rows": 0, "gaussian_pivot_tests": 0,
                "gaussian_row_additions": 0, "witness_clause_checks": 0,
                "witness_affine_checks": 0}
    for clause in clauses:
        measured["recognition_clauses"] += 1
        measured["recognition_literal_visits"] += len(clause)
        outer_counters["unit_affine_recognition_clauses"] += 1
        outer_counters["unit_affine_recognition_literal_visits"] += len(clause)
        literals = set(clause)
        if any(-literal in literals for literal in literals):
            continue
        if not literals:
            empty = True
        elif len(literals) == 1:
            literal = next(iter(literals))
            units.append((1 << (abs(literal) - 1), int(literal > 0)))
        else:
            nonunit = True
    measured["unit_rows"] = len(units)

    def finish(status, reason, witness=None):
        return {"status": status, "witness": witness, "reason": reason,
                "terminal": "unit_affine", "counters": measured}

    if empty:
        return finish("UNSAT", "unit_affine_empty_clause")
    if nonunit:
        return None
    rows = {}
    for mask, rhs in (*equations, *units):
        measured["gaussian_input_rows"] += 1
        for pivot in sorted(rows):
            measured["gaussian_pivot_tests"] += 1
            if (mask >> pivot) & 1:
                other, value = rows[pivot]
                mask ^= other
                rhs ^= value
                measured["gaussian_row_additions"] += 1
        if not mask:
            if rhs:
                measured["elimination_rank_before_contradiction"] = len(rows)
                return finish("UNSAT", "unit_affine_inconsistent_system")
            continue
        pivot = (mask & -mask).bit_length() - 1
        for previous, (other, value) in list(rows.items()):
            measured["gaussian_pivot_tests"] += 1
            if (other >> pivot) & 1:
                rows[previous] = other ^ mask, value ^ rhs
                measured["gaussian_row_additions"] += 1
        rows[pivot] = mask, rhs
    measured["combined_affine_rank"] = len(rows)
    witness = sum(rhs << pivot for pivot, (_, rhs) in rows.items())
    if witness >> n:
        raise AssertionError("Gaussian terminal produced an out-of-scope witness")
    for clause in clauses:
        measured["witness_clause_checks"] += 1
        if not any(bool((witness >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause):
            raise AssertionError("Gaussian terminal violated a local clause")
    for mask, rhs in equations:
        measured["witness_affine_checks"] += 1
        if (witness & mask).bit_count() % 2 != rhs:
            raise AssertionError("Gaussian terminal violated an affine row")
    return finish("SAT", "unit_affine_gaussian_model", witness)


def solve_decomposed(n: int, clauses, equations, decomposition, mode="2cnf",
                     strategy="polynomial", term_cap=None, seed_cap=None):
    """Solve an explicit forest decomposition and return status/witness/audit data.

    decomposition = {"bags": [[zero_based_global_var, ...], ...],
                     "edges": [[bag_index, bag_index], ...],
                     "discovery_counters": {...}}.
    Input identifiers are a declared integer variable namespace. Callers that read
    sparse external identifiers should first relabel them densely, as in the prior
    compiler. Bad input or a bad decomposition raises ValueError; resource caps
    produce UNRESOLVED. Every input and decomposition record is validated before
    any SAT/UNSAT conclusion.
    """
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError("n must be a nonnegative integer")
    if mode not in ("2cnf", "horn"):
        raise ValueError("mode must be '2cnf' or 'horn'")
    if strategy == "seed":
        strategy = "seeds"
    if strategy not in ("polynomial", "seeds"):
        raise ValueError("strategy must be 'polynomial' or 'seeds'")
    if not _valid_cap(term_cap) or not _valid_cap(seed_cap):
        raise ValueError("Caps must be nonnegative integers or None")
    if not isinstance(decomposition, dict):
        raise ValueError("The decomposition must be an object")
    if "bags" not in decomposition or "edges" not in decomposition:
        raise ValueError("The decomposition must supply bags and edges")
    if not isinstance(decomposition["bags"], (list, tuple)) or not isinstance(decomposition["edges"], (list, tuple)):
        raise ValueError("bags and edges must be explicit sequences")
    discovery = decomposition.get("discovery_counters", {})
    if not isinstance(discovery, dict):
        raise ValueError("discovery_counters must be an object")
    counters = {name: 0 for name in (
        "input_literal_visits", "input_affine_rows", "bag_memberships_read",
        "forest_edges_checked", "running_intersection_variables",
        "factor_containment_tests", "factor_scope_memberships",
        "local_remapped_literals", "local_remapped_affine_coefficients",
        "local_rank_pivot_tests", "local_rank_row_additions", "message_clauses",
        "message_literal_occurrences", "pin_clauses", "backend_calls",
        "frozen_backend_calls", "affine_terminal_calls", "unit_affine_recognition_calls",
        "unit_affine_recognition_clauses", "unit_affine_recognition_literal_visits",
        "states_sat", "states_unsat", "states_unresolved", "child_state_selections",
        "reconstruction_bag_visits", "reconstruction_variable_visits",
        "witness_clause_checks", "witness_affine_checks",
    )}
    counters.update(discovery_counters=discovery, mode=mode, strategy=strategy,
                    term_cap=term_cap, seed_cap=seed_cap)

    original_clauses = []
    clause_scopes = []
    for raw in clauses:
        clause = tuple(raw)
        counters["input_literal_visits"] += len(clause)
        if mode == "2cnf" and len(clause) > 2:
            raise ValueError("A 2-CNF clause has more than two literals")
        if any(not isinstance(lit, int) or isinstance(lit, bool) or lit == 0 or abs(lit) > n
               for lit in clause):
            raise ValueError("Invalid clause literal")
        unique = set(clause)
        tautological = any(-lit in unique for lit in unique)
        if mode == "horn" and not tautological and sum(lit > 0 for lit in unique) > 1:
            raise ValueError("A nontautological input clause is not Horn")
        original_clauses.append(clause)
        clause_scopes.append({abs(lit) - 1 for lit in clause})
    original_equations = []
    equation_scopes = []
    for row in equations:
        if len(row) != 2:
            raise ValueError("Every affine equation must be (mask,rhs)")
        mask, rhs = row
        if (not isinstance(mask, int) or isinstance(mask, bool) or mask < 0 or mask >> n
                or rhs not in (0, 1)):
            raise ValueError("Invalid affine equation")
        original_equations.append((mask, int(rhs)))
        equation_scopes.append(set(_bits(mask)))
        counters["input_affine_rows"] += 1

    bags = []
    bag_sets = []
    occurrences = {}
    for index, raw in enumerate(decomposition["bags"]):
        if not isinstance(raw, (list, tuple)):
            raise ValueError("Every bag must be an explicit variable sequence")
        bag = tuple(raw)
        if any(not isinstance(v, int) or isinstance(v, bool) or not 0 <= v < n for v in bag):
            raise ValueError("A bag contains an invalid variable identifier")
        if len(set(bag)) != len(bag):
            raise ValueError("A bag repeats a variable")
        bag = tuple(sorted(bag))
        bags.append(bag)
        bag_sets.append(set(bag))
        counters["bag_memberships_read"] += len(bag)
        for v in bag:
            occurrences.setdefault(v, []).append(index)
    count = len(bags)
    adjacency = [[] for _ in bags]
    union_parent = list(range(count))

    def representative(x):
        while union_parent[x] != x:
            union_parent[x] = union_parent[union_parent[x]]
            x = union_parent[x]
        return x

    edges_seen = set()
    separator_bound = 2 if mode == "2cnf" else 1
    connecting_edges = {v: 0 for v in occurrences}
    for raw in decomposition["edges"]:
        if not isinstance(raw, (list, tuple)) or len(raw) != 2:
            raise ValueError("Every forest edge must have two bag indices")
        a, b = raw
        if any(not isinstance(x, int) or isinstance(x, bool) or not 0 <= x < count for x in (a, b)):
            raise ValueError("Invalid bag index in a forest edge")
        if a == b:
            raise ValueError("A forest cannot contain a self-edge")
        edge = tuple(sorted((a, b)))
        if edge in edges_seen:
            raise ValueError("A forest repeats an undirected edge")
        edges_seen.add(edge)
        first, second = representative(a), representative(b)
        if first == second:
            raise ValueError("The decomposition contains a cycle")
        union_parent[first] = second
        separator = bag_sets[a] & bag_sets[b]
        if len(separator) > separator_bound:
            raise ValueError("An adhesion exceeds the selected message-language bound")
        for v in separator:
            connecting_edges[v] += 1
        adjacency[a].append(b)
        adjacency[b].append(a)
        counters["forest_edges_checked"] += 1
    for variable, containing in occurrences.items():
        counters["running_intersection_variables"] += 1
        # In a forest, the induced occurrence subgraph is connected exactly when
        # its number of edges is its number of vertices minus one.
        if connecting_edges[variable] != len(containing) - 1:
            raise ValueError(f"Running intersection fails for variable {variable}")
    for neighbors in adjacency:
        neighbors.sort()

    assigned_clauses = [[] for _ in bags]
    assigned_equations = [[] for _ in bags]
    clause_owners = []
    equation_owners = []
    constant_clauses = []
    constant_equations = []

    def first_container(scope):
        counters["factor_scope_memberships"] += len(scope)
        for index, bag in enumerate(bag_sets):
            counters["factor_containment_tests"] += 1
            if scope <= bag:
                return index
        if scope:
            raise ValueError("An original factor has no containing bag")
        return None  # zero-scope factors are handled globally only if no bags exist

    for i, scope in enumerate(clause_scopes):
        owner = first_container(scope)
        clause_owners.append(owner)
        if owner is None:
            constant_clauses.append(i)
        else:
            assigned_clauses[owner].append(i)
    for i, scope in enumerate(equation_scopes):
        owner = first_container(scope)
        equation_owners.append(owner)
        if owner is None:
            constant_equations.append(i)
        else:
            assigned_equations[owner].append(i)

    parents = [-2] * count
    children = [[] for _ in bags]
    roots = []
    traversal = []
    for start in range(count):
        if parents[start] != -2:
            continue
        parents[start] = -1
        roots.append(start)
        stack = [start]
        while stack:
            bag = stack.pop()
            traversal.append(bag)
            for other in reversed(adjacency[bag]):
                if other == parents[bag]:
                    continue
                if parents[other] != -2:
                    raise AssertionError("Validated forest orientation revisited a bag")
                parents[other] = bag
                children[bag].append(other)
                stack.append(other)
            children[bag].sort()

    results = [None] * count
    overall = {"status": None, "witness": None, "reason": None, "counters": counters,
               "component_roots": roots, "bag_results": results,
               "factor_owners": {"clauses": clause_owners, "equations": equation_owners},
               "global_constant_clause_indices": constant_clauses,
               "global_constant_equation_indices": constant_equations}
    counters.update(bags=count, forest_components=len(roots),
                    input_clauses=len(original_clauses), max_separator_size=0,
                    max_local_affine_rank=0, max_bag_variables=max(map(len, bags), default=0))
    if not count:
        contradiction = bool(constant_clauses) or any(original_equations[i][1] for i in constant_equations)
        overall.update(status="UNSAT" if contradiction else "SAT", witness=None if contradiction else 0,
                       reason="constant_factors_without_bags")
        if not contradiction:
            counters["witness_affine_checks"] = len(original_equations)
        return overall

    if strategy == "polynomial":
        from closure_parity import solve_2cnf_affine, solve_horn_affine
        solver = solve_2cnf_affine if mode == "2cnf" else solve_horn_affine
        cap_arguments = {"term_cap": term_cap}
    else:
        from seed_parity import solve_2cnf_affine_seeds, solve_horn_affine_seeds
        solver = solve_2cnf_affine_seeds if mode == "2cnf" else solve_horn_affine_seeds
        cap_arguments = {"seed_cap": seed_cap}

    for bag in reversed(traversal):
        variables = bags[bag]
        local = {v: j for j, v in enumerate(variables)}
        parent = parents[bag]
        separator = tuple(sorted(bag_sets[bag] & bag_sets[parent])) if parent >= 0 else ()
        counters["max_separator_size"] = max(counters["max_separator_size"], len(separator))
        local_clauses = []
        for i in assigned_clauses[bag]:
            translated = tuple((local[abs(lit) - 1] + 1) * (1 if lit > 0 else -1)
                               for lit in original_clauses[i])
            counters["local_remapped_literals"] += len(translated)
            local_clauses.append(translated)
        local_equations = []
        for i in assigned_equations[bag]:
            mask, rhs = original_equations[i]
            remapped = sum(1 << local[v] for v in _bits(mask))
            counters["local_remapped_affine_coefficients"] += mask.bit_count()
            local_equations.append((remapped, rhs))
        local_rank = _coefficient_rank((mask for mask, _ in local_equations), counters)
        counters["max_local_affine_rank"] = max(counters["max_local_affine_rank"], local_rank)
        message_clauses = []
        for child in children[bag]:
            message = results[child]
            for state in message["states"]:
                if state["status"] == "UNSAT":
                    clause = tuple(-(local[v] + 1) if (state["assignment"] >> j) & 1 else local[v] + 1
                                   for j, v in enumerate(message["separator"]))
                    message_clauses.append(clause)
                    counters["message_clauses"] += 1
                    counters["message_literal_occurrences"] += len(clause)
        entry = {"bag_index": bag, "parent": parent if parent >= 0 else None,
                 "variables": list(variables), "separator": list(separator),
                 "assigned_clause_indices": assigned_clauses[bag],
                 "assigned_equation_indices": assigned_equations[bag],
                 "local_affine_rank": local_rank,
                 "possible_child_message_clauses_local": message_clauses,
                 "states": []}
        results[bag] = entry
        for assignment in range(1 << len(separator)):
            pins = tuple(((local[v] + 1) if (assignment >> j) & 1 else -(local[v] + 1),)
                         for j, v in enumerate(separator))
            counters["pin_clauses"] += len(pins)
            counters["backend_calls"] += 1
            query_clauses = [*local_clauses, *message_clauses, *pins]
            backend = _try_unit_affine(len(variables), query_clauses, local_equations, counters)
            if backend is None:
                counters["frozen_backend_calls"] += 1
                backend = solver(len(variables), query_clauses, local_equations, **cap_arguments)
            else:
                counters["affine_terminal_calls"] += 1
            status = backend["status"]
            if status not in ("SAT", "UNSAT", "UNRESOLVED"):
                raise AssertionError("The exact backend returned an unknown status")
            selected = []
            witness = None
            reason = "possible_relaxation_unsatisfiable" if status == "UNSAT" else "backend_resource_cap"
            if status == "SAT":
                candidate = backend["witness"]
                if not isinstance(candidate, int) or candidate < 0 or candidate >> len(variables):
                    raise AssertionError("The backend supplied an invalid local witness")
                if any(((candidate >> local[v]) & 1) != ((assignment >> j) & 1)
                       for j, v in enumerate(separator)):
                    raise AssertionError("The backend witness violates a separator pin")
                for child in children[bag]:
                    child_message = results[child]
                    child_assignment = sum(((candidate >> local[v]) & 1) << j
                                           for j, v in enumerate(child_message["separator"]))
                    child_status = child_message["states"][child_assignment]["status"]
                    counters["child_state_selections"] += 1
                    if child_status == "UNSAT":
                        raise AssertionError("A local witness selected a forbidden child state")
                    selected.append({"bag_index": child, "assignment": child_assignment,
                                     "status": child_status})
                if all(state["status"] == "SAT" for state in selected):
                    witness = candidate
                    reason = "local_model_and_certified_child_completions"
                else:
                    status = "UNRESOLVED"
                    reason = "local_model_selects_unresolved_child_state"
            counters[{"SAT": "states_sat", "UNSAT": "states_unsat", "UNRESOLVED": "states_unresolved"}[status]] += 1
            entry["states"].append({"assignment": assignment, "status": status,
                                    "local_witness": witness, "child_states": selected,
                                    "reason": reason, "backend": backend})

    root_states = [results[root]["states"][0] for root in roots]
    if any(state["status"] == "UNSAT" for state in root_states):
        overall.update(status="UNSAT", reason="a_forest_component_is_unsatisfiable")
        return overall
    if any(state["status"] == "UNRESOLVED" for state in root_states):
        overall.update(status="UNRESOLVED", reason="a_forest_component_remains_unresolved")
        return overall

    known = {}
    witness = 0
    pending = [(root, 0) for root in reversed(roots)]
    while pending:
        bag, assignment = pending.pop()
        entry = results[bag]
        state = entry["states"][assignment]
        if state["status"] != "SAT" or state["local_witness"] is None:
            raise AssertionError("Reconstruction reached an uncertified state")
        counters["reconstruction_bag_visits"] += 1
        candidate = state["local_witness"]
        for j, variable in enumerate(entry["variables"]):
            value = (candidate >> j) & 1
            counters["reconstruction_variable_visits"] += 1
            if variable in known and known[variable] != value:
                raise AssertionError("Two bag witnesses disagree on a shared variable")
            known[variable] = value
            if value:
                witness |= 1 << variable
        pending.extend((child["bag_index"], child["assignment"])
                       for child in reversed(state["child_states"]))
    for clause in original_clauses:
        counters["witness_clause_checks"] += 1
        if not any(bool((witness >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause):
            raise AssertionError("Reconstructed witness violates an original clause")
    for mask, rhs in original_equations:
        counters["witness_affine_checks"] += 1
        if (mask & witness).bit_count() % 2 != rhs:
            raise AssertionError("Reconstructed witness violates an original affine row")
    overall.update(status="SAT", witness=witness, reason="all_component_witnesses_reconstructed_and_checked")
    return overall


if __name__ == "__main__":
    import argparse
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="JSON object with n, clauses, equations, decomposition")
    parser.add_argument("--mode", choices=("2cnf", "horn"), default="2cnf")
    parser.add_argument("--strategy", choices=("polynomial", "seeds"), default="polynomial")
    parser.add_argument("--term-cap", type=int)
    parser.add_argument("--seed-cap", type=int)
    args = parser.parse_args()
    with open(args.input, encoding="utf-8") as handle:
        instance = json.load(handle)
    result = solve_decomposed(instance["n"], instance["clauses"], instance["equations"],
                              instance["decomposition"], args.mode, args.strategy,
                              args.term_cap, args.seed_cap)
    print(json.dumps(result, indent=2))
