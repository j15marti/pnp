"""Recover occurrence paths from strict-C bytes. Run from the repository root."""
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations, permutations, product
import json
from pathlib import Path
import random

import t5_construction_positive_offset1_20261121 as source

DEP = "6cd122e55ab7150dff6c8a1a22099ec5b44b195395c9f83670965773417accdb"
assert sha256(Path(source.__file__).read_bytes()).hexdigest() == DEP


def incidence(n, clauses):
    touches = [set() for _ in range(n)]
    for i, clause in enumerate(clauses):
        for x in clause:
            touches[x].add(i)
    return touches


def recover(bits):
    """Certify the link partition and path quotient, or raise ValueError (UNKNOWN)."""
    n, rows = source.decode(bits)
    clauses = [frozenset(row) for row in rows]
    touches = incidence(n, clauses)
    degree = [len(s) for s in touches]
    private = set()
    links = []
    used = set()
    for x in range(n):
        if degree[x] != 3:
            continue
        partners = {y for i in touches[x] for y in clauses[i] if y != x and degree[y] == 3}
        if len(partners) != 1:
            raise ValueError("degree-three partner")
        y, = partners
        if y < x:
            continue
        common = touches[x] & touches[y]
        sides = {z for i in common for z in clauses[i] if z not in (x, y)}
        if len(common) != 2 or len(sides) != 2:
            raise ValueError("side ports")
        a, b = sorted(sides)
        outer = touches[a] & touches[b]
        gadget_rows = touches[x] | touches[y] | outer
        if len(outer) != 2 or len(gadget_rows) != 6:
            raise ValueError("pin")
        ends = {z for i in outer for z in clauses[i] if z not in sides}
        four = {a, b, x, y}
        if len(ends) != 2 or ends & four or private & four or used & gadget_rows:
            raise ValueError("overlap")
        actual = Counter(clauses[i] for i in gadget_rows)
        orientation = []
        for u, v in permutations(sorted(ends)):
            for left, right in [(a, b), (b, a)]:
                cycle = (u, left, x, y, right)
                template = [frozenset(cycle[(i+j) % 5] for j in range(3)) for i in range(5)]
                template.append(frozenset((right, v, left)))
                if Counter(template) == actual:
                    orientation.append((u, v))
        if len(orientation) != 1 or any(touches[z] - gadget_rows for z in four):
            raise ValueError("template authentication")
        private.update(four)
        used.update(gadget_rows)
        links.append(orientation[0])
    copies = set(range(n)) - private
    core = [tuple(row) for i, row in enumerate(rows) if i not in used]
    if Counter(z for row in core for z in row) != Counter({z: 1 for z in copies}):
        raise ValueError("core occurrence")
    succ = dict(links)
    incoming = {v for u, v in links}
    if len(succ) != len(links) or len(incoming) != len(links) or not (set(succ) | incoming) <= copies:
        raise ValueError("path degrees")
    component = {}
    for start in sorted(copies - incoming):
        x = start
        while x not in component:
            component[x] = start
            if x not in succ:
                break
            x = succ[x]
        else:
            raise ValueError("path intersection")
    if set(component) != copies:
        raise ValueError("cycle")
    quotient = [tuple(component[x] for x in row) for row in core]
    if any(len(set(row)) != 3 for row in quotient):
        raise ValueError("repeated variable in quotient")
    histogram = Counter(Counter(component.values()).values())
    # The circuit uses only this fixed-radius mark, without traversing whole paths.
    neighbors = defaultdict(list)
    for u, v in links:
        neighbors[u].append(v)
        neighbors[v].append(u)
    marks = sum(len(adj) == 2 and all(len(neighbors[v]) == 1 for v in adj)
                for adj in neighbors.values())
    if marks != histogram[3]:
        raise AssertionError("local mark disagrees with authenticated quotient")
    return histogram, len(links), quotient


def wrapped(n, rows, seed):
    rng = random.Random(seed)
    names = list(range(n))
    rng.shuffle(names)
    renamed = []
    for row in rows:
        clause = [names[x] for x in row]
        rng.shuffle(clause)
        renamed.append(tuple(clause))
    rng.shuffle(renamed)
    return source.encode(n, renamed)


def positive(p, gates):
    gates = tuple(gates)
    n, cs = source.compile_circuit(*source.lift(p, gates, p+len(gates)-1))
    return cs, source.split(n, cs)


def joint_trials(p, seed):
    rows = []
    for tag, gates in [
        ("repeat", [("or", 0, 0)]), ("distinct", [("or", 0, 1)]),
        ("nor", [("or", 0, 1), ("not", p)]),
        ("implies", [("not", 0), ("or", p, 1)])]:
        cs, (n, split, e) = positive(p, gates)
        bits = wrapped(n, split, seed)
        hist, got_e, quotient = recover(bits)
        assert hist == Counter(Counter(x for row in cs for x in row).values())
        assert got_e == e and len(quotient) == len(cs)
        count = 10 * (1 << e) * ((1 << p) + source.source_count(p, gates, p+len(gates)-1))
        rows.append(dict(tag=tag, n=n, m=len(split), N=len(bits), E=e, paths=sorted(hist.items()),
                         three=hist[3], count=str(count), encoding_sha256=sha256(bits.encode()).hexdigest()))
    assert rows[0]["three"] == p+3 and rows[1]["three"] == p+2
    answers = [r["count"] for r in rows[:2]]
    matrix = [[int(z == answers[int(r["three"] == p+2)]) for z in answers] for r in rows[:2]]
    assert matrix == [[1, 0], [0, 1]]
    assert rows[2]["paths"] == rows[3]["paths"] and rows[2]["count"] != rows[3]["count"]
    return dict(p=p, seed=seed, sources=rows, joint=matrix)


def small_controls():
    # Independently enumerate every coloring of a single six-clause link.
    legal = {tuple(sorted((k, (k+1) % 5, (k+2) % 5))) for k in range(5)}
    gadget = [(0,1,2), (1,2,3), (2,3,4), (3,4,0), (4,0,1), (4,5,1)]
    fibers = [[0]*5 for _ in range(5)]
    for colors in product(range(5), repeat=6):
        if all(tuple(sorted(colors[x] for x in row)) in legal for row in gadget):
            fibers[colors[0]][colors[5]] += 1
    assert fibers == [[2*int(i==j) for j in range(5)] for i in range(5)]
    # Controls outside the OR family, also covering private leaves, disjoint and shared sources.
    tests = []
    for k, cs in [(3, [(0,1,2)]), (5, [(0,1,2),(2,3,4)]),
                  (6, [(0,1,2),(3,4,5)]), (4, list(combinations(range(4),3)))]:
        nn, split, e = source.split(k, cs)
        bits = wrapped(nn, split, 61)
        hist, got_e, recovered = recover(bits)
        assert hist == Counter(Counter(x for row in cs for x in row).values())
        labels = {x:i for i,x in enumerate(sorted({x for row in recovered for x in row}))}
        reindexed = [tuple(labels[x] for x in row) for row in recovered]
        direct = lambda rows: sum(all(tuple(sorted(a[x] for x in t)) in legal for t in rows)
                                  for a in product(range(5), repeat=k))
        z = direct(cs)
        assert got_e == e and direct(reindexed) == z
        tests.append(dict(n=k, source=cs, E=e, quotient_count=z, split_count_by_identity=z << e))
    # A valid strict C formula outside the recognize-and-contract architecture.
    star = [(0,1,2),(0,3,4),(0,5,6)]
    try:
        recover(source.encode(7, star))
    except ValueError as exc:
        rejection = str(exc)
    else:
        raise AssertionError("uncertified star accepted")
    # Under uniform name randomization, all images of one ordered triple occur equally.
    trans = Counter(tuple(perm[i] for i in (4,1,3)) for perm in permutations(range(5)))
    assert len(trans) == 60 and set(trans.values()) == {2}
    return dict(link_fibers=fibers, colors_checked=5**6, outside_or=tests,
                rejected_star=rejection, single_clause_frequencies_n5=[len(trans),2])


if __name__ == "__main__":
    print(json.dumps(dict(lemma="T5-WRAPPER-ORBIT-TEST1", generator_sha256=DEP,
                         controls=small_controls(),
                         trials=[joint_trials(p,s) for p in (2,3,6,10) for s in (11,23,59,97)]),
                     sort_keys=True, indent=2))
