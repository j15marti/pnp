#!/usr/bin/env python3
"""Independent no-import spot check of GATE311. Does not import compact311."""
import itertools, json
POS=('156','238','135','469','247','789')
NEG=('468','167','234','358','129','579')
def build(k):
    out=[]
    for i in range(k):
        for j,s in enumerate(POS):
            out.append(tuple((i*9+int(a)) if (j!=0 or a!='5') else ((i+1)%k)*9+5 for a in s))
        for s in NEG:out.append(tuple(-i*9-int(a) for a in s))
    return out
def count(F,p):
    z=0;checked=0
    for a in range(1<<18):
        if any((a>>(v-1)&1)!=b for v,b in p.items()):continue
        checked+=1
        if all(any((a>>(abs(v)-1)&1)==int(v>0) for v in c) for c in F):z+=1
    return z,checked
def safe(bits,t):
    return all(bits>>(2*i)&3!=3 for i in range(t))
def verify():
    F=build(2)
    assert len(F)==24 and len(set(F))==24
    occurrence={i:[0,0] for i in range(1,19)}
    for c in F:
        assert len(c)==len(set(abs(v) for v in c))==3
        assert len(set(v>0 for v in c))==1
        for v in c:occurrence[abs(v)][int(v>0)]+=1
    assert all(k==[2,2] for k in occurrence.values())
    profiles={ 'AZ':{5:1},'AQ':{5:1,10:0,14:0,15:0},
               'BZ':{5:1,4:0,6:0},'BQ':{5:1,4:0,6:0,10:0,14:0,15:0} }
    models={label:count(F,p) for label,p in profiles.items()}
    assert {k:v[0] for k,v in models.items()}=={'AZ':2377,'AQ':299,'BZ':108,'BQ':0}
    assert models['BQ'][1]==4096
    checked=0
    for t in range(1,6):
        live=[s for s in range(4**t) if safe(s,t)]
        dead=[s for s in range(4**t) if not safe(s,t)]
        assert len(live)==3**t and len(dead)==4**t-3**t
        for i,a in enumerate(live):
            for b in live[i+1:]:
                checked+=1
                assert any(safe(a|(1<<bit),t)!=safe(b|(1<<bit),t)
                           for bit in range(2*t))
        for s in dead:assert all(not safe(s|(1<<bit),t) for bit in range(2*t))
    print(json.dumps({'status':'PASS','assertion_pairs_one_step':checked,
        'same_original_G2_exact_models':{k:v[0] for k,v in models.items()},
        'monotone_state_classes':[3**t+1 for t in range(1,7)],
        'P_versus_NP':'OPEN'},sort_keys=True))
if __name__=='__main__':verify()
