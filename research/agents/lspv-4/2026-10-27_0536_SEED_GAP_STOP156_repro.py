#!/usr/bin/env python3
"""LSPV-4 SEED-GAP-QUERY156. Deterministic, exhaustive black-box seed audit.

Use python3 2026-10-27_0536_SEED_GAP_STOP156_repro.py; no dependencies or RNG.
The tester is a finite seed-bit oracle, NOT a physical SAT machine.
"""
from functools import lru_cache
from math import comb
import json

checks=0
def ck(condition,label):
    global checks
    checks+=1
    if not condition:
        raise AssertionError(label)

def stop(bits,a,b):
    n=len(bits)
    assert 0<=a<b<=n
    ones=zeros=0
    for i,bit in enumerate(bits,start=1):
        if bit:
            ones+=1
        else:
            zeros+=1
        if ones>=a+1:
            return True,i
        if zeros>=n-b+1:
            return False,i
    raise AssertionError("threshold stopping invariant violated")

def decision_tree(n,a,b):
    """Exact minimax depth; fresh positions are symmetric."""
    @lru_cache(None)
    def walk(o,z):
        remaining=n-o-z
        low=(o<=a)
        high=(o+remaining>=b)
        if not(low and high):
            return 0
        children=[]
        for bit in (0,1):
            no,nz=o+bit,z+(1-bit)
            if no<=a or no+(n-no-nz)>=b:
                children.append(walk(no,nz))
        return 1+max(children)
    return walk(0,0),walk.cache_info().currsize

def enumerate_tests(max_n=10):
    cases=profiles=minimax_states=0
    selected={}
    for n in range(1,max_n+1):
        for a in range(n):
            for b in range(a+1,n+1):
                cases+=1
                k=n-(b-a)+1
                depth,states=decision_tree(n,a,b)
                minimax_states+=states
                ck(depth==k,f"minimax failed {(n,a,b,depth,k)}")
                maximum=0
                for mask in range(1<<n):
                    bits=[(mask>>i)&1 for i in range(n)]
                    result,used=stop(bits,a,b)
                    weight=mask.bit_count()
                    profiles+=1
                    ck(used<=k,f"call cap failed {(n,a,b,mask)}")
                    if weight<=a:
                        ck(not result,f"SAT false accept {(n,a,b,mask)}")
                        maximum=max(maximum,used)
                    elif weight>=b:
                        ck(result,f"UNSAT witness missed {(n,a,b,mask)}")
                        maximum=max(maximum,used)
                ck(maximum==k,f"sharpness failed {(n,a,b,maximum,k)}")
                if n in (2,4,8,10) and a in (0,n//4) and b in (n//2,n):
                    selected[f"{n},{a},{b}"]={"K":k,"observed_max":maximum}
    return {"max_R":max_n,"gap_pairs":cases,"bit_profiles":profiles,
            "minimax_states_checked":minimax_states,"selected_cases":selected}

def hostile_controls():
    n,a,b=8,2,6
    k=n-(b-a)+1
    accepted,used=stop([1]*n,a,b)
    ck(accepted and used==a+1,"early acceptance")
    ck(used<n,"no early save")
    rej,used_low=stop([0]*n,a,b)
    ck((not rej) and used_low==n-b+1,"early rejection")
    low=[1]*a+[0]*(n-a)
    high=[1]*a+[0]*(n-b)+[1]*(b-a)
    low_ans,low_used=stop(low,a,b)
    high_ans,high_used=stop(high,a,b)
    ck(low_used==k and high_used==k and not low_ans and high_ans,"common prefix depths")
    ck(low[:k-1]==high[:k-1],"adversarial common prefix")
    trials=0
    for proof in range(1<<n):
        proof_bits=[(proof>>i)&1 for i in range(n)]
        sat_bits=[int(i<a) for i in range(n)]
        sat_ok,_=stop(sat_bits,a,b)
        ck(not sat_ok,"mock SAT unsound")
        unsat_ok,unsat_reads=stop(proof_bits,a,b)
        if proof==(1<<n)-1:
            ck(unsat_ok and unsat_reads==a+1,"mock UNSAT incomplete")
        ck(unsat_reads<=k,"UNSAT mock time cap")
        trials+=1
    alias=[0 if z<=a else z-a for z in range(n)]
    proof_cells=[1]*(max(alias)+1)
    oracle_bits=[proof_cells[alias[z]] for z in range(n)]
    physically_ok,physical_reads=stop(oracle_bits,a,b)
    early_union=len(set(alias[:physical_reads]))
    full_union=len(set(alias))
    ck(physically_ok and physical_reads==a+1,"physical good proof rejected")
    ck(early_union==1 and full_union>early_union,"actual stopped union not strict")
    ck(full_union==n-a,"full proof union")
    for mask in range(1<<len(proof_cells)):
        candidate=[(mask>>j)&1 for j in range(len(proof_cells))]
        bits=[candidate[u] for u in alias]
        ok,_=stop(bits,a,b)
        if all(candidate):
            ck(ok,"UNSAT good fixed proof")
        sat_ok,_=stop([int(z<a) for z in range(n)],a,b)
        ck(not sat_ok,"SAT false acceptance")
    sat=[int(i<a) for i in range(n)]
    ck(any(sat) and sum(sat)==a,"single-seed shortcut control")
    p=comb(a,2)/comb(n,2)
    ck(p>0,"sampler falsely appears zero error")
    return {"R":n,"A":a,"B":b,"K":k,"all_seed_queries":n,
            "good_proof_early_queries":used,
            "physical_aliased_early_union":early_union,
            "physical_aliased_all_seed_union":full_union,
            "worst_case_early_queries":k,"SAT_early_reject_queries":used_low,
            "proof_trials":trials,"two_seed_SAT_false_positive_probability":p,
            "two_seed_SAT_false_positive_exact":"1/28"}

if __name__=="__main__":
    systematic=enumerate_tests(10)
    hostile=hostile_controls()
    result={"run":"SEED-GAP-QUERY156","date":"2026-10-27",
            "status":"COMPUTATIONAL for finite tests; exact black-box theorem separately proved",
            "source_model":"abstract deterministic seed-bit oracle, independent of SAT semantics",
            "random_seed":None,"assertion_groups":checks,"failures":0,
            "systematic":systematic,"hostile":hostile,
            "limits":"Finite promise oracle enumeration does not establish generic SAT hardness, transcript all-input completeness, or machine-bit-time lower bounds."}
    print(json.dumps(result,indent=2,sort_keys=True))
