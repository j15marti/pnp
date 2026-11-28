import hashlib,itertools,json,sys
from pathlib import Path

def encode(x): return (json.dumps(x,separators=(',',':'))+'\n').encode()
def h(b): return hashlib.sha256(b).hexdigest()
def check(src,cert):
    assert h(src)==cert['instance_id'].split(':')[-1]
    assert 8*len(src)==cert['original_N_bits']
    rows={i:tuple(map(int,c.split()[:-1])) for i,c in enumerate(src.decode().splitlines()[1:],1)}
    a={v:bool(b) for v,b in cert['guard']}
    gid='GUARD-v1:sha256:'+h(encode(['PNP-GUARD-v1',cert['instance_id'],'CNF-VAR-PINS-v1',h(encode(cert['guard']))]))
    assert gid==cert['guard_id']
    while True:
        db={i:tuple(sorted(set(l for l in c if abs(l) not in a),key=lambda l:(abs(l),l))) for i,c in rows.items() if not any(a.get(abs(l))==(l>0) for l in c)}
        assert all(db.values())
        units={c[0] for c in db.values() if len(c)==1}
        assert not any(-l in units for l in units)
        if not units: break
        a.update({abs(l):l>0 for l in units})
    assert h(encode([[i,list(c)] for i,c in db.items()]))==cert['residual_sha256']
    total=set();words=0
    for g in cert['generators']:
        scope=g['scope']; parents=[db[i] for i in g['parents']];poly=[tuple(m) for m in g['p']]
        assert all(abs(l) in scope for c in parents for l in c)
        assert all(set(m)<=set(scope) and len(set(m))==len(m) and len(m)<=2 for m in poly)
        for b in itertools.product((0,1),repeat=len(scope)):
            z=dict(zip(scope,b));words+=1
            if all(any(z[abs(l)]==(l>0) for l in c) for c in parents):
                assert sum(all(z[x] for x in m) for m in poly)%2==0
        for m in poly: total.symmetric_difference_update([m])
    assert total=={()}
    return words,a

if __name__=='__main__':
    src=Path(sys.argv[1]).read_bytes();cert=Path(sys.argv[2]).read_bytes();obj=json.loads(cert)
    print('certificate',h(cert),'verified',check(src,obj))
    bad=json.loads(cert);bad['generators'].pop()
    try: check(src,bad)
    except AssertionError: print('negative control: omitted generator rejected')
    else: raise AssertionError('corrupted certificate accepted')
