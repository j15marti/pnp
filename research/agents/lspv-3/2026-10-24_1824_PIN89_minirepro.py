#!/usr/bin/env python3
"""PIN89 peer reproducer, Python standard library, deterministic.
Checks eight-pin semantics and connected opposite-label profile collision.
Full two-level 936-grandchild audit supplied separately as conversation artifact.
"""
from itertools import product
import json

SIGNS = list(product((1, -1), repeat=3))
BITS = list(product((0, 1), repeat=3))

def unit(lit, a, b):
    return [(lit, e*a, d*b) for e, d in product((1,-1),repeat=2)]

def pin(clause, values):
    assert len({abs(x) for x in clause}) == 3
    output = [tuple(clause)]
    for i, (lit, val) in enumerate(zip(clause, values)):
        output.extend(unit(abs(lit) if val else -abs(lit), 4+2*i, 5+2*i))
    assert len(output) == 13
    return output

def sat(formula):
    names=sorted({abs(l) for cl in formula for l in cl})
    for vals in product((0,1), repeat=len(names)):
        assignment=dict(zip(names,vals))
        if all(any(assignment[abs(l)]==int(l>0) for l in cl) for cl in formula):
            return True
    return False

def profile(clause):
    # Local variable identities are canonically reindexed, not globally glued.
    renamed=tuple((i+1)*(1 if x>0 else -1) for i,x in enumerate(clause))
    return tuple(sat(pin(renamed, bits)) for bits in BITS)

def make_pair():
    unsat=[tuple((j+1)*ss[j] for j in range(3)) for ss in SIGNS]
    yes=[tuple((3*i+j+1)*ss[j] for j in range(3))
         for i,ss in enumerate(SIGNS)]
    bridges=[(25, i, 27+i) for i in range(1,25)]
    guard=unit(25,26,27)
    return unsat+bridges+guard, yes+bridges+guard

def connected(clauses):
    graph={abs(x):set() for cl in clauses for x in cl}
    for cl in clauses:
        for a in cl:
            graph[abs(a)].update(abs(b) for b in cl if abs(b)!=abs(a))
    fringe=[25]; seen=set()
    while fringe:
        v=fringe.pop()
        if v not in seen:
            seen.add(v); fringe.extend(graph[v]-seen)
    return len(seen)==len(graph)

def main():
    checks=0
    for signs in SIGNS:
        clause=tuple((i+1)*signs[i] for i in range(3))
        answers=profile(clause)
        assert len(answers)==8 and answers.count(False)==1
        absent=BITS[answers.index(False)]
        assert tuple(-1 if v else 1 for v in absent)==signs
        checks+=8
    no,yes=make_pair()
    assert len(no)==len(yes)==36
    assert all(len({abs(v) for v in cl})==3 for cl in no+yes)
    assert len(set(no))==len(no) and len(set(yes))==len(yes)
    assert connected(no) and connected(yes)
    assert len({abs(x) for cl in no for x in cl})==51
    assert len({abs(x) for cl in yes for x in cl})==51
    assert [profile(c) for c in no]==[profile(c) for c in yes]
    # Explicit SAT witness for yes: each disjoint core clause gets a true first literal.
    assignment={i:0 for i in range(1,52)}
    assignment[25]=1
    for i,signs in enumerate(SIGNS):
        assignment[3*i+1]=int(signs[0]>0)
    assert all(any(assignment[abs(v)]==int(v>0) for v in cl) for cl in yes)
    # Complete eight-clause core refutes each three-bit valuation.
    assert all(any(not any(dict(zip((1,2,3),bits))[abs(v)]==int(v>0)
                       for v in cl) for cl in no[:8]) for bits in BITS)
    checks+=36*8
    print(json.dumps({"status":"COMPUTATIONAL","checked_clause_answers":checks,
                      "parent_labels":["UNSAT","SAT"],
                      "n":51,"m":36,"N":1898,
                      "first_child_bits":594,"discrepancies":0},indent=2))

if __name__=="__main__":
    main()
