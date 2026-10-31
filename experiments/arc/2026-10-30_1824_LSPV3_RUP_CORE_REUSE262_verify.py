#!/usr/bin/env python3
"""Independent checker: no imports from producer. Replays RUP + UNSAT trees.
Call python arc262_verify.py --raw raw.json --group 0
Group 0: repeated family; 1: W1/SWAP6 and controls; 2: random.
"""
import json,argparse,itertools,collections,sys,time

def lit_val(l,a):
    return None if abs(l) not in a else int(l>0)==a[abs(l)]

def up(F, assumptions):
    a={}
    for l in assumptions:
        v=abs(l);b=int(l>0)
        if v in a and a[v]!=b:return None
        a[v]=b
    while True:
        changed=False
        for c in F:
            if any(lit_val(l,a) is True for l in c):continue
            rem=[l for l in c if abs(l) not in a]
            if not rem:return None
            if len(rem)==1:
                l=rem[0]
                if abs(l) in a:assert a[abs(l)]==int(l>0)
                else:a[abs(l)]=int(l>0);changed=True;break
        if not changed:return a

def satisfy(F,a):
    return all(any(lit_val(l,a) is True for l in c) for c in F)

def check_tree(F,learned,tree,desired,proof_stats):
    all_db=F+learned
    def rec(node,path):
        proof_stats['tree_nodes']+=1
        if node['kind']=='sat':
            assert desired
            w={int(k):v for k,v in node['witness'].items()}
            assert satisfy(F,w)
            return True
        if node['kind']=='conflict':
            assert [int(z) for z in node['decisions']]==path
            assert up(all_db,path) is None
            proof_stats['tree_conflict_leaves']+=1
            return False
        assert node['kind']=='branch'
        v=node['variable']
        assert v>0 and v not in {abs(l) for l in path}
        children=node['children']
        assert len(children) in (1,2)
        results=[]
        for j,kid in enumerate(children):results.append(rec(kid,path+[v if j else -v]))
        if len(children)==1:assert results==[True]
        else:assert results in ([False,False],[False,True])
        return any(results)
    assert rec(tree,[])==desired

def check_proof(F,rec,truth,st):
    db=list(F)
    for p in rec['proofs']:
        c=tuple(int(x) for x in p['clause']);core=p['core']
        assert p['parent_db_size']==len(db)
        assert len({abs(x) for x in c})==len(c)
        assert set(c)=={-l for l in core}
        assert up(db,[-l for l in c]) is None
        db.append(c)
        st['rup_clauses']+=1
        st['rup_literals']+=len(c)
    assert [list(c) for c in db[len(F):]]==rec['learned_clauses']
    w=rec['witness'];assert (w is not None)==truth
    if truth:
        w={int(k):int(v) for k,v in w.items()};assert satisfy(F,w)
        st['verified_witnesses']+=1
    if rec['tree'] is not None:check_tree(F,db[len(F):],rec['tree'],truth,st)
    assert rec['selected_events']==sum(rec['counter'].values())
    assert rec['peak_clause_count']>=len(db)
    assert rec['peak_approx_live_bits']>=0

def check_audit(F,n,A,st):
    assert all(len(c)==3 and len({abs(l) for l in c})==3 for c in F)
    assert A['applicable']
    assert len(A['per_clause_targets'])==len(F)
    for j,c in enumerate(F):
        record=A['per_clause_targets'][j];assert record['j']==j+1
        s={str(abs(l)):int(l>0) for l in c};u={v:1-b for v,b in s.items()}
        assert record['S']==s and record['U']==u and record['not_S_is_U']==u and record['not_U_is_S']==s
        for l,o in zip(c,record['signed_occurrences']):
            assert o['x']==abs(l) and o['sign']==(1 if l>0 else -1)
            assert o['S']==int(l>0) and o['U']==int(l<0)
            assert o['invert_S_to_U']==o['U'] and o['invert_U_to_S']==o['S']
            st['source_occurrence_checks']+=1
    def compatible(c,d,mode):
        a={}
        for clause,typ in ((c,mode[0]),(d,mode[1])):
            for l in clause:
                v=abs(l);b=int(l>0) if typ=='S' else int(l<0)
                if v in a and a[v]!=b:return False
                a[v]=b
        return True
    for pair in A['pair_matrix']:
        j,k=pair['clauses'];expected=[int(compatible(F[j-1],F[k-1],mode)) for mode in ('SS','SU','US','UU')]
        assert expected==pair['SS_SU_US_UU']
        support=sorted({abs(l) for c in (F[j-1],F[k-1]) for l in c})
        for mode,flag in zip(('SS','SU','US','UU'),expected):
            found=False
            for bits in itertools.product((0,1),repeat=len(support)):
                a=dict(zip(support,bits));counts=[sum(a[abs(l)]==int(l>0) for l in F[t-1]) for t in (j,k)]
                if all(q==(3 if m=='S' else 0) for q,m in zip(counts,mode)):
                    found=True;break
            assert found==bool(flag)
            st['pair_mode_enumerations']+=1
    for label,value in (('zero',0),('one',1)):
        a={v:value for v in range(1,n+1)}
        q=[sum(a[abs(l)]==int(l>0) for l in c) for c in F]
        assert A['endpoints'][label]['per_clause']==q
        assert A['endpoints'][label]['N']==[q.count(x) for x in range(4)]
    a={v:0 for v in range(1,n+1)}
    for tr in A['flip_trail']:
        a[tr['flip']]^=1
        q=[sum(a[abs(l)]==int(l>0) for l in c) for c in F]
        qc=[sum((1-a[abs(l)])==int(l>0) for l in c) for c in F]
        assert all(x+y==3 for x,y in zip(q,qc))
        assert tr['statuses']==[q.count(x) for x in range(4)]
        assert tr['complement_statuses']==[qc.count(x) for x in range(4)]
        st['coherent_flip_controls']+=1

def main():
    par=argparse.ArgumentParser();par.add_argument('--raw',default='raw.json');par.add_argument('--group',type=int,default=0);par.add_argument('--output',default=None);a=par.parse_args()
    dat=json.load(open(a.raw));assert dat['name']=='RUP-CORE-REUSE262'
    st=collections.Counter();start=time.monotonic()
    for z in dat['cases']:
        name=z['name']
        group=2 if name.startswith('random') else 0 if name.startswith('repeat') else 1
        if group!=a.group:continue
        F=[tuple(c) for c in z['source']];n=z['n']
        if z['model_count_oracle'] is not None:
            models=0
            for bits in itertools.product((0,1),repeat=n):
                aa=dict(enumerate(bits,1))
                if satisfy(F,aa):models+=1
            assert models==z['model_count_oracle']
            assert (models>0)==z['SAT']
            st['independent_truth_tables']+=1
        if z.get('controller'):assert z['controller']['SAT']==z['SAT']
        for mode,rec in z['solver'].items():
            check_proof(F,rec,z['SAT'],st)
            st['solver_mode_checks']+=1
            if mode=='min':
                for c in rec['learned_clauses']:
                    pass
        if name in dat['source_audits']:
            check_audit(F,n,dat['source_audits'][name],st)
        st['formulas']+=1
    assert a.group in (0,1,2)
    if a.group==1:
        old=dat['stale_cache_control'];F=[tuple(c) for c in old['F']]
        old_a=up(F,old['assumptions_old']);new_a=up(F,old['assumptions_new'])
        assert {int(k):v for k,v in old['old_UP_assignment'].items()}==old_a
        assert new_a is None and old['new_UP_conflict']
        st['stale_cache_counterexample']=1
    result={'run':'RUP-CORE-REUSE262','group':a.group,'checks':dict(st),'seconds':time.monotonic()-start,'passed':True}
    print(json.dumps(result,indent=2,sort_keys=True))
    if a.output:open(a.output,'w').write(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
