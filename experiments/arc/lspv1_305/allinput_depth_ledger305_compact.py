#!/usr/bin/env python3
"""LSPV-1 ALLINPUT-DEPTH-LEDGER305, standalone exact F9/Y6 control.
Native indexed-TM time/space is NOT measured. Full independent verifier archived.
"""
import json
from collections import Counter
from itertools import product
P9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N9=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F9=P9+tuple(tuple(-v for v in c) for c in N9)
P6=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
N6=((1,2,4),(1,3,6),(2,3,5),(4,5,6))
Y6=P6+tuple(tuple(-v for v in c) for c in N6)

def grammar(F):
    if not F or any(len(c)!=3 or len({abs(l) for l in c})!=3 or
       not (all(l>0 for l in c) or all(l<0 for l in c)) for c in F):return False
    n=max(abs(v) for c in F for v in c)
    if n%3 or len(F)*3!=4*n or len(set(tuple(sorted(c)) for c in F))!=len(F):return False
    h=Counter((abs(l),l>0) for c in F for l in c)
    return all(h[v,True]==h[v,False]==2 for v in range(1,n+1))

def true(c,a):return any(abs(l) in a and a[abs(l)]==int(l>0) for l in c)

def models(F,p):
    n=max(abs(l) for c in F for l in c)
    free=[v for v in range(1,n+1) if v not in p]
    for vals in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,vals))}
        if all(true(c,a) for c in F):yield a

def solve(F,p):
    if not grammar(F):return {'label':'MALFORMED'}
    n=max(abs(l) for c in F for l in c)
    if any(v<1 or v>n or a not in (0,1) for v,a in p.items()):return {'label':'MALFORMED'}
    stats=Counter()
    def go(a,depth):
        stats['nodes']+=1;stats['max_or_depth']=max(stats['max_or_depth'],depth)
        while True:
            rows=[]
            for j,c in enumerate(F):
                stats['source_literal_reads']+=3
                if true(c,a):continue
                row=[l for l in c if abs(l) not in a]
                if not row:return False,None
                rows.append((j,row))
            if not rows:return True,a
            units=[r[0] for j,r in rows if len(r)==1]
            if not units:break
            x=units[0];v=abs(x);a={**a,v:int(x>0)};stats['units']+=1
        v=min(abs(l) for j,r in rows for l in r)
        stats['or_nodes']+=1
        for bit in (0,1):
            yes,witness=go({**a,v:bit},depth+1)
            if yes:return True,witness
        return False,None
    yes,a=go(dict(p),0)
    if yes:
        for v in range(1,n+1):a.setdefault(v,0)
        assert all(true(c,a) for c in F)
        stats['original_witness_clause_checks']+=len(F)
    f=n-len(p);b=stats['max_or_depth']
    assert stats['nodes'] <= max(1,(3*f-1)*2**b)
    return {'label':'SAT' if yes else 'UNSAT','model':[a[v] for v in range(1,n+1)] if yes else None,
            'stats':dict(stats),'node_envelope':(3*f-1)*2**b}

def main():
    assert all(grammar(F) for F in (F9,Y6))
    samples={'F9_root':(F9,{}),'F9_S':(F9,{1:0,2:0,8:1,9:1}),
       'F9_U':(F9,{3:0,6:1,7:1,9:1}),
       'F9_6pin_U':(F9,{8:0,3:0,7:0,6:0,1:1,5:1}),
       'Y6_root':(Y6,{}),'Y6_S':(Y6,{1:0})}
    out={}
    for name,(F,p) in samples.items():
        r=solve(F,p);k=sum(1 for _ in models(F,p))
        assert (r['label']=='SAT')==(k>0)
        out[name]={'exact_models':k,**r}
    malformed=[(),((1,1,2),),((1,2,3),(1,2,3)),((1,-2,3),),((1,2,3),)]
    assert all(solve(x,{})['label']=='MALFORMED' for x in malformed)
    print(json.dumps({'status':'PASS','source_label_controls':out,'malformed_rejections':len(malformed),
      'statement':'P vs NP OPEN; all-input polynomial OR-depth bound UNPROVED'},indent=2,sort_keys=True))
if __name__=='__main__':main()
