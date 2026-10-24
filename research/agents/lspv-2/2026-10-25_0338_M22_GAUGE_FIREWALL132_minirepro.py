#!/usr/bin/env python3
"""M22-GAUGE-FIREWALL132: exact target-preserving source complement group.
Standard-library deterministic/exhaustive finite audit; not a SAT lower bound.
"""
from collections import Counter, defaultdict
import hashlib, json
from pathlib import Path

Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
   (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))

def normalize(F):
    return tuple(tuple(sorted(c,key=lambda z:abs(z))) for c in F)

def validate(F):
    F=normalize(F)
    if len(F)!=len(set(F)) or not F: return False
    pos,neg=Counter(),Counter()
    for c in F:
        if len(c)!=3 or len({abs(x) for x in c})!=3: return False
        if not (all(x>0 for x in c) or all(x<0 for x in c)): return False
        for x in c: (pos if x>0 else neg)[abs(x)]+=1
    V=set(pos)|set(neg)
    return all(pos[v]==neg[v]==2 for v in V)

def defect(F):
    ss=set(normalize(F))
    return sum(1 for c in ss if all(x>0 for x in c) and tuple(-x for x in c) not in ss)

def components(F):
    adj=defaultdict(set)
    for c in F:
        v=[abs(x) for x in c]
        for a in v: adj[a].update(v)
    unseen=set(adj); out=[]
    while unseen:
        v=min(unseen); unseen.remove(v); todo=[v]; cc=[]
        while todo:
            a=todo.pop(); cc.append(a)
            for b in adj[a]&unseen: unseen.remove(b); todo.append(b)
        out.append(frozenset(cc))
    return sorted(out,key=lambda x:min(x))

def switch(F,S):
    return normalize(tuple(tuple(-x if abs(x) in S else x for x in c) for c in F))

def models(F,n):
    return sum(all(any(((mask>>(abs(x)-1))&1)==(x>0) for x in c) for c in F)
               for mask in range(1<<n))

def prism(h):
    assert h>=4
    edges=[(i,(i+1)%h) for i in range(h)]+[(h+i,h+(i+1)%h) for i in range(h)]+[(i,h+i) for i in range(h)]
    stars=[tuple(j+1 for j,e in enumerate(edges) if v in e) for v in range(2*h)]
    assert all(len(s)==3 for s in stars)
    F=tuple(stars)+tuple(tuple(-x for x in s) for s in stars)
    return normalize(F),stars

def unpair_prism(F,stars):
    a,b=stars[0],stars[2]; i,j=a[0],b[0]
    na=tuple(-j if x==i else -x for x in a)
    nb=tuple(-i if x==j else -x for x in b)
    q=list(F);q.remove(tuple(-x for x in a));q.remove(tuple(-x for x in b))
    q.extend((na,nb))
    return normalize(q)

def exhaustive_switch(F):
    vs=sorted({abs(x) for c in F for x in c})
    assert len(vs)<=20
    cc=components(F); valid=0; orbits=set()
    for mask in range(1<<len(vs)):
        S={v for i,v in enumerate(vs) if (mask>>i)&1}
        G=switch(F,S)
        if validate(G):
            valid+=1; orbits.add(frozenset(G))
            assert all(not(S&comp) or comp<=S for comp in cc)
            assert defect(G)==defect(F)
    assert valid==(1<<len(cc))
    nonpaired=sum(defect(tuple(c for c in F if abs(c[0]) in C))>0 for C in cc)
    assert len(orbits)==(1<<nonpaired)
    return {'variables':len(vs),'clauses':len(F),'components':len(cc),
            'gauges_tested':1<<len(vs),'legal_gauges':valid,
            'nonpaired_components':nonpaired,'distinct_orbit_members':len(orbits),
            'unpaired_supports_per_polarity':defect(F)}

def run():
    assert validate(Y) and models(Y,6)==20
    paired,stars=prism(4)
    nonpaired=unpair_prism(paired,stars)
    assert validate(paired) and validate(nonpaired)
    assert defect(paired)==0 and defect(nonpaired)==2
    q2_models=models(nonpaired,12)
    assert q2_models==406
    disconnected=normalize(tuple(Y)+tuple(tuple(x+6 if x>0 else x-6 for x in c) for c in paired))
    assert validate(disconnected) and defect(disconnected)==4
    cases={'Y':exhaustive_switch(Y),'prism_paired':exhaustive_switch(paired),
           'prism_nonpaired_q2':exhaustive_switch(nonpaired),
           'disconnected_Y_and_paired':exhaustive_switch(disconnected)}
    assert cases['disconnected_Y_and_paired']['legal_gauges']==4
    assert cases['disconnected_Y_and_paired']['distinct_orbit_members']==2
    assert not validate(switch(nonpaired,{1}))
    return {'claim':'M22-GAUGE-FIREWALL132',
            'status':'PROVED/EXACT restricted theorem, COMPUTATIONAL finite controls',
            'Y_models':20,'q2_models':q2_models,
            'cases':cases,'gauges_checked':sum(v['gauges_tested'] for v in cases.values()),
            'total_legal_gauges':sum(v['legal_gauges'] for v in cases.values()),
            'failures':0,'limits':'not FLMV bit counts or universal SAT time lower bounds'}

if __name__=='__main__':
    results=run()
    results['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    Path(__file__).with_name('2026-10-25_0338_M22_GAUGE_FIREWALL132_results.json').write_text(
        json.dumps(results,indent=2,sort_keys=True)+'\n')
    print(json.dumps(results,indent=2,sort_keys=True))
