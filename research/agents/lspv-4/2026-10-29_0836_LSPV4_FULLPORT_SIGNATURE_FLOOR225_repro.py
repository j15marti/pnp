#!/usr/bin/env python3
"""Independent all-port signature counting barrier audit (stdlib only).

PROVED mathematical claims are documented separately in the LaTeX report.
Finite tests compare direct existential evaluation, resolution, and compact form.
No general SAT complexity claim is made.
"""
from __future__ import annotations
from itertools import product
from pathlib import Path
from hashlib import sha256
import json, math, random

OUT = Path(__file__).with_name('2026-10-29_0836_LSPV4_FULLPORT_SIGNATURE_FLOOR225_raw.json')

def unpack(t: int, code: int):
    """Tuple (a0,b0,c0,d0,a1,b1,c1,d1,...)."""
    return tuple((code >> j) & 1 for j in range(4*t))

def a_clause(signs, i, v):
    a,b = v[4*i:4*i+2]
    return bool((a ^ signs[i]) | b)

def b_clause(i,v):
    c,d=v[4*i+2:4*i+4]
    return bool(c|d)

def full_with_z(signs, v, z):
    t=len(signs)
    return all(z or a_clause(signs,i,v) for i in range(t)) and all((not z) or b_clause(i,v) for i in range(t))

def projection(signs, v):
    return full_with_z(signs,v,0) or full_with_z(signs,v,1)

def compact(signs,v):
    return all(a_clause(signs,i,v) for i in range(len(signs))) or all(b_clause(i,v) for i in range(len(signs)))

def resolvents(signs,v):
    return all(a_clause(signs,i,v) or b_clause(j,v) for i in range(len(signs)) for j in range(len(signs)))

def witness(t, s, u):
    """Deterministically construct port vector distinguishing sign patterns."""
    i=next(j for j in range(t) if s[j]!=u[j])
    v=[0]*(4*t)
    for j in range(t):
        v[4*j+1]=int(j!=i)  # other A_j trivially true
        v[4*j+2]=1          # all but B_0 true
    v[2]=0                 # force B_0 false (c_0=d_0=0)
    v[3]=0
    v[4*i]=1 ^ s[i]        # (a_i xor s_i) true; xor u_i false
    return v

def cnf_text(signs):
    t=len(signs);z=4*t+1
    lines=[f'p cnf {z} {2*t}']
    for i,sign in enumerate(signs):
        a=4*i+1;b=4*i+2;c=4*i+3;d=4*i+4
        lines.append(f'{z} {(-a if sign else a)} {b} 0')
        lines.append(f'{-z} {c} {d} 0')
    return '\n'.join(lines)+'\n'

def self_delim_child(signs):
    # Unary length+separator makes overhead O(t); use conventional binary-size header instead.
    t=len(signs)
    width=max(1,t.bit_length())
    # Elias gamma encoding of t (prefix zeros and binary t) + t sign bits.
    gamma=('0'*(width-1))+format(t,'b')
    return gamma+''.join(str(x) for x in signs)

def run():
    checks=0
    fixed_assignment_checks=0
    signature_assignment_checks=0
    signature_uniqueness_counts={}
    witness_pair_checks=0
    sizes=[]
    for t in range(1,5):
        patterns=[tuple((k>>i)&1 for i in range(t)) for k in range(1<<t)]
        # Original handoff control: exactly sum_t 2^(4t) = 69,904 assignments.
        signs=(0,)*t
        for code in range(1<<(4*t)):
            v=unpack(t,code)
            a=projection(signs,v);b=compact(signs,v);c=resolvents(signs,v)
            assert a==b==c, (t,code,a,b,c)
            checks+=2;fixed_assignment_checks+=1
        unique=set()
        for sig in patterns:
            h=sha256()
            # Full all-port semantic fingerprints for all 2^t source formulas.
            for code in range(1<<(4*t)):
                v=unpack(t,code)
                h.update(bytes([int(compact(sig,v))]))
                signature_assignment_checks+=1
            unique.add(h.hexdigest())
        assert len(unique)==2**t
        signature_uniqueness_counts[str(t)]=len(unique)
        checks+=len(unique)
    # Pairwise mathematical distinguishing witnesses, exhaustive for t <= 8.
    for t in range(1,9):
        pats=[tuple((k>>i)&1 for i in range(t)) for k in range(1<<t)]
        for pidx,s in enumerate(pats):
            for u in pats[pidx+1:]:
                v=witness(t,s,u)
                assert compact(s,v) != compact(u,v)
                witness_pair_checks+=1;checks+=1
    rng=random.Random(20261029)
    for t in (12,24,48):
        for _ in range(500):
            s=tuple(rng.randrange(2) for _ in range(t))
            u=tuple(rng.randrange(2) for _ in range(t))
            if s==u:
                u=tuple((1-x if i==0 else x) for i,x in enumerate(s))
            v=witness(t,s,u)
            assert compact(s,v)!=compact(u,v)
            checks+=1;witness_pair_checks+=1
    for t in (1,2,4,8,16,32,64,128,256,512):
        signs=tuple((i%2) for i in range(t))
        src=cnf_text(signs)
        child=self_delim_child(signs)
        max_consecutive_bits=t
        sizes.append({
            't':t,'n_vars':4*t+1,'n_clauses':2*t,
            'canonical_dimacs_ascii_bytes':len(src.encode()),
            'compact_sign_child_bits':len(child),
            'all_signs_count':str(2**t),
            'counting_minimax_lower_bound_bits':max_consecutive_bits,
            'resolution_clause_count':t*t,
            'source_hex_sha256':sha256(src.encode()).hexdigest(),
        })
        assert len(child)>=t and len(src)>0
        checks+=1
    assert fixed_assignment_checks==69904
    out={
        'status':'PASS', 'claim_type':'Finite computational controls, not kernel verified',
        'fixed_sign_elimination_assignments':fixed_assignment_checks,
        'all_signatures_truth_table_assignments':signature_assignment_checks,
        'exhaustive_distinguishing_witnesses':witness_pair_checks-1500,
        'random_large_witnesses':1500,
        'total_witness_pair_checks':witness_pair_checks,
        'total_assertion_units':checks,
        'distinct_signatures_by_t':signature_uniqueness_counts,
        'size_series':sizes,
        'library_audit_reference_sha256':'05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca',
        'limitations':['All-port exact semantic preservation only, not SAT decision preservation','Family is satisfiable for every sign pattern','No exact22 occurrence guarantee','Generated signatures are deliberately restricted and easy to evaluate','Finite tests do not prove asymptotics'],
    }
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ('size_series','limitations')},indent=2))

if __name__=='__main__':run()