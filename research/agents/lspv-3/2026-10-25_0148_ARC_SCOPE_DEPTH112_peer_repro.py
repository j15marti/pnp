#!/usr/bin/env python3
"""Peer mini for ARC-SCOPED-DEPTH-BUDGET112. Restricted promise, not all-input."""
from itertools import product
from functools import lru_cache
import json
import math

def pin(v,b,nextid):
    lit = v if b else -v
    return [(lit, a*nextid, c*(nextid+1))
            for a,c in product((1,-1),repeat=2)]

def profile(clauses):
    intervals={}
    for i,c in enumerate(clauses):
        for lit in c:
            v=abs(lit)
            if v in intervals: intervals[v][1]=i
            else: intervals[v]=[i,i]
    cuts=[tuple(sorted(v for v,(a,b) in intervals.items() if a<j<=b))
          for j in range(len(clauses)+1)]
    return cuts, max((len(x) for x in cuts),default=0)

def sat(clauses):
    @lru_cache(None)
    def rec(cs):
        if not cs: return True
        if any(not x for x in cs): return False
        unit=next((x[0] for x in cs if len(x)==1),None)
        v=unit if unit is not None else cs[0][0]
        def assign(lit):
            return rec(tuple(sorted(tuple(q for q in clause if q!=-lit)
                       for clause in cs if lit not in clause)))
        return assign(v) if unit is not None else assign(v) or assign(-v)
    return rec(tuple(sorted(tuple(x) for x in clauses)))

def child(src,lo,hi,Lbits,Rbits,scopes):
    L=scopes[lo]; R=scopes[hi]
    a=dict(zip(L,Lbits)); b=dict(zip(R,Rbits))
    if any(a[v]!=b[v] for v in set(L)&set(R)): return None
    out=[]; nextid=max(abs(x) for c in src for x in c)+1
    for v in L:
        out+=pin(v,a[v],nextid);nextid+=2
    out+=src[lo:hi]
    for v in R:
        if v not in a:
            out+=pin(v,b[v],nextid);nextid+=2
    ids=sorted({abs(x) for c in out for x in c})
    remap={x:i+1 for i,x in enumerate(ids)}
    cnf=[tuple((1 if x>0 else -1)*remap[abs(x)] for x in c) for c in out]
    assert all(len(c)==3 and len({abs(x) for x in c})==3 for c in cnf)
    return cnf

def parts(m):
    B=min(m,max(2,math.ceil(math.sqrt(m))))
    widths=[m//B+(j<m%B) for j in range(B)]
    p=0;ans=[]
    for size in widths:ans.append((p,p+size));p+=size
    return ans

def scoped(cnf,depth,stats):
    if depth==0 or len(cnf)<4:
        stats['leaf']+=1
        return sat(cnf)
    scopes,w=profile(cnf)
    allowed={()}
    for lo,hi in parts(len(cnf)):
        states=set()
        for a in allowed:
            for b in product((0,1),repeat=len(scopes[hi])):
                ch=child(cnf,lo,hi,a,b,scopes)
                if ch is None: continue
                wc=profile(ch)[1]
                assert wc<=w+2,(wc,w)
                stats['maximum_per_level_width_gain']=max(
                    stats['maximum_per_level_width_gain'],wc-w)
                stats['children']+=1
                if scoped(ch,depth-1,stats):states.add(b)
        allowed=states
        if not allowed: break
    return () in allowed

def eq_path(q,last):
    out=[]; aux=q+1
    for j in range(1,q):
        for c in ((-j,j+1),(j,-(j+1))):
            out+=[(*c,aux),(*c,-aux)];aux+=1
    out+=pin(1,1,aux);aux+=2
    out+=pin(q,last,aux)
    return out

def main():
    result=[]
    for q in (3,4):
        for b in (0,1):
            f=eq_path(q,b)
            st={'children':0,'leaf':0,'maximum_per_level_width_gain':0}
            ans=scoped(f,2,st)
            assert ans==sat(f)==bool(b)
            result.append({'q':q,'end_pin':b,'answer':'SAT' if ans else 'UNSAT',**st})
    print(json.dumps({'status':'COMPUTATIONAL','controls':result,'discrepancies':0},indent=2))

if __name__=='__main__':
    main()
