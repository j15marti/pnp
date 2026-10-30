#!/usr/bin/env python3
"""Local exact count -> certified reduction -> restart. Each batch <=25s."""
import argparse,hashlib,importlib.util,itertools,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
dep=HERE/'2026-10-29_2225_CONSTRUCTION-STRENGTHEN12-test.py'
assert hashlib.sha256(dep.read_bytes()).hexdigest()=='63e00b35bf4e1a88a9cebd7c87ebd95d7c2f7ddc5188149036a4fd3f864dd569'
spec=importlib.util.spec_from_file_location('prior',dep);prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)

def reduce_loop(n,source,group_cap=4,width_cap=6):
    clauses=[tuple(c) for c in source];assigned={};trace=[]
    ledger=dict(groups=0,scope_rejects=0,assignment_trials=0,clause_evaluations=0,restarts=0)
    def result(status):
        return dict(status=status,clauses=clauses,assigned=assigned,trace=trace,ledger=ledger)
    while True:
        residual=[]
        for c in clauses:
            if any(abs(l) in assigned and assigned[abs(l)]==(l>0) for l in c):continue
            r=tuple(l for l in c if abs(l) not in assigned)
            if not r:return result('UNSAT')
            residual.append(r)
        clauses=residual
        if not clauses:return result('SAT')
        action=None
        for k in range(1,min(group_cap,len(clauses))+1):
            for ids in itertools.combinations(range(len(clauses)),k):
                ledger['groups']+=1
                group=[clauses[i] for i in ids];scope=sorted({abs(l) for c in group for l in c})
                if len(scope)>width_cap:ledger['scope_rejects']+=1;continue
                models=[];drop_counts=[0]*k
                for bits in itertools.product((0,1),repeat=len(scope)):
                    ledger['assignment_trials']+=1;values=dict(zip(scope,bits))
                    sat=[any(values[abs(l)]==(l>0) for l in c) for c in group]
                    ledger['clause_evaluations']+=k
                    if all(sat):models.append(bits)
                    for j in range(k):
                        if all(sat[t] for t in range(k) if t!=j):drop_counts[j]+=1
                if not models:
                    trace.append(dict(kind='local_zero',ids=ids));return result('UNSAT')
                for j,v in enumerate(scope):
                    ones=sum(b[j] for b in models)
                    if ones in (0,len(models)):
                        action=('pin',v,int(ones>0),ids,len(models));break
                if action is None:
                    for j,count in enumerate(drop_counts):
                        if count==len(models):action=('delete',ids[j],None,ids,count);break
                if action is not None:break
            if action is not None:break
        if action is None:return result('UNRESOLVED')
        kind,index,value,ids,count=action
        trace.append(dict(kind=kind,index=index,value=value,ids=ids,local_count=count))
        if kind=='pin':assigned[index]=value
        else:clauses.pop(index)
        ledger['restarts']+=1

def audit(n,f):
    r=reduce_loop(n,f)
    exact=prior.brute(n,[],f)
    if r['status']=='UNSAT':assert exact==0
    else:
        pins=[(1<<(v-1))|(bit<<n) for v,bit in r['assigned'].items()]
        assert prior.brute(n,pins,r['clauses'])==exact
    if r['status']=='SAT':assert exact>0
    r.update(n=n,initial_clauses=len(f),original_count=exact)
    return r

def run(batch):
    if batch=='controls':
        f=[(1,2,3),(1,2,-3),(1,-2,3),(1,-2,-3),(-1,4,5),(-1,4,-5)]
        r=audit(5,f);assert r['status']=='SAT' and r['ledger']['restarts']>=2
        no=audit(3,prior.xor_clauses((1,2,3),0)+prior.xor_clauses((1,2,3),1))
        # Small local counts need not detect the global contradiction.
        dup=audit(3,[(1,2,3),(1,2,3)]);assert len(dup['clauses'])==1
        return dict(cascade=r,global_unsat=no,duplicate=dup)
    sources=json.loads((HERE/'2026-10-29_2225_CONSTRUCTION-STRENGTHEN12-strict22.json').read_text())['result']['records']
    sources=[r for r in sources if r['connected'] and r['n']>3]
    start=int(batch)*6
    return [audit(r['n'],r['formula']) for r in sources[start:start+6]]

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--batch',required=True);p.add_argument('--output',required=True);a=p.parse_args()
    r=dict(batch=a.batch,code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),result=run(a.batch))
    Path(a.output).write_text(json.dumps(r,sort_keys=True,indent=2)+'\n');print(a.batch,'PASS')
