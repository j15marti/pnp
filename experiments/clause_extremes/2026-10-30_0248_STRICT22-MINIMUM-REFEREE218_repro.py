#!/usr/bin/env python3
"""Clause-indexed extreme audit and strict-(2,2) minimum correction.

Dependency-free, deterministic, exhaustive only on explicitly bounded controls.
The SAT-2024 lower bound is imported as a cited KNOWN THEOREM; this program
independently checks only its 20-clause strict witness and the logical controls.
"""
from __future__ import annotations
import itertools, json, time, tracemalloc
from collections import Counter, defaultdict

SEED = 202610300248

W1 = [
 (-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
 (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
 (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
 (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)
]
SWAP6 = [tuple((-x if abs(x)==6 and j in (9,13) else x) for x in c)
         for j,c in enumerate(W1)]
STRICT8_SAT = [
 (4,5,1),(4,5,-1),(-4,6,2),(-4,6,-2),
 (-5,-6,3),(-5,-6,-3),(1,2,3),(-1,-2,-3)
]

def ell_false_at(var: int, bit: int) -> int:
    return var if bit == 0 else -var

def selector(sign: int, z0: int) -> list[tuple[int,...]]:
    out=[]
    for b in range(8):
        bits=((b>>2)&1,(b>>1)&1,b&1)
        z=z0+b
        out.append((sign,ell_false_at(2,bits[0]),z))
        out.append((-z,ell_false_at(3,bits[1]),ell_false_at(4,bits[2])))
    return out

G_PLUS = selector(1,5)
G_DOUBLE = G_PLUS + selector(-1,13)

def unit_block(lit: int, a: int, b: int):
    return [(lit,sa*a,sb*b) for sa in (1,-1) for sb in (1,-1)]

PADDED_UNIT_UNSAT = unit_block(1,2,3)+unit_block(-1,4,5)
HORN_SAT = [(-1,-2,3),(-3,-4,-5),(-1,-4,-6),(2,-3,-6)]

def parity_cnf(vars_, parity):
    out=[]
    for bits in itertools.product((0,1), repeat=len(vars_)):
        if sum(bits)%2 != parity:
            out.append(tuple(ell_false_at(v,b) for v,b in zip(vars_,bits)))
    return out

XOR_CONTRADICTION = parity_cnf((1,2,3),0)+parity_cnf((1,2,3),1)

def nvars(F): return max((abs(x) for c in F for x in c), default=0)

def lit_true(lit, mask):
    return ((mask>>(abs(lit)-1))&1) == (lit>0)

def truth_vector(c, mask): return tuple(int(lit_true(x,mask)) for x in c)
def status(F,mask):
    tv=[truth_vector(c,mask) for c in F]
    counts=[sum(v) for v in tv]
    return {"mask":mask,"truth_vectors":["".join(map(str,v)) for v in tv],
            "true_counts":counts,"N":[counts.count(i) for i in range(4)],
            "sat":all(counts)}

def local_targets(F):
    out=[]
    for j,c in enumerate(F):
        occ=[]
        for p,lit in enumerate(c):
            s=int(lit>0); u=1-s
            occ.append({"occurrence":f"x_{{{abs(lit)},{j}}}","position":p,
                        "variable":abs(lit),"sign":"+" if lit>0 else "-",
                        "S_all_literals_true":s,"invert_S_to_U":1-s,
                        "U_all_literals_false":u,"invert_U_to_S":1-u})
        out.append({"clause_index":j,"source_clause":list(c),"occurrences":occ})
    return out

def req(c, mode):
    # S: literal true; U: literal false
    return {abs(lit): int((lit>0) == (mode=="S")) for lit in c}

def combine_requirements(items):
    r={}; conflicts=[]
    for clause_index,c,mode in items:
        for v,val in req(c,mode).items():
            if v in r and r[v]!=val: conflicts.append(v)
            r[v]=val
    return (not conflicts),sorted(set(conflicts)),r

def pair_matrix(F):
    out=[]
    for j,k in itertools.combinations(range(len(F)),2):
        shared=sorted(set(map(abs,F[j]))&set(map(abs,F[k])))
        same=[];opp=[]
        for v in shared:
            sj=next(x>0 for x in F[j] if abs(x)==v)
            sk=next(x>0 for x in F[k] if abs(x)==v)
            (same if sj==sk else opp).append(v)
        modes={}
        for mode in ("SS","SU","US","UU"):
            ok,conf,r=combine_requirements(((j,F[j],mode[0]),(k,F[k],mode[1])))
            modes[mode]={"feasible":ok,"conflicting_variables":conf,
                         "witness_partial":{str(v):x for v,x in sorted(r.items())} if ok else None}
        out.append({"clause_indices":[j,k],"shared":shared,
                    "same_polarity":same,"opposite_polarity":opp,"modes":modes})
    return out

def triple_mode_audit(F):
    feasible=0; infeasible=0; examples=[]
    for js in itertools.combinations(range(len(F)),3):
        for mode in itertools.product("SU",repeat=3):
            ok,conf,r=combine_requirements(tuple((j,F[j],m) for j,m in zip(js,mode)))
            feasible += ok; infeasible += (not ok)
            if len(examples)<12:
                examples.append({"clauses":list(js),"mode":"".join(mode),"feasible":ok,
                                 "conflicts":conf,"partial":r if ok else None})
    return {"feasible":feasible,"infeasible":infeasible,"examples":examples}

def flip_trails(F):
    n=nvars(F); out=[]
    for start in (0,(1<<n)-1):
        mask=start; trail=[]
        picks=list(range(min(n,6)))
        for step,v in enumerate(picks):
            before=status(F,mask); mask ^= 1<<v; after=status(F,mask)
            # exact source-indexed update check
            predicted=[]
            for j,c in enumerate(F):
                old=before["true_counts"][j]
                delta=sum(1 for x in c if abs(x)==v+1 and not lit_true(x,start if step==0 else (mask^(1<<v))))
                delta-=sum(1 for x in c if abs(x)==v+1 and lit_true(x,start if step==0 else (mask^(1<<v))))
                predicted.append(old+delta)
            assert predicted==after["true_counts"]
            trail.append({"flip_variable":v+1,"before_mask":before["mask"],"after":after})
        out.append({"start":start,"trail":trail})
    return out

def resolvents(F):
    out=[]; seen=set()
    for j,k in itertools.combinations(range(len(F)),2):
        for p in F[j]:
            if -p not in F[k]: continue
            tail=list(F[j]);tail.remove(p)
            tail2=list(F[k]);tail2.remove(-p)
            R=tuple(sorted(set(tail+tail2),key=lambda x:(abs(x),x)))
            taut=any(-x in R for x in R)
            if taut: continue
            key=(j,k,p,R)
            if key in seen: continue
            seen.add(key)
            cube={str(abs(x)):int(x<0) for x in R} # falsify literal
            out.append({"parents":[j,k],"pivot":abs(p),"pivot_sign_in_first":int(p>0),
                        "resolvent":list(R),"forbidden_cube":cube,
                        "proof":"parents reduce to opposite pivot units when cube is pinned"})
    return out

def validate(F):
    n=nvars(F); deg=defaultdict(lambda:[0,0])
    proper=all(len(c)==3 and len(set(map(abs,c)))==3 for c in F)
    for c in F:
        for x in c: deg[abs(x)][int(x>0)]+=1
    # connected primal graph
    adj={i:set() for i in range(1,n+1)}
    for c in F:
        for a,b in itertools.combinations(map(abs,c),2):adj[a].add(b);adj[b].add(a)
    seen=set(); stack=[1] if n else []
    while stack:
        v=stack.pop()
        if v in seen: continue
        seen.add(v);stack.extend(adj[v]-seen)
    unique=len(set(map(tuple,F)))==len(F)
    return {"n":n,"m":len(F),"proper":proper,"unique_clauses":unique,"connected":len(seen)==n,
            "degrees":{str(v):{"negative":deg[v][0],"positive":deg[v][1]} for v in range(1,n+1)},
            "strict22":proper and unique and all(deg[v]==[2,2] for v in range(1,n+1))}

def count_models(F,cap_n=15):
    n=nvars(F); assert n<=cap_n
    models=[]
    for a in range(1<<n):
        if all(any(lit_true(x,a) for x in c) for c in F): models.append(a)
    return models

class DPLL:
    def __init__(self,F): self.F=[tuple(c) for c in F];self.w=Counter()
    def solve(self):
        n=nvars(self.F); ans=self._go({})
        if ans is not None:
            for v in range(1,n+1):ans.setdefault(v,False)
        return ans,dict(self.w)
    def _go(self,a):
        self.w['nodes']+=1
        while True:
            changed=False
            for j,c in enumerate(self.F):
                self.w['clause_reads']+=1
                sat=False; free=[]
                for x in c:
                    self.w['literal_reads']+=1;v=abs(x)
                    if v in a:
                        if a[v]==(x>0):sat=True;break
                    else:free.append(x)
                if sat:continue
                if not free:
                    self.w['conflict_leaves']+=1;return None
                if len(free)==1:
                    x=free[0];v=abs(x);val=x>0
                    if v in a and a[v]!=val:
                        self.w['conflict_leaves']+=1;return None
                    if v not in a:a[v]=val;self.w['unit_props']+=1;changed=True
            if not changed:break
        if all(any((abs(x) in a and a[abs(x)]==(x>0)) for x in c) for c in self.F):return a
        n=nvars(self.F);v=next(v for v in range(1,n+1) if v not in a)
        self.w['branches']+=1
        for val in (False,True):
            b=dict(a);b[v]=val;r=self._go(b)
            if r is not None:return r
        return None

def diagnostic_cost(F,audit):
    # Explicit selected-event ledger, not machine instructions.
    return (sum(len(c)*4 for c in F) + len(audit['pair_matrix'])*4 +
            sum(len(c) for c in F)*2 + sum(len(t['trail'])*len(F) for t in audit['flip_trails']) +
            sum(len(r['resolvent'])+2 for r in audit['resolvents']))

def audit_formula(name,F,enumerate_models=True):
    t0=time.perf_counter();tracemalloc.start()
    local=local_targets(F);pm=pair_matrix(F);tm=triple_mode_audit(F)
    n=nvars(F); endpoints={"zero":status(F,0),"one":status(F,(1<<n)-1)}
    comp=[]
    for a in [0,(1<<n)-1]+[1<<i for i in range(min(n,5))]:
        s=status(F,a);q=status(F,((1<<n)-1)^a)
        assert all(q['true_counts'][j]==3-s['true_counts'][j] for j in range(len(F)))
        comp.append({"a":a,"complement":q["mask"],"N_a":s['N'],"N_complement":q['N']})
    trails=flip_trails(F);res=resolvents(F)
    solver=DPLL(F);model,work=solver.solve()
    models=count_models(F) if enumerate_models else None
    if models is not None: assert (model is not None)==bool(models)
    peak=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
    obj={"name":name,"source_clauses":[list(c) for c in F],"validation":validate(F),
         "local_targets":local,"pair_matrix":pm,"triple_extreme_audit":tm,
         "global_endpoints":endpoints,"complements":comp,"flip_trails":trails,
         "resolvents":res,"exact_model_count":None if models is None else len(models),
         "first_model":None if not models else models[0],"dpll":work,
         "elapsed_seconds":time.perf_counter()-t0,"python_peak_bytes":peak}
    obj['diagnostic_selected_events']=diagnostic_cost(F,obj)
    obj['diagnostics_plus_dpll_selected_events']=obj['diagnostic_selected_events']+sum(work.values())
    return obj

def selector_proof():
    # Machine-check the 15-step projected resolution DAG on the positive module.
    cur=[];steps=[]
    for b in range(8):
        A=G_PLUS[2*b];B=G_PLUS[2*b+1];z=5+b
        R=tuple(x for x in A if x!=z)+tuple(x for x in B if x!=-z)
        R=tuple(dict.fromkeys(R));cur.append(R);steps.append({"pivot":z,"parents":[list(A),list(B)],"resolvent":list(R)})
    for var in (4,3,2):
        nxt=[]
        used=[False]*len(cur)
        for i,C in enumerate(cur):
            if used[i]:continue
            mate=next(j for j,D in enumerate(cur) if j!=i and not used[j] and var in map(abs,C) and
                      var in map(abs,D) and ((var in C) != (var in D)) and set(map(abs,C))==set(map(abs,D)))
            D=cur[mate];used[i]=used[mate]=True
            R=tuple(x for x in C if abs(x)!=var)+tuple(x for x in D if abs(x)!=var)
            R=tuple(dict.fromkeys(R));nxt.append(R);steps.append({"pivot":var,"parents":[list(C),list(D)],"resolvent":list(R)})
        cur=nxt
    assert cur==[(1,)] and len(steps)==15
    # Every deletion admits s=0 and the missing pattern's x-values.
    deletion=[]
    for miss in range(8):
        bits=((miss>>2)&1,(miss>>1)&1,miss&1);base=(bits[0]<<1)|(bits[1]<<2)|(bits[2]<<3)
        found=None
        H=[c for b in range(8) if b!=miss for c in G_PLUS[2*b:2*b+2]]
        for zmask in range(1<<8):
            a=base|(zmask<<4)
            if all(any(lit_true(x,a) for x in c) for c in H):found=a;break
        assert found is not None; deletion.append({"missing_pattern":miss,"witness_mask":found})
    return {"steps":steps,"deletion_witnesses":deletion}

def main():
    t0=time.perf_counter()
    cases=[
      ("W1_strict22_UNSAT",W1,True),("SWAP6_strict22_SAT",SWAP6,True),
      ("STRICT8_SAT",STRICT8_SAT,True),("SELECTOR_G_PLUS",G_PLUS,True),
      ("SELECTOR_DOUBLE_UNSAT",G_DOUBLE,False),("PADDED_UNIT_2SAT_UNSAT",PADDED_UNIT_UNSAT,True),
      ("HORN_SAT",HORN_SAT,True),("XOR_CONTRADICTION",XOR_CONTRADICTION,True)]
    audits=[]
    for args in cases:audits.append(audit_formula(*args))
    # Required strict witness checks.
    w=audits[0];v=audits[1]
    assert w['validation']['strict22'] and w['validation']['connected'] and w['exact_model_count']==0
    assert v['validation']['strict22'] and v['validation']['connected'] and v['exact_model_count']==54
    assert len(W1)==20 and 3*len(W1)==4*nvars(W1)
    proof=selector_proof()
    out={
      "run_id":"STRICT22-MINIMUM-REFEREE218","timestamp":"2026-10-30T02:48:00-07:00",
      "seed":SEED,
      "epistemic_status":{
        "mu_3_2_2_equals_20":"KNOWN THEOREM: Zhang-Peitl-Szeider SAT 2024 Table 1 and Theorem 15 plus 20-clause construction",
        "strict_exact22_minimum_equals_20":"PROVED/EXACT corollary using the independently checked W1 witness",
        "finite_audits":"COMPUTATIONAL exhaustive on declared bounded controls",
        "general_SAT":"OPEN"},
      "strict_minimum_proof_ledger":{
        "lower":"Every strict exact22 source is a (3,2,2)-formula; known mu(3,2,2)=20",
        "upper":"W1 is connected, proper, strict exact22, has 20 clauses, and exhaustive enumeration plus DPLL find zero models",
        "conclusion":"minimum number of clauses in an UNSAT strict exact22 source is exactly 20"},
      "selector_resolution_proof":proof,
      "cases":audits,
      "total_elapsed_seconds":time.perf_counter()-t0,
      "limitations":["The SAT-2024 global lower bound is not reproved by this finite program.",
        "Selected-event counts are not native TM/RAM instructions.",
        "No arbitrary-SAT shortcut or lower bound follows; P versus NP remains OPEN."]}
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=="__main__":main()
