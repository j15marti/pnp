#!/usr/bin/env python3
"""TREE-AFFINE-JOIN122 compact independent source/gadget control.
Standard library; not the complete 108-random-tree extended audit.
Status COMPUTATIONAL, P vs NP OPEN. Run: python this_file.py
"""
from itertools import product
from random import Random
import json

def compile_chain(b,p,d):
    out=[];n=3*b+1
    def add(cl):
        nonlocal n
        if len(cl)==2:
            n+=1;z=n
            out.extend((tuple(cl)+(z,),tuple(cl)+(-z,)))
        elif len(cl)==1:
            n+=1;a=n;n+=1;c=n
            for aa in (a,-a):
                for cc in (c,-c):out.append(tuple(cl)+(aa,cc))
        elif len(cl)==3:out.append(tuple(cl))
        else:raise AssertionError("bad source width")
    for j in range(b):
        t=j+1;tn=j+2;u=b+2+j;w=2*b+2+j
        add((-u,t));add((u,-t));add((-w,))
        if j==0:add((-1,))
        if j==b-1:add(((b+1) if d else -(b+1),))
        for bits in product((0,1),repeat=3):
            if sum(bits)%2!=p[j]:
                add(tuple(-x if v else x for x,v in zip((u,tn,w),bits)))
    assert n==7*b+5 and len(out)==12*b+8
    return n,tuple(out)

def decode(n,cnf):
    if (n-5)%7 or n<12:return None
    b=(n-5)//7
    if len(cnf)!=12*b+8:return None
    p=[];pos=0
    for j in range(b):
        k=8+4*(j==0)+4*(j==b-1)
        found=[]
        for rhs in (0,1):
            a,bound,c=b+2+j,j+2,2*b+2+j
            wanted=tuple(tuple(-x if bit else x for x,bit in zip((a,bound,c),bits))
                for bits in product((0,1),repeat=3) if sum(bits)%2!=rhs)
            if cnf[pos+k:pos+k+4]==wanted:found.append(rhs)
        if len(found)!=1:return None
        p.append(found[0]);pos+=k+4
    for d in (0,1):
        if compile_chain(b,p,d)==(n,cnf):return (b,tuple(p),d)
    return None

def verify(n,cnf,a):
    return all(any(a.get(abs(x),0)==int(x>0) for x in c) for c in cnf)

def source_witness(b,p):
    t=[0]*(b+1)
    for j in range(b):t[j+1]=t[j]^p[j]
    a={j+1:t[j] for j in range(b+1)}
    for j in range(b):
        a[b+2+j]=t[j];a[2*b+2+j]=0
    return a

def brute_original_blocks(b,p,d):
    for values in product((0,1),repeat=3*b+1):
        a={i+1:values[i] for i in range(3*b+1)}
        if a[1]!=0 or a[b+1]!=d:continue
        if any(a[b+2+j]!=a[j+1] or a[2*b+2+j]!=0
            or (a[b+2+j]+a[j+2]+a[2*b+2+j])%2!=p[j] for j in range(b)):
            continue
        return True
    return False

def tree_messages(b,p,d):
    msg={d}
    total_probes=0
    for j in range(b-1,-1,-1):
        new=set()
        for v in (0,1):
            total_probes+=1
            if (v^p[j]) in msg:new.add(v)
        msg=new
    return 0 in msg,total_probes

def run():
    rng=Random(202610240508);rows=[];checked=0;deletions=0
    for b in (1,2,3,4,5,8,16,32,64,128):
        p=tuple(rng.randrange(2) for _ in range(b))
        for label in (False,True):
            d=(sum(p)%2)^(0 if label else 1)
            n,cnf=compile_chain(b,p,d)
            assert decode(n,cnf)==(b,p,d)
            t,queries=tree_messages(b,p,d)
            assert t==label and queries==2*b
            if label:assert verify(n,cnf,source_witness(b,p))
            if b<=5:
                assert brute_original_blocks(b,p,d)==label
                checked+=1
            if b<=16 and not label:
                for removed in range(b):
                    # Cut the removed-th relation. Independently solve left and
                    # right chains and verify all remaining original constraints.
                    tvals=[None]*(b+1);tvals[0]=0;tvals[b]=d
                    for j in range(removed):tvals[j+1]=tvals[j]^p[j]
                    for j in range(b-1,removed,-1):tvals[j]=tvals[j+1]^p[j]
                    assert all(v in (0,1) for v in tvals)
                    assert all((tvals[j]^tvals[j+1])==p[j]
                               for j in range(b) if j!=removed)
                    assert tvals[0]==0 and tvals[b]==d
                    deletions+=1
            w=(64*(n+len(cnf)+1)-1).bit_length()
            rows.append(dict(blocks=b,label='SAT' if label else 'UNSAT',
                variables=n,clauses=len(cnf),bits=(4*len(cnf)+2)*w,
                local_probe_candidates=queries))
    # Full gadget truth rows, proved independently of the source generator.
    for x,y,z in product((0,1),repeat=3):
        assert ((x or y or z) and (x or y or not z))==bool(x or y)
    for x in (0,1):
        sat=any(all(x or (a if sa else not a) or (c if sc else not c)
            for sa,sc in product((0,1),repeat=2))
            for a,c in product((0,1),repeat=2))
        assert sat==bool(x)
    for rhs in (0,1):
        for vals in product((0,1),repeat=3):
            unsatrows=[bits for bits in product((0,1),repeat=3) if sum(bits)%2!=rhs]
            observed=all(bits!=vals for bits in unsatrows)
            assert observed==(sum(vals)%2==rhs)
    print(json.dumps(dict(run='TREE-AFFINE-JOIN122',seed=202610240508,
        canonical_cases=len(rows),small_independent_brute=checked,
        parity_block_deletion_scenarios=deletions,
        gadget_truth_rows=8+2+16, failures=0, last=rows[-1],
        scope='canonical proper3CNF only; no all-input improvement',
        status='COMPUTATIONAL, P versus NP OPEN'),indent=2))
if __name__=='__main__':run()
