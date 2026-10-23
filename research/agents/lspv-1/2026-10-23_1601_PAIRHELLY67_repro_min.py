#!/usr/bin/env python3
"""Self-contained PAIRHELLY67 core auditor (stdlib, exhaustive small cases).
The complete 9793-assertion battery is available in the research handoff archive.
This minimal independent version checks the key two-variable and two-ternary claims.
No finite test proves a deterministic SAT lower bound.
"""
from itertools import combinations_with_replacement, product

def sat(cnf, n):
    for assignment in product((False, True), repeat=n):
        if all(any(assignment[abs(lit)-1] == (lit > 0)
                   for lit in clause) for clause in cnf):
            return True
    return False

def choice_sat(B, T, n):
    if not sat(B, n):
        return False
    for choices in product(*T):
        units = [(u,) for u in choices]
        if all(sat(B + [units[a], units[b]], n)
               for a in range(len(units))
               for b in range(a, len(units))):
            return True
    return False

def helly_two_var_exhaustive():
    atoms = [(1,),(-1,),(2,),(-2,),
             (1,2),(1,-2),(-1,2),(-1,-2)]
    checks = 0
    for mask in range(1 << len(atoms)):
        B = [atoms[i] for i in range(8) if mask >> i & 1]
        if not sat(B, 2):
            continue
        for m in range(16):
            U = [(1,-1,2,-2)[i] for i in range(4) if m >> i & 1]
            pair = all(sat(B+[(u,), (v,)], 2)
                       for u,v in combinations_with_replacement(U,2))
            actual = sat(B+[(u,) for u in U], 2)
            assert pair == actual, (B,U)
            checks += 1
    return checks

def two_group_exhaustive():
    T = [(1,2,3),(4,5,6)]
    cross = [(-a,-b) for a in T[0] for b in T[1]]
    checks = 0
    for mask in range(512):
        B = [c for i,c in enumerate(cross) if mask >> i & 1]
        expected = mask != 511
        assert sat(B+T, 6) == expected
        assert choice_sat(B,T,6) == expected
        checks += 2
    assert not sat(cross+T,6)
    for i in range(11):
        source = cross+T
        assert sat(source[:i]+source[i+1:],6)
        checks += 1
    return checks

def single_edge_drop():
    checks=0
    for k in range(2,10):
        before=3**k
        after=before-3**(k-2)
        if k<=7:
            brute=sum(not (seq[0]==0 and seq[1]==0)
                      for seq in product(range(3),repeat=k))
            assert brute==after
            checks+=1
        assert before-after==3**(k-2)
        checks+=1
    return checks

def ladder_checks():
    checks=0
    for q in range(1,9):
        for fields in product((0,1), repeat=q):
            cnf=[(1,),(-(q+1),)]
            for i,b in enumerate(fields,1):
                cnf.append((-i, i+1 if b else -(i+1)))
            assert sat(cnf,q+1)==(not all(fields))
            checks+=1
    return checks

if __name__ == "__main__":
    result = {
        "2CNF_pairwise_Helly":helly_two_var_exhaustive(),
        "2_group_conflict_exact":two_group_exhaustive(),
        "single_edge_amortization":single_edge_drop(),
        "implication_ladders":ladder_checks()
    }
    print(result)
    print("PASSED",sum(result.values()),"finite assertions; P vs NP OPEN.")
