"""Exact finite controls for RECOVERY-PATH3; no polynomial SAT oracle."""
import itertools, json, hashlib
from fractions import Fraction as Q
from pathlib import Path

stats=dict(layouts=0,sat=0,unsat=0,selector_checks=0,false_selector_accepts=0,
           path_is_not_strategy=0,t5_rotated_witnesses=0,t5_arc_checks=0)
for bits in itertools.product((0,1),repeat=8):
    # Two rows, two disjoint private one-bit blocks, truth-table input.
    table=lambda z,i,y: bits[4*z+2*i+y]
    sat=any(table(z,0,a) and table(z,1,b)
            for z,a,b in itertools.product((0,1),repeat=3))
    accepted=[]
    for selector in itertools.product((0,1),repeat=2):
        valid=all(not table(z,selector[z],y)
                  for z,y in itertools.product((0,1),repeat=2))
        stats['selector_checks']+=1
        if valid: accepted.append(selector)
        assert not(valid and sat)
    assert bool(accepted)==(not sat)
    partial=any(all(not table(z,i,y) for y in (0,1))
                for z,i in itertools.product((0,1),repeat=2))
    stats['path_is_not_strategy']+=bool(partial and sat)
    stats['layouts']+=1; stats['sat' if sat else 'unsat']+=1

# Inspect existing full original-source witnesses, including all five rotations.
raw=Path('source079.t5').read_bytes()
arcs=[tuple(map(int,l.split()[1:])) for l in raw.decode().splitlines() if l.startswith('a ')]
data=json.loads(Path('results.complete.json').read_text())
assert hashlib.sha256(raw).hexdigest()==data['source']['sha256']
for e,c in data['lifting']['witnesses'].items():
    for shift in range(5):
        x=[(v+shift)%5 for v in c]
        assert len(x)==33
        for j,(u,v) in enumerate(arcs):
            assert (((x[v]-x[u])%5 in (1,3)) == (j!=int(e)))
            stats['t5_arc_checks']+=1
        stats['t5_rotated_witnesses']+=1

a,b,r=Q(35,100),Q(65,100),Q(195,1000)
threshold=(Q(133,100)-b-r)/a
assert threshold==Q(97,70)
assert (b+r)/(1-a)==Q(13,10)
stats['seed_time_threshold']=str(threshold)
stats['seed_space_threshold']=str(Q(1,2)/a)
stats['log_certificate_exponent_budget']=str(Q(134070,100000)-Q(133,100))
stats['recurrence_fixed_point']=str((b+r)/(1-a))
stats['scope']='Finite truth tables and supplied T5 certificate verification; no discovery speedup claimed.'
print(json.dumps(stats,sort_keys=True,indent=2))
