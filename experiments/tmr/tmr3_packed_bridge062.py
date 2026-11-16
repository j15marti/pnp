#!/usr/bin/env python3
"""Finite TMR-3/062 audit: two live writable tracks, bounded head spread,
charged virtual one-head sweeps and both-label source/output agreement.
No native transition compiler or 2/5-space simulator is run.
"""
from itertools import product
from collections import Counter
from pathlib import Path
import json, hashlib, random, sys
REV='tmr3-packed-bridge062-v2'; SEED=202611152224
rng=random.Random(SEED); C=Counter()
def test(ok, tag):
    C[tag]+=1
    if not ok: raise AssertionError(tag)
def run(x):
    if any(c not in '01' for c in x): return None
    direct=[{},{}]; packed={}; pos=[0,0]; mark=[0,0]
    state=prev=0; physical=0; spread=0; seen=set()
    for ch in x:
        v=int(ch); L=min(mark); R=max(mark); d=R-L
        spread=max(spread,d)
        test(pos==mark,'head_identical')
        # The one-head packer reads all p marked tracks in a bounded sweep.
        old=[direct[k].get(pos[k],0) for k in (0,1)]
        recovered=[packed.get(mark[k],[0,0])[k] for k in (0,1)]
        test(old==recovered,'symbol_identical')
        # Two scans collect/read and write the simultaneous original step.
        # Two extra enlarged scans carry pending radius-one marker moves.
        stepcost=4*(d+3)+2
        physical+=stepcost
        seen.update(range(L-1,R+2))
        w=[old[0]^v^state,old[1]^old[0]^v]
        for k in (0,1):
            direct[k][pos[k]]=w[k]
            packed.setdefault(mark[k],[0,0])[k]=w[k]
        next_state=state^(old[0]&old[1])^v
        direction=2*v-1
        shifts=[direction,prev]
        pos=[pos[k]+shifts[k] for k in (0,1)]
        mark=[mark[k]+shifts[k] for k in (0,1)]
        state,prev=next_state,direction
        test(pos[0]-pos[1]==direction,'telescoping_diameter')
        test(max(pos)-min(pos)<=1,'actual_diameter_at_most_one')
        test(stepcost<=18*(d+3),'charged_scan_bound')
    physical+=1  # EOF and output
    test(physical<=18*(spread+3)*len(x)+1,'global_same_execution_budget')
    return {'out':state,'heads':pos,'t':len(x)+1,'spread':spread,
            'packed_scan_steps':physical,'packed_cell_span':len(seen)}
def independent(x):
    tapes=[{},{}]; p=[0,0]; s=prev=0
    for char in x:
        z=int(char); a=tapes[0].get(p[0],0); b=tapes[1].get(p[1],0)
        tapes[0][p[0]]=a^z^s; tapes[1][p[1]]=b^a^z
        s^=(a&b)^z; d=2*z-1; p=[p[0]+d,p[1]+prev]; prev=d
    return s,p
allcases=[]
for n in range(11):
    for bits in product('01',repeat=n):
        x=''.join(bits); got=run(x); s,p=independent(x)
        test((got['out'],got['heads'])==(s,p),'independent_output_and_heads')
        allcases.append(got)
for n in (16,32,64,100):
    for _ in range(30):
        x=''.join(str(rng.randrange(2)) for _ in range(n))
        got=run(x)
        test((got['out'],got['heads'])==independent(x),'random_semantics')
for bad in ('2','001x','X','11\n','1\u00a0'):
    test(run(bad) is None,'malformed_rejected')
deltas=[(a,b) for a,b in ((0,1),(1,8),(1,4),(1,3),(1,2),(1,1))]
raw={'revision':REV,'seed':SEED,'assertions':sum(C.values()),'failures':0,
     'exhaustive_binary_sources':len(allcases),'random_sources':120,
     'malformed_controls':5,'max_spread':max(z['spread'] for z in allcases),
     'output_labels':sorted({z['out'] for z in allcases}),
     'exponent_tests':[{'delta':f'{a}/{b}','exponent':2*(1+a/b)/5,
                         'beats_half':(a/b)<0.25} for a,b in deltas],
     'scope':'abstract simultaneous packed track sweeps, not native microcode',
     'source_symbol_access':'real read-only source, one input bit per original step',
     'time_model':'actual final space-simulator running time unrestricted',
     'review':'math proof and OAI comparator not independently executed'}
if __name__=='__main__':
    raw['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    dest=Path(sys.argv[1]) if len(sys.argv)>1 else Path('raw062.json')
    dest.write_text(json.dumps(raw,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:raw[k] for k in ('revision','assertions','exhaustive_binary_sources','random_sources','failures')}))
