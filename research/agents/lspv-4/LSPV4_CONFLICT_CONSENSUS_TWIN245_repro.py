#!/usr/bin/env python3
"""LSPV-4: original clause indexed conflict-consensus flip experiment.

Dependency-free, deterministic. Verifies local extreme targets, their inversions,
coherent assignments, source-parent resolution, proof-carrying UP-DPLL, and a
user-proposed SAT-literal-key flip walk. Reports exact resource event ledgers.

Finite exhaustive checks are NOT an unrestricted SAT lower bound.
"""
import argparse
import collections
import hashlib
import itertools
import json
import random
import sys
import time
import tracemalloc
from pathlib import Path

SEED=202610300236
W1_SOURCE='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
W1=[tuple(map(int,part.split())) for part in W1_SOURCE.split(';')]
H1=[(1,3,5),(1,-3,6),(-1,4,5),(-1,-4,6),(2,3,-5),(2,-3,-6),(-2,4,-5),(-2,-4,-6)]
NAE_DESIGNATED=[(1,2,3),(-1,4,5),(2,4,6),(3,5,6)]

def twin(W):
    F=[list(c) for c in W]
    # 0-based source clauses C9, C13 exchange the polarity of ORIGINAL x6;
    # each original variable retains two positive and two negative occurrences.
    for j in (9,13):
        assert any(abs(l)==6 for l in F[j])
        F[j]=[-l if abs(l)==6 else l for l in F[j]]
    return [tuple(c) for c in F]
TWIN=twin(W1)

def parity3(vars_,value):
    return [tuple(v if bit else -v for v,bit in zip(vars_,bits))
            for bits in itertools.product((0,1),repeat=3)
            if sum(bits)%2 != value]

def tseitin_k4():
    # K4 vertices 0...3, edges as 1...6, charge parity sum odd => UNSAT.
    edges=list(itertools.combinations(range(4),2)); ans=[]
    for v in range(4):
        involved=[idx+1 for idx,(u,w) in enumerate(edges) if v in (u,w)]
        ans+=parity3(involved,1 if v==0 else 0)
    return ans

def dense_planted(seed=SEED):
    rng=random.Random(seed); n=9; model=0b101101011
    seen=set(); F=[]
    while len(F)<30:
        variables=sorted(rng.sample(range(1,n+1),3))
        lits=tuple(v*(1 if rng.getrandbits(1) else -1) for v in variables)
        if lits in seen or not satisfied_clause(lits,model):continue
        F.append(lits);seen.add(lits)
    return F

def get_cases():
    paired=NAE_DESIGNATED+[tuple(-l for l in c) for c in NAE_DESIGNATED]
    return {
        'W1_strict22_UNSAT':W1,
        'SWAP6_strict22_SAT':TWIN,
        'H1_plateau_strict22_SAT':H1,
        'PAIRED_K4_strict22_SAT':paired,
        'HORN_SAT':[(1,-2,-3),(-1,3),(-3,2)],
        'TWO_SAT_UNSAT':[(1,2),(-1,2),(1,-2),(-1,-2)],
        'XOR3_SAT':parity3((1,2,3),0),
        'XOR3_UNSAT':parity3((1,2,3),0)+parity3((1,2,3),1),
        'TSEITIN_K4_UNSAT':tseitin_k4(),
        'DENSE_PLANTED_SAT':dense_planted(),
    }

def nvars(F):return max((abs(l) for c in F for l in c),default=0)
def satisfied_clause(C,a):return any(((a>>(abs(l)-1))&1)==int(l>0) for l in C)
def truth(C,a):return sum(((a>>(abs(l)-1))&1)==int(l>0) for l in C)
def scores(F,a):
    t=[truth(C,a) for C in F]; return t,[sum(k==q for k in t) for q in range(4)]
def is_sat(F,a):return all(satisfied_clause(C,a) for C in F)
def strict22(F):
    n=nvars(F);h=collections.Counter(l for c in F for l in c)
    return (len(F)*3==4*n and all(len(c)==3 and len(set(map(abs,c)))==3 for c in F)
            and all(h[x]==2 and h[-x]==2 for x in range(1,n+1)))
def incidence(F):return [tuple(sorted(map(abs,c))) for c in F]
def full_status(F,a):
    t,N=scores(F,a)
    return {'assignment':{str(i):int((a>>(i-1))&1) for i in range(1,nvars(F)+1)},
            'mask':a,'true_literal_count_by_source_clause':t,'N0_N1_N2_N3':N,
            'false_clause_indices':[j for j,v in enumerate(t) if v==0],
            'disjunctive_SAT':N[0]==0}

def local_target(C,mode):
    return {abs(l):(int(l>0) if mode=='S' else int(l<0)) for l in C}

def clause_extremes(F,book):
    out=[]
    for j,C in enumerate(F):
        sj=local_target(C,'S'); uj=local_target(C,'U')
        occ=[]
        for k,l in enumerate(C):
            book['source_literal_reads']+=1; book['local_target_values']+=4
            v=abs(l);s=sj[v];u=uj[v]
            assert u==1-s
            occ.append({'source_clause_j':j,'source_occurrence_k':k,
                'indexed_variable':f'x_{{{v},{j}}}','original_variable':v,
                'signed_literal':l,'sign':'positive' if l>0 else 'negative',
                'S_literal_TRUE_target_x':s,'invert_S_literal_FALSE_target_x':1-s,
                'U_literal_FALSE_target_x':u,'invert_U_literal_TRUE_target_x':1-u})
        out.append({'original_clause_j':j,'signed_literals':list(C),
                    'S_local_all_literals_TRUE':{str(k):v for k,v in sj.items()},
                    'invert_S_gives_U':{str(k):1-v for k,v in sj.items()},
                    'U_local_all_literals_FALSE':{str(k):v for k,v in uj.items()},
                    'invert_U_gives_S':{str(k):1-v for k,v in uj.items()},
                    'occurrences':occ})
    return out

def pair_modes(F,book,verify=True):
    out=[]; hist=collections.Counter()
    for j,C in enumerate(F):
        CJ={abs(l):int(l>0) for l in C}
        for k in range(j+1,len(F)):
            D=F[k]; CK={abs(l):int(l>0) for l in D}
            shared=sorted(set(CJ)&set(CK))
            same=[v for v in shared if CJ[v]==CK[v]]
            opposite=[v for v in shared if CJ[v]!=CK[v]]
            book['pair_shared_variable_checks']+=len(C)*len(D)
            modes={'SS':not opposite,'SU':not same,'US':not same,'UU':not opposite}
            hist[(len(same),len(opposite))]+=1
            if verify:
                # A union of <=6 original variables; enumerate coherent truth assignments.
                vars_=sorted(set(map(abs,C))|set(map(abs,D)))
                brute={'SS':False,'SU':False,'US':False,'UU':False}
                for mask in range(1<<len(vars_)):
                    bits={v:(mask>>p)&1 for p,v in enumerate(vars_)}
                    ct=sum(bits[abs(l)]==int(l>0) for l in C)
                    dt=sum(bits[abs(l)]==int(l>0) for l in D)
                    if ct==len(C) and dt==len(D):brute['SS']=True
                    if ct==len(C) and dt==0:brute['SU']=True
                    if ct==0 and dt==len(D):brute['US']=True
                    if ct==0 and dt==0:brute['UU']=True
                    book['pair_bruteforce_assignments']+=1
                assert brute==modes,(j,k,brute,modes)
            out.append({'source_clause_pair':[j,k], 'shared_same_sign_original_variables':same,
                        'shared_opposite_sign_original_variables':opposite,
                        'all_literal_extreme_compatibility':modes,
                        'at_least_one_middle_for_every_global_assignment':bool(same and opposite)})
    return out,{'same_'+str(a)+'_opposite_'+str(b):count for (a,b),count in sorted(hist.items())}

def source_resolvents(F,book,limit=None):
    entries=[];seen=set()
    for pivot in range(1,nvars(F)+1):
        pos=[j for j,C in enumerate(F) if pivot in C]
        neg=[j for j,C in enumerate(F) if -pivot in C]
        book['occurrence_discovery_reads']+=sum(len(C) for C in F)*2
        for j in pos:
            for k in neg:
                book['pivot_source_pair_candidates']+=1
                C=F[j];D=F[k]
                raw=[l for l in C if abs(l)!=pivot]+[l for l in D if abs(l)!=pivot]
                book['resolvent_literal_reads']+=len(C)+len(D)
                R=tuple(sorted(set(raw),key=lambda t:(abs(t),t<0)))
                if any(-l in R for l in R):
                    book['tautological_resolvent_candidates']+=1;continue
                if R in seen:continue
                seen.add(R)
                # Certificate: restricting all R literals false reduces source parents to x,-x.
                cube={str(abs(l)):int(l<0) for l in R}
                assert all(not (l in R and -l in R) for l in R)
                r={'parents':[j,k],'pivot':pivot,'non_tautological_resolvent':list(R),
                   'forbidden_partial_cube':cube,
                   'source_certificate':f'Parents C{j},C{k} restrict to x{pivot},not x{pivot} when every resolvent literal is FALSE'}
                if len(R)<=3:entries.append(r)
                else:entries.append(r)
                book['source_resolvent_proof_checks']+=len(C)+len(D)+len(R)
                # Direct syntactic source-parent resolution certificate.
                assert pivot in C and -pivot in D
                assert set(R)==(set(C)-{pivot})|(set(D)-{-pivot})
                if limit and len(entries)>=limit:return entries
    return entries

def pure_vars(F,book):
    signs={i:set() for i in range(1,nvars(F)+1)}
    for C in F:
        for l in C:signs[abs(l)].add(l>0);book['pure_occurrence_reads']+=1
    pure={i:int(True in sign) for i,sign in signs.items() if len(sign)==1}
    conflict=[i for i,sign in signs.items() if len(sign)==2]
    return pure,conflict

def make_incidence(F):
    adj={i:[] for i in range(1,nvars(F)+1)}
    for j,C in enumerate(F):
        for l in C:adj[abs(l)].append((j,l))
    return adj

def move_flip(F,a,t,N,adj,x,book):
    # One coherent GLOBAL variable flip, all occurrences touched, constant per occurrence.
    old=(a>>(x-1))&1; a^=(1<<(x-1))
    delta=[]
    for j,l in adj[x]:
        before=t[j]
        # TRUE literal before becomes FALSE: -1; vice versa: +1.
        before_lit_true=(old==int(l>0))
        after=before+(-1 if before_lit_true else 1)
        assert 0<=after<=len(F[j])
        t[j]=after;N[before]-=1;N[after]+=1
        book['flip_occurrence_updates']+=1
        book['flip_histogram_bucket_updates']+=2
        delta.append({'original_clause_j':j,'before_true_literals':before,'after_true_literals':after})
    book['global_variable_flips']+=1
    return a,delta

def key_walk(F,seed,policy,book):
    n=nvars(F); adj=make_incidence(F)
    pure,conflict=pure_vars(F,book)
    a=seed;t,N=scores(F,a);book['status_clause_scans']+=len(F)
    book['status_literal_reads']+=sum(map(len,F))
    initial={'step':0,'global_assignment_mask':a,'N0_N1_N2_N3':N.copy(),
             'clause_t':t.copy(),'false_clause_indices':[j for j,u in enumerate(t) if u==0],
             'action':'globally coherent endpoint'}
    trail=[initial]
    used=set()
    # Corrected interpretation: only variables without contradictory local U
    # demands can be inverted globally without choosing between occurrences.
    for x,value in sorted(pure.items()):
        if ((a>>(x-1))&1)!=value:
            old=a;a,delta=move_flip(F,a,t,N,adj,x,book)
            trail.append({'step':len(trail),'action':'invert coherent pure-U target',
                          'key_variable':x,'old_mask':old,'global_assignment_mask':a,
                          'N0_N1_N2_N3':N.copy(),'clause_t':t.copy(),
                          'false_clause_indices':[j for j,u in enumerate(t) if u==0],
                          'source_clause_updates':delta})
        used.add(x)
    # User's SAT-key rule, or a failure-first repair adjustment. Both flip each
    # key at most once per endpoint; UNSAT is never inferred on exhaustion.
    for _ in range(len(conflict)):
        if N[0]==0:break
        selected=None
        if policy=='SAT_KEY':
            for j,C in enumerate(F):
                book['SAT_key_clause_scans']+=1
                if t[j]==0:continue
                for l in C:
                    book['SAT_key_occurrence_checks']+=1
                    x=abs(l)
                    if x not in used and ((a>>(x-1))&1)==int(l>0):
                        selected=(x,j,l);break
                if selected:break
        elif policy=='FALSE_REPAIR':
            for j,C in enumerate(F):
                book['repair_clause_scans']+=1
                if t[j]!=0:continue
                for l in C:
                    book['repair_occurrence_checks']+=1
                    x=abs(l)
                    if x not in used:
                        # Choose smallest x in earliest violated original clause,
                        # no hidden SAT oracle; allow plateaus and uphill moves.
                        if selected is None or x<selected[0]:selected=(x,j,l)
                if selected:break
        else:raise ValueError(policy)
        if selected is None:break
        x,j,l=selected;old=a;a,delta=move_flip(F,a,t,N,adj,x,book)
        used.add(x)
        assert scores(F,a)==(t,N)
        trail.append({'step':len(trail),'action':policy,'source_key_clause_j':j,
                      'source_key_occurrence_literal':l,'original_variable_x':x,
                      'old_mask':old,'global_assignment_mask':a,
                      'N0_N1_N2_N3':N.copy(),'clause_t':t.copy(),
                      'false_clause_indices':[jj for jj,u in enumerate(t) if u==0],
                      'source_clause_updates':delta})
    result={'policy':policy,'seed_mask':seed,'pure_literals_set_to_S':pure,
            'conflicting_original_variables':conflict,
            'terminus':'SAT_WITNESS' if N[0]==0 else 'UNKNOWN_NOT_UNSAT',
            'witness':a if N[0]==0 else None,'tried_global_states':len(trail),
            'trail':trail}
    if N[0]==0:
        assert is_sat(F,a)
        book['witness_verification_literal_reads']+=sum(map(len,F))
    return result

def unit_propagation(F,assignment,book,save_proof):
    vals=dict(assignment);step_log=[]
    while True:
        changed=False
        for j,C in enumerate(F):
            book['DPLL_source_clause_scans']+=1
            sat=False;remaining=[]
            for l in C:
                book['DPLL_literal_reads']+=1
                v=abs(l)
                if v not in vals:remaining.append(l)
                elif vals[v]==int(l>0):sat=True;break
            if sat:continue
            if len(remaining)==0:
                book['DPLL_conflict_leaves']+=1
                return vals,step_log,j
            if len(remaining)==1:
                lit=remaining[0];v=abs(lit);b=int(lit>0)
                assert v not in vals
                vals[v]=b;changed=True
                book['DPLL_unit_assignments']+=1
                if save_proof:step_log.append({'j':j,'v':v,'value':b})
                break
        if not changed:return vals,step_log,None

def dpll(F,book,proof=True):
    n=nvars(F);rec_calls=0
    def rec(partial):
        nonlocal rec_calls
        rec_calls+=1;book['DPLL_nodes']+=1
        vals,up,conflict=unit_propagation(F,partial,book,proof)
        if conflict is not None:
            return None,{'up':up,'conflict_clause':conflict}
        if len(vals)==n:
            witness=sum(vals.get(i,0)<<(i-1) for i in range(1,n+1))
            assert is_sat(F,witness)
            book['witness_verification_literal_reads']+=sum(map(len,F))
            return witness,{'up':up,'witness':witness}
        v=next(x for x in range(1,n+1) if x not in vals)
        children=[]
        for bit in (0,1):
            book['DPLL_branches']+=1
            nxt=dict(vals);nxt[v]=bit
            witness,node=rec(nxt)
            children.append({'value':bit,'proof':node})
            if witness is not None:return witness,{'up':up,'branch_var':v,'children':children}
        return None,{'up':up,'branch_var':v,'children':children}
    model,tree=rec({})
    return {'model':model,'SAT':model is not None,'nodes':rec_calls,
            'proof_tree':tree if proof else None}

def independent_replay_dpll(F,tree,vals,book):
    # An independent proof checker replaying recorded *original source* UP events.
    vals=dict(vals)
    for step in tree['up']:
        j=step['j'];v=step['v'];value=step['value'];C=F[j]
        assert v not in vals
        assert (v if value else -v) in C
        assert all(abs(l)==v or (abs(l) in vals and vals[abs(l)]!=int(l>0)) for l in C)
        vals[v]=value
        book['proof_replay_literal_reads']+=len(C)
    if 'conflict_clause' in tree:
        C=F[tree['conflict_clause']]
        assert all(abs(l) in vals and vals[abs(l)]!=int(l>0) for l in C)
        book['proof_replay_literal_reads']+=len(C)
        book['proof_checked_conflict_leaves']+=1
        return False
    if 'witness' in tree:
        a=tree['witness'];assert all(((a>>(v-1))&1)==b for v,b in vals.items())
        assert is_sat(F,a);book['proof_replay_literal_reads']+=sum(map(len,F))
        return True
    v=tree['branch_var'];assert v not in vals
    children=tree['children'];seen=[]
    for obj in children:
        child=dict(vals);child[v]=obj['value']
        seen.append((obj['value'],independent_replay_dpll(F,obj['proof'],child,book)))
        if seen[-1][1]:
            assert obj['value'] in (0,1)
            return True
    assert [b for b,_ in seen]==[0,1]
    assert all(not outcome for _,outcome in seen)
    return False

def exhaustive(F,book,do_full=True):
    n=nvars(F)
    if n>15 or not do_full:return None
    cnt=0;first=None;complement=0;endpoint_extremes=[]
    for a in range(1<<n):
        t,N=scores(F,a)
        if N[0]==0:
            cnt+=1
            if first is None:first=a
        ca=(1<<n)-1-a
        t2,_=scores(F,ca)
        assert all(t[j]+t2[j]==len(F[j]) for j in range(len(F)))
        book['exhaustive_global_assignments']+=1
        book['exhaustive_literal_reads']+=2*sum(map(len,F))
        complement+=1
    return {'global_assignment_checks':1<<n,'SAT_model_count':cnt,
            'first_model_mask':first,'complete_complement_checks':complement}

def trace_peak_workload(F,controller):
    """Peak Python allocator snapshot for exactly the chosen workload,
    exclusive of experimental full enumeration and JSON serialization.
    It is NOT a native Turing-machine space measure."""
    tracemalloc.start()
    b=collections.Counter()
    if controller:
        local=clause_extremes(F,b)
        pairs,_=pair_modes(F,b,verify=False)
        proofs=source_resolvents(F,b)
        pure,conflict=pure_vars(F,b)
        ends=[full_status(F,0),full_status(F,(1<<nvars(F))-1)]
        walks=[key_walk(F,seed,policy,b)
               for seed in (0,(1<<nvars(F))-1)
               for policy in ('SAT_KEY','FALSE_REPAIR')]
        model=next((w['witness'] for w in walks if w['witness'] is not None),None)
        if model is None:
            solve=dpll(F,b,proof=True)
            assert independent_replay_dpll(F,solve['proof_tree'],{},b)==solve['SAT']
            model=solve['model']
        if model is not None:assert is_sat(F,model)
    else:
        solve=dpll(F,b,proof=True)
        assert independent_replay_dpll(F,solve['proof_tree'],{},b)==solve['SAT']
    current,peak=tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak

def gather(F,name,exhaustive_mode=True):
    n=nvars(F);m=len(F)
    for C in F:assert len(set(map(abs,C)))==len(C)
    book=collections.Counter()
    t0=time.perf_counter()
    local=clause_extremes(F,book)
    pairs,hist=pair_modes(F,book,verify=True)
    resolvents=source_resolvents(F,book)
    pure,conflict=pure_vars(F,book)
    end0=full_status(F,0);end1=full_status(F,(1<<n)-1)
    book['endpoint_literal_reads']+=2*sum(map(len,F))
    proof_examples=[]
    for c in resolvents[:3]:
        R=c['non_tautological_resolvent'];cube={int(v):b for v,b in c['forbidden_partial_cube'].items()}
        # Verify that no complete source model extends the forbidden cube for n<=15.
        if n<=15:
            for a in range(1<<n):
                if all(((a>>(v-1))&1)==b for v,b in cube.items()):
                    assert not is_sat(F,a)
                    book['resolvent_cube_completed_checks']+=1
        proof_examples.append(c)
    ex=exhaustive(F,book,exhaustive_mode)
    walk_results=[]
    for seed in (0,(1<<n)-1):
        for policy in ('SAT_KEY','FALSE_REPAIR'):
            walk_results.append(key_walk(F,seed,policy,book))
    base=collections.Counter();base_t0=time.perf_counter()
    baseline=dpll(F,base,proof=True)
    baseline_time=time.perf_counter()-base_t0
    assert independent_replay_dpll(F,baseline['proof_tree'],{},base)==baseline['SAT']
    # Charge controller's own search and all failed routes, with verified
    # DPLL fallback only when all four attempted deterministic walks fail.
    controller_book=collections.Counter()
    controller_book.update(book)
    witness=next((w['witness'] for w in walk_results if w['witness'] is not None),None)
    if witness is None:
        controller_book['fallback_invocations']+=1
        solver=dpll(F,controller_book,proof=True)
        assert independent_replay_dpll(F,solver['proof_tree'],{},controller_book)==solver['SAT']
        witness=solver['model'];fallback_nodes=solver['nodes']
    else:
        controller_book['witness_verification_literal_reads']+=sum(map(len,F))
        assert is_sat(F,witness)
        fallback_nodes=0
    book['total_run_seconds_round_ms']=int((time.perf_counter()-t0)*1000)
    # Do not charge offline independent exhaustive oracle to the solver.
    offline_keys={'exhaustive_global_assignments','exhaustive_literal_reads',
                  'pair_bruteforce_assignments','resolvent_cube_completed_checks'}
    accounting_keys={'total_run_seconds_round_ms'}
    charge_keys=set(book)-offline_keys-accounting_keys
    audit_work=sum(book[k] for k in charge_keys)
    control_work=sum(controller_book[k] for k in charge_keys)+sum(v for k,v in controller_book.items() if k not in book and k not in offline_keys and k not in accounting_keys)
    baseline_work=sum(base.values())
    # Controller can solve via early walk; it need not rerun DPLL when witness found.
    assert witness is None or is_sat(F,witness)
    assert (witness is None)==(baseline['model'] is None)
    if ex:assert (ex['SAT_model_count']>0)==(witness is not None)
    baseline_traced_peak=trace_peak_workload(F,False)
    controller_traced_peak=trace_peak_workload(F,True)
    return {
      'name':name,'n':n,'m':m,'original_signed_clauses':[list(C) for C in F],
      'strict_2positive_2negative':strict22(F),
      'original_unsigned_scope_by_clause':[list(x) for x in incidence(F)],
      'all_signed_original_occurrences_local_S_U_and_inversions':local,
      'source_clause_pair_extreme_matrix':pairs,
      'pair_mode_signature_histogram':hist,
      'globally_coherent_endpoints':{'all_zero':end0,'all_one':end1},
      'nonconflicting_variables_pure_literal_assignments':pure,
      'conflicting_original_variable_ids':conflict,
      'source_parent_resolvent_count':len(resolvents),
      'sample_proved_forbidden_partial_cubes':proof_examples,
      'uniform_walks':walk_results,
      'independent_exhaustive_oracle':ex,
      'solver_compare':{'baseline':{'SAT':baseline['SAT'],'model_mask':baseline['model'],
                          'DPLL_nodes':baseline['nodes'],'selected_work_events':baseline_work,
                          'work_event_breakdown':dict(sorted(base.items())),
                          'elapsed_seconds':round(baseline_time,6),
                          'peak_python_tracemalloc_bytes':baseline_traced_peak,
                          'complete_DPLL_tree_original_source_checker_PASSED':True,
                          'formal_UNSAT_coverage':baseline['SAT'] is False,
                          'source_authenticated_DPLL_certificate':baseline['proof_tree'] if not baseline['SAT'] else None},
                        'four_walk_prepass_plus_fallback':{'SAT':witness is not None,
                           'model_mask':witness,'fallback_DPLL_nodes':fallback_nodes,
                           'selected_work_events':control_work,
                           'selected_analytic_audit_work_events':audit_work,
                           'peak_python_tracemalloc_bytes':controller_traced_peak,
                           'work_event_breakdown':dict(sorted(controller_book.items()))}},
      'elapsed_run_seconds':round(time.perf_counter()-t0,6)
    }

def check_matched(F,U):
    assert strict22(F) and strict22(U)
    assert incidence(F)==incidence(U)
    assert all(len([l for C in F for l in C if l==x])==2 for x in range(1,16))
    a=collections.Counter();b=collections.Counter()
    _,histF=pair_modes(F,a,verify=True);_,histU=pair_modes(U,b,verify=True)
    assert histF==histU
    for endpoint in (0,(1<<nvars(F))-1):
        assert scores(F,endpoint)[1]==scores(U,endpoint)[1]
    all0=scores(F,0)[1];all1=scores(F,(1<<nvars(F))-1)[1]
    assert all0[0]>0 and all1[0]>0
    model_F=[a for a in range(1<<15) if is_sat(F,a)]
    model_U=[a for a in range(1<<15) if is_sat(U,a)]
    assert len(model_F)==0 and len(model_U)>0
    assert model_U[0]==19186
    return {'original_W1_UNSAT':'exhaustive_32768_assignments',
            'matched_SAT_twin_witness_mask':model_U[0],
            'witness_true_variable_ids':[x for x in range(1,16) if (model_U[0]>>(x-1))&1],
            'two_signed_occurrences_flipped':[
                {'original_variable':6,'source_clause_j':9,'original_signed_literal':-6,'twin_signed_literal':6},
                {'original_variable':6,'source_clause_j':13,'original_signed_literal':6,'twin_signed_literal':-6}],
            'same_original_unsigned_clause_supports':True,
            'same_original_variable_2plus_2minus_counts':True,
            'all_variables_have_opposite_local_U_demands_in_both':True,
            'endpoint_histograms_identical':{'all_zero':all0,'all_one':all1},
            'aggregate_pairwise_signed_overlap_histograms_identical':histF,
            'indexed_full_pair_matrix_is_not_claimed_identical':True,
            'infinite_family':'disjoint r copies of W1 vs disjoint r copies of SWAP6 twin, for each integer r>=1; same diagnostics, opposite SAT status',
            'new_independent_checks':{'pair_assignment_enumerations':a['pair_bruteforce_assignments']+b['pair_bruteforce_assignments'],
                                        'formula_full_assignments_each':32768}}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--out',default='/mnt/data/lspv4_run43/LSPV4_CONFLICT_CONSENSUS_TWIN245_raw.json')
    parser.add_argument('--cases',nargs='*',default=None);args=parser.parse_args()
    F=get_cases(); names=args.cases or list(F)
    start=time.perf_counter();records=[]
    for name in names:
        case=gather(F[name],name)
        records.append(case)
        print(name,'strict22',case['strict_2positive_2negative'],
              'base nodes/work',case['solver_compare']['baseline']['DPLL_nodes'],case['solver_compare']['baseline']['selected_work_events'],
              'walk+fallback nodes/work',case['solver_compare']['four_walk_prepass_plus_fallback']['fallback_DPLL_nodes'],case['solver_compare']['four_walk_prepass_plus_fallback']['selected_work_events'],
              'witness',case['solver_compare']['four_walk_prepass_plus_fallback']['model_mask'],
              'seconds',case['elapsed_run_seconds'],flush=True)
    matched=check_matched(W1,TWIN)
    output={'run_id':'LSPV4_CONFLICT_CONSENSUS_TWIN245','seed':SEED,
            'epistemic_status':{'proved':'matched-family coarse-invariant nondecidability by explicit W1 UNSAT certificate and SWAP6 SAT witness','computational':'finite test and operation ledger','open':'general SAT'},
            'counting_conventions':'selected indexed-RAM-style events, not native CPU/TM steps; independent exhaustive oracle excluded from solver costs',
            'model':'one global original-variable assignment throughout; occurrence indices never independent variables',
            'matched_W1_unsat_vs_SAT_twin':matched,'cases':records}
    path=Path(args.out);path.parent.mkdir(parents=True,exist_ok=True)
    blob=json.dumps(output,indent=2,sort_keys=True).encode('utf-8')+b'\n';path.write_bytes(blob)
    print('RESULT_PATH',path,'BYTES',len(blob),'SHA256',hashlib.sha256(blob).hexdigest(),
          'TOTAL_SECONDS',round(time.perf_counter()-start,3))
if __name__=='__main__':main()
