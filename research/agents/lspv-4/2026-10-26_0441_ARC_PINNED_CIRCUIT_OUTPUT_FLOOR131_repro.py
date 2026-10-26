#!/usr/bin/env python3
"""Independent exact arithmetic audit of Role-2 SORT166 fixed-record pinned SAT reduction.

This code does not claim to construct/solve the enormous CNFs or measure an FLMV
machine. It verifies symbolic clause/variable propagation, canonical bit floors,
and a scan-before-solve countermodel in a declared virtual-input simulation.
No randomness or external packages. Python 3.11+.
"""
from __future__ import annotations
import json
from fractions import Fraction
from math import ceil, log2
from pathlib import Path

CHECKS = 0

def check(predicate, message):
    global CHECKS
    CHECKS += 1
    if not predicate:
        raise AssertionError(message)

def ceil_log2(n):
    check(n > 0, 'log input')
    return (n - 1).bit_length()

def digits10_sum(z):
    """Number of decimal digit characters when printing IDs 1..z once each."""
    if z <= 0:
        return 0
    total = 0
    lo = 1
    width = 1
    while lo <= z:
        upper = min(z, lo * 10 - 1)
        total += (upper - lo + 1) * width
        lo *= 10
        width += 1
    return total

def model(q,m):
    check(q >= 3 and m >= 1, 'declared q,m')
    w = ceil_log2(q + 1)
    N = m * (1 + 3 * (w + 1))
    K = 1 << ceil_log2(q + 3*m)
    h = ceil_log2(K)
    C_times_four = K*h*(h+1)
    check(C_times_four % 4 == 0, 'integer Batcher comparator count')
    C = C_times_four // 4
    G = C*(13*w+38) + 19*K + (K-1)*(4*w-1) + m*(36*w+16)-1
    n0, m0 = 9*G+3*N+q+8, 13*G+4*N+12
    n1, m1 = 33*m0+48*n0,44*m0+64*n0
    n2, m2 = 3036*m0+4416*n0,4048*m0+5888*n0
    check(m2*3 == n2*4, 'signed (2,2) incidence identity')
    check(m2 == 105616*G + 33856*N + 5888*q + 95680, 'expanded m2 identity')
    check(n2 == 79212*G + 25392*N + 4416*q + 71760, 'expanded n2 identity')
    check(m2 >= 33856*N and n2 >= 25392*N, 'source-bit pin floor')
    check(m0 >= 4*N and n0 >= 3*N, 'source pin count')
    check(n2 > N and m2 > N, 'no strict child shrink in count')
    check(m1*3 == n1*4, 'level-one signed (2,2) incidence')
    ascii_id_bits = 32*digits10_sum(n2)
    ascii_floor_from_pins = 32*digits10_sum(25392*N)
    check(ascii_id_bits >= ascii_floor_from_pins,'decimal ID printed bit floor')
    binary_min = 3*m2*(1+ceil_log2(n2+1))
    check(binary_min >= 3*m2, 'binary ID/sign field floor')
    # Exact source-bit polarity influences are 4, 8, 16 in the three levels.
    check(16*N <= 3*m2, '16 disjoint sign positions fit physical ternary fields')
    return {'q':q,'m':m,'source_N_bits':N,'w':w,'K':K,'comparators':C,
        'gate_count_G':G,'base_variables_n0':n0,'base_clauses_m0':m0,
        'level1_variables_n1':n1,'level1_clauses_m1':m1,
        'level2_variables_n2':n2,'level2_clauses_m2':m2,
        'source_dependent_level2_sign_positions':16*N,
        'decimal_id_floor_bits':ascii_id_bits,
        'pin_only_decimal_floor_bits':ascii_floor_from_pins,
        'fixed_width_binary_fields_floor_bits':binary_min,
        'second_level_clauses_per_input_bit_lower_bound':33856,
        'second_level_variables_per_input_bit_lower_bound':25392,
        'binary_floor_to_source_ratio':round(binary_min/N,6),
        'decimal_floor_to_source_ratio':round(ascii_id_bits/N,6)}

def beta(c):
    return ((c+2)/c**2 - c)/2

def exhaustive_small_id_checks():
    # Independent digit-sum implementation by direct enumeration, small sizes.
    for z in range(1,300):
        check(digits10_sum(z) == sum(len(str(i)) for i in range(1,z+1)),f'digit sum z={z}')

def scan_countermodel(length,answer):
    """Toy complete fixed-language decider: deliberately reads EVERY virtual bit,
    then invokes a separate known-exact decision routine (answer supplied here).
    This only simulates the scan prefix; it is not a full universal SAT decider.
    """
    queries = 0
    parity = 0
    for i in range(length):
        parity ^= ((i*5 + 1)%2)
        queries += 1
    return {'virtual_length':length,'input_read_calls':queries,
            'toy_exact_label_after_scan':int(bool(answer)),'scan_parity':parity}

def main():
    exhaustive_small_id_checks()
    models=[]
    for q,m in [(3,1),(3,8),(4,8),(7,8),(16,64),(64,256),(256,1024),(1024,1024)]:
        models.append(model(q,m))
    check(models[0]['gate_count_G']==1824, 'peer q3m1 gate count')
    check(models[0]['level2_clauses_m2']==193095488, 'peer q3m1 clause count')
    check(models[1]['gate_count_G']==16888, 'peer q3m8 gate count')
    check(models[1]['level2_clauses_m2']==1786464832,'peer q3m8 clause count')
    # Asymptotic attack: for all m>=1, q=3 implies N=10m, m2>=33856N,
    # n2>=25392N, so canonical proper exact-(2,2) serialization is
    # Omega(N log N); both bits and input-read demands cannot be compressed
    # into N^lambda with lambda<1 in this fixed architecture.
    for m in range(1,35):
        t=model(3,m)
        check(t['pin_only_decimal_floor_bits'] > t['source_N_bits'],'pin length check')
        check(t['source_dependent_level2_sign_positions'] < t['level2_clauses_m2']*3,
              'source influence not full output')
    c=Fraction(241,200)
    target_s=Fraction(11642479,23232400)
    check(beta(c)==target_s,'exact FLMV beta')
    test_t,test_s=Fraction(11,10),Fraction(1,2)
    margins={'time':str(c-test_t),'space':str(target_s-test_s)}
    check(c-test_t==Fraction(21,200),'time margin')
    check(target_s-test_s==Fraction(26279,23232400),'space margin')
    d=Fraction(901,500)
    co_threshold=Fraction(2*d-1,d*(d-1))
    # Master Theorem 1.3 second condition cd(d-1)-2d+1 < 0.
    check(co_threshold==Fraction(651000,361301),'van Melkebeek time formula')
    circuit_q=(d*d)/(d*d-1)
    check(circuit_q==Fraction(811801,561801),'conditional circuit q formula')
    # Numeric only: composition hypotheses for c and q remain open.
    scans=[]
    for bit_length in [1,2,3,16,257,1024]:
        for truth in (False,True):
            rec=scan_countermodel(bit_length,truth)
            check(rec['input_read_calls']==bit_length,'scanning every virtual bit')
            check(rec['toy_exact_label_after_scan']==int(truth),'scan preserves downstream label')
            scans.append(rec)
    output={'audit_id':'ARC-PINNED-CIRCUIT-OUTPUT-FLOOR131','status':
            'PROVED/EXACT restricted symbolic bound; COMPUTATIONAL arithmetic tests; OPEN unrestricted SAT',
        'dependency':'LSPV-2 CIRCUIT-OBLIVIOUS-INVERSE-SORT166 exact gate and Q15/J counts; finite machine counts not established',
        'reference': 'research/agents/lspv-2/2026-10-26_1035_LSPV-2_CIRCUIT_OBLIVIOUS_INVERSE_SORT166.tex',
        'input_measure':'N=m[1+3(ceil(log2(q+1))+1)] bits, q>=3, m>=1',
        'identities':{'m2':'105616 G + 33856 N + 5888 q + 95680',
                      'n2':'79212 G + 25392 N + 4416 q + 71760',
                      'incidence':'3 m2 = 4 n2',
                      'virtual_changed_signs':'16 N',
                      'physical_id_bit_floor':'32 sum_{i=1}^{n2} digits10(i)'},
        'flmv':{'time_boundary':str(c),'space_boundary':str(target_s),
                'pair_under_test':[str(test_t),str(test_s)],'strict_margins':margins,
                'conditional_d':str(d),'conditional_coNTIME_c':str(co_threshold),
                'conditional_circuit_q':str(circuit_q),
                'note':'extra d is not implied by P=NP; circuit q needs full decision circuits and Sigma2SAT small-space'},
        'models':models,'toy_adversarial_scan_prefix':scans,
        'assertions':CHECKS,'failures':0,'seed':'none, exact deterministic',
        'limitation':'does not instantiate all-input solver A; no guest FLMV bit-time; does not serialize huge child CNFs'}
    dst=Path(__file__).with_name(Path(__file__).name.replace('_repro.py','_raw.json'))
    dst.write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'assertions':CHECKS,'failures':0,
                      'test_models':len(models),'q3m1_m2':models[0]['level2_clauses_m2'],
                      'q3m8_m2':models[1]['level2_clauses_m2'],
                      'raw_json':str(dst)},indent=2))

if __name__=='__main__':main()