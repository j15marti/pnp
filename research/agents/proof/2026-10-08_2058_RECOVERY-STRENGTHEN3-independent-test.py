"""Independent affine-composition model checks; not a SAT solver or coverage test."""
import json
import random
import signal
import time
from pathlib import Path

signal.alarm(25)
started = time.monotonic()
rng = random.Random(3058)

def mv(a, x, p):
    return [sum(v*w for v, w in zip(row, x)) % p for row in a]

def add(x, y, p):
    return [(a+b) % p for a,b in zip(x,y)]

def mm(a, b, p):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b))) % p
             for j in range(len(b[0]))] for i in range(len(a))]

cases = 0
root_calls = 0
for p in (2,3,5,7):
    for dims in ((8,4,2,1), (8,8,4,4,2,1)):
        for _ in range(20):
            edges = [([[rng.randrange(p) for _ in range(d1)] for _ in range(d0)],
                      [rng.randrange(p) for _ in range(d0)])
                     for d0,d1 in zip(dims,dims[1:])]
            mat = [[int(i==j) for j in range(dims[0])] for i in range(dims[0])]
            shift = [0]*dims[0]
            for b,c in edges:
                shift = add(mv(mat,c,p),shift,p)  # MUST use pre-update mat.
                mat = mm(mat,b,p)
            for z0 in range(p):
                z = [z0]
                for b,c in reversed(edges):
                    z = add(mv(b,z,p),c,p)
                composed = add(mv(mat,[z0],p),shift,p)
                assert z == composed
                # A supplied field evaluator; acquisition is not modeled.
                root_value = sum((i+1)*x*x for i,x in enumerate(composed)) % p
                root_calls += 1
                for mask in range(1 << (p-1).bit_length()):
                    bit = (root_value & mask).bit_count() % 2
                    ref = (sum((i+1)*x*x for i,x in enumerate(z)) % p & mask).bit_count() % 2
                    assert bit == ref
                cases += 1

probe_cases = 0
for k in range(1,12):
    for _ in range(50):
        a = [rng.randrange(1,5) for _ in range(k)]
        w = [rng.randrange(9) for _ in range(k)]
        q0 = rng.randrange(10)
        q = q0
        for ai,wi in zip(a,w):
            q = wi+ai*q
        prod=1
        unrolled=0
        for ai,wi in zip(reversed(a),reversed(w)):
            unrolled += wi*prod
            prod *= ai
        unrolled += q0*prod
        assert q==unrolled
        probe_cases += 1

result = {"status":"COMPUTATIONAL", "scope":"Supplied affine descriptors and evaluator only; no SAT acquisition/return claim",
          "seed":3058,"affine_cases":cases,"root_calls":root_calls,
          "probe_recurrence_cases":probe_cases,"all_passed":True,
          "elapsed_seconds":round(time.monotonic()-started,6),"python_budget_seconds":25}
out = Path(__file__).with_suffix('.json')
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
