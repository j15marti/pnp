#!/usr/bin/env python3
"""Reproduce TMR-2/081 using the verified, lossless standard-library source."""
import base64
import gzip
import hashlib
from pathlib import Path

ARCHIVE = Path(__file__).with_suffix(".py.gz.b64")
EXPECTED = "eced239cdaf688fa4941af8d091365f0db6a983a71c7b4cdde1498b4a75d9945"
data = gzip.decompress(base64.b64decode(ARCHIVE.read_text().strip()))
if hashlib.sha256(data).hexdigest() != EXPECTED:
    raise RuntimeError("TMR-2/081 source SHA256 mismatch")
exec(compile(data.decode("utf-8"), str(ARCHIVE) + "::decoded.py", "exec"),
     {"__name__": "__main__", "__file__": str(ARCHIVE) + "::decoded.py"})
