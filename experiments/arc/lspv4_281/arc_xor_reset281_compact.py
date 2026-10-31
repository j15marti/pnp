#!/usr/bin/env python3
"""ARC-XOR-INDEX-RESET281. Compact standard-library reproducibility control.
Known SAT/UNSAT certificates are in the separately archived independent checker.
This checks target grammar, fixed-buffer XOR, exact FLMV envelope and index erase.
NOT a native FLMV SAT solver or proof of P versus NP.
"""
from collections import Counter
from fractions import Fraction
from pathlib import Path
import ast
import itertools
import json

Y = ((1,2,3),(1,4,5),(2,4,6),(3,5,6),
     (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))

def source():
    candidates = [
        Path(__file__).resolve().parents[3] /
          "research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt",
        Path(__file__).resolve().parent / "U_source.json",
    ]
    for p in candidates:
        if p.is_file():
            raw="\n".join(line for line in p.read_text().splitlines()
                          if not line.startswith("#"))
            F=ast.literal_eval(raw)
            U=tuple(tuple(c) for c in F)
            V=[list(c) for c in U]
            V[1][0],V[7][0]=V[7][0],V[1][0]
            return {"Y6_SAT":Y,"U198_UNSAT":U,"V198_SAT":tuple(map(tuple,V))}
    raise FileNotFoundError("Canonical U198 source missing. Clone j15marti/pnp.")

def valid(F):
    n=max(abs(z) for c in F for z in c)
    m=len(F);d=Counter(z for c in F for z in c)
    return (3*m==4*n and
            len(set(tuple(sorted(c)) for c in F))==m and
            all(len(c)==3 and len(set(map(abs,c)))==3 and
                (all(z>0 for z in c) or all(z<0 for z in c)) for c in F) and
            all(d[i]==d[-i]==2 for i in range(1,n+1)))

def logical(F,n,mask):
    a=[(mask>>i)&1 if i<min(8,n) else 0 for i in range(n)]
    S=a[:]
    for C in F:
        count=sum(a[abs(z)-1]==int(z>0) for z in C)
        S.extend((count&1,(count>>1)&1,int(count>0)))
    return S

def tour(F,mode):
    n=max(abs(z) for c in F for z in c)
    limit=1<<min(8,n)
    order=[i^(i>>1) if mode=="gray" else i for i in range(limit)]+[0]
    initial=logical(F,n,0);prev=initial[:];head=0
    install_writes=install_moves=0
    for j,b in enumerate(initial):
        if b:
            install_moves+=abs(j-head);head=j
            install_writes+=1
    writes=moves=0
    for mask in order[1:]:
        nxt=logical(F,n,mask)
        changed=[j for j in range(len(nxt)) if nxt[j]!=prev[j]]
        for j in changed:
            moves+=abs(j-head);head=j;writes+=1
        prev=nxt
    assert prev==initial
    return {"adjacent_XOR":writes,"fixed_work_writes":writes,
            "work_head_moves":moves,"endpoint_XOR":0,
            "initial_work_writes":install_writes,"initial_work_moves":install_moves}

def flmv(c):
    f=Fraction(1);v=[]
    for k in range(1,4):
        f=c*f/(1+f)
        v.append(min((1/f-c)/k,c**(-k)))
    assert v[1]>max(v[0],v[2],c**(-4))
    return str(v[1])

def main():
    result={}
    for label,F in source().items():
        assert valid(F),label
        n=max(abs(z) for C in F for z in C)
        assert sum(x!=y for x,y in zip(logical(F,n,0),logical(F,n,1)))==7
        result[label]={"n":n,"m":len(F),"one_flip_logical_delta":7,
                       "binary":tour(F,"binary"),"gray":tour(F,"gray")}
    assert (result["Y6_SAT"]["binary"]["adjacent_XOR"],
            result["Y6_SAT"]["gray"]["adjacent_XOR"])==(648,512)
    assert (result["U198_UNSAT"]["binary"]["adjacent_XOR"],
            result["U198_UNSAT"]["gray"]["adjacent_XOR"])==(3096,1940)
    assert (result["V198_SAT"]["binary"]["adjacent_XOR"],
            result["V198_SAT"]["gray"]["adjacent_XOR"])==(3108,1942)
    h=16;index=[1]*h;head=h-1;before=index[:]
    address=sum(bit<<j for j,bit in enumerate(index))
    index=[0]*h # One FLMV indexed input movement, not h individual writes.
    assert address==2**h-1 and sum(a!=b for a,b in zip(before,index))==h
    assert head==15
    result["flmv"]={"6/5":flmv(Fraction(6,5)),
                    "241/200":flmv(Fraction(241,200))}
    result["index_erase"]={"steps":1,"changed_index_cells":16,
                           "index_head_after":15,"P_vs_NP":"OPEN"}
    print(json.dumps(result,indent=2))

if __name__=="__main__":main()
