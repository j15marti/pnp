#!/usr/bin/env python3
"""LSPV-2/417: replay full typed proof using the actual published CANON2 and CANON2R checkers.
Run at repo root: python experiments/arc/lspv2_417_affine_parent_bridge_replay.py
No new inference rule is introduced; the proposed broad AND3 input is a rejection control.
"""
from pathlib import Path
import copy
import importlib.util
import itertools
import json

ROOT = Path(__file__).resolve().parents[2]

def load(name, location):
    spec = importlib.util.spec_from_file_location(name, ROOT / location)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

c2 = load("canon2", "experiments/arc/lspv5_361/rmix341_canon2_repair_referee361.py")
r2 = load("canon2r", "experiments/arc/lspv5_362/rmix341_raw_affine_firewall_referee362.py")
record = json.loads((ROOT / "results/raw/arc/2026-11-05_0612_LSPV2_AFFINE_AND3_BRIDGE417_raw.json").read_text())
strict, broad = record["strict_certificate"], record["broad_candidate"]
raw = record["source_raw"].encode("ascii")
assert len(strict["nodes"]) == 18 and len(broad["nodes"]) == 17
assert [n["rule"] for n in strict["nodes"]].count("LOCAL") == 1
assert strict["nodes"][15]["rule"] == "LOCAL"
assert strict["nodes"][15]["parent"] == {"node":14,"view":"affine"}
assert strict["nodes"][15]["out"]["factor"] == {"support":[],"truth":[1]}
assert strict["nodes"][16]["left"] == {"node":15,"view":"factor"}
assert broad["nodes"][15]["left"] == {"node":14,"view":"affine"}

stats = c2.Checker(strict, strict["source"]).run()
assert stats["accepted"] and stats["paid_nodes"] == 18
wrapper_stats = r2.check_wrapper(r2.wrap(raw, strict))
assert wrapper_stats["paid_nodes"] == 18 or wrapper_stats.get("checker",{}).get("paid_nodes")==18

try:
    c2.Checker(broad, broad["source"]).run()
    raise AssertionError("broad affine-input AND3 incorrectly accepted")
except c2.Reject as e:
    assert "bad AND3 parents" in str(e)

def is_sat(clauses, nvars):
    for bits in itertools.product((0,1), repeat=nvars):
        if all(any(bits[abs(x)-1] == int(x>0) for x in clause) for clause in clauses):
            return True
    return False

assert not is_sat(strict["source"]["clauses"],2)
assert is_sat(strict["source"]["clauses"][:2],2)

controls = []
for label in ("bad_GF2","wrong_source","false_LOCAL","wrong_DEF","false_AND3"):
    altered = copy.deepcopy(strict)
    if label == "bad_GF2":
        altered["nodes"][17]["affine"]["rhs"] = 0
    elif label == "wrong_source":
        altered["source"]["clauses"][2] = [1]
    elif label == "false_LOCAL":
        altered["nodes"][15]["out"]["factor"]["truth"] = [0]
    elif label == "wrong_DEF":
        altered["nodes"][1]["var"] = 5
    else:
        altered["nodes"][16]["factor"]["truth"] = [0,1]
    try:
        c2.Checker(altered, strict["source"]).run()
        raise AssertionError("bad certificate unexpectedly accepted: "+label)
    except c2.Reject:
        controls.append(label)
assert len(controls) == 5

print(json.dumps({"status":"PASS","strict_paid_nodes":stats["paid_nodes"],
                  "strict_references":stats["references"],"strict_truth_rows":stats["truth_rows"],
                  "broad_rejection":"bad AND3 parents","raw_source_bytes":len(raw),
                  "negative_controls":controls,"same_R_B3":"OPEN"},indent=2))
