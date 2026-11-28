"""Check LPD1 against exact guarded rows. Source/guard reconstruction is separate."""
import argparse, base64, hashlib, json
from pathlib import Path

def verify(rows, payload):
    assert payload[:4] == b'LPD1'
    db = [frozenset(c) for _, c in rows]
    vs = sorted({abs(l) for c in db for l in c})
    pos = 4
    initial = len(db)
    edges = reads = 0
    def get():
        nonlocal pos
        x = 0
        for shift in range(0, 70, 7):
            assert pos < len(payload)
            b = payload[pos]; pos += 1
            x |= (b & 127) << shift
            if b < 128:
                assert x < 2**64 and (shift == 0 or b != 0)
                return x
        raise ValueError('overlong varint')
    n = get(); assert n <= len(payload)-pos
    for _ in range(n):
        w = get(); assert w <= len(vs) and w <= len(payload)-pos
        c = []
        for _ in range(w):
            a = get(); assert a//2 < len(vs)
            c.append((-1 if a & 1 else 1)*vs[a//2])
        C = frozenset(c)
        assert len(C) == w and not any(-l in C for l in C)
        h = get(); assert 1 <= h <= len(payload)-pos
        trail = {-l for l in C}
        for j in range(h):
            p = get(); assert p < len(db)
            r = db[p]; reads += len(r)+1; edges += 1
            assert not trail.intersection(r)
            free = r - {-l for l in trail}
            assert len(free) == (0 if j == h-1 else 1)
            if free: trail.update(free)
        db.append(C)
    end = get()
    assert pos == len(payload) and initial <= end < len(db) and not db[end]
    return n, edges, reads

def main():
    assert __debug__, 'Do not run with -O'
    p = argparse.ArgumentParser(); p.add_argument('residual'); p.add_argument('certificate'); a=p.parse_args()
    raw = Path(a.residual).read_bytes(); cert=json.loads(Path(a.certificate).read_bytes())
    assert hashlib.sha256(raw).hexdigest() == cert['residual_sha256']
    payload = base64.b64decode(cert['payload_base64'], validate=True)
    assert hashlib.sha256(payload).hexdigest() == cert['payload_sha256']
    n,e,r=verify(json.loads(raw), payload)
    assert (n,e)==(cert['logical_nodes'],cert['reference_edges'])
    print(json.dumps({'status':'UNSAT relative to exact guarded rows','nodes':n,'edges':e,'reads':r}))
if __name__ == '__main__': main()
