#!/usr/bin/env python3
"""Standalone exact structural reproducer for QUOTIENT-PIVOT-SWITCH71."""
from itertools import product

def source(q,bits,z,u,v):
    f=[(z[0],u),(z[0],-u),(-z[q],v),(-z[q],-v)]
    f += [(-z[i-1],z[i] if bits[i-1] else -z[i])
          for i in range(1,q+1)]
    return f

def build(q,bits0,bits1):
    n0=2*q+7;x=n0;n=n0;B=[];T=[]
    for a,bits in enumerate((bits0,bits1)):
        start=1+a*(q+3)
        z=list(range(start,start+q+1))
        u,v=start+q+1,start+q+2
        for l1,l2 in source(q,bits,z,u,v):
            p,c1,c2=n+1,n+2,n+3
            n+=3
            for c,lit in ((c1,l1),(c2,l2)):
                v=abs(lit)
                B.extend(((-c,v),(c,-v)))
            if a==0:B.extend(((-p,x),(p,-x)))
            else:B.extend(((p,x),(-p,-x)))
            T.append((p,c1 if l1>0 else -c1,
                       c2 if l2>0 else -c2))
    return n,x,B,T

def scc(n,clauses):
    g=[[] for _ in range(2*n)]
    r=[[] for _ in range(2*n)]
    ix=lambda v:2*(abs(v)-1)+(v<0)
    for a,b in clauses:
        for u,v in ((-a,b),(-b,a)):
            i,j=ix(u),ix(v)
            g[i].append(j);r[j].append(i)
    used=set();order=[]
    def dfs(root,graph,seen,finish=None):
        stack=[(root,0)];seen.add(root)
        while stack:
            u,i=stack[-1]
            if i<len(graph[u]):
                v=graph[u][i];stack[-1]=(u,i+1)
                if v not in seen:
                    seen.add(v);stack.append((v,0))
            else:
                stack.pop()
                if finish is not None:finish.append(u)
    for v in range(2*n):
        if v not in used:dfs(v,g,used,order)
    comp=[-1]*(2*n);cid=0
    for v in reversed(order):
        if comp[v]>=0:continue
        seen=set();dfs(v,r,seen)
        for w in seen:comp[w]=cid
        cid+=1
    return comp

def chain_sat(bits):
    dp=[0,1]
    for bit in bits:
        a,b=dp
        dp=[a+(b if bit==0 else 0),
            a+(b if bit==1 else 0)]
    return dp[0]>0

def analyze(q,b0,b1):
    n,x,B,T=build(q,b0,b1)
    k=len(T)
    assert n==8*q+31 and len(B)==12*(q+4)
    assert k==2*(q+4)
    assert len({abs(l) for c in T for l in c})==3*k
    comp=scc(n,B)
    assert all(comp[2*i]!=comp[2*i+1] for i in range(n))
    best={}
    for v in range(1,n+1):
        for sign in (1,-1):
            lit=sign*v
            cid=comp[2*(v-1)+(sign<0)]
            if cid not in best or abs(lit)<abs(best[cid]):
                best[cid]=lit
    Q=[tuple(best[comp[2*(abs(l)-1)+(l<0)]] for l in c)
       for c in T]
    assert all(len(set(map(abs,c)))==3 for c in Q)
    common=set(map(abs,Q[0]))
    for c in Q:common.intersection_update(map(abs,c))
    assert common=={x}
    # Each branch reduces every quotient ternary to a clause
    # satisfied or containing no more than two remaining literals.
    for bit in (0,1):
        assert all(any(abs(l)==x and (l>0)==bool(bit) for l in c)
                   or sum(abs(l)!=x for l in c)<=2 for c in Q)
    return chain_sat(b0) or chain_sat(b1)

def main():
    checks=0
    for q in range(1,5):
        for b0 in product((0,1),repeat=q):
            for b1 in product((0,1),repeat=q):
                assert analyze(q,b0,b1)==(
                    b0!=(1,)*q or b1!=(1,)*q)
                checks+=1
    for q in (8,16,64,256,1024):
        for b0 in ((1,)*q,(0,)+(1,)*(q-1)):
            assert analyze(q,b0,(1,)*q)==(b0[0]==0)
            checks+=1
    print({"run":"QUOTIENT-PIVOT-SWITCH71",
           "checks":checks,"failures":0,
           "largest_q":1024,"P_vs_NP":"OPEN"})

if __name__=="__main__":
    main()
