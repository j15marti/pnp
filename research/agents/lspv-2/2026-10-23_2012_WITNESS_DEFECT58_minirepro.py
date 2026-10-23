#!/usr/bin/env python3
"""WITNESS-DEFECT58 minimal independent reproducibility control.
Full charged bipartite-flow algorithm is in the conversation research package.
This script uses only the Python standard library, and independently checks
the exact-(2,2) core, both-label SAT/UNSAT family, and source assignments.
"""
from collections import Counter
from itertools import product

def make(q, unsat):
    assert q >= 4 and q % 2 == 0
    incident = [[] for _ in range(2*q)]
    edges = {}
    eid = 0
    for off in (0,q):
        for i in range(q):
            eid += 1
            a,b = off+i, off+(i+1)%q
            edges[eid]=(a,b)
            incident[a].append(eid)
            incident[b].append(eid)
    rungs=[]
    for i in range(q):
        eid += 1
        edges[eid]=(i,q+i)
        incident[i].append(eid)
        incident[q+i].append(eid)
        rungs.append(eid)
    assert len(edges)==3*q and all(len(s)==3 for s in incident)
    core=[]
    for group in incident:
        z=tuple(sorted(group))
        core.extend((z,tuple(-v for v in z)))
    ctr=Counter((abs(l),l>0) for clause in core for l in clause)
    assert all(ctr[(v,True)]==ctr[(v,False)]==2 for v in edges)
    assert len(core)==4*q
    star=tuple(sorted(incident[0]))
    patterns=[p for p in product((0,1),repeat=3) if sum(p) in (1,2)]
    defect=[tuple(-v if bit else v for v,bit in zip(star,p)) for p in patterns]
    target=tuple(int(v==rungs[0]) for v in star)
    if not unsat:
        others=sorted(v for v in edges if v not in set(star)|{rungs[1]})
        defect[patterns.index(target)]=(rungs[1],others[0],others[1])
    source=core+defect
    assert len(source)==4*q+6
    assert all(len(set(map(abs,c)))==3 for c in source)
    assert len({frozenset(c) for c in source})==len(source)
    return source,core,rungs

def holds(cnf,mask):
    return all(any(((mask>>(abs(l)-1))&1)==int(l>0) for l in clause)
               for clause in cnf)

def main():
    for q in (4,6):
        actual=[]
        for unsat in (False,True):
            source,core,rungs=make(q,unsat)
            models=sum(holds(source,mask) for mask in range(1<<(3*q)))
            assert (models==0)==unsat
            if not unsat:
                witness=sum(1<<(v-1) for v in rungs)
                assert holds(source,witness)
            actual.append(models)
        assert actual==([75,0] if q==4 else [1571,0])
        print({"q":q,"source_variables":3*q,"clauses":4*q+6,
               "SAT_models":actual[0],"UNSAT_models":actual[1],
               "defects":6,"three_way_bound":3**6,
               "old_full_boundary_bound":2**18})
if __name__=="__main__":
    main()
