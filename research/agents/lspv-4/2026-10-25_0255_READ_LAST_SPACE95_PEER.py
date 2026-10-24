#!/usr/bin/env python3
"""Independent finite source-probe and both-label check. Not TM microcode."""
from itertools import product
import json,random
r=random.Random(202610250255)
triples=[tuple((i+1)*s[i] for i in range(3)) for s in product((-1,1),repeat=3)]
checks=0

def enc(cs):
    return tuple(map(int,'00000011'+f'{len(cs):08b}'+''.join('11'+''.join(f'{abs(x):07b}'+str(int(x<0)) for x in c) for c in cs)))

def dec(n,read):
    if n<16 or (n-16)%26:return 0
    a=lambda off,w:sum(read(off+j)<<(w-1-j) for j in range(w))
    count=a(8,8)
    if a(0,8)!=3 or count!=(n-16)//26:return 0
    cs=[]
    for j in range(count):
        p=16+26*j
        if a(p,2)!=3:return 0
        row=[]
        for k in range(3):
            v=a(p+2+8*k,7)
            if not 1<=v<=3:return 0
            row.append(-v if read(p+2+8*k+7) else v)
        cs.append(row)
    return int(any(all(any((bool((mask>>(abs(l)-1))&1))==(l>0) for l in c) for c in cs) for mask in range(8)))

def run(bits):
    global checks
    n=len(bits);read=[]
    def physical(i):
        read.append(i);return bits[i]
    for i in range(n-1):physical(i)
    answer=[]
    for b in (0,1):
        answer.append(dec(n,lambda i: b if i==n-1 else physical(i)))
        assert n-1 not in read;checks+=1
    assert len(set(read))==n-1;checks+=1
    result=answer[physical(n-1)]
    assert read[-1]==n-1 and result==dec(n,lambda i:bits[i]);checks+=1
    return result,tuple(answer)

core=[t for t in triples if t!=(1,2,3)]+[(1,2,3)]
U=enc(core);V=U[:-1]+(1,)
assert run(U)==(0,(0,1));checks+=1
assert run(V)==(1,(0,1));checks+=1
for _ in range(256):
    bits=enc([r.choice(triples) for _ in range(8)])
    run(bits)
    run(bits[:-1]+(1-bits[-1],))
print(json.dumps({'status':'PASS','checks':checks,'matched_bits':len(U),'tested_sources':514,'physical_prefix_copy_bits':0}))
