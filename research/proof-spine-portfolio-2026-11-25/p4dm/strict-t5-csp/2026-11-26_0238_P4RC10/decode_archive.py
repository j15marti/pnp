"""Reconstruct exact new RC10 scripts. Inherited helpers and raw results are in the evidence ZIP."""
import base64, gzip, hashlib, json
from pathlib import Path
p = Path(__file__).resolve().parent
b = base64.b64decode("".join((p / f"archive.part{i}.b64").read_text().strip() for i in range(1,5)), validate=True)
assert hashlib.sha256(b).hexdigest() == "0c29db3413bfe8ee4ce29b3dc74d90e8b118d99765bc6dff3cfad146970be51d"
d = json.loads(gzip.decompress(b))
assert len(d) == 8
for name, content in d.items():
    assert Path(name).name == name and name.endswith("10.py")
    out = p / name
    data = content.encode()
    if out.exists() and out.read_bytes() != data:
        raise RuntimeError(f"Refusing to overwrite {out}")
    out.write_bytes(data)
    print(name, hashlib.sha256(data).hexdigest())
print("Compare individual hashes with results-summary.json; copy inherited helpers from the full evidence ZIP.")
