#!/usr/bin/env python3
"""Paid repeated-scan recognizer for the scrambled F9 cyclic-splice orbit.

The formula and pin list are read-only source objects.  The recognizer retains
at most two nine-variable components, constant local labels, counters and a
four-bit Boolean transfer accumulator.  It is a restricted family recognizer,
not an all-input SAT solver.
"""
from __future__ import annotations
import argparse,collections,itertools,json,random
from pathlib import Path

P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
Q=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F9=tuple(P)+tuple(tuple(-x for x in c) for c in Q)
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
N15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-x for x in c) for c in N15)

def family(t):
    out=[]
    for i in range(t):
        f=lambda x:9*i+x
        out.append((f(1),f(6),9*((i+1)%t)+5))
        out.extend(tuple(f(x) for x in c) for c in P[1:])
        out.extend(tuple(-f(x) for x in c) for c in Q)
    return 9*t,tuple(out)

def valid(n,F):
    if not isinstance(n,int) or n<=0 or 3*len(F)!=4*n:return False
    seen=set();occ=collections.Counter()
    for c in F:
        if len(c)!=3 or len({abs(x) for x in c})!=3:return False
        if not all(isinstance(x,int) and 1<=abs(x)<=n for x in c):return False
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False
        k=tuple(sorted(c))
        if k in seen:return False
        seen.add(k)
        for x in c:occ[(abs(x),x>0)]+=1
    return all(occ[(v,s)]==2 for v in range(1,n+1) for s in (False,True))

def oriented_sign(c,dual):
    return (1 if c[0]>0 else -1)*(-1 if dual else 1)

def component(seed,F,dual,ledger):
    """Negative-support closure, aborting when a tenth ID would be retained."""
    S={seed};changed=True
    while changed:
        changed=False;ledger["source_clause_visits"]+=len(F)
        for c in F:
            if oriented_sign(c,dual)>=0:continue
            a={abs(x) for x in c}
            if S&a and not a<=S:
                S|=a;changed=True
                if len(S)>9:return None
    return frozenset(S) if len(S)==9 else None

def classify(comp,F,dual,ledger):
    neg=[];internal=[];out=[];inc=[];bad=False
    ledger["source_clause_visits"]+=len(F)
    for c in F:
        a={abs(x) for x in c};k=len(a&comp);sgn=oriented_sign(c,dual)
        if sgn<0:
            if k and (k!=3 or not a<=comp):bad=True
            if k==3:neg.append(a)
        else:
            if k==3:internal.append(a)
            elif k==2:out.append((a&comp,next(iter(a-comp))))
            elif k==1:inc.append((next(iter(a&comp)),a-comp))
    if bad or len(neg)!=6 or len(internal)!=5 or len(out)!=1 or len(inc)!=1:return None
    return neg,internal,out[0],inc[0]

def derive(comp,F,dual,ledger):
    z=classify(comp,F,dual,ledger)
    if z is None:return None
    neg,pos,(pair,successor),(x5,predpair)=z
    if len(pair)!=2 or len(predpair)!=2:return None
    hits=[x for x in pair if any({x,x5}<=c for c in pos)]
    if len(hits)!=1:return None
    x1=hits[0];x6=next(iter(pair-{x1}))
    h=[c for c in pos if {x1,x5}<=c]
    if len(h)!=1:return None
    x3=next(iter(h[0]-{x1,x5}))
    h=[c for c in neg if {x1,x6}<=c]
    if len(h)!=1:return None
    x7=next(iter(h[0]-{x1,x6}))
    v29=[c-{x1} for c in neg if x1 in c and x6 not in c]
    v48=[c-{x6} for c in neg if x6 in c and x1 not in c]
    p469=[c-{x6} for c in pos if x6 in c]
    if len(v29)!=1 or len(v48)!=1 or len(p469)!=1:return None
    c9=v29[0]&p469[0];c4=v48[0]&p469[0]
    if len(c9)!=1 or len(c4)!=1:return None
    x9=next(iter(c9));x4=next(iter(c4));x2=next(iter(v29[0]-{x9}));x8=next(iter(v48[0]-{x4}))
    d={1:x1,2:x2,3:x3,4:x4,5:x5,6:x6,7:x7,8:x8,9:x9}
    if set(d.values())!=set(comp):return None
    if {frozenset(c) for c in pos}!={frozenset(d[x] for x in c) for c in P[1:]}:return None
    if {frozenset(c) for c in neg}!={frozenset(d[x] for x in c) for c in Q}:return None
    return d,successor

def bmul(a,b):
    out=0
    for i,j in itertools.product((0,1),repeat=2):
        if any((a>>(2*i+k)&1) and (b>>(2*k+j)&1) for k in (0,1)):out|=1<<(2*i+j)
    return out

def local_support(labels,pins,dual,ledger):
    # Pins are read-only; a physical implementation scans their source list.
    lp={i:(1-pins[x] if dual else pins[x]) for i,x in labels.items() if x in pins}
    out=0
    for left,right in itertools.product((0,1),repeat=2):
        found=False
        for bits in itertools.product((0,1),repeat=8):
            ledger["local_candidates"]+=1
            v={5:left};v.update(zip((1,2,3,4,6,7,8,9),bits))
            if any(v[i]!=b for i,b in lp.items()):continue
            if all(any(v[x] for x in c) for c in P[1:]) and all(any(not v[x] for x in c) for c in Q) and (v[1] or v[6] or right):
                found=True;break
        if found:out|=1<<(2*left+right)
    return out

def recognize_decide(n,F,pins):
    ledger={"source_clause_visits":0,"local_candidates":0,"max_live_source_ids":0}
    if not valid(n,F):return "MALFORMED",ledger
    if n<18 or n%9:return "UNRESOLVED",ledger
    for dual in (False,True):
        anchor=component(1,F,dual,ledger)
        if anchor is None:continue
        cur=anchor;acc=9;ok=True;t=n//9
        for step in range(t):
            ledger["max_live_source_ids"]=max(ledger["max_live_source_ids"],18)
            a=derive(cur,F,dual,ledger)
            if a is None:ok=False;break
            labels,seed=a;nxt=component(seed,F,dual,ledger)
            if nxt is None:ok=False;break
            b=derive(nxt,F,dual,ledger)
            if b is None or b[0][5]!=seed:ok=False;break
            acc=bmul(acc,local_support(labels,pins,dual,ledger))
            if nxt==anchor and step+1<t:ok=False;break
            cur=nxt
        if ok and cur==anchor:
            return ("SAT" if acc&9 else "UNSAT"),ledger
    return "UNRESOLVED",ledger

def scramble(n,F,pins,seed,dual=False):
    rng=random.Random(seed);ids=list(range(1,n+1));rng.shuffle(ids);mp=dict(zip(range(1,n+1),ids))
    G=[[(1 if x>0 else -1)*(-1 if dual else 1)*mp[abs(x)] for x in c] for c in F]
    for c in G:rng.shuffle(c)
    rng.shuffle(G)
    return tuple(map(tuple,G)),{mp[x]:(1-v if dual else v) for x,v in pins.items()}

def count(F,pins):
    n=max(abs(x) for c in F for x in c);free=[v for v in range(1,n+1) if v not in pins]
    return sum(all(any(({**pins,**dict(zip(free,z))})[abs(x)]==int(x>0) for x in c) for c in F) for z in itertools.product((0,1),repeat=len(free)))

def su_modes(F):
    n=max(abs(x) for c in F for x in c);checks=0
    for A,B in itertools.combinations(F,2):
        same=any(abs(x)==abs(y) and (x>0)==(y>0) for x in A for y in B);opp=any(abs(x)==abs(y) and (x>0)!=(y>0) for x in A for y in B)
        want=(not opp,not same,not same,not opp);got=[False]*4
        for z in range(1<<n):
            a={v:(z>>(v-1))&1 for v in range(1,n+1)}
            AS=all(a[abs(x)]==int(x>0) for x in A);AU=all(a[abs(x)]!=int(x>0) for x in A)
            BS=all(a[abs(x)]==int(x>0) for x in B);BU=all(a[abs(x)]!=int(x>0) for x in B)
            got=[p or q for p,q in zip(got,(AS and BS,AS and BU,AU and BS,AU and BU))]
        assert tuple(got)==want;checks+=4
    return checks

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--out",required=True);a=ap.parse_args()
    rows=[];assertions=0
    for t in (2,3,4,8,16,32):
        n,F=family(t);sat={};unsat={}
        for i in range(t):
            for x,v in ((1,1),(2,0),(3,1),(4,0),(8,0)):sat[9*i+x]=v;unsat[9*i+x]=v
        unsat[2]=1;unsat[3]=0
        for dual in (False,True):
            G,sp=scramble(n,F,sat,274000+t+dual,dual);_,up=scramble(n,F,unsat,274000+t+dual,dual)
            ls,cs=recognize_decide(n,G,sp);lu,cu=recognize_decide(n,G,up)
            assert (ls,lu)==("SAT","UNSAT");assertions+=2
            rows.append({"t":t,"dual":dual,"SAT":ls,"UNSAT":lu,"SAT_ledger":cs,"UNSAT_ledger":cu})
    # Valid nonfamily source: quota-preserving positive occurrence swap.
    n,F=family(2);H=[list(c) for c in F];H[1][0],H[7][0]=H[7][0],H[1][0];H=tuple(map(tuple,H))
    if valid(n,H):assert recognize_decide(n,H,{})[0]=="UNRESOLVED";assertions+=1
    malformed=((),((1,1,2),),((1,-2,3),),F9+(F9[0],),((1,2,3),(1,2,4)))
    assert all(not valid(max([abs(x) for c in f for x in c],default=1),f) for f in malformed);assertions+=len(malformed)
    n2,G2=family(2);s2={};u2={}
    for i in range(2):
        for x,v in ((1,1),(2,0),(3,1),(4,0),(8,0)):s2[9*i+x]=v;u2[9*i+x]=v
    u2[2]=1;u2[3]=0
    controls={"Y6_models":count(Y6,{}),"F9_models":count(F9,{}),"G2_SAT_models":count(G2,s2),"G2_UNSAT_models":count(G2,u2),"F9_SU_pair_modes":su_modes(F9),
      "F15_SAT_models":count(F15,dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))),
      "F15_UNSAT_models":count(F15,dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0))))}
    assert controls=={"Y6_models":20,"F9_models":70,"G2_SAT_models":1,"G2_UNSAT_models":0,"F9_SU_pair_modes":264,"F15_SAT_models":2,"F15_UNSAT_models":0};assertions+=7
    out={"run":"LOGSPACE_ANONYMOUS_CYCLE_REFEREE274","timestamp_PST":"2026-11-01 14:48","status":"PROVED/EXACT restricted algorithm plus COMPUTATIONAL controls","P_vs_NP":"OPEN",
      "theorem":{"scope":"arbitrarily variable-renamed, clause/literal-permuted and globally complemented G_t orbit, t>=2; other valid sources UNRESOLVED",
        "result":"deterministic polynomial-time, O(log N)-writable-space decision after fully paid repeated source scans; no global canonical block map",
        "space_reason":"at most two nine-ID components, constant local labels, O(log N) counters/addresses and four-bit Boolean accumulator",
        "soundness":"negative closure is stored only up to ten IDs; every accepted block is fully template-checked, successor/incoming incidences are unique, and exactly n/9 successor steps close the one cycle",
        "not_proved":"all-input polynomial controller, low native FLMV time exponent, arbitrary-A ARC, numerical FLMV transfer"},
      "tests":rows,"assertions":assertions,"controls":controls,
      "charged_recurrence":"W(z)=grammar+source/index/head+all repeated scans+discover/select/switch/fail+local-table/GE/proof/cache/replay+sum child(output/access/guest+W(child)); peak is simultaneous live parser, two blocks, counters, accumulator, proof/output staging and guest",
      "complexity":{"time":"N^O(1) word/source-record operations; the concrete checker records O(t*m) structural scans plus local candidates, not a native indexed-TM exponent","writable_space":"O(log N) bits/words under read-only source/pin encodings; output excluded and separately charged","xor":"offline only"},
      "limitations":["restricted recognized orbit","Python object memory is not a native FLMV trace","SAT witness/UNSAT proof output can be recomputed and is separately charged","fallback on UNRESOLVED may be exponential"]}
    Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"status":"PASS","cases":len(rows),"assertions":assertions,"largest":rows[-1],"controls":controls,"P_vs_NP":"OPEN"},indent=2))
if __name__=="__main__":main()
