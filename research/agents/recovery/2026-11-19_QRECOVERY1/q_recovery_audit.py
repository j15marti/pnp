#!/usr/bin/env python3
"""Targeted exact-one recovery checks. No random grids or solver timings.
Run: python q_recovery_audit.py PATH_TO_UNPACKED_t5_exact_one > q_recovery_results.json
All operation counts are logical checks, not native RAM instructions.
"""
import hashlib
import itertools as it
import json
from pathlib import Path
import sys

ROOT = Path(sys.argv[1])
W = ({1, 3}, {2, 4}, {0, 3}, {1, 4}, {0, 2})
def q(a, b, c, win=W):
    return (b in win[a]) != (c in win[a])
def lift(colors, edges, win=W):
    return list(colors) + [a if b in win[a] else b
                           for u,v in edges for a,b in [(colors[u],colors[v])]]

manifest = json.loads((ROOT/'SHA256SUMS.json').read_text())
for name, digest in manifest.items():
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest() == digest, name
out = {'status':'PASS', 'seed':None, 'mode':'exhaustive deterministic targeted checks',
       'manifest_files_verified':len(manifest),
       'archive_sha256':hashlib.sha256((ROOT.parent.parent/'T5_Exact_One_Experiments_2026-11-18.zip').read_bytes()).hexdigest()}
out['relation_counts'] = {'Q':sum(q(*a) for a in it.product(range(5), repeat=3)),
                         'P':sum(b in W[a] and c in W[a] for a,b,c in it.product(range(5), repeat=3))}
assert out['relation_counts'] == {'Q':60,'P':20}
assert not any(q(a,b,c) and b in W[a] and c in W[a] for a,b,c in it.product(range(5), repeat=3))
out['head_multiplicity'] = [[sum(q(h,a,b) for h in range(5)) for b in range(5)] for a in range(5)]
core = [(0,1,2),(0,1,3),(1,0,2),(1,2,3),(2,0,3)]
out['small_core_counts'] = [sum(all(q(*(a[v] for v in c)) for j,c in enumerate(core) if j!=omit)
                            for a in it.product(range(5),repeat=4)) for omit in [-1,0,1,2,3,4]]
assert out['small_core_counts'] == [0,10,40,10,30,25]

# New targeted comparison: explicit private-head assignments vs weighted colorings.
out['small_graphs'] = []
for alphabet,n,win in [(3,4,({1},{2},{0})),(5,3,W)]:
    universe = list(it.combinations(range(n),2))
    records=[]; checks=0; assignments=0
    for mask in range(1<<len(universe)):
        edges=[e for i,e in enumerate(universe) if mask>>i&1]
        direct=weighted=proper=0
        for tail in it.product(range(alphabet),repeat=n):
            weights=[sum(q(h,tail[u],tail[v],win) for h in range(alphabet)) for u,v in edges]
            term=1
            for w in weights: term*=w
            weighted+=term
            proper+=all(tail[u]!=tail[v] for u,v in edges)
            for heads in it.product(range(alphabet),repeat=len(edges)):
                assignments+=1
                ok=True
                for h,(u,v) in zip(heads,edges):
                    checks+=1
                    if not q(h,tail[u],tail[v],win): ok=False; break
                direct+=ok
        assert direct==weighted and bool(direct)==bool(proper)
        records.append({'edge_mask':mask,'proper_tail_count':proper,'Q_count':direct})
    out['small_graphs'].append({'alphabet':alphabet,'vertices':n,'edge_order':universe,
       'records':records,'full_assignment_attempts':assignments,'Q_evaluations':checks})

# Independently rebuild source graph; read, do not regenerate, imported witnesses.
n=5; edges=sorted({tuple(sorted((i,(i+1)%5))) for i in range(5)})
for _ in range(3):
    edges=sorted(set(edges)|{tuple(sorted(e)) for u,v in edges for e in [(u,n+v),(v,n+u)]}
                 |{(n+i,2*n) for i in range(n)})
    n=2*n+1
data=json.loads((ROOT/'redteam/mycielski_fixture.json').read_text())
clauses=[(n+i,u,v) for i,(u,v) in enumerate(edges)]
assert clauses==list(map(tuple,data['clauses'])) and (n,len(edges))==(47,236)
checks=0; equalities=0; lifted_checks=0
for rec in data['deletion_witnesses']:
    omitted=rec['omitted_clause']; values=rec['assignment']; u,v=edges[omitted]
    assert values[u]==values[v]; equalities+=1
    rebuilt=lift(values[:n],edges)
    for i,(h,a,b) in enumerate(clauses):
        assert q(rebuilt[h],rebuilt[a],rebuilt[b]) == (i!=omitted); lifted_checks+=1
        for rot in range(5):
            assert q((values[h]+rot)%5,(values[a]+rot)%5,(values[b]+rot)%5)==(i!=omitted)
            checks+=1
    for head in range(5): assert not q(head,values[u],values[v])
out['fixture']={'vertices':n,'edges':len(edges),'Q_variables':n+len(edges),
    'deletion_witnesses':equalities,'rotation_clause_checks':checks,'rebuilt_lift_clause_checks':lifted_checks,
    'all_tail_rows':5**n,'rotation_normalized_tail_rows':5**(n-1),
    'imported_girth':data['constraint_incidence_girth']}

# K6: all deletion witnesses and all tail rows, one color normalized.
edges=list(it.combinations(range(6),2)); histogram=[0]*len(edges); rowchecks=0
for tail in it.product(range(5), repeat=5):
    colors=(0,)+tail
    for i,(u,v) in enumerate(edges):
        rowchecks+=1
        if colors[u]==colors[v]: histogram[i]+=1; break
    else: raise AssertionError('K6 colored')
for omitted,(u,v) in enumerate(edges):
    colors=[None]*6; colors[u]=colors[v]=0
    for label,w in enumerate([w for w in range(6) if w not in (u,v)],1): colors[w]=label
    values=lift(colors,edges)
    assert all(q(values[6+i],values[a],values[b])==(i!=omitted) for i,(a,b) in enumerate(edges))
out['K6']={'normalized_rows':5**5,'first_bad_edge_histogram':histogram,
           'edge_comparisons':rowchecks,'deletion_witnesses':len(edges)}

# Arity-three modal decoder control: complete rectangle, two points per fiber.
valid=modechecks=0; diagonal_failure=None
for a in it.product(range(5),repeat=6):
    modes=[set(a[i:i+2]) for i in (0,2,4)]
    if all(q(a[i],a[j],a[k]) for i in (0,1) for j in (2,3) for k in (4,5)):
        valid+=1
        for triple in it.product(*modes): assert q(*triple); modechecks+=1
    if diagonal_failure is None and q(a[0],a[2],a[4]) and q(a[1],a[3],a[5]):
        for triple in it.product(*modes):
            if not q(*triple): diagonal_failure={'fiber_values':a,'bad_modal_triple':triple}; break
assert diagonal_failure is not None
out['ternary_modal']={'assignments':5**6,'valid_complete_lifts':valid,
                     'modal_checks':modechecks,'projection_only_counterexample':diagonal_failure}
out['space_metrics']={'audit':'No process-RAM or wall-time claim; imported JSON and exhaustive iterators live in Python.',
    'proposed_row_scanner':'v color cells + O(log(v+m)) control bits with read-only indexed source; output streamed.',
    'proposed_lift':'v retained colors + O(log(v+m)) control bits, or log workspace with separately supplied indexed read-only colors; full witness output v+m colors.',
    'scope':'Logical operation counts above are not complete machine-instruction counts or asymptotic lower bounds.'}
print(json.dumps(out,indent=2))
