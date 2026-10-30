#!/usr/bin/env python3
"""Independent exhaustive verifier for source-indexed CLUSTER-LOG247 JSON shards.
No import from the producer; independent clause evaluation and proof-tree replay.
"""
import sys,json,itertools,collections,math,glob

def calc(F,a):
    t=[]
    for c in F:
        s=0
        for x in c:
            if a[abs(x)] == (x>0):s+=1
        t.append(s)
    return [t.count(k) for k in range(4)],t

def replay_unsat(F,node,assignment,counts):
    A=dict(assignment)
    for ev in node.get('units',[]):
        cid=ev['source_clause'];x=ev['forced_literal']; clause=F[cid-1]
        assert x in clause
        assert abs(x) not in A
        assert all(abs(y)!=abs(x) and abs(y) in A and A[abs(y)]!=(y>0) for y in clause if y!=x)
        A[abs(x)]=(x>0);counts['unit_events']+=1
    if 'conflicting_original_clause' in node:
        cid=node['conflicting_original_clause'];assert all(abs(x) in A and A[abs(x)]!=(x>0) for x in F[cid-1])
        assert {int(z):bool(v) for z,v in node['assignments'].items()}==A
        counts['verified_contradiction_leaves']+=1;return
    assert 'children' in node and 'decision' in node
    x=node['decision'];assert x not in A
    ch=node['children'];assert {int(val) for val,_ in ch}=={0,1} and len(ch)==2
    counts['branch_nodes']+=1
    for val,child in ch:
        B=dict(A);B[x]=bool(val);replay_unsat(F,child,B,counts)

def verify(path):
    raw=json.load(open(path));assert len(raw['cases'])==1
    rec=raw['cases'][0];F=rec['source_clauses'];n=rec['properties']['n'];m=len(F);r=rec['r'];test=collections.Counter()
    assert all(len(c)==3 and len({abs(x) for x in c})==3 for c in F)
    for b in (0,1):
        a={i:bool(b) for i in range(1,n+1)}
        assert calc(F,a)[0]==rec['endpoint_N'][b]
    if 'mandatory_source_audit' in rec:
        audit=rec['mandatory_source_audit']
        for j,row in enumerate(audit['clauses'],1):
            assert row['j']==j
            assert list(row['original_literals'])==list(F[j-1])
            for q,lit in zip(row['occurrences'],F[j-1]):
                assert q['variable']==abs(lit) and q['signed_occurrence']==lit
                assert q['S']==int(lit>0)==q['invert_U_to_S']
                assert q['U']==int(lit<0)==q['invert_S_to_U']
                test['occurrences']+=1
        for row in audit['pair_extreme_matrix']:
            i=row['j']-1;j=row['k']-1
            vs=sorted({abs(x) for x in F[i]+F[j]})
            actual={t:False for t in ('SS','SU','US','UU')}
            for bits in itertools.product((False,True),repeat=len(vs)):
                a=dict(zip(vs,bits));T1=sum(a[abs(x)]==(x>0) for x in F[i]);T2=sum(a[abs(x)]==(x>0) for x in F[j]);
                if T1 in (0,3) and T2 in (0,3):actual[('S' if T1==3 else 'U')+('S' if T2==3 else 'U')]=True
                test['local_pair_assignments']+=1
            assert actual==row['SS_SU_US_UU'];test['source_pairs']+=1
        for base,trail in audit['global_endpoint_flip_trails'].items():
            for event in trail:
                bits=event['values'];a={i:bits[i-1]=='1' for i in range(1,n+1)}
                N,ts=calc(F,a)
                assert N==event['N'] and ts==event['t_by_original_clause']
                comp={i:not x for i,x in a.items()}
                assert calc(F,comp)[0]==N[::-1]
                test['coherent_flip_trails']+=1
    if rec['resolution_cube'] is not None:
        rr=rec['resolution_cube'];cube={int(v):bool(x) for v,x in rr['forbidden_cube'].items()}
        for val in (False,True):
            a=dict(cube);a[rr['pivot']]=val
            assert any(all(abs(x) in a and a[abs(x)]!=(x>0) for x in F[c-1]) for c in rr['parents'])
        test['source_parent_resolvent_certificates']+=1
    result={tuple(row['N']):row['count'] for row in rec['histogram']}
    assert sum(result.values())==math.comb(n,r)
    # Full radius check independently, no access to producer internals.
    observed=collections.Counter()
    for S in itertools.combinations(range(1,n+1),r):
        a={i:(i in S) for i in range(1,n+1)};observed[tuple(calc(F,a)[0])]+=1
        test['radius_exhaustive_assignments']+=1
    assert dict(observed)==result
    if rec.get('complete_original_source_unsat_tree') is not None:
        c=collections.Counter();replay_unsat(F,rec['complete_original_source_unsat_tree'],{},c)
        assert c['verified_contradiction_leaves']==rec['baseline_proof_tree_leaf_count']
        test.update(c)
        if n<=15:
            for mask in range(1<<n):
                a={i:bool(mask>>(i-1)&1) for i in range(1,n+1)}
                assert calc(F,a)[0][0]>0;test['full_UNSAT_truth_table_assignments']+=1
    else:
        witness=rec.get('baseline_witness')
        if witness is not None:
            a={int(k):bool(v) for k,v in witness.items()}
            assert calc(F,a)[0][0]==0
            test['verified_SAT_witnesses']+=1
    assert rec['hybrid_SAT']==rec['baseline_dpll_SAT'] if 'hybrid_SAT' in rec else True
    return dict(name=rec['name'],radius=r,n=n,verified=dict(test),cluster_time=rec['connected_elapsed_s'],direct_time=rec.get('explicit_elapsed_s'),cluster_peak_B=rec['connected_peak_python_B'],direct_peak_B=rec.get('explicit_peak_python_B'),cluster_supports=rec['connected_details']['connected_supports'],histogram_buckets=rec['connected_details']['histogram_buckets'])

if __name__=='__main__':
    files=sys.argv[1:] or sorted(glob.glob('*.json'))
    out=[]
    for f in files:
        v=verify(f);out.append(v);print('VERIFIED',v['name'],v['n'],v['radius'],v['verified'],flush=True)
    with open('CONNECTED_LOG_FLIPS247_independent_summary.json','w') as o:json.dump(out,o,indent=2)