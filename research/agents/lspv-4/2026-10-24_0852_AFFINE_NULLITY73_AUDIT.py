#!/usr/bin/env python3
"""Readable mini-auditor for AFFINE-NULLITY-BOUNDARY73.
Full 1,570-check auditor and raw data are in the downloadable research package.
No finite test proves an unrestricted SAT lower bound.
"""
from itertools import product, combinations
from collections import defaultdict

def odd3(a,b,c):
    return [(a,b,c),(a,-b,-c),(-a,b,-c),(-a,-b,c)]

def cycle(q):
    return sorted({tuple(sorted((v,(v+1)%q))) for v in range(q)})

def graph_cnf(q,edges,b=None):
    b={} if b is None else b
    x=lambda v,j:3*v+j+1
    f=[]
    for v in range(q):
        a,d,c=[x(v,j) for j in range(3)]
        f.extend(odd3(a,d,c))
        f.extend([(-a,-d),(-a,-c),(-d,-c)])
    for v,w in edges:
        f.extend([(-x(v,j),-x(w,j)) for j in range(3)])
    for i,(v,bit) in enumerate(sorted(b.items())):
        c=x(v,2)*(1 if bit else -1); u=3*q+i+1
        f.extend([(c,u),(c,-u)])
    return 3*q+len(b),f

def scc_2sat(f,n):
    def idx(x):return 2*(abs(x)-1)+(x<0)
    g=[[] for _ in range(2*n)]
    r=[[] for _ in range(2*n)]
    for c in f:
        assert 1<=len(c)<=2
        a=idx(c[0])
        edges=[(a^1,a)] if len(c)==1 else [(a^1,idx(c[1])),(idx(c[1])^1,a)]
        for u,v in edges:g[u].append(v);r[v].append(u)
    used=[False]*(2*n); order=[]
    for start in range(2*n):
        if used[start]:continue
        used[start]=True; st=[(start,0)]
        while st:
            v,k=st[-1]
            if k<len(g[v]):
                u=g[v][k];st[-1]=(v,k+1)
                if not used[u]:used[u]=True;st.append((u,0))
            else:order.append(v);st.pop()
    co=[-1]*(2*n);k=0
    for v in reversed(order):
        if co[v]!=-1:continue
        co[v]=k; st=[v]
        while st:
            z=st.pop()
            for w in r[z]:
                if co[w]<0:co[w]=k;st.append(w)
        k+=1
    out={}
    for v in range(1,n+1):
        i=2*v-2
        if co[i]==co[i+1]:return None
        out[v]=co[i]>co[i+1]
    return out

def adaptive(f,n):
    seen=defaultdict(int)
    for c in f:
        if len(c)==2:
            a,d=c
            for l,u in ((a,d),(d,a)):
                seen[(l,abs(u))]|=1 if u>0 else 2
    units={l for (l,u),mask in seen.items() if mask==3}
    vals={}
    for l in units:
        if abs(l) in vals and vals[abs(l)]!=(l>0):return None,'conflict'
        vals[abs(l)]=(l>0)
    residual=[]
    for c in f:
        if any(abs(l) in vals and vals[abs(l)]==(l>0) for l in c):continue
        d=tuple(l for l in c if abs(l) not in vals)
        if not d:return None,'conflict'
        residual.append(d)
    if any(len(c)>2 for c in residual):return None,'unhandled_ternary'
    out=scc_2sat(residual,n)
    if out is None:return None,'SCC_UNSAT'
    out.update(vals)
    assert all(any(out[abs(l)]==(l>0) for l in c) for c in f)
    return out,'SCC_SAT'

def main():
    checks=0
    for values in product((0,1),repeat=3):
        a={i+1:bool(values[i]) for i in range(3)}
        f=odd3(1,2,3)
        assert all(any(a[abs(l)]==(l>0) for l in c) for c in f)==(sum(values)%2==1)
        checks+=1
    for q in (3,5,7,9):
        edges=cycle(q);zeros={v:0 for v in range(q)}
        n,base=graph_cnf(q,edges,zeros)
        assert n==4*q and len(base)==12*q
        sol,route=adaptive(base,n)
        assert sol is None and route=='SCC_UNSAT'
        checks+=2
        for v in range(q):
            b={**zeros,v:1};n2,f=graph_cnf(q,edges,b)
            sol,how=adaptive(f,n2)
            changes=sum(a!=d for c,e in zip(base,f) for a,d in zip(c,e))
            assert n2==n and len(f)==len(base) and changes==2
            assert sol is not None and how=='SCC_SAT'
            checks+=2
    for edges in (cycle(3),list(combinations(range(4),2))):
        q=max(v for e in edges for v in e)+1
        _,f=graph_cnf(q,edges)
        actual=sum(all(t[u]!=t[v] for u,v in edges) for t in product(range(3),repeat=q))
        assert (actual>0)==(q==3)
        assert sum(len(c)==3 for c in f)==4*q
        assert all(sum(l>0 for l in c)==0 for c in f if len(c)==2)
        checks+=3
    print({'checks':checks,'failures':0,'status':'COMPUTATIONAL'})

if __name__=='__main__':main()
