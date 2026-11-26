"""Verify and unpack the RC11 executed source and raw results.
Place the five base64 parts and summary.json next to this script.
For reproduction use the inherited helpers from RC10 evidence ZIP,
NetworkX 3.6.1, PYTHONHASHSEED=0, then run rc11.py, rank11.py,
scale11.py, extra11.py, rescue11.py in that order.
"""
import base64, gzip, hashlib, json
from pathlib import Path
p = Path(__file__).resolve().parent
s = json.loads((p / "summary.json").read_text())
blob = base64.b64decode("".join((p / f"archive.part{i}.b64").read_text().strip() for i in range(1,6)), validate=True)
assert hashlib.sha256(blob).hexdigest() == s["archive_sha256"]
D = json.loads(gzip.decompress(blob))
assert set(D) == set(s["hashes"])
for name, value in D.items():
    data = value.encode("utf-8")
    assert hashlib.sha256(data).hexdigest() == s["hashes"][name], name
    f = p / name
    if f.exists() and f.read_bytes() != data:
        raise FileExistsError(f)
    f.write_bytes(data)
print("Verified and unpacked", len(D), "files.")
