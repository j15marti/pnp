#!/usr/bin/env python3
"""Independent deterministic one-module exact22 and Pareto controls.

Use: python 2026-10-29_1604_LSPV4_ONE_MODULE_PARETO230_check.py
Standard library, no packages. Finite checks are not SAT lower bounds.
"""
import itertools
import json
import math
from collections import Counter

def formula(r):
    assert r>=2
    A=lambda i: i%r+1
    U=lambda i: r+i%r+1
    V=lambda i: 2*r+i%r+1
    result=[]
    for i in range(r):
        result.extend(((A(i),U(i),V(i)),
                       (A(i),U(i+1),V(i)),
                       (-A(i),-U(i),-V(i)),
                       (-A(i),-U(i+1),-V(i))))
    return result

def source(r):
    c=formula(r)
    return (f"p cnf {3*r} {4*r}\n"+
            "".join(" ".join(map(str,x))+" 0\n" for x in c)).encode("ascii")

def audit(r):
    c=formula(r)
    counts=Counter()
    adj={i:set() for i in range(1,3*r+1)}
    for clause in c:
        assert len({abs(v) for v in clause})==3
        for lit in clause:
            counts[(abs(lit),lit>0)]+=1
        for u,v in itertools.combinations(map(abs,clause),2):
            adj[u].add(v);adj[v].add(u)
    for v in adj:
        assert (counts[v,True],counts[v,False])==(2,2)
    seen={1};stack=[1]
    for u in stack:
        for v in adj[u]:
            if v not in seen:
                seen.add(v);stack.append(v)
    assert len(seen)==3*r
    # Positive clauses have positive U, negative ones negative V:
    # U=1,V=0 works regardless of A.
    for j,cl in enumerate(c):
        if j%4<2:assert any(r<lit<=2*r for lit in cl)
        else:assert any(-3*r<=lit<-2*r for lit in cl)

def q_exact_by_brute(r,Y):
    c=[cl for cl in formula(r) if not any(abs(l) in Y for l in cl)]
    p=[v for v in range(1,3*r+1) if v not in Y]
    for k in range(len(p)+1):
        for h in itertools.combinations(p,k):
            h=set(h)
            if all(any(abs(l) in h for l in cl) for cl in c):
                return k,len(c)
    raise AssertionError("missing hitting set")

def small_controls():
    subsets=0;assignments=0
    for r in (2,3,4):
        audit(r)
        for mask in range(1,(1<<r)):
            Y={i+1 for i in range(r) if mask&(1<<i)}
            b=len(Y)
            q,local=q_exact_by_brute(r,Y)
            assert (q,local)==(r-b,4*(r-b))
            for bits in itertools.product((0,1),repeat=b):
                a={i+1:0 for i in range(r)}
                a.update(dict(zip(sorted(Y),bits)))
                a.update({r+i+1:1 for i in range(r)})
                a.update({2*r+i+1:0 for i in range(r)})
                for cl in formula(r):
                    assert any(a[abs(l)] if l>0 else not a[abs(l)] for l in cl)
                assignments+=1
            subsets+=1
    return subsets,assignments

def balanced_r2():
    r=2;c=[tuple(map(abs,x)) for x in formula(r)]
    occurs={v:[] for v in range(1,7)}
    for j,cl in enumerate(c):
        for i,v in enumerate(cl):occurs[v].append((j,i))
    patterns=list(itertools.combinations(range(4),2))
    masks={(v,True):sum(1<<a for a in range(64) if (a>>(v-1))&1)
           for v in occurs}
    masks.update({(v,False):((1<<64)-1)^masks[v,True] for v in occurs})
    sat=0
    for choices in itertools.product(patterns,repeat=6):
        sign={}
        for v,pattern in enumerate(choices,start=1):
            for j,pos in enumerate(occurs[v]):
                sign[pos]=j in pattern
        alive=(1<<64)-1
        for j,cl in enumerate(c):
            clause=0
            for i,v in enumerate(cl):
                clause|=masks[v,sign[j,i]]
            alive &= clause
            if not alive:break
        if alive:sat+=1
    assert sat==6**6
    return sat

def relaxed(n,b):
    return max(0,(n-3*b+12*b-1)//(12*b))

def pareto(n=1200):
    records=[];best=None;minT=10**9;minB=[]
    for b in range(1,n+1):
        q=relaxed(n,b);t=b+q
        if best is None or t<best:
            records.append([b,q,t,b]);best=t
        if t<minT:minT=t;minB=[b]
        elif t==minT:minB.append(b)
    return {"minimum_time_proxy":minT,"minimizing_b":minB,
            "first_equal_b":next(b for b in range(1,n+1) if relaxed(n,b)==0),
            "nondominated_records":records}

def main():
    subsets,assignments=small_controls()
    cases=[]
    for r in (2,3,4,10,100,400,1000):
        audit(r)
        cases.append([r,3*r,4*r,len(source(r))])
    p=pareto()
    assert p["minimum_time_proxy"]==20
    assert p["minimizing_b"]==[9,10,11]
    assert p["first_equal_b"]==400
    assert [x[0] for x in p["nondominated_records"]]==list(range(1,10))
    assert cases[-2][-1]==25188
    result={"run_id":"ONE-MODULE-PARETO230-GITHUB-CHECK",
            "status":"COMPUTATIONAL finite controls only",
            "exhaustive_Y_subsets":subsets,
            "exhaustive_boundary_assignments":assignments,
            "balanced_r2_SAT":balanced_r2(),
            "balanced_r2_UNSAT":0,
            "canonical_samples_r_n_m_bytes":cases,
            "permitted_n1200":p,
            "theorem_scope":"k=1, residual hitting, Y subset A; q=r-b",
            "general_SAT_conclusion":False}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
