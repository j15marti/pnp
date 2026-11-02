#!/usr/bin/env python3
"""Exact rational numerical check only, not SAT-to-canonical FLMV transport."""
from fractions import Fraction as Q
import json
def envelope(c):
    assert c>1 and c*(c-1)<1
    f=Q(1);best=Q(-1);k=0;w=[]
    while True:
        k+=1;f=c*f/(1+f)
        v=min((1/f-c)/k,c**(-k))
        if v>best:best=v;w=[k]
        elif v==best:w.append(k)
        if c**(-k-1)<best:
            return {'c':str(c),'d_star':str(best),'best_k':w,
                    'evaluated_through_k':k,'strict_tail_cap':str(c**(-k-1))}
        assert k<100
a,b=envelope(Q(6,5)),envelope(Q(241,200))
assert a['d_star']=='23/45' and b['d_star']=='11642479/23232400'
print(json.dumps({'status':'known FLMV numerical region, no same-machine target reduction',
'points':[a,b],'positive_space_slack':str(Q(11642479,23232400)-Q(1,2))},indent=2))
