#!/usr/bin/env python3
"""TMR-4/063: authentic reconvergent-core span certificate and path audit.
Requires sibling tmr4_live_core062.py; semantic compiler remains unchanged.
Source revision tmr4-reconvergent-span063.v2; finite evidence COMPUTATIONAL.
"""
import hashlib, itertools, json, random
from collections import defaultdict
from pathlib import Path
import tmr4_live_core062 as core
SEED=202611152244
R=random.Random(SEED)
REVISION='tmr4-reconvergent-span063.v2'

def source(kind,m,ops=(8,6,14)):
    gates=[]
    def gate(a,b,op):
        v='g'+str(len(gates))
        gates.append(dict(id=v,a=a,b=b,op=op))
        return v
    if kind=='ladder':
        n=m+1;a=['x0']
        for i in range(1,m+1):
            p=gate(a[-1],f'x{i}',ops[0]);q=gate(a[-2] if i>1 else a[0],f'x{i}',ops[1])
            a.append(gate(p,q,ops[2]))
        root=a[-1]
    elif kind=='far':
        n=m+2; root='x1'
        for i in range(2,m+2):
            p=gate(root,f'x{i}',8);q=gate(root,'x0',6);root=gate(p,q,14)
    elif kind=='disj':
        n=2*m; leaf=[gate(f'x{i}',f'x{i+m}',7) for i in range(m)]
        root=leaf[0]
        for v in leaf[1:]:root=gate(root,v,8)
    else:raise AssertionError(kind)
    R.shuffle(gates)
    return json.dumps(dict(version=1,n=n,gates=gates,root=root),sort_keys=True,separators=(',',':')).encode('ascii')

def certify(c):
    order=c['core_order'] if 'core_order' in c else c['order']
    deps=c['dependencies'] if 'dependencies' in c else c['deps']
    pos={v:i for i,v in enumerate(order)}
    assert len(pos)==len(order) and order[-1]==c['root']
    cons=defaultdict(set)
    for t in order:
        for v in deps[t]:
            assert pos[v]<pos[t]
            cons[v].add(t)
    spans={v:max(pos[t] for t in cons[v])-pos[v] for v in c['shared']}
    delta=max(spans.values(),default=0)
    active=[]
    for i,t in enumerate(order):
        s={v for v in c['shared'] if pos[v]<=i<max(pos[u] for u in cons[v])}
        if 'frontier' in c and t==c['root']:s.add(t)
        active.append(s)
    q=max(map(len,active))
    if 'frontier' in c:assert active==[set(v) for v in c['frontier']]
    assert q==c['q'] and q<=delta+1
    return dict(delta=delta,q=q,k=len(c['shared']),K=len(order),
                reconvergent=sum(len(cons[v])>1 for v in c['shared']),
                max_consumers=max((len(cons[v]) for v in c['shared']),default=0))

def direct(c,bits):
    val={f'x{i}':bits[i] for i in range(c['n'])};remain=dict(c['gates'])
    while remain:
        ready=[v for v,e in remain.items() if e['a'] in val and e['b'] in val]
        assert ready
        for v in ready:
            e=remain.pop(v)
            val[v]=(e['op']>>(2*val[e['a']]+val[e['b']]))&1
    return val[c['root']]

def audit():
    cases=[];assignments=0;checks=0
    suite=[('ladder',m,(8,6,14)) for m in (3,4,5,6,7,8,10,12,16,32,64,128)]
    suite += [('far',m,(8,6,14)) for m in (4,6,8,12,24,48)]
    suite += [('disj',m,(8,6,14)) for m in (1,2,3,4)]
    suite += [('ladder',R.randrange(3,7),tuple(R.randrange(16) for _ in range(3))) for _ in range(24)]
    for kind,m,ops in suite:
        src=source(kind,m,ops);c=core.compile_source(src);s=certify(c)
        b=core.build_obdd(c)
        assert b['nodes']<=c['n']*(1<<c.get('bound',c.get('w_bound')))
        checks+=1
        if c['n']<=11:
            read=[c['instructions'][i][1] for i in c['reads']];yes=0
            for mask in range(1<<c['n']):
                bits=tuple((mask>>i)&1 for i in range(c['n']))
                answer=direct(c,bits);yes+=answer;v=()
                for j,idx in enumerate(read):v=b['edges'][j][(v,bits[idx])]
                got=v[1] if isinstance(v,tuple) and v[0]=='HALT' else v
                assert got==answer
                assignments+=1;checks+=2
            assert yes==b['count'];checks+=1
        if kind=='ladder' and ops==(8,6,14):
            assert s['delta']<=5
            if m>=4:assert s['reconvergent']>0
            checks+=2
        cases.append(dict(family=kind,m=m,n=c['n'],g=len(c['gates']),nodes=b['nodes'],
            count=str(b['count']),source_sha256=hashlib.sha256(src).hexdigest(),**s))
    assert any(x['delta']>10 and x['q']<=5 for x in cases if x['family']=='far')
    out=dict(revision=REVISION,seed=SEED,imported_revision=core.REVISION,cases=len(cases),
             assignments=assignments,assertions=checks,failures=0,
             source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             samples=[cases[i] for i in (0,2,5,8,10,11,12,16,18,21,22,45)])
    print(json.dumps(out,sort_keys=True,separators=(',',':')))
if __name__=='__main__':audit()
