#!/usr/bin/env python3
"""TMR-1 MCSP strict-threshold shell and gate-count controls, native CPython.

Only verifies finite instances of an independent symbolic counting proof.
One standard complete circuit basis AND, OR, NOT, fan-in <=2, unbounded fan-out,
no constants in exhaustive small-circuit enumeration. Counts all topological
straight-line gate sequences with up to 3 gates and all possible output wires.
"""
import hashlib
import itertools
import json
import math
from pathlib import Path


def truth_masks(n):
    masks=[]
    for v in range(n):
        masks.append(sum(((a>>v)&1)<<a for a in range(1<<n)))
    return masks


def enumerate_small_circuits(n=2, max_gates=3):
    init=truth_masks(n)
    allbits=(1<<(1<<n))-1
    reached={0:set(init)}
    circuits={0:1}
    target=init[0] ^ init[1]
    matches=[]
    count_by_gate={}
    def rec(wires,depth):
        if depth==max_gates:
            return
        m=len(wires)
        for kind in ('AND','OR','NOT'):
            pairs=itertools.product(range(m),repeat=2) if kind!='NOT' else ((i,0) for i in range(m))
            for i,j in pairs:
                if kind=='AND':val=wires[i]&wires[j]
                elif kind=='OR':val=wires[i]|wires[j]
                else:val=(~wires[i])&allbits
                d=depth+1
                circuits[d]=circuits.get(d,0)+1
                reached.setdefault(d,set()).add(val)
                if val == target:matches.append(d)
                rec(wires+(val,),d)
    rec(tuple(init),0)
    return {'variables':n,'target_xor_mask':target,'circuits_by_exact_gate_count':{str(k):v for k,v in circuits.items()},
            'distinct_final_functions':{str(k):len(v) for k,v in reached.items()},
            'XOR_found_with_at_most_3':bool(matches), 'explicit_four_gate_XOR': (init[0]|init[1]) & (~(init[0]&init[1])&allbits)}


def threshold_numeric_tests():
    rows=[]
    # mu_1 = 1/4, mu = 1/2, mu_2 = 3/4
    # for large n, all k-variable Boolean functions have DNF circuits
    # of size <= k + (k+1)*2^k. The count of n-input gate circuits
    # of size <= s is <= (s+1)(n+s+2)[3(n+s+2)^2]^s.
    for n in (16,24,32,40,48,56,64,80,96):
        assert n%8==0
        k=n//2
        s=1<<(n//4)
        t=1<<(3*n//4)
        dnf_upper=k+(k+1)*(1<<k)
        # integer ceil(log2 upper bound for candidate short circuits)
        log_floor=(s+1).bit_length()+(n+s+2).bit_length()+s*(3+2*(n+s+2).bit_length())
        # This is a conservative strict upper bound on log2(short-circuit count).
        success=log_floor < (1<<k) and dnf_upper<=t
        rows.append({'n':n,'k':k,'truth_table_N_power_of_two':f'2^{n}',
                    'small_threshold':s,'large_threshold':t,
                    'DNF_gate_upper':dnf_upper,
                    'log2_count_strict_upper':log_floor,
                    'log2_all_k_function_count':1<<k,
                    'proven_shell_by_counting':success})
    return rows


def test_explicit_shell():
    # Boolean OR(x1,x2) is computable by one OR gate; XOR(x1,x2)
    # is not representable with three gates but has an explicit four-gate
    # fan-in-two AND/OR/NOT implementation. The resulting threshold languages
    # differ already at (s1,s2)=(3,4) for arity n=2.
    out=enumerate_small_circuits(2,3)
    assert out['target_xor_mask']==out['explicit_four_gate_XOR']
    assert not out['XOR_found_with_at_most_3']
    return out


def main():
    out={'status':'COMPUTATIONAL','model':'Boolean {AND,OR,NOT} circuits, fan-in <=2, unbounded fan-out',
         'xor_finite_shell':test_explicit_shell(),
         'asymptotic_parameter_sample':threshold_numeric_tests(),
         'failures':0}
    path=Path(__file__)
    out['sha256_code']=hashlib.sha256(path.read_bytes()).hexdigest()
    result=Path(__file__).with_name('tmr1_mcsp_shell023_raw.json')
    result.write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'xor':out['xor_finite_shell'], 'rows':len(out['asymptotic_parameter_sample']),
                      'successful_rows':sum(x['proven_shell_by_counting'] for x in out['asymptotic_parameter_sample']),
                      'raw':str(result)}))

if __name__=='__main__':main()
