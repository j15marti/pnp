"""Source audit for exact-one articulation messages. Python 3, standard library."""
from itertools import combinations, product
import json
import random


def family(bits):
    q = len(bits)
    fresh = q + 1
    rows = []
    for i, switch in enumerate(bits):
        right = 3 if switch else 1
        names = {0: i, right: i + 1}
        for j in range(9):
            if j not in names:
                names[j] = fresh
                fresh += 1
        rows.extend((names[a], names[3+b], names[6+(a+b)%3])
                    for a in range(3) for b in range(3))
    for port in (0, q):
        rows.extend((port, fresh+j, fresh+(j+1)%3) for j in range(3))
        fresh += 3
    return rows


def components(rows, omit=None):
    graph = {}
    for row in rows:
        group = set(row) - {omit}
        for x in group:
            graph.setdefault(x, set()).update(group - {x})
    parts = []
    while graph:
        start = next(iter(graph))
        todo, part = [start], set()
        while todo:
            x = todo.pop()
            if x in graph:
                part.add(x)
                todo.extend(graph.pop(x))
        parts.append(part)
    return parts


def blocks(rows):
    for cut in [None] + sorted(set().union(*map(set, rows))):
        parts = components(rows, cut)
        if len(parts) > 1:
            return [block for part in parts for block in
                    blocks([r for r in rows if part.intersection(r)])]
    return [rows]


def models(rows):
    names = sorted(set().union(*map(set, rows)))
    for values in product((0, 1), repeat=len(names)):
        env = dict(zip(names, values))
        if all(sum(env[x] for x in row) == 1 for row in rows):
            yield env


def decide(rows):
    pieces = blocks(rows) if rows else []
    names = [set().union(*map(set, piece)) for piece in pieces]
    owners = {}
    for i, group in enumerate(names):
        for x in group:
            owners.setdefault(x, []).append(i)
    visited = set()

    def message(i, parent):
        visited.add(i)
        allowed = {}
        for x in names[i] - {parent}:
            mask = {0, 1}
            for j in owners[x]:
                if j != i:
                    assert j not in visited
                    mask &= message(j, x)
            allowed[x] = mask
        feasible = set()
        for env in models(pieces[i]):
            if all(env[x] in mask for x, mask in allowed.items()):
                feasible.add(env.get(parent, 1))
        return feasible

    answers = [bool(message(i, None)) for i in range(len(pieces)) if i not in visited]
    return all(answers)


def audit():
    rng = random.Random(324)
    generated = sat = 0
    for q in range(1, 7):
        for bits in product((0, 1), repeat=q):
            rows = family(bits)
            assert len(rows) == 9*q+6
            assert len(set().union(*map(set, rows))) == 8*q+7
            rng.shuffle(rows)
            verdict = decide(rows)
            assert verdict == (sum(bits) != 1)
            sat += verdict
            generated += 1
    latin = [(a, 3+b, 6+(a+b)%3) for a in range(3) for b in range(3)]
    fano = [tuple((i+j)%7 for j in (0,1,3)) for i in range(7)]
    for base, expected in [(latin, True), (fano, False)]:
        rows = [tuple(x+10*i for x in row) for i in range(4) for row in base]
        assert decide(rows) == expected
    triples = list(combinations(range(6), 3))
    tested = 0
    for rs in combinations(triples, 3):
        assert decide(list(rs)) == any(models(rs))
        tested += 1
    return dict(generated=generated, sat=sat, unsat=generated-sat,
                exhaustive_three_row_sources=tested, disjoint_controls=2, seed=324)

if __name__ == "__main__":
    print(json.dumps(audit(), indent=2))
