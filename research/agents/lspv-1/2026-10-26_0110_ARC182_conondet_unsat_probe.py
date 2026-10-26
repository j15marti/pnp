#!/usr/bin/env python3
"""ARC182: source-coherent accepting-path probe lower bound for UNSAT certificates.

Standalone Python 3.10+ standard library. No SAT packages or network.
Replays the fixed-incidence ARC181 proper 3-CNF parity family, independently
checks the all-zero UNSAT and its p single-bit SAT neighbours with DPLL and
selected brute-force instances, then audits the accepted-path adversary:
any probe trace missing one of the p disjoint sign-bit groups is identical on
a SAT neighbour. It also verifies the exact two-branch Theorem 1.3 algebra.

Run: python 2026-10-26_0110_ARC182_conondet_unsat_probe.py
Output: sibling JSON. Research result is a theorem only in the stated
source-probe nondeterministic verifier model, not P != NP.
"""
from __future__ import annotations
from itertools import product
from pathlib import Path
from fractions import Fraction as Q
import json, hashlib, math, time

RUN='ARC182-CONONDET-UNSAT-ACCEPTING-PATH'
OUT=Path(__file__).with_name('2026-10-26_0110_ARC182_results.json')


def force3(lit:int,a:int,b:int):
    return tuple((lit, x*a,y*b) for x,y in product((1,-1),repeat=2))


def xor3(a:int,b:int,z:int):
    return tuple(tuple(v if not value else -v for v,value in zip((a,b,z),bits))
                 for bits in product((0,1),repeat=3)
                 if bits[2] != (bits[0]^bits[1]))


def family(bits: tuple[int,...]):
    p=len(bits)
    if p<2:raise ValueError('p >= 2')
    clauses=[]
    for i,bit in enumerate(bits):
        x=i+1; a=p+2*i+1; b=p+2*i+2
        clauses.extend(force3(x if bit else -x,a,b))
    for j in range(p-1):
        left=(j+1 if j==0 else 3*p+j)
        right=j+2
        z=3*p+j+1
        clauses.extend(xor3(left,right,z))
    clauses.extend(force3(4*p-1,4*p,4*p+1))
    return tuple(clauses),4*p+1


def sat_dpll(clauses):
    def go(cs,assn):
        cs=tuple(frozenset(c) for c in cs)
        while True:
            if any(not c for c in cs):return None
            if not cs:return dict(assn)
            unit=next((next(iter(c)) for c in cs if len(c)==1),None)
            if unit is None:break
            key,value=abs(unit),unit>0
            if key in assn and assn[key]!=value:return None
            assn={**assn,key:value}
            cs=tuple(c for c in cs if unit not in c)
            cs=tuple(c-{-unit} for c in cs)
        k=abs(next(iter(min(cs,key=len))))
        for value in (0,1):
            l=k if value else -k
            r=go(tuple(c-{-l} for c in cs if l not in c),{**assn,k:bool(value)})
            if r is not None:return r
        return None
    return go(clauses,{})


def brute_sat(clauses,n):
    for values in product((False,True),repeat=n):
        if all(any(values[abs(l)-1]==(l>0) for l in c) for c in clauses):
            return True
    return False


def encode(clauses,n):
    m=len(clauses)
    w=(max(n,m)+1).bit_length()
    return (f'{n:0{w}b}{m:0{w}b}' +
            ''.join(('0' if lit>0 else '1')+f'{abs(lit):0{w}b}'
                    for c in clauses for lit in c)), w


def positions(p,w):
    return [tuple(2*w + (3*(4*i+j))*(w+1) for j in range(4))
            for i in range(p)]


def frontier(d:Q):
    if d<=1:raise ValueError('d>1')
    f=Q(1,1)+Q(1,1)/d
    g=(2*d-1)/(d*(d-1))
    return f,g,max(f,g)


def main():
    t=time.perf_counter()
    checks=0
    def ck(cond, why):
        nonlocal checks
        if not cond:raise AssertionError(why)
        checks+=1
    rows=[]; tested=0; sat=0; unsat=0; sensitive=0; blind=0; high=0
    for p in range(2,9):
        z=(0,)*p
        F,n=family(z)
        binary,w=encode(F,n)
        groups=positions(p,w)
        ck(n==4*p+1 and len(F)==8*p,'size')
        ck(len({tuple(c) for c in F})==len(F),'duplicate')
        ck(all(len(c)==3 and len(set(map(abs,c)))==3 for c in F),'proper')
        ck(len(groups)==p and len(set(sum((list(x) for x in groups),[])))==4*p,'disjoint 4-bit groups')
        ck(sat_dpll(F) is None,'zero UNSAT')
        tested+=1;unsat+=1
        if p<=3:ck(not brute_sat(F,n),'independent zero exhaustive')
        for i in range(p):
            bits=tuple(int(j==i) for j in range(p))
            G,gn=family(bits)
            binary2,w2=encode(G,gn)
            changed={k for k,(a,b) in enumerate(zip(binary,binary2)) if a!=b}
            ck(w2==w and len(binary)==len(binary2),'fixed lengths')
            ck(changed==set(groups[i]),'exactly 4 local changed sign fields')
            answer=sat_dpll(G)
            ck(answer is not None,'neighbour SAT')
            if p<=3:ck(brute_sat(G,gn),'independent SAT exhaustive')
            tested+=1;sat+=1;sensitive+=1
        # All 2^p potential remembered-source-group sets. Every proper subset
        # misses one sensitive group, yielding an indistinguishable SAT input.
        for mask in range(1<<p):
            included=[i for i in range(p) if mask & (1<<i)]
            touched={groups[i][0] for i in included}
            unseen=[i for i in range(p) if i not in included]
            if unseen:
                j=unseen[0]
                G,_=family(tuple(int(i==j) for i in range(p)))
                other,_=encode(G,n)
                ck(all(binary[k]==other[k] for k in touched),
                   'blind accepting path indistinguishable from SAT neighbour')
                blind+=1
            else:
                ck(len(touched)==p,'sharp p probes')
        # Control: on the promise, one sign from each group recovers all p bits.
        recovered=tuple(int(binary[groups[i][0]]=='0') for i in range(p))
        ck(recovered==z,'one-bit-per-group promise readout')
        rows.append({'p':p,'N_bits':len(binary),'n':n,'m':len(F),
                     'source_probe_floor':p,'independent_sensitive_groups':p,
                     'one_bit_neighbours_SAT':p,'zero_input_UNSAT':True,
                     'blind_probe_group_sets':(1<<p)-1,
                     'promised_checker_source_probes':p,
                     'formula_word_width':w})
    # An additional test of SAT/UNSAT controls for all family bits p<=6.
    for p in range(2,7):
        for bs in product((0,1),repeat=p):
            F,n=family(bs)
            label=sum(bs)%2==1
            ck((sat_dpll(F) is not None)==label,'full promise parity')
            tested+=1
            sat+=int(label);unsat+=int(not label)
    # Source-exact theorem 1.3 has OR branches, not their conjunction.
    for num,den in [(901,500),(19,10),(2,1),(5,2),(3,1),(10,1),(100,1)]:
        d=Q(num,den);f,g,H=frontier(d)
        ck((g-f)==((2-d)/(d-1)),'frontier difference identity')
        ck((g>=f)==(d<=2),'branch crossover')
        ck(H>1,'full two-branch frontier always superlinear for finite d')
        high+=1
    d=Q(901,500)
    f,g,H=frontier(d)
    ck(g==Q(651000,361301),'exact c(1.802)')
    ck(g-Q(1,1)==Q(289699,361301),'arithmetic')
    # A worst-case near-linear probe floor does not reach the 1.802 frontier.
    ck(Q(1,1)<H,'floor insufficient for contradiction')
    summary={
     'run':RUN,
     'proof':'Every accepting nondeterministic UNSAT branch on F_(p,0^p) must read >=p distinct original source-bit groups; otherwise identical branch accepts a SAT single-flip neighbour.',
     'source_model':'fixed-length, proper signed ordinary 3CNF binary indexed input. Nonuniform witness choices are free, but all source probes are charged.',
     'source_file_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'records':rows,
     'finite_controls':{'root_cases_checked':tested,'SAT':sat,'UNSAT':unsat,'single_flips_checked':sensitive,'blind_probe_masks_checked':blind,'formula_assertions':checks,'failed':0},
     'two_algorithm':{
       'primary':'van Melkebeek ECCC TR07-099 Theorem 1.3 (2007), conditions (c-1)d<1 OR cd(d-1)-2d+1<0',
       'near_boundary_d':'901/500',
       'F_901_500':str(f),
       'C_901_500':str(g),
       'C_901_500_approx':float(g),
       'branch_switch_at_d':2,
       'exact_frontier_law':'H(d)=max(1+1/d,(2d-1)/(d(d-1))), d>1; C(d)-F(d)=(2-d)/(d-1)',
       'cases_checked':high,
       'sample':[{'d':str(Q(n,d)),'frontier1':str(frontier(Q(n,d))[0]),'frontier2':str(frontier(Q(n,d))[1]),'best':str(frontier(Q(n,d))[2])}
                  for n,d in [(901,500),(2,1),(3,1),(10,1)]]
     },
     'limitations':[
       'This is a near-linear source-probe lower bound for nondeterministic accepting UNSAT branches, not a superlinear or total UNSAT certificate volume lower bound.',
       'The coNTIME theorem also requires a separate deterministic SAT solver with simultaneous small-space bound and theorem-qualified input encoding.',
       'Promise parity has a near-linear-time logarithmic-space checker; no contradiction results.',
       'The proof is on ordinary proper signed 3CNF; exact-(2,2) and clause-monotone transfer require separately charged audited reductions.',
       'No all-UNSAT affordable certificate coverage, arbitrary-K seed transition, or P != NP result follows.'
     ],
     'duration_seconds':round(time.perf_counter()-t,4)
    }
    OUT.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:summary[k] for k in ['run','finite_controls','duration_seconds']},indent=2))

if __name__=='__main__': main()
