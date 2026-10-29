#!/usr/bin/env python3
"""ARC217: independently reproducible guarded mixed-CSP projection controls.

Status: mathematical construction is proved separately; these are finite checks.
No dependencies other than Python standard library. Python 3.10+.
"""
import itertools
import json
import hashlib
import random
from pathlib import Path

SEED = 20261029
OUT = Path(__file__).with_name('ARC217_guarded_projection_raw.json')


def val(lit, x):
    value = x[abs(lit)-1]
    return value if lit > 0 else 1-value


def clause_eval(clause, x):
    return any(val(l, x) for l in clause)


def cnf_eval(clauses, x):
    return all(clause_eval(c, x) for c in clauses)


def gadget_exists(lit_values, g):
    for a, b, c, t in itertools.product((0, 1), repeat=4):
        if all(lit_values[i] or ((a,b,c)[i]) for i in range(3)) and (a ^ b ^ t) == 0 and (t ^ c ^ g) == 0:
            return True
    return False


def encode(clauses, n):
    # The control bit g appears only in affine rows, never in 2CNF.
    g = n+1
    new_id = g+1
    binary = []
    parity = []
    for clause in clauses:
        assert len(clause) == 3
        ys = list(range(new_id, new_id+3))
        t = new_id+3
        new_id += 4
        binary.extend((lit, y) for lit,y in zip(clause,ys))
        parity.append(((ys[0],ys[1],t),0))
        parity.append(((t,ys[2],g),0))
    return {"num_variables": new_id-1, "g":g, "binary":binary, "xor3":parity}


def source_projection(clauses, n):
    return any(cnf_eval(clauses, x) for x in itertools.product((0,1), repeat=n))


def full_compatible(enc, x, g):
    # Each clause has disjoint fresh auxiliaries. The gadget local quantifiers commute.
    return all(gadget_exists(tuple(val(l,x) for l in clause),g) for clause in enc["source"])


def verify_one(clauses, n):
    enc = encode(clauses,n)
    enc["source"] = clauses
    expected = source_projection(clauses,n)
    for g in (0,1):
        present = any(full_compatible(enc,x,g) for x in itertools.product((0,1),repeat=n))
        assert present == (bool(g) or expected)
    return expected


def run():
    counts={"local_truth_rows":0,"all_subsets":0,"global_source_assignments":0,"global_guard_rows":0,
            "random_instances":0,"random_sat":0,"random_unsat":0,"random_guard_rows":0,
            "onebit_projection_differences":0,"separately_satisfiable_hostile":0,
            "controlled_witness_cases":0}
    # Exhaust every local literal pattern and every auxiliary assignment.
    for v in itertools.product((0,1),repeat=3):
        for g in (0,1):
            assert gadget_exists(v,g) == (bool(g) or any(v))
            counts["local_truth_rows"] += 1
    # All 2^8 subsets of all eight proper signed triples on three variables.
    all8=[tuple((i+1) if ((mask>>i)&1) else -(i+1) for i in range(3)) for mask in range(8)]
    for subsetmask in range(256):
        clauses=[all8[i] for i in range(8) if (subsetmask>>i)&1]
        enc=encode(clauses,3)
        assert len(enc["binary"]) == 3*len(clauses)
        assert len(enc["xor3"]) == 2*len(clauses)
        srcsat=source_projection(clauses,3)
        assert srcsat == (subsetmask != 255)
        counts["all_subsets"]+=1
        for x in itertools.product((0,1),repeat=3):
            counts["global_source_assignments"]+=1
            for g in (0,1):
                present=all(gadget_exists(tuple(val(l,x) for l in c),g) for c in clauses)
                assert present == (bool(g) or cnf_eval(clauses,x))
                counts["global_guard_rows"] += 1
        if not srcsat:
            counts["onebit_projection_differences"]+=1
    # Generate a mixture of random satisfiable and unsatisfiable controls on n=4,5.
    rng=random.Random(SEED)
    for trial in range(240):
        n=4+(trial%2)
        m=8+(trial%19)
        clauses=[]
        for _ in range(m):
            ids=rng.sample(range(1,n+1),3)
            clauses.append(tuple(v if rng.randrange(2) else -v for v in ids))
        sat=verify_one(clauses,n)
        counts["random_instances"]+=1
        counts["random_sat" if sat else "random_unsat"]+=1
        counts["random_guard_rows"]+=2
    # For UNSAT 8-clause case, each pure language is satisfiable at g=0,
    # but their conjunction is not. Binary: y=1; XOR: y=t=0, g=0.
    enc=encode(all8,3)
    assert not source_projection(all8,3)
    binary_witness={i:0 for i in range(1,enc["num_variables"]+1)}
    for _,y in enc["binary"]: binary_witness[y]=1
    assert all((val(l,[binary_witness[i] for i in range(1,enc["num_variables"]+1)]) or binary_witness[y])
               for l,y in enc["binary"])
    affine_witness={i:0 for i in range(1,enc["num_variables"]+1)}
    assert all((affine_witness[a]^affine_witness[b]^affine_witness[c])==rhs
               for (a,b,c),rhs in enc["xor3"])
    assert not any(all(gadget_exists(tuple(val(l,x) for l in c),0) for c in all8)
                   for x in itertools.product((0,1),repeat=3))
    counts["separately_satisfiable_hostile"]+=1
    # Witness for g=1: every y=1 and t=0 (for any source assignment).
    # Witness for g=0: choose one true literal of every clause, set its y=0,
    # all other y=1, then t=y1^y2. Check each row.
    for v in itertools.product((0,1),repeat=3):
        g=1
        y=[1,1,1];t=0
        assert all(v[i] or y[i] for i in range(3)) and (y[0]^y[1]^t)==0 and (t^y[2]^g)==0
        counts["controlled_witness_cases"]+=1
        if any(v):
            y=[1,1,1]; y[v.index(1)]=0; g=0; t=y[0]^y[1]
            assert all(v[i] or y[i] for i in range(3)) and (y[0]^y[1]^t)==0 and (t^y[2]^g)==0
            counts["controlled_witness_cases"]+=1
    assert counts["random_sat"]>0 and counts["random_unsat"]>0
    examples=[]
    for m in (1,2,4,8,16,32,64):
        template=[all8[i%8] for i in range(m)]
        enc=encode(template,3)
        physical=len(json.dumps(enc,sort_keys=True,separators=(',',':')).encode('utf8'))
        examples.append({"clauses":m,"auxiliaries":4*m,"binary":3*m,"xor3":2*m,"mixed_encoding_bytes":physical})
    data={"status":"PASS","label":"COMPUTATIONAL","seed":SEED,"counts":counts,
          "encoding_growth":examples,"hardness_statement":"theorem proved symbolically in accompanying LaTeX",
          "caveat":"finite tests are not a universal algorithm or native TM timing experiment"}
    OUT.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n',encoding='utf8')
    print(json.dumps(data,indent=2,sort_keys=True))

if __name__=='__main__':
    run()
