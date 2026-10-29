#!/usr/bin/env python3
"""Charged adaptive partition audit; run each --batch under timeout 25s."""
import argparse, hashlib, importlib.util, itertools, json
from pathlib import Path

HERE=Path(__file__).resolve().parent
DEPENDENCY=HERE/'2026-10-29_2225_CONSTRUCTION-STRENGTHEN12-test.py'
assert hashlib.sha256(DEPENDENCY.read_bytes()).hexdigest()=='63e00b35bf4e1a88a9cebd7c87ebd95d7c2f7ddc5188149036a4fd3f864dd569'
spec=importlib.util.spec_from_file_location('signed_affine',DEPENDENCY)
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)

def acquire(n,formula,width,neutral):
    groups=[(i,) for i in range(len(formula))]
    compiled=old.compile_modules(n,formula,groups,width)
    ledger={'compilations':1,'assignment_trials':compiled[3]['assignment_trials'],
            'pair_scans':0,'scope_rejects':0,'evaluated_rejects':0,'accepted':[],
            'initial_defect':len(compiled[2])}
    while True:
        best=None
        scopes=[{abs(l) for i in g for l in formula[i]} for g in groups]
        current=len(compiled[2])
        for i,j in itertools.combinations(range(len(groups)),2):
            ledger['pair_scans']+=1
            if not scopes[i]&scopes[j] or len(scopes[i]|scopes[j])>width:
                ledger['scope_rejects']+=1;continue
            candidate=sorted([g for k,g in enumerate(groups) if k not in (i,j)]+[tuple(sorted(groups[i]+groups[j]))])
            result=old.compile_modules(n,formula,candidate,width)
            ledger['compilations']+=1
            ledger['assignment_trials']+=result[3]['assignment_trials']
            d=len(result[2])
            if d>current or (d==current and not neutral):
                ledger['evaluated_rejects']+=1;continue
            key=(d,candidate)
            if best is None or key<best[0]: best=(key,result)
        if best is None: break
        (d,groups),compiled=best
        ledger['accepted'].append({'defect':d,'modules':len(groups)})
    answer,terminal=old.count_affine(compiled[0],compiled[1],compiled[2])
    ledger.update(final_defect=len(compiled[2]),final_groups=groups,
                  boundary_count=answer,terminal=terminal)
    assert (answer>0)==(old.brute(n,[],formula)>0)
    return ledger

def run(batch):
    if batch=='controls':
        xor=old.xor_clauses((1,2,3),0)
        strict=acquire(3,xor,3,False);neutral=acquire(3,xor,3,True)
        assert strict['final_defect']==4 and not strict['accepted']
        assert neutral['final_defect']==0
        # All proper subsets of the quartet have exactly their size as defect.
        plateau=[]
        for size in (1,2,3):
            for chosen in itertools.combinations(range(4),size):
                groups=[chosen]+[(i,) for i in range(4) if i not in chosen]
                result=old.compile_modules(3,xor,groups,3)
                assert len(result[2])==4
                plateau.append(list(chosen))
        unsat=xor+old.xor_clauses((1,2,3),1)
        negative=acquire(3,unsat,3,True)
        assert negative['boundary_count']==0
        return {'xor_strict':strict,'xor_neutral':neutral,
                'plateau_subsets':len(plateau),'opposite_xor_unsat':negative}
    data=json.loads((HERE/'2026-10-29_2225_CONSTRUCTION-STRENGTHEN12-strict22.json').read_text())
    sources=[r for r in data['result']['records'] if r['connected'] and r['n']>3]
    start=int(batch)*6
    records=[]
    for source in sources[start:start+6]:
        assert old.strict22(source['n'],source['formula'])
        policies={}
        for neutral in (False,True):
            policies['neutral' if neutral else 'strict']=acquire(source['n'],source['formula'],5,neutral)
        if len({tuple(sorted(c)) for c in source['formula']})==len(source['formula']):
            assert not policies['strict']['accepted']
        records.append({'n':source['n'],'formula':source['formula'],'policies':policies})
    return {'batch':int(batch),'records':records}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--batch',required=True);ap.add_argument('--output',required=True)
    a=ap.parse_args();result={'status':'COMPUTATIONAL','code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                           'dependency_sha256':hashlib.sha256(DEPENDENCY.read_bytes()).hexdigest(),'result':run(a.batch)}
    Path(a.output).write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'batch':a.batch,'status':'PASS'}))
