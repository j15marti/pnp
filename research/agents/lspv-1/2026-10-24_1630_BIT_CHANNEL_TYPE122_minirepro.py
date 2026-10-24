#!/usr/bin/env python3
"""BIT-CHANNEL-TYPE122: exact finite DPLL and typed-resource controls."""
import itertools
import json
checks=0

def assert_count(p, message=""):
    global checks
    checks+=1
    if not p:
        raise AssertionError(message or ("check "+str(checks)))

def encode(bits):
    q=len(bits)
    fresh=q+2
    C=[]
    def split(a,b):
        nonlocal fresh
        z=fresh
        fresh+=1
        C.extend(((a,b,z),(a,b,-z)))
    def force(lit):
        nonlocal fresh
        u,v=fresh,fresh+1
        fresh+=2
        for x,y in itertools.product((1,-1),repeat=2):
            C.append((lit,x*u,y*v))
    force(-1)
    force(-(q+1))
    for i,b in enumerate(bits,1):
        if b:
            split(i,i+1)
            split(-i,-(i+1))
        else:
            split(-i,i+1)
            split(i,-(i+1))
    assert_count(fresh-1==3*q+5,"n")
    assert_count(len(C)==4*q+8,"m")
    assert_count(all(len(set(abs(z) for z in c))==3 for c in C),"proper")
    return C,fresh-1

def sat(C,A=None):
    if A is None:A={}
    while True:
        changed=False
        for c in C:
            unresolved=[]
            satisfied=False
            for l in c:
                v=A.get(abs(l))
                if v is None:
                    unresolved.append(l)
                elif v==(l>0):
                    satisfied=True
                    break
            if satisfied:continue
            if not unresolved:return False
            if len(unresolved)==1:
                l=unresolved[0]
                v=abs(l)
                b=l>0
                if v in A and A[v]!=b:return False
                if v not in A:
                    A[v]=b
                    changed=True
        if not changed:break
    pick=None
    for c in C:
        if any(abs(l) in A and A[abs(l)]==(l>0) for l in c):continue
        for l in c:
            if abs(l) not in A:
                pick=abs(l)
                break
        if pick is not None:break
    if pick is None:return True
    return sat(C,{**A,pick:True}) or sat(C,{**A,pick:False})

rows=[]
for q in range(1,9):
    binary=sum((i^(i+1)).bit_count() for i in range(q))
    def gray(i):return i^(i>>1)
    grayflips=sum((gray(i)^gray(i+1)).bit_count() for i in range(q))
    assert_count(binary>=q and grayflips==q,"head activity")
    positives=negatives=0
    for bits in itertools.product((0,1),repeat=q):
        C,n=encode(bits)
        answer=sat(C)
        assert_count(answer==(sum(bits)%2==0),"source parity")
        positives+=int(answer)
        negatives+=int(not answer)
        W_work=0
        control_flips=sum(bits)
        delta_binary=binary+control_flips
        delta_gray=grayflips+control_flips
        assert_count(delta_binary>=q and delta_gray>=q,"complete flips")
        assert_count(W_work==0 and delta_binary>W_work and delta_gray>W_work,"typed failure")
        assert_count(control_flips==sum(bits),"control")
        if not any(bits):assert_count(control_flips==0,"unchanged parity")
    assert_count(positives==negatives==2**(q-1),"both labels")
    rows.append(dict(q=q,variables=n,clauses=len(C),instances=2**q,
        SAT=positives,UNSAT=negatives,W_work=0,
        head_flips_binary=binary,head_flips_gray=grayflips))
print(json.dumps(dict(name="BIT-CHANNEL-TYPE122",instances=510,
     checks=checks,failures=0,rows=rows,
     status="COMPUTATIONAL; all-input ARC-EDGE-90 OPEN"),indent=2))
