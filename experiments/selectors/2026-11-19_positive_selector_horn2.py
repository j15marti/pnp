"""Restricted Horn selector audit. Standard library; seed 2026111902.

Functional reference, not a measured RAM implementation. Brute-force oracles
are test-only. The report proves the streamed memory/time bounds separately.
"""
import itertools as it
import json
import random
import hashlib
from collections import deque
from pathlib import Path


def normal(F):
    out = []
    for clause in F:
        C = set(clause)
        if any(-x in C for x in C):
            continue
        out.append(tuple(sorted(C)))
    return tuple(out)


def restrict(F, a):
    return tuple(tuple(x for x in C if abs(x) not in a)
                 for C in F if not any(abs(x) in a and a[abs(x)] == (x > 0) for x in C))


def satisfied(F, a):
    return all(any(a[abs(x)] == (x > 0) for x in C) for C in F)


def brute(F, n):
    for bits in it.product((False, True), repeat=n):
        a = dict(enumerate(bits, 1))
        if satisfied(F, a):
            return a
    return None


def pair(F, D):
    for C in F:
        p = [x for x in C if x > 0 and x not in D]
        if len(p) > 1:
            return p[:2]
    return None


def discover(F, budget, D=(), path=()):
    p = pair(F, D)
    if p is None:
        return D, path
    if budget == 0:
        return None
    for bit, x in enumerate(p):
        ans = discover(F, budget - 1, D + (x,), path + (bit,))
        if ans is not None:
            return ans
    return None


def replay(F, bits):
    D = ()
    for bit in bits:
        p = pair(F, D)
        if p is None:
            break
        D += (p[bit],)
    return D if pair(F, D) is None else None


def horn(F):
    """Linear incidence-queue least-model algorithm on normalized Horn CNF."""
    remaining, heads, occurrences = [], [], {}
    for j, C in enumerate(F):
        pos = [x for x in C if x > 0]
        assert len(pos) <= 1
        heads.append(pos[0] if pos else None)
        neg = [-x for x in C if x < 0]
        remaining.append(len(neg))
        for x in neg:
            occurrences.setdefault(x, []).append(j)
    q = deque(j for j, count in enumerate(remaining) if count == 0)
    true = set()
    while q:
        j = q.popleft()
        x = heads[j]
        if x is None:
            return None
        if x in true:
            continue
        true.add(x)
        for clause in occurrences.get(x, ()):
            remaining[clause] -= 1
            if remaining[clause] == 0:
                q.append(clause)
    return {abs(x): abs(x) in true for C in F for x in C}


def solve(F, budget):
    F = normal(F)
    found = discover(F, budget)
    if found is None:
        return 'UNKNOWN', None, None
    D, path = found
    assert replay(F, path) == D
    for values in it.product((False, True), repeat=len(D)):
        a = dict(zip(D, values))
        b = horn(restrict(F, a))
        if b is not None:
            a.update(b)
            for C in F:
                for x in C:
                    a.setdefault(abs(x), False)
            assert satisfied(F, a)
            return 'SAT', a, path
    return 'UNSAT', None, path


def row_residual(block, z):
    return tuple(private for guards, private in block
                 if not any(z[abs(x)-1] == (x > 0) for x in guards))


def select(blocks, h, budget):
    rows = tuple(it.product((False, True), repeat=h))
    no = [None] * len(rows)
    eligible = [True] * len(rows)
    calls = marks = 0
    for i, block in enumerate(blocks):
        support = sorted({abs(x)-1 for guards, _ in block for x in guards})
        free = [j for j in range(h) if j not in support]
        for a in it.product((False, True), repeat=len(support)):
            z = [False] * h
            for j, value in zip(support, a):
                z[j] = value
            label, _, _ = solve(row_residual(block, z), budget)
            calls += 1
            for ext in it.product((False, True), repeat=len(free)):
                for j, value in zip(free, ext):
                    z[j] = value
                r = sum(int(x) << (h-1-j) for j, x in enumerate(z))
                marks += 1
                if label != 'SAT':
                    eligible[r] = False
                if label == 'UNSAT' and no[r] is None:
                    no[r] = i
    if all(i is not None for i in no):
        return 'UNSAT', no, calls, marks
    for r, good in enumerate(eligible):
        if good:
            witnesses = []  # Test collector only; production output is streamed.
            for block in blocks:
                label, witness, _ = solve(row_residual(block, rows[r]), budget)
                assert label == 'SAT'
                witnesses.append(witness)
            return 'SAT', (rows[r], witnesses), calls, marks
    return 'UNKNOWN', None, calls, marks


def t5_control():
    paths, edges, nxt = [], [], 2
    for word in ('BBB', 'FBB', 'FFF', 'BB'):
        vertices = [0] + list(range(nxt, nxt + len(word)-1)) + [1]
        nxt += len(word)-1
        path = []
        for a, b, direction in zip(vertices, vertices[1:], word):
            edge = (a, b) if direction == 'F' else (b, a)
            edges.append(edge)
            path.append(edge)
        paths.append(path)
    def witness(E):
        colors = {0: 0}
        order = sorted(range(1, nxt), key=lambda v: -sum(v in e for e in E))
        def rec(j):
            if j == len(order):
                return dict(colors)
            v = order[j]
            for c in range(5):
                colors[v] = c
                if all((colors[b]-colors[a]) % 5 in (1, 3)
                       for a, b in E if a in colors and b in colors):
                    answer = rec(j+1)
                    if answer is not None:
                        return answer
            colors.pop(v)
            return None
        return rec(0)
    assert nxt == 9 and len(edges) == 11 and witness(edges) is None
    checks = 0
    for j in range(len(edges)):
        E = edges[:j] + edges[j+1:]
        a = witness(E)
        assert a is not None
        for shift in range(5):
            rotated = {v: (c+shift) % 5 for v, c in a.items()}
            assert all((rotated[b]-rotated[a]) % 5 in (1, 3) for a, b in E)
            checks += len(E)
    # One-hot encoding: each vertex's positive five-clause alone requires
    # four variables in every syntactic strong Horn backdoor.
    positive = tuple(tuple(5*v+c+1 for c in range(5)) for v in range(nxt))
    assert discover(positive, 2) is None
    return {'vertices': nxt, 'edges': len(edges), 'sat_deletions': 11,
            'rotation_arc_checks': checks, 'one_hot_horn_backdoor_lower_bound': 4*nxt}


def run():
    clauses = [tuple((j+1)*v for j, v in enumerate(values) if v)
               for values in it.product((-1, 0, 1), repeat=3)]
    stats = {'formulas': 0, 'budget_checks': 0, 'path_checks': 0,
             'layouts': 0, 'SAT': 0, 'UNSAT': 0, 'UNKNOWN': 0,
             'residual_calls': 0, 'row_visits': 0}
    for count in range(4):
        for F in it.combinations(clauses, count):
            stats['formulas'] += 1
            exact = brute(F, 3)
            for budget in range(3):
                label, witness, _ = solve(F, budget)
                minimum_exists = any(pair(F, D) is None for size in range(budget+1)
                                     for D in it.combinations((1, 2, 3), size))
                assert (label != 'UNKNOWN') == minimum_exists
                if label != 'UNKNOWN':
                    assert (label == 'SAT') == (exact is not None)
                if witness is not None:
                    assert satisfied(F, witness)
                for bits in it.product((0, 1), repeat=budget):
                    D = replay(F, bits)
                    if D is not None:
                        assert pair(F, D) is None
                    stats['path_checks'] += 1
                stats['budget_checks'] += 1
    rng = random.Random(2026111902)
    for trial in range(360):
        blocks = []
        for _ in range(3):
            block = []
            for _ in range(rng.randrange(1, 8)):
                guards = tuple((j+1)*rng.choice((-1, 1)) for j in range(2)
                               if rng.random() < .4)
                private = rng.choice(clauses)
                block.append((guards, private))
            blocks.append(block)
        budget = trial % 3
        label, output, calls, marks = select(blocks, 2, budget)
        true_rows = [z for z in it.product((False, True), repeat=2)
                     if all(brute(row_residual(b, z), 3) is not None for b in blocks)]
        row_classes = []
        for z in it.product((False, True), repeat=2):
            classifications = []
            for block in blocks:
                F = row_residual(block, z)
                tractable = any(pair(F, D) is None for size in range(budget+1)
                                for D in it.combinations((1, 2, 3), size))
                classifications.append(('SAT' if brute(F, 3) is not None else 'UNSAT')
                                       if tractable else 'UNKNOWN')
            row_classes.append(classifications)
        expected = ('UNSAT' if all('UNSAT' in row for row in row_classes) else
                    'SAT' if any(all(x == 'SAT' for x in row) for row in row_classes)
                    else 'UNKNOWN')
        assert label == expected
        if label != 'UNKNOWN':
            assert (label == 'SAT') == bool(true_rows)
        if label == 'UNSAT':
            for z, i in zip(it.product((False, True), repeat=2), output):
                assert brute(row_residual(blocks[i], z), 3) is None
        if label == 'SAT':
            z, assignments = output
            assert all(satisfied(row_residual(b, z), a) for b, a in zip(blocks, assignments))
        stats['layouts'] += 1
        stats[label] += 1
        stats['residual_calls'] += calls
        stats['row_visits'] += marks
    # Reject both invalid extrapolations: exhausted class search is not UNSAT;
    # a single UNSAT backdoor branch is not a global refutation.
    assert solve(((1, 2),), 0)[0] == 'UNKNOWN'
    F = ((1, 2), (-1, -2))
    assert horn(restrict(F, {1: False, 2: False})) is None
    assert brute(F, 2) is not None
    # Varying row selector with Horn terminals, plus an unrecognized SAT block.
    blocks = [[((1,), (1,)), ((1,), (-1,))],
              [((-1,), (1,)), ((-1,), (-1,))],
              [((), (1, 2, 3))]]
    assert select(blocks, 1, 0)[0:2] == ('UNSAT', [0, 1])
    stats['t5'] = t5_control()
    stats['seed'] = 2026111902
    stats['code_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    return stats


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
