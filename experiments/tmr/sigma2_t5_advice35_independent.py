#!/usr/bin/env python3
"""Independent source-first T5/selector audit, no third-party solvers."""
from itertools import product
from math import prod
paths = [([0,2,1],"++"),([0,3,4,1],"+++"),([0,5,6,1],"++-"),([0,7,8,1],"---")]
def trans(op, delete=False):
    return [[int(delete or (((b-a) if op=="+" else (a-b))%5 in (1,3))) for b in range(5)] for a in range(5)]
def mul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(5)) for j in range(5)] for i in range(5)]
def row(ops, deletion=-1):
    M=[[int(i==j) for j in range(5)] for i in range(5)]
    for i,op in enumerate(ops):M=mul(M,trans(op, i==deletion))
    return M[0]
rows=[row(p) for _,p in paths]
assert rows==[[0,1,1,0,2],[3,0,3,1,1],[1,3,0,3,1],[3,1,1,3,0]]
assert all(prod(r[d] for r in rows)==0 for d in range(5))
deletions=[]
for i,(_,p) in enumerate(paths):
    for j in range(len(p)):
        replacement=[row(q,j) if k==i else rows[k] for k,(_,q) in enumerate(paths)]
        deletions.append(5*sum(prod(replacement[k][d] for k in range(4)) for d in range(5)))
assert sorted(deletions)==sorted([180,180,60,60,60,60,60,60,40,40,40])
assert sum(deletions)==840 and all(x>0 for x in deletions)

# Four private blocks and three common bits: F UNSAT, each B_i globally SAT.
target=(1,0,1)
def blocks(z):
    # False means no private y_i can make unit y_i and guarded clause both true.
    return [z[j]==target[j] for j in range(3)]+[z!=target]
table={}
for z in product((0,1),repeat=3):
    feasible=blocks(z)
    table[''.join(map(str,z))]=[i for i,b in enumerate(feasible) if not b]
    assert not all(feasible),feasible
assert not any(all(i in table[k] for k in table) for i in range(4))
assert sum(all(blocks(z)[:3]) for z in product((0,1),repeat=3))==1

# Exact universal XOR gate trace: valid existential dependency only after universals.
assert all(any(t==z^y for t in (0,1)) for z,y in product((0,1),repeat=2))
assert not any(all(t==z^y for z,y in product((0,1),repeat=2)) for t in (0,1))
print({"t5_deleted_counts":deletions,"all_z_blockers":table,"failed_assertions":0})
