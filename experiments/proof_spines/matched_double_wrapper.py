#!/usr/bin/env python3
"""Forward inner AND/OR reduction, recursive outer exact SAT solver.
Standard library only. No SAT calls occur inside inner().
Small-instance experiment, not a polynomial-time claim.
"""
import hashlib
import itertools as it
import json
import random
from collections import Counter
from functools import lru_cache
from pathlib import Path

def canon(f):
    return tuple(sorted(set(tuple(sorted(set(c))) for c in f)))

def normalize(f):
    vs=sorted({abs(x) for c in f for x in c})
    mapping={v:i+1 for i,v in enumerate(vs)}
    return canon(tuple(mapping[abs(x)]*(1 if x>0 else -1) for x in c) for c in f)

def size(f):
    n=max((abs(x) for c in f for x in c),default=0)
    w=max(1,n.bit_length())
    return w+sum(w+(w+1)*len(c) for c in f)

def terminal(f):
    if () in f: return False
    if not f: return True
    return None

def restrict(f,assignment,metrics):
    metrics['literal_visits']+=sum(map(len,f))
    out=[]
    for c in f:
        if any(abs(x) in assignment and assignment[abs(x)]==(x>0) for x in c): continue
        out.append(tuple(x for x in c if abs(x) not in assignment))
    return canon(out)

def simplify(f,metrics):
    while terminal(f) is None:
        metrics['literal_visits']+=sum(map(len,f))
        units=[c[0] for c in f if len(c)==1]
        if not units: break
        if any(-x in units for x in units): return ((),)
        f=restrict(f,{abs(x):x>0 for x in units},metrics)
    metrics['literal_visits']+=sum(map(len,f))
    return normalize(f)

def components(f,deleted,metrics):
    metrics['literal_visits']+=sum(map(len,f))
    vertices={abs(x) for c in f for x in c}-set(deleted)
    adj={v:set() for v in vertices}
    for c in f:
        vs=[abs(x) for x in c if abs(x) in vertices]
        if vs:
            for v in vs[1:]: adj[vs[0]].add(v); adj[v].add(vs[0])
    groups=[]
    while vertices:
        todo=[min(vertices)]; group=set()
        while todo:
            v=todo.pop()
            if v in group: continue
            group.add(v); vertices.discard(v)
            todo.extend(adj[v]-group)
        groups.append(group)
    return groups

def choose_boundary(f,strategy,metrics):
    occ=Counter(abs(x) for c in f for x in c)
    ranked=sorted(occ,key=lambda v:(-occ[v],v))
    fallback=(ranked[0],)
    if strategy not in ('separator','separator_fast'): return fallback
    # Exhaustive candidates of size <=2 for a finite structural diagnostic.
    # This cost is recorded, and is not claimed near-linear.
    best=None
    pool=sorted(occ) if strategy=='separator' else ranked[:4]
    for k in (1,2):
        for boundary in it.combinations(pool,k):
            metrics['separator_candidates']+=1
            groups=components(f,boundary,metrics)
            if len(groups)<2: continue
            weights=[]
            for group in groups:
                projected=[tuple(x for x in c if abs(x) in group) for c in f
                           if any(abs(x) in group for x in c)]
                metrics['literal_visits']+=sum(map(len,f))
                weights.append(size(normalize(projected)))
            score=(max(weights,default=0),2**k,boundary)
            if best is None or score<best[0]: best=(score,boundary)
    if best:
        metrics['separators_used']+=1
        metrics['max_boundary_size']=max(metrics['max_boundary_size'],len(best[1]))
        return best[1]
    return fallback

@lru_cache(None)
def prime_list(k):
    out=[]; p=2
    while len(out)<k:
        if all(p%q for q in out if q*q<=p): out.append(p)
        p+=1
    return tuple(out)

def inner(source,strategy='separator'):
    """Iterative forward builder. Leaves are genuine small standard CNFs.
    Integer node IDs are verified by exact formula keys, not hash equality.
    OR branches bind a common boundary assignment before component AND splits.
    """
    source=normalize(source)
    N=size(source); target=max(2,int(N**(2/3)))
    m={'literal_visits':0,'separator_candidates':0,'separators_used':0,
       'max_boundary_size':0,'SAT_calls':0,'intern_calls':0,'cache_reuses':0}
    nodes=[]; keys={}; todo=[]
    def intern(raw):
        m['intern_calls']+=1
        f=simplify(raw,m)
        if f in keys:
            m['cache_reuses']+=1
            return keys[f]
        idx=len(nodes); keys[f]=idx
        nodes.append({'formula':f,'type':None}); todo.append(idx)
        return idx
    root=intern(source)
    while todo:
        idx=todo.pop(); node=nodes[idx]; f=node['formula']; t=terminal(f)
        if t is not None:
            node.update(type='CONST',value=t); continue
        if size(f)<=target:
            node.update(type='LEAF'); continue
        groups=components(f,(),m) if strategy!='flat' else []
        if len(groups)>1:
            children=[]
            for group in groups:
                m['literal_visits']+=sum(map(len,f))
                children.append(intern([c for c in f if abs(c[0]) in group]))
            node.update(type='AND',children=sorted(set(children)))
            continue
        boundary=choose_boundary(f,strategy,m)
        children=[]; routes=[]
        ps=prime_list(4*max(abs(x) for c in f for x in c))
        for values in it.product((False,True),repeat=len(boundary)):
            assignment=dict(zip(boundary,values))
            child=intern(restrict(f,assignment,m)); children.append(child)
            # Audit identifier only, not a collision-free correctness premise.
            labels=[]
            for v,b in zip(boundary,values):
                alias=digest_byte(f,v)%2
                label=(0 if b else 2) if not alias else (3 if b else 1)
                labels.append([v,('TRUE','NOT_TRUE','FALSE','NOT_FALSE')[label],ps[4*(v-1)+label]])
            routes.append({'assignment':list(zip(boundary,values)),'prime_labels':labels,
                           'child':child,'tag':hashlib.sha256(repr((f,boundary,values)).encode()).hexdigest()})
        node.update(type='OR',children=sorted(set(children)),routes=routes)
    leaves=[x['formula'] for x in nodes if x['type']=='LEAF']
    assert all(size(f)<=target for f in leaves)
    m.update(N_bits=N,target_bits=target,dag_nodes=len(nodes),
             leaf_count=len(leaves),max_leaf_bits=max(map(size,leaves),default=0),
             child_bits=sum(map(size,leaves)),q_budget=N**(1/3),
             gates=sum(x['type'] in ('AND','OR') for x in nodes),
             stored_formula_bits=sum(size(x['formula']) for x in nodes))
    return {'nodes':nodes,'root':root,'metrics':m}

def digest_byte(f,v):
    return hashlib.sha256(repr((f,v)).encode()).digest()[0]

def evaluate(plan,leaf_solver):
    @lru_cache(None)
    def walk(idx):
        node=plan['nodes'][idx]; kind=node['type']
        if kind=='CONST': return node['value']
        if kind=='LEAF': return leaf_solver(node['formula'])
        if kind=='AND': return all(walk(c) for c in node['children'])
        if kind=='OR': return any(walk(c) for c in node['children'])
        raise ValueError(kind)
    return walk(plan['root'])

@lru_cache(None)
def reference(f):
    vs=sorted({abs(x) for c in f for x in c})
    for values in it.product((False,True),repeat=len(vs)):
        a=dict(zip(vs,values))
        if all(any(a[abs(x)]==(x>0) for x in c) for c in f): return True
    return False

def outer(f,strategy):
    metrics={'inner_calls':0,'literal_visits':0,'separator_candidates':0,
             'dag_nodes':0,'reference_calls':0}
    @lru_cache(None)
    def solve(f):
        t=terminal(f)
        if t is not None: return t
        plan=inner(f,strategy)
        metrics['inner_calls']+=1
        for k in ('literal_visits','separator_candidates','dag_nodes'): metrics[k]+=plan['metrics'][k]
        def child_solver(child):
            assert size(child)<size(f)
            return solve(child)
        return evaluate(plan,child_solver)
    answer=solve(normalize(f))
    metrics['cached_answers']=solve.cache_info().currsize
    return answer,metrics

def php(p,h):
    var=lambda i,j:i*h+j+1
    return canon([tuple(var(i,j) for j in range(h)) for i in range(p)]+
                 [(-var(i,j),-var(k,j)) for j in range(h) for i in range(p) for k in range(i+1,p)])

def planted_separator(seed,bridges=0):
    rng=random.Random(seed); f=[]; blocks=[list(range(3+3*i,6+3*i)) for i in range(4)]
    # Each block admits a planted all-true witness but has a non-affine OR constraint.
    for block in blocks:
        f.append(tuple(block))
        for s in (1,2):
            for _ in range(2):
                a,b=rng.sample(block,2)
                clause=(s*rng.choice((-1,1)),a*rng.choice((-1,1)),b)
                f.append(clause)
    # Add bridge clauses one at a time; all remain satisfied by all-true.
    for i in range(bridges):
        left=blocks[i%4]; right=blocks[(i+1)%4]
        f.append((left[i%3],-left[(i+1)%3],right[i%3]))
    return canon(f)

def xor_triangle(odd):
    f=[]
    for a,b,parity in ((1,2,0),(2,3,0),(1,3,int(odd))):
        for x,y in it.product((0,1),repeat=2):
            if x^y != parity: f.append((a if not x else -a,b if not y else -b))
    return canon(f)

def cases():
    cs=[tuple((i+1)*s for i,s in enumerate(sign)) for sign in it.product((-1,1),repeat=3)]
    for mask in range(256): yield 'exhaustive_3var',mask,canon(c for i,c in enumerate(cs) if mask>>i&1)
    for seed in (17,29):
        rng=random.Random(seed)
        for n in (5,8,12):
            for j in range(4):
                f=canon(tuple(v*rng.choice((-1,1)) for v in rng.sample(range(1,n+1),3)) for _ in range(round(4.3*n)))
                yield f'random_{n}var',seed*100+j,f
        for bridges in (0,1,2,3,4): yield f'planted_separator_bridges_{bridges}',seed,planted_separator(seed,bridges)
    yield 'PHP_4_3',0,php(4,3)
    yield 'PHP_3_3',0,php(3,3)
    yield 'XOR_SAT',0,xor_triangle(False)
    yield 'XOR_UNSAT',0,xor_triangle(True)
    yield 'Horn',0,canon([(-1,2),(-2,3),(-3,4),(-1,-4,5),(-5,6)])
    yield 'disjoint',0,canon([(1,2,3),(4,5,6),(7,8,9),(10,11,12)])

def main():
    rows=[]; sample=None
    for family,seed,f in cases():
        expected=reference(normalize(f))
        row={'family':family,'seed':seed,'SAT':expected,'input_bits':size(normalize(f))}
        for strategy in ('flat','components','separator','separator_fast'):
            plan=inner(f,strategy)
            assert evaluate(plan,reference)==expected
            answer,metrics=outer(f,strategy)
            assert answer==expected
            row[strategy]={'inner':plan['metrics'],'outer':metrics}
            if family=='planted_separator_bridges_0' and seed==17 and strategy=='separator_fast': sample=plan
        rows.append(row)
    # A deliberately unsafe AND merge loses shared-variable compatibility.
    left=canon([(1,)]); right=canon([(-1,)])
    unsafe={'left_SAT':reference(left),'right_SAT':reference(right),
            'naive_AND':reference(left) and reference(right),'joint_SAT':reference(canon(left+right))}
    assert unsafe['naive_AND'] and not unsafe['joint_SAT']
    out={'formula_cases':len(rows),'correctness_checks':8*len(rows),'errors':0,
         'SAT_calls_in_inner':0,'unsafe_AND_control':unsafe,'details':rows,
         'limitations':['Exhaustive separator search of size <=2 is charged, not near-linear.',
           'Counters omit sorting/hash overhead; stored_formula_bits is not total peak memory.',
           'Outer solver is exact but has no proved general polynomial bound.',
           'No use of a hypothetical polynomial solver code; no nonrelativization claimed.',
           'Internal formulas materialized, so no Williams-space guarantee.',
           'The algorithms implement small-separator heuristics, not the published FPT backdoor-depth algorithm.']}
    here=Path(__file__).parent
    (here/'results.json').write_text(json.dumps(out,indent=2)+'\n')
    (here/'example_dag.json').write_text(json.dumps(sample,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ('formula_cases','correctness_checks','errors','SAT_calls_in_inner','unsafe_AND_control')},indent=2))
    for row in rows:
        if row['family'] in ('planted_separator_bridges_0','planted_separator_bridges_4','PHP_4_3') or (row['family']=='random_12var' and row['seed']==1700):
            print(json.dumps(row))

if __name__=='__main__': main()

