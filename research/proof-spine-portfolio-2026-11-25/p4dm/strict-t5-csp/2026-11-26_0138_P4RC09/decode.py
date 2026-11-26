"""Decode exact executed P4RC09 new code archive; verify hashes first.
The full conversation ZIP also contains five inherited helpers and 22 raw result files.
Copy these helpers from that ZIP or the earlier RC08/RC07/RC06 archives.
Run with NetworkX 3.6.1 and NumPy.
"""
from pathlib import Path
import base64, gzip, hashlib, json
root=Path(__file__).resolve().parent
blob=base64.b64decode("".join((root/f"archive.part{i}.b64").read_text().strip() for i in range(1,4)),validate=True)
assert hashlib.sha256(blob).hexdigest()=="011ea6d440b1ad96dcfb5074b5358ad1b7efae514f41896b4cc127a53a81ee39"
files=json.loads(gzip.decompress(blob))
ledger=json.loads((root/"hash-ledger.json").read_text())
assert set(files)==set(ledger["code_sha256"])
for name, source in files.items():
    raw=source.encode("utf-8")
    assert hashlib.sha256(raw).hexdigest()==ledger["code_sha256"][name],name
    p=root/name
    if p.exists() and p.read_bytes()!=raw:raise RuntimeError(f"Refusing to overwrite {p}")
    p.write_bytes(raw)
for group in ("dependency_sha256","raw_sha256"):
    for name,digest in ledger[group].items():
        p=root/name
        if p.exists():assert hashlib.sha256(p.read_bytes()).hexdigest()==digest,name
print("Verified and decoded",len(files),"new code files; present helpers/results checked.")
