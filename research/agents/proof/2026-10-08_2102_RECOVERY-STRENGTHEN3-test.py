"""Declared same-field restriction/orbit access; not the full SU/vMS extractor."""
from itertools import product
from pathlib import Path
import hashlib, json, random, signal, time
signal.alarm(25)
started = time.monotonic()
rng = random.Random(3102)

def mm(a,b,p):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))%p
             for j in range(len(b[0]))] for i in range(len(a))]
def mv(a,x,p):
    return [sum(u*v for u,v in zip(row,x))%p for row in a]
def plus(x,y,p): return [(a+b)%p for a,b in zip(x,y)]
def power(a,k,p):
    d=len(a); out=[[int(i==j) for j in range(d)] for i in range(d)]
    while k:
        if k&1: out=mm(out,a,p)
        a=mm(a,a,p); k//=2
    return out
def gl2(p):
    return [[[a,b],[c,d]] for a,b,c,d in product(range(p),repeat=4)
            if (a*d-b*c)%p]
def edge(a,k,b,side,p):
    a=power(a,k,p); d=len(a); z=[[0]*d for _ in range(d)]
    return (a+z,[0]*d+list(b)) if side==0 else (z+a,list(b)+[0]*d)
def compose(edges,p):
    d=len(edges[0][0]); m=[[int(i==j) for j in range(d)] for i in range(d)]; c=[0]*d
    for b,s in edges:
        c=plus(mv(m,s,p),c,p)
        m=mm(m,b,p)
    return m,c
def chain_point(edges,z,p):
    for b,c in reversed(edges): z=plus(mv(b,z,p),c,p)
    return z
def root_value(z,p):
    return (sum((i+1)*v*v for i,v in enumerate(z))+z[0]*z[-1])%p
def bit(value,mask): return (value&mask).bit_count()%2

calls=0
def requested_bit(edges,z,mask,p):
    global calls
    point=chain_point(edges,z,p)
    calls+=1  # exactly one invocation in this no-cache implementation
    return bit(root_value(point,p),mask)

paths=0; checks=0; cases=[]
for p in (2,3,5):
    mats=gl2(p)
    if p==2:
        configs=product(mats,range(1,p),product(range(p),repeat=2),range(p),range(2),range(2),range(1,4),range(1,4))
    else:
        configs=[(rng.choice(mats),rng.randrange(1,p),(rng.randrange(p),rng.randrange(p)),rng.randrange(p),rng.randrange(2),rng.randrange(2),rng.randrange(1,8),rng.randrange(1,8)) for _ in range(100)]
    local_paths=0; local_checks=0
    for a,s,b,c,side1,side2,i,j in configs:
        edges=[edge(a,i,b,side1,p),edge([[s]],j,[c],side2,p)]
        m,shift=compose(edges,p)
        for z in range(p):
            direct=chain_point(edges,[z],p)
            fused=plus(mv(m,[z],p),shift,p)
            assert direct==fused
            for mask in range(1<<(p-1).bit_length()):
                assert requested_bit(edges,[z],mask,p)==bit(root_value(fused,p),mask)
                checks+=1; local_checks+=1
        paths+=1; local_paths+=1
    cases.append({'p':p,'paths':local_paths,'coordinate_bit_checks':local_checks,'mode':'exhaustive supplied GL2/block/short-orbit grid' if p==2 else 'seeded paths; exhaustive bottom points and masks'})

assert calls==checks
before=calls
for _ in range(7): requested_bit(edges,[0],1,p)
assert calls-before==7
# Nonlinear type-changing re-encoding is not an affine coordinate map:
# x->x*x over F_3 cannot equal ax+b, since values at 0,1 force a=1,b=0,
# while value at 2 is 1, not 2.
assert (2*2)%3 != 2
result={'status':'COMPUTATIONAL','scope':'Same-field affine address composition only; no extractor quality, vMS identity, SAT-return or acquisition theorem',
        'seed':3102,'paths':paths,'bit_checks':checks,'root_calls_in_main_checks':checks,
        'repeat_request_calls':7,'cases':cases,'nonlinear_reencoding_affine_control':'rejected',
        'budget_seconds':25,'elapsed_seconds':round(time.monotonic()-started,6),
        'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'all_passed':True}
print(json.dumps(result,indent=2))
