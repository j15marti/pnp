#!/usr/bin/env python3
"""ARC228 independent fixed-codimension 2-SUB-SAT solver.
Clauses: signed nonzero 1-based ints, length 1 or 2.
Affine rows: (mask, rhs) over GF(2).
This is a reconstruction of known Arvind--Guruswami IPEC 2021 techniques.
Not a general polynomial SAT algorithm, no NP-completeness claim.
"""
from itertools import product
from collections import Counter
from pathlib import Path
import json,random,sys,time

def sat_clauses(cls,a):
    return all(any(a[abs(l)-1]==int(l>0) for l in c) for c in cls)

def sat_eqs(eqs,a):
    mask=sum(int(v)<<i for i,v in enumerate(a))
    return all(((mask&m).bit_count()%2)==b for m,b in eqs)

def scc_graph(n,cls):
    g=[[] for _ in range(2*n)]; r=[[] for _ in range(2*n)]
    def ix(l):return 2*(abs(l)-1)+(l<0)
    for c in cls:
        if not c:return None
        if len(c)>2:raise ValueError('not 2CNF')
        a,b=c[0],c[-1]
        for x,y in ((-a,b),(-b,a)):
            i,j=ix(x),ix(y);g[i].append(j);r[j].append(i)
    vis=[0]*(2*n);order=[]
    for start in range(2*n):
        if vis[start]:continue
        vis[start]=1; st=[(start,0)]
        while st:
            v,k=st[-1]
            if k<len(g[v]):
                w=g[v][k]; st[-1]=(v,k+1)
                if not vis[w]:vis[w]=1;st.append((w,0))
            else:order.append(v);st.pop()
    comp=[-1]*(2*n);num=0
    for start in reversed(order):
        if comp[start]>=0:continue
        comp[start]=num;st=[start]
        while st:
            v=st.pop()
            for w in r[v]:
                if comp[w]<0:comp[w]=num;st.append(w)
        num+=1
    if any(comp[2*i]==comp[2*i+1] for i in range(n)):return None
    return comp

def solve_2sat(n,cls):
    comp=scc_graph(n,cls)
    if comp is None:return None
    return tuple(int(comp[2*i]>comp[2*i+1]) for i in range(n))

def compress(n,cls,eqs,stats):
    comp=scc_graph(n,cls)
    if comp is None:return None
    pairs={}; mapping=[]
    for i in range(n):
        a,b=comp[2*i],comp[2*i+1];key=min(a,b)
        if key not in pairs:pairs[key]=len(pairs)
        mapping.append((pairs[key],int(a!=key)))
    m=len(pairs);newcls=[]
    for c in cls:
        out=set()
        for lit in c:
            j,flip=mapping[abs(lit)-1]
            sign=(lit>0)^bool(flip)
            out.add((j+1) if sign else -(j+1))
        if any(-l in out for l in out):continue
        newcls.append(tuple(sorted(out)))
    neweq=[]
    for mask,rhs in eqs:
        newmask=0
        for i in range(n):
            if mask>>i&1:
                j,flip=mapping[i];newmask^=1<<j;rhs^=flip
        if newmask==0:
            if rhs:return None
        else:neweq.append((newmask,rhs))
    stats['compress_calls']+=1
    return m,newcls,neweq,mapping

def pluck(n,cls,eqs,v):
    idx=next((j for j,(m,b) in enumerate(eqs) if m>>v&1),None)
    assert idx is not None
    pivotmask,pivotrhs=eqs[idx];keep=[i for i in range(n) if i!=v]
    def drop(mask):
        return sum(((mask>>i)&1)<<j for j,i in enumerate(keep))
    neweq=[]
    for j,(mask,rhs) in enumerate(eqs):
        if j==idx:continue
        if mask>>v&1:mask^=pivotmask;rhs^=pivotrhs
        mm=drop(mask)
        if not mm:
            if rhs:return None
        else:neweq.append((mm,rhs))
    newcls=[]
    for c in cls:
        out=[]
        for lit in c:
            i=abs(lit)-1
            if i==v:continue
            j=i-int(i>v)
            out.append((j+1) if lit>0 else -(j+1))
        if not out:return None
        newcls.append(tuple(out))
    return n-1,newcls,neweq,(pivotmask,pivotrhs,keep)

def fixed_codim_solver(n,cls,eqs,stats=None):
    """Deterministic <= n^rank nodes, plus polynomial SCC/row work per node."""
    if stats is None:stats=Counter()
    originalcls=tuple(tuple(c) for c in cls)
    originale=tuple(tuple(e) for e in eqs)
    def dfs(n,cls,eqs):
        stats['nodes']+=1
        q=compress(n,cls,eqs,stats)
        if q is None:return None
        m,C,E,mapping=q
        base=solve_2sat(m,C)
        if base is None:return None
        if sat_eqs(E,base):
            stats['base_hits']+=1
            return tuple(base[j]^flip for j,flip in mapping)
        for v in range(m):
            if not any(mask>>v&1 for mask,rhs in E):continue
            stats['plucks_tried']+=1
            p=pluck(m,C,E,v)
            if p is None:continue
            nn,cc,ee,(mask,rhs,keep)=p
            w=dfs(nn,cc,ee)
            if w is None:continue
            val=rhs
            for j,i in enumerate(keep):
                if mask>>i&1:val^=w[j]
            result=[None]*m
            for j,i in enumerate(keep):result[i]=w[j]
            result[v]=val
            assert sat_clauses(C,result) and sat_eqs(E,result)
            return tuple(result[j]^flip for j,flip in mapping)
        return None
    sol=dfs(n,cls,eqs)
    if sol is not None:
        assert sat_clauses(originalcls,sol) and sat_eqs(originale,sol)
        stats['source_verified']+=1
    return sol

def brute(n,cls,eqs):
    for a in product((0,1),repeat=n):
        if sat_clauses(cls,a) and sat_eqs(eqs,a):return a
    return None

def rand_case(rng,n,count,e):
    C=[]
    for j in range(count):
        vs=rng.sample(range(n),rng.randrange(1,min(2,n)+1))
        C.append(tuple((v+1)*(1 if rng.randrange(2) else -1) for v in vs))
    E=[(rng.randrange(1,1<<n),rng.randrange(2)) for i in range(e)]
    return C,E

def main():
    rng=random.Random(2282026)
    data={'seed':2282026,'tests':0,'SAT':0,'UNSAT':0,'mismatches':0}
    stats=Counter()
    for n in range(1,9):
        for e in range(min(n,3)+1):
            for repeat in range(100):
                C,E=rand_case(rng,n,rng.randrange(0,3*n+1),e)
                want=brute(n,C,E)
                got=fixed_codim_solver(n,C,E,stats)
                assert (want is None)==(got is None),(n,e,C,E,want,got)
                data['tests']+=1
                data['SAT']+=want is not None;data['UNSAT']+=want is None
    data['stats']=dict(stats)
    print(json.dumps(data,indent=2))
if __name__=='__main__':main()
