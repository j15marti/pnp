#!/usr/bin/env python3
"""Exact interface-gauge invariance audit for cyclic decision transfer.

This is a restricted theorem on already authenticated cyclic residuals.  It
does not authenticate an arbitrary source and does not prove SAT hardness.
"""
from __future__ import annotations

import argparse
import collections
import itertools
import json
from pathlib import Path

F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
N15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-v for v in c) for c in N15)

PROFILE={
    "2":((0,2),(0,0)),"8":((0,0),(0,10)),
    "B":((3,9),(0,3)),"C":((0,0),(8,18)),
    "A":((0,0),(23,36)),"b":((0,0),(0,3)),
    "Q":((0,13),(0,0)),"Z":((34,47),(23,36)),
}
SAT_WORD=("2","8","B","8","C","B")
UNSAT_WORD=("2","8","C","B","8","B")
I=((1,0),(0,1)); X=((0,1),(1,0))

def mm(a,b):
    return tuple(tuple(sum(a[i][k]*b[k][j] for k in (0,1)) for j in (0,1)) for i in (0,1))
def mt(a): return tuple(tuple(a[j][i] for j in (0,1)) for i in (0,1))
def prod(ms):
    z=I
    for m in ms:z=mm(z,m)
    return z
def tr(a): return a[0][0]+a[1][1]
def supp(a): return tuple(tuple(int(a[i][j]>0) for j in (0,1)) for i in (0,1))
def bmm(a,b):
    return tuple(tuple(int(any(a[i][k] and b[k][j] for k in (0,1))) for j in (0,1)) for i in (0,1))
def bprod(ms):
    z=I
    for m in ms:z=bmm(z,supp(m))
    return z
def bdiag(a): return bool(a[0][0] or a[1][1])

def gauge(ms,bits):
    ps=[X if b else I for b in bits]
    return tuple(mm(mm(ps[i],ms[i]),ps[(i+1)%len(ms)]) for i in range(len(ms)))

def grammar(f,n=None):
    try:
        if not f:return False
        n=n or max(abs(x) for c in f for x in c)
        if n%3 or 3*len(f)!=4*n:return False
        seen=set();q=collections.Counter()
        for c in f:
            if len(c)!=3 or len({abs(x) for x in c})!=3:return False
            if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
            k=tuple(sorted(c))
            if k in seen:return False
            seen.add(k);q.update(c)
        return all(q[v]==q[-v]==2 for v in range(1,n+1))
    except Exception:return False

def sat(f,a):return all(any(a[abs(x)]==int(x>0) for x in c) for c in f)
def count(f,pins):
    n=max(abs(x) for c in f for x in c);free=[v for v in range(1,n+1) if v not in pins]
    return sum(sat(f,{**pins,**dict(zip(free,z))}) for z in itertools.product((0,1),repeat=len(free)))
def su_modes(f):
    n=max(abs(x) for c in f for x in c);checks=0
    for a,b in itertools.combinations(f,2):
        same=any(abs(x)==abs(y) and (x>0)==(y>0) for x in a for y in b)
        opp=any(abs(x)==abs(y) and (x>0)!=(y>0) for x in a for y in b)
        want=(not opp,not same,not same,not opp);got=[False]*4
        for z in range(1<<n):
            v={i:(z>>(i-1))&1 for i in range(1,n+1)}
            AS=all(v[abs(x)]==int(x>0) for x in a);AU=all(v[abs(x)]!=int(x>0) for x in a)
            BS=all(v[abs(x)]==int(x>0) for x in b);BU=all(v[abs(x)]!=int(x>0) for x in b)
            got=[p or q for p,q in zip(got,(AS and BS,AS and BU,AU and BS,AU and BU))]
        assert tuple(got)==want;checks+=4
    return checks

def audit_word(word):
    ms=tuple(PROFILE[x] for x in word);base=tr(prod(ms));label=bdiag(bprod(ms));checks=0
    for bits in itertools.product((0,1),repeat=len(ms)):
        gm=gauge(ms,bits)
        assert tr(prod(gm))==base and bdiag(bprod(gm))==label
        checks+=2
    for r in range(len(ms)):
        rot=ms[r:]+ms[:r]
        assert tr(prod(rot))==base and bdiag(bprod(rot))==label
        rev=tuple(mt(x) for x in reversed(rot))
        assert tr(prod(rev))==base and bdiag(bprod(rev))==label
        checks+=4
    return base,label,checks

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",required=True);args=ap.parse_args()
    assert grammar(F9,9) and grammar(Y6,6) and grammar(F15,15)
    rows=[];checks=0
    for name,w in (("SAT",SAT_WORD),("UNSAT",UNSAT_WORD)):
        c,label,k=audit_word(w);checks+=k
        rows.append({"name":name,"word":"".join(w),"integer_trace":c,"decision":label,
                     "gauges_checked":2**len(w),"rotations":len(w)})
    assert rows[0]["integer_trace"]==14400 and rows[0]["decision"]
    assert rows[1]["integer_trace"]==0 and not rows[1]["decision"]

    # Exhaust every short profile word and every local binary interface gauge.
    alphabet=("2","8","B","C")
    exhaustive=[]
    for n in range(1,7):
        words=0
        for w in itertools.product(alphabet,repeat=n):
            c,label,k=audit_word(w);checks+=k;words+=1
            assert label==(c>0)
        exhaustive.append({"length":n,"words":words,"gauges_per_word":2**n})

    # GATE309 local context products remain label/count exact under gauges.
    theta={x+y:tr(mm(PROFILE[x],PROFILE[y])) for x in ("A","b") for y in ("Z","Q")}
    assert theta=={"AZ":2377,"AQ":299,"bZ":108,"bQ":0}
    for w in (("A","Z"),("A","Q"),("b","Z"),("b","Q")):
        c,label,k=audit_word(w);checks+=k
        assert c==theta["".join(w)] and label==(c>0)

    controls={"Y6_models":count(Y6,{}),"F9_models":count(F9,{}),"F9_SU_pair_modes":su_modes(F9),
      "F15_SAT_models":count(F15,dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))),
      "F15_UNSAT_models":count(F15,dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0))))}
    assert controls=={"Y6_models":20,"F9_models":70,"F9_SU_pair_modes":264,"F15_SAT_models":2,"F15_UNSAT_models":0}
    malformed=[(),((1,1,2),),((1,-2,3),),F9+(F9[0],),((1,2,3),(1,2,4))]
    assert all(not grammar(f) for f in malformed);controls["malformed_rejected"]=len(malformed)

    out={
      "run":"ANONYMOUS_INTERFACE_GAUGE_REFEREE273","timestamp_PST":"2026-11-01 13:48",
      "status":"PROVED/EXACT algebraic theorem; COMPUTATIONAL finite controls","P_vs_NP":"OPEN",
      "theorem":{
        "quantifiers":"every cyclic sequence of square matrices over a commutative semiring and every independent interface permutation gauge",
        "identity":"Mhat_i=P_i^-1 M_i P_(i+1), cyclic indices; product(Mhat)=P_1^-1 product(M) P_1",
        "consequences":["trace and Boolean diagonal nonemptiness are gauge invariant","cyclic start is irrelevant","reversal plus local transpose is irrelevant"],
        "decision_only_scope":"a unique global block start, orientation, and binary interface naming are not necessary once the cyclic factors are authenticated",
        "not_proved":"cheap authentication, all-input acquisition, arbitrary-machine lower bound, ARC contraction, or FLMV transfer"},
      "named_words":rows,"exhaustive_short_words":exhaustive,"theta":theta,"assertions":checks,"controls":controls,
      "charged_recurrence":"W(s)=C_grammar+source/index/head reads+C_component/interface discovery+sum attempted(select/switch/fail)+sum local-table/GE/proof/cache/replay+sum children(output/access/guest+W(child)); peak=max simultaneous live source maps, matrices, proof and guest tapes",
      "algorithms":{
        "cached":"O(N log N) word operations and O(N) retained source/mapping words on the recognized orbit (GATE310 bound)",
        "recompute":"conservative O(N^2 log N) time and O(log N) live indices plus a constant 2x2 accumulator, by repeated paid scans without a global canonical label table"},
      "wrappers":{"DELAY_COPY_RECOMP":"all charged even if logical XOR is zero","logical_XOR":"offline diagnostic only"},
      "search_scope":"primary gauge/normal-factor-graph and bounded-valence canonization literature; project and github.com/openai searches",
      "limitations":["restricted authenticated G_t orbit","anonymous traversal still requires paid local consistency and closure checks","no total polynomial all-input recurrence","U198/V198 inherited controls are labels only, not instances of this terminal"]}
    Path(args.out).parent.mkdir(parents=True,exist_ok=True)
    Path(args.out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","assertions":checks,"named":rows,"controls":controls,"P_vs_NP":"OPEN"},indent=2))
if __name__=="__main__":main()
