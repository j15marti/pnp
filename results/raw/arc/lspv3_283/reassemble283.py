#!/usr/bin/env python3
"""Reconstruct exact GATE283 indexed raw JSON from seven verified GitHub text segments."""
from pathlib import Path
import base64
import gzip
import hashlib

ROOT = Path(__file__).resolve().parent
PARTS = [ROOT / f'raw283.json.gz.b64.part{i:02d}' for i in range(7)]
EXPECTED_SHA256 = '1335ce08289c101208d3fca92f4a2aa48df9f0e37a32891a7203392dbcc06cae'


def main():
    for p in PARTS:
        if not p.is_file():
            raise FileNotFoundError(p)
    payload = ''.join(p.read_text(encoding='ascii').strip() for p in PARTS)
    data = gzip.decompress(base64.b64decode(payload, validate=True))
    observed = hashlib.sha256(data).hexdigest()
    if observed != EXPECTED_SHA256:
        raise ValueError(f'Raw checksum mismatch: {observed}')
    outfile = ROOT / 'raw283.json'
    outfile.write_bytes(data)
    print(f'PASS GATE283 complete original indexed raw: {len(data)} bytes; SHA-256 {observed}')
    return outfile


if __name__ == '__main__':
    main()
