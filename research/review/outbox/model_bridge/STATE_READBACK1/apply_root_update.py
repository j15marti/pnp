#!/usr/bin/env python3
"""Insert the exact reviewed addition only inside LSPV-4's owned root region.
Run in a freshly fetched checkout. This script does not publish remotely.
"""
import argparse
import hashlib
import signal
from pathlib import Path
signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('25-second budget')))
signal.alarm(25)
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('checkout',type=Path)
p.add_argument('--apply',action='store_true',help='replace local root main.tex; otherwise write an outbox candidate')
a=p.parse_args()
root=a.checkout/'main.tex'
body=root.read_bytes().decode('utf-8')
start='% BEGIN LSPV-4 OWNED'; end='% END LSPV-4 OWNED'
if body.count(start)!=1 or body.count(end)!=1:
    raise SystemExit('Missing or nonunique ownership markers; no changes made.')
i=body.index(start); j=body.index(end)
if not i<j: raise SystemExit('Reversed ownership markers; no changes made.')
addition=Path(__file__).with_name('root_addition.tex').read_text()
marker='% BEGIN LSPV4 STATE_READBACK1 ADDITION'
if marker in body:
    raise SystemExit('STATE_READBACK1 addition already present; no duplicate inserted.')
updated=body[:j]+addition+'\n'+body[j:]
newj=updated.index(end)
assert body[:i]==updated[:i] and body[j:]==updated[newj:]
assert updated.count(start)==updated.count(end)==1
out=root if a.apply else a.checkout/'research'/'outbox'/'STATE_READBACK1'/'root_main_after.tex'
out.parent.mkdir(parents=True,exist_ok=True)
out.write_bytes(updated.encode('utf-8'))
def blob(text):
    b=text.encode();return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
print('Base Git blob:',blob(body))
print('Candidate Git blob:',blob(updated))
print('Outside LSPV-4 region: byte-identical UTF-8')
print('Output:',out)
print('Refetch current remote SHA immediately before publication; merge if changed.')
signal.alarm(0)
