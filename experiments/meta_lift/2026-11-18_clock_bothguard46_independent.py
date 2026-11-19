#!/usr/bin/env python3
"""Independent stdlib finite controls for CLOCKBOTHGUARD46.
No native RAM/TM cost assertions; abstract verifier clock/space only.
"""
from itertools import product
import json

checks = 0

def ck(p, why):
    global checks
    checks += 1
    if not p: raise AssertionError(why)

def sat(clauses, vars_):
    return any(all(any((a[abs(l)-1] == (l > 0)) for l in c) for c in clauses)
               for a in product((False, True), repeat=vars_))

def rem(clauses, shared_z):
    out = []
    for c in clauses:
        if any(abs(l) == 1 and ((l > 0) == bool(shared_z)) for l in c): continue
        out.append(tuple(l for l in c if abs(l) != 1))
    return out

def verify(clauses, mode, record, time_limit=10000, space_limit=10000):
    """An explicit independent guard. Every path returns SAT/UNSAT/UNKNOWN.
    Abstract cost = number of literal and proof tests, not physical machine time.
    """
    time,peak = 0,0
    def meter(t,s):
        nonlocal time,peak
        time += t
        peak = max(peak,s)
        return time <= time_limit and peak <= space_limit
    if mode == 'SAT':
        if len(record) != 3 or any(b not in (False,True) for b in record): return 'UNKNOWN'
        if not meter(3,3): return 'UNKNOWN'
        for c in clauses:
            if not meter(len(c)+1,3+3*len(c)): return 'UNKNOWN'
            if not any(record[abs(l)-1] == (l>0) for l in c): return 'UNKNOWN'
        return 'SAT'
    if mode == 'UNSAT':
        if len(record) != 2: return 'UNKNOWN'
        for z in range(2):
            r = record[z]
            if not isinstance(r,dict) or r.get('z') != z or r.get('block') not in (0,1): return 'UNKNOWN'
            b = r['block']
            source_block = clauses[:2] if b==0 else clauses[2:]
            if not meter(2+sum(len(c)+1 for c in source_block),10): return 'UNKNOWN'
            residue = rem(source_block,z)
            proof = r.get('proof')
            if not isinstance(proof,list) or len(proof)!=3: return 'UNKNOWN'
            unit = 2 if b==0 else 3
            expected = [(unit,),(-unit,),()]
            for j,c in enumerate(proof):
                if not meter(1+len(c),12+3*len(c)): return 'UNKNOWN'
                if tuple(c)!=expected[j]: return 'UNKNOWN'
            if tuple(residue)!=tuple(expected[:2]): return 'UNKNOWN'
        return 'UNSAT'
    return 'UNKNOWN'

A = [(1,),(-1,),(2,),(-2,),(1,2),(1,-2)]
B = [(1,),(-1,),(3,),(-3,),(-1,3),(-1,-3)]
stats = {'sat':0,'unsat':0}
for mask_a in range(64):
    a = [v for j,v in enumerate(A) if mask_a>>j&1]
    for mask_b in range(64):
        b = [v for j,v in enumerate(B) if mask_b>>j&1]
        original = sat(a+b,3)
        projected = any(sat(rem(a,z),3) and sat(rem(b,z),3) for z in (0,1))
        ck(original==projected,'source-disjoint row theorem')
        stats['sat' if original else 'unsat'] += 1
ck(stats=={'sat':623,'unsat':3473},'match full audit')
unsat_source = [(1,2),(1,-2),(-1,3),(-1,-3)]
record=[{'z':0,'block':0,'proof':[(2,),(-2,),()]},
        {'z':1,'block':1,'proof':[(3,),(-3,),()]}]
ck(verify(unsat_source,'UNSAT',record)=='UNSAT','complete original row cover')
ck(verify(unsat_source,'UNSAT',record,time_limit=1)=='UNKNOWN','UNSAT time guard')
ck(verify(unsat_source,'UNSAT',record,space_limit=1)=='UNKNOWN','UNSAT space guard')
ck(verify(unsat_source,'UNSAT',record[:1])=='UNKNOWN','missing z rejected')
modified=[dict(x) for x in record];modified[1]['proof']=[(3,),(3,),()]
ck(verify(unsat_source,'UNSAT',modified)=='UNKNOWN','wrong proof rejected')
sat_source=[(1,2),(-1,3)]
ck(verify(sat_source,'SAT',(False,True,False))=='SAT','real witness')
ck(verify(sat_source,'SAT',(False,True,False),time_limit=1)=='UNKNOWN','SAT time guard')
ck(verify(sat_source,'SAT',(False,True,False),space_limit=1)=='UNKNOWN','SAT space guard')
ck(verify(unsat_source,'SAT',(False,True,False))=='UNKNOWN','no false SAT')
ck(verify(sat_source,'UNSAT',record)=='UNKNOWN','no false UNSAT')

def rel(a,b): return (b-a)%5 in (1,3)

edges = [(a,b) for a in range(3) for b in range(3) if a!=b]
tstats={'sat':0,'unsat':0}
for bits in range(64):
    arcs = [e for j,e in enumerate(edges) if bits>>j&1]
    exists = any(all(rel(cols[u],cols[v]) for u,v in arcs) for cols in product(range(5),repeat=3))
    tstats['sat' if exists else 'unsat']+=1
ck(tstats=={'sat':27,'unsat':37},'T5 three-vertex control')

def cycle(alt):
    steps=[(1,3) if not alt or i%2==0 else (2,4) for i in range(8)]
    return sum(all((colors[(i+1)%8]-colors[i])%5 in steps[i] for i in range(8))
               for colors in product(range(5),repeat=8))

ck(cycle(False)==180,'directed eight-cycle')
ck(cycle(True)==350,'alternating eight-cycle')
# Five independent three-edge paths, common terminals; endpoint counts multiply.
M=[[sum(rel(x,a) and rel(a,b) and rel(b,y) for a,b in product(range(5),repeat=2))
    for y in range(5)] for x in range(5)]
ck(sum(M[x][y]**5 for x,y in product(range(5),repeat=2))==2440,'five three-edge paths')
print(json.dumps({'revision':'CLOCKBOTHGUARD46.independent.v1','checks':checks,
                  'failures':0,'cnf_sources':4096,'cnf_results':stats,
                  't5_sources':64,'t5_results':tstats,
                  'time_space_guards':'both polarities yield UNKNOWN on breach',
                  'scope':'abstract proxy clocks and storage; not native RAM/TM'},sort_keys=True,indent=2))
