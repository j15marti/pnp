#!/usr/bin/env python3
"""RESOURCE-CORESEARCH8: finite off-image diagonal using finite-field trace tables.
Exhaustive across every coefficient vector, seed, and output position for each
listed public adaptive/nonadaptive two-probe decoder. No SAT/P!=NP inference.
Python 3 standard library. Deterministic, no random seed.
"""
from __future__ import annotations
import hashlib, itertools, json, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def gf_mul(a:int, b:int, poly:int, n:int)->int:
    mask = (1<<n)-1
    z=0
    for _ in range(n):
        if b&1: z ^= a
        b >>= 1
        a <<= 1
        if a & (1<<n): a ^= poly
        a &= mask
    return z

def trace(x:int, poly:int, n:int)->int:
    a=x; out=0
    for _ in range(n):
        out ^= a
        a = gf_mul(a,a,poly,n)
    assert out in (0,1)
    return out

def trace_codewords(n:int,k:int,poly:int):
    Q=1<<n; words={}; ntested=0
    for coeff in itertools.product(range(Q),repeat=k):
        word=0
        for x in range(Q):
            p=0
            for a in coeff[::-1]: p = gf_mul(p,x,poly,n)^a
            word |= trace(p,poly,n)<<x
        words.setdefault(word,coeff)
        ntested += 1
    return words,ntested

# Each query coordinate has a deterministic tree encoded as callable
# (q,z) -> bit, with depth at most two and seed length S.
def make_decoders(Q,S,codewords):
    dec=[]
    dec.append(('zero',lambda q,z:0))
    dec.append(('one',lambda q,z:1))
    dec.append(('alternating',lambda q,z:q&1))
    dec.append(('constant_seed',lambda q,z:z&1))
    dec.append(('xor_adjacent',lambda q,z:((z>>(q%S))&1)^((z>>((q+1)%S))&1)))
    dec.append(('and_offsets',lambda q,z:((z>>(q%S))&1)&((z>>((q+1)%S))&1)))
    dec.append(('adaptive_mux',lambda q,z:((z>>((q+1+(z>>(q%S)&1))%S))&1)))
    dec.append(('nonlinear_mixed',lambda q,z:((z>>(q%S))&1)|((z>>((q+1)%S))&1)))
    ordered=sorted(codewords)
    if S==2:
        lookup={z: ordered[z] for z in range(4)}
        dec.append(('promise_columns_encoded',lambda q,z: (lookup[z]>>q)&1))
    return dec

def run(n:int,k:int,poly:int,S:int)->dict:
    start=time.monotonic(); Q=1<<n
    words,all_coeff=trace_codewords(n,k,poly)
    decoders=make_decoders(Q,S,words)
    assert len(words)>1<<S
    block_words=[]; cases=[]; seed_checks=0; clause_checks=0; core_checks=0
    for name,gen in decoders:
        images=set(); seed_maps=[]
        for z in range(1<<S):
            word=sum(gen(q,z)<<q for q in range(Q))
            images.add(word); seed_maps.append(word)
        chosen=next(word for word in sorted(words) if word not in images)
        assert chosen not in images
        block_words.append(chosen)
        core=set(range(Q))
        for q in range(Q):
            candidate=core-{q}
            if all(any((chosen^gw)&(1<<j) for j in candidate) for gw in seed_maps):
                core=candidate
        assert all(any((chosen^gw)&(1<<j) for j in core) for gw in seed_maps)
        for z in range(1<<S):
            assert any(((chosen>>q)&1)!=gen(q,z) for q in range(Q))
            seed_checks+=1
            assert any(((chosen>>q)&1)!=gen(q,z) for q in core)
            core_checks+=1
        cases.append({'decoder':name,'seed_bits':S,'image_cardinality':len(images),
                     'chosen_database_coefficients':list(words[chosen]),
                     'chosen_block_int':chosen,'chosen_core_coordinates':sorted(core),
                     'core_size':len(core),'small_offimage_core_bound':min(Q,4*S-2)})
        assert len(core)<=min(Q,4*S-2)
    H=sum(w<<(j*Q) for j,w in enumerate(block_words))
    for j,(name,gen) in enumerate(decoders):
        for z in range(1<<S):
            outputs=sum(gen(q,z)<<q for q in range(Q))
            assert outputs!=((H>>(j*Q))&((1<<Q)-1))
            clause_checks+=1
    return {'n':n,'k':k,'field_polynomial':hex(poly),'Q':Q,'seed_bits':S,
            'coefficient_vectors_exhausted':all_coeff,
            'distinct_KPI_trace_columns':len(words),
            'number_of_public_decoders':len(decoders),'assembled_target_bits':Q*len(decoders),
            'image_offrange_seed_checks':seed_checks,
            'certificate_seed_checks':core_checks,
            'diagonal_global_seed_checks':clause_checks,
            'case_results':cases,
            'elapsed_seconds':round(time.monotonic()-start,3)}

def main():
    t=time.monotonic()
    results=[run(3,2,0b1011,2),run(4,3,0b10011,3)]
    data={'run_id':'RESOURCE-CORESEARCH8','timestamp_kst':'2026-10-18 19:25',
          'test_type':'exhaustive coefficient vectors, deterministic seed verification and greedy off-image cores',
          'results':results,'total_elapsed_seconds':round(time.monotonic()-t,3),
          'limitations':['Small finite examples do not establish KPI asymptotic lower bounds',
                         'No arbitrary-machine time lower bound, SAT reduction, or P != NP theorem',
                         'Toy two-probe decoders only; asymptotic universal decoder treated symbolically',
                         'This tests decoder-specific complete-block exclusion, not a uniform global memory cell set']}
    data['code_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    path=ROOT/'2026-10-18_RESOURCE_CORESEARCH8_summary.json'
    path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'out':str(path),'sha256':data['code_sha256'],
       'cases':[(r['Q'],r['number_of_public_decoders'],r['distinct_KPI_trace_columns'],r['elapsed_seconds']) for r in results],
       'seconds':data['total_elapsed_seconds']}))

if __name__=='__main__':main()
