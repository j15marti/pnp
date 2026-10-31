#!/usr/bin/env python3
"""LSPV-2 guarded SCC symbolic source clause, with checked resolution trace.
Python 3.10+. Run: python guarded_scc261.py [--out raw261.json]
All source clauses immutable signed literals; no separate occurrence variables.
"""
from __future__ import annotations
import argparse,collections,hashlib,json,itertools,random,time,tracemalloc
from pathlib import Path


def clean(c): return tuple(sorted(set(c),key=lambda t:(abs(t),t<0)))
def taut(c): return any(-x in c for x in c)
def assign_lit(l,a): return (a[abs(l)]==int(l>0))
def eval_formula(F,a): return all(any(assign_lit(l,a) for l in c) for c in F)
def nvars(F): return max((abs(l) for c in F for l in c),default=0)

def source_extremes(F,n):
    """Full original-occurrence S/U/inversion controls, pair four-way matrix,
    coherent endpoint and flip trails. Does NOT take local targets as global assignments."""
    occ=[]; pairs=[]
    for j,c in enumerate(F):
        def target(mode): return {str(abs(l)):(int(l>0) if mode=='S' else int(l<0)) for l in c}
        s,u=target('S'),target('U')
        occ.append({'source_clause':j+1,'literals':list(c),
                    'signed_occurrences':[{'source_clause':j+1,'variable':abs(l),'literal':l,
                                           'S':int(l>0),'inverse_S_U':int(l<0),
                                           'U':int(l<0),'inverse_U_S':int(l>0)} for l in c],
                    'S':s,'inverse_S_U':u,'U':u,'inverse_U_S':s})
    for j in range(len(F)):
        for k in range(j+1,len(F)):
            ms={}
            for m1,m2 in itertools.product('SU',repeat=2):
                a=occ[j][m1]; b=occ[k][m2];ms[m1+m2]=all(a[v]==b[v] for v in a.keys()&b.keys())
            pairs.append({'source_pair':[j+1,k+1],'SS':ms['SS'],'SU':ms['SU'],'US':ms['US'],'UU':ms['UU']})
    aa={i:0 for i in range(1,n+1)}; paths=[]
    candidates=[('all_zero',dict(aa))]
    for i in range(1,n+1):
        aa[i]^=1;candidates.append(('flip_'+str(i),dict(aa)))
    aa={i:1 for i in range(1,n+1)}; candidates.append(('all_one',dict(aa)))
    for i in range(1,min(n,6)+1):
        aa[i]^=1;candidates.append(('reverse_flip_'+str(i),dict(aa)))
    for name,a in candidates:
        tj=[sum(assign_lit(l,a) for l in c) for c in F]
        paths.append({'name':name,'assignment':''.join(str(a[i]) for i in range(1,n+1)),
                      'true_literal_counts':tj,'histogram':[tj.count(t) for t in range(max(map(len,F),default=0)+1)],'four_categories':[tj.count(t) for t in range(4)],
                      'satisfied':0 not in tj})
    return {'original_clause_targets':occ,'source_pair_compatibility':pairs,'coherent_flip_trail':paths}


def discover_guards(F):
    """Renaming-invariant syntactic selector: vars appearing with just one sign
    in ternary clauses. This may be a poor selector; its discovery is counted."""
    signs=collections.defaultdict(set)
    for c in F:
        if len(c)==3:
            for l in c:signs[abs(l)].add(l>0)
    return {v for v,s in signs.items() if len(s)==1}


def find_guarded_scc(F,B,counters):
    """One optimistic implication graph. Guard compatibility is checked only
    *after* explicit paths are found, so inconsistent guard sources cannot
    yield false blockers. Incomplete by design."""
    ed=collections.defaultdict(list)
    hidden=sorted({abs(l) for c in F for l in c if abs(l) not in B})
    for j,c in enumerate(F):
        counters['source_occurrence_reads']+=len(c)
        guards=[l for l in c if abs(l) in B]
        core=[l for l in c if abs(l) not in B]
        if len(core)==2:
            u,v=core;ed[-u].append((v,j,guards));ed[-v].append((u,j,guards));counters['edges']+=2
        elif len(core)==1:
            u=core[0];ed[-u].append((u,j,guards));counters['edges']+=1
    for x in ed: ed[x].sort(key=lambda e:(e[1],e[0]))
    def bfs(s,t):
        queue=collections.deque([s]);pr={s:None}
        while queue:
            v=queue.popleft()
            if v==t:break
            for w,j,g in ed[v]:
                counters['graph_edge_visits']+=1
                if w not in pr:pr[w]=(v,j,g);queue.append(w)
        if t not in pr:return None
        cur=t;path=[]
        while pr[cur] is not None:
            prev,j,g=pr[cur];path.append({'from':prev,'to':cur,'source':j+1,'guard_literals':g});cur=prev
        return path[::-1]
    for v in hidden:
        counters['pivot_trials']+=1
        p=bfs(v,-v)
        if p is None:continue
        q=bfs(-v,v)
        if q is None:continue
        G=set(l for e in p+q for l in e['guard_literals'])
        if taut(G): counters['inconsistent_guard_candidates']+=1;continue
        return {'pivot':v,'guard_variables':sorted(B),'paths':[p,q], 'learned':list(clean(G))}
    return None


def source_resolution_proof(F,cert):
    """Lift both implication paths and resolve final opposing source literals.
    All internal proof nodes use *only* resolution; no uncharged semantic step.
    """
    if cert is None:return None
    derived=[];next_id=len(F)+1
    def get(node):return clean(F[node-1]) if node<=len(F) else tuple(derived[node-len(F)-1]['clause'])
    def resolve(a,b,p):
        nonlocal next_id
        ca=set(get(a));cb=set(get(b))
        if p in ca and -p in cb: out=(ca-{p})|(cb-{-p})
        elif -p in ca and p in cb: out=(ca-{-p})|(cb-{p})
        else:raise AssertionError('invalid pivot '+str((a,b,p,ca,cb)))
        if taut(out):raise AssertionError('unexpected tautology')
        eid=next_id;next_id+=1;derived.append({'id':eid,'parents':[a,b],'pivot':p,'clause':list(clean(out))});return eid
    def proof_path(path):
        assert path
        last=path[0]['source']
        for e in path[1:]:last=resolve(last,e['source'],e['from'])
        return last
    p,q=cert['paths'];a=proof_path(p);b=proof_path(q)
    last=resolve(a,b,cert['pivot'])
    if set(get(last))!=set(cert['learned']):raise AssertionError('guard union mismatch')
    return {'source_count':len(F),'steps':derived,'root':last,'learned':cert['learned']}


def check_proof(F,proof):
    d={i+1:set(c) for i,c in enumerate(F)}
    for step in proof['steps']:
        a,b=step['parents'];p=step['pivot'];ca,cb=d[a],d[b]
        assert (p in ca and -p in cb) or (-p in ca and p in cb)
        if p in ca: c=(ca-{p})|(cb-{-p})
        else:c=(ca-{-p})|(cb-{p})
        assert not taut(c) and c==set(step['clause'])
        d[step['id']]=c
    assert d[proof['root']]==set(proof['learned'])
    return True


def rup_check(F,clause):
    # UP under negation of proposed source clause, independent of graph proof.
    n=nvars(F);a={abs(l):int(l<0) for l in clause}
    for _ in range(n+1):
        changed=False
        for c in F:
            if any(assign_lit(l,a) for l in c if abs(l) in a):continue
            unresolved=[l for l in c if abs(l) not in a]
            if not unresolved:return True
            if len(unresolved)==1:
                l=unresolved[0];v=abs(l);val=int(l>0)
                if v in a and a[v]!=val:return True
                if v not in a:a[v]=val;changed=True
        if not changed:return False
    return False


def solve_dpll(F,n,counters):
    """Deterministic first-unassigned, true-first UP DPLL.
    UNSAT proof is complete branch tree with independently checkable UP leaves.
    Baseline and enhanced use exactly the same procedure.
    """
    def propagate(a):
        local=dict(a)
        while True:
            changed=False
            for j,c in enumerate(F):
                counters['literal_tests']+=len(c)
                if any(assign_lit(l,local) for l in c if abs(l) in local):continue
                pending=[l for l in c if abs(l) not in local]
                if not pending: return None,j
                if len(pending)==1:
                    l=pending[0];v=abs(l);local[v]=int(l>0);counters['unit_propagations']+=1;changed=True
            if not changed:return local,None
    def run(a):
        counters['nodes']+=1
        b,bad=propagate(a)
        if bad is not None:return {'type':'UNSAT_LEAF','assumptions':{str(v):x for v,x in a.items()},'contradiction_clause':bad+1},None
        v=next((i for i in range(1,n+1) if i not in b),None)
        if v is None:
            assert eval_formula(F,b)
            return {'type':'SAT_LEAF','full_assignment':{str(v):b[v] for v in range(1,n+1)}},b
        kids=[]
        for val in (1,0):
            child,sol=run({**b,v:val})
            kids.append({'value':val,'tree':child})
            if sol is not None:return {'type':'SAT_BRANCH','var':v,'children':kids},sol
        return {'type':'UNSAT_BRANCH','var':v,'children':kids},None
    return run({})


def verify_tree(F,n,tree):
    def prop(a):
        b=dict(a)
        while True:
            move=False
            for c in F:
                if any(assign_lit(l,b) for l in c if abs(l) in b):continue
                ls=[l for l in c if abs(l) not in b]
                if not ls:return None
                if len(ls)==1:
                    l=ls[0];v=abs(l);val=int(l>0)
                    if v in b and b[v]!=val:return None
                    if v not in b:b[v]=val;move=True
            if not move:return b
    def check(t,ass):
        state=prop(ass)
        if t['type']=='UNSAT_LEAF':return state is None
        if t['type']=='SAT_LEAF':
            a={int(v):x for v,x in t['full_assignment'].items()}
            return all(a.get(v)==val for v,val in ass.items()) and eval_formula(F,a)
        if state is None:return False
        v=t['var']
        if v in state:return False
        children=t['children']
        if t['type']=='UNSAT_BRANCH' and len(children)!=2:return False
        if {c['value'] for c in children}!=({0,1} if t['type']=='UNSAT_BRANCH' else {1}):
            # SAT_BRANCH may terminate after first branch or after two.
            if t['type']!='SAT_BRANCH' or [c['value'] for c in children] not in ([1],[1,0]):return False
        statuses=[]
        for c in children:
            z=check(c['tree'],{**state,v:c['value']});statuses.append(z)
        if not all(statuses):return False
        if t['type']=='SAT_BRANCH':return any('SAT' in c['tree']['type'] and c['tree']['type']!='UNSAT_LEAF' for c in children) or any(c['tree']['type']=='SAT_BRANCH' for c in children)
        return True
    # More reliable verifier below returns (valid, sat/unsat) and enforces child status.
    def status(t,ass):
        state=prop(ass)
        if t['type']=='UNSAT_LEAF':return (state is None,False)
        if t['type']=='SAT_LEAF':
            a={int(v):x for v,x in t['full_assignment'].items()}
            return (state is not None and len(a)==n and all(a.get(v)==val for v,val in state.items()) and eval_formula(F,a),True)
        if state is None or t['var'] in state:return (False,False)
        kids=t['children'];values=[c['value'] for c in kids]
        if values not in ([1],[1,0]):return (False,False)
        child=[status(c['tree'],{**state,t['var']:c['value']}) for c in kids]
        if not all(k[0] for k in child):return (False,False)
        if t['type']=='UNSAT_BRANCH':return (values==[1,0] and not any(k[1] for k in child),False)
        return ((values==[1] and child[0][1]) or (values==[1,0] and not child[0][1] and child[1][1]),True)
    return status(tree,{})


def guarded_cycle(k,force=False):
    """Two guards per conditional equality/disequality pair; general k.
    If all guards true, an odd signed cycle is impossible.
    Each guard occurs twice with one polarity in 3-CNF.
    """
    F=[];hidden=[i+1 for i in range(k)];guard=[k+i+1 for i in range(k)]
    for i,(x,g) in enumerate(zip(hidden,guard)):
        y=hidden[(i+1)%k]
        if i<k-1: F.extend([(-g,-x,y),(-g,x,-y)])
        else: F.extend([(-g,-x,-y),(-g,x,y)])
    if force:F.extend((g,) for g in guard)
    return [list(c) for c in F]

def contradictory_guards():
    # Independently SAT for each g; ignoring guard labels creates spurious SCC.
    return [[-3,1,2],[-3,-1,2],[3,1,-2],[3,-1,-2]]

def boundary_four(force):
    F=[[-3,1,2],[-3,-1,2],[-3,1,-2],[-3,-1,-2]]
    if force:F.append([3])
    return F

def signed_rename(F,seed):
    rr=random.Random(seed);n=nvars(F);perm=list(range(1,n+1));rr.shuffle(perm)
    flips={x:rr.randrange(2) for x in range(1,n+1)}
    return [[(1 if l>0 else -1)*(-1 if flips[abs(l)] else 1)*perm[abs(l)-1] for l in c] for c in F]

def load_cases(root):
    pairs=json.loads((root/'matched_cases260.json').read_text());cases=[]
    for k in (2,3,5,9):
        for forced in (False,True):cases.append((f'odd_guard_cycle_{k}_{"NO" if forced else "YES"}',guarded_cycle(k,forced)))
    for forced in (False,True):cases.append((f'four_binary_guard_{"NO" if forced else "YES"}',boundary_four(forced)))
    cases.append(('conflicting_guards_SAT',contradictory_guards()))
    cases.append(('conflicting_guards_renamed',signed_rename(contradictory_guards(),804)))
    cases.extend((label,pairs[label]) for label in sorted(pairs))
    cases.append(('renamed_odd_cycle_NO',signed_rename(guarded_cycle(6,True),15)))
    cases.append(('renamed_odd_cycle_YES',signed_rename(guarded_cycle(6,False),15)))
    cases.append(('easy_horn_SAT',[[1,-2,-3],[-1,2],[-1,3]]))
    cases.append(('easy_horn_UNSAT',[[1],[-1]]))
    cases.append(('easy_highwidth_SAT',[[1,2,3,4,5],[1,2,3,4,-5]]))
    cases.append(('binary_no_units_UNSAT',[[1,2],[-1,2],[1,-2],[-1,-2]]))
    rr=random.Random(20261030)
    for z in range(12):
        n=7;num=15+z%7
        F=[]
        for j in range(num):
            ids=rr.sample(range(1,n+1),3);F.append([x*(1 if rr.getrandbits(1) else -1) for x in ids])
        cases.append((f'random_{z}',F))
    return cases

def run(out):
    start=time.perf_counter();tracemalloc.start();root=Path(__file__).parent
    cases=load_cases(root);raw=[];sumr=collections.Counter();work={'baseline':collections.Counter(),'enhanced':collections.Counter()}
    for name,F in cases:
        n=nvars(F)
        assert all(len(set(map(abs,c)))==len(c) for c in F)
        B=discover_guards(F);discover_cost=sum(len(c) for c in F)
        t=collections.Counter();cert=find_guarded_scc(F,B,t);proof=source_resolution_proof(F,cert) if cert else None
        if proof:check_proof(F,proof)
        learned=cert['learned'] if cert else None
        t['selector_source_reads']=discover_cost;t['policy_recognitions']+=1
        if not cert:t['failed_policy_attempts']+=1
        if cert:t['resolution_literal_work']=sum(sum(len(F[p-1]) if p<=len(F) else len(proof['steps'][p-len(F)-1]['clause']) for p in s['parents']) for s in proof['steps'])
        base=collections.Counter();tree1,w1=solve_dpll(F,n,base)
        enhanced=collections.Counter();tree2,w2=solve_dpll(F+([learned] if learned is not None else []),n,enhanced)
        assert (w1 is None)==(w2 is None)
        assert verify_tree(F,n,tree1)==(True,w1 is not None)
        assert verify_tree(F+([learned] if learned is not None else []),n,tree2)==(True,w2 is not None)
        if w2 is not None:assert eval_formula(F,w2)
        # Independent semantic sampling/exhaustion. For n<=16 enumerate all assignments;
        # tests pairwise ordinary source assignment, not occurrence-level targets.
        model_count=None
        if n<=16:
            model_count=sum(eval_formula(F,{i+1:(mask>>i)&1 for i in range(n)}) for mask in range(1<<n))
            assert bool(model_count)==(w1 is not None)
            if learned is not None:
                for mask in range(1<<n):
                    a={i+1:(mask>>i)&1 for i in range(n)}
                    if eval_formula(F,a):assert any(assign_lit(l,a) for l in learned)
        controls=source_extremes(F,n)
        # Independent exact pair compatibility: enumerate only the shared
        # source-variable support (<=6 vars in proper 3CNF).
        for pair in controls['source_pair_compatibility']:
            j,k=pair['source_pair'];cj,ck=F[j-1],F[k-1]
            support=sorted({abs(l) for l in cj+ck})
            for m1,m2 in itertools.product('SU',repeat=2):
                possible=False
                for mask in range(1<<len(support)):
                    a={v:(mask>>p)&1 for p,v in enumerate(support)}
                    if all(assign_lit(l,a)==(m1=='S') for l in cj) and all(assign_lit(l,a)==(m2=='S') for l in ck):possible=True;break
                assert pair[m1+m2]==possible
        for w,c in [('baseline',base),('enhanced',enhanced)]:work[w].update(c)
        work['enhanced'].update(t)
        sumr['cases']+=1;sumr['SAT' if w1 is not None else 'UNSAT']+=1;sumr['certificates']+=int(bool(cert));sumr['nonRUP_certificates']+=int(bool(cert) and not rup_check(F,learned))
        raw.append({'name':name,'n':n,'source_formula':F,'source_models':model_count,
                    'selector_guard_variables':sorted(B),'cert':cert,'resolution_dag':proof,
                    'learned_clause_rup':rup_check(F,learned) if learned is not None else None,
                    'selector_counters':dict(t),'baseline_counters':dict(base),'enhanced_counters':dict(enhanced),
                    'SAT_witness':{str(x):v for x,v in w2.items()} if w2 else None,
                    'baseline_tree':tree1,'enhanced_tree':tree2,
                    'source_controls':controls})
    # Distinct negative experiment: force an intentionally overinclusive
    # selector B={3} on an F whose guard signs conflict. The UNION graph
    # has contradictory paths, but the joint guards are inconsistent.
    cross=collections.Counter()
    bad_cert=find_guarded_scc(contradictory_guards(),{3},cross)
    assert bad_cert is None and cross['inconsistent_guard_candidates']>=1
    peak=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
    body={'run_id':'GUARDED-SCC261','date_pacific':'2026-10-30', 'type':'COMPUTATIONAL and PROVED/EXACT restricted lemma, referee pending',
          'cases':raw,'aggregate_cases':dict(sumr),'aggregate_work':{k:dict(v) for k,v in work.items()},
          'peak_python_tracemalloc_bytes':peak,'producer_wall_seconds':round(time.perf_counter()-start,5),
          'not_native_flmv':True,'inconsistent_guard_negative_control':{'source_formula':contradictory_guards(),'forced_candidate_guards':[3], 'certificate':bad_cert,'counters':dict(cross)}}
    Path(out).write_text(json.dumps(body,indent=2,sort_keys=True));
    print(json.dumps({'cases':sumr,'work':{k:dict(v) for k,v in work.items()},'peak_python_bytes':peak,'seconds':body['producer_wall_seconds'],'out':out},indent=2))
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--out',default=str(Path(__file__).parent/'raw261.json'));args=parser.parse_args();run(args.out)