#!/usr/bin/env python3
"""Exact arithmetic only. No SAT-transition construction is asserted."""
import json, signal, time
from fractions import Fraction as F
from pathlib import Path
signal.alarm(25)
start=time.monotonic()
c=F(1201,1000)
d=((c+2)/c**2-c)/2
assert c>F(6,5) and d>F(1,2)
checks=2
records=[]
for lam in (F(1,4),F(1,2),F(3,4)):
    for floor in (F(1),F(11,10),F(6,5)):
        b=(floor-1)*(1-lam)
        for initial in (F(2),F(10),F(100)):
            t=initial
            j=0
            while t>=c:
                j+=1
                t=1+lam*(t-1)+b
                assert t==floor+lam**j*(initial-floor)
                checks+=1
                assert j<1000
            records.append({'lambda':str(lam),'floor':str(floor),'initial':str(initial),'first_crossing':j})
# Equality of the limiting floor with the boundary does not yield finite entry.
t=F(10);lam=F(1,2);b=(c-1)*(1-lam)
for _ in range(100):
    t=1+lam*(t-1)+b
    assert t>c
    checks+=1
# Certified paid-prefix map is the identity above its floors.
for t in (F(2),F(10),F(100)):
    for s in (F(1),F(2),F(10)):
        assert (max(t,F(3,2)),max(s,F(1,2)))==(t,s)
        checks+=1
out={'status':'COMPUTATIONAL arithmetic audit only','checks':checks,'c':str(c),'d':str(d),'space_margin':str(d-F(1,2)),'runs':records,'elapsed_seconds':time.monotonic()-start,'sat_transition_constructed':False}
path=Path(__file__).with_name('arc_strengthen1_results.json')
path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='runs'}))
