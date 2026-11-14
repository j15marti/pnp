#!/usr/bin/env python3
"""Finite hostile controls for exact MCSP circuit-size threshold mismatch.
AND/OR/NOT basis, fan-in at most 2, free constants and input wires,
sharing allowed. Gate count is the only circuit resource charged here.
No general complexity lower bound follows from these finite controls.
"""
import itertools
import json
import hashlib
from collections import Counter


def truth_wires(n):
    count = 1 << n
    whole = (1 << count) - 1
    inputs = [sum(((a >> (n-1-j)) & 1) << a for a in range(count)) for j in range(n)]
    return tuple([0,whole]+inputs), whole


def circuit_minima(n, max_gates):
    initial, mask = truth_wires(n)
    cc = {v:0 for v in initial}
    # Each internal circuit state is an ordered tuple of gate truth tables.
    # Duplicates are harmless and eliminated only when entire state identical.
    active = {()}
    states_by_layer = [len(active)]
    for cost in range(1, max_gates+1):
        new = set()
        for gates in active:
            wires = initial + gates
            length = len(wires)
            for a in range(length):
                z = mask ^ wires[a]
                cc.setdefault(z,cost)
                new.add(gates+(z,))
            for a in range(length):
                for b in range(a,length):
                    x,y = wires[a],wires[b]
                    for z in (x & y, x | y):
                        cc.setdefault(z,cost)
                        new.add(gates+(z,))
        active = new
        states_by_layer.append(len(active))
    return cc,states_by_layer


def pad_bits(mask,n,t):
    repeat=1<<t
    out=0
    for a in range(1<<n):
        if (mask>>a)&1:
            out |= ((1<<repeat)-1)<<(a*repeat)
    return out


def run():
    minima2, state2 = circuit_minima(2,3)
    minima3, state3 = circuit_minima(3,3)
    tests=0
    # Exhaustive full n=2 source truth tables, all matched integer thresholds <=2.
    for x in range(16):
        y=pad_bits(x,2,1)
        for s in range(3):
            assert (minima2.get(x,99)<=s)==(minima3.get(y,99)<=s)
            tests+=1
    # For thresholds in the finite range, find a strict size spectrum witness.
    crossing={}
    for lo in range(3):
        for hi in range(lo+1,4):
            witnesses=[x for x,cc in minima3.items() if lo<cc<=hi]
            if witnesses:
                x=min(witnesses)
                assert minima3[x]>lo and minima3[x]<=hi
                crossing[f'{lo}:{hi}']={'truth_table_hex':hex(x),'minimal_gates':minima3[x]}
                tests+=1
    # Gray-style single-bit path from constant zero to each known level >=1.
    path_checks=[]
    for target in range(1,4):
        hard=next(x for x,c in sorted(minima3.items()) if c>=target)
        prefix=0
        for bit in range(8):
            if (hard>>bit)&1:
                prefix |= 1<<bit
                assert minima3.get(prefix,99) <= (2*3+4)*8
                tests+=1
        path_checks.append({'target_level':target,'endpoint':hex(hard),'endpoint_min_gates':minima3[hard]})
    result={'status':'COMPUTATIONAL','n_source':2,'n_target':3,'circuit_basis':'AND,OR,NOT; free constants; unrestricted fanout','max_gates_enumerated':3,'circuit_state_counts_n2':state2,'circuit_state_counts_n3':state3,'distinct_known_functions_n2':len(minima2),'distinct_known_functions_n3':len(minima3),'same_threshold_padding_checks':48,'crossing_witnesses':crossing,'path_controls':path_checks,'assertions_passed':tests,'assertion_failures':0,'caveat':'unknown minimum above 3 gates remains unclassified; symbolic argument is separate'}
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':
    run()
