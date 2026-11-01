#!/usr/bin/env python3
"""Independent LSPV-5 referee for source-authenticated affine prefix cuts.

Deterministic, standard-library only, exhaustive on the small named sources.
This is not a native FLMV implementation and proves no SAT time lower bound.
"""
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path

F9_POS=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
F9_NEG=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F9=F9_POS+tuple(tuple(-x for x in c) for c in F9_NEG)
F9_U={8:0,3:0,7:0,6:0,1:1,5:1}
F15_POS=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),
         (6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
F15_NEG=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),
         (4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=F15_POS+tuple(tuple(-x for x in c) for c in F15_NEG)
F15_S=dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))
F9_CYCLES=((3,4,10),)
F15_CYCLES=((1,10,11),(2,3,14))

def grammar(F):
    if not F or not all(len(c)==3 for c in F):
        return False
    n=max(abs(l) for c in F for l in c)
    if len(F)*3!=4*n:
        return False
    if len({tuple(sorted(c)) for c in F})!=len(F):
        return False
    counts=Counter((abs(l),l>0) for c in F for l in c)
    return all(len({abs(l) for l in c})==3 and
               (all(l>0 for l in c) or all(l<0 for l in c))
               for c in F) and all(counts[v,True]==counts[v,False]==2
                                   for v in range(1,n+1))

def truth(F,a):
    return all(any(a[abs(l)]==int(l>0) for l in c) for c in F)

def extensions(F,p):
    n=max(abs(l) for c in F for l in c)
    free=[v for v in range(1,n+1) if v not in p]
    for bits in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,bits))}
        if truth(F,a):
            yield a

def gate(F,p,cycles):
    n=max(abs(l) for c in F for l in c)
    free=[v for v in range(1,n+1) if v not in p]
    uncovered=[];covered=[]
    for j,c in enumerate(F):
        if any(abs(l) in p and p[abs(l)]==int(l>0) for l in c):
            covered.append(j)
        else:
            uncovered.append(j)
    assert not any(all(abs(l) in p for l in F[j]) for j in uncovered)
    sc=Counter()
    for j in covered:
        for l in F[j]:
            if abs(l) not in p:
                sc[abs(l),l>0]+=1
    eta=sum(min(sc[v,True],sc[v,False]) for v in free)
    prefs={v:(0 if sc[v,True]>sc[v,False] else 1)
           for v in free if sc[v,True]!=sc[v,False]}
    return dict(n=n,free=free,uncovered=uncovered,covered=covered,prefs=prefs,
                eta=eta,e=2*len(free)-len(uncovered),
                nu=len(cycles),delta=2*len(free)-len(uncovered)-eta-len(cycles))

def certify_cycles(F,p,cycles):
    used=set()
    for cyc in cycles:
        assert len(cyc)%2==1 and len(set(cyc))==len(cyc)
        assert not used.intersection(cyc)
        used.update(cyc)
        deg=Counter()
        for j in cyc:
            free=[abs(l) for l in F[j] if abs(l) not in p]
            assert len(free)==2
            deg.update(free)
        assert len(deg)==len(cyc) and all(d==2 for d in deg.values())
    return True

def base_rows(F,p,cycles,g):
    oncycle={j for cyc in cycles for j in cyc}
    rows=[]
    for j in g["uncovered"]:
        if j in oncycle:
            continue
        free=[l for l in F[j] if abs(l) not in p]
        mask=sum(1<<(abs(l)-1) for l in free)
        rhs=1^((len(free)&1) if F[j][0]<0 else 0)
        rows.append((mask,rhs,("outside_parity",j),frozenset()))
    for v,b in sorted(g["prefs"].items()):
        rows.append((1<<(v-1),b,("preference",v),frozenset()))
    return rows

def choice_rows(F,p,cyc,choice,coord):
    out=[]
    dep=frozenset({coord})
    for j in cyc:
        free=[abs(l) for l in F[j] if abs(l) not in p]
        assert len(free)==2
        if j==choice:
            val=int(F[j][0]>0)
            for v in free:
                out.append((1<<(v-1),val,("both_true",coord,j,v),dep))
        else:
            out.append(((1<<(free[0]-1))^(1<<(free[1]-1)),1,
                        ("one_true",coord,j),dep))
    return out

def eliminate(rows):
    """Return rank and a provenance-checked contradiction, if one exists."""
    basis={}
    for idx,(mask,rhs,tag,dep) in enumerate(rows):
        m=mask;r=rhs;prov=1<<idx
        while m:
            p=m.bit_length()-1
            if p not in basis:
                basis[p]=(m,r,prov)
                break
            bm,br,bp=basis[p]
            m^=bm;r^=br;prov^=bp
        if not m and r:
            ids=[i for i in range(len(rows)) if (prov>>i)&1]
            xm=0;xr=0
            for i in ids:
                xm^=rows[i][0];xr^=rows[i][1]
            assert xm==0 and xr==1
            return {"consistent":False,"rank":len(basis),"proof_ids":ids,
                    "proof_tags":[rows[i][2] for i in ids],
                    "proof_dependencies":sorted(set().union(*(rows[i][3] for i in ids)))}
    return {"consistent":True,"rank":len(basis),"proof_ids":[],
            "proof_tags":[],"proof_dependencies":[]}

def system(F,p,cycles,choices):
    g=gate(F,p,cycles)
    rows=base_rows(F,p,cycles,g)
    for i,ch in enumerate(choices):
        rows.extend(choice_rows(F,p,cycles[i],ch,i))
    e=eliminate(rows)
    e["rows"]=len(rows)
    e["choices"]=list(choices)
    return e

def affine_models(F,p,cycles,choices):
    g=gate(F,p,cycles)
    rows=base_rows(F,p,cycles,g)
    for i,ch in enumerate(choices):
        rows.extend(choice_rows(F,p,cycles[i],ch,i))
    out=[]
    for bits in product((0,1),repeat=len(g["free"])):
        a={**p,**dict(zip(g["free"],bits))}
        if all(((mask & sum((a[v]<<(v-1)) for v in a)).bit_count()&1)==rhs
               for mask,rhs,_,_ in rows):
            out.append(a)
    return out

def actual_cycle_choice(F,p,cyc,a):
    over=[]
    for j in cyc:
        free=[l for l in F[j] if abs(l) not in p]
        t=sum(a[abs(l)]==int(l>0) for l in free)
        if t==2:
            over.append(j)
        assert t>=1
    return tuple(over)

def prefix_free_cover(certificates,cycles):
    certs=[tuple(x) for x in certificates]
    assert len(set(certs))==len(certs)
    prefix_free=all(not (len(a)<len(b) and b[:len(a)]==a)
                    for a in certs for b in certs)
    leaves=list(product(*cycles))
    covered=[leaf for leaf in leaves if any(leaf[:len(c)]==c for c in certs)]
    weight=sum(__import__("math").prod(len(cycles[i]) for i in range(len(c),len(cycles)))
               for c in certs)
    return dict(prefix_free=prefix_free,leaf_count=len(leaves),
                covered_count=len(covered),uncovered_count=len(leaves)-len(covered),
                cylinder_weight=weight,no_double_count=(weight==len(covered)))

def pair_extreme_control(F):
    checked=0;feasible=0
    for i,j in combinations(range(len(F)),2):
        ci,cj=F[i],F[j]
        for mi,mj in product(("S","U"),repeat=2):
            req={}
            ok=True
            for c,mode in ((ci,mi),(cj,mj)):
                for l in c:
                    val=int(l>0)
                    if mode=="U":
                        val^=1
                    v=abs(l)
                    if v in req and req[v]!=val:
                        ok=False
                    req[v]=val
            shared={abs(x) for x in ci}&{abs(x) for x in cj}
            same=any((next(x for x in ci if abs(x)==v)>0) ==
                     (next(x for x in cj if abs(x)==v)>0) for v in shared)
            opp=any((next(x for x in ci if abs(x)==v)>0) !=
                    (next(x for x in cj if abs(x)==v)>0) for v in shared)
            pred=(not opp) if mi==mj else (not same)
            assert ok==pred
            checked+=1;feasible+=ok
    return dict(checked=checked,feasible=feasible)

def physical_xor_controls(w=8,delay=257):
    # Build an index 1^w, read a delimiter, jump; jump atomically erases I.
    T=w+2;D=2*w
    binary=sum((i^(i+1)).bit_count() for i in range((1<<6)-1))
    gray=sum(((i^(i>>1))^((i+1)^((i+1)>>1))).bit_count()
             for i in range((1<<6)-1))
    return dict(index_width=w,index_steps=T,index_adjacent_delta=D,
                index_endpoint_delta=0,unqualified_T_ge_D=(T>=D),
                amortized_half_D_le_T=(D/2<=T),
                delay_steps=delay,delay_data_delta=0,
                restored_bit_adjacent_delta=2,restored_bit_endpoint_delta=0,
                binary_enumeration_adjacent_delta=binary,
                gray_enumeration_adjacent_delta=gray,
                enumeration_endpoint_delta=6,
                note="offline diagnostics; FLMV jump clears index tape atomically")

def main():
    assert grammar(F9) and grammar(F15)
    malformed=[
        F9+(F9[0],),
        (F9[0],),
        ((1,1,2),),
        ((1,-2,3),),
        tuple(c for c in F9 if c!=F9[0]),
        ((1,2),),
    ]
    assert all(not grammar(x) for x in malformed)
    certify_cycles(F9,F9_U,F9_CYCLES)
    certify_cycles(F15,F15_S,F15_CYCLES)
    g9=gate(F9,F9_U,F9_CYCLES);g15=gate(F15,F15_S,F15_CYCLES)
    assert g9["delta"]==g15["delta"]==0

    # F9 parity-only hole and exhaustive branch refutations.
    outside9=system(F9,F9_U,F9_CYCLES,())
    assert outside9["consistent"]
    f9_branches={str(ch):system(F9,F9_U,F9_CYCLES,(ch,))
                 for ch in F9_CYCLES[0]}
    assert all(not z["consistent"] for z in f9_branches.values())
    assert len(list(extensions(F9,F9_U)))==0
    assert len(list(extensions(F9,{})))==70

    # F15 proves the dependency-scope firewall with same-prefix SAT siblings.
    p10=system(F15,F15_S,F15_CYCLES,(10,))
    assert p10["consistent"]
    leaves15={(a,b):system(F15,F15_S,F15_CYCLES,(a,b))
              for a in F15_CYCLES[0] for b in F15_CYCLES[1]}
    assert not leaves15[(10,2)]["consistent"]
    assert leaves15[(10,3)]["consistent"] and leaves15[(10,14)]["consistent"]
    leak=leaves15[(10,2)]
    assert 1 in leak["proof_dependencies"] and set(leak["proof_dependencies"])!={0}
    sat_models=list(extensions(F15,F15_S))
    assert len(sat_models)==2
    actual=[]
    leaf_model_sets={}
    for a in sat_models:
        choices=tuple(actual_cycle_choice(F15,F15_S,cyc,a)[0] for cyc in F15_CYCLES)
        actual.append(choices)
    for ch in product(*F15_CYCLES):
        mods=affine_models(F15,F15_S,F15_CYCLES,ch)
        leaf_model_sets[ch]={tuple(a[v] for v in range(1,16)) for a in mods}
    union=set().union(*leaf_model_sets.values())
    total=sum(len(s) for s in leaf_model_sets.values())
    assert total==len(union)==2
    assert set(actual)=={(10,3),(10,14)}
    assert all(len(actual_cycle_choice(F15,F15_S,cyc,a))==1
               for a in sat_models for cyc in F15_CYCLES)

    cover9=prefix_free_cover([(3,),(4,),(10,)],F9_CYCLES)
    assert cover9["prefix_free"] and cover9["uncovered_count"]==0
    F9x2=F9+tuple(tuple((1 if l>0 else -1)*(abs(l)+9) for l in c) for c in F9)
    P9x2={**F9_U,**{v+9:b for v,b in F9_U.items()}}
    C9x2=(F9_CYCLES[0],tuple(j+12 for j in F9_CYCLES[0]))
    assert grammar(F9x2);certify_cycles(F9x2,P9x2,C9x2)
    cover9x2=prefix_free_cover([(3,),(4,),(10,)],C9x2)
    assert cover9x2["covered_count"]==9 and cover9x2["no_double_count"]
    for c in (3,4,10):
        assert not system(F9x2,P9x2,C9x2,(c,))["consistent"]

    cover15=prefix_free_cover([(1,),(11,),(10,2)],F15_CYCLES)
    assert cover15["uncovered_count"]==2
    same_source=dict(F9_root="SAT",F9_root_models=70,F9_cube="UNSAT",
                     F9_cube_models=0,F15_cube="SAT",F15_cube_models=2)
    result={
      "run":"PREFIX_SCOPE_REFEREE263",
      "status":"PROVED/EXACT restricted lemmas; COMPUTATIONAL exhaustive controls; P versus NP OPEN",
      "seed":None,"exhaustive":True,
      "grammar":{"valid_sources":2,"malformed_rejected":len(malformed)},
      "gates":{"F9":g9,"F15":g15},
      "same_source_labels":same_source,
      "F9_parity_hole":{"outside_cycle_consistent":outside9["consistent"],
         "outside_rows":outside9["rows"],"all_cycle_choices_inconsistent":True,
         "branches":f9_branches,"cover":cover9},
      "F15_dependency_scope":{"prefix_10_consistent":p10["consistent"],
         "failed_leaf":[10,2],"failed_leaf_proof_dependencies":leak["proof_dependencies"],
         "failed_leaf_proof_tags":leak["proof_tags"],
         "sat_sibling_leaves":[[10,3],[10,14]],
         "naive_promotion_to_prefix_10_is_unsound":True,
         "actual_unique_choices":[list(x) for x in actual],
         "affine_union_total":total,"affine_union_distinct":len(union),
         "unsat_prefix_cover":cover15},
      "double_F9_prefix_cover":cover9x2,
      "pair_extremes_F9":pair_extreme_control(F9),
      "physical_xor":physical_xor_controls(),
      "limitations":[
        "small exhaustive sources; no all-input polynomial SAT algorithm",
        "affine children are noncanonical; no hereditary target closure",
        "no arbitrary-A to Phi(A) contraction or numerical FLMV transport",
        "physical XOR traces are offline and representation/model dependent"
      ],
      "P_vs_NP":"OPEN"
    }
    out=Path(__file__).with_name("prefix_scope_referee263_raw.json")
    out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"run":result["run"],"F9":result["F9_parity_hole"],
                      "F15":result["F15_dependency_scope"],
                      "double_F9":cover9x2,"physical_xor":result["physical_xor"],
                      "raw":str(out)},indent=2))

if __name__=="__main__":
    main()
