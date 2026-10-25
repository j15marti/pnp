#!/usr/bin/env python3
"""M22-PIN-ERASURE147: independent standard-library reproducer.
Exhausts the 729 partial assignments for canonical Y and paired H.
Option --u PATH validates all 396 one-pin restrictions of the original
signed 198-variable/264-clause source represented as a Python list.
Finite controls, not physical FLMV random-access machine measurements.
"""
import ast, itertools, json, sys
from collections import Counter, defaultdict
P=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
Q=[(1,2,4),(1,3,6),(2,3,5),(4,5,6)]
Y=P+[tuple(-x for x in c) for c in Q]
H=P+[tuple(-x for x in c) for c in P]
def target(f):
    if any(len(c)!=3 or len(set(map(abs,c)))!=3 or not (all(x>0 for x in c) or all(x<0 for x in c)) for c in f):
        return (False,False)
    cs={tuple(sorted(c)) for c in f}
    if len(cs)!=len(f):return (False,False)
    d=defaultdict(lambda:[0,0])
    for c in f:
        for x in c:d[abs(x)][x>0]+=1
    if any(z!=[2,2] for z in d.values()):return (False,False)
    paired=all(tuple(sorted(-x for x in c)) in cs for c in f)
    return (True,not paired)
def restrict(f,a):
    return [tuple(x for x in c if abs(x) not in a)
            for c in f if not any((x>0)==a[abs(x)] for x in c if abs(x) in a)]
def true(f,a):return all(any((x>0)==a[abs(x)] for x in c) for c in f)
def classification(f):
    if not f:return 'TRUE'
    if any(not c for c in f):return 'FALSE_CLAUSE'
    t=target(f)
    return 'C_STAR' if t==(True,True) else 'PAIRED_CM' if t==(True,False) else 'OUTSIDE_CM'
def exhaustive(f):
    state=Counter();best=7;count=0;example=None
    for pat in itertools.product((None,False,True),repeat=6):
        pins={i+1:v for i,v in enumerate(pat) if v is not None}
        g=restrict(f,pins);state[classification(g)]+=1
        assert all(true(f,{i+1:bool((bits>>i)&1) for i in range(6)})==
                   true(g,{i+1:bool((bits>>i)&1) for i in range(6)})
                   for bits in range(64) if all(bool((bits>>(i-1))&1)==v for i,v in pins.items()))
        if pins and g:assert not target(g)[0]
        if not g and len(pins)<best:best=len(pins);count=1;example=pins
        elif not g and len(pins)==best:count+=1
    return {'states':dict(state),'min_true_erasure_pins':best,
            'number_minimum_covers':count,'example':example,'cases':729}
def main():
    assert target(Y)==(True,True) and target(H)==(True,False)
    assert sum(true(Y,{i+1:bool((bits>>i)&1) for i in range(6)}) for bits in range(64))==20
    out={'Y':exhaustive(Y),'H':exhaustive(H),'status':'COMPUTATIONAL checks of symbolic restricted theorem'}
    h=[tuple((1 if x>0 else -1)*(abs(x)+6) for x in c) for c in H]
    start=Y+h
    middle=restrict(start,{7:False,8:True})
    final=restrict(start,{7:False,8:True,11:True,12:False})
    assert target(start)==(True,True) and target(middle)==(False,False)
    assert sorted(map(sorted,final))==sorted(map(sorted,Y)) and target(final)==(True,True)
    out['two_level']={'root':list(target(start)),'level1':list(target(middle)),
                      'level2':list(target(final))}
    if '--u' in sys.argv:
        s=open(sys.argv[sys.argv.index('--u')+1]).read()
        s='\n'.join(s.splitlines()[1:]) if s.startswith('#') else s
        u=[tuple(c) for c in ast.literal_eval(s)]
        assert len(u)==264 and target(u)==(True,True)
        assert max(abs(x) for c in u for x in c)==198
        n=0
        for i in range(1,199):
            for v in (False,True):
                g=restrict(u,{i:v});assert g and not target(g)[0];n+=1
        out['U']={'original_clauses':264,'single_pin_checks':n}
    print(json.dumps(out,sort_keys=True,indent=2))
if __name__=='__main__':main()
