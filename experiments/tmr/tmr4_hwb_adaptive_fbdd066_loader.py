#!/usr/bin/env python3
"""Authenticated loader of the exact CPython source for TMR-4/066."""
import base64
import hashlib
from pathlib import Path
import zlib

p = Path(__file__).with_name('tmr4_hwb_adaptive_fbdd066.py.zlib.b64')
source = zlib.decompress(base64.b64decode(p.read_text('ascii').strip()))
expected = 'b8637e823a65fa5772ef2f8d1f6e928c0f1f9c3e52750722a84a6ec23b0f8d1f'
if hashlib.sha256(source).hexdigest() != expected:
    raise RuntimeError('Authenticated source digest mismatch')
exec(compile(source, 'tmr4_hwb_adaptive_fbdd066.py', 'exec'), {'__name__': '__main__'})
