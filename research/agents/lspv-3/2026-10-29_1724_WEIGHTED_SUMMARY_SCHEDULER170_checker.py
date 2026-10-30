#!/usr/bin/env python3
"""Independent exact-table certificate verifier for LSPV-3 / 170.

The source is supplied separately from certificate.  This verifies semantic
local table entries against source clauses and child truth tables.  This is not
an LRAT/Resolution kernel.
"""
from pathlib import Path
import json, hashlib, copy, sys, importlib.util

ROOT=Path(__file__).parent
PREFIX='2026-10-29_1724_WEIGHTED_SUMMARY_SCHEDULER170'

def mk(h,w,unsat):
    src=ROOT/(PREFIX.replace('WEIGHTED_SUMMARY_SCHEDULER','LSPV-3_WEIGHTED_SUMMARY_SCHEDULER')+'_repro.py')
    # Actual source path is uniquely fixed by this report name.
    spec=importlib.util.spec_from_file_location('source170',str(src))
    m=importlib.util.module_from_spec(spec);sys.modules['source170']=m;spec.loader.exec_module(m)
    tree=m.family(h,1<<w)
    nodes,clauses,nvars=m.make_cnf(tree,unsat)
    source={"nvars":nvars,"nodes":[{"id":v.idx,"children":[c.idx for c in v.kids],"own":list(v.own),"bag":list(v.bag)} for v in nodes],
            "clauses":[{"owner":owner,"literals":list(cl)} for owner,cl in clauses]}
    table={}
    for v in reversed(nodes):
        owned=[cl for own,cl in clauses if own==v.idx]
        rel=0
        for mask in range(1<<len(v.bag)):
            assignment={x:bool((mask>>i)&1) for i,x in enumerate(v.bag)}
            if any(not any(assignment[abs(x)]==(x>0) for x in cl) for cl in owned):continue
            compatible=True
            for c in v.kids:
                row=sum(int(assignment[x])<<i for i,x in enumerate(c.own))
                if not ((table[c.idx]>>row)&1):compatible=False;break
            if compatible:
                row=sum(int(assignment[x])<<i for i,x in enumerate(v.own))
                rel|=1<<row
        table[v.idx]=rel
    cert={"tables":[{"node":v.idx,"truth_mask":table[v.idx],"source_clause_ids":[j for j,cl in enumerate(source['clauses']) if cl['owner']==v.idx]} for v in reversed(nodes)],
          "decision":"UNSAT" if table[0]==0 else "SAT"}
    if not unsat: cert['witness']={str(v):1 for v in range(1,nvars+1)}
    return source,cert


def check(source,cert):
    try:
        nodes=source['nodes']; clauses=source['clauses'];m=len(nodes)
        assert m>=1 and [v['id'] for v in nodes]==list(range(m))
        assert len(cert['tables'])==m
        expected_ids=set(range(source['nvars']))
        owns={int(x) for v in nodes for x in v['own']}
        assert owns==set(range(1,source['nvars']+1))
        assert sum(len(v['own']) for v in nodes)==source['nvars']
        p={c:node['id'] for node in nodes for c in node['children']}
        assert len(p)==m-1 and set(p)==set(range(1,m))
        assert all(p[c]<c for c in p)
        bag={v['id']:set(v['bag']) for v in nodes}
        for v in nodes:
            assert bag[v['id']]==set(v['own']).union(*(set(nodes[c]['own']) for c in v['children']))
        for cl in clauses:
            owner=cl['owner']; lits=cl['literals']
            assert owner in range(m) and 1<=len(lits)<=3
            assert all(abs(a) in bag[owner] and abs(a) in owns for a in lits)
            assert len(set(map(abs,lits)))==len(lits)
        verified={}
        for rec in cert['tables']:
            i=rec['node']; assert i not in verified and i in range(m)
            v=nodes[i]
            ids=[j for j,cl in enumerate(clauses) if cl['owner']==i]
            assert ids==rec['source_clause_ids']
            assert all(c in verified for c in v['children'])
            witness_truth=0
            for mask in range(1<<len(v['bag'])):
                a={x:bool((mask>>k)&1) for k,x in enumerate(v['bag'])}
                good=all(any(a[abs(lit)]==(lit>0) for lit in clauses[j]['literals']) for j in ids)
                if not good:continue
                for c in v['children']:
                    idx=sum(int(a[x])<<k for k,x in enumerate(nodes[c]['own']))
                    if not (verified[c]>>idx)&1:good=False;break
                if good:
                    idx=sum(int(a[x])<<k for k,x in enumerate(v['own']))
                    witness_truth|=1<<idx
            assert witness_truth==rec['truth_mask']
            verified[i]=witness_truth
        assert set(verified)==set(range(m))
        assert cert['decision']==('UNSAT' if verified[0]==0 else 'SAT')
        if cert['decision']=='SAT':
            witness={int(k):bool(val) for k,val in cert['witness'].items()}
            assert set(witness)==owns
            assert all(any(witness[abs(a)]==(a>0) for a in cl['literals']) for cl in clauses)
        return True
    except (AssertionError,KeyError,TypeError,ValueError,IndexError,OverflowError):
        return False


def main():
    result={'examples':[], 'corrupted_rejected':0}
    for unsat in [False,True]:
        source,cert=mk(2,3,unsat)
        assert check(source,cert)
        o={"h":2,"w":3,"source":source,"certificate":cert}
        f=ROOT/(PREFIX+('_UNSAT' if unsat else '_SAT')+'_certificate.json')
        f.write_text(json.dumps(o,sort_keys=True,indent=2)+'\n')
        result['examples'].append({'status':cert['decision'],'file':f.name,'table_records':len(cert['tables']),
                                   'source_clauses':len(source['clauses']), 'bytes':f.stat().st_size})
        mutations=[]
        x=copy.deepcopy(cert);x['tables'][0]['truth_mask']^=1;mutations.append(x)
        x=copy.deepcopy(cert);x['tables'][0]['source_clause_ids']=[-99];mutations.append(x)
        x=copy.deepcopy(cert);x['tables'].pop();mutations.append(x)
        x=copy.deepcopy(cert);x['decision']='UNSAT' if cert['decision']=='SAT' else 'SAT';mutations.append(x)
        for x in mutations:
            assert not check(source,x)
            result['corrupted_rejected']+=1
    p=ROOT/(PREFIX+'_checker_results.json')
    p.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
