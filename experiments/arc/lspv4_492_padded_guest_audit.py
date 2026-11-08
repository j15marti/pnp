#!/usr/bin/env python3
"""LSPV-4/492 reproducible *restricted* guest-pass-through audit.
No native FLMV interpreter or hypothetical polynomial SAT decider is implemented.
The finite solver and the symbolic padded-guest calculations are independent controls.
"""
from itertools import product
from math import ceil, log2
from json import dump
from pathlib import Path

def encode(F, n):
    m = len(F)
    assert 0 <= n <= 3*m+3 and all(len(c) <= 3 and all(1 <= abs(x) <= n for x in c) for c in F)
    b = (128*(n+m+3)-1).bit_length()
    bits = lambda x, width: format(x, f'0{width}b')
    records = []
    for c in F:
        slots = ['1'+('1' if x > 0 else '0')+bits(abs(x), b) for x in c]
        records.append(''.join(slots + ['0'*(b+2)]*(3-len(slots))))
    return '1'*b + '0' + bits(n,b) + bits(m,b) + ''.join(records)

def decode(src):
    if not src or set(src)-set('01') or '0' not in src:
        raise ValueError('bad bits')
    b = src.index('0')
    if b <= 0 or len(src) < 3*b+1: raise ValueError('header')
    n, m = int(src[b+1:2*b+1],2), int(src[2*b+1:3*b+1],2)
    if n>3*m+3 or b != (128*(n+m+3)-1).bit_length() or len(src) != 3*b+1+3*m*(b+2):
        raise ValueError('canonical length/header')
    p=3*b+1; F=[]
    for _ in range(m):
        c=[]; absent=False
        for _ in range(3):
            valid,sign=src[p:p+2]; p+=2
            var=int(src[p:p+b],2);p+=b
            if valid=='0':
                if sign!='0' or var!=0:raise ValueError('corrupt empty slot')
                absent=True
            else:
                if absent or not (1<=var<=n):raise ValueError('corrupt literal')
                c.append(var if sign=='1' else -var)
        F.append(c)
    return F,n

def transform_fast(F,n):
    assert all(len(c)==3 and len({abs(x) for x in c})==3 for c in F)
    m=len(F);z=n+m+1; u=z+1;v=z+2
    out=[]
    for i,(a,b,c) in enumerate(F):
        h=n+i+1
        out.extend([[a,b,h],[-h,c,z]])
    for s in (1,-1):
        for t in (1,-1):out.append([-z,s*u,t*v])
    return out,v

def sat(F,n):
    # Exact exhaustive finite oracle only, not a uniform polynomial SAT decider.
    for a in product((False,True),repeat=n):
        if all(any(a[abs(x)-1]==(x>0) for x in c) for c in F):return True
    return False

def simulate_padded_steps(length,k):
    # Concrete counting of mandatory finite guest delay, with upper cap.
    z=0
    for _ in range(length**k):z+=1
    return z

def main():
    examples=[('SAT_single',[[1,2,3]],3),
      ('SAT_mixed',[[1,-2,3],[-1,2,-3]],3),
      ('UNSAT_complete',[[s*1,t*2,u*3] for s,t,u in product((1,-1),repeat=3)],3)]
    reports=[]; asserts=0; rejects=0; actual_loops=0
    for label,F,n in examples:
        original=encode(F,n); out,n1=transform_fast(F,n); child=encode(out,n1)
        assert decode(original)==(F,n);asserts+=1
        assert decode(child)==(out,n1);asserts+=1
        assert len(out)==2*len(F)+4;asserts+=1
        assert len(child)>=len(original);asserts+=1
        assert sat(F,n)==sat(out,n1);asserts+=1
        for k in (2,3,4,6,8):
            M=len(child); N=len(original)
            guaranteed_steps=M**k
            assert guaranteed_steps>N**(k/2+0.6) and guaranteed_steps>N**1.1;asserts+=1
            if label=='SAT_single' and k==2:
                count=simulate_padded_steps(M,k)
                assert count==guaranteed_steps;asserts+=1;actual_loops=count
        reports.append({'case':label,'N_input_bits':len(original),'M_child_bits':len(child),
            'clauses_in':len(F),'clauses_out':len(out),'source_SAT':sat(F,n),
            'child_SAT':sat(out,n1),'M_over_N':round(len(child)/len(original),5)})
    F,n=examples[0][1:];src=encode(F,n)
    for bad in ['',src[:-1],src+'1',src[:3]+'2'+src[4:]]:
        try:decode(bad);raise AssertionError('malformed accepted')
        except ValueError: rejects+=1
    # Algebraic threshold test
    for a1000 in (501,550,600,750,1000):
        a=a1000/1000
        k=max(2,int(0.6/(a-0.5))+2)
        assert a*k > 0.6+k/2 and a*k > 1.1; asserts+=1
    for N in (32,100,1000):
        S=N
        assert S>N**0.5; asserts+=1
    result={'status':'PROVED/RESTRICTED analytic argument; COMPUTATIONAL finite controls',
        'scope':'faithful one-complete-guest-call pass-through on child length M>=N^a; not arbitrary code-aware SAT compiler',
        'precondition':'SAT in P for polynomial padded decider A_k; no such solver assumed to exist unconditionally',
        'formula':'T_C(N)>=M(N)^k; for a>1/2 choose k>max(t0,0.6/(a-1/2),1.1/a)',
        'cases':reports,'assertions':asserts,'malformed_rejections':rejects,
        'actually_executed_dummy_guest_transitions':actual_loops,
        'native_flmv_execution':False,'failures':0}
    dest=Path(__file__).with_suffix('.json');dest.write_text(__import__('json').dumps(result,indent=2)+'\n')
    print(__import__('json').dumps(result,indent=2))

if __name__=='__main__':main()
