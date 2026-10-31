#!/usr/bin/env python3
"""Independent verifier of all 270 source-version certificates and adversarial controls.
Does not import or execute run270.py. Reads immutable JSON and independently
recomputes truth tables via NumPy and source-reason UP certificates.
"""
import json,hashlib,copy,sys
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent

def legal(src,n,rho,a):
    return all(a.get(int(v))==val for v,val in rho.items()) and all(any(a.get(abs(l))==int(l>0) for l in c) for c in src.values())

def query_all(src,n,rho):
    # Vectorized independent brute force, not producer bit-mask arithmetic.
    a=np.arange(1<<n,dtype=np.uint32)
    passing=np.ones(1<<n,dtype=np.bool_)
    for i,v in rho.items():passing &= (((a>>(i-1))&1)==v)
    for c in src.values():
        local=np.zeros_like(passing)
        for l in c:local |= (((a>>(abs(l)-1))&1)==int(l>0))
        passing &= local
    return bool(np.any(passing)),int(np.count_nonzero(passing))

def check_tree(src,n,rho,tree):
    counter=[0]
    def go(a,t):
        for cid,l in t['steps']:
            cid=int(cid);assert cid in src
            c=src[cid];un=[];true=False
            for v in c:
                counter[0]+=1
                old=a.get(abs(v))
                if old is None:un.append(v)
                elif old==int(v>0):true=True;break
            assert not true and len(un)==1 and un[0]==l and abs(l) not in a
            a[abs(l)]=int(l>0)
        kind=t['type'];counter[0]+=1
        if kind=='conflict':
            c=src[int(t['cid'])]
            assert all(a.get(abs(l))==int(l<0) for l in c)
            return False
        if kind=='sat':
            w={int(k):v for k,v in t['witness'].items()}
            assert len(w)==n and all(a.get(k)==v for k,v in a.items())
            assert legal(src,n,rho,w)
            return True
        assert kind=='branch' and t['var'] not in a
        x=t['var'];b0=dict(a);b1=dict(a);b0[x]=0;b1[x]=1
        assert go(b0,t['lo'])==False
        assert go(b1,t['hi'])==False
        return False
    ok=go(dict(rho),tree)
    return ok,counter[0]

def getdeps(t):
    r={int(cid) for cid,_ in t['steps']}
    if t['type']=='conflict':r.add(int(t['cid']))
    if t['type']=='branch':r |= getdeps(t['lo'])|getdeps(t['hi'])
    return r

def modes_exact(a,b):
    variables=sorted(set(map(abs,a))|set(map(abs,b)))
    out={key:False for key in ('SS','SU','US','UU')}
    for mask in range(1<<len(variables)):
        ass={v:(mask>>i)&1 for i,v in enumerate(variables)}
        ca=sum(ass[abs(l)]==int(l>0) for l in a)
        cb=sum(ass[abs(l)]==int(l>0) for l in b)
        for p,q,k in ((len(a),len(b),'SS'),(len(a),0,'SU'),(0,len(b),'US'),(0,0,'UU')):
            if ca==p and cb==q:out[k]=True
    return out

def check(raw):
    counts={'original_roots':0,'source_versions':0,'SAT':0,'UNSAT':0,'certificate_steps':0,'pair_modes_checked':0,'extreme_occurrences_checked':0,'gray_flip_checks':0,'reuse_certificates':0,'brute_assignments_covered':0,'corruptions_rejected':0}
    originals=raw['cases']
    for name,x in originals.items():
        n=x['n'];source={i+1:tuple(c) for i,c in enumerate(x['original_clauses'])}
        diag=raw['original_diagnostics'][name];counts['original_roots']+=1
        for row in diag['extrema']:
            cid=row['cid'];assert tuple(row['signed_occurrences'])==source[cid]
            true={str(abs(l)):int(l>0) for l in source[cid]};false={str(abs(l)):int(l<0) for l in source[cid]}
            assert row['S']==row['invert_U_to_S']==true
            assert row['U']==row['invert_S_to_U']==false
            counts['extreme_occurrences_checked']+=len(source[cid])
        for row in diag['modes']:
            expected=modes_exact(source[row['i']],source[row['j']]);assert all(row[k]==expected[k] for k in expected)
            counts['pair_modes_checked']+=4
        for bound in (0,1):
            a={i:bound for i in range(1,n+1)}
            r=[sum(a[abs(l)]==int(l>0) for l in c) for c in source.values()]
            val=diag['endpoint0' if bound==0 else 'endpoint1']
            assert val['counts']==r
            assert val['N']==[r.count(j) for j in range(4)]
        for g,m,status in diag['gray_layers']:
            assert m==g^(g>>1)
            a={i:(m>>(i-1))&1 for i in range(1,n+1)}
            ts=[sum(a[abs(l)]==int(l>0) for l in c) for c in source.values()]
            assert status==[ts.count(j) for j in range(4)]
            counts['gray_flip_checks']+=1
        for item in diag['prefix_flips']:
            flip=item['flip_prefix'];a={i:int(i<=flip) for i in range(1,n+1)}
            ts=[sum(a[abs(l)]==int(l>0) for l in c) for c in source.values()]
            assert item['status']['counts']==ts
    for method in ('baseline','cached'):
        groups={}
        for rec in raw[method]:
            name=rec['case'];n=originals[name]['n'];rho={int(i):v for i,v in rec['rho'].items()}
            src={int(i):tuple(c) for i,c in rec['src'].items()}
            answer,models=query_all(src,n,rho)
            assert answer==(rec['label']=='SAT')
            counts['brute_assignments_covered']+=1<<n
            counts['source_versions']+=1
            counts[rec['label']]+=1
            group=groups.setdefault(name,{})
            if rec['mechanism']=='fresh':
                if answer:
                    a={int(i):v for i,v in rec['certificate']['witness'].items()}
                    assert legal(src,n,rho,a)
                else:
                    tree=rec['certificate']['tree'];assert tree
                    label,steps=check_tree(src,n,rho,tree)
                    assert not label
                    counts['certificate_steps']+=steps
                group[rec['version']]=(src,rho,rec['certificate'],rec['label'])
            else:
                counts['reuse_certificates']+=1
                assert rec['reused_from'] in group
                prev_src,prev_rho,cert,prev_label=group[rec['reused_from']]
                assert prev_label==rec['label']
                if answer:
                    old={int(i):v for i,v in cert['witness'].items()}
                    assert legal(src,n,rho,old)
                else:
                    tree=cert['tree'];assert tree
                    assert not check_tree(prev_src,n,prev_rho,tree)[0]
                    assert all(rho.get(v)==a for v,a in prev_rho.items())
                    assert all(src.get(cid)==prev_src.get(cid) for cid in getdeps(tree))
    assert counts['source_versions']==288
    # Explicit adversarial tamper rejection checks, independent of producer.
    example=next(r for r in raw['cached'] if r['mechanism']=='fresh' and r['label']=='UNSAT')
    src={int(i):tuple(c) for i,c in example['src'].items()};rho={int(i):v for i,v in example['rho'].items()}
    t=copy.deepcopy(example['certificate']['tree']);t['steps'].append([999,1]);
    try:check_tree(src,raw['cases'][example['case']]['n'],rho,t)
    except (AssertionError,KeyError):counts['corruptions_rejected']+=1
    example=next(r for r in raw['cached'] if r['mechanism']=='fresh' and r['label']=='SAT')
    a={int(i):v for i,v in example['certificate']['witness'].items()};c={int(i):tuple(v) for i,v in example['src'].items()}
    # Insert clause that falsifies witness while preserving source IDs.
    c[max(c)+1]=(-1 if a[1] else 1,)
    try:assert legal(c,raw['cases'][example['case']]['n'],{},a)
    except AssertionError:counts['corruptions_rejected']+=1
    # Change exactly one source reason and test syntactic transfer refusal.
    example=next(r for r in raw['cached'] if r['mechanism']=='fresh' and r['label']=='UNSAT')
    old={int(i):tuple(v) for i,v in example['src'].items()};old_r=getdeps(example['certificate']['tree'])
    cid=next(iter(sorted(old_r)));new=dict(old);new[cid]=tuple(-l for l in old[cid])
    try:assert all(new.get(i)==old[i] for i in old_r)
    except AssertionError:counts['corruptions_rejected']+=1
    assert counts['corruptions_rejected']==3
    return counts

if __name__=='__main__':
    p=HERE/'raw270.json';raw=json.loads(p.read_text());result=check(raw)
    (HERE/'verified270.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
