#!/usr/bin/env python3
"""Independent no-producer-import audit for LSPV-1 PAID-HIGHWIDTH-NAE314.
Reconstructs original clauses from a separate port/stub generator.
Finite verification is not unrestricted SAT hardness or native FLMV timing.
"""
from collections import Counter,defaultdict
from itertools import combinations
import hashlib,json

F9_P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
F9_N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F9=F9_P+tuple(tuple(-x for x in c) for c in F9_N)
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
F15P=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),
      (6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
F15N=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),
      (4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=F15P+tuple(tuple(-x for x in c) for c in F15N)

def verify_formula(F):
    n=max(abs(x) for c in F for x in c)
    cnt=Counter(x for c in F for x in c)
    assert len(F)*3==4*n
    assert len(set(tuple(sorted(c)) for c in F))==len(F)
    assert all(len(c)==3 and len({abs(x) for x in c})==3 and
               (all(x>0 for x in c) or all(x<0 for x in c)) for c in F)
    assert all(cnt[x]==cnt[-x]==2 for x in range(1,n+1))
def truth(F,a):
    return all(any((a[abs(x)]==1)==(x>0) for x in c) for c in F)
def gamma(q):
    s=bin(q)[2:];return '0'*(len(s)-1)+s
def bits(F):
    n=max(abs(x) for c in F for x in c);w=n.bit_length()
    return gamma(n)+gamma(len(F))+''.join(
        ('1' if c[0]>0 else '0')+''.join(bin(abs(x))[2:].zfill(w) for x in c)
        for c in F)
def reconstruct(k):
    def v(i,j,p):return (i%k,j%k,'NESW'[p])
    edges={}
    for i in range(k):
        for j in range(k):
            for p,q in ((0,1),(1,2),(2,3),(3,0)):
                edges[tuple(sorted((v(i,j,p),v(i,j,q))))]='inside'
            edges[tuple(sorted((v(i,j,1),v(i,j+1,3))))]='outside'
            edges[tuple(sorted((v(i,j,2),v(i+1,j,0))))]='outside'
    edges=sorted(edges.items())
    assert len(edges)==6*k*k
    star=defaultdict(list);matching=set()
    for x,(edge,category) in enumerate(edges,1):
        for endpoint in edge:star[endpoint].append(x)
        if category=='inside' and {edge[0][2],edge[1][2]} in ({'E','N'},{'S','W'}):
            matching.add(x)
    pos=tuple(tuple(sorted(star[v])) for v in sorted(star))
    F=pos+tuple(tuple(-x for x in c) for c in pos)
    a={x:int(x in matching) for x in range(1,6*k*k+1)}
    verify_formula(F);assert truth(F,a)
    assert all(sum(x in matching for x in star[v])==1 for v in star)
    assert len(star)==4*k*k and len(matching)==2*k*k
    colors={v:((v[0]+v[1])&1)^(0 if v[2] in ('N','S') else 1) for v in star}
    assert all(colors[a]!=colors[b] for (a,b),_ in edges)
    assert len([e for e,t in edges if t=='outside'])==2*k*k
    return F,a
def models(F,p=None):
    p=p or {};n=max(abs(x) for c in F for x in c);out=[]
    for z in range(1<<n):
        a={i:(z>>(i-1))&1 for i in range(1,n+1)}
        if all(a[x]==v for x,v in p.items()) and truth(F,a):out.append(z)
    return out

def run():
    # Independently reconstructed original-source hashes must match the separate producer.
    expected={
      4:(96,128,2844,64,"1a55552dcbb6042a46b8be4f378acd848899d68711f3d07120a90c19c5a446df"),
      6:(216,288,7232,144,"c9ba2d1086e3fab06fce1db796439ba83d12c3e7ac60a8415501f49fa86504e1"),
      8:(384,512,14372,256,"99aaae69c9a35c0b8bea2077b8b21b612eaf4abc5ba365d8d8e1429277484bc5")}
    stars=0;dual_edges=0
    for k,(n,m,L,d,h) in expected.items():
        F,a=reconstruct(k);star_count=4*k*k
        assert len(F)==m and len(a)==n and len(bits(F))==L
        assert hashlib.sha256(bits(F).encode()).hexdigest()==h
        assert 2*n-m==d
        stars+=star_count;dual_edges+=6*k*k
    assert (stars,dual_edges)==(464,696) # k=4+6+8 only, no lifted copies
    for F,total in ((F9,70),(Y6,20),(F15,1032)):
        verify_formula(F);assert len(models(F))==total
    pS={1:0,3:0,5:1,6:0,7:0,8:0};pU={**pS,1:1}
    assert len(models(F9,pS))==2 and len(models(F9,pU))==0
    for z in range(8):
        a={**pU,2:z&1,4:(z>>1)&1,9:(z>>2)&1}
        assert not truth(F9,a)
    # Original-clause pair-extreme compatibility with explicit local target assignments.
    extreme_count=0
    for i,j in combinations(range(12),2):
        for first in (0,1):
            for second in (0,1):
                required={};good=True
                for clause,flag in ((F9[i],first),(F9[j],second)):
                    for lit in clause:
                        q=int((lit>0)==bool(flag))
                        if abs(lit) in required and required[abs(lit)]!=q:good=False
                        required[abs(lit)]=q
                opposite=any(-x in F9[j] for x in F9[i])
                same=any(x in F9[j] for x in F9[i])
                assert good== (not opposite if first==second else not same)
                extreme_count+=1
    assert extreme_count==264
    complement_checks=0
    for F in (F9,Y6,F15):
        n=max(abs(x) for c in F for x in c)
        for z in range(1<<n):
            for c in F:
                t=sum(int(((z>>(abs(x)-1))&1)==int(x>0)) for x in c)
                u=sum(int((((~z)>>(abs(x)-1))&1)==int(x>0)) for x in c)
                assert t+u==3;complement_checks+=1
    assert complement_checks==662016
    print(json.dumps({"PASS":True,"source_stars":stars,"dual_edges":dual_edges,
        "source_sha256_matched":3,"F9_Y6_F15_models":[70,20,1032],
        "F9_same_original_SAT_UNSAT":[2,0],
        "SU_modes":extreme_count,"complement_checks":complement_checks,
        "unrestricted_complexity":"OPEN"},indent=2))
if __name__=="__main__":run()
