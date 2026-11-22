"""Projected optimum relation obstruction and same-length residual-service audit."""
from hashlib import sha256
from itertools import product
import json
import dynamic_construction_dihedral_choice_20261121 as construction

def closure_witness(missing):
    models = [x for x in range(8) if x != missing]
    for x,y in product(models, repeat=2):
        if (x & y) == missing or (x | y) == missing:
            return {"missing":missing, "x":x, "y":y, "meet":x&y, "join":x|y}
    raise AssertionError("closure obstruction missing")

def implication_basis(models):
    lower = 7
    upper = 0
    for x in models:
        lower &= x
        upper |= x
    edges=[]
    for i in range(3):
        if upper >> i & 1:
            meet=7
            for x in models:
                if x >> i & 1:
                    meet &= x
            edges.extend((i,j) for j in range(3) if meet >> j & 1)
    return [x for x in range(8) if x&lower==lower and x|upper==upper and
            all(not (x>>i&1) or (x>>j&1) for i,j in edges)]

def main():
    closed=[]
    for mask in range(1,256):
        models=[x for x in range(8) if mask>>x&1]
        if all((x&y) in models and (x|y) in models for x,y in product(models,repeat=2)):
            assert implication_basis(models)==models
            closed.append(mask)
    mod=construction.codec.load_generator()
    clauses=[tuple(-i if a>>(i-1)&1 else i for i in (1,2,3)) for a in range(8)]
    records=[]
    for q in (1,2):
        families=[(f"missing-{a}",[clause]*(8*q)) for a,clause in enumerate(clauses)]
        families.append(("unsat",clauses*q))
        lengths=set()
        for name,rows in families:
            bits,program,r=construction.build(mod,rows)
            n,target,*_=construction.codec.parse(bits)
            truth=[]
            for x in range(8):
                sat=all(any(bool(x>>(abs(l)-1)&1)==(l>0) for l in row) for row in rows)
                vertex=0
                for instruction in program:
                    vertex=construction.step(instruction,(x>>(abs(instruction[0])-1))&1,vertex,r)
                assert sat==(vertex==0)
                truth.append(int(sat))
            expected = name!="unsat"
            assert bool(sum(truth))==expected
            if expected:
                assert sum(truth)==7
            lengths.add(len(bits))
            records.append(dict(q=q,name=name,N=len(bits),n=n,m=len(target),truth=truth,
                                input_sha256=sha256(bits.encode()).hexdigest()))
        assert len(lengths)==1
    return dict(closure_witnesses=[closure_witness(a) for a in range(8)],
                closed_nonempty_relations=len(closed),closed_masks=closed,
                records=records,conditional_entropy_bits=1.5,
                status="COMPUTATIONAL finite validation; no TM timing or unrestricted lower bound")

if __name__=="__main__":
    print(json.dumps(main(),indent=2))
