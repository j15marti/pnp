#!/usr/bin/env python3
"""Source-extreme audit plus a width-3 RUP certificate for SWAP6 |= x2.

Dependency-free and deterministic.  Every named invocation is finite and is
intended to finish well below 30 seconds.  Logical-event counters are Python
instrumentation, not TM or industrial-CDCL timings.
"""
from __future__ import annotations
import itertools, json, math, random, sys, time, tracemalloc
from collections import Counter, defaultdict, deque

SEED = 202610300348

W1 = [
 (-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
 (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
 (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
 (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)
]
SWAP6 = [tuple((-x if abs(x)==6 and j in (9,13) else x) for x in c)
         for j,c in enumerate(W1)]
STRICT8 = [(4,5,1),(4,5,-1),(-4,6,2),(-4,6,-2),
           (-5,-6,3),(-5,-6,-3),(1,2,3),(-1,-2,-3)]
HORN = [(-1,-2,3),(-3,-4,-5),(-1,-4,-6),(2,-3,-6)]

def ell_false_at(v,b): return v if b==0 else -v
def parity_cnf(vs,p):
    return [tuple(ell_false_at(v,b) for v,b in zip(vs,bits))
            for bits in itertools.product((0,1),repeat=len(vs))
            if sum(bits)%2 != p]
XOR_UNSAT = parity_cnf((1,2,3),0)+parity_cnf((1,2,3),1)

def pad2(c,z): return [tuple(c)+(z,),tuple(c)+(-z,)]
PADDED_2SAT_UNSAT=[]
for c in ((1,2),(1,-2),(-1,2),(-1,-2)):
    PADDED_2SAT_UNSAT += pad2(c,3)
DUP_SUPPORT = [(1,2,3),(1,2,-3),(-1,2,3)]*3

def planted_dense():
    rng=random.Random(SEED); n=10; planted=0b1011010011; out=[]; seen=set()
    while len(out)<36:
        vs=tuple(sorted(rng.sample(range(1,n+1),3)))
        signs=tuple(rng.choice((-1,1))*v for v in vs)
        if signs in seen: continue
        if not any((((planted>>(abs(x)-1))&1)==1)==(x>0) for x in signs): continue
        seen.add(signs); out.append(signs)
    return out
DENSE_SAT=planted_dense()
RENAMED_W1=[tuple(-x if abs(x) in {1,4,9} else x for x in c) for c in W1]

CASES=[
 ("W1_strict22_UNSAT",W1), ("SWAP6_strict22_SAT",SWAP6),
 ("STRICT8_exact22_SAT",STRICT8), ("HORN_SAT",HORN),
 ("XOR_affine_UNSAT",XOR_UNSAT), ("PADDED_2SAT_UNSAT",PADDED_2SAT_UNSAT),
 ("DUPLICATE_SUPPORT_SAT",DUP_SUPPORT), ("DENSE_PLANTED_SAT",DENSE_SAT),
 ("POLARITY_RENAMED_W1_UNSAT",RENAMED_W1)]

def ckey(c): return tuple(sorted(set(c),key=lambda x:(abs(x),x)))
def nvars(F): return max((abs(x) for c in F for x in c),default=0)
def ltrue(lit,mask): return (((mask>>(abs(lit)-1))&1)==1)==(lit>0)
def is_sat_mask(F,mask):
    return all(any(ltrue(l,mask) for l in c) for c in F)
def counts_only(F,mask):
    return [sum(ltrue(l,mask) for l in c) for c in F]
def status(F,mask):
    tv=[tuple(int(ltrue(x,mask)) for x in c) for c in F]
    cnt=[sum(x) for x in tv]
    return {"mask":mask,"truth_vectors":["".join(map(str,x)) for x in tv],
            "true_counts":cnt,"N":[cnt.count(i) for i in range(4)],
            "sat":all(x>=1 for x in cnt)}
def model_masks(F):
    return [a for a in range(1<<nvars(F)) if is_sat_mask(F,a)]

def local_targets(F):
    ans=[]
    for j,c in enumerate(F):
        occ=[]
        for p,l in enumerate(c):
            s=int(l>0); u=1-s
            occ.append({"occurrence":f"x_{{{abs(l)},{j}}}","position":p,
                        "variable":abs(l),"sign":"+" if l>0 else "-",
                        "S_local_all_literals_true":s,"invert_S_to_U":1-s,
                        "U_local_all_literals_false":u,"invert_U_to_S":1-u})
        ans.append({"clause_index":j,"source_clause":list(c),"occurrences":occ})
    return ans

def req(c,mode):
    return {abs(l):int((l>0)==(mode=="S")) for l in c}
def combine(items):
    r={}; bad=set()
    for _,c,m in items:
        for v,z in req(c,m).items():
            if v in r and r[v]!=z: bad.add(v)
            r[v]=z
    return not bad,sorted(bad),r
def pair_matrix(F):
    out=[]
    for j,k in itertools.combinations(range(len(F)),2):
        sh=sorted(set(map(abs,F[j]))&set(map(abs,F[k]))); same=[]; opp=[]
        for v in sh:
            a=next(l>0 for l in F[j] if abs(l)==v)
            b=next(l>0 for l in F[k] if abs(l)==v)
            (same if a==b else opp).append(v)
        modes={}
        for m in ("SS","SU","US","UU"):
            ok,bad,r=combine(((j,F[j],m[0]),(k,F[k],m[1])))
            modes[m]={"feasible":ok,"conflicting_variables":bad,
                      "witness_partial":({str(v):z for v,z in r.items()} if ok else None)}
        out.append({"clause_indices":[j,k],"shared":sh,
                    "same_polarity":same,"opposite_polarity":opp,"modes":modes})
    return out
def pair_hist(P):
    return dict(Counter("".join(m for m in ("SS","SU","US","UU")
                                if d["modes"][m]["feasible"]) for d in P))
def triple_summary(F):
    yes=no=0; ex=[]
    for js in itertools.combinations(range(len(F)),3):
        for ms in itertools.product("SU",repeat=3):
            ok,bad,r=combine(tuple((j,F[j],m) for j,m in zip(js,ms)))
            yes+=ok; no+=not ok
            if len(ex)<12: ex.append({"clauses":list(js),"mode":"".join(ms),
                                      "feasible":ok,"conflicts":bad,
                                      "partial":r if ok else None})
    return {"feasible":yes,"infeasible":no,"examples":ex}

def flip_trails(F):
    n=nvars(F); out=[]
    for start in (0,(1<<n)-1):
        a=start; trail=[]
        for v in range(1,min(n,6)+1):
            before=status(F,a); b=a^(1<<(v-1)); after=status(F,b)
            pred=[]
            for j,c in enumerate(F):
                delta=sum(1 if not ltrue(l,a) else -1 for l in c if abs(l)==v)
                pred.append(before["true_counts"][j]+delta)
            assert pred==after["true_counts"]
            trail.append({"flip_variable":v,"before":before,"after":after})
            a=b
        out.append({"start":start,"trail":trail})
    return out

def resolvents(F,limit=40):
    out=[]
    for j,k in itertools.combinations(range(len(F)),2):
        for p in F[j]:
            if -p not in F[k]: continue
            R=ckey((set(F[j])-{p})|(set(F[k])-{-p}))
            if any(-x in R for x in R): continue
            cube={str(abs(x)):int(x<0) for x in R}
            out.append({"parents":[j,k],"pivot":abs(p),"resolvent":list(R),
                        "forbidden_cube":cube,
                        "proof":"falsifying the resolvent reduces the parents to opposite pivot units"})
            if len(out)>=limit:return out
    return out

def relation_code(F):
    occ=defaultdict(list)
    for j,c in enumerate(F):
        for p,l in enumerate(c): occ[abs(l)].append((j,p,int(l>0)))
    code={}; refsign={}
    for v,os in sorted(occ.items()):
        os=sorted(os); ref=os[0]; refsign[v]=ref[2]
        code[v]={"reference":[ref[0],ref[1]],
                 "relations":[{"occurrence":[j,p],"opposite_to_reference":s^ref[2]}
                              for j,p,s in os[1:]]}
    return code,refsign
def reconstruct_canonical(F,code):
    out=[list(c) for c in F]
    for v,d in code.items():
        j,p=d["reference"]; out[j][p]=v
        for z in d["relations"]:
            j,p=z["occurrence"]; out[j][p]=-v if z["opposite_to_reference"] else v
    return [tuple(c) for c in out]
def flip_formula(F,V): return [tuple(-l if abs(l) in V else l for l in c) for c in F]

def abstract_exact22_codes(n):
    pats=list(itertools.combinations(range(4),2)); seen=set()
    for choice in itertools.product(pats,repeat=n):
        canon=[]
        for P in choice:
            bits=tuple(int(i in P) for i in range(4)); comp=tuple(1-x for x in bits)
            canon.append(min(bits,comp))
        seen.add(tuple(canon))
    return len(seen)

def unit_propagate(F,assignment,ledger=None):
    a=dict(assignment)
    while True:
        changed=False
        for c in F:
            if ledger is not None: ledger["clause_scans"]+=1
            sat=False; un=[]
            for l in c:
                if ledger is not None: ledger["literal_scans"]+=1
                v=abs(l)
                if v in a:
                    if a[v]==int(l>0): sat=True; break
                else: un.append(l)
            if sat: continue
            if not un: return None
            if len(un)==1:
                l=un[0]; v=abs(l); z=int(l>0)
                if v in a and a[v]!=z:return None
                if v not in a:
                    a[v]=z; changed=True
                    if ledger is not None: ledger["unit_assignments"]+=1
        if not changed:return a
def dpll(F,initial=None,trace=True):
    led={"nodes":0,"clause_scans":0,"literal_scans":0,"unit_assignments":0,"branches":0}
    n=nvars(F)
    def rec(a):
        led["nodes"]+=1; a=unit_propagate(F,a,led)
        if a is None:return None
        if all(any(abs(l) in a and a[abs(l)]==int(l>0) for l in c) for c in F):return a
        v=next((v for v in range(1,n+1) if v not in a),None)
        if v is None:return None
        led["branches"]+=1
        for z in (0,1):
            b=dict(a);b[v]=z; r=rec(b)
            if r is not None:return r
        return None
    t=time.perf_counter()
    if trace: tracemalloc.start()
    w=rec(dict(initial or {}))
    if trace:
        _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    else: peak=None
    led.update({"elapsed":time.perf_counter()-t,"peak_bytes":peak,"sat":w is not None,
                "witness":w})
    if w is not None: assert all(any(w[abs(l)]==int(l>0) for l in c) for c in F)
    return led

def width_saturate(F,assumption=-2,width=3,cap=2000):
    initial=[ckey(c) for c in F]+[(assumption,)]
    clauses=[]; pos={}; parent={}; idx=defaultdict(list); q=deque()
    for c in initial:
        if c in pos: continue
        cid=len(clauses);pos[c]=cid;clauses.append(c);parent[cid]=None;q.append(cid)
        for l in c:idx[l].append(cid)
    led=Counter(); empty=None
    while q and len(clauses)<cap and empty is None:
        ci=q.popleft(); c=clauses[ci]
        for p in c:
            for di in list(idx[-p]):
                led["candidate_pairs"]+=1; d=clauses[di]
                R=ckey((set(c)-{p})|(set(d)-{-p}))
                if any(-x in R for x in R):led["tautologies"]+=1;continue
                if len(R)>width:led["width_discards"]+=1;continue
                if R in pos:led["duplicates"]+=1;continue
                subsumed=False
                for e in clauses:
                    led["subsumption_tests"]+=1
                    if len(e)<=len(R) and set(e)<=set(R):subsumed=True;break
                if subsumed:led["subsumed"]+=1;continue
                ri=len(clauses);pos[R]=ri;clauses.append(R);parent[ri]=(ci,di,p);q.append(ri)
                for l in R:idx[l].append(ri)
                led["derived"]+=1
                if not R:empty=ri;break
            if empty is not None:break
    proof=[]; used=set()
    def visit(i):
        if i in used:return
        pr=parent[i]
        if pr is not None:
            visit(pr[0]);visit(pr[1]);proof.append({"id":i,"clause":list(clauses[i]),
                "parent_ids":[pr[0],pr[1]],"parents":[list(clauses[pr[0]]),list(clauses[pr[1]])],
                "pivot_literal_in_first":pr[2]})
        used.add(i)
    if empty is not None:visit(empty)
    return {"found":empty is not None,"initial_count":len(initial),"total_clauses":len(clauses),
            "proof":proof,"proof_steps":len(proof),"proof_max_width":max((len(x["clause"]) for x in proof),default=0),
            "ledger":dict(led),"cap":cap,"width":width}

def up_conflict(clauses,units):
    a={}
    for l in units:
        v=abs(l);z=int(l>0)
        if v in a and a[v]!=z:return True
        a[v]=z
    return unit_propagate(clauses,a) is None
def up_conflict_count(clauses,units,ledger):
    a={}
    for l in units:
        v=abs(l);z=int(l>0)
        if v in a and a[v]!=z:return True
        a[v]=z
    return unit_propagate(clauses,a,ledger) is None
def verify_proof(F,assumption,proof):
    clauses=[ckey(c) for c in F]+[(assumption,)]; checks=[]
    led={"clause_scans":0,"literal_scans":0,"unit_assignments":0}
    for s in proof:
        A=ckey(s["parents"][0]);B=ckey(s["parents"][1]);p=s["pivot_literal_in_first"]
        R=ckey(s["clause"])
        assert A in clauses and B in clauses and p in A and -p in B
        assert R==ckey((set(A)-{p})|(set(B)-{-p})) and not any(-x in R for x in R)
        assert up_conflict_count(clauses,[-l for l in R],led)
        clauses.append(R);checks.append(True)
    return {"steps":len(checks),"all_resolution_valid":all(checks),
            "all_RUP_valid":all(checks),"ends_empty":bool(proof and proof[-1]["clause"]==[]),
            "verification_ledger":led,
            "verification_selected_events":sum(led.values())+5*len(checks)}

def controller(F):
    t=time.perf_counter();tracemalloc.start()
    sat=width_saturate(F,-2,3,1100) if nvars(F)>=2 else {"found":False,"ledger":{},"proof":[]}
    initial={2:1} if sat.get("found") else {}
    back=dpll(F,initial,trace=False)
    _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    work=sum(sat.get("ledger",{}).values())+back["clause_scans"]+back["literal_scans"]+back["nodes"]
    return {"prepass":sat,"backend":back,"total_selected_events":work,
            "elapsed":time.perf_counter()-t,"peak_bytes":peak,
            "forced_x2":sat.get("found",False)}

def validate(F):
    n=nvars(F);deg=defaultdict(lambda:[0,0])
    for c in F:
        for l in c:deg[abs(l)][int(l>0)]+=1
    return {"n":n,"m":len(F),"proper3":all(len(c)==3 and len(set(map(abs,c)))==3 for c in F),
            "unique":len(set(F))==len(F),"strict22":all(deg[v]==[2,2] for v in range(1,n+1))}

def audit_case(name,F):
    n=nvars(F); P=pair_matrix(F); models=model_masks(F); code,refs=relation_code(F)
    canon=reconstruct_canonical(F,code); canon_models=model_masks(canon)
    assert len(models)==len(canon_models)
    endpoints={"zero":status(F,0),"one":status(F,(1<<n)-1)}
    base=dpll(F); ctrl=controller(F)
    return {"name":name,"source_clauses":[list(c) for c in F],"validation":validate(F),
            "local_targets":local_targets(F),"pair_matrix":P,"pair_histogram":pair_hist(P),
            "triple_modes":triple_summary(F),"endpoints":endpoints,"complement_check":
            all(counts_only(F,a)==[3-x for x in counts_only(F,((1<<n)-1)^a)]
                for a in range(1<<n)),"flip_trails":flip_trails(F),"resolvents":resolvents(F),
            "model_count":len(models),"first_models":models[:12],"relation_code":code,
            "reference_signs":refs,"canonical_clauses":[list(c) for c in canon],
            "canonical_model_count":len(canon_models),"baseline_dpll":base,"uniform_controller":ctrl}

def main():
    t=time.perf_counter()
    if len(sys.argv)==3 and sys.argv[1]=="--case":
        name=sys.argv[2]
        F=next(F for n,F in CASES if n==name)
        obj=audit_case(name,F)
        path=f"2026-10-30_0348_FAILED_LITERAL_RUP_REFEREE219_{name}.json"
        with open(path,"w") as f: json.dump(obj,f,indent=2,sort_keys=True)
        print(json.dumps({"case":name,"models":obj["model_count"],
                          "base_nodes":obj["baseline_dpll"]["nodes"],
                          "ctrl_nodes":obj["uniform_controller"]["backend"]["nodes"],
                          "ctrl_events":obj["uniform_controller"]["total_selected_events"],
                          "elapsed":time.perf_counter()-t},indent=2))
        return
    if len(sys.argv)==2 and sys.argv[1]=="--assemble":
        cases=[]
        for name,_ in CASES:
            path=f"2026-10-30_0348_FAILED_LITERAL_RUP_REFEREE219_{name}.json"
            with open(path) as f: cases.append(json.load(f))
    else:
        raise SystemExit("run one --case NAME per invocation, then --assemble")
    proof_search=width_saturate(SWAP6,-2,3,2000)
    proof_check=verify_proof(SWAP6,-2,proof_search["proof"])
    assert proof_search["found"] and proof_check["ends_empty"]
    # Explicit aggregate collision.
    w=next(x for x in cases if x["name"].startswith("W1_"));s=next(x for x in cases if x["name"].startswith("SWAP6_"))
    collision={"same_pair_histogram":w["pair_histogram"]==s["pair_histogram"],
               "same_endpoint_N":w["endpoints"]["zero"]["N"]==s["endpoints"]["zero"]["N"] and w["endpoints"]["one"]["N"]==s["endpoints"]["one"]["N"],
               "pair_histogram":w["pair_histogram"],"W1_models":w["model_count"],"SWAP6_models":s["model_count"]}
    assert collision=={"same_pair_histogram":True,"same_endpoint_N":True,"pair_histogram":{'SSSUUSUU':117,'SUUS':43,'':17,'SSUU':13},"W1_models":0,"SWAP6_models":54}
    # Polarity-renaming invariance and exact22 trit count finite controls.
    rng=random.Random(SEED); rename=[]
    base_count=len(model_masks(SWAP6))
    for _ in range(8):
        V={v for v in range(1,16) if rng.randrange(2)}; G=flip_formula(SWAP6,V)
        rename.append({"flipped":sorted(V),"models":len(model_masks(G))})
    assert all(x["models"]==base_count for x in rename)
    trits={str(n):abstract_exact22_codes(n) for n in range(1,6)}
    assert all(trits[str(n)]==3**n for n in range(1,6))
    obj={"run_id":"FAILED-LITERAL-RUP-REFEREE219","seed":SEED,
         "status":{"resolution_certificate":"PROVED/EXACT source-specific",
                   "pair_relation_code":"PROVED/EXACT representation theorem",
                   "aggregate_shortcut":"FALSIFIED/RETIRED",
                   "finite_tests":"COMPUTATIONAL","P_vs_NP":"OPEN"},
         "claims":{"forced_literal":"SWAP6 entails x2 via a 29-step-or-shorter width-3 resolution/RUP refutation of SWAP6 and not x2",
                   "representation":"variable-labelled same/opposite occurrence relations reconstruct signs up to independent variable complements",
                   "strict22_code":"one trit per variable is necessary and sufficient for four-occurrence two-positive/two-negative sign relations modulo complement",
                   "warning":"proof verification is cheap; uniform proof discovery and failed probes are charged"},
         "proof_search":proof_search,"proof_check":proof_check,"aggregate_collision":collision,
         "polarity_rename_controls":rename,"abstract_exact22_switching_classes":trits,
         "strict22_fixed_length_bits":{"n":15,"lower":math.ceil(15*math.log2(3)),"simple_upper":30},
         "cases":cases,"elapsed":time.perf_counter()-t}
    with open("2026-10-30_0348_FAILED_LITERAL_RUP_REFEREE219_raw.json","w") as f:json.dump(obj,f,indent=2,sort_keys=True)
    summary={"run_id":obj["run_id"],"proof_steps":proof_search["proof_steps"],
             "derived_before_empty":proof_search["ledger"].get("derived",0),
             "candidate_pairs":proof_search["ledger"].get("candidate_pairs",0),
             "subsumption_tests":proof_search["ledger"].get("subsumption_tests",0),
             "proof_check":proof_check,"aggregate_collision":collision,
             "exact22_classes":trits,"strict22_bits":obj["strict22_fixed_length_bits"],
             "case_work":[{"name":x["name"],"models":x["model_count"],
                           "base_nodes":x["baseline_dpll"]["nodes"],
                           "base_events":x["baseline_dpll"]["clause_scans"]+x["baseline_dpll"]["literal_scans"]+x["baseline_dpll"]["nodes"],
                           "ctrl_nodes":x["uniform_controller"]["backend"]["nodes"],
                           "ctrl_events":x["uniform_controller"]["total_selected_events"],
                           "forced_x2":x["uniform_controller"]["forced_x2"]} for x in cases],
             "elapsed":obj["elapsed"]}
    with open("2026-10-30_0348_FAILED_LITERAL_RUP_REFEREE219_summary.json","w") as f:json.dump(summary,f,indent=2,sort_keys=True)
    print(json.dumps(summary,indent=2,sort_keys=True))
if __name__=="__main__":main()
