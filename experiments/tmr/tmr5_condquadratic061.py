#!/usr/bin/env python3
"""Reproducible TMR-5/061 reference runner.

The complete 12.8 KB readable Python source is preserved losslessly in
tmr5_condquadratic061_source.py.gz.b64. To inspect it, run:
    python experiments/tmr/tmr5_condquadratic061.py --extract > full_source.py
The payload is SHA-256 checked before extraction or execution. This runner
uses only Python standard-library modules, not an external oracle.
"""
import base64
import gzip
import hashlib
from pathlib import Path
import sys

PAYLOAD_SHA256 = "f587a607561e80df00529ddf2bdf0b66dc940571227a4a3dc398a800f297c4f1"
PAYLOAD = Path(__file__).with_name("tmr5_condquadratic061_source.py.gz.b64")
encoded = "".join(PAYLOAD.read_text(encoding="ascii").split())
full_source = gzip.decompress(base64.b64decode(encoded, validate=True))
if hashlib.sha256(full_source).hexdigest() != PAYLOAD_SHA256:
    raise SystemExit("TMR-5/061 source authentication failed")
if sys.argv[1:] == ["--extract"]:
    sys.stdout.buffer.write(full_source)
elif len(sys.argv) != 1:
    raise SystemExit("usage: python tmr5_condquadratic061.py [--extract]")
else:
    exec(compile(full_source, str(PAYLOAD) + ".expanded.py", "exec"),
         {"__name__": "__main__", "__file__": str(PAYLOAD) + ".expanded.py"})
