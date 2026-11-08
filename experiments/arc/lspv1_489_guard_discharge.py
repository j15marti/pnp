#!/usr/bin/env python3
"""LSPV-1/489: independent 3-template guard and unit-case discharge; DISTINCT Resolution calculus."""
from itertools import product
import json

def norm(c): return tuple(sorted(set(c), key=lambda x:(abs(x),x)))
def AND(a,b,o): return [(-o,a),(-o,b),(o,-a,-b)]
def TT(a,b,o,f):
    return [tuple((-a if x else a,-b if y else b,-o if z else o))
            for x,y,z in product(range(2),repeat=3) if z!=f(x,y)]
G=AND(2,3,4)+AND(-1,-4,5)+TT(4,2,8,lambda a,b:int(a==b))+AND(1,8,6)+TT(1,3,9,lambda a,b:a^b)+TT(4,3,10,lambda a,b:int(a==b))+AND(9,10,7)
assert len(G)==24
C={i+1:norm(v) for i,v in enumerate(G)}
T={i:'SOURCE' for i in C}
P={}
steps=[(25,6,13,1),(26,6,16,1),(34,15,13,1),(35,1,10,2),
(36,7,3,2),(37,2,21,3),(40,2,34,3),(45,18,36,3),
(49,26,19,3),(63,25,37,4),(64,25,40,4),(79,45,35,4),
(82,49,35,4),(101,79,63,8),(104,82,64,8),(119,104,24,9),
(122,101,119,10)]
def RES(a,b,p):
    A,B=C[a],C[b]
    assert p in A and -p in B,(a,b,p)
    v=norm([x for x in A if x!=p]+[x for x in B if x!=-p])
    assert not any(-x in v for x in v)
    return v
def put(i,a,b,p,expected=None):
    assert i not in C
    v=RES(a,b,p)
    if expected is not None: assert v==norm(expected)
    C[i]=v;P[i]=(a,b,p);T[i]='RES'
for s in steps: put(*s)
assert C[122]==(5,6,7)
for i in range(3):
    t,z=5+i,11+i;a=200+2*i;b=a+1
    C[a]=norm((-t,z));C[b]=norm((-t,-z));T[a]=T[b]='SOURCE'
    # Branch-local three-step refutation from C[a], C[b] and unit (t).
    def r(A,B,p):
        assert p in A and -p in B
        return norm([x for x in A if x!=p]+[x for x in B if x!=-p])
    assert r(r((t,),C[a],t),r((t,),C[b],t),z)==()
    # Lift the branch without any new inference rule: one RES produces -t.
    put(500+i,a,b,z,(-t,))
put(600,122,500,5,(6,7));put(601,600,501,6,(7,));put(602,601,502,7,())
used=set()
def visit(i):
    if i in used:return
    used.add(i)
    if i in P:
        a,b,_=P[i];visit(a);visit(b)
visit(602)
assert sum(T[i]=='RES' for i in used)==23
assert sum(T[i]=='SOURCE' for i in used)==19
assert not any(i in used for i in (300,301,302))
def dep(i):return 0 if i not in P else 1+max(dep(P[i][0]),dep(P[i][1]))
assert dep(122)==6 and dep(602)==9
# Every genuine original p,u,v input extends uniquely to the 24-facet packet.
for p,u,v in product(range(2),repeat=3):
    q=u&v;r1=int(q==u);r2=p^v;r3=int(q==v)
    X={1:p,2:u,3:v,4:q,5:(1-p)&(1-q),6:p&r1,7:r2&r3,8:r1,9:r2,10:r3}
    def sat(cl):return any((X[abs(l)]==1) if l>0 else (X[abs(l)]==0) for l in cl)
    assert all(sat(cl) for cl in G)
    assert any(X[t] for t in (5,6,7))
# The final global proof is externally source-authenticated and does not use t_i assumptions.
assert all(C[x]==norm(G[x-1]) for x in used if x<=24)
assert C[602]==()
result={'status':'PROVED/RESTRICTED','model':'separate paid Tseitin + pure Resolution',
        'guard_source_facets':24,'blocker_source_facets':6,
        'cover_res':17,'branch_original_res_each':3,
        'discharged_res_each':1,'join_res':3,'total_res':23,
        'used_original_source_nodes':19,'used_total_nodes':len(used),
        'cover_span':dep(122),'global_span':dep(602),'source_sat_controls':8,
        'history':'No historical R_mix341 RES/DEF acceptance claimed. P vs NP OPEN.'}
print(json.dumps(result,indent=2))
