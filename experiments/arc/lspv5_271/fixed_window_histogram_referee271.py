#!/usr/bin/env python3
"""Exact decision-only red team for cyclic local-profile histograms.

Proves a restricted infinite theorem on the authenticated connected F9 cyclic
source family.  It is not an all-input SAT solver or a runtime lower bound.
"""
from __future__ import annotations

import argparse
import collections
import itertools
import json
from pathlib import Path

F9 = (
    (1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9),
)
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
N15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-v for v in c) for c in N15)

PINS={
    "2":{2:1,6:0,7:1,9:1},
    "8":{1:0,3:0,6:0},
    "B":{4:0,6:0},
    "C":{1:0,3:0},
}
EXPECTED={
    "2":((0,2),(0,0)),
    "8":((0,0),(0,10)),
    "B":((3,9),(0,3)),
    "C":((0,0),(8,18)),
}
S=("2","8","B","8","C","B")
U=("2","8","C","B","8","B")
AB_A={1:1,2:0,3:1,4:0,8:0}
AB_B={1:1,2:1,3:0,4:0,8:0}

def sat(F,a):
    return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)

def grammar(F,n=None):
    try:
        if not F:return False
        n=n or max(abs(x) for c in F for x in c)
        if n%3 or 3*len(F)!=4*n:return False
        seen=set(); q=collections.Counter()
        for c in F:
            if len(c)!=3 or len({abs(x) for x in c})!=3:return False
            if not (all(x>0 for x in c) or all(x<0 for x in c)):return False
            k=tuple(sorted(c))
            if k in seen:return False
            seen.add(k);q.update(c)
        return all(q[v]==q[-v]==2 for v in range(1,n+1))
    except Exception:return False

def build(t):
    out=[]
    for i in range(t):
        off=9*i; nxt=9*((i+1)%t)+5
        for j,c in enumerate(F9):
            cc=[]
            for x in c:
                v=abs(x)+off
                if j==0 and x==5:v=nxt
                cc.append(v if x>0 else -v)
            out.append(tuple(cc))
    return tuple(out)

def local_matrix(pins):
    M=[[0,0],[0,0]]
    for left,right in itertools.product((0,1),repeat=2):
        free=[v for v in range(1,10) if v not in pins and v!=5]
        for bits in itertools.product((0,1),repeat=len(free)):
            a=dict(pins);a.update(zip(free,bits));a[5]=left
            ok=True
            for j,c in enumerate(F9):
                if not any((right if j==0 and x==5 else a[abs(x)])==int(x>0) for x in c):
                    ok=False;break
            M[left][right]+=ok
    return tuple(map(tuple,M))

def imul(A,B):
    return tuple(tuple(sum(A[i][h]*B[h][j] for h in (0,1)) for j in (0,1)) for i in (0,1))

def support(A):
    return sum((A[i][j]>0)<<(2*i+j) for i in (0,1) for j in (0,1))

def bmul(a,b):
    out=0
    for i,j in itertools.product((0,1),repeat=2):
        if any((a>>(2*i+h)&1) and (b>>(2*h+j)&1) for h in (0,1)):
            out|=1<<(2*i+j)
    return out

def iprod(word):
    A=((1,0),(0,1))
    for x in word:A=imul(A,EXPECTED[x])
    return A

def bprod(word):
    a=9
    for x in word:a=bmul(a,support(EXPECTED[x]))
    return a

def trace(A):return A[0][0]+A[1][1]

def inflate(word,L):
    return tuple(y for x in word for y in (("B",)*L+(x,)))

def cyclic_deck(word,k):
    n=len(word)
    return collections.Counter(tuple(word[(i+j)%n] for j in range(k)) for i in range(n))

def direct_count(F,pins):
    n=max(abs(x) for c in F for x in c);free=[v for v in range(1,n+1) if v not in pins]
    return sum(sat(F,{**pins,**dict(zip(free,bits))}) for bits in itertools.product((0,1),repeat=len(free)))

def su_modes(F):
    n=max(abs(x) for c in F for x in c);checks=0
    for A,B in itertools.combinations(F,2):
        same=any(abs(x)==abs(y) and (x>0)==(y>0) for x in A for y in B)
        opp=any(abs(x)==abs(y) and (x>0)!=(y>0) for x in A for y in B)
        want=(not opp,not same,not same,not opp); got=[False]*4
        for z in range(1<<n):
            a={v:(z>>(v-1))&1 for v in range(1,n+1)}
            AS=all(a[abs(x)]==int(x>0) for x in A);AU=all(a[abs(x)]!=int(x>0) for x in A)
            BS=all(a[abs(x)]==int(x>0) for x in B);BU=all(a[abs(x)]!=int(x>0) for x in B)
            got=[p or q for p,q in zip(got,(AS and BS,AS and BU,AU and BS,AU and BU))]
        assert tuple(got)==want;checks+=4
    return checks

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",required=True);args=ap.parse_args()
    assert grammar(F9,9) and grammar(Y6,6) and grammar(F15,15)
    matrices={x:local_matrix(PINS[x]) for x in PINS}
    assert matrices==EXPECTED
    assert [support(EXPECTED[x]) for x in ("2","8","B","C")]==[2,8,11,12]
    assert bmul(11,11)==11
    rows=[]
    for k in range(1,65):
        L=max(0,k-2); ws=inflate(S,L); wu=inflate(U,L)
        assert ws!=wu and len(ws)==6*(L+1)
        assert collections.Counter(ws)==collections.Counter(wu)
        assert all(cyclic_deck(ws,j)==cyclic_deck(wu,j) for j in range(1,k+1))
        ps,pu=bprod(ws),bprod(wu)
        assert ps==3 and pu==2 and ps&9 and not pu&9
        Is,Iu=iprod(ws),iprod(wu)
        assert trace(Is)>0 and trace(Iu)==0
        if k<=12 or k in (16,24,32,48,64):
            assert grammar(build(len(ws)),9*len(ws))
            rows.append({"k":k,"separator_length":L,"blocks":len(ws),
                         "SAT_support_mask":ps,"UNSAT_support_mask":pu,
                         "SAT_models":str(trace(Is)),"UNSAT_models":str(trace(Iu)),
                         "all_cyclic_decks_through_k_equal":True})

    # Recheck DECISION307's distinct AND_t promise and tight query cover.
    WA=local_matrix(AB_A);WB=local_matrix(AB_B)
    assert WA==((1,1),(0,0)) and WB==((0,0),(0,0))
    ab=[]
    for t in (1,2,3,4,8,16,64):
        regions=[{2*i,2*i+1} for i in range(t)]
        witness={2*i for i in range(t)}
        assert all(witness&r for r in regions)
        if t<=8:
            assert not any(all(set(c)&r for r in regions)
                           for q in range(t) for c in itertools.combinations(range(2*t),q))
        ab.append({"t":t,"lower_bound":t,"matching_scan":t})

    controls={
      "Y6_models":direct_count(Y6,{}),"F9_models":direct_count(F9,{}),
      "F9_A_models":direct_count(F9,AB_A),"F9_B_models":direct_count(F9,AB_B),
      "F9_SU_pair_modes":su_modes(F9),
      "F15_SAT_models":direct_count(F15,dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))),
      "F15_UNSAT_models":direct_count(F15,dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0))))}
    assert controls=={"Y6_models":20,"F9_models":70,"F9_A_models":1,"F9_B_models":0,
                      "F9_SU_pair_modes":264,"F15_SAT_models":2,"F15_UNSAT_models":0}
    malformed=[(),((1,1,2),),((1,-2,3),),F9+(F9[0],),((1,2,3),(1,2,4))]
    assert all(not grammar(x) for x in malformed);controls["malformed_rejected"]=len(malformed)

    out={
      "run":"FIXED_WINDOW_HISTOGRAM_REFEREE271",
      "timestamp_PST":"2026-11-01 11:48",
      "status":"PROVED/EXACT restricted symbolic theorem plus COMPUTATIONAL controls",
      "P_vs_NP":"OPEN",
      "theorem":{
        "quantifiers":"for every k>=1 there exists one valid connected canonical G_{6(max(0,k-2)+1)} original and two coherent pinned residuals",
        "equal_information":"identical cyclic factor-count decks for every length 1..k",
        "opposite_labels":"inflated S is SAT; inflated U is UNSAT",
        "proof":"uniform morphism h_L(a)=B^L a; windows of length <=L+2 depend only on a source bigram, while B support 11 is Boolean-idempotent and ordered products remain masks 3 versus 2",
        "scope":"recognized F9 cyclic-splice family; pinned residuals, not opposite untouched originals"},
      "matrices":{x:[list(r) for r in EXPECTED[x]] for x in EXPECTED},
      "base_words":{"SAT":S,"UNSAT":U},
      "selected_checks":rows,
      "AB_tight_linear_query_recheck":ab,
      "controls":controls,
      "charged_algorithm":"paid grammar/profile recognition + source/index/head reads + ordered 4-bit relation streaming; O(N) table operations on recognized family",
      "charged_recurrence":"W(z)=C_grammar/source/index/head + sum_attempted C_discover/select/switch/failed + C_relation/GE/proof/cache/replay + sum_children(C_output/access/guest+W(child)); peak is simultaneous live state",
      "wrappers":{"DELAY":"charged even with zero logical XOR","COPY_RECOMP":"charged","logical_XOR":"offline only"},
      "limitations":["fixed-window collision is not a time lower bound","ordered streaming remains cheap","no all-input semantic-quotient acquisition bound","no arbitrary-A ARC","no numerical same-machine FLMV transfer"]}
    Path(args.out).parent.mkdir(parents=True,exist_ok=True)
    Path(args.out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","k_checked":64,"controls":controls,"P_vs_NP":"OPEN"},indent=2))

if __name__=="__main__":main()
