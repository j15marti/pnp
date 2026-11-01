#!/usr/bin/env python3
"""Exact rational 2005 FLMV theorem 5.7 envelope (established theorem)."""
from fractions import Fraction as Q
from pathlib import Path
import json
P=Path(__file__).resolve().parent

def envelope(c):
    f=Q(1);v=[]; k=0
    while True:
        k+=1;f=c*f/(1+f)
        a=(1/f-c)/k;b=c**(-k);d=min(a,b)
        v.append({'k':k,'f_k':str(f),'d_k':str(d),'term1':str(a),'term2':str(b)})
        best=max(Q(r['d_k']) for r in v)
        # For every j>=k+1, d_j<=c^-j<=c^-(k+1)<best.
        if c**(-(k+1))<best and k>=3:break
    idx=[r['k'] for r in v if Q(r['d_k'])==best]
    assert idx==[2]
    assert Q(v[0]['d_k'])<best and Q(v[2]['d_k'])<best
    assert c**(-4)<best
    return {'c':str(c),'max_d':str(best),'best_k':idx,'visited':v,
       'tail_start_k':k+1,'tail_upper_bound':str(c**(-(k+1))),
       'tail_strict':c**(-(k+1))<best,'slack_above_half':str(best-Q(1,2)),
       'strict_c_inequality_6_5':c>Q(6,5)}

def main():
    result={'theorem':'FLMV Thm 5.7, NTIME[n] not subset DTISP[n^c,o(n^d)]',
    'points':[envelope(Q(6,5)),envelope(Q(241,200))],
    'target':'same deterministic indexed random-access machine, no automatic NP-completeness exponent transfer',
    'conditional_ARC_exponents':{'alpha':'11/10','gamma':'3/5','lambda':'1/2','sigma':'1/2',
        'Kstar':'6/5','Lstar':'1/2','scope':'UNCONSTRUCTED'} }
    assert result['points'][0]['max_d']=='23/45'
    assert result['points'][1]['max_d']=='11642479/23232400'
    assert Q(result['points'][1]['max_d'])>Q(1,2)
    (P/'flmv_envelope293_exact.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
