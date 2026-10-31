#!/usr/bin/env python3
"""Separate full S/U source-control verifier; no producer imports. Python 3 stdlib."""
import argparse,ast,base64,collections,gzip,hashlib,itertools,json,pathlib

def load(path):return json.loads(gzip.decompress(base64.b64decode(pathlib.Path(path).read_text().strip())).decode())

def sourceU(path):
    lines=[z for z in pathlib.Path(path).read_text().splitlines() if z.strip() and not z.startswith('#')]
    return ast.literal_eval('\n'.join(lines))

def acceptable(c,a):return sum(a[abs(x)]==int(x>0) for x in c)

def verify_one(case,source,metrics):
    E=case['full_occurrence_extrema'];n=case['n'];m=case['m'];assert len(E)==m==len(source)
    for j,c in enumerate(source):
        d=E[j];assert d['source_clause_index']==j
        assert len(d['literal_occurrences'])==3
        for l,r in zip(c,d['literal_occurrences']):
            assert r['literal']==l and r['variable']==abs(l)
            assert r['S']==int(l>0) and r['U']==int(l<0)
            assert r['invert_S_is_U']==r['U'] and r['invert_U_is_S']==r['S']
            metrics['original_signed_occurrence_targets']+=4
    assert case['pairs_checked']==m*(m-1)//2
    none=0
    for i,j,mask in case['all_source_indexed_clause_pair_modes']:
        assert i<j and 0<=mask<=15
        for bit,(a,b) in enumerate(itertools.product('SU',repeat=2)):
            aa={abs(l):(int(l>0) if a=='S' else int(l<0)) for l in source[i]}
            bb={abs(l):(int(l>0) if b=='S' else int(l<0)) for l in source[j]}
            possible=all(aa[k]==bb[k] for k in aa.keys()&bb.keys())
            assert bool(mask & (1<<bit))==possible
            metrics['source_indexed_pair_modes']+=1
        assert mask!=0
        none+=int(mask==0)
    assert none==case['none_compatible_pair_count']==0
    for trail in case['globally_coherent_endpoint_and_flip_controls']:
        mask=trail['source_mask'];mask=((1<<n)-1) if mask==-1 else mask
        a=[0]+[(mask>>(k-1))&1 for k in range(1,n+1)]
        h=[sum(acceptable(c,a)==t for c in source) for t in range(4)]
        assert trail['histogram_t0_t1_t2_t3']==h
        assert trail['complement_histogram']==h[::-1]
        assert trail['source_formula_satisfied']==(h[0]==0)
        metrics['coherent_flip_trails']+=1
    for p in case['first_24_original_source_resolution_proofs']:
        i,j=p['parent_clause_indices'];v=p['pivot_variable'];r=p['derived_nontautological_resolvent'];cube=p['prohibited_falsifying_cube']
        assert any(l==v for l in source[i]+source[j]) and any(l==-v for l in source[i]+source[j])
        expect=set(l for l in source[i]+source[j] if abs(l)!=v)
        assert set(r)==expect and all(-l not in expect for l in expect)
        assert {int(k):b for k,b in cube.items()}=={abs(l):int(l<0) for l in r}
        # Check the resolvent directly under every assignment to its variables and pivot.
        vs=sorted({abs(l) for l in source[i]+source[j]});assert len(vs)<=5
        for bits in itertools.product((0,1),repeat=len(vs)):
            a=dict(zip(vs,bits))
            if acceptable(source[i],a)>0 and acceptable(source[j],a)>0:
                assert acceptable(r,a)>0
                metrics['resolution_truth_rows']+=1
    metrics['resolution_proofs']+=len(case['first_24_original_source_resolution_proofs'])

def main():
    a=argparse.ArgumentParser();a.add_argument('--input',required=True);a.add_argument('--data',required=True);a.add_argument('--u',required=True);a.add_argument('--out',required=True);opt=a.parse_args()
    obj=load(opt.input);raw=json.loads(pathlib.Path(opt.data).read_text());U=sourceU(opt.u)
    assert obj['U_compact_json_sha256']==hashlib.sha256(json.dumps(U,separators=(',',':')).encode()).hexdigest()
    sources={t['name']:t['formula'] for t in raw['cases']};sources['DOECKER_U198_UNSAT']=U
    metric=collections.Counter()
    assert len(obj['controls'])==8
    for c in obj['controls']:verify_one(c,sources[c['name']],metric)
    digest=hashlib.sha256(gzip.decompress(base64.b64decode(pathlib.Path(opt.input).read_text().strip()))).hexdigest()
    results={'status':'independent source control verified','sha256_uncompressed_json':digest,'metrics':dict(metric)}
    pathlib.Path(opt.out).write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
    print(json.dumps(results,indent=2,sort_keys=True))
if __name__=='__main__':main()