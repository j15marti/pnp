#!/usr/bin/env python3
"""ARC214: exact, charged mixed 2CNF/XOR interface projection audit.
No external packages or SAT oracle. Run: python3 arc214_overlap_projection.py
"""
import itertools
import json
import random
import hashlib
from collections import Counter


def normal_clause(clause):
    s = set(int(v) for v in clause)
    if 0 in s:
        raise ValueError('zero is not a literal')
    if any(-v in s for v in s):
        return None  # tautology
    return tuple(sorted(s, key=lambda x:(abs(x), x<0)))


def project_2cnf(clauses, boundary):
    """Davis-Putnam existentially eliminates all variables outside boundary.
    In 2CNF every resolvent remains binary or shorter. Returns canonical clauses.
    """
    form = set()
    for c in clauses:
        cc = normal_clause(c)
        if cc is not None:
            assert len(cc) <= 2
            form.add(cc)
    touched = {abs(l) for c in form for l in c}
    events = 0
    peak = len(form)
    for v in sorted(touched - set(boundary)):
        positive = [c for c in form if v in c]
        negative = [c for c in form if -v in c]
        retained = {c for c in form if v not in c and -v not in c}
        for p in positive:
            for n in negative:
                events += 1
                cc = normal_clause(tuple(l for l in p if l != v) +
                                   tuple(l for l in n if l != -v))
                if cc is not None:
                    assert len(cc) <= 2
                    retained.add(cc)
        form = retained
        peak = max(peak, len(form))
    assert not ({abs(l) for c in form for l in c} - set(boundary))
    return tuple(sorted(form, key=lambda c:(len(c),c))), dict(resolutions=events,peak_clauses=peak)


def project_xor(equations, boundary):
    """Eliminate private XOR variables by row operations and dropping pivots.
    Each row is (iterable of 1-based variable indices, rhs parity 0/1).
    """
    rows=[]
    for variables,rhs in equations:
        mask=0
        for v in variables:
            assert v>0
            mask ^= 1 << (v-1)  # duplicates cancel
        rows.append([mask, int(rhs)&1])
    all_vars={i+1 for mask,_ in rows for i in range(mask.bit_length()) if mask>>i&1}
    updates=0
    for v in sorted(all_vars - set(boundary)):
        bit=1 << (v-1)
        pivot=next((i for i,r in enumerate(rows) if r[0]&bit),None)
        if pivot is None: continue
        pm,pr=rows.pop(pivot)
        for r in rows:
            if r[0]&bit:
                r[0]^=pm; r[1]^=pr; updates+=1
    # Make a linearly independent, reduced system on boundary; detect 0=1.
    basis={}
    for mask,rhs in rows:
        while mask:
            col=mask.bit_length()-1
            if col not in basis:
                basis[col]=(mask,rhs)
                break
            other,obit=basis[col]
            mask^=other;rhs^=obit;updates+=1
        else:
            if rhs:
                return (((),1),),dict(row_xors=updates,unsat=True)
    compact=[]
    for mask,rhs in basis.values():
        variables=tuple(i+1 for i in range(mask.bit_length()) if mask>>i&1)
        assert all(v in boundary for v in variables)
        compact.append((variables,rhs))
    compact=tuple(sorted(compact))
    assert len(compact)<=len(boundary)
    return compact,dict(row_xors=updates,unsat=False)


def vars2(clauses):
    return {abs(l) for c in clauses for l in c}


def varsxor(equations):
    return {v for vs,_ in equations for v in vs}


def projected_instance(clauses,equations):
    boundary=tuple(sorted(vars2(clauses)&varsxor(equations)))
    c2,stat2=project_2cnf(clauses,set(boundary))
    cx,statx=project_xor(equations,set(boundary))
    # Local renumbering eliminates source indices from child encoding.
    mapping={v:i+1 for i,v in enumerate(boundary)}
    child2=tuple(tuple((1 if l>0 else -1)*mapping[abs(l)] for l in c) for c in c2)
    childx=tuple((tuple(mapping[v] for v in vs),rhs) for vs,rhs in cx)
    return boundary,child2,childx,dict(**stat2,**statx)


def satisfies2(clauses, assignment):
    return all(any((assignment[abs(l)]==int(l>0)) for l in c) for c in clauses)


def satisfiesxor(rows,assignment):
    return all((sum(assignment[v] for v in vs)&1)==rhs for vs,rhs in rows)


def all_assignments(n):
    for bits in itertools.product((0,1),repeat=n):
        yield {i+1:v for i,v in enumerate(bits)}


def sat_mixed_brute(clauses,rows,n):
    return any(satisfies2(clauses,a) and satisfiesxor(rows,a) for a in all_assignments(n))


def projected_truth_set(clauses,rows,shared,n):
    allowed=set()
    for assignment in all_assignments(n):
        if satisfies2(clauses,assignment) and satisfiesxor(rows,assignment):
            allowed.add(tuple(assignment[v] for v in shared))
    return allowed


def projected_semantics(clauses,rows):
    boundary,pc,px,stats=projected_instance(clauses,rows)
    accepted=set()
    for assignment in all_assignments(len(boundary)):
        if satisfies2(pc,assignment) and satisfiesxor(px,assignment):
            accepted.add(tuple(assignment.values()))
    return boundary,pc,px,stats,accepted


def compact_bytes(clauses,rows):
    # Explicit physical encoding, not an abstract node or succinct pointer.
    return len(json.dumps({'2CNF':clauses,'XOR':rows},separators=(',',':')).encode())


def check_case(clauses,rows,n):
    b,pc,px,stats,got=projected_semantics(clauses,rows)
    expected=projected_truth_set(clauses,rows,b,n)
    assert got==expected, {'clauses':clauses,'rows':rows,'expected':expected,'got':got}
    # Separately check both component existential projections, not only SAT.
    bset=set(b)
    p2_raw, _=project_2cnf(clauses,bset)
    px_raw, _=project_xor(rows,bset)
    raw2_allowed=set();rawx_allowed=set()
    for a in all_assignments(n):
        zbits=tuple(a[v] for v in b)
        if satisfies2(clauses,a): raw2_allowed.add(zbits)
        if satisfiesxor(rows,a): rawx_allowed.add(zbits)
    for zbits in itertools.product((0,1),repeat=len(b)):
        z=dict(zip(b,zbits))
        assert (zbits in raw2_allowed)==satisfies2(p2_raw,z)
        assert (zbits in rawx_allowed)==satisfiesxor(px_raw,z)
    return dict(shared=len(b),parent_bytes=compact_bytes(clauses,rows),
                child_bytes=compact_bytes(pc,px),sat=bool(got),stats=stats)


def arc213_gadget(three_cnf,n):
    binary=[];xor=[]
    y=n
    for c in three_cnf:
        new=[]
        for lit in c:
            y+=1;new.append(y);binary.append((lit,y))
        xor.append((tuple(new),0))
    return binary,xor,y


def run():
    rng=random.Random(21420261029)
    tally=Counter()
    checks=0;peak_b=0;reduction_stats=[]
    for j in range(1200):
        n=rng.randrange(1,9)
        clauses=[];rows=[]
        for _ in range(rng.randrange(0,12)):
            k=rng.randrange(0,3)
            clauses.append(tuple((v if rng.randrange(2) else -v)
                                 for v in rng.sample(range(1,n+1),min(k,n))))
        for _ in range(rng.randrange(0,9)):
            k=rng.randrange(0,min(4,n)+1)
            rows.append((tuple(rng.sample(range(1,n+1),k)),rng.randrange(2)))
        d=check_case(clauses,rows,n)
        checks+=1;tally['SAT' if d['sat'] else 'UNSAT']+=1
        peak_b=max(peak_b,d['shared'])
    # Construct 3CNF gadgets. Source truth is checked independently.
    for j in range(60):
        n=3
        source=[]
        for _ in range(rng.randrange(1,4)):
            vs=rng.sample(range(1,n+1),3)
            source.append(tuple(v if rng.randrange(2) else -v for v in vs))
        binary,xor,nfull=arc213_gadget(source,n)
        d=check_case(binary,xor,nfull)
        source_sat=any(satisfies2(source,a) for a in all_assignments(n))
        assert d['sat']==source_sat
        assert d['shared']==3*len(source)
        checks+=1;tally['GADGET_SAT' if d['sat'] else 'GADGET_UNSAT']+=1
        peak_b=max(peak_b,d['shared'])
    # Three 3-variable XOR equations force z=0, while 2CNF forces z=1.
    xor_zero=[((1,3,4),0),((1,3,5),0),((1,4,5),0)]
    xor_one=[((1,3,4),1),((1,3,5),0),((1,4,5),0)]
    two_force_one=[(1,2),(1,-2)]
    no=check_case(two_force_one,xor_zero,5)
    yes=check_case(two_force_one,xor_one,5)
    assert not no['sat'] and yes['sat']
    checks+=2;tally['HOSTILE_UNSAT']+=1;tally['HOSTILE_SAT']+=1
    # A large physically padded source with b shared interface bits projects
    # to a nontrivial same-b core, then the second projection is a fixed point.
    for b in (3,5,9,17):
        clauses=[(i, i%b+1) for i in range(1,b+1)]
        rows=[((i,),1) for i in range(1,b+1)]
        n=b
        for z in range(1,b+1):
            for k in range(18):
                n+=1
                clauses.extend([(z,n),(-z,-n)])  # unique extension, no z restriction
                n+=1
                rows.append(((z,n),0))  # unique extension, no z restriction
        shared,pc,px,stat=projected_instance(clauses,rows)
        assert len(shared)==b
        parent=compact_bytes(clauses,rows)
        child=compact_bytes(pc,px)
        assert child<parent
        shared2,pc2,px2,stat2=projected_instance(pc,px)
        assert len(shared2)==b and pc2==pc and px2==px
        assert compact_bytes(pc2,px2)==child
        reduction_stats.append(dict(b=b,parent_bytes=parent,child_bytes=child,
                                    second_bytes=compact_bytes(pc2,px2),
                                    first_resolutions=stat['resolutions'],
                                    first_row_xors=stat['row_xors']))
        checks+=1;tally['FIXED_POINT_CONTROLS']+=1
    out=dict(status='PASS',case_checks=checks,random_cases=1200,gadget_cases=60,
             overlap_width_max=peak_b,answers=dict(tally),
             hostile_ternary_xor=dict(sat_case=yes,unsat_case=no),
             projection_fixed_points=reduction_stats,
             original_audit_sha256='05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca',
             limits=['The algorithm is polynomial in N for projecting to shared variables.',
                     'Solving the projected mixed instance still costs up to 2^b poly(N).',
                     'The projection-only step can become a fixed point at the second level.',
                     'This does not prove P=NP or P!=NP.'])
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':
    run()