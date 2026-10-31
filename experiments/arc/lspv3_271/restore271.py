#!/usr/bin/env python3
"""Restore complete deterministic ARC271 raw results for independent verification."""
from pathlib import Path
import hashlib,gzip,base64
root=Path(__file__).resolve().parent
encoded=(root/'raw271.json.gz.b64').read_text().strip()
raw=gzip.decompress(base64.b64decode(encoded))
assert hashlib.sha256(raw).hexdigest()=="79bfb830e3a18f99bbaf6d5489b7924882e7aaa244f50726db23f0cf837783bd"
(root/'raw271.json').write_bytes(raw)
print('Restored raw271.json:',len(raw),'bytes; SHA-256 verified')
