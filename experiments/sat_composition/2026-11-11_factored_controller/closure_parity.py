#!/usr/bin/env python3
"""Exact deterministic 2-CNF plus affine-equation solver.

The algorithm operates over the implication-closed sets of one translated 2-SAT
solution.  It multiplies parity indicators in the corresponding Boolean-function
basis.  For affine rank d there are at most sum_{j<=d} binom(n,j) possible surviving
keys.  This is an XP algorithm, not an all-input polynomial SAT algorithm.

solve_2cnf_affine(n, clauses, equations, term_cap=None) returns a dictionary with
status SAT/UNSAT/UNRESOLVED, an original-variable integer witness for SAT, a reason,
and counters. Clauses use signed one-based literals. An affine row is (mask,rhs).

term_cap limits each polynomial's size, including every temporary product prefix
BEFORE later XOR cancellations. It is not a limit on every kind of memory or on
elapsed time. At most three polynomial sets are live in multiplication; their
combined size is separately recorded. No capped exit is classified as UNSAT.
"""
from __future__ import annotations


def _bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def _rref(equations, counters):
    rows = {}
    for mask, rhs in equations:
        counters["gaussian_input_rows"] += 1
        for pivot in sorted(rows):
            counters["gaussian_pivot_tests"] += 1
            if (mask >> pivot) & 1:
                other, value = rows[pivot]
                mask ^= other
                rhs ^= value
                counters["gaussian_row_additions"] += 1
        if not mask:
            if rhs:
                return None
            continue
        pivot = (mask & -mask).bit_length() - 1
        for p, (other, value) in list(rows.items()):
            counters["gaussian_pivot_tests"] += 1
            if (other >> pivot) & 1:
                rows[p] = other ^ mask, value ^ rhs
                counters["gaussian_row_additions"] += 1
        rows[pivot] = mask, rhs
    return tuple(rows[p] for p in sorted(rows))


def _two_sat_model(n, clauses, counters):
    graph = [[] for _ in range(2 * n)]
    reverse = [[] for _ in range(2 * n)]

    def vertex(literal):
        return 2 * (abs(literal) - 1) + int(literal < 0)

    def edge(u, v):
        graph[u].append(v)
        reverse[v].append(u)
        counters["scc_edges_created"] += 1

    for clause in clauses:
        if not clause:
            return None
        first = vertex(clause[0])
        if len(clause) == 1:
            edge(first ^ 1, first)
        else:
            second = vertex(clause[1])
            edge(first ^ 1, second)
            edge(second ^ 1, first)
    seen = [False] * (2 * n)
    order = []
    for start in range(2 * n):
        if seen[start]:
            continue
        seen[start] = True
        stack = [(start, 0)]
        while stack:
            node, position = stack[-1]
            if position == len(graph[node]):
                order.append(node)
                stack.pop()
                continue
            other = graph[node][position]
            counters["scc_edge_scans"] += 1
            stack[-1] = node, position + 1
            if not seen[other]:
                seen[other] = True
                stack.append((other, 0))
    component = [-1] * (2 * n)
    identity = 0
    for start in reversed(order):
        if component[start] != -1:
            continue
        component[start] = identity
        stack = [start]
        while stack:
            node = stack.pop()
            for other in reverse[node]:
                counters["scc_edge_scans"] += 1
                if component[other] == -1:
                    component[other] = identity
                    stack.append(other)
        identity += 1
    if any(component[2 * j] == component[2 * j + 1] for j in range(n)):
        return None
    return sum(int(component[2 * j] > component[2 * j + 1]) << j for j in range(n))


def solve_2cnf_affine(n: int, clauses, equations, term_cap: int | None = None):
    """Decide 2-SAT with affine restrictions, with exact original-variable witnesses.

    All inputs are read and validated before any mathematical decision. The explicit
    input model includes n variable slots; callers handling sparse identifiers should
    first relabel them densely. No claim about malformed inputs is inferred from a
    failed cap: malformed encodings raise ValueError.
    """
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError("n must be a nonnegative integer")
    if term_cap is not None and (not isinstance(term_cap, int) or isinstance(term_cap, bool) or term_cap < 0):
        raise ValueError("term_cap must be a nonnegative integer or None")
    counters = {name: 0 for name in (
        "input_clauses", "input_literal_visits", "input_affine_rows",
        "gaussian_input_rows", "gaussian_pivot_tests", "gaussian_row_additions",
        "scc_edges_created", "scc_edge_scans", "translation_clause_visits",
        "implication_edges", "conflict_pairs", "closure_starts",
        "closure_queue_pops", "closure_edge_scans", "consistency_checks",
        "consistency_variable_scans", "parity_variable_visits",
        "candidate_products", "rejected_products", "factor_rejected_terms",
        "factor_xor_cancellations", "product_xor_cancellations",
        "term_insertions", "peak_polynomial_terms", "peak_live_polynomial_terms",
        "max_prospective_polynomial_terms", "affine_rows_processed", "witness_clause_checks",
        "witness_affine_checks",
    )}
    counters["polynomial_stage_sizes"] = []
    counters["parity_factor_sizes"] = []
    counters["term_cap"] = term_cap
    original_clauses = []
    canonical_clauses = []
    for raw_clause in clauses:
        clause = tuple(raw_clause)
        counters["input_clauses"] += 1
        counters["input_literal_visits"] += len(clause)
        if len(clause) > 2 or any(not isinstance(lit, int) or isinstance(lit, bool)
                                  or lit == 0 or abs(lit) > n for lit in clause):
            raise ValueError("Every clause must have zero, one or two valid literals")
        original_clauses.append(clause)
        unique = set(clause)
        if any(-lit in unique for lit in unique):
            continue
        canonical_clauses.append(tuple(sorted(unique)))
    original_equations = []
    for row in equations:
        if len(row) != 2:
            raise ValueError("Every affine row must be a (mask,rhs) pair")
        mask, rhs = row
        if (not isinstance(mask, int) or isinstance(mask, bool) or mask < 0 or mask >> n
                or rhs not in (0, 1)):
            raise ValueError("Invalid affine row")
        original_equations.append((mask, int(rhs)))
        counters["input_affine_rows"] += 1

    def finish(status, reason, witness=None):
        if status == "SAT":
            for clause in original_clauses:
                counters["witness_clause_checks"] += 1
                if not any(bool((witness >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause):
                    raise AssertionError("Returned witness does not satisfy the original 2-CNF")
            for mask, rhs in original_equations:
                counters["witness_affine_checks"] += 1
                if (mask & witness).bit_count() % 2 != rhs:
                    raise AssertionError("Returned witness does not satisfy original affine rows")
        return {"status": status, "witness": witness, "reason": reason, "counters": counters}

    affine = _rref(original_equations, counters)
    if affine is None:
        return finish("UNSAT", "inconsistent_affine_system")
    counters["affine_rank"] = len(affine)
    base = _two_sat_model(n, canonical_clauses, counters)
    if base is None:
        return finish("UNSAT", "two_cnf_unsatisfiable")
    counters["base_assignment"] = base
    if all((base & mask).bit_count() % 2 == rhs for mask, rhs in affine):
        return finish("SAT", "initial_two_sat_witness_satisfies_affine_rows", base)

    # Substitute x=base XOR y.  Since y=0 satisfies the translated formula,
    # every remaining clause is a negative unit, an implication, or a conflict.
    graph_sets = [set() for _ in range(n)]
    conflicts = [0] * n
    forced_zero = 0
    for clause in canonical_clauses:
        counters["translation_clause_visits"] += 1
        translated = tuple(-lit if (base >> (abs(lit) - 1)) & 1 else lit for lit in clause)
        if len(translated) == 1:
            if translated[0] > 0:
                raise AssertionError("Base model did not satisfy a unit")
            forced_zero |= 1 << (-translated[0] - 1)
        elif len(translated) == 2:
            a, b = translated
            if a < 0 and b < 0:
                i, j = -a - 1, -b - 1
                if not (conflicts[i] >> j) & 1:
                    counters["conflict_pairs"] += 1
                conflicts[i] |= 1 << j
                conflicts[j] |= 1 << i
            elif a < 0 or b < 0:
                negative, positive = (a, b) if a < 0 else (b, a)
                graph_sets[-negative - 1].add(positive - 1)
            else:
                raise AssertionError("Base model did not satisfy a positive pair")
    graph = [tuple(sorted(neighbors)) for neighbors in graph_sets]
    counters["implication_edges"] = sum(map(len, graph))
    closures = []
    for start in range(n):
        counters["closure_starts"] += 1
        closed = 1 << start
        stack = [start]
        while stack:
            node = stack.pop()
            counters["closure_queue_pops"] += 1
            for other in graph[node]:
                counters["closure_edge_scans"] += 1
                if not (closed >> other) & 1:
                    closed |= 1 << other
                    stack.append(other)
        closures.append(closed)

    def consistent(closed):
        counters["consistency_checks"] += 1
        if closed & forced_zero:
            return False
        if not counters["conflict_pairs"]:
            return True
        for variable in _bits(closed):
            counters["consistency_variable_scans"] += 1
            if conflicts[variable] & closed:
                return False
        return True

    valid_closure = [consistent(closed) for closed in closures]

    class CapReached(Exception):
        pass

    def insert_or_cancel(poly, key, counter_name):
        if key in poly:
            poly.remove(key)
            counters[counter_name] += 1
            return
        prospective = len(poly) + 1
        counters["max_prospective_polynomial_terms"] = max(
            counters["max_prospective_polynomial_terms"], prospective)
        if term_cap is not None and prospective > term_cap:
            raise CapReached
        poly.add(key)
        counters["term_insertions"] += 1
        counters["peak_polynomial_terms"] = max(counters["peak_polynomial_terms"], len(poly))

    def live(*polynomials):
        counters["peak_live_polynomial_terms"] = max(
            counters["peak_live_polynomial_terms"], sum(map(len, polynomials)))

    polynomial = set()
    try:
        insert_or_cancel(polynomial, 0, "product_xor_cancellations")
        counters["polynomial_stage_sizes"].append(1)
        live(polynomial)
        for mask, rhs in affine:
            factor = set()
            constant = 1 ^ rhs ^ ((base & mask).bit_count() % 2)
            if constant:
                insert_or_cancel(factor, 0, "factor_xor_cancellations")
                live(polynomial, factor)
            for variable in _bits(mask):
                counters["parity_variable_visits"] += 1
                if valid_closure[variable]:
                    insert_or_cancel(factor, closures[variable], "factor_xor_cancellations")
                    live(polynomial, factor)
                else:
                    counters["factor_rejected_terms"] += 1
            counters["parity_factor_sizes"].append(len(factor))
            output = set()
            # Sort for deterministic execution and reproducible prefix/cap metrics.
            for left in sorted(polynomial):
                for right in sorted(factor):
                    counters["candidate_products"] += 1
                    merged = left | right  # a union of implication-closed sets is closed
                    if not consistent(merged):
                        counters["rejected_products"] += 1
                        continue
                    insert_or_cancel(output, merged, "product_xor_cancellations")
                    live(polynomial, factor, output)
            polynomial = output
            counters["affine_rows_processed"] += 1
            counters["polynomial_stage_sizes"].append(len(polynomial))
            if not polynomial:
                return finish("UNSAT", "parity_indicator_polynomial_is_zero")
    except CapReached:
        return finish("UNRESOLVED", "temporary_polynomial_term_cap_exceeded")

    # The least-cardinality remaining key is a model: every other monomial's
    # closed support is not contained in it, so exactly this term evaluates to one.
    chosen = min(polynomial, key=lambda key: (key.bit_count(), key))
    counters["witness_closed_set"] = chosen
    return finish("SAT", "nonzero_closed_set_indicator_polynomial", base ^ chosen)


def solve_horn_affine(n: int, clauses, equations, term_cap: int | None = None):
    """Exact Horn-CNF plus affine equations, using the Horn closure lattice.

    Horn clauses may have arbitrary width.  Each nontautological clause must have
    at most one positive literal after duplicate removal.  The constant basis key
    is cl_H(empty), and multiplication sends K,L to cl_H(K union L), or zero if
    closure contradicts a negative clause. The same sum-of-binomial XP bound holds.
    """
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise ValueError("n must be a nonnegative integer")
    if term_cap is not None and (not isinstance(term_cap, int) or isinstance(term_cap, bool) or term_cap < 0):
        raise ValueError("term_cap must be a nonnegative integer or None")
    counters = {name: 0 for name in (
        "input_clauses", "input_literal_visits", "input_affine_rows",
        "gaussian_input_rows", "gaussian_pivot_tests", "gaussian_row_additions",
        "closure_calls", "closure_rule_initializations", "closure_queue_pops",
        "closure_incidence_scans", "closure_rule_firings", "closure_conflicts",
        "closure_union_shortcuts", "parity_variable_visits", "candidate_products",
        "rejected_products", "factor_rejected_terms", "factor_xor_cancellations",
        "product_xor_cancellations", "term_insertions", "peak_polynomial_terms",
        "peak_live_polynomial_terms", "max_prospective_polynomial_terms",
        "affine_rows_processed", "witness_clause_checks", "witness_affine_checks",
    )}
    counters.update(polynomial_stage_sizes=[], parity_factor_sizes=[], term_cap=term_cap)
    original_clauses = []
    rules = []
    for raw_clause in clauses:
        clause = tuple(raw_clause)
        counters["input_clauses"] += 1
        counters["input_literal_visits"] += len(clause)
        if any(not isinstance(lit, int) or isinstance(lit, bool) or lit == 0 or abs(lit) > n for lit in clause):
            raise ValueError("Invalid Horn literal")
        original_clauses.append(clause)
        unique = set(clause)
        if any(-lit in unique for lit in unique):
            continue
        positive = [lit for lit in unique if lit > 0]
        if len(positive) > 1:
            raise ValueError("A nontautological clause is not Horn")
        antecedents = tuple(sorted(-lit - 1 for lit in unique if lit < 0))
        rules.append((antecedents, positive[0] - 1 if positive else None))
    original_equations = []
    for row in equations:
        if len(row) != 2:
            raise ValueError("Every affine row must be a (mask,rhs) pair")
        mask, rhs = row
        if (not isinstance(mask, int) or isinstance(mask, bool) or mask < 0 or mask >> n
                or rhs not in (0, 1)):
            raise ValueError("Invalid affine row")
        original_equations.append((mask, int(rhs)))
        counters["input_affine_rows"] += 1

    def finish(status, reason, witness=None):
        if status == "SAT":
            for clause in original_clauses:
                counters["witness_clause_checks"] += 1
                if not any(bool((witness >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause):
                    raise AssertionError("Returned witness does not satisfy original Horn clauses")
            for mask, rhs in original_equations:
                counters["witness_affine_checks"] += 1
                if (mask & witness).bit_count() % 2 != rhs:
                    raise AssertionError("Returned witness does not satisfy original affine rows")
        return {"status": status, "witness": witness, "reason": reason, "counters": counters}

    affine = _rref(original_equations, counters)
    if affine is None:
        return finish("UNSAT", "inconsistent_affine_system")
    counters["affine_rank"] = len(affine)
    occurrence = [[] for _ in range(n)]
    initial_counts = []
    zero_rules = []
    for j, (antecedents, head) in enumerate(rules):
        initial_counts.append(len(antecedents))
        if not antecedents:
            zero_rules.append(j)
        for variable in antecedents:
            occurrence[variable].append(j)

    def closure(seed):
        counters["closure_calls"] += 1
        counters["closure_rule_initializations"] += len(rules)
        pending = initial_counts.copy()
        closed = seed
        queue = list(_bits(seed))
        for j in zero_rules:
            head = rules[j][1]
            counters["closure_rule_firings"] += 1
            if head is None:
                counters["closure_conflicts"] += 1
                return None
            if not (closed >> head) & 1:
                closed |= 1 << head
                queue.append(head)
        while queue:
            variable = queue.pop()
            counters["closure_queue_pops"] += 1
            for j in occurrence[variable]:
                counters["closure_incidence_scans"] += 1
                pending[j] -= 1
                if pending[j] == 0:
                    counters["closure_rule_firings"] += 1
                    head = rules[j][1]
                    if head is None:
                        counters["closure_conflicts"] += 1
                        return None
                    if not (closed >> head) & 1:
                        closed |= 1 << head
                        queue.append(head)
        return closed

    least = closure(0)
    if least is None:
        return finish("UNSAT", "horn_formula_unsatisfiable")
    counters["least_horn_model"] = least
    if all((least & mask).bit_count() % 2 == rhs for mask, rhs in affine):
        return finish("SAT", "least_horn_model_satisfies_affine_rows", least)
    singletons = [closure(1 << j) for j in range(n)]

    class CapReached(Exception):
        pass

    def insert_or_cancel(poly, key, counter_name):
        if key in poly:
            poly.remove(key)
            counters[counter_name] += 1
            return
        prospective = len(poly) + 1
        counters["max_prospective_polynomial_terms"] = max(
            counters["max_prospective_polynomial_terms"], prospective)
        if term_cap is not None and prospective > term_cap:
            raise CapReached
        poly.add(key)
        counters["term_insertions"] += 1
        counters["peak_polynomial_terms"] = max(counters["peak_polynomial_terms"], len(poly))

    def live(*polynomials):
        counters["peak_live_polynomial_terms"] = max(
            counters["peak_live_polynomial_terms"], sum(map(len, polynomials)))

    polynomial = set()
    try:
        insert_or_cancel(polynomial, least, "product_xor_cancellations")
        counters["polynomial_stage_sizes"].append(1)
        live(polynomial)
        for mask, rhs in affine:
            factor = set()
            if 1 ^ rhs:
                insert_or_cancel(factor, least, "factor_xor_cancellations")
                live(polynomial, factor)
            for variable in _bits(mask):
                counters["parity_variable_visits"] += 1
                if singletons[variable] is None:
                    counters["factor_rejected_terms"] += 1
                else:
                    insert_or_cancel(factor, singletons[variable], "factor_xor_cancellations")
                    live(polynomial, factor)
            counters["parity_factor_sizes"].append(len(factor))
            output = set()
            for left in sorted(polynomial):
                for right in sorted(factor):
                    counters["candidate_products"] += 1
                    if left | right == left:
                        merged = left
                        counters["closure_union_shortcuts"] += 1
                    elif left | right == right:
                        merged = right
                        counters["closure_union_shortcuts"] += 1
                    else:
                        merged = closure(left | right)
                    if merged is None:
                        counters["rejected_products"] += 1
                        continue
                    insert_or_cancel(output, merged, "product_xor_cancellations")
                    live(polynomial, factor, output)
            polynomial = output
            counters["affine_rows_processed"] += 1
            counters["polynomial_stage_sizes"].append(len(polynomial))
            if not polynomial:
                return finish("UNSAT", "horn_parity_indicator_polynomial_is_zero")
    except CapReached:
        return finish("UNRESOLVED", "temporary_polynomial_term_cap_exceeded")
    chosen = min(polynomial, key=lambda key: (key.bit_count(), key))
    counters["witness_closed_set"] = chosen
    return finish("SAT", "nonzero_horn_closed_set_indicator_polynomial", chosen)


if __name__ == "__main__":
    import argparse
    import json
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="JSON object with n, clauses and equations")
    parser.add_argument("--term-cap", type=int)
    parser.add_argument("--horn", action="store_true", help="Use the general Horn-CNF engine")
    args = parser.parse_args()
    with open(args.input, encoding="utf-8") as handle:
        instance = json.load(handle)
    solver = solve_horn_affine if args.horn else solve_2cnf_affine
    result = solver(instance["n"], instance["clauses"], instance["equations"], args.term_cap)
    print(json.dumps(result, indent=2))
