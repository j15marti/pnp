from itertools import combinations
from collections import Counter
from math import comb, ceil
import networkx as nx

# SWITCH-CONTACT1
# Passive depth-2 contact-network analysis for the exact-weight-eight SAT classifier.
# Each clause-presence bit x_i controls an individual on/off contact.
# A biclique K_{A,B} in the clause-conflict graph is implemented as:
#   parallel contacts {x_a : a in A}, then parallel contacts {x_b : b in B}.
# It uses |A|+|B| controlled contacts and accepts whenever a selected conflict edge crosses A x B.
#
# D(4,8): solve the minimum-weight biclique cover exactly with scipy.optimize.milp.
# D(5,8): enumerate maximal bicliques, prove the standard |E|/kappa lower bound,
#         and construct a deterministic greedy weighted cover as an upper bound.
#
# This analyzes depth-2 biclique-form passive contact networks only.
# It is NOT the minimum unrestricted contact-scheme size.

def clauses(n):
    return [(T,p) for T in combinations(range(n),3) for p in range(8)]

def conflict(c1,c2):
    T1,p1=c1; T2,p2=c2
    i1={v:i for i,v in enumerate(T1)}
    i2={v:i for i,v in enumerate(T2)}
    return all(((p1>>i1[v])&1)==((p2>>i2[v])&1) for v in set(T1)&set(T2))

def conflict_graph_data(n):
    C=clauses(n); M=len(C)
    rel=[(i,j) for i in range(M) for j in range(i+1,M) if conflict(C[i],C[j])]
    return C,M,rel

def maximal_bicliques(n):
    C,M,rel=conflict_graph_data(n)
    relset=set(rel); idx={e:k for k,e in enumerate(rel)}
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
        es=set(); ok=True
        for i in A:
            for j in B:
                e=tuple(sorted((i,j)))
                if e not in idx:
                    ok=False; break
                es.add(idx[e])
            if not ok: break
        if ok and es:
            cand[key]=(es,len(A)+len(B),len(A),len(B))
    return M,rel,cand

def greedy_cover(rel,cand):
    uncovered=set(range(len(rel)))
    chosen=[]
    vals=list(cand.values())
    while uncovered:
        best=None
        for es,c,a,b in vals:
            gain=len(es & uncovered)
            if not gain: continue
            key=(gain/c,gain,-c,a*b)
            if best is None or key>best[0]:
                best=(key,es,c,a,b)
        if best is None:
            raise RuntimeError("cover failed")
        _,es,c,a,b=best
        chosen.append((c,a,b,len(es & uncovered)))
        uncovered-=es
    return sum(c for c,_,_,_ in chosen),chosen

def exact_d4(rel,cand):
    import numpy as np
    import scipy.sparse as sp
    from scipy.optimize import milp, LinearConstraint, Bounds

    vals=list(cand.items())
    rr=[]; cc=[]; dd=[]; costs=[]
    for j,(key,(es,c,a,b)) in enumerate(vals):
        costs.append(c)
        for e in es:
            rr.append(e); cc.append(j); dd.append(-1.0)
    A=sp.coo_matrix((dd,(rr,cc)),shape=(len(rel),len(vals))).tocsr()
    con=LinearConstraint(A,-np.inf*np.ones(len(rel)),-np.ones(len(rel)))
    res=milp(
        c=np.array(costs,float),
        integrality=np.ones(len(costs)),
        bounds=Bounds(0,1),
        constraints=con,
        options={"mip_rel_gap":0.0}
    )
    assert res.success
    chosen=[vals[j] for j,x in enumerate(res.x) if x>.5]
    cover=[0]*len(rel)
    for _,(es,c,a,b) in chosen:
        for e in es: cover[e]+=1
    assert min(cover)>=1
    return int(round(res.fun)),chosen,cover

def run(n):
    M,rel,cand=maximal_bicliques(n)
    types=Counter((a,b) for es,c,a,b in cand.values())
    kappa,a0,b0=max((a*b/(a+b),a,b) for es,c,a,b in cand.values())
    lower=ceil(len(rel)/kappa-1e-12)
    print(f"D({n},8) clause_bits={M} conflict_edges={len(rel)} maximal_bicliques={len(cand)}")
    print("biclique_types",sorted(types.items()))
    print(f"kappa={kappa:.12f} attained_by=K_{{{a0},{b0}}} weighted_cover_lower_bound={lower}")
    if n==4:
        optimum,chosen,cover=exact_d4(rel,cand)
        print("exact_depth2_contact_cost",optimum)
        print("chosen_bicliques",len(chosen))
        print("chosen_types",Counter((v[2],v[3]) for k,v in chosen))
        print("edge_cover_multiplicity_minmax",min(cover),max(cover))
        assert optimum==96
    else:
        upper,chosen=greedy_cover(rel,cand)
        print("greedy_depth2_contact_upper",upper)
        print("greedy_bicliques",len(chosen))
        print("greedy_types",Counter((a,b) for c,a,b,g in chosen))
        assert lower==298
        assert upper==605

if __name__=="__main__":
    run(4)
    run(5)
    print("STATUS COMPUTATIONAL: exact for D4 depth-2 weighted biclique cover; D5 lower/greedy-upper only.")
    print("UNRESTRICTED contact schemes, rectifier networks, circuits, branching programs, and RAM algorithms are not lower-bounded here.")
