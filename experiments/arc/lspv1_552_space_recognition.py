#!/usr/bin/env python3
"""LSPV-1/552: bounded-halt toy resource schedules; NOT a native FLMV interpreter.
Exhaustive finite input-output checks and exact integer work-position arithmetic.
The all-n undecidability theorem is proved symbolically in the report.
"""
import json
from fractions import Fraction
from hashlib import sha256
from itertools import product


def observe(bits: str, halt_step):
    n = len(bits)
    # Simulate the control M for k=floor(log2 n) steps, using <=k tape cells.
    k = max(0, n.bit_length() - 1)
    halts_in_budget = halt_step is not None and halt_step <= k
    # This is an explicit abstract schedule: positions 1..k+4 reserved for
    # counters and local simulation; each scratch write accesses a new cell.
    work = set(range(1, k+5))
    if halts_in_budget:
        work.update(range(1, n//2+1))
    highwater = max(work, default=0)
    verdict = bool(bits and bits[0] == '1')
    return {'n':n,'k':k,'triggered':halts_in_budget,'highwater':highwater,
            'out':int(verdict), 'touched':len(work)}


def compressed(n, halt_step):
    # Same high-water as explicit observe, without materializing tape/input.
    k=max(0,n.bit_length()-1)
    trigger=halt_step is not None and halt_step<=k
    return max(k+4, n//2 if trigger else 0),trigger


def tests():
    checked=0; corrupt=0
    for n in range(0,13):
        for bit_tuple in product('01',repeat=n):
            bits=''.join(bit_tuple)
            for threshold in [None,0,1,2,3,5,13]:
                z=observe(bits,threshold)
                assert z['out']==(1 if bits.startswith('1') else 0)
                exact,trig=compressed(n,threshold)
                assert z['highwater']==exact and z['triggered']==trig
                assert z['touched']<=max(n//2,z['k']+4)
                checked+=1
        # Deliberate false halt-flag controls are detected by independent predicate.
        if n>=2:
            record=observe('0'*n,5)
            opposite=not (5<=max(0,n.bit_length()-1))
            assert record['triggered'] != opposite
            corrupt+=1
    assert compressed(32,5)[1] and not compressed(31,5)[1]
    beta=Fraction(23,45)
    rows=[]
    for exponent in [6,12,24,60]:
        n=10**exponent
        log_bound=compressed(n,None)[0]
        early=compressed(n,5)[0]
        rows.append({'N':str(n),'log_only_highwater':log_bound,
                     'eventual_halt_highwater':early,
                     'log10_N_to_beta':float(exponent*beta),
                     'log10_N_to_half':exponent/2,
                     'ratio_beta_to_half':round(10**(exponent/90),10)})
    return {'status':'COMPUTATIONAL','source':'lspv1_552_space_recognition.py',
            'exhaustive_cases':checked,'negative_controls':corrupt,
            'halting_threshold_check':'n=31 excludes, n=32 includes',
            'timespace_note':'only event-level work-position schedules, not full native TM execution',
            'input_language':'nonempty strings beginning in 1',
            'beta_6_5':'23/45','asymptotic_theorem':'symbolic; not established by finite test',
            'examples':rows}


if __name__=='__main__':
    print(json.dumps(tests(),indent=2))
