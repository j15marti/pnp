#!/usr/bin/env python3
"""LSPV-3/418 native DEF polarity gauge semantics, exhaustive source controls."""
from itertools import product
import json, random
rng=random.Random(418)
checks=0
def verify(cond,msg):
    global checks
    checks+=1
    if not cond:raise AssertionError(msg)
def bitgate(tt,a,b):return (tt>>(2*a+b))&1
def evaluate(original,gates):
    state=dict(original)
    for out,u,v,tt in gates:
        if out in state or u not in state or v not in state or tt<0 or tt>15:
            raise ValueError('invalid gate record')
        state[out]=bitgate(tt,state[u],state[v])
    return state
def complement_table(tt,cu,cv,co):
    res=0
    for a in (0,1):
        for b in (0,1):
            res|=(bitgate(tt,a^cu,b^cv)^co)<<(2*a+b)
    return res
def transform(gates,flip):
    out=[]
    for z,u,v,tt in gates:
        verify(flip[z] in (0,1),'non-Boolean gauge bit')
        out.append((z,u,v,complement_table(tt,flip.get(u,0),flip.get(v,0),flip[z])))
    return out
def clause_val(c,a):return any(a[w]==sign for w,sign in c)
def flip_clause(c,g):return [(w,s^g.get(w,0)) for w,s in c]
def row_val(r,a):
    support,b=r
    return sum(a[x] for x in support)%2==b
def flip_row(r,g):
    support,b=r
    return (support,b^(sum(g.get(x,0) for x in support)%2))
orig=['x0','x1','x2','x3']
for k in range(80):
    gates=[];available=list(orig)
    for i in range(6):
        u=rng.choice(available);v=rng.choice(available)
        tt=rng.randrange(16) if i%3 else [0,3,6,9,12,15][rng.randrange(6)]
        gates.append((f'z{i}',u,v,tt));available.append(f'z{i}')
    for bits in product((0,1),repeat=6):
        flip={f'z{i}':bits[i] for i in range(6)}
        other=transform(gates,flip)
        for src in product((0,1),repeat=4):
            seed=dict(zip(orig,src));p=evaluate(seed,gates);q=evaluate(seed,other)
            for w in available:verify(p[w]^flip.get(w,0)==q[w],'output gauge mismatch')
            for c in [[(available[4],1),(available[-1],0)],
                      [(available[0],0),(available[-2],1),(available[-1],1)]]:
                verify(clause_val(c,p)==clause_val(flip_clause(c,flip),q),'clause sign mismatch')
            for support in (['x0','z0','z3'],['z1','z3','z5'],['x3','x2'],['z4'],[]):
                for b in (0,1):
                    r=(support,b)
                    verify(row_val(r,p)==row_val(flip_row(r,flip),q),'affine RHS mismatch')
positive=[[('x0',1),('x1',1)],[('x0',0),('x2',1)]]
negative=positive+[[('x0',1)],[('x0',0)]]
for clauses,expect in ((positive,8),(negative,0)):
    num=sum(all(clause_val(c,dict(zip(orig,b))) for c in clauses)
            for b in product((0,1),repeat=4))
    verify(num==expect,'source SAT/UNSAT label mismatch')
bad=[
 [('z0','x0','x1',16)],
 [('z0','x0','x1',6),('z0','x0','x2',8)],
 [('z0','z1','x1',6),('z1','x0','x2',8)],
 [('z0','x0','unknown',6)]
]
for gates in bad:
    try:evaluate(dict.fromkeys(orig,0),gates)
    except ValueError:verify(True,'malformed rejected')
    else:verify(False,'malformed accepted')
base=[('z0','x0','x1',6),('z1','z0','x2',8),('z2','z0','z1',6)]
flip={'z0':1,'z1':1,'z2':0}
src=dict(zip(orig,(1,1,1,0)))
p=evaluate(src,base);q=evaluate(src,transform(base,flip))
r=(['z0','z2','x0'],0)
verify(row_val(r,p)==row_val(flip_row(r,flip),q),'corrected GF2 row failed')
verify(row_val(r,p)!=row_val(r,q),'forgotten GF2 RHS was accepted')
print(json.dumps({'run':'LSPV-3/418','seed':418,'networks':80,'gates':6,
 'gauges_per_network':64,'assignments_per_gauge':16,
 'checks':checks,'SAT_source_models':8,'UNSAT_source_models':0,
 'malformed':4,'GF2_uncorrected_RHS':'rejected'},indent=2))
