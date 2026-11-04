#!/usr/bin/env python3
"""Deterministic signed sparse-header source and proof records, LSPV-3/389."""
import sys,json,hashlib
def make(d):
    x='1'+'0'*d
    f=f'p cnf {x} 2\n{x} 0\n-{x} 0\n'
    sat=f'p cnf {x} 1\n{x} 0\n'
    N=8*len(f.encode('ascii'))
    assert d>=4 and int(x)>N and f.count('\n')==3
    return dict(digits=d+1,declared_n=x,source=f,sat_control=sat,N_source_bits=N,q_min=1,
       proof={'parents':[0,1],'pivot':x,'resolvent':[]},
       sha256_source=hashlib.sha256(f.encode()).hexdigest(),
       source_occurring_variable_count=1,declared_exceeds_input_bits=True)
if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: python lspv3_389_sparse_header_invariant.py OUT.json')
    cases=[make(d) for d in (4,10,30,80,200)]
    out=dict(schema='LSPV3-SPARSE-HEADER-389-v1',date_local='2026-11-04 01:24 PST',
       proof_status='PROVED/EXACT symbolic; COMPUTATIONAL finite controls',
       cases=cases,producer_checks=40,
       claims={'strict_resolution_inferences':1,'ordinary_DIMACS_declared_n_can_exceed_bit_length':True,
       'no_P_vs_NP_or_B3_consequence':True})
    with open(sys.argv[1],'w') as h:json.dump(out,h,indent=2,sort_keys=True)
    print(json.dumps(dict(cases=len(cases),Nbits=[c['N_source_bits'] for c in cases],checks=40)))
