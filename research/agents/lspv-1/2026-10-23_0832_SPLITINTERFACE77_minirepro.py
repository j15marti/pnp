#!/usr/bin/env python3
"""SPLITINTERFACE77 reproducibility, Python 3 standard library only.
Run from the repository root:
python research/agents/lspv-1/2026-10-23_0832_SPLITINTERFACE77_minirepro.py
Tests the original Role-2 Doecker source without claiming a fresh UNSAT proof.
"""
import ast, json, hashlib
from collections import Counter
from itertools import product
from pathlib import Path

SOURCE=Path("research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt")

def valid(src):
    n=max(abs(x) for c in src for x in c)
    counts=Counter(x for c in src for x in c)
    assert n >= 3 and len(src)*3 == 4*n
    assert len(set(tuple(sorted(c)) for c in src)) == len(src)
    assert all(len(c)==3 and len({abs(v) for v in c})==3 for c in src)
    assert all(counts[i]==2 and counts[-i]==2 for i in range(1,n+1))
    return n

def vid(i,t):
    return 4*(i-1)+{"a":1,"b":2,"p":3,"q":4}[t]

def lift(src):
    n=valid(src)
    T=[tuple(-vid(abs(x),"a" if x>0 else "b") for x in c) for c in src]
    tgt=list(T)
    for i in range(1,n+1):
        a,b,p,q=(vid(i,t) for t in ("a","b","p","q"))
        prev=vid(n if i==1 else i-1,"q")
        tgt.extend([(a,b,p),(a,b,-p),(prev,-q,p),(prev,-q,-p)])
    return n,T,tgt

def audit(src):
    n,T,tgt=lift(src)
    assert len(tgt)==len(src)+4*n
    count=Counter(x for c in tgt for x in c)
    assert all(count[i]==count[-i]==2 for i in range(1,4*n+1))
    assert all(len({abs(x) for x in c})==3 for c in tgt)
    clauses={tuple(sorted(c)):i for i,c in enumerate(tgt)}
    assert len(clauses)==len(tgt)
    paired=set()
    for j,c in enumerate(tgt):
        partners=[]
        for r in range(3):
            d=list(c);d[r]=-d[r]
            if tuple(sorted(d)) in clauses:
                partners.append(clauses[tuple(sorted(d))])
        assert len(partners)<=1
        if partners:paired.add(j)
    assert len(paired)==4*n
    assert all(j not in paired for j in range(len(src)))
    neg_counts=Counter(x for c in T for x in c)
    assert len(neg_counts)==2*n and all(x<0 and y==2 for x,y in neg_counts.items())
    parent=list(range(4*n+1))
    def find(a):
        while a!=parent[a]:
            parent[a]=parent[parent[a]];a=parent[a]
        return a
    for c in tgt:
        u=find(abs(c[0]))
        for x in c[1:]:parent[find(abs(x))]=u
    assert len({find(j) for j in range(1,4*n+1)})==1
    return {"source_n":n,"source_m":len(src),"target_n":4*n,"target_m":len(tgt),
            "complementary_pairs":len(paired)//2,
            "unmatched_ternaries":len(tgt)-len(paired),
            "disjoint_projected_binary":n,
            "kernel_clauses":len(src)+n,
            "all_negative_residual":True,"all_residual_signed_counts_two":True,
            "connected":True}

def eval_cnf(src,a):
    return all(any(a[abs(x)-1] == (x>0) for x in c) for c in src)

def eval_kernel(src,ab):
    a=[x for x,y in ab];b=[y for x,y in ab]
    if not all(x or y for x,y in ab):return False
    return all(any((not a[abs(x)-1]) if x>0 else (not b[abs(x)-1])
                   for x in c) for c in src)

def hg(g):
    F=[]
    for j in range(g):
        x,y,z=3*j+1,3*j+2,3*j+3
        zp=3*((j+1)%g)+3
        F.extend([(x,-y,z),(x,-y,-z),(-x,y,zp),(-x,y,-zp)])
    return F

def main():
    raw=SOURCE.read_text(encoding="utf8")
    src=ast.literal_eval(raw[raw.index("[["):])
    result=audit(src)
    result["source_blob_sha256"]=hashlib.sha256(raw.encode()).hexdigest()
    source_small=hg(2)
    result["small_source"]=audit(source_small)
    source_sat=any(eval_cnf(source_small,vals) for vals in product((False,True),repeat=6))
    kernel_sat=any(eval_kernel(source_small,ab) for ab in product(((0,1),(1,0),(1,1)),repeat=6))
    assert source_sat==kernel_sat==True
    result["small_exact_SAT_equivalence"]=True
    result["major_failures"]=0
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=="__main__":main()
