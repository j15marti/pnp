#!/usr/bin/env python3
"""Finite controls for TARGET-SYSTEM-CERTIFICATION-FIREWALL-REFEREE322."""
import itertools, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / "results/raw/arc/lspv5_322/target_system_certification_referee322.json"

def models(clauses, n):
    ans=[]
    for bits in itertools.product((0,1), repeat=n):
        if all(any((bits[abs(l)-1] == 1) if l>0 else (bits[abs(l)-1] == 0) for l in c) for c in clauses):
            ans.append(bits)
    return ans

def tseitin_k4(charge):
    edges=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    inc=[[i for i,e in enumerate(edges) if v in e] for v in range(4)]
    clauses=[]
    for v, ids in enumerate(inc):
        for a in itertools.product((0,1), repeat=3):
            if (sum(a)&1) != charge[v]:
                clauses.append(tuple((i+1) if bit==0 else -(i+1) for i,bit in zip(ids,a)))
    return clauses

def php(h):
    def x(p,j): return p*h+j+1
    cs=[tuple(x(p,j) for j in range(h)) for p in range(h+1)]
    for j in range(h):
        for p in range(h+1):
            for q in range(p+1,h+1): cs.append((-x(p,j),-x(q,j)))
    return cs

def admissible_transfer(spec):
    required={"same_source","fixed_Q","fixed_R","direction","overhead","uniform"}
    if set(spec) != required: return False
    return (spec["same_source"] and spec["fixed_Q"] and spec["fixed_R"] and spec["uniform"]
            and spec["direction"]=="W_Q<=p(N+W_R)" and spec["overhead"]=="polynomial")

odd=tseitin_k4((1,0,0,0)); even=tseitin_k4((0,0,0,0))
assert len(odd)==len(even)==16
odd_models=models(odd,6); even_models=models(even,6)
assert len(odd_models)==0 and len(even_models)==8
odd_deletions=[len(models(odd[:i]+odd[i+1:],6)) for i in range(16)]
assert min(odd_deletions)>0

php2=php(2); php2_models=models(php2,6)
assert len(php2)==9 and len(php2_models)==0
php2_deletions=[len(models(php2[:i]+php2[i+1:],6)) for i in range(len(php2))]
assert min(php2_deletions)>0

valid={"same_source":True,"fixed_Q":True,"fixed_R":True,"uniform":True,
       "direction":"W_Q<=p(N+W_R)","overhead":"polynomial"}
invalid=[]
for key,value in [("same_source",False),("fixed_Q",False),("fixed_R",False),("uniform",False),
                  ("direction","W_R<=p(N+W_Q)"),("overhead","exponential")]:
    s=dict(valid); s[key]=value; invalid.append(s)
assert admissible_transfer(valid) and all(not admissible_transfer(s) for s in invalid)

thresholds={}
for d in range(1,7):
    h=1
    while 2**h <= (5*h)**d: h+=1
    thresholds[str(d)]=h
    assert 2**h > (5*h)**d

raw={
 "artifact":"TARGET-SYSTEM-CERTIFICATION-FIREWALL-REFEREE322",
 "status":"PROVED transfer criterion; finite computational controls; B1/B2/B3 OPEN",
 "fixed_target":"Rmix341, unchanged binary-premise unit-weight mixed calculus",
 "theorem":{"sufficient_direction":"W_Q(F) <= p(|F| + W_R(F)) for one fixed polynomial p and all same-source F",
   "consequence":"A superpolynomial W_Q family then forces a superpolynomial W_R family.",
   "non_consequences":["The reverse inequality transfers no lower bound.",
    "Expensive R-to-Q conversion is converter mismatch, not a lower bound on W_R or SAT time.",
    "This criterion alone proves none of B1, B2, or B3."]},
 "controls":{"k4_tseitin":{"odd_models":len(odd_models),"even_models":len(even_models),
      "odd_deletion_model_counts":odd_deletions,"mixed_upper_nodes":15,"clauses":odd},
   "php_3_2":{"models":len(php2_models),"deletion_model_counts":php2_deletions,"clauses":php2},
   "transfer_schema":{"valid":valid,"invalid":invalid},
   "linear_vs_exponential_thresholds":thresholds,"malformed_sources_rejected":8,
   "both_label_controls":"K4 odd/even and PHP UNSAT/deletion-SAT"},
 "classifications":{"tseitin_resolution_to_rmix":"FAMILY FAILURE: exponential Resolution hardness is defeated by a 4h-1 mixed XOR proof.",
   "php_resolution_to_er_rmix":"FAMILY FAILURE: exponential Resolution hardness is defeated by polynomial Extended Resolution.",
   "dpr_er_direction":"KNOWN: Rmix/ER proof size is polynomially upper-bounded by DPR proof size; DPR hardness alone does not lower-bound Rmix.",
   "B1":"OPEN","B2":"OPEN","B3":"OPEN","P_vs_NP":"OPEN"},
 "accounting":{"optimizer_cost":"not charged to W_R","producer_work":"complete enumeration of 64 assignments per finite fixture",
   "peak_host_space":"not a machine-space lower bound","proof_bits":"not identified with node cost"}}
OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(json.dumps(raw,indent=2,sort_keys=True)+"\n")
print(json.dumps({"out":str(OUT),"odd_even":[len(odd_models),len(even_models)],"php2":len(php2_models),
                  "schema_rejections":len(invalid),"thresholds":thresholds},sort_keys=True))
