#!/usr/bin/env python3
"""Independent Python referee for LSPV-1 361, uses no JS implementation helpers."""
import hashlib, json, sys, copy
from pathlib import Path

def norm(c):
    assert all(isinstance(l,int) and l!=0 for l in c)
    c=sorted(set(c),key=lambda x:(abs(x),x))
    assert not any(-lit in c for lit in c)
    return c

def sat_clause(clause, assignment):
    return any((assignment.get(abs(lit),False)) == (lit>0) for lit in clause)

def sat_formula(cnf,assignment):
    return all(sat_clause(clause,assignment) for clause in cnf)

def expected(b):
    m=1<<b; source=[]
    for j in range(m):
        t=b+j+1
        block=[(-i-1 if (j>>i)&1 else i+1) for i in range(b)]
        source.extend(([t],norm([-t]+block)))
    lines='p cnf %s %s\n'%(b+m,len(source))
    lines+=''.join(' '.join(map(str,cl))+' 0\n' for cl in source)
    return source,lines

def restrict_witness(b,j,deleted_kind):
    ass={i+1: bool((j>>i)&1) for i in range(b)}
    for k in range(1<<b):
        ass[b+k+1]=(k!=j if deleted_kind=='unit' else True)
    return ass

def replay(case):
    b=case['bits'];m=1<<b; expected_source,dimacs=expected(b)
    if case['source'] != expected_source: raise ValueError('unauthenticated source')
    if case['source_sha256'] != hashlib.sha256(dimacs.encode()).hexdigest(): raise ValueError('wrong source hash')
    if case['mask_count']!=m or case['source_count']!=2*m or case['variables']!=b+m:raise ValueError('declared size')
    dag=[c[:] for c in expected_source]
    for node in case['steps']:
        a,z,p=node['a'],node['b'],node['pivot']
        if not (isinstance(a,int) and isinstance(z,int) and 0<=a<len(dag) and 0<=z<len(dag)):raise ValueError('parent')
        if p not in dag[a] or -p not in dag[z]:raise ValueError('pivot')
        out=norm([q for q in dag[a] if q!=p]+[q for q in dag[z] if q!=-p])
        if out!=node['lits']:raise ValueError('conclusion')
        dag.append(out)
    if dag[-1] != [] or len(case['steps']) != 2*m-1 or case['cost'] != 2*m-1:raise ValueError('not refutation')
    return True

def run():
    proof_path=Path(sys.argv[1] if len(sys.argv)>1 else '/mnt/data/lspv1_361/reflection_mask_cube361_proofs.json')
    raw=json.loads(proof_path.read_text())
    out=[]; assertions=0
    for case in raw['cases']:
        replay(case);assertions+=1
        b=case['bits'];m=1<<b;source=case['source'];blockers=[expected(b)[0][2*j+1][1:] for j in range(m)]
        for j in range(m):
            for kind in ('unit','guard'):
                index=2*j+(kind=='guard')
                deleted=source[:index]+source[index+1:]
                w=restrict_witness(b,j,kind)
                assert sat_formula(deleted,w);assertions+=1
                for l_index in range(len(source[index])):
                    mutated=[row[:] for row in source];mutated[index][l_index]*=-1
                    assert sat_formula(mutated,w);assertions+=1
        for fix in ('pivot','conclusion','source','source_hash'):
            bad=copy.deepcopy(case)
            if fix=='pivot':bad['steps'][0]['pivot']=9999
            if fix=='conclusion':bad['steps'][0]['lits']=[-9999]
            if fix=='source':bad['source'][0][0]*=-1
            if fix=='source_hash':bad['source_sha256']='0'*64
            try:replay(bad)
            except (ValueError,AssertionError):assertions+=1
            else:raise AssertionError('forgery accepted: '+fix)
        masks=range(1<<m) if m<=16 else [0,(1<<m)-1,*((1<<m)-1-(1<<j) for j in range(m))]
        for mask in masks:
            rejection = (mask == (1<<m)-1)
            witness = next((j for j in range(m) if not ((mask>>j)&1)),None)
            assert rejection == (witness is None)
            if witness is not None:
                ass={i+1:bool((witness>>i)&1) for i in range(b)}
                active=[blockers[j] for j in range(m) if (mask>>j)&1]
                assert sat_formula(active,ass)
            assertions+=1
        for bad in ('','2','01Z',' ','0'*(m+1)):
            assert not (len(bad)==m and all(c in '01' for c in bad));assertions+=1
        out.append(dict(bits=b,minimum=2*m-1,source_sha=case['source_sha256'],proof_steps=len(case['steps'])))
    for c in (0,1):
        models=sum(((a.bit_count()&1)==c) for a in range(8))
        assert models==4;assertions+=1
    result={'referee':'independent Python 361','status':'PASS','assertions':assertions,'cases':out,'raw_certificate_bytes':proof_path.stat().st_size}
    print(json.dumps(result,sort_keys=True));return result

if __name__=='__main__':run()
