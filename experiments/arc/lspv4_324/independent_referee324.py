#!/usr/bin/env python3
"""Independent pure-Python combinatorial referee for LSPV-4 backdoor audit 324.
No dependency on JS producer. Exhaustive subset covers and full source assignments.
Run: python independent_referee324.py
"""
from itertools import combinations, product

F9 = [(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
      (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9)]
Y6 = [(1,2,3),(1,4,5),(2,4,6),(3,5,6),
      (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
P15 = [(1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),
       (6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15)]
N15 = [(1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),
       (4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15)]
F15 = P15 + [tuple(-x for x in c) for c in N15]


def sat(clauses, values):
    return all(any(values[abs(l)] == (l > 0) for l in c) for c in clauses)


def exact_cover(clauses, n):
    for k in range(n+1):
        covers = [B for B in combinations(range(1,n+1),k)
                  if all(set(map(abs,c)).intersection(B) for c in clauses)]
        if covers:
            return k,len(covers),covers[0]
    raise AssertionError("No cover")


def total_models(clauses, n):
    return sum(sat(clauses,{i+1:bits[i] for i in range(n)})
               for bits in product((False,True),repeat=n))


expected = {"F9": (4,15,70), "Y6": (2,1,20), "F15": (6,3,1032)}
for name, F, n in [("F9",F9,9),("Y6",Y6,6),("F15",F15,15)]:
    size,num,example=exact_cover(F,n)
    models=total_models(F,n)
    assert (size,num,models)==expected[name], (name,size,num,models)
    print(name,{"minimum_backdoor":size,"number_of_minimum_covers":num,
                "example":example,"complete_original_models":models})

common={3:False,5:True,6:False,7:False,8:False}
for x1 in (False,True):
    pins={**common,1:x1}
    free=[i for i in range(1,10) if i not in pins]
    count=sum(sat(F9,{**pins,**dict(zip(free,bits))})
              for bits in product((False,True),repeat=len(free)))
    assert count==(0 if x1 else 2)
    print("same-original",{"x1":int(x1),"completions":count})

pairs=set()
for clause in F9:
    pairs.update(combinations(sorted(map(abs,clause)),2))
missing=set(combinations(range(1,10),2))-pairs
assert len(missing)==8
assert not any(all(pair in missing for pair in combinations(t,2))
               for t in combinations(range(1,10),3))
print("missing_cooccurrence_pairs",sorted(missing))
print("INDEPENDENT_REFEREE_PASS")
