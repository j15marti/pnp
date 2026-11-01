#!/usr/bin/env python3
"""ARC-SATURATION296 compact source-authenticated two-label control.
Standalone Python 3 standard library. No SAT/UNSAT oracle in the gate.
"""
from collections import Counter
from itertools import product
import json
F=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),
(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15),
(-1,-2,-11),(-2,-3,-11),(-1,-3,-12),(-4,-5,-13),
(-5,-6,-14),(-4,-6,-15),(-7,-8,-12),(-8,-9,-13),
(-9,-10,-14),(-10,-7,-15))
PINS={'UNSAT':(0,0,0,0,1,1,1,1,0),'SAT':(1,0,0,0,1,1,1,1,0)}
CYCLES={'UNSAT':((1,2,12),(3,4,15)),'SAT':((11,2,12),(3,4,15))}
def is_sat(a):return all(any(a[abs(x)-1]==int(x>0) for x in c) for c in F)
def residual(p):
    live={};spill={i:[0,0] for i,v in enumerate(p,1) if v<0};work=Counter()
    for j,c in enumerate(F,1):
        work['source_clause_scans']+=1
        hit=False
        for x in c:
            work['source_literal_probes']+=1
            hit|=p[abs(x)-1]==int(x>0)
        if hit:
            for x in c:
                work['covered_occurrence_reads']+=1
                if p[abs(x)-1]<0:spill[abs(x)][int(x<0)]+=1
        else:live[j]=tuple(x for x in c if p[abs(x)-1]<0)
    return live,spill,work
def verify_cycles(live,cycles):
    used=set()
    for cy in cycles:
        deg=Counter();vertices={};assert len(cy)%2 and len(cy)>=3
        for j in cy:
            assert j not in used;used.add(j)
            c=live[j];assert len(c)==2
            u,v=map(abs,c);deg.update((u,v));vertices.setdefault(u,set()).add(v);vertices.setdefault(v,set()).add(u)
        assert len(deg)==len(cy) and all(d==2 for d in deg.values())
        seen={next(iter(deg))};queue=list(seen)
        while queue:
            for v in vertices[queue.pop()]:
                if v not in seen:seen.add(v);queue.append(v)
        assert len(seen)==len(deg)
    return used
def analyze(name):
    pins=PINS[name];p=(-1,)*6+pins
    live,s,work=residual(p);used=verify_cycles(live,CYCLES[name])
    e=2*p.count(-1)-len(live);eta=sum(min(v) for v in s.values())
    delta=e-eta-len(CYCLES[name]);w={i:abs(v[0]-v[1]) for i,v in s.items() if v[0]!=v[1]}
    forced={i:int(s[i][1]>s[i][0]) for i in w if w[i]>delta} if delta>=0 else {}
    completions=[]
    for bits in product((0,1),repeat=6):
        a=bits+pins
        if is_sat(a):completions.append(a)
    assert (delta<0) == (name=='UNSAT')
    assert (len(completions)>0)==(name=='SAT')
    assert all(all(a[i-1]==v for i,v in forced.items()) for a in completions)
    if delta==0:
        for a in completions:
            for j,c in live.items():
                count=sum(a[abs(x)-1]==int(x>0) for x in c)
                if len(c)==3 or (len(c)==2 and j not in used):assert count==1
    return {'label':name,'e':e,'eta':eta,'cycle_count':len(CYCLES[name]),
            'delta':delta,'forced':forced,'weighted_forbidden_cubes':
            [{ 'variable':i,'forbidden':1-v,'cost':w[i]} for i,v in forced.items()],
            'source_models':len(completions),'witnesses':completions,
            'outside_cycle_binary_ids':[j for j,c in live.items() if len(c)==2 and j not in used],
            'verified_cycle_clause_ids':CYCLES[name], 'work':dict(work)}
def main():
    occ=Counter(x for c in F for x in c)
    assert all(occ[i]==occ[-i]==2 for i in range(1,16))
    assert len(set(tuple(sorted(c)) for c in F))==20
    assert all(len(c)==3 and len(set(map(abs,c)))==3 and (all(x>0 for x in c) or all(x<0 for x in c)) for c in F)
    result={name:analyze(name) for name in PINS}
    assert result['SAT']['forced']=={1:0,2:0,4:1}
    assert result['SAT']['outside_cycle_binary_ids']==[13,14]
    assert result['SAT']['source_models']==2 and result['UNSAT']['source_models']==0
    ends={}
    for tag,a in [('zero',(0,)*15),('one',(1,)*15)]:
        counts=[sum(a[abs(x)-1]==int(x>0) for x in c) for c in F]
        ends[tag]=[counts.count(k) for k in range(4)]
    assert ends['zero']==ends['one']==[10,0,0,10]
    print(json.dumps({'status':'PASS','source':'valid canonical F15',
       'run':'ARC-SATURATION296','cases':result,'endpoints':ends,
       'scope':'exact restricted source-indexed gate, not hereditary ARC/FLMV'},sort_keys=True,indent=2))
if __name__=='__main__':main()
