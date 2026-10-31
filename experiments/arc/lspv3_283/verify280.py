#!/usr/bin/env python3
"""Independent GATE280 verifier. Pure Python 3, no imports from producer.
Runs exhaustive source truth-tables and target grammar checks; optional --u
checks all six source-module UNSAT cofactors independently.
"""
import argparse, ast, collections, itertools, json, pathlib, random


def cvalue(c,a):
    return sum((a[abs(v)] == int(v>0)) for v in c)

def grammar(f,n):
    if not isinstance(f,list) or len(f)*3!=4*n:return False
    seen=set(); signed=collections.Counter()
    for c in f:
        if len(c)!=3 or any(type(x)!=int or abs(x)<1 or abs(x)>n for x in c):return False
        if len(set(map(abs,c)))!=3:return False
        if not (all(x>0 for x in c) or all(x<0 for x in c)):return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key)
        for x in c:signed[x]+=1
    return all(signed[k]==signed[-k]==2 for k in range(1,n+1))

def all_masks(n):
    for mask in range(1<<n):yield mask,[0]+[(mask>>(v-1))&1 for v in range(1,n+1)]

def brute(f,n):
    return [mask for mask,a in all_masks(n) if all(cvalue(c,a)>0 for c in f)]

def brute_modes(c,d,n):
    out={}
    for x,y in itertools.product('SU',repeat=2):
        wanted=(3 if x=='S' else 0,3 if y=='S' else 0)
        out[x+y]=any(cvalue(c,a)==wanted[0] and cvalue(d,a)==wanted[1]
                     for _,a in all_masks(n))
    return out

def edge_model_check(f,n,matching):
    return len(matching)==len(f)//4 and len(set(matching))==len(matching) and all(sum(x in matching for x in c)==1 for c in f if c[0]>0)

def independent_dpll(f,initial,n=198):
    # Separate from producer's implementation. Return complete UNSAT proof by full split.
    metrics=collections.Counter()
    init={abs(x):(x>0) for x in initial}
    if len(init)!=len(initial):raise AssertionError('repeated assumption')
    def recur(a):
        metrics['nodes']+=1
        a=dict(a)
        while True:
            metrics['clause_scans']+=len(f)
            pending=[];picked=None
            for cl in f:
                satisfied=False;open_lits=[]
                for l in cl:
                    if abs(l) not in a:open_lits.append(l)
                    elif a[abs(l)]==(l>0):satisfied=True;break
                if satisfied:continue
                if not open_lits:
                    metrics['conflicts']+=1
                    return False
                pending.append(open_lits)
                if len(open_lits)==1:picked=open_lits[0];break
            if picked is None:
                if not pending:return True
                tally=collections.Counter(abs(l) for row in pending for l in row)
                p=min(tally,key=lambda v:(-tally[v],v))
                for b in (False,True):
                    child=dict(a);child[p]=b
                    if recur(child):return True
                return False
            if abs(picked) in a:
                assert a[abs(picked)]!=(picked>0)
                return False
            a[abs(picked)]=(picked>0);metrics['units']+=1
    result=recur(init)
    return result,dict(metrics)

def proof_u(path):
    clauses=ast.literal_eval('\n'.join(t for t in pathlib.Path(path).read_text().splitlines() if t.strip() and not t.lstrip().startswith('#')))
    assert grammar(clauses,198)
    projections=[[-194,197],[-195,196,-198],[193,-195,-197],[195,-197],[193,194,-196],[-193,198]]
    details=[]
    for j,c in enumerate(projections):
        group=clauses[2+42*j:2+42*(j+1)]
        unsat,stats=independent_dpll(group,[-l for l in c])
        assert not unsat
        details.append({'module':j,'entailed_clause':c,**stats})
    core=projections+[clauses[0],clauses[1]]
    variables=list(range(193,199))
    accepts=0
    for mask in range(64):
        a={v:(mask>>i)&1 for i,v in enumerate(variables)}
        if all(any(a[abs(l)]==int(l>0) for l in c) for c in core):accepts+=1
    assert accepts==0
    return {'independent_unsat_certificate':'6 refuted module cofactors + 64 rejected boundary rows',
            'clauses':len(clauses),'n':198,'module_splits':details,'core_models':accepts,
            'total_module_nodes':sum(x['nodes'] for x in details)}

def verify(z):
    stats=collections.Counter()
    assert z['target']=='proper duplicate-free Monotone 3-SAT-(2,2)'
    for row in z['cases']:
        f=row['formula'];n=row['n'];assert grammar(f,n)
        assert row['m']==4*n//3
        models=brute(f,n);assert row['model_count']==len(models)
        assert row['decision']==('SAT' if models else 'UNSAT')
        if row['witness'] is not None:
            assert len(row['witness'])==n+1 and all(cvalue(c,row['witness'])>=1 for c in f)
        assert row['endpoint_zero_hist'][0]==len(f)//2
        assert row['endpoint_one_hist'][0]==len(f)//2
        for trail in row['trails']:
            mask=trail['mask'];a=[0]+[(mask>>(i-1))&1 for i in range(1,n+1)]
            h=[sum(cvalue(c,a)==t for c in f) for t in range(4)]
            assert trail['hist']==h and trail['complement_hist']==h[::-1]
            assert trail['sat']==(h[0]==0)
            stats['trail_checks']+=1
        for i,j in itertools.combinations(range(len(f)),2):
            checks=brute_modes(f[i],f[j],n)
            assert any(checks.values())
            stats['source_pair_modes']+=4
        plus=[set(c) for c in f if c[0]>0]
        q=sum(all(not({a,b}<=C) for a,b in itertools.combinations(map(abs,c),2) for C in plus) for c in f if c[0]<0)
        assert q==row['q']
        if row['factors'] is not None:
            assert all(edge_model_check(f,n,M) for M in row['factors'])
            assert set(v for M in row['factors'] for v in M)==set(range(1,n+1))
            assert sum(len(M) for M in row['factors'])==n
            if q<=2:
                assert any(all(cvalue(c,[0]+[int(v in M) for v in range(1,n+1)])>0 for c in f) for M in row['factors'])
            stats['factorized_sources']+=1
        stats['brute_assignments']+=1<<n
    for malformed in z['malformed']:
        assert malformed['rejected']
        stats['malformed_rejected']+=1
    x=next(t for t in z['cases'] if t['name']=='K33_ALL_SIX_MATCHINGS')
    f=x['formula'];n=x['n']
    positive=[set(c) for c in f if c[0]>0]
    matchings=[]
    for s in itertools.combinations(range(1,n+1),3):
        if all(len(set(s)&p)==1 for p in positive):matchings.append(s)
    assert len(matchings)==6
    negative={tuple(sorted(abs(v) for v in c)) for c in f if c[0]<0}
    assert set(matchings)==negative
    assert len(brute(f,n))==18
    stats['no_safe_matching_sat_counterexample']+=1
    def reject_bad_model():
        a=list(x['witness']);a[:]=[0]*(n+1)
        return not all(cvalue(c,a)>0 for c in f)
    assert reject_bad_model();stats['corrupt_model_rejected']+=1
    assert not grammar(f+[f[0]],n);stats['corrupt_duplicate_rejected']+=1
    assert not grammar([[-f[0][0],f[0][1],f[0][2]]]+f[1:],n);stats['corrupt_mixed_clause_rejected']+=1
    # Decoder is treated as the system under test. Every response is checked
    # by this verifier's separate exhaustive source evaluator.
    from gate280 import decide_encoded
    rng=random.Random(20261031)
    for row in z['cases']:
        n=row['n'];f=row['formula']
        for trial in range(6):
            perm=list(range(1,n+1));rng.shuffle(perm)
            flipped=(trial%2)==1
            g=[[((-1 if l<0 else 1)*(-1 if flipped else 1))*perm[abs(l)-1] for l in c] for c in f]
            rng.shuffle(g)
            for c in g:rng.shuffle(c)
            assert grammar(g,n)
            expected='SAT' if brute(g,n) else 'UNSAT'
            actual=decide_encoded(json.dumps({'n':n,'clauses':g}))
            assert actual['decision']==expected
            if expected=='SAT':assert all(cvalue(c,actual['witness'])>0 for c in g)
            stats['rename_and_global_sign_controls']+=1
    bad_jsons=['{}','{"n":6,"clauses":[]}', '{"n":3,"n":6,"clauses":[]}',
          '{"n":6,"clauses":null}', '{"n":6,"clauses":[],"extra":true}', 'not-json']
    for bad in bad_jsons:
        assert decide_encoded(bad)['decision']=='REJECT';stats['malformed_encoded_rejected']+=1
    return dict(stats)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--data',default='raw280.json');parser.add_argument('--u');parser.add_argument('--out',default='verification280.json')
    args=parser.parse_args();z=json.loads(pathlib.Path(args.data).read_text());stats=verify(z)
    if args.u:stats['independent_U198_UNSAT']=proof_u(args.u)
    pathlib.Path(args.out).write_text(json.dumps(stats,indent=2,sort_keys=True)+'\n')
    print(json.dumps(stats,indent=2,sort_keys=True))
