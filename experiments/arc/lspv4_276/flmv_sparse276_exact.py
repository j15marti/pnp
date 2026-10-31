#!/usr/bin/env python3
"""Exact rational audit of the FLMV Theorem 5.7 envelope for 1<c<phi."""
from fractions import Fraction as Q
import json
def audit(c):
    assert Q(1)<c and c*(c-1)<1
    f=Q(1);k=0;best=None;winner=None;rows=[]
    while True:
        k+=1;f=c*f/(1+f)
        cap=1/(c**k)
        level=min((1/f-c)/k,cap)
        rows.append({'k':k,'f':str(f),'uncapped':str((1/f-c)/k),'cap':str(cap),'d_k':str(level)})
        if best is None or level>best:best=level;winner=k
        tailcap=1/c**(k+1)
        if best>0 and tailcap<best:break
        assert k<250
    assert all(Q(r['d_k'])<=best for r in rows)
    return {'c':str(c),'k_star':winner,'d_star':str(best),'d_decimal':float(best),'evaluated_k':k,'tail_from_k':k+1,'tail_upper':str(tailcap),'strict_tail_exclusion':tailcap<best,'sampled':rows}
if __name__=='__main__':
    cs=[Q(6,5),Q(241,200),Q(301,250)]
    r=[audit(c) for c in cs]
    assert Q(r[0]['d_star'])==Q(23,45)
    assert Q(r[1]['d_star'])==Q(11642479,23232400)
    assert Q(r[0]['d_star'])>Q(1,2)
    assert Q(r[1]['d_star'])>Q(1,2)
    print(json.dumps({'reference':'FLMV Theorem 5.7 (JACM 2005), exact rational evaluation',
    'model':'same deterministic indexed-input random-access TM; n^c time and o(n^d) space exclusion',
    'points':r,'ARC_conditional':{'Kstar':'6/5','Lstar':'1/2','test_c':'241/200',
    'test_d':str(Q(11642479,23232400)),'time_exponent_slack':str(Q(241,200)-Q(6,5)),
    'space_exponent_slack':str(Q(11642479,23232400)-Q(1,2)),'strictly_inside':True,
    'compiler_constructed':False}},indent=2))
