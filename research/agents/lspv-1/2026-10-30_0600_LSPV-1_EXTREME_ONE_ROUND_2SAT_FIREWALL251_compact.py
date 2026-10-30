#!/usr/bin/env python3
"""LSPV-1 EXTREME251 standalone strict22 source-indexed certificate; Python 3 stdlib."""
from itertools import product
F=[(6,2,-4),(3,2,-6),(4,-5,-1),(5,4,3),
   (-3,-6,-1),(1,5,-2),(-4,6,-5),(-2,-3,1)]
n=6
def truth(C,a):return sum(a[abs(l)]==(l>0) for l in C)
def target(C,s):return {abs(l):int((l>0)==(s=='S')) for l in C}
def mode(C,D,ss):
    p,q=target(C,ss[0]),target(D,ss[1])
    return all(k not in q or v==q[k] for k,v in p.items())
def resolvent(C,D,x):
    p,q=set(C),set(D)
    if x not in p:p,q=q,p
    assert x in p and -x in q
    out=(p-{x})|(q-{-x})
    assert not any(-z in out for z in out)
    return tuple(sorted(out,key=lambda z:(abs(z),z)))
def all_a():
    return [{i:b[i-1] for i in range(1,n+1)}
            for b in product((0,1),repeat=n)]
def original_up(p):
    p=dict(p)
    while True:
        change=False
        for C in F:
            if any((l>0)==p[abs(l)] for l in C if abs(l) in p):continue
            R=tuple(l for l in C if abs(l) not in p)
            if not R:return None
            if len(R)==1:
                l=R[0];v=abs(l);val=int(l>0)
                if v in p and p[v]!=val:return None
                if v not in p:p[v]=val;change=True
        if not change:return p
def first_gen():
    out=[]
    for v in range(1,n+1):
        for j,C in enumerate(F):
            if v not in C:continue
            for k,D in enumerate(F):
                if -v not in D:continue
                overlap=set(map(abs,C))&set(map(abs,D))
                if not any(u!=v and (u in C)==(u in D) for u in overlap):continue
                try:R=resolvent(C,D,v)
                except AssertionError:continue
                out.append((j,k,v,R))
    assert len(out)<=4*n
    return out
def binary_closure(p):
    p=dict(p)
    while True:
        p=original_up(p)
        if p is None:return None
        B=[]
        for C in F:
            if any((l>0)==p[abs(l)] for l in C if abs(l) in p):continue
            R=tuple(l for l in C if abs(l) not in p)
            if len(R)<=2:B.append(R)
        free=[v for v in range(1,n+1) if v not in p]
        models=[]
        for bits in product((0,1),repeat=len(free)):
            a=dict(p);a.update(dict(zip(free,bits)))
            if all(truth(C,a)>0 for C in B):models.append(a)
        if not models:return None
        forced={v:models[0][v] for v in free
                if all(a[v]==models[0][v] for a in models)}
        if not forced:return p
        p.update(forced)

def main():
    assert len(F)==8
    for v in range(1,n+1):
        assert sum(v in C for C in F)==sum(-v in C for C in F)==2
    A=all_a()
    for j,C in enumerate(F):
        assert target(C,'S')=={v:1-u for v,u in target(C,'U').items()}
        for k,D in enumerate(F):
            if k<=j:continue
            common=set(map(abs,C))&set(map(abs,D))
            same={v for v in common if (v in C)==(v in D)}
            opposite=common-same
            for ss in ('SS','SU','US','UU'):
                v=not(opposite if ss in ('SS','UU') else same)
                assert mode(C,D,ss)==v
                assert v==any(truth(C,a)==(3 if ss[0]=='S' else 0)
                      and truth(D,a)==(3 if ss[1]=='S' else 0) for a in A)
    for a in A:
        b={i:1-a[i] for i in a}
        assert all(truth(C,a)+truth(C,b)==3 for C in F)
        assert [sum(truth(C,a)==r for C in F) for r in range(4)]==[
                sum(truth(C,b)==3-r for C in F) for r in range(4)]
    for origin in (0,1):
        a={i:origin for i in range(1,n+1)}
        for flips in ((),(1,),(1,2),(1,3,5),(1,2,3,4,5,6)):
            b=dict(a)
            for i in flips:b[i]=1-b[i]
            for C in F:
                t=truth(C,a)
                delta=sum(1 if a[abs(l)]!=(l>0) else -1
                          for l in C if abs(l) in flips)
                assert truth(C,b)==t+delta
    G=first_gen()
    R1=resolvent(F[1],F[4],3)
    R2=resolvent(F[0],R1,6)
    assert set(R1)=={-1,2,-6} and set(R2)=={-1,2,-4}
    assert any(set(R)==set(R1) for _,_,_,R in G)
    rho={1:1,4:1}
    assert original_up(rho)==rho and binary_closure(rho)==rho
    for j,k,v,R in G:
        assert not any(-l in R for l in R)
        assert set(R)==set(resolvent(F[j],F[k],v))
        assert all(truth(R,a)>0 for a in A if all(truth(C,a)>0 for C in F))
    conditioned=[a for a in A
                 if all(a[v]==x for v,x in rho.items())
                 and all(truth(C,a)>0 for C in F)]
    assert len(conditioned)==4 and all(a[2]==1 for a in conditioned)
    assert original_up({1:1,4:1,2:0}) is None
    assert sum(all(truth(C,a)>0 for C in F) for a in A)==16
    print('PASS: 8 original source targets; 28 four-mode matrices; coherent endpoints/complements/flips')
    print('PASS: source-parent resolution R1, mixed one-round and binary closure firewall')
    print('PASS: strict22 R2 forces x2=1, 16 SAT models, 4 models conditioned on rho')
if __name__=='__main__':main()
