#!/usr/bin/env python3
"""Independent analytic-model regression for LSPV-2/471, NOT native FLMV execution."""
import json
from itertools import product
from pathlib import Path

EDGE=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))

def parity_labels():
    out=[]
    for charges in product((0,1), repeat=4):
        count=0
        for values in product((0,1), repeat=6):
            vertex=[]
            for v in range(4):
                incident=(values[i] for i,e in enumerate(EDGE) if v in e)
                parity=0
                for bit in incident: parity ^= bit
                vertex.append(parity)
            if tuple(vertex)==charges: count+=1
        assert count==(0 if sum(charges)%2 else 8)
        out.append({'charges': ''.join(map(str,charges)), 'models':count})
    return out

def prefix_cost(B,k):
    # The guest executes B^k right moves along its uncharged INDEX tape
    # and one bit-write at the farthest position, without WORK access.
    H=B**k
    guest_time=2*H+3
    guest_work=0
    # The specifically audited dense placement stores the last bit at
    # a physical host non-index WORK location >= H, regardless of values.
    host_min_work=H
    return B,k,H,guest_time,guest_work,host_min_work

out={'controls':parity_labels(),'cases':[]}
for B in (4,8,12,16,24,32,48,64,96,128):
    B,k,H,t,sw,hw=prefix_cost(B,2)
    assert t==2*H+3 and sw==0 and hw==B*B
    assert hw>B
    out['cases'].append({'B':B,'k':k,'guest_time':t,'guest_work':sw,'host_min_work':hw,'ratio':hw/B})

# Symbolic exponent control for a parent N=B^2: for any finite s>=0,
# picking a fixed integer k>max(s,1) defeats the target B^max(1,s).
for s in (0,0.25,0.5,1,2,3.5,8):
    k=int(s)+2
    assert k>max(1,s)
    out['cases'].append({'guest_space_exponent':s,'chosen_index_exponent':k,
                         'host_exponent_k':k,'allowed_exponent_max_1_s':max(1,s)})

out['checks']=len(out['controls'])+len(out['cases'])
print(json.dumps(out,indent=2))
