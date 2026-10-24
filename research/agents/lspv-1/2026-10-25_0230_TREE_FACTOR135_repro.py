#!/usr/bin/env python3
"""Independent finite audit of signed interval-factor tree join.
Only Python standard library. All counts are logical, not physical TM costs.
"""
import itertools, json, random, hashlib
from collections import Counter
SEED=202610250230
rng=random.Random(SEED)
stats=Counter()

def satisfied(clauses, assignment):
    for lits,lo,hi in clauses:
        v=sum((bool(assignment[abs(x)]) if x>0 else not bool(assignment[-x])) for x in lits)
        if not lo<=v<=hi:return False
    return True

def source_decide(blocks):
    clauses=[c for block in blocks for c in block]
    names=sorted({abs(lit) for lits,_,_ in clauses for lit in lits})
    for vals in itertools.product((0,1),repeat=len(names)):
        stats['source_rows']+=1
        if satisfied(clauses,dict(zip(names,vals))):return True
    return False

def factor_decide(clauses,pins):
    # Independent edge-subset enumerator for the previous graph-factor construction.
    residual=[]
    for lits,lo,hi in clauses:
        k=sum((bool(pins[abs(x)]) if x>0 else not bool(pins[-x])) for x in lits if abs(x) in pins)
        residual.append((tuple(x for x in lits if abs(x) not in pins),lo-k,hi-k))
    occurrences={}
    for j,(lits,_,_) in enumerate(residual):
        for lit in lits: occurrences.setdefault(abs(lit),[]).append((j,lit>0))
    if any(len(v)>2 for v in occurrences.values()):raise ValueError('uncertified factor core')
    edges=[]; choice=[]
    for name,occ in occurrences.items():
        if len(occ)==1:edges.append((('c',occ[0][0]),('leaf',name)))
        elif occ[0][1]==occ[1][1]:edges.append((('c',occ[0][0]),('c',occ[1][0])))
        else:
            first=len(edges)
            edges += [(('c',occ[0][0]),('choice',name)),(('c',occ[1][0]),('choice',name))]
            choice.append((first,first+1))
    for bits in itertools.product((0,1),repeat=len(edges)):
        stats['factor_edges_tested']+=1
        if any(bits[a]+bits[b]!=1 for a,b in choice):continue
        degrees=Counter()
        for bit,(a,b) in zip(bits,edges):
            if bit:degrees[a]+=1;degrees[b]+=1
        if all(lo<=degrees[('c',j)]<=hi for j,(_,lo,hi) in enumerate(residual)):
            return True
    return False

def tree_decide(blocks,tree):
    n=len(blocks); adjacency=[set() for _ in blocks]
    for u,v in tree:adjacency[u].add(v);adjacency[v].add(u)
    parent={0:-1};order=[0]
    for u in order:
        for v in sorted(adjacency[u]):
            if v not in parent:parent[v]=u;order.append(v)
    if len(order)!=n or len(tree)!=n-1:raise ValueError('not tree')
    names=[{abs(x) for lits,_,_ in block for x in lits} for block in blocks]
    allnames=set().union(*names)
    for x in allnames:
        members={i for i in range(n) if x in names[i]}
        if members:
            queue=[min(members)];seen=set(queue)
            for u in queue:
                for v in adjacency[u]&members:
                    if v not in seen:seen.add(v);queue.append(v)
            if seen!=members:raise ValueError('running intersection fails')
    exposed=[{x for x in names[i] if any(x in names[j] for j in range(n) if j!=i)} for i in range(n)]
    for i in range(n):
        core=[x for x in names[i] if x not in exposed[i]]
        counts=Counter(abs(x) for lits,_,_ in blocks[i] for x in lits)
        # Higher-degree interior variables are assigned explicitly before factor calls.
    messages={}
    for i in reversed(order):
        ex=sorted(exposed[i]);sep=sorted(names[i]&names[parent[i]]) if parent[i]>=0 else []
        children=[v for v in adjacency[i] if parent.get(v)==i]
        msg={}
        for vals in itertools.product((0,1),repeat=len(ex)):
            pins=dict(zip(ex,vals));stats['boundary_assignments']+=1
            counts=Counter(abs(x) for lits,_,_ in blocks[i] for x in lits)
            high=sorted(x for x in names[i]-exposed[i] if counts[x]>2)
            local=False
            for hv in itertools.product((0,1),repeat=len(high)):
                stats['high_degree_branches']+=1
                allpins=dict(pins);allpins.update(zip(high,hv))
                stats['factor_calls']+=1
                if factor_decide(blocks[i],allpins):local=True;break
            if local and all(messages[v].get(tuple(pins[x] for x in sorted(names[i]&names[v])),False) for v in children):
                msg[tuple(pins[x] for x in sep)]=True
        messages[i]=msg
    return messages[0].get((),False)

def make_random(high_degree=False):
    # Star of four blocks. Global name 4 and edge names 1,2,3.
    # Private core names 5..12 have at most two occurrences per block.
    blocks=[]
    shapes=[[(1,2,5),(2,3,6),(3,4,5),(4,1,6)],
            [(1,4,7),(1,4,8),(1,7,8)],
            [(2,4,9),(2,4,10),(2,9,10)],
            [(3,4,11),(3,4,12),(3,11,12)]]
    for shape in shapes:
        block=[]
        for term in shape:
            lits=tuple(x if rng.getrandbits(1) else -x for x in term)
            demand=rng.choice([(1,3),(1,1),(0,2),(2,3),(0,3)])
            block.append((lits,*demand))
        blocks.append(block)
    if high_degree:
        for sg in (1,-1,1):
            blocks[0].append(((sg*13,1,4),rng.choice([0,1]),3))
    return blocks

def main():
    labels=Counter();trials=72
    for k in range(trials):
        blocks=make_random(high_degree=(k<16))
        a=source_decide(blocks);b=tree_decide(blocks,[(0,1),(0,2),(0,3)])
        assert a==b,(k,a,b)
        labels['SAT' if a else 'UNSAT']+=1
    # Compatible shared boundary but incompatible roots.
    good=[ [((1,),1,1)], [((1,),1,1)] ]
    bad=[ [((1,),1,1)], [((1,),0,0)] ]
    for blocks,want in [(good,True),(bad,False)]:
        assert source_decide(blocks)==want
        assert tree_decide(blocks,[(0,1)])==want
        labels['SAT' if want else 'UNSAT']+=1
    # A cyclic block-membership pattern cannot be accepted as a join tree.
    triangle=[ [((1,2),1,1)], [((2,3),1,1)], [((3,1),1,1)] ]
    assert not source_decide(triangle)
    try:tree_decide(triangle,[(0,1),(1,2)])
    except ValueError as exc:
        assert 'running intersection' in str(exc);stats['rejected_invalid_join']=1
    else:raise AssertionError('invalid join accepted')
    data={'seed':SEED,'tested_valid':trials+2,'SAT':labels['SAT'],'UNSAT':labels['UNSAT'],
          'invalid_joins_rejected':stats['rejected_invalid_join'],
          'boundary_assignments':stats['boundary_assignments'],
          'factor_calls':stats['factor_calls'],
          'high_degree_branches':stats['high_degree_branches'],
          'factor_edge_subsets':stats['factor_edges_tested'],
          'source_truth_rows':stats['source_rows'],
          'discrepancies':0,
          'disclaimer':'Finite semantic checks only; no FLMV bit-operation or peak-memory measurement.'}
    print(json.dumps(data,sort_keys=True,indent=2))
if __name__=='__main__':main()
