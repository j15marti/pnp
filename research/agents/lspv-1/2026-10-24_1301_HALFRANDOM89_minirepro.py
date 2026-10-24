#!/usr/bin/env python3
"""HALFRANDOM89: self-contained constructive backdoor and octahedral controls.
Run: python research/agents/lspv-1/2026-10-24_1301_HALFRANDOM89_minirepro.py
This compact reproducer does not rerun the expanded 9,410-check audit.
"""
import itertools, collections, json

def evaluate(F, a):
    return all(any(a[abs(l)] == (l > 0) for l in c) for c in F)

def valid(F, n):
    counts = collections.Counter(l for c in F for l in c)
    supports = [tuple(sorted(c)) for c in F]
    return (len(F)*3==4*n and len(set(supports))==len(F)
       and all(len(c)==3 and len({abs(x) for x in c})==3 for c in F)
       and all(counts[v]==counts[-v]==2 for v in range(1,n+1)))

def octa(t):
    F=[];slots=[]
    for i in range(t):
        slots.append({})
        for u,v,w in itertools.product((0,1),repeat=3):
            base=6*i
            F.append([base+1+u if v==w else -(base+1+u),
                      base+3+v if u==w else -(base+3+v),
                      base+5+w if u==v else -(base+5+w)])
            slots[-1][u,v,w]=len(F)-1
    for i in range(t-1):
        a,b=slots[i][0,1,1],slots[i+1][0,0,0]
        assert F[a][0]>0 and F[b][0]>0
        F[a][0],F[b][0]=F[b][0],F[a][0]
    return F

def cover(T):
    V=sorted({abs(l) for c in T for l in c})
    occ={v:[] for v in V}
    for j,c in enumerate(T):
        for l in c:occ[abs(l)].append(j)
    assert all(len(occ[v]) in (2,4) for v in V)
    r2=sum(len(occ[v])==2 for v in V)
    delta=len(T)
    flags=[True]*delta
    q=[3]*delta
    X=set()
    for v in V:
        weight=sum(1 << (3-q[j]) for j in occ[v] if flags[j])
        if weight>4:
            X.add(v)
            for j in occ[v]:flags[j]=False
        else:
            for j in occ[v]:
                if flags[j]:q[j]-=1
    before=len(X)
    for c in T:
        if not any(abs(l) in X for l in c):X.add(abs(c[0]))
    assert all(any(abs(l) in X for l in c) for c in T)
    assert 4*len(X) <= 2*delta+r2
    return X,dict(delta=delta,r2=r2,bound=(2*delta+r2)//4,before=before)

def connected(F,n):
    nb=len(F);g=[[] for _ in range(n+nb)]
    for j,c in enumerate(F):
        for l in c:
            a,b=abs(l)-1,n+j
            g[a].append(b);g[b].append(a)
    seen={0};stack=[0]
    while stack:
        for v in g[stack.pop()]:
            if v not in seen:seen.add(v);stack.append(v)
    return len(seen)==n+nb

def brute_sat(F,n):
    for bits in itertools.product((False,True),repeat=n):
        if evaluate(F,[False]+list(bits)):return True
    return False

def main():
    records=[]
    for t in (1,2,3,4,8,16,32,64):
        F=octa(t)
        assert valid(F,6*t)
        assert connected(F,6*t)
        X,stat=cover(F)
        assert len(X)==2*t
        assert all(any(abs(l) in {6*i+j for i in range(t) for j in (3,4)}
                       for l in c) for c in F)
        # Witness 000011 repeated per block, unaffected by positive a0 swaps.
        a=[False]+([False,False,False,False,True,True]*t)
        assert evaluate(F,a)
        if t<=2:assert brute_sat(F,6*t)
        records.append(dict(t=t,n=6*t,m=8*t,minimum_backdoor=2*t,
                            constructed_backdoor=len(X),bound=stat['bound']))
    print(json.dumps(dict(id='HALFRANDOM89',status='COMPUTATIONAL',
        result='certified constructive upper bound, not all-decider lower bound',
        controls=records,failures=0),indent=2))

if __name__ == '__main__':main()
