#!/usr/bin/env python3
"""LSPV-4 BUCKET-FLIP247: source-indexed extremes, O(1) gain update on signed22,
fully charged bounded strict-descent with source-UP-DPLL fallback.
Stdlib only. Deterministic seed 202610300336. Python >=3.10.
Finite experiments are not a general P-vs-NP result.
"""
import collections, hashlib, json, random, sys, time, tracemalloc
from pathlib import Path

SEED = 202610300336
W1 = '''-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'''
H1 = ((1, 3, 5), (1,-3,6), (-1,4,5), (-1,-4,6), (2,3,-5), (2,-3,-6), (-2,4,-5), (-2,-4,-6))

def parse(s): return tuple(tuple(map(int, c.split())) for c in s.split(';'))

def h_ring(r):
    out=[]
    for j in range(r):
        for k,c in enumerate(H1):
            out.append(tuple((1 if l>0 else -1)*(6*((j+r-1)%r if k==0 and pos==0 else j)+abs(l)) for pos,l in enumerate(c)))
    return tuple(out)

def k4_paired():
    D=((1,2,3), (1,4,5), (2,4,6), (3,5,6))
    return D+tuple(tuple(-l for l in c) for c in D)

def xor3(par):
    clauses=[]
    for mask in range(8):
        if mask.bit_count()%2 != par:
            clauses.append(tuple(-v if ((mask>>(v-1))&1) else v for v in (1,2,3)))
    return tuple(clauses)

def odd_k4():
    inc=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
    return tuple(c for j,vs in enumerate(inc) for c in (
        tuple(-v if ((mask>>q)&1) else v for q,v in enumerate(vs))
        for mask in range(8) if mask.bit_count()%2 != (1 if j==0 else 0)))

def dense_planted():
    rng=random.Random(SEED)
    planted=0b101011001
    seen=set()
    while len(seen)<32:
        vs=rng.sample(range(1,10),3)
        ls=tuple(sorted((v if rng.randrange(2) else -v for v in vs), key=lambda l:abs(l)))
        if any(lit_true(l, planted) for l in ls): seen.add(ls)
    return tuple(sorted(seen))

def lit_true(l, mask): return bool((mask>>(abs(l)-1)) & 1)==(l>0)

def truth(F, mask): return [sum(lit_true(l,mask) for l in c) for c in F]

def hist(ts): return [ts.count(i) for i in range(4)]

def formula_sat(F,mask): return all(any(lit_true(l,mask) for l in c) for c in F)

def nvars(F): return max(abs(l) for c in F for l in c)

def signed22(F):
    n=nvars(F)
    d=collections.Counter(l for c in F for l in c)
    return all(len(c)==3 and len({abs(l) for l in c})==3 for c in F) and len(F)*3==4*n and all(d[i]==2 and d[-i]==2 for i in range(1,n+1))

def audits(F, name):
    n=nvars(F); m=len(F); allmask=(1<<n)-1
    clause_records=[]; pair_records=[]; pair_checks=0
    for j,c in enumerate(F):
        occ=[]
        for k,l in enumerate(c):
            s=1 if l>0 else 0
            occ.append(dict(source_clause=j, occurrence_index=k, variable=abs(l), literal=l,
                            S_all_TRUE=s, S_inverted_U_all_FALSE=1-s,
                            U_all_FALSE=1-s, U_inverted_S_all_TRUE=s))
        clause_records.append(dict(clause_index=j,literals=list(c),occurrences=occ,
                                   local_S={str(x['variable']):x['S_all_TRUE'] for x in occ},
                                   local_U={str(x['variable']):x['U_all_FALSE'] for x in occ}))
    for j,c in enumerate(F):
        a={abs(l):1 if l>0 else -1 for l in c}
        for k in range(j+1,m):
            d=F[k]; b={abs(l):1 if l>0 else -1 for l in d}
            same=sorted(v for v in a.keys()&b.keys() if a[v]==b[v])
            opp=sorted(v for v in a.keys()&b.keys() if a[v]!=b[v])
            modes={'SS':not bool(opp),'SU':not bool(same),'US':not bool(same),'UU':not bool(opp)}
            vars_=sorted(a.keys()|b.keys()); brute={k:False for k in modes}
            for state in range(1<<len(vars_)):
                assign={v:(state>>q)&1 for q,v in enumerate(vars_)}
                t1=sum(assign[abs(l)]==(1 if l>0 else 0) for l in c)
                t2=sum(assign[abs(l)]==(1 if l>0 else 0) for l in d)
                for tag,(u,v) in {'SS':(len(c),len(d)),'SU':(len(c),0),'US':(0,len(d)),'UU':(0,0)}.items():
                    if (t1,t2)==(u,v): brute[tag]=True
            assert modes==brute, (name,j,k,modes,brute)
            pair_checks+=4
            pair_records.append(dict(source_pair=[j,k],same_polarity_shared=same,
                                     opposite_polarity_shared=opp,**modes))
    triples=[]; tri_checks=0
    for (j,k,h) in list(__import__('itertools').combinations(range(m),3))[:12]:
        cs=[F[j],F[k],F[h]]
        vars_=sorted({abs(l) for c in cs for l in c})
        for mode in range(8):
            targets={}; compatible=True
            for b,c in enumerate(cs):
                for l in c:
                    val=(1 if l>0 else 0) if ((mode>>b)&1) else (0 if l>0 else 1)
                    v=abs(l)
                    if v in targets and targets[v]!=val: compatible=False
                    targets[v]=val
            exhaustive=False
            for mask in range(1<<len(vars_)):
                assign={v:(mask>>q)&1 for q,v in enumerate(vars_)}
                if all(sum(assign[abs(l)]==(1 if l>0 else 0) for l in c) == (len(c) if ((mode>>b)&1) else 0) for b,c in enumerate(cs)):
                    exhaustive=True;break
            assert compatible==exhaustive
            triples.append(dict(source_clauses=[j,k,h],modes=['S' if mode>>b&1 else 'U' for b in range(3)],realizable=compatible))
            tri_checks+=1
    exactmask = list(range(1<<n)) if n<=15 else list(sorted({0,allmask,*[random.Random(SEED+i).randrange(1<<n) for i in range(500)]}))
    for a in exactmask:
        t=truth(F,a); tt=truth(F,allmask^a)
        assert len(t)==m and all(u+v==len(F[j]) for j,(u,v) in enumerate(zip(t,tt)))
        if all(len(c)==3 for c in F): assert hist(tt)==list(reversed(hist(t)))
    # Coherent global original-variable one/two/three/multiple flip trails, including inversion.
    sample_masks=[0,1,1|2,1|2|4,allmask,allmask^1,0]
    if n>=6:sample_masks += [0,1,9,41,allmask^41]
    sample_masks=list(dict.fromkeys((step,mask) for step,mask in enumerate(sample_masks)))
    global_flip_probes=[];last=None
    for step,a in sample_masks:
        t=truth(F,a)
        rec=dict(step=step,mask=a,global_original_variable_assignments={str(v):(a>>(v-1))&1 for v in range(1,n+1)},
                 t=t,N=hist(t),ordinary_clause_SAT=[v>0 for v in t],
                 local_extreme_source_clause_status=['U' if u==0 else ('S' if u==len(F[j]) else 'M') for j,u in enumerate(t)])
        if last is not None:
            flipped=[v for v in range(1,n+1) if ((a^last)>>(v-1))&1]
            oldt=truth(F,last)
            for j,c in enumerate(F):
                s=set(flipped)
                expected=oldt[j]+sum(abs(l) in s and not lit_true(l,last) for l in c)-sum(abs(l) in s and lit_true(l,last) for l in c)
                assert expected==t[j],(name,step,j)
            rec['flip_set_from_previous']=flipped
            rec['transition_counts']={f'{i}->{k}':sum(1 for x,y in zip(oldt,t) if x==i and y==k) for i in range(4) for k in range(4) if any(x==i and y==k for x,y in zip(oldt,t))}
        global_flip_probes.append(rec);last=a
    endpoints={}
    for label,a in [('all_false',0),('all_true',allmask)]:
        t=truth(F,a)
        endpoints[label]=dict(mask=a,t=t,N=hist(t),false_original_clauses=[j for j,v in enumerate(t) if v==0],fully_TRUE_original_clauses=[j for j,v in enumerate(t) if v==3],F_sat=not 0 in t)
    # Exact provenance-checked source-parent resolvents and prohibited cubes.
    resolvents=[]
    for j,c in enumerate(F):
        for k in range(j+1,m):
            d=F[k]
            for l in c:
                if -l not in d: continue
                residual=[x for x in c if x!=l]+[x for x in d if x!=-l]
                if any(-x in residual for x in residual): continue
                R=tuple(sorted(set(residual),key=lambda x:(abs(x),x)))
                cube={str(abs(x)):int(x<0) for x in R}
                # Falsifying R makes parent clauses opposed units on pivot.
                for a in range(2):
                    sample={int(v):vv for v,vv in cube.items()};sample[abs(l)]=a
                    assert not all(any(sample[abs(x)]==(1 if x>0 else 0) for x in q) for q in (c,d))
                resolvents.append(dict(source_parents=[j,k],pivot=abs(l),pivot_literal=l,resolvent=R,forbidden_cube=cube,
                                       proof='Under forbidden cube parents become opposite unit requirements on pivot'))
                if len(resolvents)>=12: break
            if len(resolvents)>=12:break
        if len(resolvents)>=12:break
    opposite=sum(bool(x['opposite_polarity_shared']) for x in pair_records)
    same=sum(bool(x['same_polarity_shared']) for x in pair_records)
    mixed=sum(bool(x['same_polarity_shared']) and bool(x['opposite_polarity_shared']) for x in pair_records)
    diagnostic_work_estimates=dict(occurrence_target_bits_written=4*sum(map(len,F)),
      dense_matrix_bits=4*(m*(m-1)//2),
      source_pair_mode_enumeration_checks=pair_checks,
      source_pair_brute_assignments=sum(1<<len({abs(l) for q in (F[j],F[k]) for l in q}) for j in range(m) for k in range(j+1,m)),
      complement_source_literal_evaluations=2*sum(map(len,F))*len(exactmask))
    return dict(n=n,m=m,signed22=signed22(F),diagnostic_work_estimates=diagnostic_work_estimates,original_clauses=clause_records,pair_modes=pair_records,
                triple_modes=triples,source_pair_checks=pair_checks,source_triple_checks=tri_checks,
                complement_assignments_checked=len(exactmask),endpoints=endpoints,
                coherent_flip_probes=global_flip_probes,
                resolvent_forbidden_cubes=resolvents,nondefault_pairs=sum(bool(x['same_polarity_shared'] or x['opposite_polarity_shared']) for x in pair_records),
                opposite_pairs=opposite,same_pairs=same,mixed_all_extreme_forbidden_pairs=mixed)

class Ledger(collections.Counter):
    def tick(self,k,c=1):self[k]+=c
    def total(self):return sum(self.values())

class Descender:
    def __init__(self,F,n,a,strict=True,trace_mode='full'):
        assert trace_mode in ('full','delta')
        self.trace_mode=trace_mode
        self.F=F;self.n=n;self.m=len(F);self.mask=a;self.strict=strict;self.ledger=Ledger()
        self.occ=[[] for _ in range(n+1)]
        for j,c in enumerate(F):
            for l in c:
                self.ledger.tick('input_occurrence_read')
                self.occ[abs(l)].append((j,l))
        self.dmax=max(len(z) for z in self.occ)
        self.t=[];self.gain=[0]*(n+1)
        for c in F:
            t=sum(self.eval(l) for l in c); self.t.append(t)
        self.N=hist(self.t)
        for j,c in enumerate(F):
            for v,delta in self.contrib(j):
                self.gain[v]+=delta
                self.ledger.tick('initial_gain_add')
        self.head=[0]*(2*self.dmax+1)
        self.prev=[0]*(n+1);self.nxt=[0]*(n+1)
        for v in range(1,n+1):self.insert(v)
        self.trace=[self.capture(None,0,changed=None)]
    def eval(self,l):
        self.ledger.tick('literal_truth_evaluation')
        return lit_true(l,self.mask)
    def capture(self,v,g,changed):
        result=dict(mask=self.mask,flip_variable=v,gain=g,N=list(self.N))
        self.ledger.tick('trace_metadata_words',len(result['N'])+3)
        if self.trace_mode=='full':
            self.ledger.tick('trace_full_clause_slots',self.m)
            result.update(t=list(self.t), false_source_clauses=[j for j,t in enumerate(self.t) if t==0])
        else:
            if changed is None:
                self.ledger.tick('trace_delta_initial_clause_slots',self.m)
                result['initial_t']=list(self.t)
            else:
                self.ledger.tick('trace_delta_changed_clause_slots',len(changed))
                result['changed_source_clauses']=changed
        return result
    def contrib(self,j):
        self.ledger.tick('clause_contribution_read')
        c=self.F[j]; t=self.t[j]
        if t==0:return [(abs(l),1) for l in c]
        if t==1:
            return [(abs(l),-1) for l in c if self.eval(l)]
        return []
    def remove(self,v):
        k=self.gain[v]+self.dmax
        p=self.prev[v]; q=self.nxt[v]
        if p:self.nxt[p]=q
        else:assert self.head[k]==v;self.head[k]=q
        if q:self.prev[q]=p
        self.prev[v]=self.nxt[v]=0
        self.ledger.tick('bucket_link_updates',3)
    def insert(self,v):
        k=self.gain[v]+self.dmax
        assert 0<=k<len(self.head)
        q=self.head[k];self.head[k]=v
        self.prev[v]=0;self.nxt[v]=q
        if q:self.prev[q]=v
        self.ledger.tick('bucket_link_updates',3)
    def best(self):
        for g in range(self.dmax,0,-1):
            self.ledger.tick('bucket_head_tests')
            if self.head[g+self.dmax]:return self.head[g+self.dmax],g
        return None,0
    def update(self,v):
        # Recompute only original clauses adjacent to the globally flipped variable.
        clauses={j for j,l in self.occ[v]}
        affected={abs(l) for j in clauses for l in self.F[j]}
        self.ledger.tick('affected_clause_index_reads',len(clauses))
        for u in affected:self.remove(u)
        for j in clauses:
            for u,delta in self.contrib(j):
                self.gain[u]-=delta
                self.ledger.tick('gain_component_updates')
        self.mask^=1<<(v-1);self.ledger.tick('global_variable_flip')
        changes=[]
        for j in sorted(clauses):
            old=self.t[j]
            self.N[old]-=1
            self.t[j]=sum(self.eval(l) for l in self.F[j]);self.ledger.tick('clause_truth_count_rebuild')
            self.N[self.t[j]]+=1
            changes.append([j,old,self.t[j]])
            self.ledger.tick('category_bucket_updates',2)
        for j in clauses:
            for u,delta in self.contrib(j):
                self.gain[u]+=delta
                self.ledger.tick('gain_component_updates')
        for u in affected:self.insert(u)
        assert sum(self.N)==self.m
        return changes
    def run(self):
        while self.N[0]>0:
            v,g=self.best()
            if v is None:
                return dict(status='UNRESOLVED_LOCAL_OPTIMUM',trace=self.trace,work=self.ledger.total(),ledger=dict(self.ledger),flips=len(self.trace)-1)
            assert g==self.gain[v]>0
            before=self.N[0]
            changed=self.update(v)
            assert self.N[0]==before-g
            self.trace.append(self.capture(v,g,changed))
        assert formula_sat(self.F,self.mask)
        self.ledger.tick('final_witness_literal_checks',sum(map(len,self.F)))
        return dict(status='SAT',witness=self.mask,trace=self.trace,work=self.ledger.total(),ledger=dict(self.ledger),flips=len(self.trace)-1)

def naive_score_all(F,n,mask):
    # Independent full-rescan: counts both original support comparisons and literal evaluations.
    scores={}
    events=0; support_checks=0
    for v in range(1,n+1):
        gain=0
        for c in F:
            support_checks+=len(c)
            if v not in [abs(l) for l in c]:continue
            t=0
            for l in c:t+=lit_true(l,mask);events+=1
            if t==0:gain+=1
            elif t==1:
                for l in c:
                    events+=1
                    if abs(l)==v and lit_true(l,mask):gain-=1
        scores[v]=gain
    return scores,events,support_checks

def verify_gain_trail(F,n,run):
    work=0; source_work=0; t0=None
    for step in run['trace']:
        scores,cost,support=naive_score_all(F,n,step['mask']);work+=cost;source_work+=support
        if 't' in step:t=step['t']
        elif 'initial_t' in step:t=step['initial_t'];t0=list(t)
        else:
            for j,old,new in step['changed_source_clauses']:
                assert t0[j]==old
                t0[j]=new
            t=list(t0)
        assert t==truth(F,step['mask']) and hist(t)==step['N']
        if step['flip_variable'] is not None:
            assert step['gain']>0
    return work,source_work

# Independent deterministic complete source-UP-DPLL proof tree, not a semantic oracle.
def dpll(F,n):
    led=Ledger()
    def solve(assign):
        led.tick('recursion_nodes')
        trail=[]
        while True:
            forced=None
            all_sat=True
            for j,c in enumerate(F):
                led.tick('clauses_scanned')
                satisfied=False; free=[]
                for l in c:
                    led.tick('literal_read')
                    v=abs(l)
                    if v not in assign:free.append(l)
                    elif assign[v]==int(l>0):satisfied=True;break
                if satisfied:continue
                all_sat=False
                if not free:
                    led.tick('conflict_leaves')
                    return False,{'propagations':trail,'conflict':j},None
                if len(free)==1:
                    z=free[0]
                    forced=(abs(z),int(z>0),j)
                    break
            if forced is None:break
            v,bit,j=forced
            assert v not in assign
            assign[v]=bit
            trail.append([v,bit,j])
            led.tick('unit_propagations')
        if all_sat or len(assign)==n:
            mask=sum(bit<<(v-1) for v,bit in assign.items())
            assert formula_sat(F,mask)
            led.tick('witness_literal_checks',sum(map(len,F)))
            return True,{'propagations':trail,'witness':mask},mask
        v=next(v for v in range(1,n+1) if v not in assign)
        led.tick('branch_decisions')
        for bit in (0,1):
            new=dict(assign);new[v]=bit
            led.tick('copy_assignments',len(assign)+1)
            result,tree,model=solve(new)
            if result:return True,{'propagations':trail,'decision':[v,bit], 'successful_child':tree},model
            if bit==0:zero=tree
            else:one=tree
        return False,{'propagations':trail,'branch_variable':v,'zero':zero,'one':one},None
    success,tree,model=solve({})
    return dict(sat=success,model=model,nodes=led['recursion_nodes'],work=led.total(),ledger=dict(led),proof_tree=tree)

def replay_unsat(F,n,tree):
    led=Ledger()
    def rec(node,prior):
        a=prior.copy()
        for v,bit,j in node.get('propagations',[]):
            assert v not in a
            c=F[j];led.tick('source_clause_check')
            unassigned=[];is_sat=False
            for l in c:
                led.tick('source_literal_check')
                if abs(l) not in a:unassigned.append(l)
                elif a[abs(l)]==int(l>0):is_sat=True
            assert not is_sat and len(unassigned)==1 and abs(unassigned[0])==v and int(unassigned[0]>0)==bit
            a[v]=bit
            led.tick('proof_unit_replay')
        if 'conflict' in node:
            c=F[node['conflict']];led.tick('proof_leaves')
            for l in c:
                led.tick('source_literal_check')
                assert abs(l) in a and a[abs(l)]!=int(l>0)
        else:
            assert 'branch_variable' in node
            v=node['branch_variable']; assert v not in a
            led.tick('proof_branch_checks')
            for bit,child in ((0,node['zero']),(1,node['one'])):
                b=a.copy();b[v]=bit;rec(child,b)
    rec(tree,{})
    return led.total(),dict(led)

def benchmark(F,name):
    n=nvars(F);audit=audits(F,name)
    start=time.monotonic()
    tracemalloc.start()
    baseline=dpll(F,n)
    _,base_peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    if not baseline['sat']:
        check_work,check_events=replay_unsat(F,n,baseline['proof_tree'])
        baseline['unsat_proof_replay_work']=check_work
        baseline['unsat_proof_replay_event_types']=check_events
    else:
        assert formula_sat(F,baseline['model'])
        baseline['witness_verified']=True
    d_runs=[]; naive_recompute_cost=0;naive_support_cost=0
    tracemalloc.start()
    for startmask in (0,(1<<n)-1):
        dd=Descender(F,n,startmask)
        x=dd.run()
        x['endpoint']=startmask
        d_runs.append(x)
        if x['status']=='SAT':break
    if d_runs[-1]['status']=='SAT':
        answer=True;model=d_runs[-1]['witness'];fallback=None
    else:
        # Unit-propagation DPLL fallback must be paid for; reuse cached proof only in audit,
        # the solver below is deliberately independently invoked.
        fallback=dpll(F,n)
        answer=fallback['sat'];model=fallback['model']
        assert answer==baseline['sat']
    _,opt_peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    # Independent trajectory verification is deliberately OUTSIDE the measured solver invocation.
    for x in d_runs:
        lit_work,support_work=verify_gain_trail(F,n,x)
        naive_recompute_cost+=lit_work
        naive_support_cost+=support_work
    opt_work=sum(x['work'] for x in d_runs)+(fallback['work'] if fallback else 0)
    assert answer==baseline['sat']
    if answer:assert model is not None and formula_sat(F,model)
    # Paired source diagnostics are requested, but NOT used by either decision controller.
    # We report their counts separately; adding to decision work is labeled optional extra.
    proof=baseline['unsat_proof_replay_work'] if not answer else 0
    return dict(name=name,n=n,m=len(F),strict22=signed22(F),audit=audit,
                complete_solver={k:v for k,v in baseline.items() if k!='proof_tree'},
                unsat_proof_tree=baseline['proof_tree'] if not answer else None,
                descent_runs=d_runs,optimized_work=opt_work,optimized_peak_python_bytes=opt_peak,
                baseline_peak_python_bytes=base_peak,naive_candidate_rescan_literal_evals=naive_recompute_cost,
                naive_candidate_rescan_support_reads=naive_support_cost,
                diagnostic_pair_mode_checks=audit['source_pair_checks'],
                decision_including_common_unsat_proof_checks=dict(baseline=baseline['work']+proof,hybrid=opt_work+proof),
                seconds=round(time.monotonic()-start,6))

def main():
    F=parse(W1)
    Fprime=[list(c) for c in F]
    assert Fprime[9][1]==-6 and Fprime[13][1]==6
    Fprime[9][1]=6;Fprime[13][1]=-6
    Fprime=tuple(tuple(c) for c in Fprime)
    ren=[]
    for c in H1:ren.append(tuple(-l if abs(l)==1 else l for l in c))
    tests={
     'H1_strict22_sat_plateau':h_ring(1),
     'H2_strict22_sat_plateau':h_ring(2),
     'H3_strict22_sat_plateau':h_ring(3),
     'W1_strict22_unsat':F,
     'W1_SWAP6_strict22_sat':Fprime,
     'K4_signed_NAE_paired_sat':k4_paired(),
     'H1_variable_renamed_sat':tuple(ren),
     'XOR3_parity_odd_sat':xor3(1),
     'XOR3_contradiction_unsat':xor3(1)+xor3(0),
     'odd_K4_Tseitin_unsat':odd_k4(),
     'Horn_sat':((1,),(-1,2),(-2,3),(-3,4)),
     '2SAT_unsat':((1,2),(-1,2),(1,-2),(-1,-2)),
     'dense_planted_3CNF_sat':dense_planted(),
    }
    records=[]
    for name,formula in tests.items():
        r=benchmark(formula,name)
        if nvars(formula)<=15:
            exact_models=sum(formula_sat(formula,a) for a in range(1<<nvars(formula)))
            r['external_exhaustive_model_count']=exact_models
            assert (exact_models>0)==r['complete_solver']['sat']
        records.append(r)
        print(name,'baseline',r['complete_solver']['nodes'],r['complete_solver']['work'],
              'hybrid',r['optimized_work'],'steps',[x['flips'] for x in r['descent_runs']],
              'naive_score_replay_litreads',r['naive_candidate_rescan_literal_evals'],flush=True)
    # Independent complete check of initial and changed gain values on EVERY reachable n<=6 assignment.
    for formula in (h_ring(1),k4_paired(),xor3(1),xor3(0)+xor3(1)):
        n=nvars(formula)
        for a in range(1<<n):
            dd=Descender(formula,n,a)
            before,_,_=naive_score_all(formula,n,a)
            assert all(dd.gain[v]==before[v] for v in before)
            for v in range(1,n+1):
                alt=Descender(formula,n,a);alt.update(v)
                after,_,_=naive_score_all(formula,n,a^(1<<(v-1)))
                assert all(alt.gain[i]==after[i] for i in after)
                assert alt.N==hist(truth(formula,alt.mask))
    scaling=[]
    for r in (1,2,4,8,16,32,64):
        base=k4_paired()
        Fblocks=tuple(tuple((1 if l>0 else -1)*(6*j+abs(l)) for l in c) for j in range(r) for c in base)
        assert signed22(Fblocks)
        per_mode={}
        for mode in ('delta','full'):
            d=Descender(Fblocks,nvars(Fblocks),0,trace_mode=mode)
            runner=d.run()
            assert runner['status']=='SAT' and formula_sat(Fblocks,runner['witness'])
            per_mode[mode]={'flips':runner['flips'],'work':runner['work'],
               'trace_slots':sum(v for k,v in runner['ledger'].items() if k.startswith('trace_')),
               'solver_nontrace_work':sum(v for k,v in runner['ledger'].items() if not k.startswith('trace_')),
               'trace_entry_count':len(runner['trace'])}
        assert per_mode['delta']['flips']==per_mode['full']['flips']==2*r
        assert per_mode['delta']['solver_nontrace_work']==per_mode['full']['solver_nontrace_work']
        scaling.append(dict(blocks=r,n=nvars(Fblocks),m=len(Fblocks),runs=per_mode))
    output=dict(run_id='BUCKET-FLIP247',date='2026-10-30',seed=SEED,
                statement='Restricted signed22 linear strict descent via bounded-gain intrusive bucket queue; no complete SAT claim',
                cases=records,scaling=scaling,strict_gain_full_replay='PASS')
    file=Path(__file__).with_name('LSPV4_BUCKET_FLIP247_primary_raw.json')
    file.write_text(json.dumps(output,indent=2,sort_keys=True))
    print('PASS',len(records),'cases','bytes',file.stat().st_size,'sha256',hashlib.sha256(file.read_bytes()).hexdigest())
    return output

if __name__=='__main__':main()