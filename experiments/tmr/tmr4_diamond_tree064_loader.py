#!/usr/bin/env python3
"""Authenticate and execute TMR-4/064's exact audited Python source."""
import base64, hashlib, pathlib, zlib
HERE=pathlib.Path(__file__).resolve().parent
encoded=(HERE/'tmr4_diamond_tree064.py.zlib.b64').read_text(encoding='ascii').strip()
source=zlib.decompress(base64.b64decode(encoded,validate=True))
assert hashlib.sha256(source).hexdigest()=='2a4e9a29dd93864b50975c504fd516f8e082f81a08de25f62e596e70c6efd2bd', 'source integrity mismatch'
exec(compile(source,str(HERE/'tmr4_diamond_tree064.py'),'exec'),{'__name__':'__main__','__file__':str(HERE/'tmr4_diamond_tree064.py')})
