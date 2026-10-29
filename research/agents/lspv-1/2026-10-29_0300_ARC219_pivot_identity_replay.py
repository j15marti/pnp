#!/usr/bin/env python3
"""Independent exhaustive check of one-pivot existential resolution, t=1..4.
Counts assignments only to 4t non-pivot variables; z is existentially removed.
"""
import itertools, json
from pathlib import Path
out={}
for t in range(1,5):
    checked=0
    for bits in itertools.product((0,1),repeat=4*t):
        A=[bool(bits[2*i] or bits[2*i+1]) for i in range(t)]
        B=[bool(bits[2*t+2*j] or bits[2*t+2*j+1]) for j in range(t)]
        def f(z):
            return all(z or a for a in A) and all((not z) or b for b in B)
        existential=f(False) or f(True)
        expanded=all(a or b for a in A for b in B)
        compact=all(A) or all(B)
        assert existential==expanded==compact,(t,bits)
        checked+=1
    out[str(t)]=checked
out['total']=sum(out[str(t)] for t in range(1,5))
assert out['total']==69904
Path(__file__).with_name('ARC219_pivot_identity_raw.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
