#!/usr/bin/env python3
"""Independent implementation audit; no import of the producer or SCC code.
This is a second checker by the same author, NOT an independent peer review.
"""
import itertools
import json
import hashlib
import sys
from pathlib import Path

WIN=((0,1,0,1,0),(0,0,1,0,1),(1,0,0,1,0),(0,1,0,0,1),(1,0,1,0,0))
tests=0
def models(n,clauses,pins,mode):
    global tests
    pins={int(v):c for v,c in pins.items()}; choices=[(pins[v],) if v in pins else range(5) for v in range(n)]
    count=0
    for a in itertools.product(*choices):
        good=True
        for h,u,v in clauses:
            tests+=1
            x,y=WIN[a[h]][a[u]],WIN[a[h]][a[v]]
            if not ((x+y==1) if mode=='Q' else (x+y==2)):
                good=False; break
        count+=good
    return count

def check_witness(clauses,pins,w):
    assert w is not None
    assert all(w[int(v)]==c for v,c in pins.items())
    assert all(WIN[w[h]][w[u]]+WIN[w[h]][w[v]]==1 for h,u,v in clauses)

path=Path(sys.argv[1] if len(sys.argv)>1 else 'q_restricted_selector_results.json')
d=json.loads(path.read_text()); cases=0
for x in d['controls']+d['targeted_random']:
    for mode in ('Q','P'):
        assert models(x['n'],x['clauses'],x['pins'],mode)==x[mode+'_oracle']['count']
    assert (x['solver']['status']=='SAT')==(x['Q_oracle']['count']>0)
    if x['solver']['status']=='SAT': check_witness(x['clauses'],x['pins'],x['solver']['witness'])
    cases+=1
for x in d['wrapper']:
    assert models(7,x['global_clauses'],{},'Q')==x['oracle']['count']
    if x['witness']: check_witness(x['global_clauses'],{},x['witness'])
    for c in x['all_child_calls']:
        count=models(4,x['blocks'][c['block']],{0:c['row']},'Q')
        assert (c['status']=='SAT')==(count>0)
        if c['status']=='SAT': check_witness(x['blocks'][c['block']],{0:c['row']},c['witness'])
for x in d['signature_classification']:
    H=x['head_colors']; S={tuple(WIN[h][a] for h in H) for a in range(5)}
    assert S=={tuple(t) for t in x['signatures']}
    bad=x['majority_obstruction']
    if bad:
        a,b,c,t=map(tuple,bad)
        assert a in S and b in S and c in S and t not in S
        assert t==tuple(int(x+y+z>=2) for x,y,z in zip(a,b,c))
    else:
        assert len(H)<=2
x=d['many_pinned_heads']; check_witness(x['clauses'],x['pins'],x['solver']['witness'])
assert d['K6_budget_control']['solver']['status']=='UNKNOWN'
assert [x['Q_oracle']['count'] for x in d['controls'] if x['name'].startswith('five_core_delete')]==[10,40,10,30,25]
print(json.dumps({'status':'PASS','paired_instances':cases,'wrapper_instances':len(d['wrapper']),
 'direct_relation_checks':tests,'raw_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
 'auditor_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'peer_review':'PENDING; independent implementation by same author'},indent=2))
