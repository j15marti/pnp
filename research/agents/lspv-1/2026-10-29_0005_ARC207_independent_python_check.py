#!/usr/bin/env python3
"""Independent standard-library enumeration for ARC207: no input files or randomness."""
import json
rows = []
for t in range(1, 5):
    total = 1 << (4*t)
    satisfying = minimal_false = 0
    for bits in range(total):
        A = [bool(bits >> (2*i) & 1) or bool(bits >> (2*i+1) & 1) for i in range(t)]
        B = [bool(bits >> (2*t+2*j) & 1) or bool(bits >> (2*t+2*j+1) & 1) for j in range(t)]
        direct = any(all(bool(z) or a for a in A) and
                     all(not bool(z) or b for b in B) for z in (0,1))
        resolved = all(a or b for a in A for b in B)
        dag = all(A) or all(B)
        assert direct == resolved == dag, (t, bits)
        satisfying += direct
        if not direct:
            zeros = [p for p in range(4*t) if not (bits >> p & 1)]
            if len(zeros) == 4 and zeros[0]//2 == zeros[1]//2 and (
                    zeros[2]-2*t)//2 == (zeros[3]-2*t)//2:
                minimal_false += 1
    assert satisfying == 2*(3**t)*(4**t) - 3**(2*t)
    assert minimal_false == t*t
    rows.append({"t":t,"assignments":total,"satisfying":satisfying,
                 "min_false":minimal_false,"parent_clauses":2*t,
                 "aux_free_projection_clauses":t*t,"dag_gates":4*t-1})
assert sum(r["assignments"] for r in rows) == 69904
print(json.dumps({"total_assignments":69904,"rows":rows},indent=2))
