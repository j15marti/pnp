"""Positive one-in-three SAT to one synchronized cycle with short monotone runs."""
from itertools import product
from collections import Counter
import json
from dynamic_discovery_syndrome_trellis_20261122 import solve

def encode(v, clauses):
    # Each run ends with CC, AC, CC to pin its end at 0 and next start at 1.
    lengths = [2]*v + [3]*len(clauses)
    top, bottom, starts = [], [], []
    for length in lengths:
        starts.append(len(top))
        top.extend("A"*length + "CAC")
        bottom.extend("A"*length + "CCC")
    rows = []
    for start, clause in zip(starts[v:], clauses):
        for offset, var in enumerate(clause):
            rows.append((starts[var]+1, start+offset, start+offset+1))
    return "".join(top), "".join(bottom), rows

def main():
    counts = Counter()
    for v in (1,2,3):
        triples = list(product(range(v), repeat=3))
        for m in (1,2):
            for clauses in product(triples, repeat=m):
                top,bottom,rows = encode(v,clauses)
                assert len(top)==5*v+6*m and len(rows)==3*m
                assert all(len(set(row))==3 for row in rows)
                expected = any(all(sum(bits[i] for i in row)==1 for row in clauses)
                               for bits in product((0,1),repeat=v))
                actual=solve(top,bottom,rows)[0]
                assert actual==expected, (v,clauses)
                counts["SAT" if actual else "UNSAT"] += 1
    print(json.dumps(dict(counts=dict(counts), cases=sum(counts.values()),
                          projected=True, seed=None),indent=2))
if __name__=="__main__":
    main()
