#!/usr/bin/env python3
"""SHA-verified launcher for WRAPPER-SHIELD1's T5 edge-deletion cofactor audit.
Usage: python3 experiments/shield1/t5_critical_boundary_audit_20261119.py SOURCE.t5 OUTPUT.json
Requires Python 3 and NumPy; output contains full witnesses and counts.
"""
from pathlib import Path
import base64, gzip, hashlib, runpy, tempfile, sys
packed = Path(__file__).with_suffix('.py.gz.b64').read_text().strip()
source = gzip.decompress(base64.b64decode(packed))
expected = '216b9fc894dab5e9a886f3ddcb7b19b10b3503fa551e95aa55f5862742742534'
actual = hashlib.sha256(source).hexdigest()
if actual != expected:
    raise RuntimeError('Executed-source SHA256 mismatch')
with tempfile.TemporaryDirectory() as td:
    target = Path(td) / 't5_critical_boundary_audit.py'
    target.write_bytes(source)
    runpy.run_path(str(target), run_name='__main__')
