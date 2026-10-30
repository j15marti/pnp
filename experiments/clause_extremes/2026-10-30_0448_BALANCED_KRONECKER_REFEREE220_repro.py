#!/usr/bin/env python3
"""BALANCED-KRONECKER-REFEREE220.

Independent clause-extreme audit and exact bounded Kronecker packing control.
The counters describe this Python implementation, not a RAM/TM/CDCL lower bound.
"""
from __future__ import annotations
import itertools, json, math, random, time, tracemalloc
from collections import Counter, defaultdict

RUN="BALANCED-KRONECKER-REFEREE220"
SEED=202610300448

W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
    (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
    (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
    (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
SWAP6=[tuple((-x if abs(x)==6 and j in (9,13) else x) for x in c)
       for j,c in enumerate(W1)]
STRICT8=[(4,5,1),(4,5,-1),(-4,6,2),(-4,6,-2),
         (-5,-6,3),(-5,-6,-3),(1,2,3),(-1,-2,-3)]
HORN=[(-1,-2,3),(-3,-4,-5),(-1,-4,-6),(2,-3,-6)]

def false_lit(v,b): return v if b==0 else -v
def parity_cnf(vs,p):
    return [tuple(false_lit(v,b) for v,b in zip(vs,bits))
            for bits in itertools.product((0,1),repeat=len(vs))
            if sum(bits)%2 != p]
XOR_UNSAT=parity_cnf((1,2,3),0)+parity_cnf((1,2,3),1)
def pad2(c,z): return [tuple(c)+(z,),tuple(c)+(-z,)]
PADDED=[]
for c in ((1,2),(1,-2),(-1,2),(-1,-2)): PADDED+=pad2(c,3)
DUP=[(1,2,3),(1,2,-3),(-1,2,3)]*3
def planted_dense():
    rng=random.Random(SEED); n=10; planted=0b1011010011; out=[]; seen=set()
    while len(out)<36:
        vs=tuple(sorted(rng.sample(range(1,n+1),3)))
        c=tuple(rng.choice((-1,1))*v for v in vs)
        if c in seen or not any((((planted>>(abs(x)-1))&1)==1)==(x>0) for x in c): continue
        seen.add(c);out.append(c)
    return out
DENSE=planted_dense()
RENAMED=[tuple(-x if abs(x) in {1,4,9} else x for x in c) for c in W1]
CASES=[("W1_strict22_UNSAT",W1),("SWAP6_strict22_SAT",SWAP6),
       ("STRICT8_exact22_SAT",STRICT8),("HORN_SAT",HORN),
       ("XOR_affine_UNSAT",XOR_UNSAT),("PADDED_2SAT_UNSAT",PADDED),
       ("DUPLICATE_SUPPORT_SAT",DUP),("DENSE_PLANTED_SAT",DENSE),
       ("POLARITY_RENAMED_W1_UNSAT",RENAMED)]

def nvars(F): return max(abs(l) for c in F for l in c)
def ltrue(l,a): return (((a>>(abs(l)-1))&1)==1)==(l>0)
def nvec(F,a):
    t=[sum(ltrue(l,a) for l in c) for c in F]
    return tuple(t.count(r) for r in range(4)),t
def sat(F,a): return all(any(ltrue(l,a) for l in c) for c in F)
def status(F,a):
    N,t=nvec(F,a)
    return {"assignment_mask":a,"bitstring":"".join(str((a>>i)&1) for i in range(nvars(F))),
            "per_original_clause_true_literal_counts":t,"N0_N1_N2_N3":list(N),
            "formula_SAT":N[0]==0}

def local_targets(F):
    out=[]
    for j,c in enumerate(F):
        occ=[]
        for p,l in enumerate(c):
            S=int(l>0);U=1-S
            occ.append({"occurrence":f"x_{{{abs(l)},{j}}}","position":p,
              "literal":l,"sign":"+" if l>0 else "-","variable":abs(l),
              "S_local_all_literals_true":S,"invert_S_is_U":1-S,
              "U_local_all_literals_false":U,"invert_U_is_S":1-U})
        out.append({"clause_index":j,"original_clause":list(c),"occurrences":occ})
    return out

def req(c,mode): return {abs(l):int((l>0)==(mode=="S")) for l in c}
def combine(F,js,modes):
    a={};bad=set()
    for j,mode in zip(js,modes):
        for v,z in req(F[j],mode).items():
            if v in a and a[v]!=z: bad.add(v)
            a[v]=z
    return not bad,sorted(bad),a
def pair_matrix(F):
    out=[]
    for j,k in itertools.combinations(range(len(F)),2):
        shared=sorted(set(map(abs,F[j]))&set(map(abs,F[k])))
        same=[];opp=[]
        for v in shared:
            s1=next(l>0 for l in F[j] if abs(l)==v)
            s2=next(l>0 for l in F[k] if abs(l)==v)
            (same if s1==s2 else opp).append(v)
        modes={}
        for md in ("SS","SU","US","UU"):
            ok,bad,a=combine(F,(j,k),md)
            # independent brute force over union support
            vs=sorted(set(map(abs,F[j]))|set(map(abs,F[k])))
            brute=False;wit=None
            for bits in itertools.product((0,1),repeat=len(vs)):
                z=dict(zip(vs,bits))
                tj=[sum(z[abs(l)]==int(l>0) for l in F[q]) for q in (j,k)]
                if tj[0]==(3 if md[0]=='S' else 0) and tj[1]==(3 if md[1]=='S' else 0):
                    brute=True;wit=z;break
            assert brute==ok
            modes[md]={"feasible":ok,"conflicting_variables":bad,
                       "witness_partial":({str(v):z for v,z in wit.items()} if wit else None)}
        out.append({"clause_indices":[j,k],"same_polarity_shared":same,
                    "opposite_polarity_shared":opp,"modes":modes})
    return out
def triple_counts(F):
    yes=no=0;examples=[]
    for js in itertools.combinations(range(len(F)),3):
        for modes in itertools.product("SU",repeat=3):
            ok,bad,a=combine(F,js,modes);yes+=ok;no+=not ok
            if len(examples)<12: examples.append({"clauses":list(js),"mode":"".join(modes),"feasible":ok,"conflicts":bad})
    return {"feasible":yes,"infeasible":no,"examples":examples}
def flip_trails(F):
    n=nvars(F);ans=[]
    for start in (0,(1<<n)-1):
        a=start;trail=[status(F,a)]
        for v in range(1,min(n,6)+1):
            before=status(F,a);a^=1<<(v-1);after=status(F,a)
            predicted=[]
            for j,c in enumerate(F):
                d=sum(1 if not ltrue(l,before['assignment_mask']) else -1 for l in c if abs(l)==v)
                predicted.append(before['per_original_clause_true_literal_counts'][j]+d)
            assert predicted==after['per_original_clause_true_literal_counts']
            trail.append({"flipped_original_variable":v,"state":after})
        ans.append({"start":"0^n" if start==0 else "1^n","trail":trail})
    return ans
def resolvents(F,limit=48):
    out=[];n=nvars(F)
    for j,k in itertools.combinations(range(len(F)),2):
        for p in F[j]:
            if -p not in F[k]: continue
            R=tuple(sorted((set(F[j])-{p})|(set(F[k])-{-p}),key=lambda x:(abs(x),x)))
            if any(-x in R for x in R): continue
            cube={abs(x):int(x<0) for x in R};checked=excluded=0
            for a in range(1<<n):
                if all(((a>>(v-1))&1)==z for v,z in cube.items()):
                    checked+=1
                    if not (all(any(ltrue(l,a) for l in F[q]) for q in (j,k))): excluded+=1
            assert excluded==checked
            out.append({"parent_clause_indices":[j,k],"pivot":abs(p),"resolvent":list(R),
                        "prohibited_partial_cube":{str(v):z for v,z in cube.items()},
                        "checked_cube_completions":checked,"all_excluded_by_parent_pair":True,
                        "proof":"falsifying R leaves opposite pivot units in its two source parents"})
            if len(out)>=limit:return out
    return out

def sign_balanced_ternary(F):
    if any(len(c)!=3 or len(set(map(abs,c)))!=3 for c in F): return False
    d=defaultdict(lambda:[0,0])
    for c in F:
        for l in c:d[abs(l)][int(l>0)]+=1
    return all(a==b for a,b in d.values())

def profile_audit(F):
    n=nvars(F);hist=Counter();models=0;literal_evals=0
    for a in range(1<<n):
        N,_=nvec(F,a);hist[N]+=1;models+=N[0]==0;literal_evals+=sum(map(len,F))
    comp_ok=all(hist[N]==hist[(N[3],N[2],N[1],N[0])] for N in hist)
    out={"assignments":1<<n,"literal_evaluations":literal_evals,"models":models,
         "four_coordinate_support":[{"N":list(N),"coefficient":z} for N,z in sorted(hist.items())],
         "support_size_4D":len(hist),"complement_coefficient_symmetry":comp_ok}
    pairs=Counter()
    for N,z in hist.items():pairs[(N[0],N[3])]+=z
    out["two_coordinate_support"]=[{"N0_N3":list(q),"coefficient":z} for q,z in sorted(pairs.items())]
    out["support_size_2D"]=len(pairs)
    if sign_balanced_ternary(F):
        m=len(F);assert m%2==0;h=m//2;M=h+1
        for N in hist:
            n0,n1,n2,n3=N
            assert n1==h-2*n0+n3 and n2==h+n0-2*n3
            assert 0<=n0<=h and 0<=n3<=h
        packed={n0+M*n3:(n0,n3) for n0,n3 in pairs}
        assert len(packed)==len(pairs)
        for key,(n0,n3) in packed.items(): assert (key%M,key//M)==(n0,n3)
        # Delta packing for Laurent exponents: differences lie in [-h,h]^2.
        anchor=nvec(F,0)[0];deltas={(N[0]-anchor[0],N[3]-anchor[3]) for N in hist}
        Md=2*h+1
        dpacked={a+Md*b:(a,b) for a,b in deltas};assert len(dpacked)==len(deltas)
        feasible={(a,b) for a in range(h+1) for b in range(h+1)
                  if 2*a-b<=h and 2*b-a<=h}
        formula=math.floor(h*h/2+h+1)
        assert len(feasible)==formula
        # Find an observed nonzero determinant witness when present.
        witness=None
        for u,v in itertools.combinations(sorted(deltas),2):
            if u[0]*v[1]-u[1]*v[0]:witness=[list(u),list(v)];break
        out["balanced_exact"]={
          "h_m_over_2":h,"identities":"N1=h-2N0+N3; N2=h+N0-2N3",
          "algebraically_permitted_profile_count":len(feasible),
          "closed_form":"floor(h^2/2+h+1)","observed_profile_count":len(hist),
          "absolute_Kronecker_base":M,"absolute_packed_support_size":len(packed),
          "delta_Kronecker_base":Md,"delta_packed_support_size":len(dpacked),
          "delta_2D_support_size":len(deltas),"observed_rank_two_witness":witness,
          "support_preserved_4D_2D_1D":len(hist)==len(pairs)==len(packed),
          "one_scalar_decode":"N0=key mod (h+1), N3=floor(key/(h+1)); reconstruct N1,N2 by identities"}
    return out

def up(F,A,ledger):
    A=dict(A)
    while True:
        changed=False
        for c in F:
            ledger['clause_scans']+=1
            if any(abs(l) in A and A[abs(l)]==int(l>0) for l in c):continue
            U=[]
            for l in c:
                ledger['literal_scans']+=1
                if abs(l) not in A:U.append(l)
            if not U:return None
            if len(U)==1:
                l=U[0];v=abs(l);z=int(l>0)
                if v in A and A[v]!=z:return None
                if v not in A:A[v]=z;ledger['unit_assignments']+=1;changed=True
        if not changed:return A
def dpll(F,measure=True):
    L=Counter(nodes=0,branches=0,clause_scans=0,literal_scans=0,unit_assignments=0)
    n=nvars(F)
    def rec(A):
        L['nodes']+=1;B=up(F,A,L)
        if B is None:return None
        if len(B)==n:return B
        v=next(x for x in range(1,n+1) if x not in B)
        for z in (0,1):
            L['branches']+=1;C=rec({**B,v:z})
            if C is not None:return C
        return None
    t=time.perf_counter()
    if measure: tracemalloc.start()
    ans=rec({})
    if measure:
        _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    else: peak=None
    elapsed=time.perf_counter()-t
    if ans is not None: assert sat(F,sum(z<<(v-1) for v,z in ans.items()))
    L['selected_events']=sum(L.values())
    return {"sat":ans is not None,"nodes":L['nodes'],"events":dict(L),"seconds":elapsed,"peak_bytes":peak}
def controller(F):
    t=time.perf_counter();tracemalloc.start();P=profile_audit(F);B=dpll(F,False);_,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    return {"sat":B['sat'],"nodes":B['nodes'],"prepass_literal_evaluations":P['literal_evaluations'],
            "backend_selected_events":B['events']['selected_events'],
            "selected_events":P['literal_evaluations']+B['events']['selected_events'],
            "seconds":time.perf_counter()-t,"peak_bytes":peak}

def audit(name,F):
    t=time.perf_counter();P=pair_matrix(F);Prof=profile_audit(F)
    base=dpll(F);ctrl=controller(F);assert base['sat']==ctrl['sat']==(Prof['models']>0)
    return {"name":name,"n":nvars(F),"m":len(F),"source_formula":[list(c) for c in F],
      "proper":all(len(c)==len(set(c))==len(set(map(abs,c))) for c in F),
      "sign_balanced_ternary":sign_balanced_ternary(F),"local_clause_targets":local_targets(F),
      "pair_extreme_compatibility":P,"triple_extreme_summary":triple_counts(F),
      "global_endpoints":{"0^n":status(F,0),"1^n":status(F,(1<<nvars(F))-1)},
      "intermediate_flip_trails":flip_trails(F),"source_resolvent_prohibited_cubes":resolvents(F),
      "profile_audit":Prof,"baseline_UP_DPLL":base,"profile_prepass_then_same_UP_DPLL":ctrl,
      "audit_seconds":time.perf_counter()-t}

def main():
    started=time.perf_counter();cases=[audit(name,F) for name,F in CASES]
    balanced=[c for c in cases if c['sign_balanced_ternary']]
    out={"run_id":RUN,"timestamp":"2026-10-30T04:48:00-07:00","seed":SEED,
      "claims":{
       "corrected":"Two Laurent generators are minimal only for an unbounded fixed-weight lattice-homomorphic representation; bounded exact spectra admit collision-free one-exponent Kronecker packing.",
       "support_firewall":"Collision-free packing preserves nonzero support cardinality and sparse coefficient-pair work; it changes key representation, not the number of states.",
       "status":"restricted exact theorem plus computational controls; no P versus NP implication"},
      "balanced_cases":[c['name'] for c in balanced],"cases":cases,
      "summary":{"cases":len(cases),"balanced_cases":len(balanced),
        "total_assignments":sum(c['profile_audit']['assignments'] for c in cases),
        "total_pair_modes":sum(4*len(c['pair_extreme_compatibility']) for c in cases),
        "total_resolvent_cube_completions":sum(sum(r['checked_cube_completions'] for r in c['source_resolvent_prohibited_cubes']) for c in cases),
        "all_controllers_same_answer":all(c['baseline_UP_DPLL']['sat']==c['profile_prepass_then_same_UP_DPLL']['sat'] for c in cases),
        "all_balanced_support_preserved":all(c['profile_audit']['balanced_exact']['support_preserved_4D_2D_1D'] for c in balanced)},
      "elapsed_seconds":time.perf_counter()-started}
    with open("2026-10-30_0448_BALANCED_KRONECKER_REFEREE220_raw.json","w") as f:json.dump(out,f,indent=2,sort_keys=True)
    summary={"run_id":RUN,"summary":out['summary'],"elapsed_seconds":out['elapsed_seconds'],
      "cases":[{"name":c['name'],"models":c['profile_audit']['models'],
        "support4":c['profile_audit']['support_size_4D'],"support2":c['profile_audit']['support_size_2D'],
        "balanced":c['sign_balanced_ternary'],"balanced_exact":c['profile_audit'].get('balanced_exact'),
        "base_events":c['baseline_UP_DPLL']['events']['selected_events'],
        "ctrl_events":c['profile_prepass_then_same_UP_DPLL']['selected_events'],
        "base_seconds":c['baseline_UP_DPLL']['seconds'],"ctrl_seconds":c['profile_prepass_then_same_UP_DPLL']['seconds'],
        "base_peak":c['baseline_UP_DPLL']['peak_bytes'],"ctrl_peak":c['profile_prepass_then_same_UP_DPLL']['peak_bytes']} for c in cases]}
    with open("2026-10-30_0448_BALANCED_KRONECKER_REFEREE220_summary.json","w") as f:json.dump(summary,f,indent=2,sort_keys=True)
    print(json.dumps(summary,indent=2,sort_keys=True))
if __name__=="__main__":main()
