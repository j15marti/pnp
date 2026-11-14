#!/usr/bin/env python3
"""Independent TMR-5/017 red-team: delayed INDEX with movable source head.
Only finite abstract-state collisions and head geometry are executed. Runtime and
configuration-count theorems are established separately by the report proof.
"""
from collections import defaultdict
import json, hashlib, sys


def sketch(bits, size, kind):
    if size == 0: return ''
    if kind == 'prefix': return bits[:size]
    if kind == 'suffix': return bits[-size:]
    acc=[0]*size
    for i,v in enumerate(bits):
        b=int(v)
        if kind == 'xor': acc[i%size]^=b
        else:
            k=(7*i*i+3*i+1)%size
            acc[k]^=b
            if i%3==0: acc[(k+1)%size]^=b
    return ''.join(map(str,acc))


def park(bits, name):
    L=len(bits)
    if name=='left': return 0
    if name=='right': return L+1
    if name=='center': return (L+1)//2
    if name=='parity-ends': return 0 if bits.count('1')%2 == 0 else L+1
    if name=='first-one': return (bits.find('1')+1) if '1' in bits else 0
    if name=='quadrant': return (sum(int(b) for b in bits)%4)*(L+1)//3
    raise ValueError(name)


def local_observation(bits, u, t):
    return ''.join(bits[j-1] for j in range(1,len(bits)+1) if abs(j-u)<=t)


def run():
    cases=0
    guaranteed_cases=0
    collision_witnesses=0
    pair_checks=0
    max_witness_distance=0
    fullcopy_checks=0
    center_geometry_checks=0
    samples=[]
    kinds=('prefix','suffix','xor','nonlinear')
    parks=('left','right','center','parity-ends','first-one','quadrant')
    for L in range(4,11):
        inputs=[format(v,f'0{L}b') for v in range(1<<L)]
        for s in range(0,min(4,L-1)+1):
            for kind in kinds:
                for pk in parks:
                    states=[(park(x,pk),sketch(x,s,kind),x) for x in inputs]
                    for t in range(0,min(L,4)+1):
                        cases+=1
                        # Count a coarser M=2^s actual finite sketch states.
                        guaranteed=(1<<L) > (L+2)*(1<<s)*(1<<(2*t+1))
                        if guaranteed:guaranteed_cases+=1
                        seen={}; witness=None
                        for u,st,x in states:
                            key=(u,st,local_observation(x,u,t))
                            if key in seen:
                                witness=(u,st,seen[key],x)
                                break
                            seen[key]=x
                        if guaranteed:
                            assert witness is not None,(L,s,kind,pk,t,'missing collision')
                        if witness is not None:
                            collision_witnesses+=1
                            u,st,x,y=witness
                            assert x!=y and park(x,pk)==park(y,pk)==u
                            assert sketch(x,s,kind)==sketch(y,s,kind)==st
                            assert local_observation(x,u,t)==local_observation(y,u,t)
                            p=next(i+1 for i,(a,b) in enumerate(zip(x,y)) if a!=b)
                            assert abs(p-u)>t,(L,s,kind,pk,t,x,y,p,u)
                            assert x[p-1]!=y[p-1]
                            pair_checks+=1
                            max_witness_distance=max(max_witness_distance,abs(p-u))
                            if len(samples)<10 and guaranteed:
                                samples.append(dict(L=L,s=s,kind=kind,park=pk,radius=t,head=u,query=p,x=x,y=y,retained_sketch=st,physical_move_needed=abs(p-u)))
        # Full source copy is injective at every radius irrespective of parking.
        for x in inputs:
            u=(L+1)//2
            key=(u,x,local_observation(x,u,0))
            assert key[1]==x
            fullcopy_checks+=1
        u=(L+1)//2
        # Centered original head has max physical distance <= ceil(L/2).
        assert max(abs(p-u) for p in range(1,L+1))<= (L+1)//2
        center_geometry_checks+=L
    data=dict(status='COMPUTATIONAL',run='TMR-5/017',python=sys.version.split()[0],model='synthetic finite retained-work sketches with input-dependent parked head; explicit one-head geometry; not arbitrary TM compiler',lengths=[4,10],sketch_kinds=list(kinds),parking_policies=list(parks),cases=cases,guaranteed_collisions_checked=guaranteed_cases,actual_collision_cases=collision_witnesses,indistinguishability_pairs_checked=pair_checks,max_witness_bit_distance=max_witness_distance,full_source_copy_injectivity_checks=fullcopy_checks,centered_head_distance_checks=center_geometry_checks,failed_assertions=0,samples=samples,limitations='Source-preprocessing sketch and queried-position parsing use Python host operations, not charged physical TM. All-length claim is mathematical. Total TM time includes all query arithmetic; midpoint upper bound directly concerns source-head movements.')
    return data

if __name__=='__main__':
    output=json.dumps(run(),indent=2,sort_keys=True)+'\n'
    print(output)
