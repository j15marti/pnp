"""Audit one ternary parity check across synchronized columns. Run from experiments/."""
from collections import Counter
from itertools import combinations, product
import json
from dynamic_construction_synchronized_cycles_20261122 import generate, rank, transfer
from dynamic_discovery_mixed_to_binary_20261122 import reduce_source


def make_source(top, bottom, marks):
    if len(set(marks)) != 3 or not all(0 <= i < len(top) for i in marks):
        raise ValueError("choose three distinct columns")
    factors, checks, clauses = generate(top, bottom)
    extra = tuple(factors[i][2] for i in marks)
    checks.append(extra)
    for bits in product((0, 1), repeat=3):
        if sum(bits) % 2:
            clauses.append(tuple((-1 if bit else 1)*(v+1) for v, bit in zip(extra, bits)))
    return factors, checks, clauses


def decide(top, bottom, marks):
    transitions = {"A": {(0,0),(1,1),(1,0)}, "C": {(0,1),(1,0)}}
    states = {(z,z,0) for z in (0,1)}
    for i, (a,b) in enumerate(zip(top, bottom)):
        allowed = transitions[a] & transitions[b]
        states = {(start,nxt,parity ^ (cur if i in marks else 0))
                  for start,cur,parity in states for src,nxt in allowed if cur == src}
    return any(start == cur and parity == 0 for start,cur,parity in states)


def direct(factors, checks):
    # Enumerate factor choices. Each disjoint helper pair has one free XOR bit.
    port_count = 3*len(factors)
    for picks in product(range(3), repeat=len(factors)):
        ones = {row[j] for row,j in zip(factors,picks)}
        required = {}
        for row in checks:
            internal = tuple(v for v in row if v >= port_count)
            parity = sum(v in ones for v in row) % 2
            if internal:
                if required.setdefault(internal,parity) != parity:
                    break
            elif parity:
                break
        else:
            return True
    return False


def audit(t):
    counts = Counter()
    first_change = None
    for words in product("AC", repeat=2*t):
        top,bottom = "".join(words[:t]),"".join(words[t:])
        for marks in combinations(range(t),3):
            factors,checks,clauses = make_source(top,bottom,marks)
            assert not any(set(q)==set(f) for q in checks for f in factors)
            assert reduce_source(factors,checks) == "UNKNOWN"
            masks = [sum(1<<x for x in row) for row in checks]
            k = rank(masks) - rank([m >> (6*t) for m in masks])
            assert k == 3*t+1
            cover = set()
            for clause in clauses:
                scope = {abs(lit)-1 for lit in clause}
                if cover.isdisjoint(scope):
                    cover.update(scope)
            assert len(cover)==6*t and len(clauses)==26*t+4
            answer = decide(top,bottom,marks)
            if t == 3:
                assert answer == direct(factors,checks)
            counts["SAT" if answer else "UNSAT"] += 1
            if transfer(top,bottom) and not answer:
                counts["formerly_SAT"] += 1
                if first_change is None:
                    first_change = [top,bottom,marks]
    return dict(t=t, counts=dict(counts), first_lost_model_family=first_change,
                direct_oracle_checked=t==3)


if __name__ == "__main__":
    print(json.dumps([audit(t) for t in (3,4)], indent=2))
