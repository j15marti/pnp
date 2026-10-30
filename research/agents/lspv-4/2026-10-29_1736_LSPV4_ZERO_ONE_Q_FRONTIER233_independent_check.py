#!/usr/bin/env python3
"""Independent exact22 q=0,1 endpoint source checks. Python 3 stdlib."""
import itertools,json
from collections import defaultdict

def source(b,q):
    assert b>=1 and q in (0,1)
    c=[]; Y=set(range(b)); mods=[]
    def put(*args):c.append(tuple(args))
    if q==0:
        U=[b+i for i in range(b)]
        V=[2*b+i for i in range(b)]
        mods=[set(U+V)]
        for i in range(b):
            put((i,1),(U[i],1),(V[i],0))
            put((i,0),(U[i],1),(V[(i-1)%b],0))
            put((i,1),(U[(i+1)%b],0),(V[i],1))
            put((i,0),(U[(i+1)%b],0),(V[(i-1)%b],1))
        n=3*b
    else:
        n=9*b
        for i in range(b):
            for rep in range(2):
                w,u,v,z=[b+4*(2*i+rep)+r for r in range(4)]
                mods.append({w,u,v,z})
                put((w,1),(u,1),(v,0))
                put((w,0),(u,0),(v,1))
                put((w,1),(u,1),(z,0))
                put((w,0),(u,0),(z,1))
                put((i,None),(v,1),(z,0))
                put(((i+1)%b,None),(v,0),(z,1))
        counters=defaultdict(int);tmp=[]
        for clause in c:
            cc=[]
            for x,s in clause:
                if s is None:s=int(counters[x]<2);counters[x]+=1
                cc.append((x,s))
            tmp.append(tuple(cc))
        c=tmp
        assert all(counters[i]==4 for i in range(b))
    return n,Y,mods,c

def check(b,q):
    n,Y,mods,c=source(b,q)
    assert len(c)==4*n//3
    deg=[[0,0] for _ in range(n)]
    adj=[set() for _ in range(n)]
    codes=set();owner={v:i for i,m in enumerate(mods) for v in m}
    assert len(owner)==n-b
    for clause in c:
        vs=[v for v,s in clause]
        assert len(set(vs))==3
        key=tuple(sorted(clause))
        assert key not in codes;codes.add(key)
        assert len({owner[v] for v in vs if v not in Y})<=1
        for v,s in clause:deg[v][s]+=1
        for u,v in itertools.combinations(vs,2):
            adj[u].add(v);adj[v].add(u)
    assert all(pair==[2,2] for pair in deg)
    def connected(start,allowed):
        seen={start};todo=[start]
        for v in todo:
            for u in adj[v]&allowed:
                if u not in seen:seen.add(u);todo.append(u)
        return seen==allowed
    assert connected(0,set(range(n)))
    assert all(connected(next(iter(M)),M) for M in mods)
    for M in mods:
        internal=[{v for v,s in C} for C in c if all(v not in Y for v,s in C) and any(v in M for v,s in C)]
        if q==0:assert not internal
        else:
            assert internal
            assert any(all(w in C for C in internal) for w in M)
    for mask in range((1<<b) if b<=8 else 1):
        a=[1]*n
        for i in range(b):a[i]=(mask>>i)&1
        assert all(any(a[v]==s for v,s in C) for C in c)
    return dict(b=b,q=q,n=n,m=len(c),k=len(mods),strict22=True)

def qmin(n,b):
    if 3*b>=n:return 0
    return max(1,(n+3+9*b+2)//(9*b+3))
def main():
    checks=[check(b,q) for q in (0,1) for b in range(1,33)]
    checks.extend([check(400,0),check(134,1)])
    fronts={}
    for n in (3,9,21,36,900,1200,2700):
        vals=[(b,qmin(n,b)) for b in range(1,(n+2)//3+1)]
        best=min(b+q for b,q in vals)
        fronts[str(n)]=dict(best_t=best,argmin=[(b,q) for b,q in vals if b+q==best],
                             first_q0_b=(n+2)//3,first_q1_b=(n+8)//9)
    assert fronts['1200']['best_t']==23
    print(json.dumps(dict(cases=checks,frontiers=fronts),sort_keys=True,indent=2))
if __name__=='__main__':main()
