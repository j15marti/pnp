#!/usr/bin/env python3
"""Source-to-Tseitin 2CNF non-invariance, verified canonical F9, stdlib only.
Run: python source_tseitin_residual325.py
All source literals retain original variable IDs; gate literals have IDs 10..44.
The circuit is a declared private 35-gate OR/AND evaluator, NOT optimal.
"""
import itertools
import json
from collections import Counter
F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
   (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
N=9

def valid(c):
    q=Counter()
    if len(c)!=12 or len(set(tuple(sorted(a)) for a in c))!=12:return False
    for a in c:
        if len(a)!=3 or len(set(abs(z) for z in a))!=3 or any(abs(z)<1 or abs(z)>9 for z in a):return False
        if not (all(z>0 for z in a) or all(z<0 for z in a)):return False
        for z in a:q[(abs(z),z>0)]+=1
    return all(q[(i,p)]==2 for i in range(1,10) for p in (False,True))

def lit(z,a):
    t=a.get(abs(z))
    return None if t is None else (t if z>0 else not t)

def up(clauses,pins):
    a=dict(pins);probes=0;scans=0
    while True:
        again=False
        for clause in clauses:
            scans+=1;un=[];sat=False
            for z in clause:
                probes+=1;t=lit(z,a)
                if t is True:sat=True;break
                if t is None:un.append(z)
            if sat:continue
            if not un:return {'conflict':True,'scans':scans,'probes':probes,'residual':[],'assign':a}
            if len(un)==1:
                a[abs(un[0])]=un[0]>0
                again=True
                break
        if not again:break
    rem=[tuple(z for z in c if lit(z,a) is None) for c in clauses
         if not any(lit(z,a) is True for z in c)]
    return {'conflict':False,'scans':scans,'probes':probes,'residual':rem,'assign':a}

def circuit():
    gs=[];d={j:0 for j in range(1,10)}
    def gate(op,a,b):
        z=10+len(gs);gs.append((z,op,a,b))
        d[z]=1+max(d[abs(a)],d[abs(b)])
        return z
    cur=[]
    for c in F:cur.append(gate('OR',gate('OR',c[0],c[1]),c[2]))
    while len(cur)>1:
        cur=[gate('AND',cur[j],cur[j+1]) if j+1<len(cur) else cur[j]
             for j in range(0,len(cur),2)]
    C=[]
    for z,op,a,b in gs:
        if op=='OR':C.extend([(-a,z),(-b,z),(a,b,-z)])
        else:C.extend([(a,-z),(b,-z),(-a,-b,z)])
    C.append((cur[0],))
    assert len(gs)==35 and d[cur[0]]==6 and len(C)==106
    return gs,C,cur[0]

def truth(mask):
    return all(any(bool(mask&(1<<(abs(z)-1)))==(z>0) for z in c) for c in F)

def gate_truth(mask,gs,root):
    a={i:bool(mask&(1<<(i-1))) for i in range(1,10)}
    for z,op,p,q in gs:
        x=lit(p,a);y=lit(q,a)
        a[z]=(x or y) if op=='OR' else (x and y)
    return a[root]

def correct(pins,models):
    return sum(all(bool(mask&(1<<(j-1)))==v for j,v in pins.items()) for mask in models)

def run():
    assert valid(F)
    gs,C,root=circuit()
    assert gs[16]==(26,'OR',-2,-3)
    models=[]
    for mask in range(512):
        assert truth(mask)==gate_truth(mask,gs,root)
        if truth(mask):models.append(mask)
    assert len(models)==70
    stalls=[];no=0
    for trits in itertools.product((None,False,True),repeat=9):
        pins={j+1:v for j,v in enumerate(trits) if v is not None}
        if correct(pins,models):continue
        no+=1;r=up(F,pins)
        if r['conflict']:continue
        t=up(C,pins)
        assert not t['conflict']
        assert all(len(c)<=2 for c in r['residual'])
        stalls.append({'pins':{str(k):int(v) for k,v in pins.items()},
            'source_widths':dict(Counter(map(len,r['residual']))),
            'circuit_widths':dict(Counter(map(len,t['residual'])))})
    assert no==9175 and len(stalls)==3
    assert sum(int(v['circuit_widths'].get(3,0)>0) for v in stalls)==1
    p={1:True,4:False,5:True,8:False}
    s=up(F,p);t=up(C,p)
    assert not s['conflict'] and not t['conflict']
    assert len(s['residual'])==7 and all(len(c)==2 for c in s['residual'])
    assert Counter(map(len,t['residual']))=={2:23,3:1}
    assert (-2,-3,-26) in t['residual']
    sat={1:False,3:False,5:True,6:False,7:False,8:False}
    unsat=dict(sat,**{1:True}) if False else {**sat,1:True}
    assert [correct(k,models) for k in (sat,unsat)]==[2,0]
    bad=[F[:-1],F[:1]+F[:1]+F[2:],F[:1]+((1,1,6),)+F[2:],
         F[:1]+((1,-5,6),)+F[2:],F[:1]+((1,5,10),)+F[2:],
         F[:1]+((1,5,7),)+F[2:]]
    assert all(not valid(x) for x in bad)
    result={'proof_status':'EXACT private-compilation counterexample; computational exhaustive F9; P vs NP OPEN',
        'source_n':9,'source_m':12,'models':70,'truth_checks':512,'ternary_source_contexts':19683,
        'unsat_cubes':9175,'source_UP_stalled_unsat_cubes':3,
        'circuit_ternary_stall_cubes':1,'gates':35,'depth':6,'tseitin_clauses':106,
        'example_pins':{str(k):int(v) for k,v in p.items()},
        'source_binary_remaining':len(s['residual']),
        'circuit_binary_remaining':23,'circuit_ternary_remaining':1,
        'dead_gate_clause':[-2,-3,-26],'source_UP_probes':s['probes'],'source_UP_scans':s['scans'],
        'circuit_UP_probes':t['probes'],'circuit_UP_scans':t['scans'],
        'same_original_sat_unsat_completions':[2,0],
        'malformed_rejected':len(bad),'stall_cases':stalls}
    return result

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
