"""Reconstruct and check RC08 executed code. Copy audit.py and prior.py from RC07's decoded archive. Requires Python and networkx."""
import base64,gzip,json,hashlib
from pathlib import Path
p=Path(__file__).resolve().parent
b=base64.b64decode(''.join((p/f'code.part{i}.b64').read_text().strip() for i in range(1,5)),validate=True)
assert hashlib.sha256(b).hexdigest()=='24e37df88f28aad070815911d963bb1cc99bd2204e11b008d98a32fcd83728c3'
data=json.loads(gzip.decompress(b))
h=json.loads((p/'results-summary.json').read_text())['file_sha256']
assert set(data)=={'consensus.py','check.py','quad_bench.py','mesh_control.py','flow_lane.py','matching_check.py'}
for name,s in data.items():
    raw=s.encode('utf-8')
    assert hashlib.sha256(raw).hexdigest()==h[name],name
    (p/name).write_bytes(raw)
for name in ('audit.py','prior.py'):
    if (p/name).exists():
        assert hashlib.sha256((p/name).read_bytes()).hexdigest()==h[name],name
    else:
        print('Required RC07 dependency:',name)
print('Verified six RC08 source files.')
