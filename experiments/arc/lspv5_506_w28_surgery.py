#!/usr/bin/env python3
"""LSPV-5/506 red team: excise the AND2-extension detour of the LSPV-4/560 W38
packet.  Paid RES 0..6 (records 23..29) re-derive [-1,-4,-5,-7], which is
already original SOURCE record 7.  Redirect every use of records 28/29 to
record 7, drop DEF records 17..22, all three gate owners and RES 23..29.
Writes the shortened packet; acceptance is decided ONLY by the unchanged
archived /386 checker (node experiments/arc/lspv2_386_independent_verify.js).
Run: python3 experiments/arc/lspv5_506_w28_surgery.py
"""
import json, hashlib, subprocess, sys, pathlib
SRC = "results/raw/arc/2026-11-12_0436_LSPV4_560_W38_ACCEPTED.json"
OUT = "results/raw/arc/2026-11-12_0748_LSPV5_506_W28_EXCISED_NATIVE386.json"
raw = pathlib.Path(SRC).read_bytes()
blob = hashlib.sha1(b"blob %d\0" % len(raw) + raw).hexdigest()
assert blob == "6b72c961c2db19be87a0936361c467ef3445f4e2", blob
d = json.loads(raw)
R = d["records"]
assert R[7]["kind"] == "SOURCE" and R[7]["c"] == [-1, -4, -5, -7]
assert R[28]["c"] == R[29]["c"] == R[7]["c"]
drop = set(range(17, 30))
redirect = {28: 7, 29: 7}
new_index, recs = {}, []
for i, r in enumerate(R):
    if i in drop:
        continue
    r = dict(r)
    r["parents"] = [new_index[redirect.get(p, p)] for p in r["parents"]]
    new_index[i] = len(recs)
    recs.append(r)
# every surviving parent must be a surviving record (no hidden use of dropped DEF/RES)
users = {p for i, r in enumerate(R) if i not in drop for p in r["parents"]}
assert not (users & (drop - set(redirect))), users & drop
out = {"spec": d["spec"], "gate_defs": [], "records": recs,
       "summary": {"source": 17, "resolution": len(recs) - 17, "def_views": 0,
                   "paid_gates": 0, "paid_total": len(recs) - 17,
                   "live_records": len(recs)}}
# Variant B: CLI control `gate_defs.shift()` is a no-op on [] so the CLI
# harness rejects ANY zero-owner packet; keep original owner 0 unused (W29).
out29 = json.loads(json.dumps(out))
out29["gate_defs"] = [d["gate_defs"][0]]
out29["summary"]["paid_gates"] = 1
out29["summary"]["paid_total"] += 1
OUT29 = OUT.replace("W28_EXCISED", "W29_EXCISED_UNUSED_OWNER")
rc = 0
for path, obj in ((OUT, out), (OUT29, out29)):
    body = json.dumps(obj, separators=(",", ":")).encode()
    pathlib.Path(path).write_bytes(body)
    print(json.dumps({"out": path, "records": len(obj["records"]),
                      "paid_total": obj["summary"]["paid_total"],
                      "bytes": len(body),
                      "sha256": hashlib.sha256(body).hexdigest()}))
    # (i) original checker CLI, unchanged
    r = subprocess.run(["node", "experiments/arc/lspv2_386_independent_verify.js", path],
                       capture_output=True, text=True)
    print("CLI rc=%d" % r.returncode, r.stdout.strip() or r.stderr.strip().splitlines()[4][:120])
    # (ii) original checkProof core, loaded by source text, CLI loop disabled
    js = ("const fs=require('fs');let s=fs.readFileSync('experiments/arc/lspv2_386_independent_verify.js','utf8');"
          "s=s.slice(0,s.indexOf('function corrupt'));eval(s+';globalThis.CP=checkProof;');"
          "console.log(JSON.stringify(CP(JSON.parse(fs.readFileSync(process.argv[1])))))")
    r2 = subprocess.run(["node", "-e", js, path], capture_output=True, text=True)
    print("CORE rc=%d" % r2.returncode, (r2.stdout or r2.stderr).strip()[:300])
    if path == OUT29: rc = r.returncode
sys.exit(rc)
