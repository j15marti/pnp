#!/usr/bin/env python3
"""Dependency-free exact audit. Run: python3 audit.py > results.json"""
import itertools as it
import json
import random
from collections import Counter
from functools import lru_cache

def clauses_for_cycle(n):
    assert n >= 3 and n % 3 == 0
    return [(i, (i+1) % n, (i+2) % n) for i in range(n)] + [tuple(range(i, i+3)) for i in range(0,n,3)]

def canonical_signed(n):
    return [(i+1,(i+1)%n+1,-((i+2)%n+1)) for i in range(n)] + [tuple(-(j+1) for j in range(i,i+3)) for i in range(0,n,3)]

def signed_random(n,rng):
    cs=clauses_for_cycle(n)
    occ={v:[] for v in range(n)}
    for ci,c in enumerate(cs):
        for j,v in enumerate(c): occ[v].append((ci,j))
    pos=set()
    for places in occ.values():
        assert len(places)==4
        pos.update(rng.sample(places,2))
    return [tuple((v+1) if (ci,j) in pos else -(v+1) for j,v in enumerate(c)) for ci,c in enumerate(cs)]

def brute(cs,n):
    return any(all(any(bool(a>>(abs(l)-1)&1)==(l>0) for l in c) for c in cs) for a in range(1<<n))

def frontier_dp(cs,n):
    """Exact projection onto variables needed by clauses not yet checked."""
    scopes=[{abs(l)-1 for l in c} for c in cs]
    ending=[[] for _ in range(n)]
    for c,s in zip(cs,scopes): ending[max(s)].append(c)
    previous=[]
    states={()}
    max_frontier=peak_states=0
    transitions=0
    for j in range(n):
        following=sorted({v for s in scopes if max(s)>j for v in s if v<=j})
        new=set()
        for state in states:
            for bit in (0,1):
                transitions+=1
                assignment=dict(zip(previous,state))
                assignment[j]=bit
                if all(any(assignment[abs(l)-1]==(l>0) for l in c) for c in ending[j]):
                    new.add(tuple(assignment[v] for v in following))
        previous,states=following,new
        max_frontier=max(max_frontier,len(following))
        peak_states=max(peak_states,len(states))
    return bool(states),max_frontier,peak_states,transitions

@lru_cache(None)
def hitting_min(edges):
    vertices=sorted(set().union(*map(set,edges))) if edges else []
    for q in range(len(vertices)+1):
        for h in it.combinations(vertices,q):
            if all(set(h).intersection(e) for e in edges): return q
    raise AssertionError('finite hitting set missing')

def find_hitting(edges,q):
    """Search tree with at most (3^(q+1)-1)/2 nodes for ternary edges."""
    calls=1
    if not edges: return (),calls
    if q==0: return None,calls
    for v in edges[0]:
        ans,c=find_hitting(tuple(e for e in edges if v not in e),q-1)
        calls+=c
        if ans is not None: return (v,)+ans,calls
    return None,calls

def components(edges,n,Y):
    adj={v:set() for v in range(n) if v not in Y}
    for e in edges:
        private=set(e)-Y
        for v in private: adj[v].update(private-{v})
    remaining=set(adj)
    out=[]
    while remaining:
        todo=[next(iter(remaining))]; comp=set()
        while todo:
            v=todo.pop()
            if v in comp: continue
            comp.add(v);todo.extend(adj[v]-comp)
        remaining-=comp;out.append(comp)
    return out

def run():
    rng=random.Random(20261028)
    boundary_checks=discovery_checks=truth_checks=0
    worst_slack=None
    for n in (3,6,9,12):
        edges=tuple(clauses_for_cycle(n))
        assert hitting_min(edges)==n//3
        for mask in range(1<<n):
            Y={v for v in range(n) if mask>>v&1}
            comps=components(edges,n,Y)
            qs=[]
            for comp in comps:
                private_edges=tuple(e for e in edges if not set(e)&Y and set(e)<=comp)
                q=hitting_min(private_edges);qs.append(q)
                ans,calls=find_hitting(private_edges,q)
                assert ans is not None and all(set(ans)&set(e) for e in private_edges)
                assert calls <= (3**(q+1)-1)//2
                if q:
                    ans,_=find_hitting(private_edges,q-1)
                    assert ans is None
                discovery_checks+=1
            b=len(Y);k=len(comps);q=max(qs,default=0)
            assert n<=3*(b+sum(qs))
            if b:
                assert k<=4*b
                assert n<=3*b+12*b*q
                slack=3*b+12*b*q-n
                worst_slack=slack if worst_slack is None else min(worst_slack,slack)
            else:
                assert k==1 and n<=3*q
            boundary_checks+=1
    answer_counts=Counter()
    for n,reps in ((3,30),(6,30),(9,30),(12,30),(15,10)):
        for _ in range(reps):
            cs=signed_random(n,rng)
            counts=Counter(l for c in cs for l in c)
            assert all(counts[v]==counts[-v]==2 for v in range(1,n+1))
            actual,w,s,t=frontier_dp(cs,n)
            assert actual==brute(cs,n)
            assert w<=4 and s<=16 and t<=32*n
            answer_counts[str(actual)]+=1;truth_checks+=1
    # Explicit controls cover UNSAT as well as SAT; these are not exact-(2,2).
    all_eight=list(it.product(*[(i,-i) for i in (1,2,3)]))
    for remove in range(-1,8):
        cs=all_eight if remove==-1 else all_eight[:remove]+all_eight[remove+1:]
        actual,w,s,t=frontier_dp(cs,3)
        assert actual==brute(cs,3)==(remove!=-1)
        truth_checks+=1
    scaling=[]
    for n in (3,6,12,30,120,300):
        cs=canonical_signed(n)
        witness=[v%3!=2 for v in range(n)]
        assert all(any(witness[abs(l)-1]==(l>0) for l in c) for c in cs)
        counts=Counter(l for c in cs for l in c)
        assert all(counts[v]==counts[-v]==2 for v in range(1,n+1))
        sat,w,s,t=frontier_dp(cs,n)
        assert sat and w<=4 and s<=16 and t<=32*n
        scaling.append(dict(n=n,clauses=len(cs),global_backdoor=n//3,frontier=w,peak_states=s,transitions=t))
    return dict(status='PASS',seed=20261028,boundary_subsets_checked=boundary_checks,local_discovery_checks=discovery_checks,truth_table_comparisons=truth_checks,random_exact22_answers=dict(answer_counts),minimum_boundary_bound_slack=worst_slack,scaling=scaling,limitations=['Finite audits do not prove asymptotics.','Runtime counts are DP transitions, not TM steps.','Explicit UNSAT controls are outside exact-(2,2).','No unrestricted SAT shrinker constructed.'])

if __name__=='__main__':
    print(json.dumps(run(),indent=2))
