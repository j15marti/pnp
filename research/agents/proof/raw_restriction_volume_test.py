#!/usr/bin/env python3
"""Exact batch-volume controls; raw restrictions, no propagation or pruning."""
import hashlib, itertools, json, random, signal, time
from pathlib import Path
signal.signal(signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError('25s')))
signal.alarm(25)
start=time.monotonic(); checks=0
def residual(formula, assignment):
    out=[]
    for clause in formula:
        if any(abs(l) in assignment and assignment[abs(l)]==(l>0) for l in clause):
            continue
        out.append(tuple(l for l in clause if abs(l) not in assignment))
    return tuple(out)
def verify(formula, variables):
    global checks
    t=len(variables); sizes=[]
    for values in itertools.product((False,True),repeat=t):
        f=residual(formula,dict(zip(variables,values)))
        sizes.append(sum(map(len,f)))
    predicted=sum((len(c)-len(set(map(abs,c))&set(variables)))*2**(t-len(set(map(abs,c))&set(variables))) for c in formula)
    assert sum(sizes)==predicted;checks+=1
    L=sum(map(len,formula)); labels=set(abs(l) for c in formula for l in c)
    d=max((sum(abs(l)==v for c in formula for l in c) for v in labels),default=0)
    assert 8*sum(sizes)>=2**t*(L-d*t);checks+=1
    assert 4*sum(sizes)>=2**t*(L-d*t);checks+=1
    assert sum(sizes)>=2**t*(L-3*d*t);checks+=1
    return dict(t=t,L=L,d=d,volume=sum(sizes),max_child_literals=max(sizes,default=0))
clauses=[c for w in range(4) for vs in itertools.combinations(range(1,6),w) for signs in itertools.product((-1,1),repeat=w) for c in [tuple(v*s for v,s in zip(vs,signs))]]
for c in clauses:
    for t in range(6):
        for X in itertools.combinations(range(1,6),t):verify((c,),X)
rng=random.Random(20261009)
for _ in range(400):
    formula=tuple(rng.choice(clauses) for _ in range(rng.randrange(1,16)))
    verify(formula,tuple(rng.sample(range(1,6),rng.randrange(6))))
# Easy independent-product positive clauses: volume is not a SAT lower bound.
rows=[]
for n in (12,24,48,96):
    f=tuple(tuple(range(i,i+3)) for i in range(1,n+1,3))
    row=verify(f,tuple(range(1,min(6,n)+1)))
    assert all(any(l>0 for l in c) for c in f)
    row['n']=n;row['direct_all_true_witness']=True;rows.append(row)
signal.alarm(0)
result=dict(status='PASS',checks=checks,seed=20261009,elapsed_seconds=time.monotonic()-start,
    source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),rows=rows,
    scope='Raw complete assignment batches only; no conflict pruning, duplicate removal, SAT calls, component factorization or unit closure. Literal counts are not encoded bit lengths or runtime lower bounds.')
Path(__file__).with_name('raw_restriction_volume_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
