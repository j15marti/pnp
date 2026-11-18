#!/usr/bin/env python3
"""CLOCKSUCCINCTGROUP42: independent compact QBF-to-S5 verifier."""
import itertools, random
from functools import lru_cache

IDENT=tuple(range(5))
PERMS=list(itertools.permutations(range(5)))
def mul(x,y): return tuple(y[x[i]] for i in range(5))
def product(seq):
    p=IDENT
    for x in seq:p=mul(p,x)
    return p
def inverse(x):
    p=[0]*5
    for i,j in enumerate(x):p[j]=i
    return tuple(p)
def cycle5(p):
    x=0; seen=set()
    for _ in range(5):seen.add(x);x=p[x]
    return x==0 and len(seen)==5
CYCLES=[p for p in PERMS if cycle5(p)]
A=B=C=None
for a in CYCLES:
    for b in CYCLES:
        c=product((a,b,inverse(a),inverse(b)))
        if cycle5(c):A,B,C=a,b,c;break
    if A is not None:break
@lru_cache(None)
def ab(target):
    for t in PERMS:
        if product((inverse(t),C,t))==target:
            return product((inverse(t),A,t)),product((inverse(t),B,t))
    raise AssertionError

def leaf(clauses,assignment):
    return all(any((assignment[abs(k)-1]==1) if k>0
                   else (assignment[abs(k)-1]==0) for k in cl) for cl in clauses)
def qbf(Q,clauses,level=0,assignment=()):
    if level==len(Q):return leaf(clauses,assignment)
    x=qbf(Q,clauses,level+1,assignment+(0,))
    y=qbf(Q,clauses,level+1,assignment+(1,))
    return (x and y) if Q[level]=='A' else (x or y)

@lru_cache(None)
def qlen(Q,level):
    if level==len(Q):return 1
    l=qlen(Q,level+1)
    return 4*l if Q[level]=='A' else 4*(l+1)+1
def ln(node,Q):
    if node[0]=='q':return qlen(Q,node[1])
    if node[0]=='c':return 1
    if node[0]=='not':return ln(node[1],Q)+1
    return 2*(ln(node[1],Q)+ln(node[2],Q))
def expand(node,Q,clauses):
    if node[0]!='q':return node
    _,j,assignment=node
    if j==len(Q):return ('c',leaf(clauses,assignment))
    x=('q',j+1,assignment+(0,));y=('q',j+1,assignment+(1,))
    if Q[j]=='A':return ('and',x,y)
    return ('not',('and',('not',x),('not',y)))
def instruction(node,target,index,Q,clauses):
    if not 0<=index<ln(node,Q):raise IndexError(index)
    if node[0]=='q':
        return instruction(expand(node,Q,clauses),target,index,Q,clauses)
    if node[0]=='c':return target if node[1] else IDENT
    if node[0]=='not':
        k=ln(node[1],Q)
        return instruction(node[1],inverse(target),index,Q,clauses) if index<k else target
    a,b=ab(target)
    for child,t in ((node[1],a),(node[2],b),(node[1],inverse(a)),(node[2],inverse(b))):
        k=ln(child,Q)
        if index<k:return instruction(child,t,index,Q,clauses)
        index-=k
    raise AssertionError

def main():
    rng=random.Random(20261118113243)
    checks=0;instances=0
    for q in range(6):
        for _ in range(12):
            Q=tuple(rng.choice('EA') for _ in range(q))
            clauses=tuple(tuple(rng.choice([-1,1])*rng.randint(1,q)
                                for _ in range(rng.randint(1,3)))
                          for _ in range(rng.randint(0,4))) if q else ((),)
            root=('q',0,());L=qlen(Q,0);N=1<<(L-1).bit_length()
            final=IDENT;state=0
            for i in range(N):
                p=instruction(root,C,i,Q,clauses) if i<L else IDENT
                final=mul(final,p);state=p[state]
                checks+=1
            want=qbf(Q,clauses)
            assert final==(C if want else IDENT)
            assert state==(C[0] if want else 0)
            assert N>=L and N<2*L
            checks+=3;instances+=1
    print({'instances':instances,'checks':checks,'failures':0,
           'independent':'different QBF sample seed; lazy indexed compiler'})
if __name__=='__main__':main()
