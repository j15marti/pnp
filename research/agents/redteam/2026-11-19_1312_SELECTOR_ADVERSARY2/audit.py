#!/usr/bin/env python3
"""Exact finite checks for SELECTOR-ADVERSARY2.

The tested family has one guarded, connected, trivially refutable block per
row.  Its residual strong Horn-backdoor number is q although unit propagation
already refutes it.  Brute force is used only as an independent finite oracle.
"""
from __future__ import annotations

import hashlib
import itertools as it
import json
from pathlib import Path


def bits(x, h):
    return tuple((x >> j) & 1 for j in range(h))


def mismatch(row):
    return tuple(j + 1 if bit == 0 else -(j + 1)
                 for j, bit in enumerate(row))


def connected_core(q, first):
    """Return C_q and next variable. C_q is connected and unit-refutable."""
    p = first
    xs = list(range(first + 1, first + 1 + q))
    ys = list(range(first + 1 + q, first + 1 + 2*q))
    clauses = [(p,), (-p,)]
    clauses += [(x, y) for x, y in zip(xs, ys)]
    clauses.append((-p, -xs[0]))
    clauses += [(-ys[j], -xs[j+1]) for j in range(q-1)]
    clauses.append((-ys[-1], -p))
    return clauses, first + 1 + 2*q


def guarded_block(h, bad_row, q, first):
    core, nxt = connected_core(q, first)
    g = mismatch(bad_row)
    return [g + c for c in core], nxt


def residual(clauses, fixed):
    out = []
    for clause in clauses:
        if any(abs(l) in fixed and fixed[abs(l)] == (l > 0) for l in clause):
            continue
        out.append(tuple(l for l in clause if abs(l) not in fixed))
    return out


def satisfies(clauses, assignment):
    return all(any(assignment[abs(l)] == (l > 0) for l in c) for c in clauses)


def brute_sat(clauses):
    variables = sorted({abs(l) for c in clauses for l in c})
    for values in it.product((False, True), repeat=len(variables)):
        a = dict(zip(variables, values))
        if satisfies(clauses, a):
            return a
    return None


def horn_backdoor_number(clauses):
    variables = sorted({abs(l) for c in clauses for l in c})
    for size in range(len(variables) + 1):
        for selected in it.combinations(variables, size):
            chosen = set(selected)
            if all(sum(l > 0 and abs(l) not in chosen for l in c) <= 1
                   for c in clauses):
                return size, selected
    raise AssertionError


def incidence_connected(clauses):
    # Bipartite incidence graph: ('c',j) and ('v',id).
    if not clauses:
        return True
    graph = {}
    for j, clause in enumerate(clauses):
        cn = ('c', j)
        graph.setdefault(cn, set())
        for l in clause:
            vn = ('v', abs(l))
            graph.setdefault(vn, set()).add(cn)
            graph[cn].add(vn)
    seen, stack = set(), [next(iter(graph))]
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        stack.extend(graph[u] - seen)
    return len(seen) == len(graph)


def audit_layout(h, q):
    R = 1 << h
    # A full-range affine permutation modulo 2^h.
    selector = [(3*z + 1) % R for z in range(R)]
    inverse = {block: z for z, block in enumerate(selector)}
    assert len(inverse) == R
    blocks = [None] * R
    nxt = h + 1
    for block in range(R):
        blocks[block], nxt = guarded_block(h, bits(inverse[block], h), q, nxt)

    residual_checks = beta_checks = direct_refutations = 0
    for z in range(R):
        fixed = {j+1: bool(v) for j, v in enumerate(bits(z, h))}
        bad = []
        for block, clauses in enumerate(blocks):
            Q = residual(clauses, fixed)
            witness = brute_sat(Q)
            residual_checks += 1
            if witness is None:
                bad.append(block)
                beta, chosen = horn_backdoor_number(Q)
                assert beta == q
                assert len(chosen) == q
                assert incidence_connected(Q)
                # The first two residual clauses are p and not-p.
                assert len(Q[0]) == len(Q[1]) == 1 and Q[0][0] == -Q[1][0]
                beta_checks += 1
                direct_refutations += 1
        assert bad == [selector[z]]

    # Delete one block: exactly its inverse row is SAT. All private bits may be 0.
    hole = R // 2
    sat_rows = []
    for z in range(R):
        fixed = {j+1: bool(v) for j, v in enumerate(bits(z, h))}
        if all(brute_sat(residual(c, fixed)) is not None
               for block, c in enumerate(blocks) if block != hole):
            sat_rows.append(z)
    assert sat_rows == [inverse[hole]]

    # Gray-row traversal changes the selected block at every step.
    gray = [z ^ (z >> 1) for z in range(R)]
    changes = sum(selector[a] != selector[b] for a, b in zip(gray, gray[1:]))
    assert changes == R - 1

    # Any row-independent candidate set covering all rows has size R.
    assert len(set(selector)) == R
    return {
        'h': h, 'q': q, 'rows': R, 'blocks': R,
        'residual_checks': residual_checks,
        'bad_residual_beta_checks': beta_checks,
        'constant_size_refutations': direct_refutations,
        'selector_range': len(set(selector)),
        'gray_order_selector_changes': changes,
        'one_hole_block': hole,
        'one_hole_sat_row': inverse[hole],
        'private_variables': nxt - (h + 1),
    }


def restricted_query_control(R, B):
    """Fixed cyclic query strategy versus its explicit last-candidate table."""
    table, queries = [], 0
    for z in range(R):
        order = [(z + j) % B for j in range(B)]
        table.append(order[-1])
        # B-1 negative replies identify the promised final unique block.
        queries += B - 1
    assert len(table) == R and queries == R*(B-1)
    return {'rows': R, 'blocks': B, 'queries': queries,
            'selector_table': table,
            'information_bits_exact_for_all_tables': R*(B.bit_length()-1)}


def t5_h9_control():
    words = ('BBB', 'FBB', 'FFF', 'BB')
    edges, nxt = [], 2
    for word in words:
        vertices = [0] + list(range(nxt, nxt + len(word)-1)) + [1]
        nxt += len(word)-1
        for a, b, direction in zip(vertices, vertices[1:], word):
            edges.append((a, b) if direction == 'F' else (b, a))

    def find(E):
        colors = {0: 0}
        order = sorted(range(1, nxt), key=lambda v: -sum(v in e for e in E))
        def rec(k):
            if k == len(order):
                return dict(colors)
            v = order[k]
            for c in range(5):
                colors[v] = c
                if all((colors[b]-colors[a]) % 5 in (1, 3)
                       for a, b in E if a in colors and b in colors):
                    ans = rec(k+1)
                    if ans is not None:
                        return ans
            colors.pop(v)
            return None
        return rec(0)

    assert nxt == 9 and len(edges) == 11 and find(edges) is None
    checks = 0
    for missing in range(len(edges)):
        E = edges[:missing] + edges[missing+1:]
        witness = find(E)
        assert witness is not None
        for shift in range(5):
            rotated = {v: (c+shift) % 5 for v, c in witness.items()}
            assert all((rotated[b]-rotated[a]) % 5 in (1, 3) for a, b in E)
            checks += len(E)
    # One-hot positive clauses are disjoint: four variables per vertex needed.
    return {'vertices': nxt, 'edges': len(edges), 'sat_deletions': len(edges),
            'rotation_arc_checks': checks, 'one_hot_strong_horn_beta': 4*nxt}


def run():
    layouts = [audit_layout(h, q) for h in (2, 3) for q in (1, 2, 3, 4)]
    result = {
        'layouts': layouts,
        'layout_count': len(layouts),
        'total_residual_checks': sum(x['residual_checks'] for x in layouts),
        'total_beta_checks': sum(x['bad_residual_beta_checks'] for x in layouts),
        'restricted_query_control': restricted_query_control(8, 16),
        't5_h9': t5_h9_control(),
    }
    result['code_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return result


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
