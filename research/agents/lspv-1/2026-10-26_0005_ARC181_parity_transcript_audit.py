#!/usr/bin/env python3
"""ARC181: one-bit SAT parity family and checkpoint transcript firewall.

Run: python 2026-10-26_0005_ARC181_parity_transcript_audit.py
The finite test is reproducible using Python 3.10+ standard library only.
All generated ordinary formulas use proper 3-literal clauses with fixed
incidence; only the signs of four clauses per input bit depend on the bit.
A mathematical proof, not finite runs, establishes the all-p transcript
lower bound. No physical FLMV time/space measurement is claimed.
"""
from __future__ import annotations
from itertools import product
from pathlib import Path
import json, hashlib, math, time

RUN = 'ARC181-PARITY-TRANSCRIPT-FIREWALL'
OUTPUT = Path(__file__).with_name('2026-10-26_0005_ARC181_results.json')

def unit3(lit:int, a:int,b:int):
    return tuple((lit, sa*a, sb*b) for sa,sb in product((1,-1),repeat=2))

def xor3(a:int,b:int,z:int):
    # Retain exactly assignments satisfying z = (a XOR b).
    # A CNF clause forbids precisely one of eight truth assignments.
    return tuple(tuple(v if not bit else -v for v,bit in zip((a,b,z),bits))
                 for bits in product((0,1),repeat=3)
                 if bits[2] != (bits[0] ^ bits[1]))

def family(bits):
    p=len(bits)
    if p<2: raise ValueError('p>=2')
    cs=[]
    for i,bit in enumerate(bits):
        x=i+1; a=p+2*i+1; b=p+2*i+2
        cs.extend(unit3(x if bit else -x,a,b))
    for j in range(p-1):
        left=j+1 if j==0 else 3*p+j
        right=j+2
        out=3*p+j+1
        cs.extend(xor3(left,right,out))
    cs.extend(unit3(4*p-1,4*p,4*p+1))
    assert len(cs)==8*p
    assert all(len(c)==3 and len({abs(l) for l in c})==3 for c in cs)
    return tuple(cs),4*p+1

def is_model(clauses,assignment):
    return all(any((assignment[abs(l)] == (l>0)) for l in c) for c in clauses)

def brute(clauses,n):
    for bits in product((False,True),repeat=n):
        assn={i+1:bits[i] for i in range(n)}
        if is_model(clauses,assn):return assn
    return None

def dpll(clauses):
    initial=[frozenset(c) for c in clauses]
    def solve(cs,assign):
        cs=[set(c) for c in cs]
        while True:
            if any(not c for c in cs):return None
            if not cs:return dict(assign)
            singles=[next(iter(c)) for c in cs if len(c)==1]
            if not singles:break
            l=singles[0]
            k,v=abs(l),l>0
            if k in assign and assign[k]!=v:return None
            assign=dict(assign);assign[k]=v
            cs=[c for c in cs if l not in c]
            cs=[c-{-l} for c in cs]
        lit=min(next(iter(c)) for c in cs if c)
        for v in (True,False):
            l=abs(lit) if v else -abs(lit)
            nx=[c for c in cs if l not in c]
            nx=[c-{-l} for c in nx]
            ans=solve(nx,{**assign,abs(lit):v})
            if ans is not None:return ans
        return None
    return solve(initial,{})

def encoded(clauses,n):
    m=len(clauses)
    w=max(1,(max(n,m)+1).bit_length())
    # Fixed-width compact binary literal slots, position of sign is explicit.
    header=f'{n:0{w}b}{m:0{w}b}'
    slots=''.join(('0' if l>0 else '1')+f'{abs(l):0{w}b}' for c in clauses for l in c)
    return header+slots,w

def raw_bit_locations(encoded,w,m):
    # Sign field offsets for the 1st literal in 4 forcing clauses of each input bit.
    return [tuple(2*w + ((4*i+j)*3)*(w+1) for j in range(4))
            for i in range(m//8)]

def NAND(a,b):return not(a and b)

def nand_xor(a,b):
    t=NAND(a,b);u=NAND(a,t);v=NAND(b,t)
    return NAND(u,v)

def parity_nand(bits):
    layer=list(map(bool,bits)); gates=0
    while len(layer)>1:
        nx=[]
        for i in range(0,len(layer),2):
            if i+1<len(layer):nx.append(nand_xor(layer[i],layer[i+1]));gates+=4
            else:nx.append(layer[i])
        layer=nx
    return layer[0],gates

def run():
    tic=time.perf_counter();checks=0
    def ck(cond, msg='assertion failed'):
        nonlocal checks
        if not cond:raise AssertionError(msg)
        checks+=1
    records=[];roots=0;unsat=0;sat=0;exhaustive=0;dpll_cases=0;flips=0
    max_n=0;max_m=0;transcript_total=0
    for p in range(2,9):
        code_to_bits={};labels={};locs=None
        for bs in product((False,True),repeat=p):
            cs,n=family(bs);roots+=1
            ck(n==4*p+1 and len(cs)==8*p)
            ck(len(set(cs))==len(cs),'source duplicate')
            binary,w=encoded(cs,n)
            offsets=raw_bit_locations(binary,w,len(cs))
            ck(len(offsets)==p)
            for i,positions in enumerate(offsets):
                ck(len(set(positions))==4)
                ck(all(binary[j]==('0' if bs[i] else '1') for j in positions))
            expect=sum(bs)%2==1
            answer=dpll(cs);dpll_cases+=1
            ck((answer is not None)==expect,'DPLL parity mismatch')
            if answer:
                # DPLL's assignment can omit irrelevant auxiliary variables.
                witness={i:answer.get(i,False) for i in range(1,n+1)}
                ck(is_model(cs,witness),'DPLL witness incomplete')
                sat+=1
            else:unsat+=1
            if p<=3:
                witness=brute(cs,n);exhaustive+=1
                ck((witness is not None)==expect,'exhaustive parity mismatch')
            # read the first sign bit of each forcing group in canonical order.
            transcript=tuple((i,binary[offsets[i][0]]) for i in range(p))
            code_to_bits[bs]=binary
            labels[bs]=expect
            ck(tuple(char=='0' for _,char in transcript)==bs)
            gate_output,gates=parity_nand(bs)
            ck(gate_output==expect and gates==4*(p-1))
            max_n=max(max_n,n);max_m=max(max_m,len(cs))
            if locs is None:locs=offsets
        ck(len({tuple((i,code_to_bits[bs][locs[i][0]]) for i in range(p))
                for bs in code_to_bits})==2**p, 'transcript injectivity')
        transcript_total+=2**p
        # A single toggled input bit alters exactly 4 sign fields, none outside that input group.
        for bs,code in code_to_bits.items():
            for i in range(p):
                flip=list(bs);flip[i]=not flip[i];flip=tuple(flip)
                changed={j for j,(a,b) in enumerate(zip(code,code_to_bits[flip])) if a!=b}
                ck(changed==set(locs[i]),'local source sign sensitivity')
                ck(labels[bs] != labels[flip])
                flips+=1
        records.append({'p':p,'source_variables':4*p+1,'source_clauses':8*p,
                        'bits_in_input_encoding':len(next(iter(code_to_bits.values()))),
                        'promised_formulas':2**p,'distinct_transcripts':2**p,
                        'minimum_source_bit_probes':p,
                        'nand_gates':4*(p-1),
                        'nand_depth_upper_bound':3*math.ceil(math.log2(p)),
                        'single-bit_changes_tested':p*2**p,
                        'sat':sum(labels.values()),'unsat':2**p-sum(labels.values())})
    result={
      'run':RUN, 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'source_type':'proper signed ordinary 3CNF, fixed incidence and length',
      'mathematical_result':'Input-independent initial state forces p group queries and 2^p distinct full answer transcripts, although the SAT output is one bit.',
      'counterexample_scope':'The statement number-of-decision-labels <=2 remains true; the inference number-of-required-initial-transcripts <=2 is false.',
      'data':records,'checks':checks,'failed_checks':0,'roots':roots,'sat':sat,'unsat':unsat,
      'exhaustive_roots':exhaustive,'dpll_cases':dpll_cases,
      'single_bit_flips_checked':flips,'distinct_transcripts_total':transcript_total,
      'max_variables':max_n,'max_clauses':max_m,
      'limitations':[
        'Finite tests are not an all-SAT runtime lower bound.',
        'The transcript lower bound holds at an initial checkpoint independent of the input bits, not after arbitrary charged preprocessing.',
        'The full Boolean SAT decision circuits on this promise family are linear size; the number of transcripts does not lower-bound circuit size.',
        'Transfer to signed exact-(2,2) via virtual regularization depends on the separately declared source-fixed-incidence compiler; not verified here.',
        'No universal all-UNSAT certificate coverage, FLMV strict-box algorithm, or P!=NP result.'
      ],
      'elapsed_seconds':round(time.perf_counter()-tic,4)
    }
    OUTPUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:result[k] for k in ('run','roots','sat','unsat','exhaustive_roots','dpll_cases','single_bit_flips_checked','checks','failed_checks','elapsed_seconds')},indent=2))

if __name__=='__main__':run()
