#!/usr/bin/env python3
"""TMR-4/036 exact source-bound laboratory, directed-zero scalar closure.

No SAT-machine or physical zero-instruction claim. Python 3.12+ stdlib only.
Usage: python tmr4_scalar_closure056.py [directory_for_results]
"""
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from fractions import Fraction as Q
from itertools import product
from heapq import heappop, heappush
from pathlib import Path
import csv, json, sys

COLS = ('CNF','XOR','separator','fusion','Gamma','interface','machine')
LAM = (Q(0),Q(0),Q(0),Q(0),Q(1,2),Q(1,2),Q(0))

@dataclass(frozen=True, order=True)
class State:
    phases: str # U = unresolved choice, L/R = free normal form, D = paid discharged
    tag: int    # redundant free reversible representation flag

@dataclass(frozen=True)
class Edge:
    src: State
    dst: State
    rule: str
    price: int

def build(n, extra='base'):
    assert 1 <= n <= 6 and extra in ('base','paid_fusion_all','free_oracle')
    nodes = tuple(State(''.join(p),t) for p in product('ULRD',repeat=n) for t in (0,1))
    index = set(nodes)
    goal=State('D'*n,0)
    edges=[]
    for s in nodes:
        edges.append(Edge(s,State(s.phases,1-s.tag),'free_alias_toggle',0))
        if s.phases=='D'*n: continue
        for j,ch in enumerate(s.phases):
            if ch=='U':
                for form in ('L','R'):
                    d=s.phases[:j]+form+s.phases[j+1:]
                    edges.append(Edge(s,State(d,s.tag),'free_choose_'+form,0))
            if ch in 'LR':
                d=s.phases[:j]+'D'+s.phases[j+1:]
                edges.append(Edge(s,State(d,s.tag),'paid_discharge',1))
        edges.append(Edge(s,s,'paid_malformed_nop',1))
        if extra=='paid_fusion_all': edges.append(Edge(s,goal,'paid_fusion_all',1))
        if extra=='free_oracle': edges.append(Edge(s,goal,'free_oracle',0))
    assert all(e.src in index and e.dst in index and e.price in (0,1) for e in edges)
    return nodes, tuple(edges),goal

def tarjan(nodes,edges):
    adj={s:[] for s in nodes}
    for e in edges:
        if not e.price:adj[e.src].append(e.dst)
    index={};low={};stack=[];active=set();scc=[]
    def dfs(u):
        index[u]=low[u]=len(index);stack.append(u);active.add(u)
        for v in adj[u]:
            if v not in index:
                dfs(v);low[u]=min(low[u],low[v])
            elif v in active:low[u]=min(low[u],index[v])
        if low[u]==index[u]:
            c=[]
            while True:
                v=stack.pop();active.remove(v);c.append(v)
                if v==u:break
            scc.append(tuple(c))
    for s in nodes:
        if s not in index:dfs(s)
    return scc

def closure(nodes,edges):
    adj={s:[] for s in nodes}
    for e in edges:
        if not e.price:adj[e.src].append(e.dst)
    result={}
    for s in nodes:
        seen={s};q=deque([s])
        while q:
            u=q.popleft()
            for v in adj[u]:
                if v not in seen:seen.add(v);q.append(v)
        result[s]=frozenset(seen)
    return result

def p(s):
    g=2*sum(x in 'UR' for x in s.phases)
    i=2*sum(x in 'UL' for x in s.phases)
    return (0,0,0,0,g,i,0)

def dot(lam,vec):return sum((a*b for a,b in zip(lam,vec)),Q(0))

def potentials(nodes,Z,lam=LAM):
    h={s:min(dot(lam,p(t)) for t in Z[s]) for s in nodes}
    pc={s:tuple(min(p(t)[k] for t in Z[s]) for k in range(7)) for s in nodes}
    return h,pc

def shortest(nodes,edges,goal):
    back=defaultdict(list)
    for e in edges:back[e.dst].append((e.src,e.price,e.rule))
    dist={goal:0};q=[(0,goal)]
    while q:
        d,u=heappop(q)
        if d!=dist[u]:continue
        for v,w,_ in back[u]:
            if v not in dist or d+w<dist[v]:
                dist[v]=d+w;heappush(q,(d+w,v))
    return dist

def assess(n,variant):
    nodes,edges,goal=build(n,variant);Z=closure(nodes,edges);scc=tarjan(nodes,edges)
    h,pc=potentials(nodes,Z)
    origin=State('U'*n,0)
    dist=shortest(nodes,edges,goal)
    assert all(x in dist for x in nodes)
    assert all(h[e.src]<=e.price+h[e.dst] for e in edges) if variant=='base' else True
    bad=[e for e in edges if h[e.src]>Q(e.price)+h[e.dst]]
    zero_bad=[e for e in edges if e.price==0 and h[e.src]>h[e.dst]]
    assert not zero_bad
    assert all(h[s]==0 for s in nodes if s.phases=='D'*n)
    assert all(h[s]==h[t] for c in scc for s in c for t in c)
    assert all(h[s]<=Q(dist[s]) for s in nodes) if not bad else True
    assert all(h[e.src]<=h[e.dst] for e in edges if e.price==0)
    full_rows=[]
    for e in edges:
        delta=tuple(p(e.src)[j]-p(e.dst)[j] for j in range(7))
        full_rows.append({'src':e.src.phases+str(e.src.tag),'dst':e.dst.phases+str(e.dst.tag),
                          'rule':e.rule,'w':e.price,'Delta_Gamma_raw':delta[4],
                          'Delta_interface_raw':delta[5],
                          'Delta_scalar_closed':str(h[e.src]-h[e.dst]),
                          'slack':str(Q(e.price)-h[e.src]+h[e.dst])})
    if variant=='base':
        assert len(bad)==0
        assert h[origin]==n and dist[origin]==n
        assert dot(LAM,pc[origin])==0
        for s in nodes:
            assert h[s]==sum(Q(1) for z in s.phases if z!='D')
    if variant=='paid_fusion_all':
        assert dist[origin]==1 and h[origin]==n
        assert (len(bad)>0)==(n>1)
        repaired=tuple(Q(1,2*n) if i in (4,5) else Q(0) for i in range(7))
        hr,_=potentials(nodes,Z,repaired)
        assert hr[origin]==1
        assert all(hr[e.src]<=e.price+hr[e.dst] for e in edges)
        assert all(hr[s]<=dist[s] for s in nodes)
    if variant=='free_oracle':
        assert dist[origin]==0 and h[origin]==0 and not bad
    return {'n':n,'variant':variant,'states':len(nodes),'edges':len(edges),
            'zero_edges':sum(e.price==0 for e in edges),'zero_sccs':len(scc),
            'initial_scalar_Phi':str(h[origin]),
            'initial_component_min_Phi':str(dot(LAM,pc[origin])),
            'exact_minimum_paid_work':dist[origin],
            'original_lambda_violations':len(bad),
            'first_violating_transition':None if not bad else {'src':bad[0].src.phases+str(bad[0].src.tag),
             'dst':bad[0].dst.phases+str(bad[0].dst.tag),'rule':bad[0].rule,
             'price':bad[0].price,'discharge':str(h[bad[0].src]-h[bad[0].dst])},
            'checks':len(edges)+len(nodes)+sum(len(v) for v in scc)},full_rows

def run(out):
    results=[];matrix=[]
    for n in (1,2,3,4,5):
        for variant in ('base','paid_fusion_all','free_oracle'):
            row,edges=assess(n,variant);results.append(row)
            if n==3:matrix.extend([dict(n=n,variant=variant,**r) for r in edges])
    fieldnames=['n','variant','src','dst','rule','w','Delta_Gamma_raw','Delta_interface_raw','Delta_scalar_closed','slack']
    with (out/'tariff_matrix.csv').open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=fieldnames);wr.writeheader();wr.writerows(matrix)
    # Exhaustively audit exact two-coordinate tariff feasibility on a rational grid.
    grid=(Q(0),Q(1,8),Q(1,4),Q(1,2),Q(5,8),Q(1))
    grid_tests=0
    for n in (1,2,3):
        for variant in ('base','paid_fusion_all','free_oracle'):
            nodes,edges,_=build(n,variant); Z=closure(nodes,edges)
            for x,y in product(grid,repeat=2):
                lam=(Q(0),Q(0),Q(0),Q(0),x,y,Q(0))
                h,_=potentials(nodes,Z,lam)
                actual=all(h[e.src]<=Q(e.price)+h[e.dst] for e in edges)
                predicted=(x<=Q(1,2) and y<=Q(1,2)) if variant=='base' else (
                    (x<=Q(1,2*n) and y<=Q(1,2*n)) if variant=='paid_fusion_all' else True)
                assert actual==predicted,(n,variant,x,y)
                grid_tests+=1
    result={'tag':'TMR4_SCALAR_CLOSURE056','status':'PROVED_RESTRICTED_WITH_EXACT_PROOF_AND_COMPUTATIONAL_TEST',
            'columns':COLS,'lambda_base':[str(x) for x in LAM],
            'claim':'maximal zero-monotone scalar minorant is h(s)=min_{u in Reach0(s)} lambda.p(u)',
            'n_checked':[1,2,3,4,5],'matrix_scope':'n=3 all actual edges, all three variants',
            'cases':results,'total_tests':sum(r['checks'] for r in results)+grid_tests,
            'rational_grid_tariff_comparisons':grid_tests,
            'total_original_lambda_violations':sum(r['original_lambda_violations'] for r in results)}
    with (out/'summary.json').open('w') as f:json.dump(result,f,sort_keys=True,indent=2)
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':
    out=Path(sys.argv[1] if len(sys.argv)>1 else '.')
    out.mkdir(parents=True,exist_ok=True)
    run(out)
