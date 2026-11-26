"""Reconstruct the exact locally executed P4RC06 evidence; run from this directory."""
import base64, gzip, hashlib, json
from pathlib import Path
root=Path(__file__).resolve().parent
parts=[(root/f"archive.part{i}.b64").read_text().strip() for i in range(1,4)]
blob=base64.b64decode("".join(parts),validate=True)
assert hashlib.sha256(blob).hexdigest()=="83de2e90c9f29d8e88b838e1df9d13e369b4d577893c2468e36bd7ca6842d9ae"
data=json.loads(gzip.decompress(blob))
hashes=json.loads((root/"results-summary.json").read_text())["file_sha256"]
assert set(data)==set(hashes)
for name,s in data.items():
    raw=s.encode("utf-8")
    assert hashlib.sha256(raw).hexdigest()==hashes[name],name
    p=root/name
    if p.exists() and p.read_bytes()!=raw:
        raise RuntimeError(f"Refusing to overwrite {p}")
    p.write_bytes(raw)
print("Verified",len(data),"exact evidence files")
# With NetworkX 3.6.1: python audit.py; python supplement.py; python common_final.py
# common.py preserves the preliminary attempt which timed out at D8.
