#!/usr/bin/env python3
"""Adverse residual controls. Baseline UP-DPLL vs exact exhaustive labels."""
import itertools,json,hashlib
from pathlib import Path
from horn_frontier273 import run_dpll,clauses_true,flip_controls

def xor3(parity):
    c=[]
    for bits in itertools.product([0,1],repeat=3):
        if sum(bits)%2!=parity:
            c.append(tuple(i+1 if bits[i]==0 else -(i+1) for i in range(3)))
    return c

def go():
    orig=json.loads(Path(__file__).with_name('controls_fixture.json').read_text())
    cases={name:(v['n'],v['clauses'],v['expected_SAT']) for name,v in orig.items()}
    cases.update({
      'XOR3_SAT':(3,xor3(1),True),
      'XOR3_UNSAT':(3,xor3(1)+xor3(0),False),
      'KROM_SAT':(2,[(1,2),(-1,2),(1,-2)],True),
      'KROM_UNSAT':(2,[(1,2),(-1,2),(1,-2),(-1,-2)],False),
      'HORN_SAT':(3,[(-1,2),(-2,3),(1,)],True),
      'HORN_UNSAT':(3,[(-1,2),(-2,3),(1,),(-3,)],False),
      'DUAL_HORN_SAT':(3,[(1,-2),(2,-3),(-1,)],True),
      'DUAL_HORN_UNSAT':(3,[(1,-2),(2,-3),(-1,),(3,)],False),
      'HIGHWIDTH_EASY_SAT':(10,[tuple(range(1,11)),tuple(-i for i in range(1,11))],True),
      'HIGHWIDTH_EASY_UNSAT':(10,[tuple(range(1,11))]+[(-i,) for i in range(1,11)],False),
    })
    r=[]
    for name,(n,clauses,expected) in cases.items():
        witness,counts=run_dpll(clauses,n)
        exact=any(clauses_true(clauses,bb) for bb in itertools.product([False,True],repeat=n))
        assert (witness is not None)==exact==expected,(name,expected,exact)
        controls=flip_controls(clauses,n)
        assert len(controls['pair_extremes'])==len(clauses)*(len(clauses)-1)//2
        r.append({'case':name,'n':n,'m':len(clauses),'SAT':expected,'baseline':counts,
          'original_indexed_clauses':clauses,'source_sha256':hashlib.sha256(str(clauses).encode()).hexdigest(),
          'endpoints_and_flips':controls['endpoint_flip_trails'],
          'extreme_modes':len(controls['pair_extremes'])*4})
    path=Path(__file__).with_name('adversarial_raw.json');path.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'controls':len(r),'sat':sum(x['SAT'] for x in r),'unsat':sum(not x['SAT'] for x in r),
      'dpll_nodes':sum(x['baseline']['nodes'] for x in r),'extreme_mode_checks':sum(x['extreme_modes'] for x in r)}))
if __name__=='__main__':go()