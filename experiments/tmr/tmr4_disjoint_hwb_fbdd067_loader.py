#!/usr/bin/env python3
"""TMR-4/067: integrity-checked loader of the actually executed CPython source."""
import base64
import hashlib
import zlib
from pathlib import Path

f = Path(__file__).with_name("tmr4_disjoint_hwb_fbdd067.py.zlib.b64")
source = zlib.decompress(base64.b64decode(f.read_text(encoding="ascii")))
expected = "6a519a9b4e81377fc00f52fd6b402818e48b1f3181b9abed2474efd01f5ef2b8"
if hashlib.sha256(source).hexdigest() != expected:
    raise RuntimeError("TMR-4/067 executable digest mismatch")
exec(compile(source, "tmr4_composed_fbdd067.py", "exec"), {"__name__": "__main__"})
