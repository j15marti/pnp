#!/usr/bin/env python3
"""Exact UNKNOWN-domain embedding tests. Reuses authenticated prior sources."""
import contextlib, hashlib, io, itertools, json, runpy, signal, time
from pathlib import Path
signal.alarm(25)
start=time.monotonic(); here=Path(__file__).parent
with contextlib.redirect_stdout(io.StringIO()):
    ns=runpy.run_path(str(here/'2026-10-08_2110_ARC-STRENGTHEN2-test.py'))
signal.alarm(max(1,24-int(time.monotonic()-start)))
old=ns['old']; parity=ns['parity']; scan=ns['scan_star']
def embed(f,n):
    h,r,a,b,c,d=range(n+1,n+7)
    return f+((h,r),)+parity((h,a,b),0)+parity((h,c,d),0)+tuple((h,v,n+6+v) for v in range(1,n+1))
def covered(f):
    a,_=scan(f)
    return a is not None or old.run_portfolio(f)[0] is not None
# Exact image of all 256 formulas on one triple, including empty and UNSAT.
clauses=parity((1,2,3),0)+parity((1,2,3),1)
truth_counts={'SAT':0,'UNSAT':0}; max_ratio=0
for mask in range(256):
    f=tuple(c for j,c in enumerate(clauses) if mask>>j&1)
    g=embed(f,3)
    assert not covered(g)
    # Full independent assignment enumeration on the 12-variable image.
    tf=old.brute_sat(f);tg=old.brute_sat(g)
    assert tf==tg
    truth_counts['SAT' if tf else 'UNSAT']+=1
# Minimality within normalized proper width-three CNFs by variable count,
# then clause count: n<=3 always has a strong Horn backdoor of size <=2.
# Exhaust all 32 single clauses and 496 distinct pairs at n=4.
all4=tuple(tuple(v if bit else -v for v,bit in zip(s,bs))
           for s in itertools.combinations(range(1,5),3)
           for bs in itertools.product((False,True),repeat=3))
lower_checks=0
for k in (0,1,2):
    for f in itertools.combinations(all4,k):
        assert covered(f)
        lower_checks+=1
witness=((1,2,3),(1,2,4),(1,3,4))
assert not covered(witness) and old.brute_sat(witness)
# Source semantics survives every assignment, not only the final SAT bit.
extension_checks=0
for mask in range(256):
    f=tuple(c for j,c in enumerate(clauses) if mask>>j&1);g=embed(f,3)
    for bs in itertools.product((False,True),repeat=3):
        source=dict(zip(range(1,4),bs))
        # h,r,a,b,c,d = 4,5,6,7,8,9; w=10,11,12.
        ext=source|{4:True,5:True,6:True,7:False,8:True,9:False,10:False,11:False,12:False}
        assert old.evaluate(f,source)==old.evaluate(g,ext)
        extension_checks+=1
signal.alarm(0)
result={'status':'COMPUTATIONAL','passed':True,'seed':None,
 'source_commit':'5dc4147396c3969887b231a8d372c00ace23d58f',
 'embedding_cases':256,'truth_counts':truth_counts,'assignment_extension_checks':extension_checks,
 'minimality_lower_checks':lower_checks,'smallest_witness':witness,
 'minimality_scope':'proper exactly-width-three CNF; first variable count then clause count',
 'seconds':time.monotonic()-start,
 'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'source_sha256':{name:hashlib.sha256((here/name).read_bytes()).hexdigest() for name in
 ['2026-10-08_2110_ARC-STRENGTHEN2-test.py','2026-10-08_2110_ARC-STRENGTHEN2-original-portfolio.py']},
 'limitations':['Symbolic proofs establish infinite claims; tests only finite semantics.',
 'Python memory is not the claimed logspace transducer implementation.',
 'No intrinsic SAT lower bound or strict ARC transition established.']}
print(json.dumps(result,indent=2))
