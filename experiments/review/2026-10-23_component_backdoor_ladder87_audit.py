#!/usr/bin/env python3
"""Reproducible ladder control: connected 3-CNFs with k syntactic 2-CNF
backdoor variables but additive, not Cartesian-product, component work.

Stdlib only. Counters are logical operations, not CPU instructions or Python
heap bytes. Run: python ladder_component_backdoor87_audit.py --out results.json
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass, asdict
from itertools import product
import hashlib
import json
from pathlib import Path
import random
import time
from typing import Sequence

Clause = tuple[int, ...]
Formula = tuple[Clause, ...]

@dataclass
class Counts:
    acquisition_literal_visits: int = 0
    restriction_literal_visits: int = 0
    separator_assignments: int = 0
    local_assignments: int = 0
    scc_calls: int = 0
    scc_vertex_visits: int = 0
    scc_edge_visits: int = 0
    max_leaf_graph_vertices: int = 0
    max_leaf_graph_edges: int = 0
    max_dfs_stack_vertices: int = 0
    max_live_assignment_entries: int = 0

@dataclass
class Component:
    variables: list[int]
    clauses: list[Clause]
    hitting_set: list[int]

@dataclass
class Prepared:
    n: int
    separator: tuple[int, ...]
    shared: list[Clause]
    components: list[Component]
    local_index: list[int]


def prepare(formula: Formula, n: int, separator: Sequence[int], c: Counts) -> Prepared:
    """Given S, discover components and one hitting set per component.
    No claim to discover an optimal separator or minimum hitting set.
    """
    S = tuple(separator)
    if len(set(S)) != len(S) or any(v < 1 or v > n for v in S):
        raise ValueError('invalid separator')
    in_s = [False] * (n + 1)
    for v in S:
        in_s[v] = True
    graph: list[list[int]] = [[] for _ in range(n + 1)]
    present = [False] * (n + 1)
    for clause in formula:
        if len(clause) > 3:
            raise ValueError('only width-at-most-three CNF is supported')
        local = []
        for lit in clause:
            c.acquisition_literal_visits += 1
            if lit == 0 or abs(lit) > n:
                raise ValueError('literal outside declared range')
            v = abs(lit)
            if not in_s[v]:
                present[v] = True
                local.append(v)
        if local:
            a = local[0]
            for b in local[1:]:
                graph[a].append(b)
                graph[b].append(a)
    owner = [-1] * (n + 1)
    local_index = [0] * (n + 1)
    comps: list[Component] = []
    for root in range(1, n + 1):
        if not present[root] or owner[root] != -1:
            continue
        j = len(comps)
        owner[root] = j
        stack = [root]
        variables = []
        while stack:
            v = stack.pop()
            variables.append(v)
            local_index[v] = len(variables)
            for u in graph[v]:
                if owner[u] == -1:
                    owner[u] = j
                    stack.append(u)
        comps.append(Component(variables, [], []))
    shared: list[Clause] = []
    chosen = [False] * (n + 1)
    for clause in formula:
        local = []
        has_s = False
        for lit in clause:
            c.acquisition_literal_visits += 1
            if in_s[abs(lit)]:
                has_s = True
            else:
                local.append(abs(lit))
        if not local:
            shared.append(clause)
            continue
        j = owner[local[0]]
        if any(owner[v] != j for v in local):
            raise AssertionError('source coherence violated')
        comps[j].clauses.append(clause)
        # All ternary clauses touching S become binary or disappear.
        if len(clause) == 3 and not has_s and not any(chosen[v] for v in local):
            v = local[0]
            chosen[v] = True
            comps[j].hitting_set.append(v)
    return Prepared(n, S, shared, comps, local_index)


def two_sat(clauses: list[Clause], n: int, c: Counts) -> bool:
    """Iterative Kosaraju SCC implementation on locally numbered literals."""
    c.scc_calls += 1
    V = 2 * n
    graph: list[list[int]] = [[] for _ in range(V)]
    reverse: list[list[int]] = [[] for _ in range(V)]
    E = 0
    def node(lit: int) -> int:
        return 2 * (abs(lit) - 1) + int(lit < 0)
    for clause in clauses:
        if not clause:
            return False
        if len(clause) > 2:
            raise AssertionError('hitting-set certificate did not produce 2-CNF')
        a = node(clause[0])
        edges = [(a ^ 1, a)] if len(clause) == 1 else [
            (a ^ 1, node(clause[1])), (node(clause[1]) ^ 1, a)]
        for u, v in edges:
            graph[u].append(v)
            reverse[v].append(u)
            E += 1
    c.max_leaf_graph_vertices = max(c.max_leaf_graph_vertices, V)
    c.max_leaf_graph_edges = max(c.max_leaf_graph_edges, E)
    visited = [False] * V
    next_edge = [0] * V
    order: list[int] = []
    for root in range(V):
        if visited[root]:
            continue
        visited[root] = True
        c.scc_vertex_visits += 1
        stack = [root]
        while stack:
            c.max_dfs_stack_vertices = max(c.max_dfs_stack_vertices, len(stack))
            v = stack[-1]
            if next_edge[v] == len(graph[v]):
                order.append(v)
                stack.pop()
                continue
            u = graph[v][next_edge[v]]
            next_edge[v] += 1
            c.scc_edge_visits += 1
            if not visited[u]:
                visited[u] = True
                c.scc_vertex_visits += 1
                stack.append(u)
    color = [-1] * V
    color_id = 0
    for root in reversed(order):
        if color[root] != -1:
            continue
        color[root] = color_id
        stack = [root]
        while stack:
            c.max_dfs_stack_vertices = max(c.max_dfs_stack_vertices, len(stack))
            v = stack.pop()
            c.scc_vertex_visits += 1
            for u in reverse[v]:
                c.scc_edge_visits += 1
                if color[u] == -1:
                    color[u] = color_id
                    stack.append(u)
        color_id += 1
    return all(color[2*v] != color[2*v+1] for v in range(n))


def solve(formula: Formula, n: int, separator: Sequence[int]) -> tuple[bool, Counts, Prepared]:
    c = Counts()
    p = prepare(formula, n, separator, c)
    assignment = [-1] * (n + 1)
    for sigma in product((0, 1), repeat=len(p.separator)):
        c.separator_assignments += 1
        for v, value in zip(p.separator, sigma):
            assignment[v] = value
        shared_ok = True
        for clause in p.shared:
            c.restriction_literal_visits += len(clause)
            if not any(assignment[abs(lit)] == int(lit > 0) for lit in clause):
                shared_ok = False
                break
        if not shared_ok:
            continue
        all_ok = True
        for comp in p.components:
            local_ok = False
            H = comp.hitting_set
            c.max_live_assignment_entries = max(c.max_live_assignment_entries,
                                                 len(p.separator) + len(H))
            for eta in product((0, 1), repeat=len(H)):
                c.local_assignments += 1
                for v, value in zip(H, eta):
                    assignment[v] = value
                residual: list[Clause] = []
                for clause in comp.clauses:
                    keep = []
                    satisfied = False
                    for lit in clause:
                        c.restriction_literal_visits += 1
                        v = abs(lit)
                        value = assignment[v]
                        if value == -1:
                            ix = p.local_index[v]
                            keep.append(ix if lit > 0 else -ix)
                        elif value == int(lit > 0):
                            satisfied = True
                    if not satisfied:
                        residual.append(tuple(keep))
                result = two_sat(residual, len(comp.variables), c)
                for v in H:
                    assignment[v] = -1
                if result:
                    local_ok = True
                    break
            if not local_ok:
                all_ok = False
                break
        if all_ok:
            return True, c, p
    return False, c, p


def chain(bits: Sequence[int]) -> Formula:
    q = len(bits)
    return ((1,), (-(q+1),)) + tuple(
        (-i, (i+1) if bit else -(i+1)) for i, bit in enumerate(bits, start=1))


def family(bits: Sequence[int], k: int) -> tuple[Formula, int, int]:
    q = len(bits)
    if q < 2 or k < 1:
        raise ValueError('family requires q>=2 and k>=1')
    s = q + 2
    mid = q // 2 + 1
    clauses = list(chain(bits)) + [(-s, mid), (s, -mid)]
    for j in range(k):
        x = q + 3 + 3*j
        y, u = x+1, x+2
        clauses.extend([(x, y, u), (-x, -y), (-x, -u), (-y, -u), (s, -x)])
    return tuple(clauses), q + 2 + 3*k, s


def evaluate(formula: Formula, mask: int) -> bool:
    return all(any(((mask >> (abs(lit)-1)) & 1) == int(lit > 0)
                   for lit in clause) for clause in formula)


def brute_count(formula: Formula, n: int) -> int:
    return sum(evaluate(formula, mask) for mask in range(1 << n))


def encoding(formula: Formula, n: int) -> tuple[list[int], int]:
    # n,m headers; each record is arity + three signed literal slots.
    # Code 0 is padding; positive v is 2v, negative v is 2v+1.
    m = len(formula)
    # Include address capacity for all charged input and workspace arrays.
    w = max(1, (64*(n+m+1)-1).bit_length())
    words = [n, m]
    for clause in formula:
        words.extend([len(clause)] + [2*abs(lit)+int(lit<0) for lit in clause]
                     + [0] * (3-len(clause)))
    if any(value >= (1 << w) for value in words):
        raise AssertionError('word encoding overflow')
    return words, w



def canonical_decide(formula: Formula, n: int) -> bool | None:
    """Recognize the canonical family in one record scan and constant words.
    None means not this family, so a total SAT solver must use a fallback.
    """
    m = len(formula)
    difference = m - n - 2
    if difference < 2 or difference % 2:
        return None
    k = difference // 2
    q = n - 2 - 3*k
    if q < 2 or m != q+4+5*k:
        return None
    if formula[0] != (1,) or formula[1] != (-(q+1),):
        return None
    all_one = True
    for i in range(1, q+1):
        clause = formula[i+1]
        if len(clause) != 2 or clause[0] != -i or abs(clause[1]) != i+1:
            return None
        all_one = all_one and (clause[1] > 0)
    selector = q+2
    mid = q//2+1
    if formula[q+2] != (-selector, mid) or formula[q+3] != (selector, -mid):
        return None
    for j in range(k):
        x = q+3+3*j
        y, u = x+1, x+2
        expected = ((x,y,u),(-x,-y),(-x,-u),(-y,-u),(selector,-x))
        for offset, clause in enumerate(expected):
            if formula[q+4+5*j+offset] != clause:
                return None
    return not all_one



def coloring_cnf(k: int, edges: Sequence[tuple[int, int]]) -> Formula:
    """One exactly-one ternary gadget per vertex, only binary edge clauses."""
    clauses: list[Clause] = []
    for v in range(k):
        a, b, c = 3*v+1, 3*v+2, 3*v+3
        clauses.extend(((a,b,c),(-a,-b),(-a,-c),(-b,-c)))
    for u, v in edges:
        if not (0 <= u < v < k):
            raise ValueError('edges must be ordered distinct vertex pairs')
        for color in range(3):
            clauses.append((-(3*u+color+1), -(3*v+color+1)))
    return tuple(clauses)


def graph_colorings(k: int, edges: Sequence[tuple[int, int]]) -> int:
    return sum(all(colors[u] != colors[v] for u,v in edges)
               for colors in product(range(3), repeat=k))


def run() -> dict:
    assertions = 0
    def check(condition: bool) -> None:
        nonlocal assertions
        assertions += 1
        if not condition:
            raise AssertionError(f'assertion {assertions} failed')
    out: dict = {'run_id':'COMPONENT_BACKDOOR_LADDER87', 'seed':20261023,
                 'status':'COMPUTATIONAL', 'model':'logical operation counters; not timings or heap measurements'}
    # Independent SCC checks against all assignments, including empty clauses.
    rng = random.Random(20261023)
    random_cases = 0
    brute_assignments = 0
    for n in range(1, 10):
        for case in range(40):
            clauses = []
            for _ in range(rng.randrange(0, 2*n+5)):
                width = rng.randrange(1, min(3, n)+1)
                variables = rng.sample(range(1, n+1), width)
                clauses.append(tuple(v if rng.randrange(2) else -v for v in variables))
            if case == 0:
                clauses.append(())
            F = tuple(clauses)
            S = rng.sample(range(1, n+1), rng.randrange(min(3, n)+1))
            truth = brute_count(F, n) > 0
            brute_assignments += 1 << n
            answer, counts, prep = solve(F, n, S)
            check(answer == truth)
            cap = (1 << len(S)) * sum(1 << len(comp.hitting_set) for comp in prep.components)
            check(counts.scc_calls <= cap)
            random_cases += 1
    out['random_general_3cnf_cases'] = random_cases
    # Exhaustive orientations on the connected ladder extension.
    family_cases = 0
    irredundancy_witnesses = 0
    for q in range(2, 5):
        for k in (1, 2):
            for bits in product((0, 1), repeat=q):
                F, n, s = family(bits, k)
                truth_count = brute_count(F, n)
                brute_assignments += 1 << n
                answer, counts, prep = solve(F, n, (s,))
                check(answer == (not all(bits)))
                check(canonical_decide(F, n) == answer)
                check(answer == (truth_count > 0))
                check(len(F) == q+4+5*k)
                check(sum(map(len, F)) == 2*q+6+11*k)
                check(len(prep.components) == k+1)
                check(sum(len(C.hitting_set) for C in prep.components) == k)
                check(max(map(lambda C:len(C.hitting_set), prep.components)) == 1)
                check(counts.scc_calls <= 4*k+2)
                whole = prepare(F, n, (), Counts())
                check(len(whole.components) == 1)
                if answer:
                    first_zero = bits.index(0) + 1
                    mask = sum(1 << (i-1) for i in range(1, first_zero+1))
                    if (mask >> (q//2)) & 1:
                        mask |= 1 << (s-1)
                    for j in range(k):
                        y = q+4+3*j
                        mask |= 1 << (y-1)
                    check(evaluate(F, mask))
                    for j in range(k):
                        y = q+4+3*j
                        bad = mask & ~(1 << (y-1))
                        index = q+4+5*j
                        reduced = F[:index] + F[index+1:]
                        check(not evaluate(F, bad))
                        check(evaluate(reduced, bad))
                        irredundancy_witnesses += 1
                family_cases += 1
    out['exhaustive_connected_family_instances'] = family_cases
    out['ternary_irredundancy_witnesses'] = irredundancy_witnesses
    # Minimum syntactic 2-CNF backdoor = hitting number of disjoint triples.
    backdoor_subsets = 0
    for k in (1, 2, 3):
        F, n, s = family((0, 1), k)
        triples = [set(map(abs, C)) for C in F if len(C) == 3]
        best = n+1
        for mask in range(1 << n):
            H = {v for v in range(1, n+1) if (mask >> (v-1)) & 1}
            if all(H & triple for triple in triples):
                best = min(best, len(H))
            backdoor_subsets += 1
        check(best == k)
    out['backdoor_subsets_examined'] = backdoor_subsets
    # Actual word layout: a one-orientation flip changes exactly one data word.
    flip_controls = 0
    for q in (2, 3, 4, 8, 16, 32):
        F, n, s = family((1,)*q, 3)
        words, w = encoding(F, n)
        check(not solve(F, n, (s,))[0])
        for i in range(q):
            bits = [1]*q
            bits[i] = 0
            G, nn, ss = family(bits, 3)
            other, ww = encoding(G, nn)
            check(w == ww and n == nn and s == ss and len(words) == len(other))
            changes = [j for j, pair in enumerate(zip(words, other)) if pair[0] != pair[1]]
            check(len(changes) == 1)
            check((words[changes[0]] ^ other[changes[0]]) == 1)
            check(solve(G, nn, (ss,))[0])
            flip_controls += 1
    out['equal_length_one_bit_flip_controls'] = flip_controls
    # Mixed-source check: independently satisfiable local units cannot be joined.
    check(brute_count(((1,),), 1) == 1)
    check(brute_count(((-1,),), 1) == 1)
    check(not solve(((1,),(-1,)), 1, (1,))[0])
    # Increasing q=k. No brute-force solve is used at these sizes.
    scaling = []
    for k in (4, 8, 16, 32, 64, 128, 256):
        q = k
        for sat in (False, True):
            bits = [1]*q
            if sat:
                bits[0] = 0
            F, n, s = family(bits, k)
            words, w = encoding(F, n)
            answer, counts, prep = solve(F, n, (s,))
            check(answer == sat)
            check(canonical_decide(F, n) == sat)
            check(counts.scc_calls <= 4*k+2)
            scaling.append({'q':q, 'k':k, 'SAT':sat, 'n':n, 'm':len(F),
                'literal_occurrences':sum(map(len,F)), 'word_bits':w,
                'encoded_bits_N':len(words)*w, 'global_backdoor_size':k,
                'components_after_selector':len(prep.components),
                'SCC_call_upper_bound':4*k+2,
                'naive_global_assignments':str(1 << k), **asdict(counts)})
    # Negative control for template recognition: changing a private clause is not ignored.
    F, n, s = family((0,1,1), 2)
    corrupted = list(F)
    triple_index = 3+4
    x, y, u = corrupted[triple_index]
    corrupted[triple_index] = (-x, y, u)
    check(canonical_decide(tuple(corrupted), n) is None)
    check(solve(tuple(corrupted), n, (s,))[0] == (brute_count(tuple(corrupted), n)>0))
    brute_assignments += 1 << n
    # Binary coupling of the same one-hot ternary blocks reaches graph 3-coloring.
    graph_cases = 0
    graph_assignments = 0
    for k in range(1, 6):
        pairs = [(u,v) for u in range(k) for v in range(u+1,k)]
        for mask in range(1 << len(pairs)):
            edges = [edge for j,edge in enumerate(pairs) if (mask >> j)&1]
            F = coloring_cnf(k, edges)
            color_count = graph_colorings(k, edges)
            graph_assignments += 3**k
            check(solve(F, 3*k, ())[0] == (color_count > 0))
            check(len(F) == 4*k+3*len(edges))
            check(sum(map(len,F)) == 9*k+6*len(edges))
            if k <= 4:
                count = brute_count(F, 3*k)
                brute_assignments += 1 << (3*k)
                check(count == color_count)
            graph_cases += 1
    out['exhaustive_labeled_graphs_through_5_vertices'] = graph_cases
    out['three_color_assignments_tested'] = graph_assignments
    coupling_controls = []
    for k,edges,name in [
        (3,[(0,1),(1,2),(0,2)],'triangle_SAT'),
        (4,[(u,v) for u in range(4) for v in range(u+1,4)],'K4_UNSAT')]:
        F = coloring_cnf(k,edges)
        answer,counts,prep = solve(F,3*k,())
        coupling_controls.append({'name':name,'SAT':answer,'k':k,'n':3*k,
                                  'm':len(F),'edges':len(edges),**asdict(counts)})
        check(answer == (k == 3))
    out['coupling_controls'] = coupling_controls
    out['scaling'] = scaling
    out['total_bruteforce_assignments'] = brute_assignments
    out['assertions'] = assertions
    out['failures'] = 0
    out['limits'] = [
        'Finite checks validate code and stated examples, not asymptotic hardness.',
        'The upper bound uses a supplied separator; global optimum acquisition is not free.',
        'Minimum backdoor refers to plain syntactic restriction without unit propagation.',
        'Logical counters are not machine timings or measured physical peak memory.',
        'No superlinear or superpolynomial SAT lower bound is obtained.'
    ]
    return out


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=Path('ladder87_raw.json'))
    args = parser.parse_args()
    started = time.perf_counter()
    result = run()
    result['audit_wall_seconds'] = round(time.perf_counter() - started, 6)
    result['code_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k != 'scaling'}, indent=2))

if __name__ == '__main__':
    main()
