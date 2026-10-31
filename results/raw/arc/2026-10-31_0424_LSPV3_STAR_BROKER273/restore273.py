#!/usr/bin/env python3
"""Restore the exact original-source ARC273 JSON from numbered GitHub chunks."""
from pathlib import Path
import json, base64, gzip, hashlib, sys

here = Path(__file__).resolve().parent
meta = json.loads((here / "manifest273.json").read_text())
joined = "".join("".join((here / name).read_text().split())
                 for name in meta["chunk_files"])
encoded = joined.encode("ascii")
assert hashlib.sha256(encoded).hexdigest() == meta["base64_sha256"], "Base64 mismatch"
payload = base64.b64decode(encoded, validate=True)
assert len(payload) == meta["gzip_bytes"]
assert hashlib.sha256(payload).hexdigest() == meta["gzip_sha256"], "Compressed mismatch"
raw = gzip.decompress(payload)
assert len(raw) == meta["raw_bytes"]
assert hashlib.sha256(raw).hexdigest() == meta["raw_sha256"], "Raw mismatch"
out = Path(sys.argv[1]) if len(sys.argv) > 1 else here / "raw273.json"
out.write_bytes(raw)
print("PASS", out, len(raw), meta["raw_sha256"])
