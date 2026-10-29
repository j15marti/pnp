#!/usr/bin/env python3
"""Independent constructive control for LSPV-4 PAID-SELECTOR-GADGET224.

Outputs reproducible JSON from elementary finite checks. No SAT library needed.
The XOR-plus-2CNF model is explicit; checks are not machine-model timings.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import math
import random
from collections import defaultdict
from pathlib import Path

SEED = 20261029
RNG = random.Random(SEED)


def eval_lit(lit, bits):
    return (bool(bits[abs(lit)-1]) == (lit > 0))


def eval_cnf(formula, bits):
    return all(any(eval_lit(lit,bits) for lit in clause) for clause in formula)


def proper(formula):
    return all(len(c)==3 and len(set(map(abs,c)))==3 for c in formula)


def active_vars(formula):
    return sorted({abs(l) for c in formula for l in c})


def canonical_renumber(formula):
    names=active_vars(formula)
    remap={x:i+1 for i,x in enumerate(names)}
    return [tuple(remap[abs(l)] if l>0 else -remap[abs(l)] for l in c) for c in formula]


def source_components(formula):
    # Incidence components: connect variables occurring together in any clause.
    graph=defaultdict(set)
    for clause in formula:
        v=[abs(l) for l in clause]
        for a in v:
            graph[a].update(set(v)-{a})
    unseen=set(graph)
    comps=[]
    while unseen:
        root=next(iter(unseen));stack=[root];reached=set()
        while stack:
            v=stack.pop()
            if v in reached:continue
            reached.add(v);stack.extend(graph[v]-reached)
        comps.append(reached);unseen-=reached
    return comps


def connectedize(formula):
    # Fresh always-satisfiable 3-clauses link all incidence components.
    source=canonical_renumber(formula)
    comps=source_components(source)
    if len(comps)<2:return source
    n=max(active_vars(source))
    z=n+1
    bridges=[(z,min(comp),z+i+1) for i,comp in enumerate(comps)]
    return source+bridges


def convert_to_mixed(formula):
    assert proper(formula)
    n=max(active_vars(formula),default=0)
    xor=[]; binary=[]; groups=[]
    for j,c in enumerate(formula):
        s=(n+3*j+1,n+3*j+2,n+3*j+3)
        groups.append(s);xor.append((s,1))
        binary.extend((-s[a],-s[b]) for a,b in ((0,1),(0,2),(1,2)))
        binary.extend((-s[a],c[a]) for a in range(3))
    return {"n_source":n,"n_total":n+3*len(formula),"xor":xor,"binary":binary,"groups":groups}


def source_bit_iterator(n):
    return itertools.product((0,1),repeat=n)


def exact_port_by_local_existence(formula,bits,mixed):
    # Independently enumerate all 8 local selector assignments per gadget.
    for j,c in enumerate(formula):
        sj=mixed['groups'][j]
        local_binary=[(-sj[a],-sj[b]) for a,b in ((0,1),(0,2),(1,2))]
        local_binary += [(-sj[a],c[a]) for a in range(3)]
        ok=False
        for trial in itertools.product((0,1),repeat=3):
            ext=tuple(bits)+tuple(trial)
            assign={sj[i]:trial[i] for i in range(3)}
            def vl(lit):
                v=assign[abs(lit)] if abs(lit) in assign else bits[abs(lit)-1]
                return bool(v)==(lit>0)
            if (sum(trial)%2==1) and all(vl(a) or vl(b) for a,b in local_binary):
                ok=True;break
        if not ok:return False
    return True


def full_mixed_eval(mixed,bits):
    if not all((sum(bits[v-1] for v in xs)&1)==parity for xs,parity in mixed['xor']):return False
    return all(eval_lit(a,bits) or eval_lit(b,bits) for a,b in mixed['binary'])


def graph_components_undirected(n, edges):
    adj=[set() for _ in range(n+1)]
    for a,b in edges:
        aa,bb=abs(a),abs(b)
        if aa!=bb:adj[aa].add(bb);adj[bb].add(aa)
    unseen=set(range(1,n+1));count=0
    while unseen:
        count+=1;stack=[next(iter(unseen))];s=set()
        while stack:
            v=stack.pop()
            if v in s:continue
            s.add(v);stack.extend(adj[v]-s)
        unseen-=s
    return count


def affine_binary_clusters(mixed):
    n=mixed['n_total']
    parent=list(range(n+1))
    def find(a):
        while parent[a]!=a:
            parent[a]=parent[parent[a]]
            a=parent[a]
        return a
    def union(a,b):
        a=find(a);b=find(b)
        if a!=b:parent[b]=a
    for xs,_ in mixed['xor']:
        for x in xs[1:]: union(xs[0],x)
    reps=set(find(i) for i in range(1,n+1))
    edges={(find(abs(a)),find(abs(b))) for a,b in mixed['binary'] if find(abs(a))!=find(abs(b))}
    return graph_components_undirected(n,edges) if len(reps)==n else _n_components(reps,edges)


def _n_components(nodes,edges):
    adj={a:set() for a in nodes}
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    unseen=set(nodes);k=0
    while unseen:
        k+=1;st=[next(iter(unseen))];seen=set()
        while st:
            x=st.pop()
            if x in seen:continue
            seen.add(x);st.extend(adj[x]-seen)
        unseen-=seen
    return k


def computed_excess(mixed):
    # Every selector triple is a rank-2 affine component and all three selectors
    # occur in binary clauses. Every original variable is a rank-1 singleton.
    # Validate membership in both binary and affine support, independently.
    n=mixed['n_source'];m=len(mixed['groups'])
    seen={abs(v) for e in mixed['binary'] for v in e}
    assert seen==set(range(1,n+3*m+1))
    assert len(mixed['xor'])==m
    assert len(set(v for vs,_ in mixed['xor'] for v in vs))==3*m
    for xs,parity in mixed['xor']:
        assert parity==1 and len(xs)==3 and len(set(xs))==3
    return m


def edges_undirected(binary):
    return frozenset(tuple(sorted((abs(a),abs(b)))) for a,b in binary if abs(a)!=abs(b))


def vertex_cover_exists(edges,k):
    # Certified exhaustive bounded search. Useful only on small controls.
    E=frozenset(edges)
    if not E:return True
    if k<=0:return False
    a,b=next(iter(E))
    for v in (a,b):
        if vertex_cover_exists(frozenset(e for e in E if v not in e),k-1):return True
    return False


def encode_source(formula):
    n=max(active_vars(formula),default=0)
    return 'proper3 n='+str(n)+' m='+str(len(formula))+'\n'+''.join('cl '+' '.join(('+' if l>0 else '-')+str(abs(l)) for l in c)+'\n' for c in formula)


def encode_mixed(mixed):
    s='mixxor2 n='+str(mixed['n_total'])+' q='+str(len(mixed['xor']))+' b='+str(len(mixed['binary']))+'\n'
    for xs,parity in mixed['xor']:
        s+='xor '+' '.join(str(v) for v in xs)+' ='+str(parity)+'\n'
    for a,b in mixed['binary']:
        s+='or '+('+' if a>0 else '-')+str(abs(a))+' '+('+' if b>0 else '-')+str(abs(b))+'\n'
    return s


def positive_chain(m):
    return [(i+1,i+2,i+3) for i in range(m)]


def matched_pair():
    # Nine distinct proper clauses on four live variables in each source.
    triples=[tuple(xs) for xs in itertools.combinations(range(1,5),3)]
    eligible=[tuple(v if sg else -v for v,sg in zip(xs,signs)) for xs in triples for signs in itertools.product((0,1),repeat=3) if any(signs)]
    rng=random.Random(1204)
    rng.shuffle(eligible)
    sat=[]
    for c in eligible:
        sat.append(c)
        if len(sat)==9 and len(source_components(sat))==1 and len(active_vars(sat))==4:break
    assert len(sat)==9 and eval_cnf(sat,(1,1,1,1))
    unsat=[tuple(v if sg else -v for v,sg in zip((1,2,3),signs)) for signs in itertools.product((0,1),repeat=3)]
    unsat.append((1,3,4))
    assert len(unsat)==9 and len(source_components(unsat))==1
    return sat,unsat


def run():
    count={"clause_assignment":0,"mixed_full":0,"vertex_cover_negative":0,"connectedization":0,"matched_truth":0,"resolution_projection":0}
    # Truth-table enumeration of the complete extension for small clause counts.
    for n in (3,4):
        choices=[tuple(v if sg else -v for v,sg in zip(xs,signs)) for xs in itertools.combinations(range(1,n+1),3) for signs in itertools.product((0,1),repeat=3)]
        for m in (1,2,3):
            for rep in range(90):
                f=[choices[RNG.randrange(len(choices))] for _ in range(m)]
                f=canonical_renumber(f)
                nn=max(active_vars(f));g=convert_to_mixed(f)
                assert proper(f)
                assert len(g['xor'])==m and len(g['binary'])==6*m
                assert computed_excess(g)==m
                assert 2*m<=3*m
                for x in source_bit_iterator(nn):
                    expected=eval_cnf(f,x)
                    got=exact_port_by_local_existence(f,x,g)
                    assert expected==got
                    count['clause_assignment']+=1
                if m<=2:
                    # Independently enumerate the whole extended assignment space.
                    for bits in source_bit_iterator(g['n_total']):
                        expected=eval_cnf(f,bits[:nn]) and all(
                            sum(bits[v-1] for v in group)==1 and
                            all((not bits[group[i]-1]) or eval_lit(f[j][i],bits[:nn]) for i in range(3))
                            for j,group in enumerate(g['groups'])
                        )
                        assert full_mixed_eval(g,bits)==expected
                        count['mixed_full']+=1
    # Independently reproduce the classical z-elimination control exactly:
    # t=1..4, 16+256+4096+65536 = 69,904 surviving assignments.
    for t in range(1,5):
        for bits in source_bit_iterator(4*t):
            A=[bool(bits[2*i]) or bool(bits[2*i+1]) for i in range(t)]
            B=[bool(bits[2*t+2*j]) or bool(bits[2*t+2*j+1]) for j in range(t)]
            projected=any(all((z or ai) for ai in A) and all(((not z) or bj) for bj in B) for z in (False,True))
            compact=all(A) or all(B)
            resolvents=all(ai or bj for ai in A for bj in B)
            assert projected == compact == resolvents
            count['resolution_projection']+=1
    assert count['resolution_projection']==69904
    # Independence from original SAT: the joint cluster can be large on trivial positives.
    scaling=[]
    for m in (1,2,3,6,12,24,48,96,192):
        f=positive_chain(m);g=convert_to_mixed(f)
        assert len(source_components(f))==1
        assert affine_binary_clusters(g)==1
        assert computed_excess(g)==m
        S=len(encode_source(f));M=len(encode_mixed(g))
        assert M>S
        scaling.append({"clauses":m,"original_variables":m+2,"mixed_variables":4*m+2,"xor_equations":m,"binary_clauses":6*m,"projected_excess":m,"vertex_cover_lower":2*m,"vertex_cover_upper":3*m,"single_cluster":True,"original_encoded_bytes":S,"mixed_encoded_bytes":M,"size_ratio":round(M/S,5)})
        if m<=3:
            e=edges_undirected(g['binary'])
            assert not vertex_cover_exists(e,2*m-1)
            count['vertex_cover_negative']+=1
    # Every 3SAT formula admits a SAT-preserving proper connectedization.
    for n in (6,9,12):
        pieces=[(j+1,j+2,j+3) for j in range(0,n,3)]
        conn=connectedize(pieces)
        assert proper(conn) and len(source_components(conn))==1
        for x in source_bit_iterator(n):
            if eval_cnf(pieces,x):
                z=1
                y=(1,)*len(pieces)
                assert eval_cnf(conn,tuple(x)+(z,)+y)
                count['connectedization']+=1
        assert any(eval_cnf(conn,x) for x in source_bit_iterator(max(active_vars(conn))))
    # Matched SAT/UNSAT connected sources with equal n, m and encoded lengths.
    fs,fu=matched_pair(); gs,gu=convert_to_mixed(fs),convert_to_mixed(fu)
    assert len(encode_source(fs))==len(encode_source(fu))
    assert len(encode_mixed(gs))==len(encode_mixed(gu))
    assert len(source_components(fs))==len(source_components(fu))==1
    sat_results=[]
    for f,g in ((fs,gs),(fu,gu)):
        good=[x for x in source_bit_iterator(4) if eval_cnf(f,x)]
        good2=[x for x in source_bit_iterator(4) if exact_port_by_local_existence(f,x,g)]
        assert good==good2 and computed_excess(g)==len(f)==9
        assert affine_binary_clusters(g)==1
        sat_results.append(bool(good))
        count['matched_truth']+=16
    assert sat_results==[True,False]
    return {"status":"PASS","seed":SEED,"checks":count,"matched":{"source_n":4,"source_m":9,"source_encoded_bytes":len(encode_source(fs)),"mixed_encoded_bytes":len(encode_mixed(gs)),"sat_answers":sat_results,"K":9,"vertex_cover_lower":18},"scaling":scaling,"limitations":["Native TM steps are not measured: lengths count actual UTF-8 encoding bytes.","K and k are bounds on one portfolio, not lower bounds for all SAT algorithms.","The converter outputs a larger mixed formula and supplies no recursive shrinker.","The mixed encoding does not enforce exact-(2,2) signed occurrence balance.","Finite checks do not replace the universal reduction proof."]}

if __name__=='__main__':
    print(json.dumps(run(),sort_keys=True,indent=2))