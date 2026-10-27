#!/usr/bin/env python3
"""HEADMOVE-RAM-VALIDATOR171: GitHub quick verifier for the exact22 code theorem.
Standard library only. The separate complete local audit also implements an
explicit four-sweep source-to-single-tape simulator and 85 itineraries.
"""
import itertools
from collections import Counter

W=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
A=(6,11); B=(17,9)
FIXED=tuple(j for j in range(20) if j not in A+B)
MAGIC="1010111100010010"

def gadget(a,b):
    out=[list(c) for c in W]
    if not a:
        for j in A:out[j][0]*=-1
    if not b:
        for j in B:out[j][2]*=-1
    return [tuple(row) for row in out]

def models(clauses):
    count=0
    for x in range(1<<15):
        if all(any(bool(x&(1<<(abs(l)-1)))==(l>0) for l in row)
               for row in clauses):count+=1
    return count

def spec(m):
    w=(20*m).bit_length()
    return w,16+2*w+60*m*(w+1)

def enc(m,a,b):
    w,n=spec(m)
    rows=[]
    for i in range(m):
        g=gadget(a[i],b[i])
        rows.extend(tuple((15*i+abs(l))*(1 if l>0 else -1)
                          for l in g[j]) for j in A)
    for i in range(m):
        g=gadget(a[i],b[i])
        rows.extend(tuple((15*i+abs(l))*(1 if l>0 else -1)
                          for l in g[j]) for j in FIXED)
    for i in range(m):
        g=gadget(a[i],b[i])
        rows.extend(tuple((15*i+abs(l))*(1 if l>0 else -1)
                          for l in g[j]) for j in B)
    assert len(rows)==20*m
    pos=Counter();neg=Counter()
    assert len(set(rows))==len(rows)
    for row in rows:
        assert len({abs(l) for l in row})==3
        for l in row:(pos if l>0 else neg)[abs(l)]+=1
    assert all(pos[i]==neg[i]==2 for i in range(1,15*m+1))
    def binary(i):return format(i,f"0{w}b")
    s=MAGIC+binary(15*m)+binary(20*m)
    for row in rows:
        for l in row:s+=("1" if l>0 else "0")+binary(abs(l))
    assert len(s)==n
    return s

def at(m,side,i):
    w,n=spec(m)
    head=16+2*w;stride=3*(w+1)
    if side=="A":return head+2*i*stride
    return head+(18*m+2*i)*stride+2*(w+1)

def query_image(x,m):
    w,n=spec(m)
    return not any(x[at(m,"A",i)]=="1" and x[at(m,"B",i)]=="1"
                   for i in range(m))

def jump_counts(m,cap,J):
    w,n=spec(m);targets=[]
    for lo in range(0,m,cap):
        hi=min(lo+cap,m)
        targets.extend(at(m,"A",i) for i in range(lo,hi))
        targets.extend(at(m,"B",i) for i in range(lo,hi))
    head=0;direction=0;length=0;commands=0;reversals=0
    for target in targets:
        distance=target-head
        if distance:
            direction2=(1 if distance>0 else -1)
            reversals+=int(direction!=0 and direction2!=direction)
            direction=direction2
            length+=abs(distance)
            commands+=(abs(distance)+J-1)//J
            head=target
    return length,commands,reversals

def main():
    expected=[772,272,272,0]
    got=[models(gadget(a,b)) for a in (0,1) for b in (0,1)]
    assert got==expected,(got,expected)
    tested=0; corrupted=0
    for m in range(1,4):
        controls=list(itertools.product((0,1),repeat=m))
        images={}
        for a in controls:
            for b in controls:
                s=enc(m,a,b)
                assert query_image(s,m)==(not any(ai&bi for ai,bi in zip(a,b)))
                images[a,b]=s;tested+=1
        for (a,b),s in images.items():
            for (c,d),t in images.items():
                distance=sum(x!=y for x,y in zip(s,t))
                expected_distance=2*sum(x!=y for x,y in zip(a,c))+2*sum(x!=y for x,y in zip(b,d))
                assert distance==expected_distance
        # On a canonical input every singleton bit change is noncanonical.
        choices=set(images.values())
        s=images[(0,)*m,(0,)*m]
        for i in range(len(s)):
            t=s[:i]+("0" if s[i]=="1" else "1")+s[i+1:]
            assert t not in choices
            corrupted+=1
    m=128;n=spec(m)[1]
    assert n==99880
    assert jump_counts(m,1,1)==(22910044,22910044,254)
    assert jump_counts(m,1,n)==(22910044,256,254)
    assert jump_counts(m,m,1)==(99828,99828,0)
    print({"W1_models":got,"whole_formulas":tested,
           "single_flips_rejected":corrupted,"m128_length":n,
           "jump1":jump_counts(m,1,1),"jumpN":jump_counts(m,1,n)})
if __name__=="__main__":main()
