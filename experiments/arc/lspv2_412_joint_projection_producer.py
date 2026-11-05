#!/usr/bin/env python3
"""Deterministic exhaustive joint-vs-independent DEF projection falsifier. No packages."""
import json
from pathlib import Path

OUT=Path(__file__).with_name("2026-11-05_0112_LSPV2_JOINT_DEF_PROJECTION412_summary.json")

def gate(x,y):
    a=x^y
    return a,a^y

def independent_projection(x,a,b):
    return any(a==(x^y) for y in (0,1)) and any(b==(a^y) for y in (0,1))

def joint_projection(x,a,b):
    return any(a==(x^y) and b==(a^y) for y in (0,1))

def test(k):
    assert 1<=k<=6
    total_joint=total_separate=0
    for xm in range(1<<k):
        exact=approx=0
        for am in range(1<<k):
            for bm in range(1<<k):
                j=s=True
                for i in range(k):
                    x=(xm>>i)&1; a=(am>>i)&1; b=(bm>>i)&1
                    j &= joint_projection(x,a,b)
                    s &= independent_projection(x,a,b)
                    assert joint_projection(x,a,b)==(b==x)
                    assert ((not b or x) and (b or not x))==(b==x)
                exact += j; approx += s
        assert exact==2**k and approx==2**(2*k)
        total_joint+=exact; total_separate+=approx
    plus=minus=0
    for ym in range(1<<k):
        xx=(1<<k)-1
        assert all(((xx>>i)&1) or ((ym>>i)&1) for i in range(k))
        assert all(gate((xx>>i)&1,(ym>>i)&1)[1]==1 for i in range(k))
        plus+=1
        xx=0
        if all(((xx>>i)&1) or ((ym>>i)&1) for i in range(k)):
            assert all(gate((xx>>i)&1,(ym>>i)&1)[1]==0 for i in range(k))
            minus+=1
    assert plus==2**k and minus==1
    assert total_joint==2**(2*k) and total_separate==2**(3*k)
    return dict(k=k,paid_definitions=2*k,original_variables=2*k,
      joint_models_over_x_a_b=total_joint,independent_models_over_x_a_b=total_separate,
      projection_spurious_multiplier=total_separate//total_joint,
      plus_source_models=plus,minus_source_models=minus,
      compact_equality_clauses=2*k,conditional_row_export_proof_nodes=5*k)

def negative_controls():
    bad=[None,{'op':'XOR','in':['x']},{'op':'XOR','in':['x','q']},
         {'op':'XOR','in':['a','x'],'out':'a'},
         {'op':'XOR','in':['a','y'],'out':'b','row_rhs':1},
         {'op':'XOR','in':['a','y'],'out':'b','exported_without_rights':True}]
    for c in bad:
        ok=(isinstance(c,dict) and c.get('op')=='XOR' and
            isinstance(c.get('in'),list) and len(c['in'])==2 and
            c.get('out') in {'a','b'} and c['out'] not in c['in'] and
            not c.get('row_rhs',0) and not c.get('exported_without_rights',False) and
            all(v in {'x','y','a'} for v in c['in']))
        assert not ok
    return len(bad)

def run():
    rows=[test(i) for i in range(1,7)]
    return {'algorithm':'deterministic exhaustive','k_range':[1,6],
      'label':'LSPV2_412_joint_projection_failure','malformed_rejections':negative_controls(),
      'random_seed':None,'rows':rows,
      'statement':'exists y (D1 and D2) differs from exists y D1 and exists y D2',
      'status':'COMPUTATIONAL; symbolic theorem separately proved; no native-export claim'}

if __name__=='__main__':
    result=run()
    OUT.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
