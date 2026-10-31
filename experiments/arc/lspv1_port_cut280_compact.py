#!/usr/bin/env python3
"""Dependency-free compact referee of MONOTONE-PORT-CUT280.
Run from repository root: python experiments/arc/lspv1_port_cut280_compact.py
Full original-occurrence matrices and original-source U198 refutation
are in the separate full producer / reproducibility archive.
"""
import ast
import collections
import itertools
from pathlib import Path

CANON = Path("research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt")

def fixture(b):
    out = []
    for j in range(b):
        for t in range(2):
            s = 2*j+t
            a,c,d,e = (b+4*s+k+1 for k in range(4))
            y,z = j+1,(j+1)%b+1
            out.extend([(y,a,c),(a,d,e),(c,d,e),(-z,-a,-c),(-a,-d,-e),(-c,-d,-e)])
    return out

def syntax(F):
    if not F or any(len(C)!=3 for C in F):return False
    n=max(abs(x) for C in F for x in C)
    if not n or 3*len(F)!=4*n:return False
    cnt=collections.Counter(x for C in F for x in C)
    if len({tuple(sorted(C)) for C in F})!=len(F):return False
    return (all(len({abs(x) for x in C})==3 and 0 not in C and
          (all(x>0 for x in C) or all(x<0 for x in C)) for C in F)
          and all(cnt[i]==cnt[-i]==2 for i in range(1,n+1)))

def components(F,B):
    n=max(abs(x) for C in F for x in C);B=set(B)
    P=set(range(1,n+1))-B;adj={v:set() for v in P}
    for C in F:
        q=[abs(x) for x in C if abs(x) in P]
        for v in q:adj[v].update(q)
    seen=set();out=[]
    for v in sorted(P):
        if v in seen:continue
        stack=[v];seen.add(v);S=set()
        while stack:
            x=stack.pop();S.add(x)
            for w in adj[x]-seen:seen.add(w);stack.append(w)
        out.append(S)
    return out

def port_check(F,B):
    assert syntax(F)
    n=max(abs(x) for C in F for x in C);B=set(B)
    parts=components(F,B);total=0
    for P in parts:
        rows=[C for C in F if any(abs(x) in P for x in C)]
        pos=sum(sum(x>0 and abs(x) in B for x in C) for C in rows)
        neg=sum(sum(x<0 and abs(x) in B for x in C) for C in rows)
        mp=sum(C[0]>0 for C in rows);mn=len(rows)-mp
        assert 3*mp==2*len(P)+pos
        assert 3*mn==2*len(P)+neg
        assert pos%3==neg%3 and pos+neg>=2
        total+=pos+neg
    assert len(parts)<=2*len(B) if B else len(parts)==1
    assert total<=4*len(B)
    kept=[C for C in F if not any(abs(x) in B for x in C)]
    if B:
        lookup={v:i for i,P in enumerate(parts) for v in P}
        counts=collections.Counter(lookup[abs(C[0])] for C in kept)
        assert max(counts.values(),default=0)>=(4*n/3-4*len(B))/(2*len(B))
    return len(parts)

def sat(F,a):
    return all(any(a[abs(z)-1]==(z>0) for z in C) for C in F)

def exact_small(F):
    n=max(abs(z) for C in F for z in C)
    assert n<=18
    return any(sat(F,a) for a in itertools.product((False,True),repeat=n))

def main():
    checks=0
    for b in (1,2,3,4,7):
        F=fixture(b);n=9*b
        assert syntax(F) and len(F)==12*b
        assert port_check(F,range(1,b+1))==2*b
        assert len(components(F,()))==1
        witness=[False]*b+[x for _ in range(2*b) for x in (False,True,False,True)]
        assert sat(F,witness)
        assert not sat(F,[False]*n) and not sat(F,[True]*n)
        for x in range(1,n+1):port_check(F,[x]);checks+=1
        if b<=2:
            for x in range(1,n+1):
                for y in range(x+1,n+1):port_check(F,[x,y]);checks+=1
            assert exact_small(F)
    unsat=[tuple(s[i]*(i+1) for i in range(3)) for s in itertools.product((1,-1),repeat=3)]
    assert not exact_small(unsat)
    malformed=[[],fixture(1)[:-1],fixture(1)+fixture(1)[:1],[(1,-2,3)]+fixture(1)[1:]]
    assert all(not syntax(Q) for Q in malformed)
    print("MONOTONE-PORT-CUT280 PASS, alternative single/double cuts",checks,
          "malformed controls",len(malformed))
    if CANON.exists():
        raw="\n".join(s for s in CANON.read_text().splitlines() if not s.startswith("#"))
        U=[tuple(C) for C in ast.literal_eval(raw)]
        assert len(U)==264 and syntax(U)
        V=list(U);a=list(V[2]);z=list(V[44]);a[-1],z[-1]=z[-1],a[-1]
        V[2]=tuple(a);V[44]=tuple(z)
        assert syntax(V)
        witness=("001110010011110001010001110100111110011011000101000101001010100001011010"
                 "101011000100000111001010110101001110001001101000110001100010100101101110"
                 "010101011001001100000110111001001101001101101001010101")
        assert len(witness)==198 and sat(V,[x=="1" for x in witness])
        for B in ([193,194,195,196,197,198],[193],[1],[193,194]):port_check(U,B)
        print("original U198 grammar PASS; valid V198 witness PASS; port congruence PASS")
    else:
        print("repository original U198 source absent; U/V checks skipped")
if __name__=="__main__":main()
