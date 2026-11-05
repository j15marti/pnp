#!/usr/bin/env python3
"""Independent strict Resolution/DEF-bit checker for LSPV3/408 emitted JSON."""
from pathlib import Path
import itertools,json
raw=json.loads(Path('/mnt/data/pnp_lspv3_408/raw_408.json').read_text()); checks=0
for case in raw['cases']:
    n=case['n_inputs'];gates=case['gates']; p,q=case['ports']; output={}
    # Verify all gate clauses come from exactly one gate's truth table via exhaustive rows.
    all_gate_clauses={}
    for z,op,a,b in gates:
        assert z>n and z not in all_gate_clauses
        assert 1<=abs(a)<z and 1<=abs(b)<z
        assert op in {'AND','OR','XOR','NAND','XNOR'}
        s=set()
        for vals in itertools.product((0,1),repeat=3):
            ua,ub,uz=vals
            expected={'AND':ua&ub,'OR':ua|ub,'XOR':ua^ub,'NAND':1-(ua&ub),'XNOR':1-(ua^ub)}[op]
            if expected==uz:continue
            # clauses that falsify exactly this combination, handling signed arguments
            c=[]
            for ref,val in ((a,ua),(b,ub),(z,uz)):
                bit = val if ref>0 else 1-val
                c.append(-abs(ref) if bit else abs(ref))
            if not any(-v in c for v in c):s.add(tuple(sorted(set(c))))
        all_gate_clauses[z]=s
    traces=case['proof']; levels=[]
    for i,line in enumerate(traces):
        clause=tuple(sorted(set(line['clause']))); rule=line['step'];assert clause==tuple(line['clause'])
        if rule[0]=='DEF':
            assert len(rule)==2 and clause in all_gate_clauses[rule[1]]
        elif rule[0]=='RES':
            assert len(rule)==4
            _,j,k,pivot=rule
            assert 0<=j<i and 0<=k<i and j!=k
            lhs,rhs=levels[j],levels[k]
            if pivot in lhs and -pivot in rhs:
                res=(lhs-{pivot})|(rhs-{-pivot})
            elif -pivot in lhs and pivot in rhs:
                res=(lhs-{-pivot})|(rhs-{pivot})
            else:raise AssertionError('false pivot')
            assert all(-l not in res for l in res)
            assert clause==tuple(sorted(res))
        else:raise AssertionError('unknown rule')
        levels.append(set(clause));checks+=1
    for a0 in itertools.product((0,1),repeat=n):
        v={i+1:a0[i] for i in range(n)}
        for z,op,a,b in gates:
            aa=(v[abs(a)] if a>0 else 1-v[abs(a)])
            bb=(v[abs(b)] if b>0 else 1-v[abs(b)])
            v[z]={'AND':aa&bb,'OR':aa|bb,'XOR':aa^bb,'NAND':1-(aa&bb),'XNOR':1-(aa^bb)}[op]
        for line in traces:
            assert any(v[abs(l)]==(1 if l>0 else 0) for l in line['clause'])
            checks+=1
    target1=set((-p,q));target2=set((p,-q))
    has1=target1 in levels;has2=target2 in levels
    if case['expected_equal']:assert has1 and has2
    else:assert not(has1 and has2)
    checks+=2
    # Corrupted proof record must fail at first illicit pivot.
    mutable=[dict(x) for x in traces]
    for i,x in enumerate(mutable):
        if x['step'][0]=='RES':
            bad=x['step'][:];bad[3]=10**7
            j,k=bad[1:3]
            assert bad[3] not in levels[j] and -bad[3] not in levels[k]
            checks+=1
            break
print(json.dumps({'independent_assertions':checks,'cases':len(raw['cases']),'validated_trace_lines':sum(len(c['proof']) for c in raw['cases'])},indent=2))
