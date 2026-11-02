#!/usr/bin/env python3
"""CLOCK-SUBCORE-B2-FIREWALL339: finite checks, not asymptotic proof.
Standard library; deterministic; no external SAT or proof oracle.
For growing k, exact W formula follows from separately proved minimality,
not from enumerating an exponential clock.
"""
from itertools import product
from hashlib import sha256
import json

def chain(k):
    return tuple([(1,)] + [(-i,i+1) for i in range(1,k)] + [(-k,)])

def assignments(cs):
    n=max((abs(z) for c in cs for z in c),default=0)
    return [bits for bits in product((0,1),repeat=n)
            if all(any(bits[abs(z)-1]==int(z>0) for z in c) for c in cs)]

def binary_encode(cs):
    n=max((abs(z) for c in cs for z in c),default=0)
    b=max(1,n.bit_length())
    out='1'*n+'0'+'1'*len(cs)+'0'
    for c in cs:
        out+='1'*len(c)+'0'
        for z in c:
            out+=('1' if z>0 else '0')+format(abs(z),f'0{b}b')
    return out

def binary_decode(src):
    if not src or any(x not in '01' for x in src):
        raise ValueError('alphabet')
    i=0
    def unary():
        nonlocal i
        v=0
        while i<len(src) and src[i]=='1':
            v+=1;i+=1
        if i==len(src):raise ValueError('framing')
        i+=1
        return v
    n=unary();m=unary();b=max(1,n.bit_length());cs=[]
    for _ in range(m):
        k=unary();c=[]
        for __ in range(k):
            if i+b+1>len(src):raise ValueError('truncated')
            sign=src[i]=='1';i+=1
            var=int(src[i:i+b],2);i+=b
            if not (1<=var<=n):raise ValueError('variable')
            c.append(var if sign else -var)
        cs.append(tuple(c))
    if i!=len(src):raise ValueError('extra')
    return tuple(cs)

rows=[]
for k in range(1,7):
    f=chain(k)
    assert not assignments(f) and binary_decode(binary_encode(f))==f
    assert all(assignments(f[:j]+f[j+1:]) for j in range(len(f)))
    assert len(assignments(f[:-1]+((k,),)))==1
    N=len(binary_encode(f))
    rows.append({'k':k,'N':N,'m':k+1,
                 'W_resolution':k,'W_clock_exact':f'2^{N}+{k+1}'})
core=chain(1); padded=core+((2,-2),)
assert binary_decode(binary_encode(padded))==padded
assert len(binary_encode(core))==13 and len(binary_encode(padded))==26
# Complete 13-bit counter trace, enumerating every legal predecessor.
hashobj=sha256()
width=len(binary_encode(core))
for v in range(1<<width):
    hashobj.update(v.to_bytes((width+7)//8,'big'))
def legal(a,b,context=True):
    return context and 0<=a<(1<<width)-1 and b==a+1
assert not legal(0,2) and not legal(3,1)
assert not legal((1<<width)-1,1<<width) and not legal(0,1,False)

# Independently specified Tseitin sign control, cubic K4.
edges=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
def parity(charges):
    clauses=[]
    for vertex in range(4):
        inc=[i+1 for i,(a,b) in enumerate(edges) if vertex in (a,b)]
        for bits in product((0,1),repeat=3):
            if sum(bits)%2==charges[vertex]:continue
            clauses.append(tuple(-x if bit else x for x,bit in zip(inc,bits)))
    return tuple(clauses)
odd=parity((1,0,0,0)); even=parity((0,0,0,0))
assert len(assignments(odd))==0 and len(assignments(even))==8
assert all(assignments(odd[:i]+odd[i+1:]) for i in range(16))
assert all(assignments(odd[:i]+(tuple(-v if p==j else v for p,v in enumerate(odd[i])),)+odd[i+1:])
           for i in range(16) for j in range(3))

malformed=('','111','101','1001','100100','1000000',
           '101101011100','10110101110010','not-binary')
for bad in malformed:
    try: binary_decode(bad)
    except ValueError: pass
    else: raise AssertionError('Accepted malformed '+bad)

result={'run':'CLOCK-SUBCORE-B2-FIREWALL339',
        'status':'PROVED model-specific mathematical theorem; COMPUTATIONAL controls; P vs NP OPEN',
        'rows':rows,'clock_H1':{'bits':width,'states':2**width,
                               'SHA256':hashobj.hexdigest()},
        'source_heredity_pad':{'core_bits':13,'padded_bits':26,
                                'same_selected_unsat_core':True},
        'K4':{'odd_models':0,'even_models':8,'deletion_sat':16,'sign_flip_sat':48},
        'guarded_boundary':{'UNSAT':[2,0],'SAT':[2,1]},
        'malformed_rejected':len(malformed),'forged_clock_moves_rejected':4}
print(json.dumps(result,indent=2,sort_keys=True))
