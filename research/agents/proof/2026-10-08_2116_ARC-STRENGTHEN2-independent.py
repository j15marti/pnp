"""Independent brute-force backdoor and hostile-domain validation; 25s cap."""
import itertools, json, runpy, signal, contextlib, io, time
from pathlib import Path
signal.alarm(25)
start=time.monotonic()
p=Path(__file__).parent
with contextlib.redirect_stdout(io.StringIO()):
    ns=runpy.run_path(str(p/'2026-10-08_2110_ARC-STRENGTHEN2-test.py'))
signal.alarm(25)
old=ns['old']; star=ns['star']; parity=ns['parity']; scan=ns['scan_star']
def minimum(f):
    vs=sorted({abs(v) for c in f for v in c})
    for k in range(len(vs)+1):
        for b in itertools.combinations(vs,k):
            if all(all(sum(v>0 for v in c)<=1 for c in old.restrict(f,dict(zip(b,a))))
                   for a in itertools.product((False,True),repeat=k)):
                return k
rows=[]
for m in (2,3):
    for bs in itertools.product((0,1),repeat=m):
        f=star(bs)
        sat_k=minimum(f)
        unsat_k=minimum(f+parity((1,2,3),1-bs[0]))
        assert sat_k==m+1 and unsat_k==3
        rows.append([m,list(bs),sat_k,unsat_k])
# Every subset of two overlapping triple blocks: semantic soundness even off-star.
clauses=parity((1,2,3),0)+parity((2,3,4),1)
checks=0
for mask in range(256):
    f=tuple(c for i,c in enumerate(clauses) if mask>>i&1)
    a,_=scan(f)
    if a is not None:
        assert a==old.brute_sat(f)
    checks+=1
signal.alarm(0)
print(json.dumps({'passed':True,'minimum_backdoor_cases':len(rows)*2,
 'off_domain_checks':checks,'rows':rows,'seconds':time.monotonic()-start,
 'claim':'Finite semantic validation; no asymptotic runtime certification'},indent=2))
