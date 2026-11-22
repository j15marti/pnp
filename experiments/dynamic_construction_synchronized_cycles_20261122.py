"""Generate and audit synchronized mixed cycles. Python 3, no dependencies."""
from itertools import product, combinations
import json


def generate(top, bottom):
    t = len(top)
    assert t >= 3 and len(bottom) == t and set(top + bottom) <= set("AC")
    factors = [tuple(range(3*i, 3*i+3)) for i in range(2*t)]
    checks = []
    for layer, word in enumerate((top, bottom)):
        for i, link in enumerate(word):
            a, b, _ = factors[layer*t+i]
            dest = factors[layer*t+(i+1) % t]
            checks.append((a, b, dest[2 if link == "C" else 0]))
    for i in range(t):
        h = 6*t + 2*i
        for layer in range(2):
            checks.append((factors[layer*t+i][2], h, h+1))
    clauses = []
    for scope, parity in [(row, False) for row in factors] + [(row, True) for row in checks]:
        for bits in product((0, 1), repeat=3):
            legal = sum(bits) % 2 == 0 if parity else sum(bits) == 1
            if not legal:
                clauses.append(tuple((-1 if bit else 1)*(v+1) for v, bit in zip(scope, bits)))
    return factors, checks, clauses


def rank(rows):
    basis = {}
    for mask in rows:
        while mask:
            pivot = mask.bit_length()-1
            if pivot not in basis:
                basis[pivot] = mask
                break
            mask ^= basis[pivot]
    return len(basis)


def transfer(top, bottom):
    options = {"A": {(0,0), (1,1), (1,0)}, "C": {(0,1), (1,0)}}
    reach = {(0,0), (1,1)}
    for a, b in zip(top, bottom):
        relation = options[a] & options[b]
        reach = {(x,z) for x,y in reach for u,z in relation if y == u}
    return any(x == y for x,y in reach)


def audit(t):
    totals = [0, 0]
    for pair in product(product("AC", repeat=t), repeat=2):
        top, bottom = map("".join, pair)
        factors, checks, clauses = generate(top, bottom)
        assert len(clauses) == 26*t
        masks = [sum(1 << x for x in row) for row in checks]
        k = rank(masks) - rank([m >> (6*t) for m in masks])
        assert k == 3*t
        group = {v:i for i, row in enumerate(factors) for v in row}
        group.update({v:2*t+v-6*t for v in range(6*t,8*t)})
        neighbors = [set() for _ in range(4*t)]
        for row in checks:
            for x,y in combinations({group[v] for v in row},2):
                neighbors[x].add(y)
                neighbors[y].add(x)
        assert min(map(len,neighbors)) == 3
        # Independent oracle on the emitted constraints. Enumerate every
        # one-hot choice, then try all four helper pairs on each local rung.
        sat = False
        for picks in product(range(3), repeat=2*t):
            ones = {row[j] for row,j in zip(factors,picks)}
            if any(sum(v in ones for v in row) % 2 for row in checks[:2*t]):
                continue
            for i in range(t):
                rung = checks[2*t+2*i:2*t+2*i+2]
                h = 6*t+2*i
                choices = [ones | {h+j for j,bit in enumerate(bits) if bit}
                           for bits in product((0,1), repeat=2)]
                witness = next((z for z in choices if all(sum(v in z for v in row)%2==0 for row in rung)),None)
                if witness is None:
                    break
                ones = witness
            else:
                assert all(any(((abs(l)-1) in ones) == (l>0) for l in clause) for clause in clauses)
                sat = True
                break
        assert sat == transfer(top,bottom)
        totals[int(sat)] += 1
    return {"t":t, "SAT":totals[1], "UNSAT":totals[0], "r":4*t, "s":3*t, "k":3*t}


if __name__ == "__main__":
    print(json.dumps([audit(t) for t in (3,4)], indent=2))
