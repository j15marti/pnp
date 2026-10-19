#!/usr/bin/env python3
"""CHMY conditional base-slot injection erasure audit.

Implements the field-inner-product T-layer primitive of CHMY ECCC TR20-103,
Definition 36/Theorems 33 and 35: T_i(j)=<a_i^(j+1),b_i>_F2,
with a,b uniform in GF(2^h), outer layers independent.
The first CHMY private PRG layer is REPLACED by arbitrary source f: this is
a proposed reduction being falsified, not a claim about original PRG security.
The tiny field parameters check local identities, not full CHMY PRG fooling.
"""
import argparse
import itertools
import json
import math
import random
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

IRREDUCIBLES = {3: 0b1011, 4: 0b10011, 5: 0b100101}

def gf_mul(a, b, h, modulus):
    out = 0
    top, mask = 1 << h, (1 << h)-1
    for _ in range(h):
        if b&1: out ^= a
        b >>= 1
        a <<= 1
        if a&top: a ^= modulus
        a &= mask
    return out

def t_mask(a, b, N, h, modulus):
    p, result = 1, 0
    for j in range(N):
        p=gf_mul(p,a,h,modulus)
        if (p&b).bit_count()&1: result |= 1<<j
    return result

def apply_fk_to_base(x, ds, ts, N):
    assert len(ds)==len(ts)
    mask=(1<<N)-1
    for d,t in zip(ds,ts): x=(d^(t&x))&mask
    return x

def fold_base_coeff(ts,N):
    mask=(1<<N)-1
    for t in ts: mask &= t
    return mask

def exhaustive_controls(N,h,poly):
    assert (N,h) in {(4,3),(8,4)}
    masks=[t_mask(a,b,N,h,poly) for a in range(1<<h) for b in range(1<<h)]
    R=1<<(2*h)
    count=[sum((v>>j)&1 for v in masks) for j in range(N)]
    assert count==[((1<<h)-1)*(1<<(h-1))]*N
    layers=N.bit_length()-2
    sequences=((x,) for x in masks) if layers==1 else itertools.product(masks,masks)
    totals={"total_seed_sequences":0,"support_1_collisions":0,"support_2_collisions":0,
            "rank_sum":0,"identity_failures":0,"max_rank":0}
    s1, s2=1, 1|(1<<(N-1))
    for ts in sequences:
        visible=fold_base_coeff(ts,N)
        totals["total_seed_sequences"]+=1
        totals["rank_sum"]+=visible.bit_count()
        totals["max_rank"]=max(totals["max_rank"],visible.bit_count())
        if not visible&s1: totals["support_1_collisions"]+=1
        if not visible&s2: totals["support_2_collisions"]+=1
        ds=[(i*7+5)&((1<<N)-1) for i in range(layers)]
        u=apply_fk_to_base(0,ds,ts,N)
        v=apply_fk_to_base(s2,ds,ts,N)
        if u^v != s2&visible: totals["identity_failures"]+=1
    assert totals["identity_failures"]==0
    assert totals["total_seed_sequences"]==R**layers
    assert totals["rank_sum"]==N*(count[0]**layers)
    p=(2**h-1)/(2**(h+1))
    totals.update({"N":N,"field_bits":h,"field_polynomial":hex(poly),"r":layers+1,
      "marginal_one_probability":f"{count[0]}/{R}",
      "exact_expected_visible_positions":totals["rank_sum"]/totals["total_seed_sequences"],
      "observed_any_visible_probability_support_2":
        1-totals["support_2_collisions"]/totals["total_seed_sequences"],
      "union_bound_probability_support_2":min(1,2*p**layers)})
    if layers>1:
        totals["hostile_correlated_layers_expected_rank"]=N*p
        totals["hostile_correlated_layers_violates_constant_two_bound"]=N*p>2
    return totals

def randomized_controls(seed,trials):
    rng=random.Random(seed)
    N,h,poly=16,5,IRREDUCIBLES[5]
    layers=int(math.log2(N))-1
    differences={"1":1,"2":1|(1<<5),"4":sum(1<<j for j in [0,5,10,15])}
    counts={k:{"different":0,"equal":0} for k in differences}
    checked,maxrank,sumrank=0,0,0
    for _ in range(trials):
        ts=[t_mask(rng.randrange(1<<h),rng.randrange(1<<h),N,h,poly) for _ in range(layers)]
        ds=[rng.getrandbits(N) for _ in range(layers)]
        base=rng.getrandbits(N)
        coefficient=fold_base_coeff(ts,N)
        maxrank=max(maxrank,coefficient.bit_count())
        sumrank+=coefficient.bit_count()
        output=apply_fk_to_base(base,ds,ts,N)
        for key,delta in differences.items():
            other=apply_fk_to_base(base^delta,ds,ts,N)
            assert output^other==delta&coefficient
            checked+=1
            counts[key]["equal" if output==other else "different"]+=1
    p=((2**h-1)/2**(h+1))**layers
    return {"N":N,"field_bits":h,"field_polynomial":hex(poly),"r":layers+1,
       "seed":seed,"trials":trials,"checked_identity_pairs":checked,
       "estimated_expected_visible_positions":sumrank/trials,"max_visible_positions":maxrank,
       "exact_expected_visible_positions_formula":N*p,
       "observed_collisions_by_support_size":counts,
       "union_bound_any_difference_probability":{k:min(1,int(k)*p) for k in differences}}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--seed",type=int,default=202610200014)
    parser.add_argument("--trials",type=int,default=15000)
    parser.add_argument("--output",type=str,default="results/raw/separation/2026-10-20_FKBASEERASURE1.json")
    opt=parser.parse_args()
    exact=[exhaustive_controls(4,3,IRREDUCIBLES[3]),exhaustive_controls(8,4,IRREDUCIBLES[4])]
    sampled=randomized_controls(opt.seed,opt.trials)
    result={"run_id":"CHMY_FK_BASE_ERASURE_NO_GO",
       "timestamp_KST":datetime.now(ZoneInfo("Asia/Seoul")).isoformat(),
       "status":"PROVED/EXACT symbolic base-slot lemma, COMPUTATIONAL bounded tests, independent review pending, P vs NP OPEN",
       "source":"CHMY ECCC TR20-103 rev1 Definitions 36 Theorems 33/35",
       "interpretation":"Original private G1 is replaced by arbitrary source f ONLY for testing a candidate reduction",
       "symbolic_identity":"Phi_r(f) xor Phi_r(f')=(f xor f') and intersect_i T_i",
       "bit_marginal":"(2^h-1)/2^(h+1), independently across outer layers only",
       "same_seed_collision":"Pr[same output] >= 1-2delta for source disagreement at most delta*N",
       "two_promise_NO":"supported hard source exists by circuit counting and Chernoff",
       "not_proved":"No cofinal beta descent, CHMY full PRG security at toy parameters, one-work-tape reduction or P != NP",
       "exact_cases":exact,"sampled_cases":sampled,"failures":0}
    path=Path(opt.output);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"path":str(path),
      "checks":sum(t["total_seed_sequences"] for t in exact)+sampled["checked_identity_pairs"],
      "failures":result["failures"],
      "sampled_collisions":sampled["observed_collisions_by_support_size"]},indent=2))

if __name__=="__main__": main()
