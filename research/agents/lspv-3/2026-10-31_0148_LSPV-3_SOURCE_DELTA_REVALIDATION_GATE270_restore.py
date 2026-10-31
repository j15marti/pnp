#!/usr/bin/env python3
"""Reconstitute the raw proof dataset from raw270.json.gz.b64."""
from pathlib import Path
import base64,gzip,hashlib
here=Path(__file__).resolve().parent
payload=base64.b64decode((here/'raw270.json.gz.b64').read_text())
raw=gzip.decompress(payload)
assert hashlib.sha256(raw).hexdigest()=='79348a72b3d28a35387177dcc91bb6c93f409cc755b5eea94e9c3ca5ad718946'
(here/'raw270.json').write_bytes(raw)
print('Restored',len(raw),'bytes SHA-256',hashlib.sha256(raw).hexdigest())
