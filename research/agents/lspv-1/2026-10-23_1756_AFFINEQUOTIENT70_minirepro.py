#!/usr/bin/env python3
"""Independent small exhaustive checks for AFFINEQUOTIENT70. Stdlib only.

This is a compact subset of the 16,019-assertion local audit.
No finite test can prove a universal deterministic time lower bound.
"""
from itertools import combinations, product

def sat_count(n, clauses, xor_rows=()):
    total=0
    for bits in product((0,1), repeat=n):
        if any(sum(bits[i] for i in row[0])%2 != row[1] for row in xor_rows):
            continue
        if all(any(bits[abs(lit)-1] == int(lit>0) for lit in clause)
               for clause in clauses):
            total+=1
    return total

def parity_cnf3(triple, rhs):
    return [tuple(-(v+1) if bit else (v+1)
                  for v,bit in zip(triple,assignment))
            for assignment in product((0,1),repeat=3)
            if sum(assignment)%2 != rhs]

def main():
    checks=0
    full=parity_cnf3((0,1,2),0)+parity_cnf3((0,1,2),1)
    assert len(full)==8
    for mask in range(256):
        clauses=[c for i,c in enumerate(full) if mask>>i & 1]
        assert sat_count(3,clauses)==8-len(clauses)
        checks+=1
    for n in range(3,7):
        for a,b,c in combinations(range(n),3):
            triple=(a,b,c)
            xor=[(triple,1)]
            atmost=[(-(u+1),-(v+1)) for u,v in combinations(triple,2)]
            parity=parity_cnf3(triple,1)
            exact=sum(sum(bits[v] for v in triple)==1
                      for bits in product((0,1),repeat=n))
            assert sat_count(n,atmost,xor)==exact
            assert sat_count(n,parity+atmost)==exact
            checks+=2
    three=[(1,),(-1,2),(-1,-2)]
    assert sat_count(2,three)==0
    for i in range(3):
        assert sat_count(2,three[:i]+three[i+1:])>0
        checks+=1
    for d in range(2,14):
        one=[[1]*d for _ in range(d)]
        assert not any(row.count(0)==1 for row in one)
        for i in range(d):
            for j in range(d):
                mat=[row[:] for row in one]
                mat[i][j]=0
                assert sum(row.count(0)==1 for row in mat)==1
                mat[i][(j+1)%d]=0
                assert not any(row.count(0)==1 for row in mat)
                checks+=2
    for q in range(1,9):
        for orient in product((0,1),repeat=q):
            clauses=[(1,),(-(q+1),)]
            for i,b in enumerate(orient,1):
                clauses.append((-i,i+1 if b else -(i+1)))
            assert (sat_count(q+1,clauses)==0)==all(orient)
            checks+=1
    print("AFFINEQUOTIENT70 mini:", checks, "checks; 0 failures")

if __name__=="__main__":
    main()
