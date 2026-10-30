#!/usr/bin/env python3
"""Infinitely scalable signed exact-(2,2) three-partite proper-3CNF,
with a one-pivot Shannon-DAG increase. Source-coded no-shrink control.
"""
from pathlib import Path
import json,random,math,sys,collections
sys.path.insert(0,str(Path(__file__).resolve().parent))
from arc_mixed_projection_test import Store,run_case,source_sat,bitcnf


def formula(k):
    assert k>=7 and k%2==1
    n=3*k
    clauses=[]
    for s in range(4):
        sign=1 if s<2 else -1
        for i in range(k):
            a=i+1
            b=k+(i+s)%k+1
            c=2*k+(i+2*s)%k+1
            clauses.append((sign*a,sign*b,sign*c))
    return n,clauses


def factored_projection(store, clauses, x):
    pivot=x+1
    other=[]; positive=[]; negative=[]
    for c in clauses:
        if pivot in c:
            positive.append(tuple(z for z in c if z!=pivot))
        elif -pivot in c:
            negative.append(tuple(z for z in c if z!=-pivot))
        else:
            other.append(c)
    # The formula is H AND (AND_i (x OR A_i)) AND (AND_j (-x OR B_j)).
    # Existentially eliminate x by distributivity, preserving the entire
    # residual Boolean function: H AND ((AND_i A_i) OR (AND_j B_j)).
    H=store.from_cnf(other)
    pa=store.from_cnf(positive)
    pb=store.from_cnf(negative)
    return store.gate('and',[H,store.gate('or',[pa,pb])])

def audit(k,seed=47):
    n,clauses=formula(k)
    assert len(clauses)==4*k
    assert len(set(tuple(sorted(map(abs,c))) for c in clauses))==4*k
    assert all(len(set(map(abs,c)))==3 for c in clauses)
    assert all(sum(v in c for c in clauses)==2 and sum(-v in c for c in clauses)==2 for v in range(1,n+1))
    # Linear hypergraph: every pair of variable names occurs in at most one edge.
    pairs=collections.Counter()
    for c in clauses:
        a,b,d=sorted(map(abs,c))
        for p in ((a,b),(a,d),(b,d)):
            pairs[p]+=1
    assert max(pairs.values())==1
    # Connected hypergraph; BFS on primal adjacency.
    neighbors=[set() for _ in range(n)]
    for c in clauses:
        ids=[abs(z)-1 for z in c]
        for x in ids:
            neighbors[x].update(y for y in ids if x!=y)
    visited={0}
    for x in list(range(n)):
        changed=True
        while changed:
            before=len(visited)
            for v in list(visited):visited.update(neighbors[v])
            changed=len(visited)>before
    assert len(visited)==n
    # Construct known witness: A_i=1, B_i=C_i=0.
    witness=([1]*k)+([0]*(2*k))
    assert source_sat(clauses,witness)
    # Separate stores avoid counting the unused naive Shannon nodes in the
    # serialized factored result. Compare against native CNF and original circuit.
    st=Store();root=st.from_cnf(clauses)
    old=st.nodesizes(root)
    allchildren=[]
    for x in range(n):
        before=st.calls
        nxt=factored_projection(st,clauses,x)
        d=st.nodesizes(nxt)
        allchildren.append(dict(x=x,**d,construct_gate_calls=st.calls-before))
    best=min(allchildren,key=lambda z:(z['bits'],z['x']))
    result={'source_cnf_bits':bitcnf(clauses,n),'source_circuit':old,
            'best_pivot':best,'all_pivots':allchildren,
            'search_gate_calls':sum(z['construct_gate_calls'] for z in allchildren)}
    st=Store();root=st.from_cnf(clauses)
    rng=random.Random(seed+k)
    checked=0
    for x in range(n):
        pr=factored_projection(st,clauses,x)
        for _ in range(50):
            a=[rng.randrange(2) for _ in range(n)]
            a[x]=0;y0=source_sat(clauses,a)
            a[x]=1;y1=source_sat(clauses,a)
            assert st.evaluate(pr,a)==(y0 or y1)
            checked+=1
    # Gate-only normalized identity: 3 extra gates, 2 fewer signed literal nodes.
    old=result['source_circuit']
    assert old['gates']==len(clauses)+1
    assert old['lits']==2*n
    assert old['edges']==4*len(clauses)
    # Since each four clauses has disjoint neighbors and each neighbor has other clauses,
    # each pivot creates 4 OR2, 2 AND2, 1 OR2 and removes its 2 signed literals.
    expected_bits_if_no_index_jump=8
    for child in result['all_pivots']:
        assert child['gates']==old['gates']+3,child
        assert child['lits']==old['lits']-2,child
        assert child['edges']==old['edges']-1,child
        assert child['reachable']==old['reachable']+1,child
        assert child['bits']>=old['bits']+expected_bits_if_no_index_jump
    return dict(k=k,n=n,m=len(clauses),source_cnf_bits=result['source_cnf_bits'],
       original_circuit_bits=old['bits'],best_child_circuit_bits=result['best_pivot']['bits'],
       min_delta=min(z['bits']-old['bits'] for z in result['all_pivots']),
       max_delta=max(z['bits']-old['bits'] for z in result['all_pivots']),
       full_pivot_attempt_gate_calls=result['search_gate_calls'],
       original_gates=old['gates'],child_gates=result['best_pivot']['gates'],
       original_edges=old['edges'],child_edges=result['best_pivot']['edges'],
       original_literals=old['lits'],child_literals=result['best_pivot']['lits'],
       independent_semantic_samples=checked,source_has_explicit_witness=True)

if __name__=='__main__':
    rows=[audit(k) for k in (7,9,11,15,21,31)]
    print(json.dumps(rows,indent=2))
    with open(str(Path(__file__).resolve().parent / 'arc_linear22_projection_firewall_results.json'),'w') as f:
        json.dump({'status':'COMPUTATIONAL','theorem':'explicit linear hypergraph first-pivot circuit node+1, edges-1, no raw circuit shrink under declared canonicalization','rows':rows},f,indent=2)
