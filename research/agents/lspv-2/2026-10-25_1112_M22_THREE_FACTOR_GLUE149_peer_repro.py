#!/usr/bin/env python3
"""Peer reproduction for M22-THREE-FACTOR-GLUE149.
Run from the root of a clone of j15marti/pnp:
  python research/agents/lspv-2/2026-10-25_1112_M22_THREE_FACTOR_GLUE149_peer_repro.py
The U UNSAT label is imported from D\"ocker 1912.08032, not proven by this script.
All measured lengths are ordinary indexed encoding bits, not FLMV TM steps.
"""
import ast
import json
import math
from pathlib import Path
from collections import Counter
from itertools import product

UPATH=Path("research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt")
P=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
Q=((1,2,4),(1,3,6),(2,3,5),(4,5,6))

def source(p,q):
    return tuple(p)+tuple(tuple(-v for v in c) for c in q)

def valid(F):
    if any(len(c)!=3 or len({abs(v) for v in c})!=3 or
           (not all(v>0 for v in c) and not all(v<0 for v in c))
           for c in F):return False,False,0
    signs=Counter(); pos=set(); neg=set(); keys=set()
    for c in F:
        ss=tuple(sorted(abs(v) for v in c))
        k=(c[0]>0,ss)
        if k in keys:return False,False,0
        keys.add(k)
        (pos if c[0]>0 else neg).add(ss)
        for v in c:signs[(abs(v),v>0)]+=1
    ids={v for v,sgn in signs}
    if ids!=set(range(1,len(ids)+1)) or any(signs[v,pol]!=2 for v in ids for pol in (True,False)):
        return False,False,0
    return True,(pos!=neg),len(ids)

def Z(h):
    def six(j):return tuple(6*(j%h)+a for a in range(1,7))
    F=[]
    for j in range(h):
        a,b,c,d,e,f=six(j); nxt=six(j+1)[0]
        F+= [(nxt,b,c),(a,d,e),(b,d,f),(c,e,f),
             (-a,-b,-d),(-a,-c,-f),(-b,-c,-e),(-d,-e,-f)]
    return tuple(F)

def split(F,k):
    A=tuple(tuple(k+v for v in c) for c in F if c[0]>0)
    B=tuple(c for c in F if c[0]<0)
    I=tuple((-(k+j),j) for j in range(1,k+1))
    return A,B,I

def yes(F,values):
    return all(any((bool(values[abs(lit)-1]) if lit>0 else not values[abs(lit)-1])
                   for lit in c) for c in F)

def encode(F,n):
    M=len(F); w=(64*(n+M+1)-1).bit_length()
    words=[n,M]
    for c in F:
        words.extend([len(c)]+[(abs(lit)<<1)|int(lit<0) for lit in c]+[0]*(3-len(c)))
    assert len(words)==4*M+2 and all(0<=x<2**w for x in words)
    return "".join(format(x,f"0{w}b") for x in words)

def connected(F,n):
    edges=[set() for _ in range(n+1)]
    for c in F:
        a,b,d=map(abs,c)
        for x,y in ((a,b),(b,d),(a,d)):
            edges[x].add(y);edges[y].add(x)
    stack=[1]; seen={1}
    while stack:
        for v in edges[stack.pop()]:
            if v not in seen: seen.add(v);stack.append(v)
    return len(seen)==n

def compute(name,F,want,full=False):
    ok,nonpaired,k=valid(F)
    assert ok and nonpaired, name
    A,B,I=split(F,k);G=A+B+I
    assert len(A)==len(B)==2*k//3 and len(I)==k and len(G)==7*k//3
    degree=Counter(abs(l) for c in G for l in c)
    assert len(degree)==2*k and set(degree.values())=={3}
    ab=[False]*k+[True]*k
    ai=[True]*(2*k);bi=[False]*(2*k)
    assert yes(A+B,ab) and yes(A+I,ai) and yes(B+I,bi)
    lens={label:len(encode(child,n)) for label,child,n in
          (("F",F,k),("G",G,2*k),("A",A,2*k),("B",B,2*k),("I",I,2*k),
           ("AB",A+B,2*k),("AI",A+I,2*k),("BI",B+I,2*k))}
    p={tuple(sorted(map(abs,c))) for c in F if c[0]>0}
    q={tuple(sorted(map(abs,c))) for c in F if c[0]<0}
    record={"name":name,"label":want,"k":k,"m":len(F),"q":len(p-q),
            "connected":connected(F,k),"pairwise_sat":(True,True,True),
            "factor_lengths":lens,"G_all_variables_degree":3,
            "materialized_three_factor_bits":lens["A"]+lens["B"]+lens["I"],
            "TM_work_space_flips_bit_time":"UNMEASURED"}
    if full:
        source_count=sum(yes(F,x) for x in product((False,True),repeat=k))
        expanded_count=0
        for bits in product((False,True),repeat=2*k):
            if yes(G,bits):
                expanded_count+=1
                assert yes(F,bits[:k])
        assert source_count==20 and expanded_count==44
        record["source_models"]=source_count;record["image_models"]=expanded_count
    else:
        record["label_evidence"]="Döcker published UNSAT" if want=="UNSAT" else "explicit repeated witness"
    return record

def main():
    raw=UPATH.read_text(encoding="utf-8")
    U=ast.literal_eval(raw[raw.index("[["):])
    Y=source(P,Q);Z33=Z(33)
    results=[compute("Y",Y,"SAT",True),compute("U",U,"UNSAT"),compute("Z33",Z33,"SAT")]
    assert results[1]["connected"] and results[2]["connected"]
    assert results[1]["q"]==results[2]["q"]==132
    assert results[1]["factor_lengths"]==results[2]["factor_lengths"]
    assert yes(Z33, tuple(t for _ in range(33) for t in (True,True,True,False,False,False)))
    pair=source(P,P)
    assert valid(pair)==(True,False,6) and sum(yes(pair,x) for x in product((False,True),repeat=6))==18
    assert not valid(Y[:-1]+((1,-2,3),))[0]
    print(json.dumps({"run":"M22-THREE-FACTOR-GLUE149","results":results,
      "outside_target_paired_sat":True,"invalid_mixed_clause_rejected":True,
      "U_UNSAT_independent_check":"NOT DONE","ARC_EDGE_90":"OPEN","DIRECT_POST":"OPEN",
      "P_versus_NP":"OPEN"},indent=2,sort_keys=True))
if __name__=="__main__":
    main()
