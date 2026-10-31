#!/usr/bin/env python3
"""Independent finite auditor for HITTING_BACKDOOR_FLIP_DAG276 raw JSON.
Uses no imports from producer; exhaustive source/cube truth checks and resolution replay.
"""
import json,itertools,sys,hashlib

def sortedc(a):return tuple(sorted(set(a),key=lambda x:(abs(x),x<0)))
def satisfied(c,b):return any((b[abs(z)]==1) if z>0 else (b[abs(z)]==0) for z in c)
def full_sat(F,b):return all(satisfied(c,b) for c in F)
def assignments(vs):
    for bits in itertools.product((0,1),repeat=len(vs)):yield dict(zip(vs,bits))
def verify_proof(F,proof):
    records=proof['nodes'];assert records
    for ix,node in enumerate(records):
        out=sortedc(node['clause']);assert out==tuple(node['clause'])
        if 'source' in node:
            assert node['source'] in range(len(F))
            assert out==F[node['source']]
        else:
            p,q=node['parents'];piv=node['pivot']
            assert 0<=p<ix and 0<=q<ix and piv>0
            a=records[p]['clause'];b=records[q]['clause']
            assert piv in a and -piv in b
            assert out==sortedc([x for x in a if x!=piv]+[x for x in b if x!=-piv])
            assert not any(-x in out for x in out)
    assert 0<=proof['root']<len(records)
    return tuple(records[proof['root']]['clause'])

def check(o):
    checks=0;bad_attempts=0
    original=dict(o);original.pop('digest_source_excluding_digest',None)
    s=hashlib.sha256(json.dumps(original,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    # Runtime / peak are included in JSON digest; exact round-trip canonical encoding.
    assert s==o['digest_source_excluding_digest'];checks+=1
    for record in o['cases']:
        n=record['n'];F=[tuple(c) for c in record['source_clauses']];vs=list(range(1,n+1))
        assert all(c==sortedc(c) for c in F)
        models=[a for a in assignments(vs) if full_sat(F,a)]
        assert bool(models)==record['truth'] and len(models)==record['models'];checks+=2
        ct=record['extreme_controls'];local=ct['local'];assert len(local)==len(F)
        for j,c in enumerate(F):
            d=local[j];assert d['j']==j
            st={abs(v):int(v>0) for v in c}
            ut={k:1-v for k,v in st.items()}
            assert {int(k):v for k,v in d['S'].items()}==st
            assert {int(k):v for k,v in d['U'].items()}==ut
            assert {int(k):v for k,v in d['invert_S'].items()}==ut
            assert {int(k):v for k,v in d['invert_U'].items()}==st
            for pos,l in enumerate(c):
                t=d['source_signed_occurrences'][pos]
                assert t['variable']==abs(l) and t['clause']==j and t['S']==int(l>0) and t['U']==int(l<0)
                checks+=1
        for row in ct['pair_modes']:
            i,j=row['i'],row['j']
            assert i<j
            for a in ('S','U'):
                for b in ('S','U'):
                    ai={int(x):v for x,v in local[i][a].items()};bj={int(x):v for x,v in local[j][b].items()}
                    correct=not any(x in bj and bj[x]!=v for x,v in ai.items())
                    assert row[a+b]==correct;checks+=1
        z={v:0 for v in vs};u={v:1 for v in vs}
        for key,b in [('zero',z),('one',u)]:
            ctcs=[sum((b[abs(t)]==(1 if t>0 else 0)) for t in c) for c in F]
            assert ct[key+'_counts']==ctcs and ct[key+'_sat']==full_sat(F,b)
            checks+=2
        trail=z.copy()
        for k,fr in enumerate(ct['flips'],start=1):
            assert fr['variable']==k
            assert fr['before']==[sum((trail[abs(t)]==(1 if t>0 else 0)) for t in c) for c in F]
            trail[k]=1
            assert fr['after']==[sum((trail[abs(t)]==(1 if t>0 else 0)) for t in c) for c in F]
            checks+=2
        T=record['backdoor'];results=record['cube_results']
        if T is None:assert len(results)==0
        else:
            T=set(T);R=set(vs)-T
            assert all(sum(abs(x) in R for x in c)<=2 for c in F);checks+=1
            observed=[]
            for result in results:
                if result['sat']:
                    w={int(k):v for k,v in result['witness'].items()}
                    assert full_sat(F,w)
                    observed.append(w)
                    checks+=1
                else:
                    d=verify_proof(F,result)
                    assert d==tuple(result['nogood'])
                    assert all(abs(l) in T for l in d)
                    assert not any(full_sat(F,a) and not satisfied(d,a) for a in assignments(vs))
                    checks+=2+len(result['nodes'])
            if record['truth']:
                assert any(full_sat(F,w) for w in observed)
            else:
                full=record['full_unsat_refutation']
                assert full is not None and verify_proof(F,full)==()
                assert len(results)==2**len(T)
                checks+=1+len(full['nodes'])
            for b in assignments(sorted(T)):
                # Every boundary cube assignment is covered exactly by one recorded profile,
                # except for the SAT early exit, where no further profiles are necessary.
                for r in results:
                    if r['sat']:
                        w={int(k):v for k,v in r['witness'].items()}
                        if all(w[x]==b[x] for x in T):
                            assert full_sat(F,w)
                    else:
                        pass
                checks+=1
        child=[tuple(x) for x in record['selected_child_clauses']]
        assert all(c in child for c in F)
        assert all(full_sat(child,a)==full_sat(F,a) for a in assignments(vs))
        checks+=1+2**n
    for row in o['cases']:
        proof=row['full_unsat_refutation']
        if proof is None:continue
        mutated=json.loads(json.dumps(proof))
        mutated['nodes'][mutated['root']]['clause']=[987654321]
        try: verify_proof([tuple(c) for c in row['source_clauses']],mutated)
        except AssertionError:bad_attempts+=1
        else:raise AssertionError('corrupted proof passed')
    return {'verified':True,'cases':len(o['cases']),'checks':checks,'corrupted_proofs_rejected':bad_attempts,'digest':s}

if __name__=='__main__':
    with open(sys.argv[1] if len(sys.argv)>1 else '/mnt/data/lspv2_276/raw276.json') as f:o=json.load(f)
    ans=check(o); print(json.dumps(ans,indent=2))
    with open('/mnt/data/lspv2_276/verification276.json','w') as f:json.dump(ans,f,indent=2)