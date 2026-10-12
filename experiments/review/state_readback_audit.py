#!/usr/bin/env python3
"""STATE_READBACK1: exact checkpoint/readback rank audit and clean-core control.

Standard library only. Every invocation has a 25-second cooperative alarm.
The Hamming scheme answers a specified fully-pinned compatibility subservice,
NOT arbitrary partial-assignment SAT queries. Probe counts concern the immutable
source only; query reads, preprocessing and work bits are reported separately.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
import math
import random
import signal
import time
from collections import Counter
from functools import lru_cache
from pathlib import Path

START = time.monotonic()
CHECKS = Counter()

def alarm_handler(signum, frame):
    raise TimeoutError('25-second cooperative budget exceeded; split invocation')
signal.signal(signal.SIGALRM, alarm_handler)
signal.alarm(25)

def check(ok: bool, label: str) -> None:
    CHECKS[label] += 1
    if not ok:
        raise AssertionError(label)

F0 = ((1,2,3),(1,2,4),(3,5,6),(4,5,6),
      (-1,-2,-3),(-1,-2,-4),(-3,-5,-6),(-4,-5,-6))
F1 = ((1,2,3),(1,2,4),(3,5,6),(4,5,6),
      (-1,-2,-4),(-1,-2,-5),(-3,-4,-6),(-3,-5,-6))

def satisfies(f, assignment: int) -> bool:
    return all(any(bool((assignment >> (abs(l)-1)) & 1) == (l > 0)
                   for l in c) for c in f)

def models(f, n):
    return {a for a in range(1 << n) if satisfies(f, a)}

M0, M1 = models(F0,6), models(F1,6)
A0, A1, COMMON = min(M0-M1), min(M1-M0), min(M0 & M1)

def core_ok(f) -> bool:
    variables = {abs(l) for c in f for l in c}
    pos, neg = Counter(l for c in f for l in c if l>0), Counter(-l for c in f for l in c if l<0)
    return (len(set(f)) == len(f) and all(len(c)==3 and len({abs(l) for l in c})==3
         and (all(l>0 for l in c) or all(l<0 for l in c)) for c in f)
         and all(pos[v]==neg[v]==2 for v in variables))

@lru_cache(maxsize=256)
def core_formula(word: int, m: int):
    positive, negative = [], []
    for block in range(m):
        f = F1 if (word >> block)&1 else F0
        shifted = [tuple((abs(l)+6*block)*(1 if l>0 else -1) for l in c) for c in f]
        positive.extend(shifted[:4]); negative.extend(shifted[4:])
    return tuple(positive+negative)

def gamma(n: int) -> str:
    assert n > 0
    word = bin(n)[2:]
    return '0'*(len(word)-1)+word

def encode(f) -> str:
    n = max(abs(l) for c in f for l in c)
    w = max(1,n.bit_length())
    return gamma(n)+gamma(len(f)+1)+''.join(('0' if l>0 else '1')+format(abs(l), f'0{w}b') for c in f for l in c)

def selector_address(m: int, j: int) -> int:
    w = (6*m).bit_length()
    header = len(gamma(6*m))+len(gamma(8*m+1))
    row = 4*m+4*j
    return header+3*(row+1)*(1+w)-1

def preprocess_template(bits: str):
    """Validate every encoded bit, then erase the decoded selector after sketching.
    Stores only one 4-clause negative block and an m-bit selector temporarily.
    Returns summary, public block count and exact source-read count.
    """
    cursor=0
    def read():
        nonlocal cursor
        if cursor>=len(bits) or bits[cursor] not in '01':
            raise ValueError('truncated or nonbinary source')
        value=int(bits[cursor]); cursor+=1
        return value
    def integer(width):
        value=0
        for _ in range(width): value=(value<<1)|read()
        return value
    def gamma_read():
        zeros=0
        while read()==0:
            zeros+=1
            if zeros>len(bits).bit_length(): raise ValueError('oversized gamma header')
        return (1<<zeros)|integer(zeros)
    n=gamma_read(); clauses=gamma_read()-1
    if n%6 or n<18: raise ValueError('not a block template')
    m=n//6
    w=max(1,n.bit_length())
    if cursor+24*m*(1+w)!=len(bits): raise ValueError('template length mismatch')
    dimensions(m)
    if clauses!=8*m: raise ValueError('wrong clause count')
    w=max(1,n.bit_length())
    def clause():
        out=[]
        for _ in range(3):
            sign=read(); v=integer(w)
            if not 1<=v<=n: raise ValueError('bad variable')
            out.append(-v if sign else v)
        return tuple(out)
    for j in range(m):
        for row in F0[:4]:
            if clause()!=tuple(v+6*j for v in row): raise ValueError('bad positive block')
    word=0
    for j in range(m):
        block=tuple(clause() for _ in range(4))
        expected0=tuple(tuple(-(abs(v)+6*j) for v in row) for row in F0[4:])
        expected1=tuple(tuple(-(abs(v)+6*j) for v in row) for row in F1[4:])
        if block==expected1: word|=1<<j
        elif block!=expected0: raise ValueError('bad negative block')
    if cursor!=len(bits): raise ValueError('trailing bits')
    summary=summarize(word,m)
    del word
    return summary,m,cursor

def contextual_assignment(word: int, m: int) -> int:
    return sum((A1 if (word>>j)&1 else A0) << (6*j) for j in range(m))

def syndrome(word: int, m: int) -> int:
    value = 0
    for i in range(1,m+1):
        if (word>>(i-1))&1:
            value ^= i
    return value

def dimensions(m: int):
    r = (m+1).bit_length()-1
    if m != (1<<r)-1 or r < 2:
        raise ValueError('m must equal 2^r-1 for r>=2')
    data_positions = (i for i in range(1,m+1) if i&(i-1))
    return r, data_positions

def summarize(word: int, m: int) -> int:
    _, data = dimensions(m)
    error = syndrome(word,m)
    center = word ^ (1<<(error-1)) if error else word
    packed = sum(((center>>(i-1))&1)<<j for j,i in enumerate(data))
    return (packed<<1) | int(error!=0)

def center_from_summary(summary: int, m: int) -> int:
    r, data = dimensions(m)
    center = sum(((summary>>(j+1))&1)<<(i-1) for j,i in enumerate(data))
    syn = syndrome(center,m)
    for j in range(r):
        if (syn>>j)&1:
            center ^= 1<<((1<<j)-1)
    return center

def answer(summary: int, query: int, m: int, read_source_bit):
    """Return (exact equality bit, source-probe count). Query is read-only."""
    if summarize(query,m) != summary:
        return False, 0
    if summary&1 == 0:
        return True, 0
    j = syndrome(query,m)-1
    assert 0 <= j < m
    return read_source_bit(j) == ((query>>j)&1), 1

def test_hamming(m: int, exhaustive: bool, seed: int):
    r,_ = dimensions(m)
    B = m-r+1
    groups = {}
    for x in range(1<<m):
        s = summarize(x,m)
        groups.setdefault(s,[]).append(x)
        c = center_from_summary(s,m)
        check(syndrome(c,m)==0 and (x^c).bit_count() <= 1, 'hamming_center')
        check(s < (1<<B), 'summary_bit_budget')
    check(len(groups)==1<<B, 'summary_count')
    check(set(map(len,groups.values()))=={1,m}, 'fiber_sizes')
    probe_hist = Counter()
    if exhaustive:
        pairs = itertools.product(range(1<<m), repeat=2)
    else:
        rng = random.Random(seed)
        pairs = itertools.chain(((x,x) for x in range(1<<m)),
            ((x,y) for s,xs in groups.items() for x in xs for y in xs),
            ((rng.randrange(1<<m),rng.randrange(1<<m)) for _ in range(4096)))
    count = 0
    for x,y in pairs:
        observed=[]
        def read(j):
            observed.append(j)
            return (x>>j)&1
        result, probes = answer(summarize(x,m),y,m,read)
        check(result == (x==y), 'hamming_exact_answer')
        check(probes == len(observed) and probes <= 1, 'hamming_probe_budget')
        probe_hist[probes] += 1; count += 1
    check((1<<m) <= (1<<B)*(m+1), 'repaired_rank_bound')
    if m>=7:
        check(B+1<m, 'additive_B_plus_q_counterexample')
    return {'m':m, 'summary_bits_B':B, 'max_source_bit_probes_q':1,
            'source_count':1<<m,'fibers':len(groups),'fiber_sizes':[1,m],
            'pairs_checked':count,'probe_histogram':dict(probe_hist),
            'B_plus_q':B+1,'log2_rank_H':m,
            'rank_bound_rhs':(1<<B)*(m+1),
            'preprocessing_cost':'All source bits read; O(m^2) conservative integer bit work for sketching, plus encoded parsing',
            'query_cost':'O(m^2) conservative integer bit work and O(m) temporary bits; query reads charged separately',
            'warning':'B is retained checkpoint/advice, not total query workspace'}

def test_core(m: int):
    check(core_ok(F0) and core_ok(F1), 'base_signed_core')
    check(A0 in M0-M1 and A1 in M1-M0 and COMMON in M0&M1,'base_contexts')
    n_sources=1<<m
    all_queries = [contextual_assignment(y,m) for y in range(n_sources)]
    source_probes=0; pairs=0; N=None
    for x in range(n_sources):
        f=core_formula(x,m); bits=encode(f); N=len(bits)
        check(core_ok(f),'product_signed_core')
        common = sum(COMMON << (6*j) for j in range(m))
        check(satisfies(f,common),'all_sources_common_SAT_witness')
        recovered=0
        for j in range(m):
            bit=1-int(bits[selector_address(m,j)])
            check(bit==((x>>j)&1),'actual_CNF_bit_accessor')
            recovered |= bit<<j
        check(recovered==x,'source_template_decode')
        s, public_m, reads = preprocess_template(bits)
        check(public_m==m and reads==len(bits) and s==summarize(recovered,m), 'full_source_preprocessing_scan')
        for y, assignment in enumerate(all_queries):
            used=[]
            def read(j):
                address=selector_address(m,j)
                used.append(address)
                return 1-int(bits[address])
            got,q=answer(s,y,m,read)
            actual=satisfies(f,assignment)
            check(got==actual==(x==y),'CNF_compatibility_identity')
            check(q==len(used)<=1,'CNF_actual_bit_probe_budget')
            source_probes+=q; pairs+=1
    malformed=0
    sample=encode(core_formula(0,m))
    for broken in (sample[:-1], sample+'0', '2'+sample[1:], sample[:30]+'2'+sample[31:]):
        try: preprocess_template(broken)
        except ValueError: malformed+=1
    check(malformed==4,'malformed_template_rejected')
    return {'m_blocks':m,'variables':6*m,'clauses':8*m,'source_formulas':n_sources,
            'encoded_source_bits_N':N,'pairs_checked':pairs,'post_cut_source_bit_probes':source_probes,
            'compatibility_submatrix':'identity','exact_rank':1<<m,'SAT_answers':'all YES',
            'exclusive_assignment_a0':A0,'exclusive_assignment_a1':A1,'common_assignment':COMMON,
            'scope':'disconnected products inside signed Monotone 3SAT-(2,2); contexts fully pin all variables',
            'preprocessing_source_reads_per_input':N,
            'full_partial_compatibility_service_implemented':False}

def evaluate_tree(tree,x):
    if isinstance(tree,int): return tree
    i,left,right=tree
    return evaluate_tree(right if ((x>>i)&1) else left,x)

def tree(rng,n,depth,available=None):
    if depth==0: return rng.randrange(2)
    available=tuple(range(n)) if available is None else available
    i=rng.choice(available)
    rest=tuple(j for j in available if j!=i)
    return (i,tree(rng,n,depth-1,rest),tree(rng,n,depth-1,rest))

def degree_from_values(values,n):
    coeff=list(values)
    for i in range(n):
        for mask in range(1<<n):
            if mask>>i&1:
                coeff[mask]-=coeff[mask^(1<<i)]
    return max((mask.bit_count() for mask,v in enumerate(coeff) if v),default=0)

def rank_integer(rows):
    """Exact rational rank using fraction-free row elimination and gcd reduction."""
    a=[list(map(int,row)) for row in rows]; rank=0
    if not a: return 0
    for j in range(len(a[0])):
        pivot=next((i for i in range(rank,len(a)) if a[i][j]),None)
        if pivot is None: continue
        a[rank],a[pivot]=a[pivot],a[rank]
        for i in range(rank+1,len(a)):
            if not a[i][j]: continue
            p,v=a[rank][j],a[i][j]
            a[i]=[p*x-v*y for x,y in zip(a[i],a[rank])]
            g=math.gcd(*a[i])
            if g>1: a[i]=[x//g for x in a[i]]
        rank+=1
        if rank==len(a): break
    return rank

def test_rank(seed: int):
    rng=random.Random(seed); cells=[]
    for n in range(1,7):
        for q in range(0,min(n,3)+1):
            for B in (0,1,2):
                for trial in range(3):
                    labels=[rng.randrange(1<<B) for _ in range(1<<n)]
                    qcount=12
                    trees={(s,j):tree(rng,n,q) for s in set(labels) for j in range(qcount)}
                    for t in trees.values():
                        vals=[evaluate_tree(t,x) for x in range(1<<n)]
                        check(degree_from_values(vals,n)<=q,'adaptive_tree_degree')
                    H=[[evaluate_tree(trees[labels[x],j],x) for j in range(qcount)] for x in range(1<<n)]
                    R=rank_integer(H); dim=sum(math.comb(n,j) for j in range(q+1))
                    fiber_ranks=[]
                    for s in set(labels):
                        sr=rank_integer([H[x] for x in range(1<<n) if labels[x]==s])
                        check(sr<=dim,'state_fiber_rank_bound'); fiber_ranks.append(sr)
                    check(R<=sum(fiber_ranks)<=len(set(labels))*dim,'global_rank_bound')
                    cells.append({'n':n,'q':q,'B':B,'rank':R,'states':len(set(labels)),'dimension':dim})
    # Hypothesis guards: a query-dependent checkpoint is not preprocessing.
    n=3; H=[[int(x==y) for y in range(1<<n)] for x in range(1<<n)]
    check(rank_integer(H)==8>2,'query_dependent_checkpoint_invalidates_rank_bound')
    check(rank_integer(H)>sum(math.comb(n,j) for j in range(2)), 'whole_source_oracle_outside_bit_probe_model')
    return {'parameter_cells':len(cells),'cells':cells,
            'hypothesis_guards':['context available before preprocessing','uncharged whole-source equality oracle']}

def test_easy():
    families={
      'Horn':(((1,),(-1,2),(-2,3)),3),
      '2SAT':(((1,2),(-1,2),(-2,3)),3),
      'affine_parity':(((1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3)),3),
      'treewidth_one':(((1,2),(-2,3),(-3,4)),4),
      'independent_product':(((1,2),(-1,-2),(3,4),(-3,-4)),4),
      'UNSAT':(((1,),(-1,)),1),
      'redundant_padding':(((1,2,3),(1,2,3),(1,-1)),3),
      'signed_core':(F0,6)}
    for name,(f,n) in families.items():
        truth=models(f,n)
        for alpha in itertools.product((-1,0,1),repeat=n):
            expected=any(all(a==-1 or ((x>>i)&1)==a for i,a in enumerate(alpha)) for x in truth)
            # Separately evaluate the restricted CNF, without a SAT oracle.
            rf=[]
            for c in f:
                if any(alpha[abs(l)-1]!=-1 and (alpha[abs(l)-1]==1)==(l>0) for l in c): continue
                rf.append(tuple(l for l in c if alpha[abs(l)-1]==-1))
            actual=bool(models(rf,n))
            check(expected==actual,'easy_family_restriction_semantics')
        for label in ('DIRECT','COPY','DEAD','DELAY','INTERP','RECOMP'):
            # Extensional control only, not a timed simulation of each wrapper.
            check(bool(truth)==any(satisfies(f,x) for x in range(1<<n)),'wrapper_answer_identity')
        flipped=tuple(tuple(-l for l in c) for c in f)
        check(models(flipped,n)=={x^((1<<n)-1) for x in truth},'polarity_transport')
    return {'families':list(families),'wrapper_scope':'finite semantic identity checks, not measured machine runtimes'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mode', choices=['rank','core','hamming15','easy'],required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--seed',type=int,default=202610121659)
    args=p.parse_args()
    if args.mode=='rank': result=test_rank(args.seed)
    elif args.mode=='core': result={'hamming':test_hamming(7,True,args.seed),'core':test_core(7),'small':test_hamming(3,True,args.seed)}
    elif args.mode=='hamming15': result=test_hamming(15,False,args.seed)
    else: result=test_easy()
    out={'run_id':'STATE_READBACK1','mode':args.mode,'status':'COMPUTATIONAL','seed':args.seed,
         'checks':dict(CHECKS),'assertions':sum(CHECKS.values()),'failures':0,
         'elapsed_seconds':time.monotonic()-START,'cooperative_budget_seconds':25,
         'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'results':result,
         'limitations':['No unrestricted-SAT runtime lower bound.','Hamming upper bound is for selected fully-pinned equality contexts only.',
           'Retained checkpoint B is not total workspace.','Probe counts do not price all internal computation.',
           'No claim that a one-bit SAT decider must provide a later-query service.','Formal proof is not proof-assistant checked.']}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('mode','assertions','failures','elapsed_seconds','checks')},indent=2))
    signal.alarm(0)
if __name__=='__main__': main()
