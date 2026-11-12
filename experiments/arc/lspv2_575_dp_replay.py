#!/usr/bin/env python3
"""LSPV-2/575 restricted DP-order generator; NOT the original proof checker."""
import collections, copy, hashlib, itertools, json, pathlib, subprocess, sys, tempfile
root=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else '.')
seed_path=root/'results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json'
checker=root/'experiments/arc/lspv2_386_independent_verify.js'
source=root/'results/raw/arc/574_k01_SIGNED_SOURCE.cnf'
seed=json.loads(seed_path.read_text()); sources=[r for r in seed['records'] if r['kind']=='SOURCE']
assert len(sources)==17 and len(seed['gate_defs'])==1
line=source.read_text().strip().splitlines()
assert line[0]=='p cnf 7 17' and len(line)==18
assert [list(map(int,s.split()))[:-1] for s in line[1:]]==[r['c'] for r in sources]
sha=lambda b: hashlib.sha256(b).hexdigest()
git=lambda b: hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
assert git(checker.read_bytes())=='338305c0ce101704205e57543756b8127074a986'
canon=lambda c: tuple(sorted(set(c),key=lambda x:(abs(x),x)))
def proof(order):
    facts={tuple(r['c']):None for r in sources}; active=set(facts)
    for p in order:
        pos=sorted(c for c in active if p in c); neg=sorted(c for c in active if -p in c)
        nxt={c for c in active if p not in c and -p not in c}
        for a in pos:
            for b in neg:
                c=canon([x for x in a if x!=p]+[x for x in b if x!=-p])
                if not any(-x in c for x in c):
                    facts.setdefault(c,(a,b,p)); nxt.add(c)
        active=nxt
    assert () in facts
    idx={tuple(r['c']):i for i,r in enumerate(sources)}; derived=[]
    def visit(c):
        if c in idx:return
        a,b,p=facts[c];visit(a);visit(b)
        idx[c]=17+len(derived)
        derived.append({'kind':'RES','c':list(c),'parents':[idx[a],idx[b]],'pivot':p})
    visit(())
    k=len(derived)
    return {'spec':seed['spec'],'gate_defs':seed['gate_defs'],
      'records':sources+derived,'summary':{'source':17,'def_views':0,
      'resolution':k,'paid_gates':1,'paid_total':k+1,'live_records':17+k}}
hist=collections.Counter();lo=(100,None);hi=(-1,None)
for order in itertools.permutations(range(1,8)):
    n=proof(order)['summary']['resolution'];hist[n]+=1
    if n<lo[0]:lo=(n,order)
    if n>hi[0]:hi=(n,order)
assert sum(hist.values())==5040
cases=[('minimum',proof(lo[1]),True),('maximum',proof(hi[1]),True)]
for name,mut in [('bad_cost',lambda d:d['summary'].__setitem__('paid_total',0)),
 ('bad_source',lambda d:d['records'][0]['c'].__setitem__(0,-1)),
 ('bad_kind',lambda d:d['records'][-1].__setitem__('kind','AND3')),
 ('bad_parent',lambda d:d['records'][-1]['parents'].__setitem__(0,len(d['records'])))]:
 d=copy.deepcopy(cases[0][1]);mut(d);cases.append((name,d,False))
raw=[]
with tempfile.TemporaryDirectory() as temp:
 for name,d,want in cases:
    b=(json.dumps(d,separators=(',',':'))+'\n').encode()
    p=pathlib.Path(temp)/(name+'.json');p.write_bytes(b)
    out=subprocess.run(['node',str(checker),str(p)],capture_output=True,text=True,timeout=10)
    ok=out.returncode==0
    assert ok==want,(name,out.stdout,out.stderr)
    raw.append({'case':name,'accepted':ok,'work':d['summary']['paid_total'],'bytes':len(b),'sha256':sha(b),'native_assertions':json.loads(out.stdout)['assertions'] if ok else None,'error':out.stderr.strip()[:120] if not ok else None})
result={'id':'LSPV2_575_NATIVE386_DP_ORDER_PYTHON_INDEPENDENT','checker_git_blob':git(checker.read_bytes()),'source_sha256':sha(source.read_bytes()),'seed_git_blob':git(seed_path.read_bytes()),'orders':5040,'histogram':dict(sorted(hist.items())),'min_order':lo[1],'max_order':hi[1],'min_resolution':lo[0],'max_resolution':hi[0],'cases':raw,'status':'COMPUTATIONAL, restricted deterministic first-witness DP scheduling only; full R_mix341 OPEN'}
output=pathlib.Path(sys.argv[2] if len(sys.argv)>2 else '/mnt/data/pnp575/575_python_compact.json');output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'hist':result['histogram'],'min':lo,'max':hi,'cases':len(cases),'accepts':sum(x['accepted'] for x in raw),'sha256':sha(output.read_bytes())}))
