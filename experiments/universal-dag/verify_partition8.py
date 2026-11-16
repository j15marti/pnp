#!/usr/bin/env python3
"""Independent literal semantics, exhaustive partition count, and weighted DAG check.

Usage: python3 verify_partition8.py N PARTITIONS.bin DAG OUTPUT_PREFIX [SECOND.bin]
Python 3.10+, no dependencies. Does not enumerate C choose 8 formula inputs.
"""
import csv
import hashlib
import json
import math
import sys
from collections import Counter
from functools import lru_cache
from itertools import combinations
from pathlib import Path

n = int(sys.argv[1])
raw_path, dag_path, out = map(Path, sys.argv[2:5])
assert 3 <= n <= 6
clauses = [(vs, s) for vs in combinations(range(n), 3) for s in range(8)]
C = len(clauses)
full = (1 << (1 << n)) - 1
sat = []
for vs, s in clauses:
    truth = 0
    for a in range(1 << n):
        if any(((a >> v) & 1) != ((s >> j) & 1) for j, v in enumerate(vs)):
            truth |= 1 << a
    sat.append(truth)
falsified = [full ^ x for x in sat]
incident = [[q for q in range(C) if falsified[q] >> a & 1] for a in range(1 << n)]

def read_rows(path):
    data = path.read_bytes()
    assert len(data) % 8 == 0
    rows = [tuple(data[i:i+8]) for i in range(0, len(data), 8)]
    assert len(set(rows)) == len(rows)
    assert all(tuple(sorted(set(r))) == r and max(r) < C for r in rows)
    return rows

rows = read_rows(raw_path)
if len(sys.argv) > 5:
    assert set(rows) == set(read_rows(Path(sys.argv[5])))
active = Counter()
profiles = Counter()
rowbits = []
by_clause = [[] for _ in range(C)]
for index, row in enumerate(rows):
    truth = full
    pos, neg = [0]*n, [0]*n
    for q in row:
        truth &= sat[q]
        vs, pattern = clauses[q]
        for j, v in enumerate(vs):
            (neg if pattern >> j & 1 else pos)[v] += 1
        by_clause[q].append(index)
    assert truth == 0
    d = [a+b for a,b in zip(pos,neg)]
    I = sum(abs(a-b) for a,b in zip(pos,neg))
    Vn = n*sum(a*a for a in d)-24**2
    profiles[I,Vn] += 1
    active[sum(x>0 for x in d)] += 1
    rowbits.append(sum(1<<q for q in row))

# A separate memoized recurrence checks completeness, not merely validity.
@lru_cache(None)
def count_partitions(uncovered):
    if not uncovered:
        return 1
    a = (uncovered & -uncovered).bit_length()-1
    return sum(count_partitions(uncovered ^ falsified[q])
               for q in incident[a]
               if falsified[q] & uncovered == falsified[q])
count = count_partitions(full)
assert count == len(rows)

with dag_path.open() as f:
    nn, m, cc, root, N = map(int, next(f).split())
    assert (nn,m,cc) == (n,8,C)
    order = list(map(int,next(f).split()))
    assert sorted(order) == list(range(C))
    rank = {q:i for i,q in enumerate(order)}
    nodes = [(None,0,0),(None,1,1)]
    for line in f:
        i,q,lo,hi = map(int,line.split())
        assert i == len(nodes) and 0 <= q < C and 0 <= lo < i and 0 <= hi < i
        assert all(child < 2 or rank[nodes[child][0]] > rank[q] for child in (lo,hi))
        nodes.append((q,lo,hi))
    assert len(nodes) == N and 0 <= root < N
for b in rowbits:
    id = root
    while id >= 2:
        q,lo,hi = nodes[id]
        id = hi if b >> q & 1 else lo
    assert id == 1

def level(id):
    return C if id < 2 else rank[nodes[id][0]]
@lru_cache(None)
def ways(id,k):
    remaining = C-level(id)
    if k < 0 or k > remaining:
        return 0
    if id < 2:
        return int(id == 1 and k == 0)
    q,lo,hi = nodes[id]
    result = 0
    for bit,child in ((0,lo),(1,hi)):
        gap = level(child)-rank[q]-1
        for j in range(min(gap,k-bit)+1):
            result += math.comb(gap,j)*ways(child,k-bit-j)
    return result
accepted = sum(math.comb(level(root),j)*ways(root,8-j)
               for j in range(min(8,level(root))+1))
assert accepted == count  # Together with all true positives: zero false positives.
seen=set()
def walk(id):
    if id<2 or id in seen:
        return
    seen.add(id)
    _,lo,hi=nodes[id]
    walk(lo);walk(hi)
walk(root)

# Every omitted pair has two promised inputs with opposite answers.
with Path(str(out)+"_pair_witnesses.csv").open('w') as f:
    writer=csv.writer(f)
    writer.writerow(['edge_a','edge_b','unsat_row_index','satisfying_assignment_after_swap'])
    for a,b in combinations(range(C),2):
        index=next(i for i in by_clause[a] if not (rowbits[i]>>b&1))
        changed=(rowbits[index]^(1<<a))|(1<<b)
        assert changed.bit_count()==8
        truth=full
        for q in rows[index]:
            if q!=a:
                truth &= sat[q]
        truth &= sat[b]
        assert truth
        assignment=(truth&-truth).bit_length()-1
        writer.writerow([a,b,index,assignment])

result=dict(n=n,m=8,clauses=C,raw_formulas=math.comb(C,8),unsat=count,
            sat=math.comb(C,8)-count,unsat_fraction=count/math.comb(C,8),
            active_variables=dict(sorted(active.items())),
            unsat_profiles=[dict(I=i,V_times_n=v,count=c) for (i,v),c in sorted(profiles.items())],
            independent_count_states=count_partitions.cache_info().currsize,
            weighted_count_states=ways.cache_info().currsize,
            dag_nodes=len(seen),dag_accepted_weight8=accepted,verified_true_positives=count,
            pair_witnesses=math.comb(C,2),query_node_lower_bound=C-1,
            circuit_gate_lower_bound=C-2,circuit_gate_upper_bound=(1<<n)*math.comb(n,3),
            all_unsat_sign_balanced=all(i==0 for i,v in profiles),
            regular_unsat_count=sum(c for (i,v),c in profiles.items() if v==0),
            binary_sha256=hashlib.sha256(raw_path.read_bytes()).hexdigest(),
            dag_sha256=hashlib.sha256(dag_path.read_bytes()).hexdigest(),
            verification='PASS: independent completeness count + all positives + weighted DAG count',
            global_minimum_proved=False)
Path(str(out)+"_verification.json").write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
