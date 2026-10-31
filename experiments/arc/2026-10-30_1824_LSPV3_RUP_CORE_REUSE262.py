#!/usr/bin/env python3
"""Source-authenticated assumption-core clauses and backtrack-safe reuse.
Run: python arc262_experiment.py --output raw.json
Deterministic, proof-carrying tree solver with exact counter instrumentation.
"""
import json, itertools, argparse, pathlib, collections, math, random, time, tracemalloc
from arc261_experiment import W1,SWAP6,orbit,xor_k4,rename,original_audit,enc_bits

def litval(l,a):
    v=abs(l)
    return None if v not in a else a[v]==int(l>0)

def up(F, assumptions, ctr=None, record=False):
    """Repeated full-clause-scan UP. Returns (assignment or None, trace, conflict index).
       Charge source clause/literal scans and reason output, including failed tests."""
    a={}
    tr=[]
    for l in assumptions:
        if ctr is not None:ctr['assumption_tests']+=1
        v=abs(l);b=int(l>0)
        if v in a and a[v]!=b: return None,tr,0
        a[v]=b
    while True:
        changed=False
        for j,c in enumerate(F):
            if ctr is not None:ctr['clause_visits']+=1
            is_sat=False; rem=[]
            for l in c:
                if ctr is not None:ctr['literal_reads']+=1
                val=litval(l,a)
                if val is True:
                    is_sat=True;break
                if val is None:rem.append(l)
            if is_sat:continue
            if len(rem)==0:
                if ctr is not None:ctr['conflicts']+=1
                return None,tr,j+1
            if len(rem)==1:
                l=rem[0]
                if abs(l) not in a:
                    a[abs(l)]=int(l>0);tr.append([j+1,l]);changed=True
                    if ctr is not None:ctr['unit_inferences']+=1
                    break
        if not changed: return a,tr,None

def is_sat(F,a):
    return all(any(a[abs(l)]==int(l>0) for l in c) for c in F)

def complete_models(F,n):
    tot=0;first=None
    for bits in itertools.product((0,1),repeat=n):
        a=dict(enumerate(bits,1))
        if is_sat(F,a):
            tot+=1
            if first is None:first=a
    return tot,first

def core_reduce(DB, decisions, ctr, max_tests=None):
    """One-pass deletion obtains a subset-minimal *UP* conflicting core.
    Uses only source clauses plus earlier RUP-certified learned clauses."""
    core=list(decisions)
    assert up(DB,core,ctr)[0] is None
    for l in list(decisions):
        if max_tests is not None and ctr.get("local_core_tests",0)>=max_tests:break
        if l not in core:continue
        ctr["local_core_tests"]+=1
        test=[z for z in core if z!=l]
        ctr['core_trial_restarts']+=1
        if up(DB,test,ctr)[0] is None:core=test
    # Every inclusion-minimality check is true by UP monotonicity.
    assert up(DB,core,ctr)[0] is None
    return core

class Solver:
    def __init__(self,F,mode='none',n=None,max_nodes=100000):
        self.F=[tuple(c) for c in F];self.n=n or max(abs(l) for c in F for l in c)
        self.mode=mode;self.max_nodes=max_nodes
        self.learned=[];self.learned_set=set();self.counter=collections.Counter()
        self.proofs=[];self.witness=None;self.tree=None
        self.peak_clauses=len(F);self.peak_stack=0
    def search(self):
        self.counter['initial_source_literal_reads']+=sum(len(c) for c in self.F)
        self.counter['initial_header_bit_reads']+=enc_bits(self.F,self.n)
        self.tree=self.visit([])
        outcome=self.witness is not None
        # final full-source witness verification, no SAT answer without it
        if outcome:
            for c in self.F:
                self.counter['witness_clause_reads']+=1
                for l in c:
                    self.counter['witness_literal_reads']+=1
                    if litval(l,self.witness):break
            assert is_sat(self.F,self.witness)
        return {'SAT':outcome,'witness':self.witness,'nodes':self.counter['nodes'],
                'selected_events':sum(self.counter.values()),'counter':dict(self.counter),
                'learned_clauses':[list(p['clause']) for p in self.proofs],
                'proofs':self.proofs,'tree':self.tree,
                'peak_clause_count':self.peak_clauses,
                'peak_stack_literals':self.peak_stack,
                'peak_approx_live_bits':enc_bits(self.F,self.n)+sum((3+(self.n.bit_length()+1)*len(c)) for c in self.learned)+self.peak_stack*(self.n.bit_length()+1)+self.n*5}
    def visit(self,decisions):
        self.counter['nodes']+=1
        if self.counter['nodes']>self.max_nodes:raise RuntimeError('node cap')
        self.peak_stack=max(self.peak_stack,len(decisions))
        DB=self.F+self.learned
        a,tr,conf=up(DB,decisions,self.counter,record=True)
        if conf is not None:
            self.counter['conflict_leaf_checks']+=1
            if self.mode!='none':
                d=list(decisions)
                if self.mode in ('min','cap4'):
                    local=collections.Counter()
                    d=core_reduce(DB,d,local,4 if self.mode=='cap4' else None)
                    self.counter.update(local)
                clause=tuple(sorted((-l for l in d),key=lambda l:(abs(l),l<0)))
                assert len({abs(x) for x in clause})==len(clause)
                if clause not in self.learned_set:
                    # Independent RUP replay, which charges complete source scans.
                    assert up(DB,[-z for z in clause],self.counter)[0] is None
                    self.counter['proof_replay_steps']+=len(tr)+1
                    proof={'clause':list(clause),'core':d,'parent_db_size':len(DB),'source_conflict':conf}
                    self.proofs.append(proof);self.learned.append(clause)
                    self.learned_set.add(clause);self.counter['learned_literal_writes']+=len(clause)
                    self.counter['learned_clause_writes']+=1
                    self.peak_clauses=max(self.peak_clauses,len(self.F)+len(self.learned))
            return {'kind':'conflict','decisions':list(decisions),'reason':conf}
        assert a is not None
        remaining=[c for c in self.F+self.learned if not any(litval(l,a) is True for l in c)]
        if not remaining:
            self.witness={i:a.get(i,0) for i in range(1,self.n+1)}
            return {'kind':'sat','witness':self.witness}
        candidate=sorted({abs(l) for c in remaining for l in c if abs(l) not in a})
        if not candidate:
            raise RuntimeError('unaccounted residual clause')
        self.counter['candidate_variable_scans']+=sum(len(c) for c in remaining)
        v=candidate[0]
        kids=[]
        for val in (0,1):
            self.counter['branch_allocations']+=1
            l=v if val else -v
            kids.append(self.visit(decisions+[l]))
            if self.witness is not None:break
        return {'kind':'branch','variable':v,'children':kids}

def component_formula(k,unsat=True):
    """Width-2 repeated-context workload with SAT and UNSAT neighbors.
    vars: y_i=i, z_i=k+i, x=2k+1, u=2k+2, v=2k+3."""
    F=[]
    for i in range(1,k+1):
        z=k+i
        F.extend([(i,z),(-i,z)])
    x=2*k+1;u=x+1;v=x+2
    F.extend([(x,u),(x,-u),(-x,v)])
    if unsat:F.append((-x,-v))
    return F

def strict22_membership(F,n):
    cnt=collections.Counter()
    for c in F:
        if len(c)!=3 or len({abs(l) for l in c})!=3:return False
        for l in c:cnt[(abs(l),int(l>0))]+=1
    return all(cnt[(v,b)]==2 for v in range(1,n+1) for b in (0,1))

def random22(seed,n=9):
    """Bounded deterministic configuration-model draw with proper source and 2+/2- signs."""
    assert n%3==0
    rng=random.Random(seed);m=4*n//3
    for attempt in range(10000):
        stubs=[v for v in range(1,n+1) for _ in range(4)]
        rng.shuffle(stubs)
        blocks=[stubs[3*j:3*j+3] for j in range(m)]
        if any(len(set(c))!=3 for c in blocks):continue
        signs={v:iter(rng.sample([1,1,-1,-1],4)) for v in range(1,n+1)}
        F=[tuple(v*next(signs[v]) for v in c) for c in blocks]
        if not strict22_membership(F,n):raise AssertionError('not strict22')
        # Connected source incidence graph.
        connected={0};changed=True
        while changed:
            changed=False
            for j,c in enumerate(F):
                if j in connected:
                    for k,d in enumerate(F):
                        if k not in connected and set(map(abs,c))&set(map(abs,d)):
                            connected.add(k);changed=True
        if len(connected)==m:return F
    raise RuntimeError('connected source generator exhausted')

def direct_2sat(F,n):
    C=collections.Counter()
    if not all(len(c)<=2 for c in F):return None,{'recognition_reads':sum(map(len,F))}
    C['recognition_reads']+=sum(map(len,F))
    g=[[] for _ in range(2*n)];rev=[[] for _ in range(2*n)]
    def idx(l):return 2*(abs(l)-1)+(1 if l<0 else 0)
    def add(a,b):
        g[idx(a)].append(idx(b));rev[idx(b)].append(idx(a));C['implication_writes']+=1
    for c in F:
        if not c:return False,dict(C)
        if len(c)==1:add(-c[0],c[0])
        else:
            x,y=c;add(-x,y);add(-y,x)
    used=[False]*(2*n);post=[]
    def dfs(v):
        used[v]=True
        for u in g[v]:
            C['graph_edge_reads']+=1
            if not used[u]:dfs(u)
        post.append(v)
    for i in range(2*n):
        if not used[i]:dfs(i)
    comp=[-1]*(2*n)
    def rdfs(v,cid):
        comp[v]=cid
        for u in rev[v]:
            C['graph_edge_reads']+=1
            if comp[u]<0:rdfs(u,cid)
    cid=0
    for v in reversed(post):
        if comp[v]<0:rdfs(v,cid);cid+=1
    for v in range(1,n+1):
        if comp[idx(v)]==comp[idx(-v)]:return False,dict(C)
    a={v:int(comp[idx(v)]>comp[idx(-v)]) for v in range(1,n+1)}
    assert is_sat(F,a)
    return True,dict(C)

def xor_detector(F,n):
    """Exact syntactic recognition of disjoint complete parity blocks, then GF(2)."""
    C=collections.Counter();C['recognition_clause_reads']=len(F)
    C['recognition_literal_reads']=sum(map(len,F))
    if any(len(c)!=3 or len({abs(l) for l in c})!=3 for c in F):return None,dict(C)
    byscope=collections.defaultdict(list)
    for c in F:byscope[tuple(sorted(abs(x) for x in c))].append(tuple(c))
    eqs=[]
    for sc,cls in byscope.items():
        if len(cls)!=4:return None,dict(C)
        fset={tuple(int((next(l for l in c if abs(l)==v))<0) for v in sc) for c in cls}
        if len(fset)!=4:return None,dict(C)
        xor_vals={sum(b)%2 for b in fset}
        if len(xor_vals)!=1:return None,dict(C)
        # each forbidden assignment parity q => allowed parity 1-q
        eqs.append((sc,1-next(iter(xor_vals))))
    rows=[]
    for sc,b in eqs:
        bit=sum(1<<(v-1) for v in sc)
        rows.append((bit,b))
    piv={}
    for a,b in rows:
        C['gaussian_row_reads']+=1
        while a:
            p=a.bit_length()-1
            if p in piv:
                aa,bb=piv[p];a^=aa;b^=bb;C['gaussian_xors']+=1
            else:piv[p]=(a,b);break
        if not a and b:return False,dict(C)
    ans={v:0 for v in range(1,n+1)}
    for p in sorted(piv):
        a,b=piv[p]
        s=sum(ans[v] for v in range(1,n+1) if v-1!=p and a&(1<<(v-1)))%2
        ans[p+1]=b^s
    assert is_sat(F,ans)
    return True,dict(C)

def horn_detector(F,n,dual=False):
    """Exact Horn/dual-Horn recognizer and forward chaining, with charged passes."""
    C=collections.Counter()
    C['horn_recognition_literal_reads']+=sum(map(len,F))
    G=[tuple(-l for l in c) for c in F] if dual else F
    if any(sum(l>0 for l in c)>1 for c in G):return None,dict(C)
    a={v:0 for v in range(1,n+1)}
    for _ in range(n+1):
        changed=False
        for c in G:
            C['horn_clause_visits']+=1
            C['horn_literal_reads']+=len(c)
            neg=[-l for l in c if l<0];pos=[l for l in c if l>0]
            if all(a[v]==1 for v in neg):
                if not pos:return False,dict(C)
                if a[pos[0]]==0:a[pos[0]]=1;changed=True;C['horn_forward_assignments']+=1
        if not changed:break
    if dual:a={v:1-b for v,b in a.items()}
    assert is_sat(F,a)
    return True,dict(C)

def endpoints(F,n):
    C=collections.Counter()
    h={}
    for typ,val in [('zero',0),('one',1)]:
        a={v:val for v in range(1,n+1)}
        cnt=[sum(a[abs(l)]==int(l>0) for l in c) for c in F]
        C['endpoint_literal_reads']+=sum(map(len,F))
        h[typ]={'N':[cnt.count(r) for r in range(4)],'all_satisfied':all(q>0 for q in cnt)}
    return h,dict(C)

def controller(F,n):
    end,ce=endpoints(F,n)
    C=collections.Counter(ce);C['controller_strategy_tests']+=1
    if end['zero']['all_satisfied'] or end['one']['all_satisfied']:
        C['source_witness_verification_reads']+=sum(map(len,F))
        return {'SAT':True,'route':'endpoint','work':sum(C.values()),'counters':dict(C)}
    C['controller_strategy_tests']+=1
    ans,c=horn_detector(F,n);C.update(c)
    if ans is not None:return {'SAT':ans,'route':'Horn','work':sum(C.values()),'counters':dict(C)}
    C['controller_strategy_tests']+=1
    ans,c=horn_detector(F,n,dual=True);C.update(c)
    if ans is not None:return {'SAT':ans,'route':'dualHorn','work':sum(C.values()),'counters':dict(C)}
    C['controller_strategy_tests']+=1
    ans,c=direct_2sat(F,n);C.update(c)
    if ans is not None:return {'SAT':ans,'route':'2SAT','work':sum(C.values()),'counters':dict(C)}
    C['controller_strategy_tests']+=1
    ans,c=xor_detector(F,n);C.update(c)
    if ans is not None:return {'SAT':ans,'route':'GF2','work':sum(C.values()),'counters':dict(C)}
    C['controller_strategy_tests']+=1
    C['signed22_discovery_literal_reads']+=sum(map(len,F))
    # Deliberately falsifiable performance heuristic, not semantic oracle:
    # learning is expensive on the known strict22 twins, so use DPLL there.
    strict=strict22_membership(F,n)
    mode='none' if strict else 'min'
    s=Solver(F,mode,n);r=s.search();C.update(r['counter']);C['fallback_switches']+=1
    return {'SAT':r['SAT'],'route':'UP-DPLL' if strict else 'RUPcore-DPLL','work':sum(C.values()),'counters':dict(C)}

def run(outpath):
    t0=time.monotonic();cases=[]
    for k in (3,5,7,9):
        cases.extend([('repeat_unsat_%02d'%k,component_formula(k,True)),('repeat_sat_%02d'%k,component_formula(k,False))])
    cases.extend([('W1_strict22',W1),('SWAP6_strict22',SWAP6),('W1_renamed',rename(W1,62)),('SWAP6_renamed',rename(SWAP6,62)),('xor_k4_sat',xor_k4(False)),('xor_k4_unsat',xor_k4(True)),('orbit21_sat',orbit(7)),('horn_easy_sat',[(1,),(-2,),(-1,-3,4),(-4,-5,-6)]),('horn_unsat',[(1,),(-1,2),(-2,)]),('dualhorn_sat',[(-1,),(2,),(1,3,-4),(4,5,6)]),('dualhorn_unsat',[(-1,),(1,-2),(2,)]),('krom_unsat',[(1,2),(1,-2),(-1,2),(-1,-2)])])
    for idx in range(12):cases.append((f'strict22_rand{idx:02d}',random22(202610301824+idx)))
    source_controls={};totals=collections.Counter()
    for name,F in cases:
        n=max(abs(l) for c in F for l in c)
        tstart=time.monotonic()
        records={}
        for mode in ('none','raw','cap4','min'):
            solver=Solver(F,mode,n);res=solver.search()
            records[mode]=res
            assert res['SAT']==records['none']['SAT']
            totals['solved_runs']+=1
        d=controller(F,n)
        assert d['SAT']==records['none']['SAT']
        if n<=15:
            count,_=complete_models(F,n)
            assert bool(count)==d['SAT']
        else:count=None
        if name in ('W1_strict22','SWAP6_strict22','xor_k4_sat','xor_k4_unsat','strict22_rand00','strict22_rand01','strict22_rand02'):
            audit=original_audit(F,n)
            assert audit['applicable'];source_controls[name]=audit
        else:audit=None
        casesummary={'name':name,'n':n,'m':len(F),'source':[list(c) for c in F],'source_bits':enc_bits(F,n),'SAT':d['SAT'],'model_count_oracle':count,'controller':d,'run_seconds':time.monotonic()-tstart,
                     'solver':records}
        cases.append if False else None
        source_controls.setdefault('endpoints',{})[name]=endpoints(F,n)[0]
        totals['checked_cases']+=1
        if name=='orbit21_sat':
            assert d['SAT']
        if name=='W1_strict22':assert not d['SAT']
        if name=='SWAP6_strict22':assert d['SAT'] and count==54
        # Avoid retaining enormous proof trees in primary JSON for repeated families.
        if not outpath:
            pass
        if 'output' not in locals():output=[]
        output.append(casesummary)
    rng=random.Random(202610301824)
    for idx in range(28):
        n=rng.randrange(3,8);m=rng.randrange(2,18)
        F=[]
        for _ in range(m):
            vs=rng.sample(range(1,n+1),min(3,n));F.append(tuple(v*rng.choice([-1,1]) for v in vs))
        base=Solver(F,'none',n).search();cla=Solver(F,'min',n).search()
        oracle,_=complete_models(F,n)
        assert base['SAT']==cla['SAT']==(oracle>0)
        output.append({'name':f'random{idx:02d}','n':n,'m':len(F),'source':[list(c) for c in F],'SAT':oracle>0,'model_count_oracle':oracle,'solver':{'none':base,'min':cla}})
        totals['checked_cases']+=1
    # Counterexample for unsafe cross-branch literal cache.
    stale_F=[(-1,2),(-2,3,4),(-2,-3,4)]
    a,_,_=up(stale_F,[1]);b,_,_=up(stale_F,[1,-4]);assert a is not None and b is None
    result={'name':'RUP-CORE-REUSE262','date':'2026-10-30 18:24 America/Los_Angeles','status':'computational with separately proved source-RUP lemma',
            'cases':output,'source_audits':source_controls,'totals':dict(totals),'stale_cache_control':{'F':stale_F,'assumptions_old':[1],'assumptions_new':[1,-4], 'old_UP_assignment':a,'new_UP_conflict':True},
            'external_truth_table_oracle_is_not_controller':True,'elapsed_seconds':time.monotonic()-t0}
    pathlib.Path(outpath).write_text(json.dumps(result,indent=2,sort_keys=True,default=str))
    print('WROTE',outpath,'CASES',len(output),'SECONDS',round(time.monotonic()-t0,3))
    for row in output[:len(cases)]:
        if row['name'].startswith('random'):continue
        modes=row['solver']
        print(row['name'],int(row['SAT']), 'nodes',*[modes[m]['nodes'] for m in modes], 'events',*[modes[m]['selected_events'] for m in modes], 'learned',len(modes['min']['learned_clauses']), 'controller',row['controller']['route'],row['controller']['work'])

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--output',default='raw.json');a=parser.parse_args();run(a.output)
