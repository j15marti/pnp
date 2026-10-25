#!/usr/bin/env python3
"""ARC-BIPHASE-TYPED176: source-verified two-phase CNF child constructor.
Deterministic stdlib experiment. Only a promised, easy path-XOR grammar
has power-short children; total ordinary-CNF fallback is not contracted.
No physical FLMV step/space measurement is made here.
"""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from itertools import product
from math import isqrt, log
from collections import Counter
import hashlib
import json
import sys
import time

Clause = tuple[int, ...]
CNF = tuple[Clause, ...]

@dataclass(frozen=True)
class Spec:
    bits: tuple[int, ...]
    pins: tuple[tuple[int, int], ...] = ()
    # p_i is Boolean port i; a_i is an auxiliary in each module.
    # Every pin is on an endpoint, although repeated opposite pins
    # are permitted (and correctly make the instance UNSAT).
    def __post_init__(self):
        m = len(self.bits)
        assert m >= 1 and all(x in (0, 1) for x in self.bits)
        assert all(j in (0, m) and b in (0, 1) for j,b in self.pins)

def xor3_zero(p,q,a):
    # All assignments with odd parity are forbidden, four 3-clauses.
    return tuple(tuple(v if b == 0 else -v
        for v,b in zip((p,q,a), vals))
        for vals in product((0,1),repeat=3) if sum(vals)%2)

def ordinary_cnf(spec:Spec)->CNF:
    n=len(spec.bits)
    clauses=[]
    for i,b in enumerate(spec.bits):
        p,q,a=i+1,i+2,n+i+2
        clauses.extend(xor3_zero(p,q,a))
        clauses.append((a if b else -a,))
    for j,b in spec.pins:
        p=j+1
        clauses.append((p if b else -p,))
    return tuple(clauses)

def dimacs(clauses:CNF,nvars:int)->bytes:
    assert all(1<=abs(x)<=nvars for c in clauses for x in c)
    return (f"p cnf {nvars} {len(clauses)}\n"+
        "".join(" ".join(str(x) for x in c)+" 0\n"
                for c in clauses)).encode("ascii")

def parse_dimacs(s:bytes):
    lines=s.decode("ascii").splitlines()
    h=lines[0].split()
    if len(h)!=4 or h[:2]!=["p","cnf"]:
        raise ValueError("invalid header")
    n=int(h[2]); m=int(h[3])
    cs=[]
    for line in lines[1:]:
        x=[int(y) for y in line.split()]
        if not x or x[-1]!=0 or any(v==0 or abs(v)>n for v in x[:-1]):
            raise ValueError("bad literal")
        cs.append(tuple(x[:-1]))
    if len(cs)!=m: raise ValueError("wrong clause count")
    return n,tuple(cs)

def recognize(nvars:int,clauses:CNF)->Spec|None:
    """Check exact canonical source grammar in a streaming-compatible order."""
    if nvars<3 or nvars%2!=1:
        return None
    n=(nvars-1)//2
    if len(clauses)<5*n:
        return None
    bits=[]
    for i in range(n):
        p,q,a=i+1,i+2,n+i+2
        if clauses[5*i:5*i+4]!=xor3_zero(p,q,a):
            return None
        unit=clauses[5*i+4]
        if unit==(-a,): bits.append(0)
        elif unit==(a,): bits.append(1)
        else: return None
    pins=[]
    for clause in clauses[5*n:]:
        if len(clause)!=1 or abs(clause[0]) not in (1,n+1):
            return None
        j=abs(clause[0])-1
        pins.append((j,1 if clause[0]>0 else 0))
    return Spec(tuple(bits),tuple(pins))

def brute_sat(clauses:CNF)->bool:
    """Independent generic exact SAT fallback: DPLL+unit propagation."""
    calls=0
    @lru_cache(maxsize=None)
    def rec(form:CNF)->bool:
        nonlocal calls
        calls+=1
        while True:
            if not form: return True
            if any(len(c)==0 for c in form): return False
            unit=next((c[0] for c in form if len(c)==1),None)
            if unit is None:
                break
            form=tuple(sorted(tuple(x for x in c if x!=-unit)
                    for c in form if unit not in c))
        atom=min(form,key=len)[0]
        for bit in (atom,-atom):
            reduced=tuple(sorted(tuple(x for x in c if x!=-bit)
                          for c in form if bit not in c))
            if rec(reduced): return True
        return False
    return rec(tuple(sorted(clauses)))

def oracle_parity(spec:Spec)->bool:
    # Independent linear-time checker valid only for this fixed grammar.
    n=len(spec.bits); parity=0
    for b in spec.bits: parity^=b
    implied={}
    for idx,b in spec.pins:
        mapped=b ^ (parity if idx==n else 0)
        if "p0" in implied and implied["p0"]!=mapped:
            return False
        implied["p0"]=mapped
    return True

def blocks(n:int):
    step=max(1,isqrt(n))
    result=[]
    for start in range(0,n,step):
        result.append((start,min(n,start+step)))
    return tuple(result)

def child(spec:Spec,lo:int,hi:int,left:int,right:int)->Spec:
    local=tuple((j-lo,b) for j,b in spec.pins if lo<=j<=hi)
    return Spec(spec.bits[lo:hi],local+((0,left),(hi-lo,right)))

class Ledger:
    def __init__(self):
        self.ctr=Counter()
        self.max_bytes=0
        self.first_max_bytes=0
        self.second_max_bytes=0
        self.first_calls=0
        self.second_calls=0
        self.checked=0
        self.level_bytes=Counter()
        self.parents={}
    def check(self,truth):
        if not truth: raise AssertionError("assertion failed")
        self.checked+=1

def typed_eval(spec:Spec,depth:int,mode:str,L:Ledger,level=0,check_internals=True)->bool:
    cnf=ordinary_cnf(spec); buf=dimacs(cnf,2*len(spec.bits)+1)
    n,roundtrip=parse_dimacs(buf)
    L.check(roundtrip==cnf and recognize(n,roundtrip)==spec)
    L.ctr["typed_calls"]+=1
    L.ctr["bytes_written_logical"]+=len(buf)
    L.level_bytes[level]+=len(buf)
    L.max_bytes=max(L.max_bytes,len(buf))
    if level==1:
        L.first_calls+=1
        L.first_max_bytes=max(L.first_max_bytes,len(buf))
    if level==2:
        L.second_calls+=1
        L.second_max_bytes=max(L.second_max_bytes,len(buf))
    if depth==0 or len(spec.bits)<=1:
        L.ctr["leaf_guest_calls"]+=1
        return brute_sat(roundtrip)
    spans=blocks(len(spec.bits))
    tables=[]
    for lo,hi in spans:
        rel=[[False,False],[False,False]]
        for b1,b2 in product((0,1),repeat=2):
            c=child(spec,lo,hi,b1,b2)
            ans=typed_eval(c,depth-1,"R" if mode=="L" else "L",L,level+1,check_internals)
            rel[b1][b2]=ans
        tables.append(rel)
    vec=[True,True]
    if mode=="L":
        for R in tables:
            vec=[any(vec[a] and R[a][b] for a in (0,1)) for b in (0,1)]
    else:
        for R in reversed(tables):
            vec=[any(R[a][b] and vec[b] for b in (0,1)) for a in (0,1)]
    out=any(vec)
    if check_internals and (level>=1 or len(spec.bits)<=64):
        L.check(out==brute_sat(roundtrip))
        L.ctr["independent_internal_checks"]+=1
    return out

def total_policy(nvars:int,clauses:CNF,guest=brute_sat,ledger=None)->bool:
    spec=recognize(nvars,clauses)
    if spec is None:
        if ledger is not None: ledger.ctr["off_type_parent_fallback"]+=1
        return guest(clauses)
    if ledger is not None: ledger.ctr["recognized_original_sources"]+=1
    return typed_eval(spec,2,"L",ledger) if ledger is not None else oracle_parity(spec)

def sample(n:int,tag:str):
    bits=tuple(int((7*i+3)%5 in (0,2,3)) for i in range(n))
    par=0
    for b in bits: par^=b
    pn=1^par
    if tag=="SAT":
        pins=((0,1),(n,pn))
    elif tag=="UNSAT":
        pins=((0,1),(n,1-pn))
    elif tag=="CONTRADICTORY":
        pins=((0,0),(0,1))
    elif tag=="UNPINNED":
        pins=()
    else: raise ValueError(tag)
    return Spec(bits,pins)

def main():
    started=time.time()
    L=Ledger()
    checks=[]
    # Actual SAT and UNSAT parents; two genuine levels, with both
    # phase orientations. Each child is parsed as ordinary DIMACS CNF.
    for n in (4,16,64,256):
        for tag in ("SAT","UNSAT","CONTRADICTORY","UNPINNED"):
            spec=sample(n,tag)
            clauses=ordinary_cnf(spec)
            parent_bytes=len(dimacs(clauses,2*n+1))
            exp=oracle_parity(spec)
            L.check(exp==brute_sat(clauses))
            L.check(total_policy(2*n+1,clauses,ledger=L)==exp)
            # independent alternate rule orientation as a second actual phase
            if n<=64:
                L.check(typed_eval(spec,2,"R",L)==exp)
            checks.append({"modules":n,"case":tag,"SAT":exp,"parent_bytes":parent_bytes,
                "first_level_max_bytes":L.first_max_bytes,
                "second_level_max_bytes":L.second_max_bytes})
    # Strict, local read-only grammar recognition and off-type controls.
    for clauses,n in [
        (((1,),(-1,)),1),
        (((1,2),(-1,2)),2),
        (((1,2,3),(-1,-2,-3)),3),
        ((),2),
    ]:
        L.check(recognize(n,clauses) is None)
        L.check(total_policy(n,clauses,ledger=L)==brute_sat(clauses))
    # A one-sign mutation leaves the promised grammar. Totality survives
    # only because generic DPLL remains available, with no favorable bound.
    t=sample(16,"SAT")
    cl=list(ordinary_cnf(t))
    cl[0]=tuple([-cl[0][0],*cl[0][1:]])
    n=2*len(t.bits)+1
    L.check(recognize(n,tuple(cl)) is None)
    L.check(total_policy(n,tuple(cl),ledger=L)==brute_sat(tuple(cl)))
    # Two-phase exact rational resource composition, purely conditional:
    # a_i=beta_i=1/2, r_i=1, delta_i=1/2; pair a=3/4,beta=1/4.
    from fractions import Fraction as Q
    a0=a1=b0=b1=Q(1,2); r0=r1=Q(1); d0=d1=Q(1,2)
    pair_a=a0+b0*a1; pair_b=b0*b1
    pair_r=max(r0,a0+b0*r1); pair_delta=max(d0,b0*d1)
    t_limit=max(pair_r,pair_a/(1-pair_b)); s_limit=pair_delta
    L.check((pair_a,pair_b,pair_r,pair_delta,t_limit,s_limit)==
       (Q(3,4),Q(1,4),Q(1),Q(1,2),Q(1),Q(1,2)))
    # Explicitly show the all-input fallback is still parent-size,
    # not a new achievable-pair ARC edge.
    L.check(L.ctr["off_type_parent_fallback"]==5)
    data={"id":"ARC-BIPHASE-TYPED176",
          "date":"2026-10-25 America/Los_Angeles",
          "status":"COMPUTATIONAL exact both-label two-level typed construction; ARC-EDGE-90 OPEN",
          "params":{"seed":None,"execution":"deterministic exhaustive orientations and labels",
                    "n":[4,16,64,256],"depth":2,"phases":["L","R"]},
          "limits":{"pair_a":str(pair_a),"pair_beta":str(pair_b),
                    "pair_r":str(pair_r),"pair_delta":str(pair_delta),
                    "uniform_deepening_conditional_time":str(t_limit),
                    "uniform_deepening_conditional_space":str(s_limit)},
          "counts":dict(L.ctr),"assertions":L.checked,
          "first_level_calls":L.first_calls,"second_level_calls":L.second_calls,
          "peak_serialized_input_bytes":L.max_bytes,
          "peak_first_child_bytes":L.first_max_bytes,
          "peak_second_child_bytes":L.second_max_bytes,
          "bytes_by_level":dict(L.level_bytes),
          "samples":checks,
          "limitations":[
            "Only canonical endpoint-pinned XOR path sources have a power-short typed recurrence.",
            "Generic arbitrary-CNF inputs fall back to a parent-scale exact guest with no exponent gain.",
            "This path family is decidable in linear time by parity; it is not an FLMV-hard image.",
            "The two-level experiment is not a uniform infinite recursion proof.",
            "Serialized byte traffic is not a calibrated primitive FLMV bit work or peak tape measurement.",
            "Both-phase bounds are restricted construction, not the hypothetical unstable matrices."],
          "elapsed_seconds":round(time.time()-started,4)}
    out=json.dumps(data,sort_keys=True,indent=2)
    print(out)
    return data

if __name__=="__main__":
    main()
