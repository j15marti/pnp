from itertools import combinations
from collections import Counter
from functools import lru_cache
from math import comb, ceil
import math
import networkx as nx
import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog

# SWITCH-RECTIFIER2
# Exact endpoint-contact theorem + finite routing compression experiments.
#
# Model:
#   One optional entry contact and one optional exit contact per clause variable.
#   Every conflict edge is oriented from an entry-capable endpoint to an exit-capable endpoint.
#   Between entry and exit layers, a directed static rectifier network realizes the oriented relation.
#   Contacts are controlled by clause-presence bits; static routing edges are separately charged.
#
# This is NOT the minimum unrestricted contact-scheme complexity.

BEST_D5_ORDER=[
16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,
32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,
48,78,67,58,52,53,54,55,56,57,73,59,60,61,74,63,
64,65,66,50,68,69,70,71,72,51,62,75,76,77,49,79
]

def clauses(n):
    return [(T,p) for T in combinations(range(n),3) for p in range(8)]

def conflict(c1,c2):
    T1,p1=c1
    T2,p2=c2
    i1={v:i for i,v in enumerate(T1)}
    i2={v:i for i,v in enumerate(T2)}
    return all(((p1>>i1[v])&1)==((p2>>i2[v])&1)
               for v in set(T1)&set(T2))

def conflict_graph(n):
    C=clauses(n)
    M=len(C)
    E=[(i,j) for i in range(M) for j in range(i+1,M)
       if conflict(C[i],C[j])]
    return C,M,E

def oriented_relation(n,order=None):
    C,M,E=conflict_graph(n)

    # Two disjoint exact covers: all 8 sign patterns on two distinct variable triples.
    A=set(range(8))
    B=set(range(8,16))
    assert A.isdisjoint(B)

    Eset=set(E)
    assert all(tuple(sorted((i,j))) not in Eset for i,j in combinations(A,2))
    assert all(tuple(sorted((i,j))) not in Eset for i,j in combinations(B,2))

    mixed=[v for v in range(M) if v not in A and v not in B]
    if order is None:
        order=mixed
    pos={v:i for i,v in enumerate(order)}

    arcs=[]
    for u,v in E:
        if u in A:
            arcs.append((u,v))
        elif v in A:
            arcs.append((v,u))
        elif u in B:
            arcs.append((v,u))
        elif v in B:
            arcs.append((u,v))
        else:
            arcs.append((u,v) if pos[u]<pos[v] else (v,u))

    outdeg=[0]*M
    indeg=[0]*M
    for u,v in arcs:
        outdeg[u]+=1
        indeg[v]+=1

    contacts=sum(d>0 for d in outdeg)+sum(d>0 for d in indeg)
    return M,E,arcs,contacts,A,B

def greedy_rectifier(M,arcs):
    # Every sink expression begins as the OR of all predecessor source literals.
    # Repeated pairs with frequency >=3 are factored into reusable static nodes.
    expr=[set() for _ in range(M)]
    for u,v in arcs:
        expr[v].add(u)

    defs={}
    nid=M
    total_edges=len(arcs)

    while True:
        freq={}
        for s in expr:
            for a,b in combinations(sorted(s),2):
                freq[(a,b)]=freq.get((a,b),0)+1
        if not freq:
            break
        (a,b),k=max(freq.items(), key=lambda kv:(kv[1],kv[0]))
        if k<=2:
            break

        defs[nid]=(a,b)
        total_edges += 2
        replaced=0
        for s in expr:
            if a in s and b in s:
                s.remove(a)
                s.remove(b)
                s.add(nid)
                replaced+=1
        total_edges -= replaced
        nid+=1

    depth={i:0 for i in range(M)}
    for x in range(M,nid):
        a,b=defs[x]
        depth[x]=1+max(depth[a],depth[b])

    route_depth=max((depth[x]+1 for s in expr for x in s), default=0)

    @lru_cache(None)
    def sources(x):
        if x<M:
            return frozenset([x])
        a,b=defs[x]
        return sources(a)|sources(b)

    expected=[set() for _ in range(M)]
    for u,v in arcs:
        expected[v].add(u)

    recovered=[]
    for s in expr:
        z=set()
        for x in s:
            z.update(sources(x))
        recovered.append(z)

    assert recovered==expected

    return {
        "routing_edges": total_edges,
        "intermediate_nodes": len(defs),
        "routing_depth": route_depth,
        "output_refs": sum(map(len,expr)),
    }

def maximal_bicliques(n):
    C,M,rel=conflict_graph(n)
    relset=set(rel)
    idx={e:k for k,e in enumerate(rel)}

    G=nx.Graph()
    L=[("L",i) for i in range(M)]
    R=[("R",i) for i in range(M)]

    for side in (L,R):
        G.add_nodes_from(side)
        for i in range(M):
            for j in range(i+1,M):
                G.add_edge(side[i],side[j])

    for i in range(M):
        for j in range(M):
            if i!=j and tuple(sorted((i,j))) in relset:
                G.add_edge(("L",i),("R",j))

    cand={}
    for q in nx.find_cliques(G):
        A=tuple(sorted(i for s,i in q if s=="L"))
        B=tuple(sorted(i for s,i in q if s=="R"))
        if not A or not B or set(A)&set(B):
            continue

        key=min((A,B),(B,A))
        if key in cand:
            continue

        es=set()
        ok=True
        for i in A:
            for j in B:
                e=tuple(sorted((i,j)))
                if e not in idx:
                    ok=False
                    break
                es.add(idx[e])
            if not ok:
                break

        if ok and es:
            cand[key]=(es,len(A)+len(B),len(A),len(B))

    return M,rel,cand

def d5_fractional_depth2_lower():
    M,rel,cand=maximal_bicliques(5)
    vals=list(cand.values())

    rr=[]
    cc=[]
    dd=[]
    for j,(es,cost,a,b) in enumerate(vals):
        for e in es:
            rr.append(e)
            cc.append(j)
            dd.append(-1.0)

    A=sp.coo_matrix(
        (dd,(rr,cc)),
        shape=(len(rel),len(vals))
    ).tocsr()

    res=linprog(
        c=np.array([v[1] for v in vals],float),
        A_ub=A,
        b_ub=-np.ones(len(rel)),
        bounds=(0,None),
        method="highs",
    )
    assert res.success
    return len(cand),res.fun,ceil(res.fun-1e-9)

def main():
    print("MODEL_ENDPOINT_CONTACT_THEOREM")
    print("For M=8*C(n,3), any endpoint-routed realization has C >= 2M-16.")
    print("Reason: source-only and sink-only vertices are independent sets; each has size <=8.")
    print("Two disjoint exact covers attain 16 pure vertices, so C=2M-16 is exact in this model.")

    M4,E4,A4,C4,_,_=oriented_relation(4)
    R4=greedy_rectifier(M4,A4)
    print("D4",{
        "clause_bits":M4,
        "conflict_edges":len(E4),
        "controlled_contacts":C4,
        **R4
    })
    assert C4==48
    assert R4["routing_edges"]==96
    assert R4["routing_depth"]==1

    M5,E5,A5,C5,_,_=oriented_relation(5,BEST_D5_ORDER)
    R5=greedy_rectifier(M5,A5)
    print("D5",{
        "clause_bits":M5,
        "conflict_edges":len(E5),
        "controlled_contacts":C5,
        **R5
    })
    assert C5==144
    assert R5["routing_edges"]==548
    assert R5["intermediate_nodes"]==98
    assert R5["routing_depth"]==6

    nb,lp,lb=d5_fractional_depth2_lower()
    print("D5_DEPTH2",{
        "maximal_bicliques":nb,
        "fractional_weighted_cover":lp,
        "integer_lower_bound":lb,
        "known_greedy_upper_bound":605,
    })
    assert nb==15542
    assert lb==314

    print("WEIGHTED_TRADEOFF")
    print("D4 depth2 exact: 96 controlled contacts.")
    print("D4 routed: 48 controlled contacts + 96 static routing edges.")
    print("For objective lambda*C + R, routed beats depth2 exactly when lambda>2.")

    print("D5 depth2: 314 <= contact optimum <=605.")
    print("D5 routed construction: 144 controlled contacts + 548 static routing edges.")
    print("Against the known 605-contact construction, routed is cheaper when lambda>548/(605-144) ~= 1.1887.")
    print("Against the LP-certified lower bound 314, routed is certainly below every depth2 realization when lambda>548/(314-144) ~= 3.2236.")

    print("STATUS: endpoint-contact count is PROVED/EXACT in the declared routed architecture.")
    print("Routing compression numbers are COMPUTATIONAL upper bounds; unrestricted contact-scheme minimum remains OPEN.")
    print("P versus NP remains OPEN.")

if __name__=="__main__":
    main()
