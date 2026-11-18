#!/usr/bin/env python3
"""Reproducible launcher for TMR-2/080's immutable executed Python source.

Usage:
python3 experiments/tmr/tmr2_t5_bucket080.py \
  research/agents/tmr-2/certificates/2026-11-18_0112_TMR2_T5_GIRTH8_33_NO079.t5 \
  /tmp/tmr2_bucket080.json

The complete original readable source is embedded losslessly in the adjacent
tmr2_t5_bucket080.py.gz.b64 archive. Only standard-library modules are used.
The source hash is verified before execution. Extraction instead of execution:
python3 -c 'import base64,gzip,pathlib; p=pathlib.Path("experiments/tmr/tmr2_t5_bucket080.py.gz.b64"); pathlib.Path("tmr2_bucket080_extracted.py").write_bytes(gzip.decompress(base64.b64decode(p.read_bytes())))'
"""
import base64
import gzip
import hashlib
from pathlib import Path

ORIGINAL_SHA256="51fe1e2b837f97cae6e6ec40f69874398d7f7ec9b64e41e054ab4a14393abc96"
archive=Path(__file__).with_name("tmr2_t5_bucket080.py.gz.b64")
source=gzip.decompress(base64.b64decode(archive.read_bytes()))
actual=hashlib.sha256(source).hexdigest()
if actual!=ORIGINAL_SHA256:
    raise RuntimeError(f"Immutable executed source digest mismatch: {actual}")
exec(compile(source, str(archive), "exec"), {"__name__":"__main__", "__file__":str(archive)})
