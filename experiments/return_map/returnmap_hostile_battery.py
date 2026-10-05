#!/usr/bin/env python3
"""RETURNMAP1 finite/symbolic hostile battery.

Tests candidate SAT-return exponent ledgers. This does not construct a return
map and cannot establish an asymptotic lower bound. It is designed to reject
candidate ledgers that already violate known accounting constraints.
"""
import argparse, itertools, json, math, random

def classify(zeta, calls, call_scale, build, space, generic=False, fullcarry=False):
    reasons=[]
    if generic: reasons.append("GENERIC_COMPUTATION_ENCODING")
    if fullcarry and zeta < 1-1e-12: reasons.append("FULL_INPUT_CARRY_CONTRADICTION")
    inherited = calls + call_scale
    if call_scale >= 1-1e-12: reasons.append("CURRENT_SCALE_SAT_CALL")
    if zeta >= 1-1e-12: reasons.append("NONCONTRACTIVE_RETURN_LENGTH")
    return {"survives":not reasons,"reasons":reasons,
            "zeta":zeta,"call_count_exp":calls,"call_scale_exp":call_scale,
            "inherited_sat_exp_coefficient":inherited,
            "build_exp":build,"space_exp":space}

def cycle_gain(edges):
    g=1.0
    for e in edges:g*=e
    return g

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--seed",type=int,default=271828)
    args=ap.parse_args()
    rng=random.Random(args.seed)

    named={
      "generic_robson": classify(1.0,0.0,1.0,1.0,1.0,generic=True,fullcarry=True),
      "fullcarry_fake_half": classify(0.5,0.0,0.5,0.5,0.5,fullcarry=True),
      "current_scale_oracle": classify(0.5,0.0,1.0,0.5,0.5),
      "typed_fractional_candidate": classify(0.5,0.0,0.5,0.6,0.5)
    }

    grid=[]
    vals=[0.0,0.25,0.5,0.75,1.0,1.25]
    for z,c,s,b in itertools.product(vals,vals,vals,vals):
        q=classify(z,c,s,b,0.5)
        if q["survives"]:
            grid.append(q)
    cycles=[]
    for _ in range(32):
        es=[rng.choice([0.5,0.75,1.0]) for _ in range(rng.choice([2,3,4]))]
        cycles.append({"edges":es,"gain":cycle_gain(es),"contractive":cycle_gain(es)<1-1e-12})

    print(json.dumps({
      "status":"COMPUTATIONAL hostile accounting only",
      "seed":args.seed,
      "named_controls":named,
      "grid_survivor_count":len(grid),
      "grid_survivor_examples":grid[:20],
      "cycle_controls":cycles,
      "interpretation":[
        "A survivor is only not-yet-falsified by this ledger.",
        "A real candidate still needs exact SAT semantics, SAME_REALIZATION, acquisition, setup, classification, construction, writing, workspace, repeatability and model matching.",
        "Dell-van Melkebeek compression barriers are not terminal under the P=NP counterfactual."
      ]},indent=2,sort_keys=True))
if __name__=="__main__":main()
