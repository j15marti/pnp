#!/usr/bin/env python3
"""ARC236: source-authenticated ternary-message hitting-cover research reproducer.
Standard-library only. Proof applies to verified module trees; this executable
implements an exact star-tree special case with rank-one XOR3 leaves.
The program is NOT a polynomial-time general SAT solver.
"""
import argparse, itertools, json, math, random, hashlib, time
from collections import Counter


def serialize(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':')).encode('utf-8')

def truth_clause(clause, assignment):
    return any((assignment[abs(l)] == int(l > 0)) for l in clause)

def parse_star(src):
    n=src['n']; assert isinstance(n,int) and n>=3
    ids=set(); selectors=set(); clauses=[]
    for item in src['root_clauses']:
        c=tuple(item)
        assert 0<=len(c)<=2 and all(1<=abs(x)<=n and x!=0 for x in c)
        clauses.append(c)
    for leaf in src['leaves']:
        sid=leaf['source_id']; assert isinstance(sid,int) and sid>=0 and sid not in ids
        ids.add(sid)
        c=tuple(leaf['source_clause']); sel=tuple(leaf['selectors'])
        assert len(c)==len(sel)==3 and len({abs(x) for x in c})==3
        assert all(1<=abs(x)<=n for x in c)
        assert len(set(sel))==3 and all(s>n and s not in selectors for s in sel)
        selectors.update(sel)
        assert leaf['xor_rhs']==1
        assert [list((-s,l)) for s,l in zip(sel,c)] == leaf['implications']
    return n,clauses

def make_star(n, ternary, root=()):
    leaves=[]
    for j,c0 in enumerate(ternary):
        c=tuple(c0); sel=(n+3*j+1,n+3*j+2,n+3*j+3)
        leaves.append(dict(source_id=j,source_clause=list(c),selectors=list(sel),
                           xor_rhs=1,implications=[[-s,l] for s,l in zip(sel,c)]))
    return dict(n=n,root_clauses=[list(c) for c in root],leaves=leaves)

def leaf_table(leaf):
    c=tuple(leaf['source_clause']); sel=tuple(leaf['selectors']); scope=tuple(abs(x) for x in c)
    rel=set()
    for bits in itertools.product((0,1),repeat=3):
        a={v:b for v,b in zip(scope,bits)}
        for sbits in itertools.product((0,1),repeat=3):
            if (sum(sbits)%2)!=leaf['xor_rhs']: continue
            if all((not sbits[i]) or truth_clause((c[i],),a) for i in range(3)):
                rel.add(bits); break
    return scope,frozenset(rel)

def forbidden_tuple_clauses(scope,rel):
    assert len(scope)<=2
    return [tuple(v if b==0 else -v for v,b in zip(scope,bits))
            for bits in itertools.product((0,1),repeat=len(scope)) if bits not in rel]

def valid_binary_clauses(scope, rel):
    cand=[]
    for i,v in enumerate(scope):
        for s in (1,-1):
            c=(s*v,)
            if all(truth_clause(c,{z:b for z,b in zip(scope,point)}) for point in rel):cand.append(c)
    for i,j in itertools.combinations(range(len(scope)),2):
        for si,sj in itertools.product((1,-1),repeat=2):
            c=(si*scope[i],sj*scope[j])
            if all(truth_clause(c,{z:b for z,b in zip(scope,point)}) for point in rel):cand.append(c)
    return cand

def rel_is_2cnf(scope, rel):
    cs=valid_binary_clauses(scope,rel)
    witness=frozenset(point for point in itertools.product((0,1),repeat=len(scope))
        if all(truth_clause(c,{v:b for v,b in zip(scope,point)}) for c in cs))
    return witness==rel,cs

def pin_relation(scope,rel,pins):
    rem=tuple(v for v in scope if v not in pins)
    rel2=frozenset(tuple(bits[i] for i,v in enumerate(scope) if v not in pins)
        for bits in rel if all(bits[i]==pins[v] for i,v in enumerate(scope) if v in pins))
    return rem,rel2

def two_sat(n,clauses,stats):
    stats['two_sat_calls']+=1
    g=[[] for _ in range(2*n)]; gr=[[] for _ in range(2*n)]
    def idx(lit):return 2*(abs(lit)-1)+(1 if lit>0 else 0)
    def edge(a,b):
        v=idx(a); w=idx(b); g[v].append(w);gr[w].append(v);stats['implication_edges']+=1
    for clause in clauses:
        stats['charged_clauses']+=1
        if len(clause)==0:return None
        if len(clause)==1:edge(-clause[0],clause[0])
        elif len(clause)==2:
            a,b=clause;edge(-a,b);edge(-b,a)
        else:raise ValueError('not 2CNF')
    seen=[False]*(2*n);order=[]
    for start in range(2*n):
        if seen[start]:continue
        stack=[(start,0)];seen[start]=True
        while stack:
            v,k=stack[-1]
            if k==len(g[v]):order.append(v);stack.pop();continue
            stack[-1]=(v,k+1);w=g[v][k]
            if not seen[w]:seen[w]=True;stack.append((w,0))
    comp=[-1]*(2*n);cid=0
    for start in reversed(order):
        if comp[start]>=0:continue
        todo=[start];comp[start]=cid
        while todo:
            v=todo.pop()
            for w in gr[v]:
                if comp[w]<0:comp[w]=cid;todo.append(w)
        cid+=1
    a={v:int(comp[2*(v-1)+1]>comp[2*(v-1)]) for v in range(1,n+1)}
    if any(comp[2*(v-1)+1]==comp[2*(v-1)] for v in range(1,n+1)):
        return None
    assert all(truth_clause(c,a) for c in clauses)
    return a

def hit_cover(edges,cap,stats):
    edges=tuple(sorted(set(tuple(sorted(e)) for e in edges)))
    def dfs(selected,remaining):
        stats['cover_search_nodes']+=1
        unhit=next((e for e in edges if not set(e).intersection(selected)),None)
        if unhit is None:return selected
        if remaining==0:return None
        for v in unhit:
            res=dfs(selected+(v,),remaining-1)
            if res is not None:return res
        return None
    for k in range(cap+1):
        ans=dfs(tuple(),k)
        if ans is not None:return tuple(sorted(set(ans)))
    return None

def solve_star(src,cap=5):
    n,root=parse_star(src)
    stats=Counter();stats['physical_input_bytes']=len(serialize(src))
    stats['source_clause_count']=len(root)+len(src['leaves'])
    tables=[];bad=[]
    for leaf in src['leaves']:
        scope,rel=leaf_table(leaf)
        assert rel == frozenset(bits for bits in itertools.product((0,1),repeat=3)
                                    if any((bits[i]==int(l>0)) for i,l in enumerate(leaf['source_clause'])))
        good,compiled=rel_is_2cnf(scope,rel)
        tables.append((scope,rel,good,compiled))
        if not good:bad.append(tuple(sorted(scope)))
    stats['bad_child_messages']=len(bad)
    union=set(v for e in bad for v in e)
    stats['exceptional_union']=len(union)
    cover=hit_cover(bad,cap,stats)
    if cover is None:
        return {'status':'UNKNOWN_COVER_EXCEEDS_CAP','stats':dict(stats)}
    stats['cover_size']=len(cover)
    for bits in itertools.product((0,1),repeat=len(cover)):
        pins=dict(zip(cover,bits));clauses=list(root)
        clauses.extend((v if bit else -v,) for v,bit in pins.items())
        for scope,rel,good,compiled in tables:
            if good:clauses.extend(compiled)
            else:
                rem,r2=pin_relation(scope,rel,pins)
                assert len(rem)<=2
                clauses.extend(forbidden_tuple_clauses(rem,r2))
        a=two_sat(n,clauses,stats)
        if a is not None:
            assert all(truth_clause(c,a) for c in root)
            assert all(truth_clause(l['source_clause'],a) for l in src['leaves'])
            # Reconstruct actual private selectors and verify their XOR + implications.
            witness=dict(a)
            for leaf in src['leaves']:
                true_idxs=[i for i,l in enumerate(leaf['source_clause']) if truth_clause((l,),a)]
                assert true_idxs
                for i,s in enumerate(leaf['selectors']):witness[s]=int(i==true_idxs[0])
                assert sum(witness[s] for s in leaf['selectors'])%2 ==1
                assert all((witness[s]==0 or truth_clause((l,),witness))
                            for s,l in zip(leaf['selectors'],leaf['source_clause']))
            stats['reconstructed_selector_bits']=3*len(src['leaves'])
            return {'status':'SAT','assignment':{str(i):a[i] for i in sorted(a)},'stats':dict(stats)}
    stats['exhausted_assignments']=2**len(cover)
    return {'status':'UNSAT','stats':dict(stats)}

def brute_source(src):
    n,root=parse_star(src)
    F=root+[tuple(l['source_clause']) for l in src['leaves']]
    for bits in itertools.product((0,1),repeat=n):
        a={i+1:b for i,b in enumerate(bits)}
        if all(truth_clause(c,a) for c in F):return a
    return None

def shared_center_family(q,unsat=False):
    assert q>=2
    z=1; n=2*q+1
    leaves=[]
    for i in range(q):
        a,b=2*i+2,2*i+3
        leaves.append((-z,a,b) if i==1 else (z,a,b))
    root=[(-2,),(-3,),(-4,),((-5,) if unsat else (5,))]
    return make_star(n,leaves,root)

def run(seed=2361029):
    rng=random.Random(seed)
    out={'seed':seed,'script_version':'ARC236-v1','tests':{},'large':[], 'controls':{}}
    count_2cnf=0;pin_slices=0;nonbij=[]
    scope=(1,2,3)
    for mask in range(256):
        rel=frozenset(bits for i,bits in enumerate(itertools.product((0,1),repeat=3)) if mask>>i&1)
        ok,_=rel_is_2cnf(scope,rel)
        count_2cnf+=ok
        if not ok:nonbij.append(mask)
        for v in scope:
            for bit in (0,1):
                rem,rr=pin_relation(scope,rel,{v:bit})
                cls=forbidden_tuple_clauses(rem,rr)
                for bits in itertools.product((0,1),repeat=2):
                    a=dict(zip(rem,bits)); assert (bits in rr)==all(truth_clause(c,a) for c in cls)
                pin_slices+=1
    out['tests']['ternary_relation_masks']=256
    out['tests']['bijunctive_ternary_relations']=count_2cnf
    out['tests']['all_pinned_ternary_slices']=pin_slices
    out['tests']['nonbijunctive_masks']=len(nonbij)
    assert count_2cnf==166
    # Exhaust all eight signed proper clauses subsets on exactly 3 vars.
    signed=[tuple(sign*(i+1) for i,sign in enumerate(signs)) for signs in itertools.product((1,-1),repeat=3)]
    ctr=Counter()
    for subset in range(256):
        src=make_star(3,[signed[i] for i in range(8) if subset>>i&1]);res=solve_star(src,cap=3)
        correct=brute_source(src)
        assert (res['status']=='SAT') == (correct is not None), (subset,res)
        ctr[res['status']]+=1
    out['tests']['exhaustive_3var_signed_clause_subsets']=dict(ctr)
    ctr=Counter();st=[]
    for test_i in range(600):
        n=rng.randint(3,10)
        cs=[]
        for j in range(rng.randint(0,16)):
            v=rng.sample(range(1,n+1),3)
            cs.append(tuple(x if rng.randrange(2) else -x for x in v))
        root=[]
        for j in range(rng.randint(0,6)):
            v=rng.sample(range(1,n+1),rng.randint(1,2))
            root.append(tuple(x if rng.randrange(2) else -x for x in v))
        src=make_star(n,cs,root)
        res=solve_star(src,cap=4);correct=brute_source(src)
        assert res['status'] in ('SAT','UNSAT'),(test_i,res)
        assert (res['status']=='SAT') == (correct is not None), (test_i,src,res)
        ctr[res['status']]+=1;st.append(res['stats'])
    out['tests']['randomized_source_compares']=dict(ctr)
    out['tests']['randomized_max_cover_search_nodes']=max(s['cover_search_nodes'] for s in st)
    for q in (16,32,64,128,256):
        for unsat in (False,True):
            src=shared_center_family(q,unsat)
            t0=time.monotonic();ans=solve_star(src,cap=1);elapsed=time.monotonic()-t0
            assert ans['status']==('UNSAT' if unsat else 'SAT')
            assert ans['stats']['cover_size']==1
            assert ans['stats']['bad_child_messages']==q
            assert ans['stats']['exceptional_union']==2*q+1
            out['large'].append(dict(q=q,source_state='UNSAT' if unsat else 'SAT',status=ans['status'],
                                     seconds=round(elapsed,6),**ans['stats']))
    # Bounded h is sufficient, never necessary. Disjoint leaf relations are trivial independently.
    q=8;disjoint=make_star(3*q,[(3*i+1,3*i+2,3*i+3) for i in range(q)])
    reject=solve_star(disjoint,cap=3)
    assert reject['status']=='UNKNOWN_COVER_EXCEEDS_CAP'
    out['controls']['disjoint_easy_source_cap_rejection']={'q':q,'status':reject['status'],
                  'fact':'SAT by setting first variable of each triple true; cover size q'}
    # Source-authenticity tampering controls.
    base=shared_center_family(3,False)
    for mode in ('xor_rhs','implication','duplicated_source_id','selector'):
        tampered=json.loads(serialize(base))
        if mode=='xor_rhs':tampered['leaves'][0]['xor_rhs']=0
        elif mode=='implication':tampered['leaves'][0]['implications'][0][0]=1
        elif mode=='duplicated_source_id':tampered['leaves'][1]['source_id']=0
        else:tampered['leaves'][1]['selectors'][0]=tampered['leaves'][0]['selectors'][0]
        try:solve_star(tampered,cap=2)
        except AssertionError:pass
        else:raise AssertionError('forged source accepted: '+mode)
    out['controls']['forged_sources_rejected']=4
    # n=1200 exact static architecture PROXY: integer relaxation only, not realizable proof.
    n=1200;rows=[]
    for b in range(1,n+1):
        q=max(0,math.ceil((n-3*b)/(12*b)))
        rows.append((b,q,b+q))
    floor=min(v for _,_,v in rows)
    out['controls']['static_proxy_n1200']={'min_log2_exponent':floor,
        'minimizing_b':[b for b,q,v in rows if v==floor],
        'first_lexponent_equality_b':min(b for b,q,v in rows if q==0)}
    assert floor==20 and [b for b,q,v in rows if v==floor]==[9,10,11]
    assert min(b for b,q,v in rows if q==0)==400
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',default='ARC236_results.json');ap.add_argument('--seed',type=int,default=2361029)
    args=ap.parse_args();out=run(args.seed)
    with open(args.out,'w',encoding='utf-8') as f:json.dump(out,f,indent=2,sort_keys=True)
    print(json.dumps({'sha256_results':hashlib.sha256(open(args.out,'rb').read()).hexdigest(),
             'tests':out['tests'],'large_cases':len(out['large']),'controls':out['controls']},indent=2))
