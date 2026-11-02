#!/usr/bin/env python3
"""Recompute exact whole-resolution time/space optima, Python standard library.
Time = source loads + resolutions + erase_cost * erasures.
Space = sum(1 + literal_count) across live clauses, including a new conclusion
before either parent can be erased. This is NOT native machine bit-time/RAM.
"""
from collections import deque
from itertools import combinations
import json

F = tuple(map(frozenset, ((1,), (2,), (-1,-2,3), (-2,-3,4), (-1,-4,5), (-5,))))

def resolve(c, d):
    out = set()
    for x in c:
        if -x in d:
            r = (c - {x}) | (d - {-x})
            if not any(-y in r for y in r): out.add(frozenset(r))
    return out

clauses = set(F)
while True:
    new = {r for c,d in combinations(clauses,2) for r in resolve(c,d)} - clauses
    if not new: break
    clauses.update(new)
C = sorted(clauses, key=lambda c:(len(c),sorted(c)))
index = {c:i for i,c in enumerate(C)}
sources = [index[c] for c in F]
size = [1+len(c) for c in C]
rules = {(i,j):sorted(index[r] for r in resolve(C[i],C[j]))
         for i,j in combinations(range(len(C)),2)}

def optimum(cap, erase_cost):
    todo = deque([(0,0)])
    dist = {0:0}
    while todo:
        state,d = todo.popleft()
        if d != dist[state]: continue
        if state & 1: return d
        live = [i for i in range(len(C)) if state >> i & 1]
        used = sum(size[i] for i in live)
        moves = [(state ^ (1<<i),erase_cost) for i in live]
        moves += [(state | (1<<i),1) for i in sources
                  if not state >> i & 1 and used+size[i] <= cap]
        for i,j in combinations(live,2):
            moves += [(state | (1<<r),1) for r in rules[i,j]
                      if not state >> r & 1 and used+size[r] <= cap]
        for nxt,cost in moves:
            nd = d+cost
            if nd < dist.get(nxt,10**30):
                dist[nxt] = nd
                (todo.appendleft if cost==0 else todo.append)((nxt,nd))
    return None

def models(formula):
    return [a for a in range(32) if all(any(bool(a>>(abs(x)-1)&1)==(x>0)
                                                for x in c) for c in formula)]
assert not models(F)
assert all(models(F[:i]+F[i+1:]) for i in range(len(F)))
assert len(C)==33
rows = []
for erase_cost,expected in [(0,[None,15,13,11,11]),(1,[None,25,21,17,16])]:
    actual = [optimum(s,erase_cost) for s in range(8,13)]
    assert actual==expected, (erase_cost,actual)
    rows.append({'erase_cost':erase_cost,'capacity_tokens':list(range(8,13)),
                 'optimal_operations':actual})
print(json.dumps({'source_clauses':[sorted(c) for c in F],
                  'resolution_closure':len(C),'minimum_distinct_inferences':5,
                  'frontier':rows,'status':'EXACT finite fixed-calculus optima; P vs NP OPEN'},indent=2))
