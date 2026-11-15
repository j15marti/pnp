#!/usr/bin/env python3
"""TMR-3/053: exhaustive checkpoint-work selector service and sketch/probe tradeoff.

Strictly scoped: a fixed locally moving two-work-tape service suffix begins
from a CHECKPOINT, not from an ordinary blank-work-tape initial configuration.
The data tape contains z[0]..z[k-1], followed by an endmarker, and the
motion tape is blank. One paid transition consumes each data symbol; the
motion head moves right iff the bit is 1. The endmarker halts the suffix.

For s in [0,k], the exact interface sketch is z[:s] and the probe transcript
is z[s:], totaling k bits. This verifies a sharp upper witness to s+q>=k;
the universal lower bound is proved by a transcript-counting argument in the
report, not by finite enumeration of all algorithms.
"""
from __future__ import annotations
from collections import defaultdict
from hashlib import sha256
import json, sys
from pathlib import Path

VERSION = 'tmr3-work-checkpoint053.v1'

def service(z: tuple[int,...]):
    # Encoded tape A is z followed by #. Tape B is all blank.
    # Initial control is READ; state after k transitions is HALT pending #.
    data_head = 0
    movement_head = 0
    steps = 0
    motion = []
    trace = []
    for bit in z:
        assert bit in (0,1)
        # A genuine TM transition: A advances one, B right or stays.
        old_A, old_B = data_head, movement_head
        data_head += 1
        movement_head += bit
        steps += 1
        motion.append(bit)
        trace.append((old_A,old_B,bit,data_head,movement_head))
    steps += 1 # paid endmarker HALT
    return {'motion': tuple(motion), 'B_final': movement_head,
            'A_final':data_head,'paid_steps':steps,'trace':tuple(trace),
            'visited_A':len(z)+1,'visited_B':movement_head+1}

def reproduce(z: tuple[int,...], s: int):
    # Information retained in s-bit sketch is NOT free to create.
    sketch = z[:s]
    queries = tuple(range(s, len(z)))
    replies = tuple(z[j] for j in queries)
    return sketch + replies, len(queries), len(sketch)

def main():
    assertions=0
    service_cases=0
    sketch_cases=0
    examples=[]
    for k in range(1,13):
        graphs=set()
        # No arbitrary "semantic graph" count: every signature is executed.
        for a in range(1<<k):
            z=tuple((a>>(k-1-j))&1 for j in range(k))
            p=service(z)
            assert p['motion']==z; assertions+=1
            assert p['B_final']==sum(z); assertions+=1
            assert p['A_final']==k; assertions+=1
            assert p['paid_steps']==k+1; assertions+=1
            assert p['visited_A']==k+1; assertions+=1
            assert p['visited_B']==sum(z)+1; assertions+=1
            for i,t in enumerate(p['trace']):
                assert (t[3]-t[0],t[4]-t[1])==(1,z[i]); assertions+=1
            graphs.add(p['motion'])
            service_cases+=1
            for s in range(k+1):
                recovered,q,storage=reproduce(z,s)
                assert recovered==p['motion']; assertions+=1
                assert storage+q==k; assertions+=1
                sketch_cases+=1
        assert len(graphs)==(1<<k);assertions+=1
        # A preprocessor retaining only s prefix bits and with q=0 has
        # collisions if s<k. This is one particular failing scheme.
        for s in range(k):
            seen=defaultdict(set)
            for z in graphs:
                seen[z[:s]].add(z)
            assert len(seen)==1<<s; assertions+=1
            assert all(len(v)==1<<(k-s) for v in seen.values());assertions+=1
        if k in (1,2,4,8,12):
            examples.append({'k':k,'genuine_graphs':len(graphs),
                             'no_probe_min_information_bits':k,
                             'sharp_one_pass_probes':k,
                             'charged_suffix_paid_steps':k+1,
                             'illustrative_s':k//2,'illustrative_q':k-k//2})
    src=Path(__file__).read_bytes()
    raw={'version':VERSION,'status':'COMPUTATIONAL','assertions':assertions,
         'failures':0,'service_cases':service_cases,
         'sharp_sketch_probe_pairs':sketch_cases,
         'k_range':[1,12], 'random_seed':None,'examples':examples,
         'source_sha256':sha256(src).hexdigest(),
         'python':sys.version.split()[0],
         'limitations':['Finite testing is not a proof of the lower bound for all selectors.',
           'States are preloaded CHECKPOINT states and do not arise from one fixed blank tape input x.',
           'Advice construction, probes, storage, movement and output all require actual physical work.',
           'Graph is reconstructible with k authenticated work-cell probes; no unconditional cube-root-space obstruction.',
           'No SAT-machine, FLMV, or P-versus-NP claim.']}
    dest=Path(sys.argv[1]) if len(sys.argv)>1 else Path('results.json')
    dest.write_text(json.dumps(raw,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:raw[k] for k in ('version','assertions','failures','service_cases','sharp_sketch_probe_pairs')},sort_keys=True))

if __name__=='__main__':main()
