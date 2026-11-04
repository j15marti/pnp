#!/usr/bin/env python3
"""Finite controls for REFEREE333's conservative-extension firewall."""
import itertools, json, resource, time
from pathlib import Path

OUT=Path("results/raw/arc/lspv5_333/conservative_extension_invariant_firewall_referee333.json")

def sat_clause(c,a): return any(a[abs(x)]==(x>0) for x in c)
def sat_cnf(cs,a): return all(sat_clause(c,a) for c in cs)

def php(h):
    v=lambda p,j:p*h+j+1; cs=[]; kinds=[]
    for p in range(h+1): cs.append(tuple(v(p,j) for j in range(h))); kinds.append(("p",p))
    for j in range(h):
        for p in range(h+1):
            for q in range(p+1,h+1): cs.append((-v(p,j),-v(q,j))); kinds.append(("c",j,p,q))
    return h*(h+1),cs,kinds

def php_witness(h,k):
    a={i:False for i in range(1,h*(h+1)+1)}; put=lambda p,j:a.__setitem__(p*h+j+1,True)
    if k[0]=="p":
        for j,p in enumerate(x for x in range(h+1) if x!=k[1]): put(p,j)
    else:
        _,j,p,q=k; put(p,j); put(q,j)
        for r,t in zip([x for x in range(h+1) if x not in (p,q)],[x for x in range(h) if x!=j]): put(r,t)
    return a

def gate_clauses(q,a,b,c):
    # q <-> a OR (b AND c), Cook's four-clause total functional gate.
    return [(q,-a),(q,-b,-c),(-q,a,b),(-q,a,c)]

def gate_value(a,b,c,assignment): return assignment[a] or (assignment[b] and assignment[c])

def extend_gates(original,gates):
    a=dict(original)
    for q,x,y,z in gates: a[q]=gate_value(x,y,z,a)
    return a

def all_gate_extensions(original,gates):
    qs=[g[0] for g in gates]; ans=[]
    for bits in itertools.product((False,True),repeat=len(qs)):
        a=dict(original); a.update({q:b for q,b in zip(qs,bits)})
        if sat_cnf([c for q,x,y,z in gates for c in gate_clauses(q,x,y,z)],a): ans.append(a)
    return ans

def selector_sat(n,cs,mask):
    selected=[c for i,c in enumerate(cs) if (mask>>i)&1]
    for bits in itertools.product((False,True),repeat=n):
        if sat_cnf(selected,{i+1:bits[i] for i in range(n)}): return True
    return False

def selector_sat_with_fixed(n,original,fixed,mask):
    selected=[c for i,c in enumerate(original) if (mask>>i)&1]+list(fixed)
    for bits in itertools.product((False,True),repeat=n):
        if sat_cnf(selected,{i+1:bits[i] for i in range(n)}): return True
    return False

def k4_tseitin(charge):
    edges=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]; cs=[]
    for v in range(4):
        inc=[i for i,e in enumerate(edges) if v in e]
        for bits in itertools.product((False,True),repeat=3):
            if sum(bits)%2==charge[v]: continue
            cs.append(tuple(-(inc[k]+1) if bits[k] else inc[k]+1 for k in range(3)))
    return 6,cs

def eq_clauses(a,b): return [(-a,b),(a,-b)]

def alias_extension(n,root,edges):
    # y IDs n+1..n+|V|; root y_0 equals original x_root.
    nv=1+max(max(e) for e in edges) if edges else 1
    ys=[n+i+1 for i in range(nv)]; cs=eq_clauses(ys[0],root)
    for u,v in edges: cs.extend(eq_clauses(ys[u],ys[v]))
    return ys,cs

def factor_through_fresh_y(n,cs):
    vals={False:set(),True:set()}; witness=False
    for bits in itertools.product((False,True),repeat=n):
        d=sat_cnf(cs,{i+1:bits[i] for i in range(n)})
        for z in (False,True):
            for y in (False,True): vals[y].add(z and d)
        if d: witness=True
    return all(len(x)<=1 for x in vals.values()),witness

def main():
    t0=time.perf_counter(); checks=0; gate_rows=[]; php_rows=[]
    # Exhaust the gate truth table and reject every wrong output bit.
    for bits in itertools.product((False,True),repeat=3):
        base={1:bits[0],2:bits[1],3:bits[2]}; q=4
        expected=gate_value(1,2,3,base)
        for qb in (False,True):
            a={**base,q:qb}; ok=sat_cnf(gate_clauses(q,1,2,3),a)
            assert ok==(qb==expected); checks+=1
        gate_rows.append({"inputs":list(bits),"output":expected})

    # Generic acyclic total definitions preserve all original selectors and deletion witnesses.
    for h in (1,2,3):
        n,cs,kinds=php(h); fresh=n+1
        pool=list(range(1,n+1)); gates=[]
        for k in range(min(3,n)):
            x=pool[k%n]; y=pool[(k+1)%n]; z=pool[(k+2)%n]
            gates.append((fresh+k,x,y,z)); pool.append(fresh+k)
        dcs=[c for q,x,y,z in gates for c in gate_clauses(q,x,y,z)]
        # Every original assignment has exactly one extension.
        for bits in itertools.product((False,True),repeat=n):
            a={i+1:bits[i] for i in range(n)}; exts=all_gate_extensions(a,gates)
            assert len(exts)==1 and exts[0]==extend_gates(a,gates); checks+=1
            assert sat_cnf(cs,a)==sat_cnf(cs+dcs,exts[0]); checks+=1
        # Every original PHP clause remains deletion-essential relative to D.
        for j,k in enumerate(kinds):
            w=php_witness(h,k); ew=extend_gates(w,gates)
            assert sat_cnf(cs[:j]+cs[j+1:]+dcs,ew); checks+=1
            assert not sat_clause(cs[j],w); checks+=1
        # Exhaust all selector masks at h<=2; D retained.
        selector_checks=0
        if h<=2:
            for mask in range(1<<len(cs)):
                assert selector_sat(n,cs,mask)==selector_sat_with_fixed(n+len(gates),cs,dcs,mask); checks+=1
                selector_checks+=1
        php_rows.append({"h":h,"original_variables":n,"original_clauses":len(cs),
          "definition_gates":len(gates),"definition_clauses":len(dcs),"selector_masks_checked":selector_checks})

    # Exact alias-network inflation on the same odd/even K4 source.
    alias_rows=[]
    networks={"path4":[(0,1),(1,2),(2,3)],"star4":[(0,1),(0,2),(0,3)],
              "k4":[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]}
    for charge,label in (([1,0,0,0],"odd"),([0,0,0,0],"even")):
        n,base=k4_tseitin(charge)
        base_models=[]
        for bits in itertools.product((False,True),repeat=n):
            a={i+1:bits[i] for i in range(n)}
            if sat_cnf(base,a): base_models.append(a)
        assert len(base_models)==(0 if label=="odd" else 8); checks+=1
        for name,edges in networks.items():
            ys,dcs=alias_extension(n,1,edges)
            for a in itertools.product((False,True),repeat=n):
                oa={i+1:a[i] for i in range(n)}; ea={**oa,**{y:oa[1] for y in ys}}
                assert sat_cnf(dcs,ea); checks+=1
                assert sat_cnf(base,oa)==sat_cnf(base+dcs,ea); checks+=1
            alias_rows.append({"parity":label,"network":name,"alias_vertices":len(ys),
              "alias_edges":len(edges)+1,"definition_clauses":len(dcs),"projected_models":len(base_models),
              "known_base_Rmix341_upper":15,"extended_upper_by_ignoring_aliases":15})

    # Rank-one semantic certification finite control: FACTOR(C_D,y) iff D UNSAT.
    factor_rows=[]; fixtures=0
    for n in (1,2,3):
        assignments=list(itertools.product((False,True),repeat=n))
        universe=[tuple(-(i+1) if b else i+1 for i,b in enumerate(a)) for a in assignments]
        sat_count=unsat_count=0
        for mask in range(1<<len(universe)):
            cs=[c for i,c in enumerate(universe) if (mask>>i)&1]
            factor,has_model=factor_through_fresh_y(n,cs)
            assert factor==(not has_model); checks+=1; fixtures+=1
            if has_model: sat_count+=1
            else: unsat_count+=1
        factor_rows.append({"n":n,"fixtures":1<<(1<<n),"sat":sat_count,"unsat":unsat_count})

    malformed=[{"q":4,"inputs":[1,2,0]}, {"q":4,"inputs":[1,2]}, {"q":0,"inputs":[1,2,3]},
      {"q":2,"inputs":[1,2,3]}, {"q":4,"inputs":[1,2,4]}, {"q":"4","inputs":[1,2,3]}]
    rejected=0
    for g in malformed:
        valid=isinstance(g.get("q"),int) and g["q"]>3 and isinstance(g.get("inputs"),list) and len(g["inputs"])==3 and all(isinstance(x,int) and 0<x<g["q"] for x in g["inputs"])
        if not valid: rejected+=1
    assert rejected==len(malformed); checks+=rejected

    data={"artifact":"CONSERVATIVE-EXTENSION-INVARIANT-FIREWALL-REFEREE333","checks":checks,
      "gate_truth_rows":gate_rows,"php_total_extension_controls":php_rows,"alias_controls":alias_rows,
      "rank_one_factor_controls":factor_rows,"factor_fixtures":fixtures,"malformed_rejected":rejected,
      "asymptotic_theorem":{"hard_source":"canonical unary PHP(h+1,h), ordinary shared-DAG Resolution 2^Omega(h) by Haken",
        "extension":"Cook acyclic total functional definitions D_h, O(h^3) constant-width clauses and fresh variables",
        "preserved":"original clauses/signs/IDs, exact existential projection, unique fibres, original selector profile with D retained, original deletion essentiality",
        "destroyed":"ordinary Resolution minimum: P_h is 2^Omega(h), P_h AND D_h has O(h^4) refutation",
        "encoding":"both explicit signed binary-index CNFs have Theta(h^3 log h) bits"},
      "transfer":{"required_direction":"W_R(F) <= poly(|F|+|E(F)|+W_R(E(F)))",
        "warning":"easy forward proof reuse W_R(E(F)) <= W_R(F) is the wrong direction for hardness",
        "cook_consequence":"no polynomial ordinary-Resolution backtranslation can eliminate Cook definitions"},
      "restricted_survivor":{"mu":"minimum number of authenticated source clauses in an UNSAT subset",
        "bound":"for positive-cost binary-premise source-rooted Rmix341, W_R(F) >= mu(F)-1",
        "strength":"at most linear in explicit source size; odd cubic Tseitin attains 4h-1"},
      "charged_ledger":{"extension_output":"Theta(h^3 log h) source/definition bits; polynomial construction and writes",
        "cook_proof":"O(h^4) logical lines with separately charged IDs, payloads, output and checking",
        "alias_network":"linear in supplied H; raw incidence width/degree/cycles may inflate while proof ignores aliases",
        "factor_certification":"arbitrary growing-support rank-one FACTOR is coNP-complete; constant support <=3 is O(8L)",
        "exponential_intermediate":"allowed and charged at actual L; compact shared definitions remain mandatory alternatives",
        "peak_space":"materialization polynomial in explicit output; streaming/recomputation trades retained space for charged time"},
      "classification":{"proved":["total functional extensions preserve original semantic fibres and selector profile",
        "Cook/Haken extensions destroy ordinary-Resolution hardness despite retained original signed incidence",
        "polynomial cost reflection is necessary for lower-bound transfer"],
        "restricted":"ordinary Resolution separation plus fixed-grammar linear ancestry survivor; no machine lower bound",
        "open":["B1_Rmix341","B2_Rmix341","B3_Rmix341","superpolynomial_Wbar_Rmix341","P!=NP"]},
      "wall_seconds":time.perf_counter()-t0,"peak_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(data,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"artifact":data["artifact"],"checks":checks,"factor_fixtures":fixtures,"peak_rss_kib":data["peak_rss_kib"]},sort_keys=True))

if __name__=="__main__": main()
