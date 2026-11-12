#!/usr/bin/env python3
"""LSPV-5/506: assemble raw evidence.  Independently REPLAYS every C-solver
witness used in a claim (parents resident, keep subset of previous residents,
peak/overwrite rule, cap, final sink) and recomputes its areas in Python.
Usage: python3 lspv5_506_assemble.py <scratch_dir> <out.json>"""
import json, sys, hashlib, os
sys.path.insert(0, os.path.dirname(__file__))
from lspv5_506_recompute_frontier import dag
W38 = "results/raw/arc/2026-11-12_0436_LSPV4_560_W38_ACCEPTED.json"
W28 = "results/raw/arc/2026-11-12_0748_LSPV5_506_W28_EXCISED_NATIVE386.json"
W29 = "results/raw/arc/2026-11-12_0748_LSPV5_506_W29_EXCISED_UNUSED_OWNER_NATIVE386.json"
def replay(path, trace, residents, cap):
    par, size = dag(path); old = set(); A = B = 0
    for j, row in zip(trace, residents):
        post = set(row); keep = post - {j}
        assert j in post and keep <= old and set(par[j]) <= old
        peak = len(keep | set(par[j])) + 1
        assert peak <= cap or (peak == cap + 1 and any(
            p not in keep and size[p] >= size[j] for p in par[j]))
        A += len(post); B += sum(size[p] for p in post); old = post
    assert len(par) - 1 in old
    return {"executions": len(trace), "distinct": len(set(trace)), "slot_area": A, "byte_area": B}
def load(sp, name):
    return [json.loads(l) for l in open(os.path.join(sp, name + ".jsonl"))]
sp, out = sys.argv[1], sys.argv[2]
res = {"id": "LSPV-5/506", "date_pst": "2026-11-12 07:48",
       "status": "COMPUTATIONAL exact finite search + PROVED/EXACT restricted lemma; P versus NP OPEN",
       "packets": {}}
for p in (W38, W28, W29):
    b = open(p, "rb").read()
    res["packets"][p] = {"bytes": len(b), "sha256": hashlib.sha256(b).hexdigest(),
                         "git_blob": hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()}
for tag, path, cap in (("W38_cap4_slot", W38, 4), ("W38_cap4_byte", W38, 4),
                       ("W28_cap4_slot", W28, 4), ("W28_cap4_byte", W28, 4)):
    fn = {"W38_cap4_slot": "w38_c4_o0", "W38_cap4_byte": "w38_c4_o1",
          "W28_cap4_slot": "w28_c4_o0", "W28_cap4_byte": "w28_c4_o1"}[tag]
    rows = load(sp, fn); fr = {}
    for r in rows:
        v = replay(path, r["trace"], r["residents"], cap)
        prim = v["slot_area"] if "slot" in tag else v["byte_area"]
        assert prim == r["primary"], (tag, r["w"])
        fr[r["w"]] = {"min_primary": r["primary"], "secondary_at_min": r["secondary"],
                      "replayed": v}
        if r["w"] in (28, 35, 36):
            fr[r["w"]]["trace"] = r["trace"]; fr[r["w"]]["residents"] = r["residents"]
    res[tag] = {"cap": cap, "frontier_by_RES_executions": fr}
for fn in ("w38_c3_o0", "w38_c2_o0", "w28_c3_o0", "w28_c2_o0"):
    res["no_hit_" + fn] = {"rows": len(load(sp, fn))}
res["joint_vectors_post_step_W_A_B"] = {
    "W38_once (LSPV-4/563)": [38, 83, 885], "W39_one_recompute (LSPV-4/562)": [39, 71, 748],
    "W28_excised_core": [28, 61, 615], "W29_excised_CLI_unused_owner": [29, 61, 615]}
print(json.dumps({k: v for k, v in res.items() if k.startswith("joint")}))
json.dump(res, open(out, "w"), indent=1)
