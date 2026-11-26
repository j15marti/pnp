"""Decode the exact executed P4RC07 evidence. Standard library only.

From the repository checkout: python decode.py
Or supply the verified RC06 audit.py: python decode.py /path/to/RC06/audit.py
Then with NetworkX 3.6.1: python audit.py; python supplement.py
Preserve original results separately before rerunning (library tie choices may differ).
"""
import base64
import gzip
import hashlib
import json
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
hashes = json.loads((root / "results-summary.json").read_text())["file_sha256"]

def archive(directory, stem, count, expected):
    blob = base64.b64decode("".join((directory / f"{stem}.part{i}.b64").read_text().strip()
                                     for i in range(1, count + 1)), validate=True)
    assert hashlib.sha256(blob).hexdigest() == expected, stem
    return gzip.decompress(blob)

data = json.loads(archive(root, "code", 3,
    "0372b50e59efe41a8cd9f77c67beb6ae354f7632f79b2d65ccbc8c88a9c4500d"))
data["results.json"] = archive(root, "raw", 2,
    "60565e6c6b2f1bb879d1389b9cf43ee5c559d2a643b37389d48a490180cd11d4").decode()
if len(sys.argv) > 1:
    data["prior.py"] = Path(sys.argv[1]).read_bytes().decode()
else:
    prev = root.parent / "2026-11-25_2310_P4RC06"
    prior = json.loads(archive(prev, "archive", 3,
        "83de2e90c9f29d8e88b838e1df9d13e369b4d577893c2468e36bd7ca6842d9ae"))
    data["prior.py"] = prior["audit.py"]
assert set(data) == set(hashes)
for name, content in data.items():
    raw = content.encode("utf-8")
    assert hashlib.sha256(raw).hexdigest() == hashes[name], name
    path = root / name
    if path.exists() and path.read_bytes() != raw:
        raise RuntimeError(f"Refusing to overwrite {path}")
    path.write_bytes(raw)
print("Verified and decoded", len(data), "exact evidence files")
