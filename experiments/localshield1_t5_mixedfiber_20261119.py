#!/usr/bin/env python3
"""LOCALSHIELD T5: exact finite shield and edge-deletion experiments.
Standard library only. No general lower-bound assertions.
"""
from itertools import combinations, product
from collections import Counter, deque
import json, time

R = {(a,b) for a in range(5) for b in range(5) if (b-a)%5 in (1,3)}
P = [(u,v) for u in range(4) for v in range(u+1,4)]

def sat4(edges):
    for colors in product(range(5), repeat=4):
        if all((colors[u],colors[v]) in R for u,v in edges):
            return colors
    return None

def critical4():
    found=[]
    for d in product(range(3),repeat=len(P)):
        E=[(u,v) if orient==1 else (v,u) for (u,v),orient in zip(P,d) if orient]
        if E and sat4(E) is None and all(sat4(E[:i]+E[i+1:]) is not None for i in range(len(E))):
            found.append(E)
    return found

def transfer(signs):
    diffs={0}
    for sign in signs:
        steps={1,3} if sign==1 else {(-1)%5,(-3)%5}
        diffs={(a+b)%5 for a in diffs for b in steps}
    return tuple(sorted(diffs))

def dense_base(N):
    A={(x,y) for x in range(N) for y in range(N) if x!=y}
    threshold=(N+4)//5
    masks=[s for s in range(1,1<<N) if s.bit_count()>=threshold]
    minimum=10**9
    for s in masks:
        for t in masks:
            z=sum(bool(s>>a&1) and bool(t>>b&1) for a,b in A)
            minimum=min(minimum,z)
    return A,threshold,minimum

def lift(edges,N,A):
    return tuple((u*N+a,v*N+b) for u,v in edges for a,b in sorted(A))

def ac3(dom, edges, neighbors):
    """Correct full-arc support sweep to fixed point for five-domain T5."""
    dom=list(dom)
    changed=True
    while changed:
        changed=False
        for u,v in edges:
            mu,mv=dom[u],dom[v]
            nu=0;nv=0
            for a in range(5):
                if mu & (1<<a) and any(mv&(1<<b) and (a,b) in R for b in range(5)):
                    nu|=1<<a
            if not nu:return None
            for b in range(5):
                if mv&(1<<b) and any(nu&(1<<a) and (a,b) in R for a in range(5)):
                    nv|=1<<b
            if not nv:return None
            if nu!=mu or nv!=mv:
                dom[u]=nu;dom[v]=nv;changed=True
    return tuple(dom)

def solver(edges,n):
    ne=[0]*n
    for u,v in edges:
        ne[u]+=1;ne[v]+=1
    stats={'nodes':0}
    def rec(dom):
        stats['nodes']+=1
        dom=ac3(dom,edges,ne)
        if dom is None:return None
        if all(x.bit_count()==1 for x in dom):
            sol=tuple(x.bit_length()-1 for x in dom)
            assert all((sol[u],sol[v]) in R for u,v in edges)
            return sol
        i=min((i for i,x in enumerate(dom) if x.bit_count()>1), key=lambda i:(dom[i].bit_count(),-ne[i]))
        for v in range(5):
            if dom[i]&(1<<v):
                d=list(dom);d[i]=1<<v
                s=rec(tuple(d))
                if s is not None:return s
        return None
    out=rec((31,)*n)
    return out,stats['nodes']

def main():
    t=time.monotonic()
    crit=critical4()
    assert len(crit)==48
    D=crit[0]
    assert len(D)==5
    assert sat4(D) is None
    witnesses=[sat4(D[:i]+D[i+1:]) for i in range(5)]
    assert all(w is not None for w in witnesses)
    assert all((w[u],w[v]) not in R for w,(u,v) in zip(witnesses,D))
    path={l: sorted(set(transfer(signs) for signs in product((1,-1),repeat=l))) for l in range(1,7)}
    assert all(len(k)==5 for l in (4,5,6) for k in path[l])
    assert all(len(k)==3 for k in path[2])
    assert all(len(k)==4 for k in path[3])
    N=6
    A,threshold,h=dense_base(N)
    assert (threshold,h)==(2,2)
    E=lift(D,N,A)
    assert len(E)==5*30 and len(set(E))==len(E)
    # Proof-falsification challenge: test all 150 one-arc deletions with independently coded AC3+DFS.
    nodes=[]
    for j in range(len(E)):
        sol,k=solver(E[:j]+E[j+1:],4*N)
        assert sol is None,(j,sol)
        nodes.append(k)
    result={
      'status':'PASS finite checks only; P vs NP OPEN',
      'T5_rule':'(b-a) mod 5 in {1,3}',
      'critical_n4_count':len(crit),'critical_source_arcs':D,
      'deletion_witnesses':witnesses,
      'path_reachable_difference_sets':{str(l):[list(v) for v in path[l]] for l in path},
      'dense_base_size':N,'dense_base_arcs':len(A),'majority_threshold':threshold,
      'minimum_two_fiber_arc_count_h':h,
      'lift_vertices':4*N,'lift_arcs':len(E),
      'all_single_arc_deletions_unsat':len(E),
      'dfs_nodes_min':min(nodes),'dfs_nodes_max':max(nodes),'dfs_nodes_total':sum(nodes),
      'elapsed_s':round(time.monotonic()-t,3),
      'limits':'Finite base has triangles and is NOT a high-undirected-girth example; Kun provides high-girth constructive expansion for each fixed girth, but not the critical promise.'}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
