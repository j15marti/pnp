#!/usr/bin/env python3
"""LSPV-4 CP22-GAUGE-FIREWALL98: compact standard-library reproducer.
Compiler matches j15marti/pnp experiments/review/cp22_audit.py Git blob
bb13859bc22b0219cb2ce90b679e4418a0b42c50.
A syntactic model-specific result, NOT an arbitrary-SAT lower bound.
"""
from collections import Counter, defaultdict, deque
from itertools import product
import json

W=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
   (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
   (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
   (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
Q=[c for c in W if c!=(1,7,13)]
def mixed(c):
    return any(v>0 for v in c) and any(v<0 for v in c)
def gaugeable(F):
    adj=defaultdict(list)
    for j,C in enumerate(F):
        for lit in C:
            x=('v',abs(lit)); c=('c',j); p=int(lit<0)
            adj[x].append((c,p)); adj[c].append((x,p))
    color={}
    for root in adj:
        if root in color: continue
        color[root]=0; queue=deque([root])
        while queue:
            x=queue.popleft()
            for y,p in adj[x]:
                v=color[x]^p
                if y in color:
                    if color[y]!=v: return False
                else: color[y]=v; queue.append(y)
    return True
def compiler(F):
    F=[tuple(c) for c in F]; m=len(F)
    assert m and sorted(set(abs(l) for C in F for l in C))==list(range(1,max(abs(l) for C in F for l in C)+1))
    n=max(abs(l) for C in F for l in C); s=n+1
    U=[]
    for j,(a,b,c) in enumerate(F):
        y=n+2+2*j; z=y+1
        U.extend([(s,a,y),(-y,b,c),(-s,-a,z),(-z,-b,-c)])
    B=U+U; occ=defaultdict(lambda:[[],[]])
    for j,C in enumerate(B):
        for i,l in enumerate(C): occ[abs(l)][0 if l>0 else 1].append((j,i))
    A=[[0]*3 for _ in B]; groups={}; R=0
    for x in sorted(occ):
        pos,neg=occ[x]; assert len(pos)==len(neg) and len(pos)>=2
        g=[]
        for a,b in zip(pos,neg):
            R+=1; g.append(R); A[a[0]][a[1]]=R; A[b[0]][b[1]]=-R
        groups[x]=g
    assert R==12*m
    edges=[(a,b) for g in groups.values() for a,b in zip(g,g[1:]+g[:1])]
    pad=[]
    for i,(a,b) in enumerate(edges): pad.append((-a,b,R+15*(i//3)+(1,7,13)[i%3]))
    gadget=[tuple((1 if l>0 else -1)*(R+15*j+abs(l)) for l in C)
            for j in range(R//3) for C in Q]
    T=list(map(tuple,A))+pad+gadget
    assert len(T)==96*m
    return T,R
def models(F,n):
    return sum(all(any(((mask>>(abs(l)-1))&1)==(l>0) for l in C) for C in F)
               for mask in range(1<<n))
def audit(F):
    T,R=compiler(F); m=len(F); count=Counter(l for C in T for l in C)
    assert len(count)==2*72*m
    assert all(count[x]==count[-x]==2 for x in range(1,72*m+1))
    assert all(len({abs(l) for l in C})==3 for C in T)
    assert len({frozenset(C) for C in T})==len(T)
    assert not gaugeable(T)
    assert all(mixed(C) for C in T[8*m:8*m+R])
    split=sum(map(mixed,T[:8*m])); gadget=sum(map(mixed,T[8*m+R:]))
    assert split>=4*m and gadget==68*m
    for j in range(R//3):
        off=R+15*j; start=8*m+R+j*19
        first,second=T[start],T[start+18]
        assert first==(-off-1,off+3,-off-14)
        assert second==(-off-1,off+13,off+14)
        assert (1^1^1^0)==1
    return T,dict(variables=72*m,clauses=96*m,independent_bad_cycles=R//3,
                  pre_gauge_mixed=split+R+gadget,mixed_split=split,
                  mixed_padding=R,mixed_Q=gadget,gaugeable=False)
Y=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),
   (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
U=[tuple(sign[i]*(i+1) for i in range(3)) for sign in product([1,-1],repeat=3)]
def main():
    assert len(Q)==19 and not gaugeable(Q)
    assert models(Y,6)==20 and models(U,3)==0
    rows=[]
    for name,F,label,target in [('Y',Y,'SAT',True),('cube',U,'UNSAT',False)]:
        one,r1=audit(F);two,r2=audit(one)
        rows.append(dict(source=name,label=label,source_in_Cstar=target,one=r1,two=r2))
    print(json.dumps(dict(run='CP22-GAUGE-FIREWALL98',cases=rows,errors=0,
          caveat='finite syntax checks; UNSAT transport relies on original compiler theorem'),indent=2))
if __name__=='__main__': main()
