#!/usr/bin/env python3
"""LSPV-3 ARC-FIXEDPATH-CAPSULE123: proper 3CNF two-descendant audit.

Run: python 2026-10-25_1124_ARC_FIXEDPATH_CAPSULE123_repro.py
No external dependencies. The model is an exact finite semantic audit,
NOT a measurement of FLMV machine work/space.
"""
from __future__ import annotations
import itertools, json, random, hashlib, sys
from collections import Counter
from pathlib import Path

SEED=12320261025
rng=random.Random(SEED)
checks=0

def ok(b, note=""):
    global checks
    checks += 1
    if not b:
        raise AssertionError(f"check {checks}: {note}")

def serial(n, clauses):
    for c in clauses:
        ok(len(c)==3 and len({abs(v) for v in c})==3 and all(0<abs(v)<=n for v in c), "invalid proper3 clause")
    return (f"p cnf {n} {len(clauses)}\n" + "".join(" ".join(str(x) for x in c)+" 0\n" for c in clauses)).encode('ascii')

def parse(blob):
    lines=blob.decode('ascii').splitlines()
    h=lines[0].split()
    ok(len(h)==4 and h[:2]==['p','cnf'],"header grammar")
    n,m=map(int,h[2:])
    cs=[]
    for line in lines[1:]:
        a=[int(x) for x in line.split()]
        ok(len(a)==4 and a[-1]==0 and len({abs(x) for x in a[:-1]})==3 and all(0<abs(x)<=n for x in a[:-1]),"body grammar")
        cs.append(tuple(a[:-1]))
    ok(len(cs)==m, "header count")
    return n, cs

def pin(n, cs, lit):
    # Literal lit on an EXISTING original variable, or an explicitly new variable.
    n0=max(n,abs(lit))
    a,b=n0+1,n0+2
    gadget=[(lit,a,b),(lit,a,-b),(lit,-a,b),(lit,-a,-b)]
    return n0+2, list(cs)+gadget

def sat(n, cs):
    # Independent exhaustive solver, deliberately not using support masks.
    for bits in range(1<<n):
        if all(any(((bits>>(abs(v)-1))&1)==int(v>0) for v in clause) for clause in cs):
            return True
    return False

def rootsupport(mask, n=3):
    cs=[]
    for w in range(1<<n):
        if not ((mask>>w)&1):
            cs.append(tuple(i+1 if not ((w>>i)&1) else -(i+1) for i in range(n)))
    return n,cs

def chain(n, cs):
    n0,cs0=parse(serial(n,cs))
    n1,cs1=pin(n0,cs0,-1)
    n1,cs1=parse(serial(n1,cs1))
    n2,cs2=pin(n1,cs1,-2)
    n2,cs2=parse(serial(n2,cs2))
    truth=[sat(n0,cs0),sat(n1,cs1),sat(n2,cs2)]
    code=sum(truth)
    ok(truth==[i<code for i in range(3)],"monotone two-level trace")
    return truth,code,[len(serial(n0,cs0)),len(serial(n1,cs1)),len(serial(n2,cs2))]

counts=Counter()
sizes=[]
for mask in range(256):
    n,cs=rootsupport(mask)
    trace,code,lens=chain(n,cs)
    expected=[bool(mask),any(mask & (1<<w) for w in range(8) if (w&1)==0),
              any(mask & (1<<w) for w in range(8) if (w&3)==0)]
    ok(trace==expected, f"support mask={mask}")
    counts[code]+=1
    sizes.append(lens)

ok(dict(counts)=={0:1,1:15,2:48,3:192},"exact trace-class counts")
# Real contrasting two-level proper3 continuations, both labels and source aliases.
real1=chain(*rootsupport(1<<0))
real2=chain(*rootsupport(1<<2))
real3=chain(*rootsupport(1<<7))
ok(real1[0]==[True,True,True] and real2[0]==[True,True,False]
   and real3[0]==[True,False,False],"four trajectory witnesses")
# Wrong-source pin: rename the original x_2 to independent fresh x_8.
n,cs=rootsupport(1<<2)
n1,c1=pin(n,cs,-1)
nt,ct=pin(n1,c1,-2)
nw,cw=pin(n1,c1,-(n1+1))
ok(sat(n1,c1) and not sat(nt,ct) and sat(nw,cw),"source-name alias falsifier")

# Mixed easy/hostile ordinary examples: Horn, 2CNF lift, XOR, independent products.
controls={
 "horn_easy":(3,[(-1,-2,-3)]),
 "two_sat_lift":(4,[(1,2,4),(1,2,-4)]),
 "xor_odd":rootsupport(sum(1<<w for w in range(8) if (w.bit_count()%2)==1)),
 "disconnected":(6,[(1,2,3),(4,5,6)]),
}
n0,c0=pin(3,[],-1)
n1,c1=pin(n0,c0,1)
controls['horn_bad']=(n1,c1)
control_results={}
for name,(n,cs) in controls.items():
    trace,code,lens=chain(n,cs)
    control_results[name]={"truth":trace,"code":code,"lengths":lens}

random_cases=150
random_sat=0
random_unsat=0
random_grandchild_unsat=0
for z in range(random_cases):
    n=rng.randrange(3,7)
    m=rng.randrange(0,32)
    cs=[]
    for _ in range(m):
        vs=rng.sample(range(1,n+1),3)
        cs.append(tuple(v if rng.randrange(2) else -v for v in vs))
    trace,code,lens=chain(n,cs)
    random_sat+=bool(trace[0]); random_unsat+=not trace[0]
    random_grandchild_unsat+=not trace[2]
    ok(trace==[sat(n,cs),sat(*pin(n,cs,-1)),sat(*pin(*pin(n,cs,-1),-2))],"independent path check")

body={
 "run":"ARC-FIXEDPATH-CAPSULE123",
 "seed":SEED,
 "status":"PROVED/EXACT restricted fixed two-level trace lemma; COMPUTATIONAL finite check; ARC-EDGE-90 OPEN; P versus NP OPEN",
 "assertions":checks,
 "support_masks_exhaustive":256,
 "trace_codes":{"0_UNSAT_UNSAT_UNSAT":counts[0],"1_SAT_UNSAT_UNSAT":counts[1],"2_SAT_SAT_UNSAT":counts[2],"3_SAT_SAT_SAT":counts[3]},
 "ordinary_two_level_examples":{"all_sat":real1,"late_unsat":real2,"early_unsat":real3},
 "wrong_source_alias_detected":True,
 "controls":control_results,
 "random_cases":random_cases,
 "random_seed":SEED,
 "random_root_sat":random_sat,
 "random_root_unsat":random_unsat,
 "random_grandchild_unsat":random_grandchild_unsat,
 "encoding":"complete standard ASCII DIMACS header/body; 3 pairwise-distinct source variable names per clause; 4-clause PIN with 2 new private names per level",
 "capsule_bits":2,
 "limitations":"Only a user-specified fixed two-level continuation path. A called on original-scale child encodings, NOT power-short; semantic status bits cannot generate arbitrary future named children. Python solver measures logic, not FLMV bit work, peak space, flips, circuit size or bit-time."
}
script=Path(__file__)
body['script_sha256']=hashlib.sha256(script.read_bytes()).hexdigest()
raw_path=script.with_name(script.name.replace('_repro.py','_raw.json'))
raw_path.write_text(json.dumps(body,indent=2,sort_keys=True)+'\n')
print(json.dumps(body,indent=2,sort_keys=True))
