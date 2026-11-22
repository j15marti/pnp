"""Finite deletion-certificate audit. Exhaustive order search is only a test oracle."""
from itertools import combinations, permutations, product
import json

def circular(rows):
    if not rows:
        return True
    for x in set().union(*rows):
        bits = [x in r for r in rows]
        if sum(bits[i] and not bits[i-1] for i in range(len(bits))) > 1:
            return False
    return True

def order(rows, B):
    # Fix one row to break rotational symmetry. No polynomial claim for this oracle.
    for tail in permutations(range(1,len(rows))):
        p = (0,)+tail
        if circular([rows[i]-B for i in p]):
            return p
    return None

def arc_decide(rows):
    if not rows:
        return True
    if any(not r for r in rows):
        return False
    assert circular(rows)
    m = len(rows)
    arcs = []
    for x in set().union(*rows):
        cells = {i for i,r in enumerate(rows) if x in r}
        if len(cells) == m:
            return True
        start = next(i for i in cells if (i-1)%m not in cells)
        arcs.append((start,len(cells)))
    for start,size in arcs:
        if (-start)%m >= size:
            continue
        origin = (start+size)%m
        gap = m-size
        reach = {0}
        for p in range(gap):
            if p in reach:
                for a,b in arcs:
                    if (a-origin)%m == p and p+b <= gap:
                        reach.add(p+b)
        if gap in reach:
            return True
    return False

def residual(rows, B, true):
    forced_zero = set()
    remaining = []
    for r in rows:
        count = len(r & true)
        if count > 1:
            return None
        if count == 1:
            forced_zero.update(r-B)
        else:
            remaining.append(r-B)
    return [r-forced_zero for r in remaining]

def audit():
    checked = branches = sat = 0
    triples = [frozenset(r) for r in combinations(range(5),3)]
    for rs in combinations(triples,4):
        truth = any(all(len(r & set(t)) == 1 for r in rs)
                    for j in range(6) for t in combinations(range(5),j))
        for b in range(3):
            for bt in combinations(range(5),b):
                B=set(bt)
                p=order(rs,B)
                if p is None:
                    continue
                rows=[rs[i] for i in p]
                answer=False
                for values in product((0,1),repeat=b):
                    true={v for v,a in zip(bt,values) if a}
                    rem=residual(rows,B,true)
                    if rem is not None:
                        assert circular(rem)
                        answer |= arc_decide(rem)
                    branches += 1
                assert answer == truth
                checked += 1
                sat += answer
    return dict(status='PASS',certificates=checked,branches=branches,
                sat_certificates=sat,unsat_certificates=checked-sat,
                source_families=210,seed=None,
                scope='finite deletion, propagation, and arc decision; factorial order oracle, no native tape')

if __name__ == '__main__':
    print(json.dumps(audit(),indent=2))
