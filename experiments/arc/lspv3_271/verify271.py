#!/usr/bin/env python3
"""Independent source-relative verifier for ARC271, no import of producer module.
Checks every original clause, every pair mode by local exact enumeration,
all SAT witnesses and available exhaustive SAT/UNSAT labels, backdoor witnesses,
and complete baseline UNSAT branch trees.
"""
import argparse, collections, itertools, json, math
from pathlib import Path
HERE=Path(__file__).resolve().parent

def clause_count(c,a):
    return sum(a[abs(l)] == (l>0) for l in c)

def model_ok(clauses,a):
    return all(any(a[abs(z)]==(z>0) for z in c) for c in clauses)

def independent_up(F,d):
    a=dict(d)
    while True:
        change=False
        for C in F:
            if any(z and (abs(z) in a) and a[abs(z)]==(z>0) for z in C):continue
            remaining=[z for z in C if abs(z) not in a]
            if not remaining:return True
            if len(remaining)==1:
                z=remaining[0];u=abs(z);v=z>0
                if u in a and a[u]!=v:return True
                if u not in a:a[u]=v;change=True
        if not change:return False

def tree_valid(tree,F,assumps,counts):
    counts['proof_nodes']+=1
    if 'conflict_clause' in tree:
        idx=tree['conflict_clause']-1
        assert 0<=idx<len(F)
        assert independent_up(F,assumps)
        counts['proof_leaves']+=1
        return
    v=tree['branch_var'];assert v not in assumps
    for b,name in [(False,'low'),(True,'high')]:
        a=dict(assumps);a[v]=b
        tree_valid(tree[name],F,a,counts)

def exact_pair(C,D,mode):
    vs=sorted({abs(z) for z in C+D})
    for bits in itertools.product((False,True),repeat=len(vs)):
        a=dict(zip(vs,bits))
        sC=clause_count(C,a)==(len(C) if mode[0]=='S' else 0)
        sD=clause_count(D,a)==(len(D) if mode[1]=='S' else 0)
        if sC and sD:return True
    return False

def backdoor_matches(C,B,typ):
    B=set(B)
    for c in C:
        if typ=='Krom':
            if len(c)-sum(abs(z) in B for z in c)>2:return False
        elif typ=='Horn':
            if sum(z>0 and abs(z) not in B for z in c)>1:return False
        else:
            if sum(z<0 and abs(z) not in B for z in c)>1:return False
    return True

def exact_models(F,n):
    total=0
    for mask in range(1<<n):
        a={v:bool(mask&(1<<(v-1))) for v in range(1,n+1)}
        if model_ok(F,a):total+=1
    return total

def verify(path):
    raw=json.loads(Path(path).read_text());counts=collections.Counter()
    for label,data in raw['cases'].items():
        spec=raw['formulas_sources'][label];n=spec['n'];F=spec['original_clauses'];m=len(F)
        assert data['n']==n and data['m']==m
        is22=(all(len(c)==3 and len({abs(z) for z in c})==3 for c in F) and
              all(sum(l==v for c in F for l in c)==2 and sum(l==-v for c in F for l in c)==2 for v in range(1,n+1)))
        assert data['strict22']==is22
        for e,c in zip(data['source_extrema'],F):
            assert e['clause_id']>=1
            for v in e['signed_occurrences']:
                assert v['literal'] in c and v['S']==(v['literal']>0) and v['U']==(v['literal']<0)
                assert v['S']==v['invert_U'] and v['U']==v['invert_S']
                counts['extreme_occurrences']+=1
        assert len(data['pair_compatibility'])==m*(m-1)//2
        for rec in data['pair_compatibility']:
            C,D=F[rec['C_i']-1],F[rec['C_j']-1]
            assert rec['C_i']<rec['C_j']
            for mode in ('SS','SU','US','UU'):
                assert rec[mode]==exact_pair(C,D,mode), (label,rec,mode)
                counts['independent_pair_modes']+=1
        for endpoint,bit in [('ZERO',False),('ONE',True)]:
            v=[clause_count(c,{j:bit for j in range(1,n+1)}) for c in F]
            reported=data['endpoints'][endpoint]
            assert v==reported['true_counts']
            assert [v.count(k) for k in range(4)]==reported['N']
            assert reported['satisfied']==(not 0 in v)
            counts['endpoint_clauses']+=len(F)
        previous=0
        for t,r in enumerate(data['gray_trail']):
            mask=t^(t>>1)
            assert r['gray_mask']==mask
            flip=(mask^previous)
            assert r['flipped_var']==(flip.bit_length() if t else None)
            assignment={j:bool(mask&(1<<(j-1))) for j in range(1,n+1)}
            hist=collections.Counter(clause_count(c,assignment) for c in F)
            assert r['N']==[hist[k] for k in range(4)]
            assert r['satisfied']==(hist[0]==0)
            previous=mask;counts['gray_states']+=1
        res=data['forbidden_resolvent']
        if res:
            ca,cb=[F[j-1] for j in res['from_C']];v=res['pivot']
            assert (v in ca and -v in cb) or (-v in ca and v in cb)
            assert not any(-z in res['resolvent'] for z in res['resolvent'])
            assert set(map(int,res['forbidden_cube']))==set(map(abs,res['resolvent']))
            for bits in itertools.product((False,True),repeat=len({abs(z) for z in ca+cb})):
                vs=sorted({abs(z) for z in ca+cb});a=dict(zip(vs,bits))
                assert not (model_ok([ca,cb],a) and not model_ok([res['resolvent']],a))
                counts['resolution_local_assignments']+=1
        for f in ['baseline','controller']:
            d=data[f]
            if d is None:continue
            if d['label']=='SAT':
                a={i+1:bool(b) for i,b in enumerate(d['model'])}
                assert model_ok(F,a)
                counts['witness_checks']+=1
            else:
                assert d['label']=='UNSAT'
                if f=='baseline':tree_valid(d['proof'],F,{},counts)
        if n<=15:
            cnt=exact_models(F,n);assert cnt==data['exact_models']
            assert (cnt>0)==(data['controller']['label']=='SAT')
            counts['exhaustive_assignments']+=2**n
        if is22:
            assert m*3==n*4
            assert data['analytic_lb']=={'Krom':math.ceil(n/3),'Horn':math.ceil(n/3),'DualHorn':math.ceil(n/3)}
            assert data['explicit_pair_flags_bits']==2*m*(m-1)
            for typ,record in data['backdoors'].items():
                assert record.get('solver_status')==0
                B=record['set'];assert len(B)==record['size']==len(set(B))
                assert backdoor_matches(F,B,typ)
                assert len(B)>=math.ceil(n/3)
                counts['verified_backdoor_witnesses']+=1
                if n==15:
                    # Check all subsets smaller than reported optimum, not relying on MIP result.
                    for k in range(len(B)):
                        for z in itertools.combinations(range(1,n+1),k):
                            assert not backdoor_matches(F,z,typ)
                            counts['brute_smaller_backdoors']+=1
            if label.startswith('ORBIT_K') and 'SCRAMBLED' not in label:
                k=n//3
                assert data['backdoors']['Krom']['size']==k
                assert data['backdoors']['Horn']['size']==2*k
                assert data['backdoors']['DualHorn']['size']==2*k
        counts['sources']+=1
    return counts

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--input',default=str(HERE/'raw271.json'));p=parser.parse_args()
    c=verify(p.input)
    out={'PASS':True,'assertions_by_family':dict(sorted(c.items()))}
    (HERE/'verified271.json').write_text(json.dumps(out,sort_keys=True,indent=2)+'\n')
    print(json.dumps(out,indent=2))
