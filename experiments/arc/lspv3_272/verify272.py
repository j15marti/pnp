#!/usr/bin/env python3
"""Independent SAT/source certificate and interface-checking verifier; no run272 import."""
import sys,json,collections,itertools,hashlib,time

def truth(l,a):return a[abs(l)]==(l>0)
def sat(clauses,a):return all(any(truth(l,a) for l in c) for c in clauses)

def reference_dpll(C,n,partial=None):
    def dfs(A):
        while True:
            altered=False
            for c in C:
                u=[l for l in c if abs(l) not in A]
                if any(abs(l) in A and A[abs(l)]==(l>0) for l in c):continue
                if not u:return None
                if len(u)==1:
                    l=u[0];v=abs(l);x=l>0
                    if v in A and A[v]!=x:return None
                    if v not in A:A[v]=x;altered=True
            if not altered:break
        if all(any(abs(l) in A and A[abs(l)]==(l>0) for l in c) for c in C):
            full={j:A.get(j,False) for j in range(1,n+1)}
            return full if sat(C,full) else None
        for c in C:
            if any(abs(l) in A and A[abs(l)]==(l>0) for l in c):continue
            free=[abs(l) for l in c if abs(l) not in A]
            if free: v=free[-1];break
        for x in (True,False):
            B=dict(A);B[v]=x
            m=dfs(B)
            if m is not None:return m
        return None
    return dfs(dict(partial or {}))

def proof_res(c,d,p):
    assert p in c and -p in d
    u=set(c)|set(d);u.remove(p);u.remove(-p)
    assert all(-l not in u for l in u)
    return u

def verify_source(obj):
    n=obj['n'];C=obj['clauses'];m=len(C);assert m==obj['m'];assert all(1<=abs(l)<=n and len(set(map(abs,c)))==len(c) for c in C for l in c)
    witness=obj['certificate']['witness'];proof=obj['certificate']['resolution']
    if obj['actual_sat']:
        assert witness is not None and proof is None
        a={int(k):bool(v) for k,v in witness.items()};assert len(a)==n and sat(C,a)
    else:
        assert witness is None
        if proof:
            dag={i+1:tuple(c) for i,c in enumerate(C)}
            for step in proof:
                i=step['id'];x,y=step['parents'];p=step['pivot']
                assert i not in dag and x in dag and y in dag
                assert p in dag[x] and -p in dag[y]
                q=set(dag[x]);r=set(dag[y]);q.remove(p);r.remove(-p)
                res=q|r
                assert all(-l not in res for l in res)
                actual=tuple(sorted(res,key=lambda l:(abs(l),l<0)))
                assert actual==tuple(step['clause'])
                dag[i]=actual
            assert dag[proof[-1]['id']]==()
    for cert in obj['certificate']['forbidden_cubes']:
        target=cert['unit_literal'];ids=cert['source_clause_ids'];free=sorted(cert['free_variables'])
        assert len(ids)==4 and len(set(ids))==4 and len(free)==2
        assert cert['forbidden_cube']=={str(abs(target)):int(target<0)}
        src=[C[j-1] for j in ids]
        assert all(target in c and set(map(abs,c))=={abs(target),*free} for c in src)
        u,v=free
        def find(x,y):
            for c in src:
                if x*u in c and y*v in c:return c
            raise AssertionError('missing sign combination')
        a=proof_res(find(1,1),find(1,-1),v)
        b=proof_res(find(-1,1),find(-1,-1),v)
        assert proof_res(a,b,u)=={target}
    return len(proof or [])

def verify_source_controls(obj):
    n=obj['n'];C=obj['clauses'];R=obj['source_controls'];m=len(C)
    for key,bit in [('all_zero',False),('all_one',True)]:
        a={i:bit for i in range(1,n+1)}
        t=[sum(truth(l,a) for l in c) for c in C]
        z=R['endpoints'][key]
        assert z['clause_true_counts']==t
        assert z['histogram']==[t.count(j) for j in range(4)]
        assert z['satisfied']==all(x>0 for x in t)
    assert len(R['extrema'])==m
    for j,e in enumerate(R['extrema']):
        assert e['j']==j+1
        for occ,l in zip(e['occurrences'],C[j]):
            assert occ['signed_literal']==l and occ['variable']==abs(l)
            assert occ['local_S_value']==(l>0)
            assert occ['local_U_value']==(l<0)
            assert occ['invert_S_value']==(l<0)
            assert occ['invert_U_value']==(l>0)
    pairid=0
    for j in range(m):
        for k in range(j+1,m):
            q=R['compatibility'][pairid];pairid+=1
            assert (q['j'],q['k'])==(j+1,k+1)
            vars=sorted(set(map(abs,C[j]+C[k])))
            seen={s:False for s in ('SS','SU','US','UU')}
            for bits in itertools.product([False,True], repeat=len(vars)):
                a=dict(zip(vars,bits));counts=[sum(truth(l,a) for l in C[t]) for t in (j,k)]
                for t0 in 'SU':
                    for t1 in 'SU':
                        if counts[0]==(len(C[j]) if t0=='S' else 0) and counts[1]==(len(C[k]) if t1=='S' else 0):seen[t0+t1]=True
            assert seen==q['flags'],(obj['name'],j,k,seen,q['flags'])
    assert pairid==len(R['compatibility'])
    for item in R['gray']:
        v=item['assignment_int'];a={i:bool((v>>(i-1))&1) for i in range(1,n+1)}
        t=[sum(truth(l,a) for l in c) for c in C]
        comp={i:not x for i,x in a.items()}
        tc=[sum(truth(l,comp) for l in c) for c in C]
        assert item['true_counts']==t
        assert item['complement_true_counts']==tc
        assert all(tc[j]==len(C[j])-t[j] for j in range(m))
        assert item['sat']==all(x>0 for x in t)
    return pairid,len(R['gray'])

def verify_dp(obj):
    if obj['oracle_dp'] is None:return 0
    C=obj['clauses'];G=[C[j-1] for j in obj['G']];H=[C[j-1] for j in obj['H']]
    iface=sorted({abs(l) for c in G for l in c}&{abs(l) for c in H for l in c})
    assert len(iface)==obj['b']
    calls=0
    for bits in itertools.product([False,True],repeat=len(iface)):
        calls+=1;partial=dict(zip(iface,bits))
        g=reference_dpll(G,obj['n'],partial)
        if g is None:continue
        h=reference_dpll(H,obj['n'],partial)
        if h is None:continue
        witness={i:False for i in range(1,obj['n']+1)}
        witness.update({abs(l):g[abs(l)] for c in G for l in c})
        witness.update({abs(l):h[abs(l)] for c in H for l in c})
        witness.update(partial)
        assert sat(C,witness)
        break
    assert calls==obj['oracle_dp']['events']['boundary_candidates']
    return calls

def verify_result(data):
    cnt=collections.Counter()
    for o in data['results']:
        C=o['clauses']
        ps=verify_source(o)
        pairs,gray=verify_source_controls(o)
        calls=verify_dp(o)
        basemodel=reference_dpll(C,o['n'])
        assert (basemodel is not None)==o['actual_sat'],o['name']
        cnt['sources']+=1;cnt['sat' if o['actual_sat'] else 'unsat']+=1
        cnt['resolution_steps']+=ps;cnt['extreme_pairs']+=pairs;cnt['gray_states']+=gray;cnt['boundary_candidates']+=calls
        if o['n']<=10:
            models=sum(sat(C,{j:bool((i>>(j-1))&1) for j in range(1,o['n']+1)}) for i in range(1<<o['n']))
            assert (models>0)==o['actual_sat'];cnt['exhaustive_complete_assignments']+=(1<<o['n'])
    return dict(cnt)

def main():
    path=sys.argv[1] if len(sys.argv)>1 else 'raw272.json'
    data=json.loads(open(path).read());t=time.perf_counter();stats=verify_result(data)
    # Deliberate record corruption, independently caught.
    import copy
    src=data['results'][0];bad=copy.deepcopy(src)
    bad['source_controls']['compatibility'][0]['flags']['SS']=not bad['source_controls']['compatibility'][0]['flags']['SS']
    try:verify_source_controls(bad)
    except AssertionError:stats['corrupt_compatibility_rejected']=1
    else:raise AssertionError('compatibility corruption not caught')
    src=next(o for o in data['results'] if o['certificate']['resolution']);bad=copy.deepcopy(src)
    bad['certificate']['resolution'][-1]['clause']=[1]
    try:verify_source(bad)
    except AssertionError:stats['corrupt_proof_rejected']=1
    else:raise AssertionError('proof corruption not caught')
    src=next(o for o in data['results'] if o['certificate']['witness']);bad=copy.deepcopy(src)
    w=bad['certificate']['witness'];k=next(iter(w));w[k]=1-int(w[k]);
    try:verify_source(bad)
    except AssertionError:stats['corrupt_witness_rejected']=1
    else:raise AssertionError('witness corruption not caught')
    src=next(o for o in data['results'] if o['certificate']['forbidden_cubes']);bad=copy.deepcopy(src)
    bad['certificate']['forbidden_cubes'][0]['source_clause_ids'][0]=0
    try:verify_source(bad)
    except (AssertionError,IndexError):stats['corrupt_forbidden_cube_rejected']=1
    else:raise AssertionError('forbidden cube corruption not caught')
    stats['raw_sha256']=hashlib.sha256(open(path,'rb').read()).hexdigest();stats['elapsed_sec']=time.perf_counter()-t
    print(json.dumps(stats,indent=2,sort_keys=True))
    return stats
if __name__=='__main__':main()
