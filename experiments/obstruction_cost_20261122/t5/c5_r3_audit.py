#!/usr/bin/env python3
"""Exact finite-template and anchored-source audits for three fresh C5 unknowns."""
import argparse
import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path
from time import perf_counter

D=tuple(range(5))
ALLOWED={tuple(sorted(t)) for t in ((0,1,2),(1,2,3),(2,3,4),(3,4,0),(4,0,1))}
TUPLES=tuple(itertools.product(D,repeat=3))
FULL=(1<<125)-1

def C(a,b,c):
    return tuple(sorted((a,b,c))) in ALLOWED

def rows():
    us=sorted({sum(1<<x for x in D if C(x,a,b))
               for a,b in itertools.combinations(D,2)})
    result=[]
    for v in range(3):
        for s in us:
            m=sum(1<<j for j,t in enumerate(TUPLES) if s&(1<<t[v]))
            result.append((f"U{v}:{s}",m))
    for u,v in itertools.combinations(range(3),2):
        for a in D:
            m=sum(1<<j for j,t in enumerate(TUPLES) if C(t[u],t[v],a))
            result.append((f"B{u}{v}:{a}",m))
    result.append(("T012",sum(1<<j for j,t in enumerate(TUPLES) if C(*t))))
    assert len(result)==46
    return result

def template():
    start=perf_counter()
    atoms=rows()
    cores=[]
    visited=Counter()
    # An earlier chosen row remains essential exactly while its private set
    # (assignments satisfying all other chosen rows but violating that row)
    # is nonempty. Adding rows can only shrink a private set.
    def visit(chosen,common,private,next_row):
        visited[len(chosen)]+=1
        for index in range(next_row,len(atoms)):
            m=atoms[index][1]
            new_private=common&~m
            if not new_private:
                continue
            old_private=[p&m for p in private]
            if any(p==0 for p in old_private):
                continue
            nxt=common&m
            new_chosen=chosen+(index,)
            if not nxt:
                cores.append(new_chosen)
            else:
                visit(new_chosen,nxt,old_private+[new_private],index+1)
    visit((),FULL,[],0)
    core_counts=dict(sorted(Counter(map(len,cores)).items()))
    assert core_counts=={2:135,3:950,4:4265,5:285}
    assert max(visited)==6
    # Revalidate every reported minimal core by direct tuple evaluation
    # using each atom's membership, independent of the DFS private sets.
    for core in cores:
        assert not any(all(atoms[i][1]&(1<<j) for i in core) for j in range(125))
        for omitted in core:
            assert any(all(atoms[i][1]&(1<<j) for i in core if i!=omitted)
                       for j in range(125))
    core_encoding="\n".join(",".join(map(str,core)) for core in sorted(cores)).encode()
    counts_with_ternary=dict(sorted(Counter(len(core) for core in cores if 45 in core).items()))
    five_shapes=Counter()
    for core in cores:
        if len(core)==5:
            u=sum(i<30 for i in core)
            t=int(45 in core)
            five_shapes[f"unary{u}_binary{5-u-t}_ternary{t}"]+=1
    # Complete relation closure, not sampling.
    seen={FULL}
    frontier=[FULL]
    while frontier:
        current=frontier.pop()
        for _,atom in atoms:
            nxt=current&atom
            if nxt not in seen:
                seen.add(nxt);frontier.append(nxt)
    return {
        "complete":True,"seconds":perf_counter()-start,
        "tuple_count":125,"atom_count":46,
        "row_names":[name for name,_ in atoms],
        "minimal_core_counts":core_counts,
        "minimal_core_count":len(cores),
        "all_minimal_cores_sorted_sha256":hashlib.sha256(core_encoding).hexdigest(),
        "irredundant_satisfiable_prefix_counts":dict(sorted(visited.items())),
        "minimal_cores_containing_ternary_counts":counts_with_ternary,
        "size_five_type_counts":dict(sorted(five_shapes.items())),
        "first_size_five_core":[atoms[i][0] for i in next(c for c in cores if len(c)==5)],
        "support_closure_count":len(seen),
        "support_closure_cardinality_histogram":dict(sorted(Counter(m.bit_count() for m in seen).items())),
        "contextual_fixed_bits":(len(seen)-1).bit_length(),
    }

# a0,...,a4,x,y,z are indices0,...,7.
SOURCE=[(i,(i+1)%5,(i+2)%5) for i in D]
SOURCE += [(5,1,4),(6,3,4),(5,6,1),(6,7,1),(6,7,3)]
REFERENCE=(0,1,2,3,4,0,2,0)

def source():
    start=perf_counter()
    def satisfies(a,selected):
        return all(C(*(a[v] for v in SOURCE[i])) for i in selected)
    all_rows=tuple(range(10))
    models=sum(satisfies(a,all_rows) for a in itertools.product(D,repeat=8))
    assert models==0
    failed=[i for i in all_rows if not satisfies(REFERENCE,(i,))]
    assert failed==[9]
    levels=[]
    for free in ((),(7,),(6,7),(5,6,7)):
        completions=[]
        for vals in itertools.product(D,repeat=len(free)):
            a=list(REFERENCE)
            for v,value in zip(free,vals):a[v]=value
            completions.append(tuple(a))
        for size in range(1,11):
            minimum_cores=[c for c in itertools.combinations(all_rows,size)
                           if not any(satisfies(a,c) for a in completions)]
            if minimum_cores:break
        levels.append({"free_indices":free,"minimum_core_size":size,
                       "minimum_cores":minimum_cores})
    assert [d["minimum_core_size"] for d in levels]==[1,2,4,5]
    witnesses={}
    for omitted in range(5,10):
        selected=[i for i in all_rows if i!=omitted]
        found=None
        for t in TUPLES:
            a=REFERENCE[:5]+t
            if satisfies(a,selected):found=a;break
        assert found is not None
        witnesses[omitted]=found
    return {"seconds":perf_counter()-start,"source_rows":SOURCE,
            "variable_order":["a0","a1","a2","a3","a4","x","y","z"],
            "all_assignments_examined":5**8,"models":models,
            "reference":REFERENCE,"reference_failed_rows":failed,
            "independent_levels":levels,"deletion_witnesses":witnesses}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--stage",choices=("template","source","all"),default="all")
    args=p.parse_args()
    output={"status":"PASS","stage":args.stage}
    if args.stage in ("template","all"):output["template"]=template()
    if args.stage in ("source","all"):output["source"]=source()
    print(json.dumps(output,indent=2,sort_keys=True))

if __name__=="__main__":main()
