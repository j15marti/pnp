#!/usr/bin/env python3
"""Exact FLMV 5.7 envelope; run under timeout 25s. No random seed."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json,signal
signal.alarm(24)
def optimize(c):
    assert 1<c and c*(c-1)<1
    f=Q(1); best=Q(0); winner=None; rows=[]
    for k in range(1,10000):
        f=c*f/(1+f)
        closed=(c-1)/(1-(2-c)/c**k)
        assert f==closed
        if k<2: continue
        d=min((1/f-c)/k,1/c**k)
        if d>best:best,winner=d,k
        rows.append({'k':k,'f':str(f),'d':str(d)})
        # For every j>k, d_j <= c^-j <= c^-(k+1).
        if best>1/c**(k+1):
            return dict(c=str(c),k=winner,d=str(best),decimal=float(best),stop=k,tail=str(1/c**(k+1)),rows=rows)
    raise AssertionError('budget exhausted')
values=['1.1','1.2','1.205','1.3','1.4','1.5','1.55','1.6','1.61']
out=[optimize(Q(c)) for c in values]
for r in out:
    c=Q(r['c']); d=Q(r['d'])
    assert d>=((c+2)/c**2-c)/2
    for k in range(2,101):
        f=(c-1)/(1-(2-c)/c**k)
        assert min((1/f-c)/k,c**(-k))<=d
assert out[1]['d']=='23/45'
assert out[2]['d']=='11642479/23232400'
# High-time escape: for c>=2, f_k>=1 and (1/f_k-c)/k<0.
for c in (Q(2),Q(3),Q(10)):
    for k in range(2,20):
        f=(c-1)/(1-(2-c)/c**k)
        assert min((1/f-c)/k,c**(-k))<0
print(json.dumps({'status':'PASS','code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'method':'exact rational recurrence plus independent closed form and certified infinite tail','records':out},indent=2))
