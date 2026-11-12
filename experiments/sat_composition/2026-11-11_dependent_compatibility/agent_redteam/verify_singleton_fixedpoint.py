"""Verify a 33-variable UNSAT selector system survives all singleton probes.

The reduced product exchanges the complete affine hull of a 2-CNF relation
with every unary/binary consequence of its affine component. No SAT oracle
is used. A separate graph-coloring search certifies UNSAT.
"""

from pathlib import Path
from itertools import combinations, product
import hashlib
import json
import time


def affine_basis(equations):
    basis = {}
    for mask, bit in equations:
        while mask:
            pivot = mask.bit_length() - 1
            if pivot in basis:
                row, rhs = basis[pivot]
                mask ^= row
                bit ^= rhs
            else:
                basis[pivot] = (mask, bit)
                break
        if not mask and bit:
            return None
    return basis


def consequence(basis, mask):
    bit = 0
    while mask:
        pivot = mask.bit_length() - 1
        if pivot not in basis:
            return None
        row, rhs = basis[pivot]
        mask ^= row
        bit ^= rhs
    return bit


def two_cnf_hull(n, clauses):
    reach = [1 << i for i in range(2 * n)]
    def literal(value):
        return 2 * (abs(value) - 1) + int(value < 0)
    for a, b in clauses:
        aa, bb = literal(a), literal(b)
        reach[aa ^ 1] |= 1 << bb
        reach[bb ^ 1] |= 1 << aa
    for pivot in range(2 * n):
        bit = 1 << pivot
        row = reach[pivot]
        for i in range(2 * n):
            if reach[i] & bit:
                reach[i] |= row
    def implies(a, b):
        return bool((reach[a] >> b) & 1)
    if any(implies(2 * i, 2 * i + 1) and implies(2 * i + 1, 2 * i) for i in range(n)):
        return None
    equations = []
    for i in range(n):
        if implies(2 * i + 1, 2 * i):
            equations.append((1 << i, 1))
        elif implies(2 * i, 2 * i + 1):
            equations.append((1 << i, 0))
    for i, j in combinations(range(n), 2):
        if implies(2 * i, 2 * j) and implies(2 * j, 2 * i):
            equations.append(((1 << i) | (1 << j), 0))
        elif implies(2 * i, 2 * j + 1) and implies(2 * j + 1, 2 * i):
            equations.append(((1 << i) | (1 << j), 1))
    return equations


def affine_binary_clauses(n, basis):
    clauses = set()
    for i in range(n):
        value = consequence(basis, 1 << i)
        if value is not None:
            literal = i + 1 if value else -(i + 1)
            clauses.add((literal, literal))
    for i, j in combinations(range(n), 2):
        value = consequence(basis, (1 << i) | (1 << j))
        x, y = i + 1, j + 1
        if value == 0:
            clauses.update([tuple(sorted((-x, y))), tuple(sorted((x, -y)))])
        elif value == 1:
            clauses.update([(x, y), (-y, -x)])
    return clauses


def reduced_product(n, initial_clauses, initial_equations, probe=None):
    clauses = {tuple(sorted(clause)) for clause in initial_clauses}
    if probe is not None:
        variable, value = probe
        literal = variable + 1 if value else -(variable + 1)
        clauses.add((literal, literal))
    equations = list(initial_equations)
    rounds = 0
    while True:
        rounds += 1
        hull = two_cnf_hull(n, clauses)
        if hull is None:
            return {"consistent": False, "reason": "2-CNF contradiction", "rounds": rounds}
        basis = affine_basis(equations + hull)
        if basis is None:
            return {"consistent": False, "reason": "affine contradiction", "rounds": rounds}
        binary = affine_binary_clauses(n, basis)
        new_clauses = binary - clauses
        equations = list(basis.values())
        if not new_clauses:
            return {"consistent": True, "rounds": rounds, "affine_rank": len(basis),
                    "H_hull_rank": len(affine_basis(hull)), "binary_clauses": len(clauses)}
        clauses.update(new_clauses)
        if rounds > 2 * n * n + 10:
            raise AssertionError("Reduced product failed to reach its finite fixed point")


def mycielski_cycle5():
    edges = {tuple(sorted((i, (i + 1) % 5))) for i in range(5)}
    for i in range(5):
        edges.add(tuple(sorted((i + 5, (i - 1) % 5))))
        edges.add(tuple(sorted((i + 5, (i + 1) % 5))))
        edges.add((i + 5, 10))
    return sorted(edges)


def graph_coloring_count(vertices, edges):
    neighbors = [set() for _ in range(vertices)]
    for a, b in edges:
        neighbors[a].add(b)
        neighbors[b].add(a)
    colors = [-1] * vertices
    nodes = 0
    def search():
        nonlocal nodes
        nodes += 1
        free = [v for v in range(vertices) if colors[v] < 0]
        if not free:
            return 1
        vertex = max(free, key=lambda v: (len({colors[u] for u in neighbors[v] if colors[u] >= 0}), len(neighbors[v])))
        excluded = {colors[u] for u in neighbors[vertex] if colors[u] >= 0}
        total = 0
        for color in range(3):
            if color not in excluded:
                colors[vertex] = color
                total += search()
        colors[vertex] = -1
        return total
    return search(), nodes


def audit_small_hull():
    """Check the hull implementation on every three-bit 2-CNF relation."""
    clauses = [(s * (i + 1), s * (i + 1)) for i in range(3) for s in (-1, 1)]
    clauses += [(s * (i + 1), t * (j + 1))
                for i, j in combinations(range(3), 2)
                for s, t in product((-1, 1), repeat=2)]
    def accepts(value, clause):
        return any(bool((value >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause)
    checked = 0
    for mask in range(256):
        points = {x for x in range(8) if (mask >> x) & 1}
        formula = [clause for clause in clauses if all(accepts(x, clause) for x in points)]
        actual = {x for x in range(8) if all(accepts(x, clause) for clause in formula)}
        if actual != points:
            continue
        hull = two_cnf_hull(3, formula)
        if not points:
            assert hull is None
        else:
            origin = next(iter(points))
            span = {0}
            for x in points:
                span |= {v ^ x ^ origin for v in list(span)}
            expected = {v ^ origin for v in span}
            observed = {x for x in range(8) if all(((row & x).bit_count() & 1) == bit for row, bit in hull)}
            assert observed == expected
        checked += 1
    assert checked == 166
    return checked


def main():
    started = time.perf_counter()
    small_hull_relations = audit_small_hull()
    edges = mycielski_cycle5()
    assert len(edges) == 20
    eset = set(edges)
    assert not any(all(tuple(sorted(pair)) in eset for pair in combinations(triple, 2))
                   for triple in combinations(range(11), 3))
    clauses = []
    for vertex in range(11):
        for c1, c2 in combinations(range(3), 2):
            clauses.append((-(3 * vertex + c1 + 1), -(3 * vertex + c2 + 1)))
    for a, b in edges:
        for color in range(3):
            clauses.append((-(3 * a + color + 1), -(3 * b + color + 1)))
    equations = [((7 << (3 * vertex)), 1) for vertex in range(11)]
    count, nodes = graph_coloring_count(11, edges)
    assert count == 0
    base = reduced_product(33, clauses, equations)
    assert base["consistent"]
    probes = []
    for variable in range(33):
        for value in (0, 1):
            result = reduced_product(33, clauses, equations, (variable, value))
            assert result["consistent"], (variable, value, result)
            probes.append({"variable": variable + 1, "value": value, **result})
    instance = {"variables": 33, "graph_vertices": 11, "graph_edges": edges,
                "H_clauses": clauses, "A_equations": equations}
    Path(__file__).with_name("singleton_fixedpoint_instance.json").write_text(json.dumps(instance, indent=2) + "\n")
    cnf = list(clauses)
    for vertex in range(11):
        p, q, r = 3 * vertex + 1, 3 * vertex + 2, 3 * vertex + 3
        cnf.extend([(p, q, r), (p, -q, -r), (-p, q, -r), (-p, -q, r)])
    assert len(cnf) == 137
    cnf_text = (
        "c Mycielski(C5) three-color selector encoding; UNSAT by the odd-cycle recoloring proof.\n"
        "c Variables 3v+1,3v+2,3v+3 represent the three colors of graph vertex v.\n"
        f"p cnf 33 {len(cnf)}\n"
        + "".join(" ".join(map(str, clause)) + " 0\n" for clause in cnf)
    )
    Path(__file__).with_name("mycielski_selector_33.cnf").write_text(cnf_text)
    report = {"status": "all assertions passed", "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "runtime_seconds": time.perf_counter() - started, "graph_coloring_count": count,
              "graph_coloring_search_nodes": nodes, "H_clause_count": len(clauses),
              "affine_equation_count": len(equations), "base": base,
              "exhaustive_small_hull_relations": small_hull_relations,
              "consistent_singleton_probes": len(probes), "probes": probes,
              "probe_round_counts": sorted({probe["rounds"] for probe in probes}),
              "scope": "UNSAT survives the specified exact reduced product and every independent singleton probe; stronger methods may solve it."}
    Path(__file__).with_name("singleton_fixedpoint_validation.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: value for key, value in report.items() if key != "probes"}, indent=2))


if __name__ == "__main__":
    main()
