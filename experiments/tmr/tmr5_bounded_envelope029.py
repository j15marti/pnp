#!/usr/bin/env python3
"""Independent finite verification of bounded-threshold MCSP envelope inheritance.
Native CPython semantic bitmask model, not an executed finite-alphabet TM.
"""
import itertools
import json
import random

SEED=20261114
rng=random.Random(SEED)

def catalog_min_gate(n, cap):
    """Enumerate AND/OR/NOT straight-line circuit programs with <=cap gates.
    Outputs any existing wire; constants and positive inputs cost 0.
    Return exact smallest gate count of every generated Boolean function.
    """
    length=1<<n
    allbits=(1<<length)-1
    starting=(0, allbits) + tuple(sum(((j>>i)&1)<<j for j in range(length)) for i in range(n))
    best={v:0 for v in starting}
    # Programs are tuples of semantic values on their ordered wires, so
    # distinct syntactic descriptions with same values may coalesce safely.
    programs={starting}
    for step in range(1,cap+1):
        grown=set()
        for p in programs:
            wires=set(p)
            possible={allbits^x for x in wires}
            for x in wires:
                for y in wires:
                    possible.add(x & y)
                    possible.add(x | y)
            for v in possible:
                if v not in best: best[v]=step
                grown.add(p+(v,))
        programs=grown
    return best

def online_min_gate(bits, catalog, cap):
    """Incrementally hold match flags for the *cap-envelope*, not the
    current threshold. Return capped min gate count, or None if absent.
    """
    seen=0
    flags={0:True,1:True}
    for x in bits:
        if seen and seen & (seen-1)==0:
            # At read count 2^k, promote k-input candidates to k+1.
            k=seen.bit_length()-1
            assert k+1<len(catalog)
            old=flags
            halfmask=(1<<seen)-1
            flags={c:old[c & halfmask] for c in catalog[k+1]}
        for c in flags:
            flags[c]=flags[c] and (((c>>seen)&1)==x)
        seen+=1
    if seen<2 or (seen&(seen-1)):
        return None
    arity=seen.bit_length()-1
    return min((catalog[arity][c] for c,good in flags.items() if good),default=None)

def run():
    max_n=4; cap=2
    catalog=[catalog_min_gate(n,cap) for n in range(max_n+1)]
    allmask_lengths=[len(c) for c in catalog]
    cofactor_checks=0
    for n in range(1,max_n+1):
        lowmask=(1<<(1<<(n-1)))-1
        for mask in catalog[n]:
            cofactor_checks+=1
            assert (mask&lowmask) in catalog[n-1]
    exact_cases=0; answer_checks=0; wrong=0
    # All bounded schedules on arities 1,2,3, including 0 -> 1 crossings.
    schedules=list(itertools.product(range(cap+1),repeat=3))
    for sched in schedules:
        for n in range(1,4):
            N=1<<n
            for truth in range(1<<N):
                bits=[(truth>>j)&1 for j in range(N)]
                got=online_min_gate(bits,catalog,cap)
                assert got==catalog[n].get(truth),(sched,n,truth,got)
                expected=(truth in catalog[n] and catalog[n][truth]<=sched[n-1])
                decided=(got is not None and got<=sched[n-1])
                assert decided==expected,(sched,n,truth,got)
                exact_cases+=1;answer_checks+=1
    for _ in range(1024):
        n=4; N=1<<n
        mask=rng.getrandbits(N)
        bits=[(mask>>j)&1 for j in range(N)]
        got=online_min_gate(bits,catalog,cap)
        assert got==catalog[n].get(mask)
        answer_checks+=1
    malformed_checks=0
    for L in range(1,16):
        if L&(L-1) or L==1:
            b=[rng.randrange(2) for _ in range(L)]
            assert online_min_gate(b,catalog,cap) is None
            malformed_checks+=1
    # Critical previously identified naive-pruning failure now correctly handled:
    short=[1,0]
    longer=[1,0,1,0]  # truth table of NOT x_0
    assert online_min_gate(short,catalog,1)==1
    assert online_min_gate(longer,catalog,1)==1
    assert online_min_gate(short,catalog,1)>0    # n=1 threshold 0 rejects
    assert online_min_gate(longer,catalog,1)<=1 # n=2 threshold 1 accepts
    print(json.dumps({"id":"TMR5_ENVELOPE29","status":"PASS", "seed":SEED,
       "model":"semantic masks, offline-exact circuit enumeration; no compiled one-tape TM",
       "cap":cap,"candidate_counts_n0_through_n4":allmask_lengths,
       "cofactor_membership_checks":cofactor_checks,"bounded_schedules":len(schedules),
       "exhaustive_online_minima":exact_cases,"answer_checks":answer_checks,
       "malformed_checks":malformed_checks,
       "dynamic_threshold_repair":{"stage_n1_threshold":0,"stage_n2_threshold":1,"short_10_label":"NO","long_1010_label":"YES"}},indent=2,sort_keys=True))

if __name__=='__main__':run()
