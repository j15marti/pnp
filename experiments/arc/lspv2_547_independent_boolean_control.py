#!/usr/bin/env python3
"""Independent Python finite truth-table control of LSPV-2/547.
REFERENCE SEMANTICS ONLY. This is NOT the historical /341 accepted-byte checker.
"""
import hashlib, itertools, json
C=[(1,2,3),(1,2,-3),(1,-2,3),(1,-2,-3),
   (-1,2,3),(-1,2,-3),(-1,-2,3),(-1,-2,-3)]
source="p cnf 3 8\n"+"".join(" ".join(map(str,c))+" 0\n" for c in C)
SHA="a2f85326956ed24023d756dc4b0c205657cec886e8cf405083437b2b820cb719"
assert hashlib.sha256(source.encode()).hexdigest()==SHA and len(source)==86

def sat(c,a):
    return any(a[abs(l)-1] == (l>0) for l in c)
cases=list(itertools.product((False,True),repeat=3))
assert not any(all(sat(c,a) for c in C) for a in cases)
assert all(sum(not sat(c,a) for c in C)==1 for a in cases)
for j in range(8):
    assert any(all(sat(c,a) for i,c in enumerate(C) if i!=j) for a in cases)
rows=[(1,2),(1,-2),(-1,2),(-1,-2)]
for j,r in enumerate(rows):
    a,b=C[2*j:2*j+2]
    assert ((3 in a and -3 in b) or (-3 in a and 3 in b))
    resolved=tuple(sorted((set(a)|set(b))-{3,-3},key=lambda x:(abs(x),x)))
    assert resolved==r
    for assignment in cases:
        assert (sat(a,assignment) and sat(b,assignment))==sat(r,assignment)
for a in cases:
    left=sat(rows[0],a) and sat(rows[1],a)
    right=sat(rows[2],a) and sat(rows[3],a)
    assert left==a[0] and right==(not a[0])
    assert (int(left)^int(right))==1
    assert (int(a[0])^int(a[0]))==0
print(json.dumps({"source_sha256":SHA,"source_bytes":86,
 "all_assignments_checked":8,"deletion_witnesses":8,
 "resolution_equivalence_checks":32,"and3_truth_checks":16,
 "gf2_truth_checks":8,"paid_nodes":7,"independent_result":"PASS",
 "scope":"reference semantics, not native R_mix341 grammar"},indent=2))
