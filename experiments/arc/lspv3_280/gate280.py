#!/usr/bin/env python3
"""LSPV-3 GATE280: exact monotone 2P2N 3SAT, cubic dual and safe factors.
Python 3 standard library.  Run: python gate280.py [--u path] [--output path].
Do not infer global hardness, target closure or FLMV upper bounds from any result.
"""
import argparse, ast, collections, itertools, json, math, tracemalloc
from pathlib import Path

P6 = [(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
QY = [(1,2,4),(1,3,6),(2,3,5),(4,5,6)]
P9 = [(1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9)]
Q0 = [(2,4,7),(1,6,9),(4,5,6),(3,7,8),(1,5,8),(2,3,9)]
Q1 = [(5,7,9),(2,4,8),(1,2,3),(1,5,9),(3,4,6),(6,7,8)]
Q2 = [(4,5,8),(3,5,7),(2,4,9),(1,2,6),(1,6,9),(3,7,8)]
Q3 = [(2,7,8),(3,5,7),(1,5,6),(2,4,9),(1,6,9),(3,4,8)]
QALL = [(1,5,9),(1,6,8),(2,4,9),(2,6,7),(3,4,8),(3,5,7)]

def family(P,Q):return [tuple(x for x in c) for c in P]+[tuple(-x for x in c) for c in Q]

FIXTURES = {'Y6_NONPAIRED':family(P6,QY), 'H6_PAIRED':family(P6,P6),
            'K33_Q0':family(P9,Q0),'K33_Q1':family(P9,Q1),
            'K33_Q2':family(P9,Q2),'K33_Q3':family(P9,Q3),
            'K33_ALL_SIX_MATCHINGS':family(P9,QALL)}

def validate(F, n):
    if not isinstance(n,int) or n<3 or n%3: return False, 'invalid variable count'
    if not isinstance(F,list) or len(F)!=4*n//3:return False,'4n/3 clause count violated'
    seen=set(); p=collections.Counter(); q=collections.Counter()
    for c in F:
        if not isinstance(c,(tuple,list)) or len(c)!=3:return False,'not ternary'
        if any(not isinstance(x,int) or isinstance(x,bool) or not 1<=abs(x)<=n for x in c):return False,'invalid literal'
        if len(set(map(abs,c)))!=3:return False,'repeated variable in clause'
        if not(all(x>0 for x in c) or all(x<0 for x in c)):return False,'mixed-sign clause'
        key=tuple(sorted(c))
        if key in seen:return False,'duplicate source clause'
        seen.add(key)
        for x in c:(p if x>0 else q)[abs(x)]+=1
    if any((p[v],q[v])!=(2,2) for v in range(1,n+1)):return False,'unbalanced signed degree'
    return True,'valid canonical language source'

def sat(F,model):return all(any(model[abs(x)]==(1 if x>0 else 0) for x in c) for c in F)

def counts(F,model):
    h=[0]*4
    for c in F:h[sum(model[abs(x)]==(1 if x>0 else 0) for x in c)]+=1
    return h

def dual(F,n):
    positive=[(j,c) for j,c in enumerate(F) if c[0]>0]
    negative=[(j,c) for j,c in enumerate(F) if c[0]<0]
    ids=[{},{}]; edges=[]
    for typ, group in enumerate((positive,negative)):
        for v in range(1,n+1):
            pair=[k for k,(_,c) in enumerate(group) if (v if typ==0 else -v) in c]
            assert len(pair)==2 and pair[0]!=pair[1]
            ids[typ][v]=pair
    for v in range(1,n+1):edges.append((v,tuple(ids[0][v]),tuple(ids[1][v])))
    return {'plus':[list(c) for _,c in positive],'minus':[list(c) for _,c in negative],
            'edges':[{'var':v,'plus_endpoints':a,'minus_endpoints':b} for v,a,b in edges]}

def dangerous(F, n):
    p=[set(c) for c in F if c[0]>0]
    q=[(j,[abs(x) for x in c]) for j,c in enumerate(F) if c[0]<0]
    return [(j,c) for j,c in q if all(not ({a,b}<=t) for a,b in itertools.combinations(c,2) for t in p)]

def positive_bipartition(F,n):
    edges=dual(F,n)['edges']; m=2*n//3
    adj=[set() for _ in range(m)]
    for e in edges:
        a,b=e['plus_endpoints'];adj[a].add(b);adj[b].add(a)
    col=[None]*m
    for a in range(m):
        if col[a] is not None:continue
        col[a]=0;stack=[a]
        while stack:
            u=stack.pop()
            for v in adj[u]:
                if col[v] is None:col[v]=1-col[u];stack.append(v)
                elif col[v]==col[u]:return None
    return col

def factorize(F,n,ledger):
    color=positive_bipartition(F,n)
    if color is None:return None
    E=dual(F,n)['edges'];m=2*n//3
    remaining=set(range(1,n+1));factors=[]
    for _ in range(3):
        nbr=[[] for i in range(m)]
        for e in E:
            if e['var'] not in remaining:continue
            a,b=e['plus_endpoints'];u,v=(a,b) if color[a]==0 else (b,a)
            nbr[u].append((v,e['var']))
        used={};match={}
        def dfs(u,seen):
            for v,e in nbr[u]:
                ledger['matching_edge_tests']+=1
                if v in seen:continue
                seen.add(v)
                if v not in used or dfs(used[v],seen):
                    used[v]=u;match[u]=e;return True
            return False
        for u in range(m):
            if color[u]==0:
                if not dfs(u,set()):raise AssertionError('regular bipartite matching incomplete')
                ledger['matching_augmentations']+=1
        M=set(match.values());assert len(M)==m//2
        factors.append(sorted(M));remaining-=M
    assert not remaining and sorted(set(sum(factors,[])))==list(range(1,n+1))
    return factors

def dpll(F,n,cap=None):
    L=collections.Counter();nodes=0;tests=0;failed=0;units=0
    def recurse(partial):
        nonlocal nodes,tests,failed,units
        nodes+=1
        if cap is not None and nodes>cap:return 'UNRESOLVED',None
        a=partial.copy()
        while True:
            pending=[]; forced=None; fail=False
            for c in F:
                un=[];ok=False
                for x in c:
                    tests+=1;val=a[abs(x)]
                    if val==-1:un.append(x)
                    elif val==(1 if x>0 else 0):ok=True;break
                if ok:continue
                if not un:fail=True;break
                pending.append(un)
                if len(un)==1:forced=un[0];break
            if fail:failed+=1;return 'UNSAT',None
            if forced is None:
                if not pending:return 'SAT',[0]+[max(a[i],0) for i in range(1,n+1)]
                var=collections.Counter(abs(x) for c in pending for x in c)
                pivot=min((k for k in var if a[k]==-1),key=lambda k:(-var[k],k))
                for bit in (1,0):
                    b=a.copy();b[pivot]=bit
                    decision,w=recurse(b)
                    if decision in ('SAT','UNRESOLVED'):return decision,w
                return 'UNSAT',None
            key=abs(forced);desired=int(forced>0)
            if a[key]!=-1 and a[key]!=desired:return 'UNSAT',None
            if a[key]==-1:a[key]=desired;units+=1
    decision,w=recurse([-1]*(n+1))
    return {'decision':decision,'witness':w,'nodes':nodes,'literal_tests':tests,'failed_leaves':failed,'unit_assignments':units}

def compact_modes(F):
    # true = a pair of all-TRUE/all-FALSE targets is jointly satisfiable.
    # Independent sign-source consistency rule, no derived unrestricted pruning.
    types=[];both=collections.Counter();mixed=0
    for i,c in enumerate(F):
        modes={'S':{abs(l):int(l>0) for l in c},'U':{abs(l):int(l<0) for l in c}}
        types.append({'clause':i,'S':modes['S'],'U':modes['U'],
                      'invert_S':modes['U'],'invert_U':modes['S']})
    for i in range(len(F)):
        for j in range(i+1,len(F)):
            checks={x+y:all(types[i][x][v]==types[j][y][v]
                 for v in set(types[i][x])&set(types[j][y])) for x in 'SU' for y in 'SU'}
            t=''.join(k for k in ('SS','SU','US','UU') if checks[k]);both[t]+=1
            if not t:mixed+=1
    return {'counts':dict(both),'none_compatible':mixed,'sample_targets':types[:4]}

def evaluate(name,F,baseline_cap=None):
    n=max(abs(x) for c in F for x in c)
    ledger=collections.Counter()
    tracemalloc.start()
    valid,reason=validate(F,n);ledger['grammar_literal_inspections']+=len(F)*3
    if not valid:return {'name':name,'valid':False,'reason':reason}
    D=dangerous(F,n);ledger['dangerous_pair_tests']+=sum(3 for c in F if c[0]<0)
    factors=factorize(F,n,ledger)
    witness=None;policy=''
    if factors is not None:
        for k,M in enumerate(factors):
            ledger['factor_witness_trials']+=1
            a=[0]+[int(v in M) for v in range(1,n+1)]
            ledger['witness_literal_tests']+=3*len(F)
            if sat(F,a):witness=a;policy='three_factors_'+str(k);break
    if witness is None:
        base=dpll(F,n,cap=baseline_cap)
        decision=base['decision'];witness=base['witness'];policy='DPLL_fallback'
        ledger['fallback_nodes']=base['nodes'];ledger['fallback_literal_tests']=base['literal_tests']
    else:decision='SAT'
    baseline=dpll(F,n,cap=baseline_cap)
    models=[]
    if n<=9:
        for mask in range(1<<n):
            a=[0]+[(mask>>(i-1))&1 for i in range(1,n+1)]
            if sat(F,a):models.append(mask)
        assert (decision=='SAT')==bool(models)
    if witness is not None:assert sat(F,witness)
    peak=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
    a0=[0]*(n+1);a1=[0]+[1]*n
    trails=[]
    for mask in [0,1,3,(1<<n)-1]:
        a=[0]+[(mask>>(i-1))&1 for i in range(1,n+1)]
        h=counts(F,a);hb=counts(F,[0]+[1-x for x in a[1:]])
        assert sum(k*h[k] for k in range(4))==2*n
        assert hb==list(reversed(h))
        trails.append({'mask':mask,'hist':h,'complement_hist':hb,'sat':h[0]==0})
    assert counts(F,a0)[0]>0 and counts(F,a1)[0]>0
    return {'name':name,'valid':True,'n':n,'m':len(F),'formula':[list(c) for c in F],
            'q':len(D),'dangerous_clause_indices':[j for j,c in D],
            'plus_bipartite':factors is not None,'factors':factors,'policy':policy,
            'decision':decision,'model_count':len(models) if n<=9 else None,
            'witness':witness,'endpoint_zero_hist':counts(F,a0),
            'endpoint_one_hist':counts(F,a1),'trails':trails,
            'pair_extremes':compact_modes(F),
            'baseline':{k:v for k,v in baseline.items() if k!='witness'},
            'ledger':dict(ledger),'peak_python_traced_bytes':peak}

def dpll_iterative(F,n):
    """Complete iterative backtracking and UP; no cutoffs or recursion limit.
    Retained Python states and all failed branches are charged in the ledger.
    """
    initial=[-1]*(n+1)
    stack=[initial]
    node_count=0;literal_tests=0;failed=0;units=0
    while stack:
        assignment=stack.pop();node_count+=1
        while True:
            residual=[];forced=None;conflict=False
            for clause in F:
                unassigned=[];passed=False
                for lit in clause:
                    literal_tests+=1
                    val=assignment[abs(lit)]
                    if val<0:unassigned.append(lit)
                    elif val==int(lit>0):passed=True;break
                if passed:continue
                if not unassigned:conflict=True;break
                residual.append(unassigned)
                if len(unassigned)==1:forced=unassigned[0];break
            if conflict:failed+=1;break
            if forced is not None:
                v=abs(forced);b=int(forced>0)
                if assignment[v]>=0 and assignment[v]!=b:failed+=1;break
                if assignment[v]<0:assignment[v]=b;units+=1
                continue
            if not residual:
                a=[0]+[max(0,z) for z in assignment[1:]]
                assert sat(F,a)
                return {'decision':'SAT','witness':a,'nodes':node_count,
                        'literal_tests':literal_tests,'failed_leaves':failed,
                        'unit_assignments':units}
            uses=collections.Counter(abs(x) for cl in residual for x in cl)
            pivot=min((v for v in uses if assignment[v]<0),key=lambda v:(-uses[v],v))
            next_zero=assignment.copy();next_zero[pivot]=0
            assignment[pivot]=1
            stack.append(next_zero);stack.append(assignment)
            break
    return {'decision':'UNSAT','witness':None,'nodes':node_count,
            'literal_tests':literal_tests,'failed_leaves':failed,
            'unit_assignments':units}

def _no_duplicate_fields(pairs):
    out={}
    for k,v in pairs:
        if k in out:raise ValueError('duplicate JSON object key')
        out[k]=v
    return out

def decide_encoded(source):
    """Total exact decider for fixed JSON target encoding; malformed => REJECT.
    Requires {"n": integer, "clauses": [ordered signed integer triples]}.
    Optional certified matching policy, then uncapped UP-first DPLL.
    """
    try:
        if isinstance(source,bytes):source=source.decode('utf-8','strict')
        if not isinstance(source,str):return {'decision':'REJECT','reason':'non-string input'}
        obj=json.loads(source,object_pairs_hook=_no_duplicate_fields)
        if type(obj)!=dict or set(obj)!={'n','clauses'}:return {'decision':'REJECT','reason':'invalid JSON schema'}
        n=obj['n'];F=obj['clauses'];valid,reason=validate(F,n)
        if not valid:return {'decision':'REJECT','reason':reason}
        try:
            factors=factorize(F,n,collections.Counter())
        except RecursionError:
            # Polynomial matching recursion is an implementation convenience,
            # never a reason to reject a correctly formed source.
            factors=None
        if factors is not None:
            for M in factors:
                candidate=[0]+[int(v in M) for v in range(1,n+1)]
                if sat(F,candidate):return {'decision':'SAT','witness':candidate,'policy':'certified_three_factor'}
        base=dpll_iterative(F,n)
        assert base['decision'] in ('SAT','UNSAT')
        return {'decision':base['decision'],'witness':base['witness'],'policy':'complete_UP_DPLL'}
    except (ValueError,TypeError,OverflowError,KeyError,UnicodeError) as e:
        return {'decision':'REJECT','reason':type(e).__name__+': '+str(e)}

def main():
    a=argparse.ArgumentParser();a.add_argument('--output',default='raw280.json');a.add_argument('--u');arg=a.parse_args()
    out={'run':'LSPV3_GATE280','seed':20261031,'target':'proper duplicate-free Monotone 3-SAT-(2,2)',
         'scope':'standalone small controls; U198 certificate separate', 'cases':[], 'malformed':[]}
    for name,F in FIXTURES.items():out['cases'].append(evaluate(name,F))
    for name,F in [('duplicate',[*FIXTURES['Y6_NONPAIRED'][:-1],FIXTURES['Y6_NONPAIRED'][0]]),
                   ('mixed',[(-1,2,3)]+FIXTURES['Y6_NONPAIRED'][1:]),
                   ('repeated',[(1,1,3)]+FIXTURES['Y6_NONPAIRED'][1:]),
                   ('unbalanced',FIXTURES['Y6_NONPAIRED'][:-1])]:
        ok,why=validate(F,6);assert not ok;out['malformed'].append({'name':name,'rejected':True,'reason':why})
    if arg.u:
        lines=[s for s in Path(arg.u).read_text(encoding='utf-8').splitlines() if s.strip() and not s.lstrip().startswith('#')]
        U=[tuple(c) for c in ast.literal_eval('\n'.join(lines))]
        ok,why=validate(U,198);assert ok
        d=dangerous(U,198);b=positive_bipartition(U,198)
        out['U198']={'source_path':arg.u,'valid':ok,'n':198,'m':264,'q':len(d),
                     'positive_bipartite':b is not None,'literature_UNSAT':'Döcker 2019; independently certified in project DOECKER-CORE-CERT61',
                     'endpoint_zero_hist':counts(U,[0]*199),'endpoint_one_hist':counts(U,[0]+[1]*198),
                     'pair_modes':compact_modes(U)['counts']}
    out['encoded_decider_checks']=[]
    for row in out['cases']:
        src=json.dumps({'n':row['n'],'clauses':row['formula']},separators=(',',':'))
        z=decide_encoded(src)
        assert z['decision']==row['decision']
        out['encoded_decider_checks'].append({'name':row['name'],'decision':z['decision'],'policy':z['policy']})
    bads=['{}','{"n":6,"clauses":[]}', '{"n":3,"n":6,"clauses":[]}',
          '{"n":6,"clauses":null}', '{"n":6,"clauses":[],"extra":true}', 'not-json']
    for bad in bads:assert decide_encoded(bad)['decision']=='REJECT'
    out['malformed_encoding_rejections']=len(bads)
    Path(arg.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'cases':[(x['name'],x.get('decision','INVALID'),x.get('q'),x.get('model_count'),x.get('policy')) for x in out['cases']],
                      'malformed':len(out['malformed']),'U198':out.get('U198')},indent=2))

if __name__=='__main__':main()