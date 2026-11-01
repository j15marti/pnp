#!/usr/bin/env python3
"""Canonical M22 residual leakage, odd-cycle saturation, exact two-label controls.
Run from a full j15marti/pnp checkout. Pure stdlib. This is not a FLMV TM.
Full separate producer, independent checker, raw traces in reproducibility ZIP.
"""
from itertools import product
from collections import Counter
from pathlib import Path
import ast,json,hashlib,time
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
Z=((1,2,4),(1,3,5),(2,3,6),(-1,-2,-7),(-1,-3,-8),(-2,-3,-9),
   (4,7,8),(5,7,9),(6,8,9),(-4,-5,-7),(-4,-6,-8),(-5,-6,-9))
W='001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101'
def good(F,n):
    if n%3 or not n or 3*len(F)!=4*n:return False
    cnt=Counter();seen=set()
    for c in F:
        if len(c)!=3 or len({abs(x) for x in c})!=3:return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        if any(abs(x)<1 or abs(x)>n for x in c):return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key);cnt.update(c)
    return all(cnt[i]==2 and cnt[-i]==2 for i in range(1,n+1))
def sat(F,a):
    return all(any(a[abs(v)-1]==int(v>0) for v in c) for c in F)
def rem(F,p):
    out=[]
    for j,c in enumerate(F):
        if any(p[abs(v)-1]==int(v>0) for v in c):continue
        out.append((j,tuple(v for v in c if p[abs(v)-1]<0)))
    return out
def up(F,p):
    p=list(p)
    while True:
        r=rem(F,p)
        if any(not c for _,c in r):return p,r,False
        unit=next((c[0] for _,c in r if len(c)==1),None)
        if unit is None:return p,r,True
        x=abs(unit)-1;b=int(unit>0)
        if p[x]>=0 and p[x]!=b:return p,r,False
        p[x]=b
def bip(r):
    # Union with parity, parity 1 for each monotone original clause edge.
    link={};par={}
    def root(x):
        if x not in link:link[x]=x;par[x]=0
        if link[x]==x:return x,0
        q,d=root(link[x]);par[x]^=d;link[x]=q
        return link[x],par[x]
    for _,c in r:
        assert len(c)==2 and c[0]*c[1]>0
        a,b=abs(c[0]),abs(c[1]);x,px=root(a);y,py=root(b)
        if x==y:
            if (px^py)!=1:return False
        else:link[x]=y;par[x]=1^px^py
    return True
def enumerate_small(F,n):
    assert good(F,n)
    models=[a for a in product((0,1),repeat=n) if sat(F,a)]
    stats=Counter()
    for p in product((-1,0,1),repeat=n):
        extends=any(all(v<0 or v==a[i] for i,v in enumerate(p)) for a in models)
        q,r,ok=up(F,p)
        if not ok:
            assert not extends
            stats['up_conflict']+=1;continue
        stats['stable']+=1
        f=sum(v<0 for v in q);u=len(r)
        r3=sum(len(c)==3 for _,c in r)
        h=4*f-sum(len(c) for _,c in r)
        e=2*f-u
        assert r3+h==2*e and e>=0
        stats['slack_identity_checked']+=1
        if e==0:
            assert r3==h==0 and all(len(c)==2 for _,c in r)
            assert bip(r)==extends
            stats['e0_'+('SAT' if extends else 'UNSAT')]+=1
    assert stats['stable']+stats['up_conflict']==3**n
    return {'n':n,'models':len(models),'states':3**n,**dict(stats)}
def main():
    t=time.monotonic()
    root=Path(__file__).resolve().parents[3]
    raw=(root/'research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt').read_text()
    U=tuple(tuple(c) for c in ast.literal_eval(raw[raw.index('[['):]))
    V=[list(c) for c in U];V[2][2],V[44][2]=V[44][2],V[2][2]
    V=tuple(map(tuple,V))
    assert good(Y,6) and good(Z,9) and good(U,198) and good(V,198)
    assert len(W)==198 and sat(V,tuple(map(int,W)))
    assert not good((Y[0],Y[0])+Y[1:],6)
    out={'status':'PASS','U198_grammar':'PASS (source UNSAT proof in full separate independent archive)',
         'V198_witness':'PASS','Y6':enumerate_small(Y,6),'Z9':enumerate_small(Z,9),
         'source_sha':hashlib.sha256(str(U).encode()).hexdigest(),
         'scope':'FPT residual states, not all-target P, not hereditary FLMV'}
    assert out['Y6']['models']==20 and out['Z9']['models']==74
    assert out['Y6']['e0_SAT']==212 and out['Z9']['e0_UNSAT']==1
    out['elapsed_host_seconds']=round(time.monotonic()-t,3)
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
