#!/usr/bin/env python3
"""Minimal independent check for LSPV-2 LAZY-INTERFACE-ACCESS269.
The complete 16-case proof-carrying producer and independent verifier are
in the downloadable reproducibility archive."""
from itertools import product

def sat(F,a):
    return all(any(a[abs(l)]==(l>0) for l in c) for c in F)

def projection(F,n,B,m):
    a={x:bool(m>>i&1) for i,x in enumerate(B)}
    free=[x for x in range(1,n+1) if x not in B]
    return any(sat(F,{**a,**dict(zip(free,bits))})
               for bits in product((False,True),repeat=len(free)))

def clause_line(mask,b):
    return ' '.join(str(-(i+1) if mask>>i&1 else i+1)
                    for i in range(b))+' 0\n'

class IndexedChild:
    def __init__(self,F,n,B):
        self.F,self.n,self.B=F,n,B
        self.profile_reads=0
    def good(self,m):
        self.profile_reads+=1
        return projection(self.F,self.n,self.B,m)
    def count_bad(self):
        return sum(not self.good(m) for m in range(1<<len(self.B)))
    def symbol(self,j):
        if j<0:return ' '
        b=len(self.B)
        header=f'p cnf {b} {self.count_bad()}\n'
        if j<len(header):return header[j]
        j-=len(header)
        for m in range(1<<b):
            if not self.good(m):
                row=clause_line(m,b)
                if j<len(row):return row[j]
                j-=len(row)
        return ' '

cases=[
('2SAT-SAT',2,[[1,2],[-1,2]],[1]),
('2SAT-UNSAT',2,[[1],[-1]],[1]),
('3CNF-SAT',3,[[1,2,3],[-1,-2,-3]],[1,2]),
('3CNF-UNSAT',3,[[1,2,3],[-1,-2,-3],[1],[-1]],[1,2]),
('B0-SAT',2,[[1],[-1,2]],[]),
('B0-UNSAT',1,[[1],[-1]],[])
]
checks=0
for name,n,F,B in cases:
    feasible=[projection(F,n,B,m) for m in range(1<<len(B))]
    bad=[m for m,v in enumerate(feasible) if not v]
    child=f'p cnf {len(B)} {len(bad)}\n'+''.join(clause_line(m,len(B)) for m in bad)
    oracle=IndexedChild(F,n,B)
    for j in range(-1,len(child)+2):
        expected=child[j] if 0<=j<len(child) else ' '
        assert oracle.symbol(j)==expected
        checks+=1
    rows=[[int(x) for x in clause_line(m,len(B)).split()[:-1]] for m in bad]
    for m,val in enumerate(feasible):
        y={i+1:bool(m>>i&1) for i in range(len(B))}
        assert sat(rows,y)==val
        checks+=1
    assert any(feasible)==any(sat(F,dict(zip(range(1,n+1),bits)))
                               for bits in product((False,True),repeat=n))
    print(name,'SAT' if any(feasible) else 'UNSAT',
          'child_bytes',len(child),'profile_reads',oracle.profile_reads)
print('PASS',checks,'exhaustive assertions')