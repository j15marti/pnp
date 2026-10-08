#!/usr/bin/env python3
"""Find small SAT/UNSAT 3-CNFs with no nonidentity signed syntactic symmetry.
Every candidate map is exhaustively checked on four variables (384 maps).
This is a scope control, not a SAT hardness or complexity lower bound.
"""
from __future__ import annotations
from collections import Counter
import hashlib,itertools,json,random,time
from pathlib import Path
import orbit_first_wrapper as o

def main():
    rng=random.Random(2026100805)
    clauses=[tuple(v*s for v,s in zip(vs,sgn)) for vs in itertools.combinations(range(1,5),3)
             for sgn in itertools.product((-1,1),repeat=3)]
    wanted={True:None,False:None}; checked=0; found=[]
    for attempt in range(100):
        o.guard()
        f=o.canon(rng.sample(clauses,18))
        expected=o.brute(f)
        if wanted[expected] is not None or o.simplify(f,Counter())!=f:
            continue
        autos=[]; witness=[]
        for perm in itertools.permutations(range(1,5)):
            for signs in itertools.product((-1,1),repeat=4):
                p={v:perm[v-1]*signs[v-1] for v in range(1,5)}
                mapped=o.mapped(f,p); checked+=1
                if mapped==f:
                    autos.append(p)
                else:
                    witness.append(next(c for c in mapped if c not in f))
        if len(autos)==1:
            m=Counter(); reduced=o.stream_fix(f,m)
            assert reduced==f and m['stream_fix_steps']==0
            assert autos==[{i:i for i in range(1,5)}]
            wanted[expected]=f
            found.append({'attempt':attempt,'SAT':expected,'formula':f,
                          'signed_permutations_checked':384,'automorphisms':1,
                          'rejected_map_witness_sha256':hashlib.sha256(repr(witness).encode()).hexdigest(),
                          'stream_metrics':dict(m),'identity_only':True})
        if all(v is not None for v in wanted.values()):break
    assert all(v is not None for v in wanted.values())
    out={'run_id':'ARC-0005-ORBIT','seed':2026100805,'status':'PASS',
         'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
         'total_map_checks':checked,'cases':found,'elapsed_seconds':time.monotonic()-o.START,
         'scope':'Four-variable proper 3-CNF examples only. Failure of symmetry fixing does not defeat other WRAPPER branches.'}
    path=Path(__file__).resolve().parents[2]/'results/raw/proof_spines/orbit_rigid_controls.json'
    path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2))
if __name__=='__main__': main()
