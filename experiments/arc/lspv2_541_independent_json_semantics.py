#!/usr/bin/env python3
"""Independent Python control for ECMAScript JSON nonfinite-ID identity collapse.
Not the historical checker, and does not claim to reproduce JS serializer verbatim.
"""
import json
import math
import sys

checks = 0

def ck(cond, label):
    global checks
    checks += 1
    if not cond:
        raise AssertionError(label)

def emulate_js_stringify_nonfinite(v):
    """Only special Number->null behavior; canonical decimal formatting is NOT emulated."""
    if isinstance(v, float) and not math.isfinite(v):
        return None
    if isinstance(v, list):
        return [emulate_js_stringify_nonfinite(x) for x in v]
    if isinstance(v, dict):
        return {k: emulate_js_stringify_nonfinite(x) for k, x in v.items()}
    return v

for name, raw in [
    ("paid", '{"proof":[{"id":1e400},{"id":-1e400}],"parents":[1e400,-1e400]}'),
    ("source", '{"clauses":[{"id":1e400},{"id":-1e400}],"sourceIds":[1e400,-1e400]}'),
]:
    obj = json.loads(raw)
    key = "proof" if name == "paid" else "clauses"
    ids = [e["id"] for e in obj[key]]
    ck(ids[0] == math.inf, name + " positive overflow")
    ck(ids[1] == -math.inf, name + " negative overflow")
    ck(ids[0] != ids[1], name + " distinct original IDs")
    canonical = emulate_js_stringify_nonfinite(obj)
    ck([e["id"] for e in canonical[key]] == [None, None], name + " same null key")
    ck(len({e["id"] for e in canonical[key]}) == 1, name + " collision")
    try:
        json.dumps(obj, allow_nan=False)
    except ValueError:
        checks += 1
    else:
        raise AssertionError(name + " strict JSON serializer must reject nonfinite parsed values")

finite = json.loads('{"proof":[{"id":100},{"id":-100}],"parents":[100,-100]}')
ck(len({x["id"] for x in finite["proof"]}) == 2, "finite IDs stable")
ck(len({x["id"] for x in emulate_js_stringify_nonfinite(finite)["proof"]}) == 2, "finite normalization")
small = json.loads('{"charge":1e-6}')
ck(small["charge"] == 0.000001, "small exponent exact binary floating point")
ck(math.isfinite(small["charge"]), "small exponent finite")
print(json.dumps({"checks": checks, "status": "PASS", "scope": "Python independent parsing and nonfinite ID collision; not native checker or JS numeric formatter"}))
