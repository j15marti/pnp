#!/usr/bin/env python3
"""LSPV-4 COMPLEMENT-GRAY248. Self-contained, deterministic, source-indexed.

A complete exact experiment, not a proposed unrestricted fast SAT solver.
All costs are explicitly declared selected indexed word-RAM-like events.
"""
from __future__ import annotations
import hashlib, json, random, time
from collections import Counter, defaultdict
from itertools import combinations, product
from pathlib import Path
from typing import Iterable

RUN='LSPV4_COMPLEMENT_GRAY248'
SEED=202610300436
DEST=Path(__file__).resolve().parent
W1_STR='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
W1=[tuple(map(int,c.split())) for c in W1_STR.split(';')]
HBASE=[(1,3,5),(1,-3,6),(-1,4,5),(-1,-4,6),(2,3,-5),(2,-3,-6),(-2,4,-5),(-2,-4,-6)]

def H(r):
    out=[]
    for j in range(r):
        for k,c in enumerate(HBASE):
            out.append(tuple((1 if l>0 else -1)*(6*((j-1)%r if k==0 and z==0 else j)+abs(l)) for z,l in enumerate(c)))
    return out

def xor3(parity:int):
    return [tuple((i+1 if bit==0 else -(i+1)) for i,bit in enumerate(bits))
            for bits in product((0,1),repeat=3) if sum(bits)%2!=parity]

def tee_k4():
    edges={(0,1):1,(0,2):2,(0,3):3,(1,2):4,(1,3):5,(2,3):6}
    clauses=[]
    for v in range(4):
        incident=sorted(i for edge,i in edges.items() if v in edge)
        target=1 if v==0 else 0
        for bits in product((0,1),repeat=3):
            if sum(bits)%2!=target:
                clauses.append(tuple(i if b==0 else -i for i,b in zip(incident,bits)))
    return clauses

def padded_2cnf(clauses):
    # One fresh variable z per source 2-clause: two ternary clauses are equivalent to it.
    ans=[];fresh=max(abs(l) for c in clauses for l in c)
    for c in clauses:
        fresh+=1
        ans.append(tuple(c)+(fresh,));ans.append(tuple(c)+(-fresh,))
    return ans

def dense_planted(seed=SEED):
    rng=random.Random(seed);n=9;planted=(1<<n)//3;cs=set()
    while len(cs)<27:
        vars_=rng.sample(range(1,n+1),3)
        clause=tuple(v if rng.randrange(2) else -v for v in vars_)
        if any(lit_true(l,planted) for l in clause):cs.add(clause)
    return sorted(cs),planted

def lit_true(l:int,a:int)->bool:
    return bool((a>>(abs(l)-1))&1)==(l>0)

def clauses_truth(F,a):
    return [sum(lit_true(l,a) for l in c) for c in F]

def four(t):return [t.count(k) for k in range(4)]

def signed22(F,n):
    ct=Counter(l for c in F for l in c)
    return len(F)*3==4*n and all(ct[v]==ct[-v]==2 for v in range(1,n+1))

def validate(F,n):
    assert all(len(c)==3 and len({abs(l) for l in c})==3 for c in F)
    assert set(abs(l) for c in F for l in c)==set(range(1,n+1))
    assert len(set(F))==len(F)


def cases():
    wprime=[list(c) for c in W1]
    assert wprime[7][0]==1 and wprime[19][0]==-1
    wprime[7][0]=-1; wprime[19][0]=1
    p2s=padded_2cnf([(1,2),(-1,2)])
    p2u=padded_2cnf([(1,2),(-1,2),(1,-2),(-1,-2)])
    planted,pmodel=dense_planted()
    paired=[(1,2,3),(-1,4,5),(2,4,6),(3,5,6)]
    paired+= [tuple(-l for l in c) for c in paired]
    xor_sat=xor3(1)
    xor_unsat=xor3(0)+xor3(1)
    rename=H(2)
    rename=[tuple(-l if abs(l) in (1,4,7,10) else l for l in c) for c in rename]
    raw={
     'H1_strict22_SAT':(6,H(1)), 'H2_strict22_SAT':(12,H(2)),
     'H3_strict22_SAT':(18,H(3)), 'W1_strict22_UNSAT':(15,W1),
     'W1prime_strict22_SAT':(15,[tuple(c) for c in wprime]),
     'paired_K4_strict22_SAT':(6,paired),
     'H2_signed_rename_SAT':(12,rename),
     'Horn3_SAT':(4,[(-1,-2,3),(-1,-3,4),(-2,-3,4),(-1,-2,-4)]),
     '2SAT_padded_SAT':(4,p2s),'2SAT_padded_UNSAT':(6,p2u),
     'XOR3_SAT':(3,xor_sat),'XOR3_UNSAT':(3,xor_unsat),
     'K4_odd_Tseitin_UNSAT':(6,tee_k4()),
     'dense_planted_SAT':(9,planted),
    }
    return raw


def source_extremes(F,n):
    """Record each original signed occurrence four ways, four original-source pair modes."""
    targets=[]
    event_count=Counter();pair_modes=[]
    for j,C in enumerate(F):
        occ=[]
        for q,l in enumerate(C):
            S=int(l>0);U=1-S
            occ.append({'occurrence_id':f'x_{abs(l)},{j}','clause_index':j,'slot':q,
                        'signed_literal':l,'variable':abs(l),'S_local_all_TRUE':S,
                        'invert_S_to_U':1-S,'U_local_all_FALSE':U,'invert_U_to_S':1-U})
        targets.append({'source_j':j,'original_signed_lits':list(C),
                        'occurrences':occ,
                        'S_local_cube':{str(abs(l)):int(l>0) for l in C},
                        'U_local_cube':{str(abs(l)):int(l<0) for l in C},
                        'S_inverted_U':{str(abs(l)):int(l<0) for l in C},
                        'U_inverted_S':{str(abs(l)):int(l>0) for l in C}})
    for j,C in enumerate(F):
        jc={abs(l):(l>0) for l in C}
        for k in range(j+1,len(F)):
            D=F[k];kc={abs(l):(l>0) for l in D}
            share=set(jc)&set(kc)
            same=sorted(v for v in share if jc[v]==kc[v]);opp=sorted(v for v in share if jc[v]!=kc[v])
            mode={'SS':not opp,'SU':not same,'US':not same,'UU':not opp}
            event_count['pair_mode_tuples']+=4
            event_count['pair_sign_comparisons']+=len(share)
            event_count['pair_groundtruth_assignment_checks']+=1<<(6-len(share))
            if same:event_count['pair_same_nondefault']+=1
            if opp:event_count['pair_opposite_nondefault']+=1
            if same and opp:event_count['mixed_pair']+=1
            # Independent simultaneous full coherent enumeration over source union (max 6 variables).
            if n<=18:
                union=sorted(set(jc)|set(kc))
                found={z:False for z in mode}
                for a in range(1<<len(union)):
                    state=dict((v,(a>>q)&1) for q,v in enumerate(union))
                    u=sum(state[abs(l)]==int(l>0) for l in C)
                    v=sum(state[abs(l)]==int(l>0) for l in D)
                    for z,(cu,dv) in {'SS':(3,3),'SU':(3,0),'US':(0,3),'UU':(0,0)}.items():
                        if (u,v)==(cu,dv):found[z]=True
                assert found==mode,(j,k,found,mode)
            pair_modes.append({'clause_j':j,'clause_k':k,'same_shared_variables':same,
                               'opposite_shared_variables':opp,'SS':bool(mode['SS']),
                               'SU':bool(mode['SU']),'US':bool(mode['US']), 'UU':bool(mode['UU'])})
    return targets,pair_modes,dict(event_count)


def incidence(F,n):
    O=[[] for _ in range(n)]
    for j,C in enumerate(F):
        for l in C:O[abs(l)-1].append((j,l>0))
    return O


def endpoints(F,n):
    ans=[]
    for a in [0,(1<<n)-1]:
        t=clauses_truth(F,a)
        ans.append({'assignment_mask':a,'binary_x1_to_xn':''.join(str((a>>i)&1) for i in range(n)),
                    'per_original_clause_t':t,'N0_N1_N2_N3':four(t),
                    'SAT_clause_indices':[j for j,v in enumerate(t) if v>=1],
                    'UNSAT_clause_indices':[j for j,v in enumerate(t) if v==0]})
    return ans


def make_resolvents(F):
    candidates=[];seen=set();events=Counter()
    for j,C in enumerate(F):
        for k in range(j+1,len(F)):
            D=F[k];events['source_parent_pairs']+=1
            events['source_parent_pivot_literal_compares']+=9
            for lit in C:
                if -lit not in D:continue
                events['opposing_pivots']+=1
                A=set(C)-{lit};B=set(D)-{-lit};R=A|B
                events['candidate_lit_reads']+=len(C)+len(D)
                if any(-l in R for l in R):events['tautological']+=1;continue
                RR=tuple(sorted(R,key=lambda l:(abs(l),l<0)))
                if RR in seen:events['duplicate']+=1;continue
                seen.add(RR)
                forbidden={str(abs(l)):int(l<0) for l in RR}
                candidates.append({'parent_clause_indices':[j,k],'pivot_variable':abs(lit),
                                   'resolvent':RR,'forbidden_original_cube':forbidden,
                                   'length':len(RR)})
                events['non_taut_derived']+=1
    candidates.sort(key=lambda z:(z['length'],z['parent_clause_indices'],z['pivot_variable']))
    events['candidate_sort_conservative_comparisons']=len(candidates)*(len(candidates)-1).bit_length()
    return candidates,dict(events)


def verify_resolvent_pair(F,R):
    j,k=R['parent_clause_indices'];clauses=[F[j],F[k]]
    scope=sorted({abs(l) for C in clauses for l in C})
    for values in product([0,1],repeat=len(scope)):
        a=sum(v<<(u-1) for u,v in zip(scope,values))
        if all(any(lit_true(l,a) for l in C) for C in clauses):
            assert any(lit_true(l,a) for l in R['resolvent'])
    return True


def counter():return defaultdict(int)
def eval_clause(C,ass,counts):
    counts['clause_scans']+=1
    unassigned=[]
    for l in C:
        counts['literal_reads']+=1
        v=abs(l)
        if v in ass:
            if ass[v]==int(l>0):return 1,None
        else:unassigned.append(l)
    if not unassigned:return -1,None
    if len(unassigned)==1:return 0,unassigned[0]
    return 0,None

def dpll(F,n,additions=(),collect_proofs=False):
    # DPLL per visited node, UP repeat until stable, no free P=NP oracle.
    c=counter();proofs=[];clauses=list(F)+list(additions)
    c['source_initial_occurrence_reads']=3*len(F)
    c['added_clause_verify_lit_reads']=sum(len(z) for z in additions)
    def recurse(assignment,decisions):
        c['dpll_nodes']+=1
        ass=dict(assignment);forced=[]
        while True:
            changed=False;all_sat=True
            for C in clauses:
                status,lit=eval_clause(C,ass,c)
                if status==-1:
                    c['contradiction_leaves']+=1
                    if collect_proofs:proofs.append({'decisions':decisions,'forced':forced,'conflict':C})
                    return None
                if status==0:
                    all_sat=False
                    if lit is not None:
                        v=abs(lit);value=int(lit>0)
                        if v in ass:
                            assert ass[v]==value
                        else:
                            ass[v]=value;forced.append((v,value));c['UP_assignments']+=1
                            changed=True;break
            if not changed:break
        if all_sat:
            c['candidate_witness_found']+=1
            witness=sum(value<<(v-1) for v,value in ass.items())
            assert all(any(lit_true(l,witness) for l in C) for C in F)
            c['source_witness_verify_reads']+=sum(len(C) for C in F)
            return witness
        unassigned=next((v for v in range(1,n+1) if v not in ass),None)
        if unassigned is None:raise AssertionError('full assignment with neither SAT nor conflict')
        for val in (0,1):
            c['branch_actions']+=1
            ass2=dict(ass);ass2[unassigned]=val
            ans=recurse(ass2,decisions+[(unassigned,val)])
            if ans is not None:return ans
        return None
    w=recurse({},[])
    # UP replay each contradictory DPLL leaf with only its decisions and source clauses.
    if collect_proofs and w is None:
        for P in proofs:
            u={v:val for v,val in P['decisions']};c['proof_replay_decisions']+=len(u)
            while True:
                changed=False
                for C in clauses:
                    c['proof_replay_clause_reads']+=1
                    free=[];satisfied=False
                    for l in C:
                        c['proof_replay_literal_reads']+=1
                        if abs(l) not in u:free.append(l)
                        elif u[abs(l)]==int(l>0):satisfied=True;break
                    if satisfied:continue
                    if not free:
                        changed=None;break
                    if len(free)==1:
                        lit=free[0]
                        if abs(lit) in u:raise AssertionError('contradiction replay internal')
                        u[abs(lit)]=int(lit>0);c['proof_replay_UP_assignments']+=1
                        changed=True;break
                if changed is None:break
                if not changed:raise AssertionError('proof leaf not contradictory')
            c['proof_replay_conflicts']+=1
        assert c['proof_replay_conflicts']==c['contradiction_leaves']
    return {'result':'SAT' if w is not None else 'UNSAT', 'witness_mask':w,
            'nodes':c['dpll_nodes'],'leaves':c['contradiction_leaves'],
            'selected_solver_work_no_proof_replay':sum(v for k,v in c.items() if not k.startswith('proof_replay')),
            'selected_proof_replay_work':sum(v for k,v in c.items() if k.startswith('proof_replay')),
            'work_counts':dict(c),'proof_tree_leaves':proofs if collect_proofs else []}


def gray_complement_quotient(F,n,max_steps=None,full_trace=False):
    """Exhaustive if max_steps None; scans x_n=0 Gray cube, checks its global complement implicitly.
    All full assignments represented exactly once as orientation of an orbit.
    """
    allmask=(1<<n)-1; reps=(1<<(n-1));O=incidence(F,n)
    ct=counter();ct['source_initial_occurrence_reads']=3*len(F)
    ct['index_build_occurrences']=3*len(F)
    t=clauses_truth(F,0);counts=four(t)
    ct['initial_literal_reads']=3*len(F);ct['initial_category_build']=len(F)
    a=0;states=0;witness=None;trace=[];N0N3={};first_hit=None
    scans=reps if max_steps is None else min(max_steps,reps)
    if full_trace:trace.append({'mask':0,'flipped_global_variable':None,'t_per_original_clause':t[:],'N0123':counts[:],'N_complement':counts[::-1]})
    for i in range(scans):
        if i:
            q=(i&-i).bit_length()-1;v=q+1
            # standard BRGC i xor (i >> 1), step i changes bit ctz(i).
            assert a == ((i-1)^((i-1)>>1))
            newa=i^(i>>1)
            assert (newa^a)==(1<<q)
            a=newa;ct['global_variable_flips']+=1
            old_value=1-((a>>q)&1)
            for j,ispos in O[q]:
                old_t=t[j]
                was_true=(old_value==int(ispos))
                new_t=old_t+(-1 if was_true else 1)
                assert 0<=new_t<=3
                counts[old_t]-=1;counts[new_t]+=1;t[j]=new_t
                ct['affected_clause_truth_updates']+=1
                ct['histogram_bucket_updates']+=2
                ct['occurrence_index_lookups']+=1
            ct['flip_decisions']+=1
        assert sum(counts)==len(F)
        ct['two_orientation_status_tests']+=2
        states+=1
        if len(trace)<12 or (full_trace and len(trace)<100000):
            trace.append({'mask':a,'flipped_global_variable':None if i==0 else v,
                          't_per_original_clause':t[:],'N0123':counts[:],'N_complement':counts[::-1]})
        if counts[0]==0:
            witness=a;first_hit={'gray_rep_index':i,'orientation':'direct','mask':a,'N0123':counts[:]};break
        if counts[3]==0:
            witness=allmask^a;first_hit={'gray_rep_index':i,'orientation':'complement','mask':witness,'N0123':counts[::-1]};break
    if witness is not None:
        assert all(any(lit_true(l,witness) for l in C) for C in F)
        ct['source_witness_verify_reads']+=3*len(F)
    if witness is None and max_steps is None:
        # Entire quotient enumerated, every full assignment checked via exact complement identity.
        assert states==reps
    return {'result':'SAT' if witness is not None else ('UNSAT' if max_steps is None else 'UNRESOLVED'),
            'witness_mask':witness,'representatives_visited':states,'full_assignments_implicitly_covered':states*2,
            'all_orbits_exhausted':witness is None and max_steps is None,
            'first_hit':first_hit,'last_count':counts,'sampled_flip_trail':trace[:14],
            'selected_work':sum(ct.values()),'work_counts':dict(ct)}


def naive_full_scan(F,n):
    # Independent brute verifier, full source literal evaluations for each full assignment.
    m=len(F);count=0;models=0;first=None;calls=0
    for a in range(1<<n):
        tt=clauses_truth(F,a);calls+=3*m
        if all(t>0 for t in tt):
            models+=1
            if first is None:first=a
        count+=1
    return {'complete_assignments_checked':count,'full_literal_reads':calls,'models':models,'first_model':first}


def full_gray_for_unsat(F,n):
    # Unpaired full n-dimensional Gray traversal, for comparison; always visits full cube.
    O=incidence(F,n);t=clauses_truth(F,0);a=0;flips=0;touches=0
    for i in range(1,1<<n):
        q=(i&-i).bit_length()-1
        old_val=(a>>q)&1
        a=i^(i>>1)
        for j,ispos in O[q]:
            t[j]+=(-1 if old_val==int(ispos) else 1);touches+=1
        flips+=1
    assert t==clauses_truth(F,a)
    return {'full_gray_flips':flips,'affected_clause_updates':touches}


def certify_orbit_counts(F,n):
    # Independent exact check of the Gray quotient and corresponding complements, up to n=18.
    allmask=(1<<n)-1;reps=1<<(n-1);seen=set();distr=Counter();survival=Counter()
    for i in range(reps):
        a=i^(i>>1)
        b=a^allmask
        assert (a>>(n-1))==0
        assert (b>>(n-1))==1
        assert a not in seen and b not in seen
        seen.add(a);seen.add(b)
        p=four(clauses_truth(F,a));q=four(clauses_truth(F,b))
        assert p==q[::-1]
        if p[0]==0 and p[3]==0:survival['both_orientations_SAT']+=1
        elif p[0]==0:survival['only_representative_SAT']+=1
        elif p[3]==0:survival['only_complement_SAT']+=1
        else:survival['neither_SAT']+=1
        distr[str(tuple(p))]+=1
    assert len(seen)==1<<n
    return {'exhaustive_verified_full_assignments':len(seen),
            'orbit_histogram_distribution':dict(distr),
            'complement_pair_survival_counts':dict(survival)}


def check_triples(F,limit=9):
    # Independent multiple-clause target-consistency source checker, bounded subsample.
    checked=0
    m=len(F)
    triples=list(combinations(range(m),3))
    if len(triples)>limit:
        triples=[triples[(z*len(triples))//limit] for z in range(limit)]
    for idxs in triples:
        Cs=[F[j] for j in idxs];scope=sorted({abs(l) for C in Cs for l in C})
        for modes in product((0,1),repeat=3):
            demand={};feasible=True
            for C,mode in zip(Cs,modes):
                for l in C:
                    val=int(l>0) if mode else int(l<0)
                    if abs(l) in demand and demand[abs(l)]!=val:feasible=False
                    demand[abs(l)]=val
            brute=False
            for vals in product((0,1),repeat=len(scope)):
                state=dict(zip(scope,vals))
                if all(all(state[abs(l)]==(int(l>0) if mode else int(l<0)) for l in C)
                       for C,mode in zip(Cs,modes)):
                    brute=True;break
            assert brute==feasible
            checked+=1
    return checked


def run():
    results={};start=time.perf_counter();controls=cases()
    for name,(n,F) in controls.items():
        begin=time.perf_counter();validate(F,n)
        source_targets,pair_modes,pair_counts=source_extremes(F,n)
        triple_count=check_triples(F,limit=5)
        extremes=endpoints(F,n)
        resolvents,resolve_counts=make_resolvents(F)
        verified=0
        for R in resolvents[:15]:
            assert verify_resolvent_pair(F,R)
            verified+=1
        # DPLL complete and proof replay only on UNSAT; proof leaves kept.
        baseline=dpll(F,n,collect_proofs=True)
        # Fixed recipe: up to eight width<=3, by lexicographic certified parent index,
        # plus the full original source; this is an honest fixed nonsemantic policy.
        selected=resolvents[:8]
        derived=[R['resolvent'] for R in selected]
        with_resolvents=dpll(F,n,additions=derived,collect_proofs=True)
        q=gray_complement_quotient(F,n)
        oracle=naive_full_scan(F,n)
        # All-orbit check is external, charged only to audit not the solver.
        orbits=certify_orbit_counts(F,n)
        assert (oracle['models']>0)==(baseline['result']=='SAT')==(q['result']=='SAT')
        assert with_resolvents['result']==baseline['result']
        assert baseline['witness_mask'] is None or all(any(lit_true(l,baseline['witness_mask']) for l in C) for C in F)
        if n<=15 and name in ('W1_strict22_UNSAT','W1prime_strict22_SAT','H1_strict22_SAT'):
            # Check exact formula-wide complement t identity as well as per clause.
            assert all(four(clauses_truth(F,a))==four(clauses_truth(F,a^((1<<n)-1)))[::-1] for a in range(1<<n))
        fullgray=full_gray_for_unsat(F,n) if name in ('W1_strict22_UNSAT','XOR3_UNSAT','K4_odd_Tseitin_UNSAT','H1_strict22_SAT') else None
        # All-primary-audit diagnostics charge pair-mode output, occurrence, multi-clause, endpoints.
        audit_work=(3*len(F)*4 + sum(len(z['occurrences']) for z in source_targets)
                    + 4*len(pair_modes)+pair_counts['pair_sign_comparisons']
                    + 3*len(F)*2)
        res_acquisition=(resolve_counts['source_parent_pairs']+resolve_counts['candidate_lit_reads']
                        +resolve_counts.get('opposing_pivots',0)+resolve_counts.get('non_taut_derived',0)
                        +verified*6+resolve_counts.get('source_parent_pivot_literal_compares',0)
                        +resolve_counts.get('candidate_sort_conservative_comparisons',0))
        qfull=q['selected_work']+audit_work
        rs_work=with_resolvents['selected_solver_work_no_proof_replay']+audit_work+res_acquisition
        local=[{'original_clause_index':r['parent_clause_indices'],'pivot_variable':r['pivot_variable'],
                'derived_clause':r['resolvent'],'source_proof':'one opposite-signed pivot; RUP via parent contradictory units',
                'forbidden_cube':r['forbidden_original_cube']} for r in selected]
        results[name]={
          'source_n':n,'source_m':len(F),'strict22':signed22(F,n),'original_clauses':F,
          'local_S_U_targets_and_inverses':source_targets,'original_pair_four_mode_matrix':pair_modes,
          'pair_audit':pair_counts,'triple_extreme_checks':triple_count,
          'coherent_global_endpoints':extremes,
          'source_derived_forbidden_cubes':local,'firstgen_non_taut_resolvents':len(resolvents),
          'source_proof_parent_checks':verified,'source_resolvent_work':resolve_counts,
          'oracle_and_independent_verification_not_charged_as_solver':{
             'full_assignment_oracle_literal_visits':oracle['full_literal_reads'],
             'independent_quotient_double_source_literal_visits':3*len(F)*(1<<n),
             'pair_mode_brute_assignment_checks':pair_counts['pair_groundtruth_assignment_checks'],
             'triple_extreme_mode_checks':triple_count,
             'source_parent_resolvent_bruteforce_checks':verified},
          'baseline_UP_DPLL':baseline,'selected_resolvent_DPLL':with_resolvents,
          'quotient_Gray_exact':q,'naive_complete_assignment_scan_oracle':oracle,
          'independent_complement_orbit_checks':orbits,'full_gray_complete_cost_control':fullgray,
          'charged_audit_prepass_work':audit_work,
          'fully_charged_quotient_work':qfull,
          'fully_charged_resolution_DPLL_work_no_replay':rs_work,
          'fully_charged_resolution_DPLL_proof_replay':with_resolvents['selected_proof_replay_work'],
          'elapsed_seconds':round(time.perf_counter()-begin,4),
        }
        print(name, 'N',n,'m',len(F),'models',oracle['models'],'dpll_nodes',baseline['nodes'],
              'q_orbits',q['representatives_visited'],'qWork',qfull,'time',round(time.perf_counter()-begin,3),flush=True)
    records={'id':RUN,'date':'2026-10-30','seed':SEED,'evaluation_model':'selected indexed word-RAM-like events, not machine instructions',
             'all_trials_complete_exhaustive':True,'P_vs_NP':'OPEN',
             'theorem_scope':'explicit complement-pair enumeration on proper width-3 sources; strict22 constant-degree flip updates',
             'instances':results,'runtime_seconds':round(time.perf_counter()-start,3)}
    p=DEST/'LSPV4_COMPLEMENT_GRAY248_raw.json'
    b=(json.dumps(records,indent=2,sort_keys=True)+'\n').encode();p.write_bytes(b)
    digest=hashlib.sha256(b).hexdigest()
    succinct={name:{'n':R['source_n'],'m':R['source_m'],'SAT_models':R['naive_complete_assignment_scan_oracle']['models'],
       'dpll_nodes':R['baseline_UP_DPLL']['nodes'],'dpll_work':R['baseline_UP_DPLL']['selected_solver_work_no_proof_replay'],
       'dpll_proof_replay':R['baseline_UP_DPLL']['selected_proof_replay_work'],
       'selected_resolvent_nodes':R['selected_resolvent_DPLL']['nodes'],
       'selected_resolvent_work_full':R['fully_charged_resolution_DPLL_work_no_replay'],
       'orbit_gray_representatives_visited':R['quotient_Gray_exact']['representatives_visited'],
       'quotient_work_full':R['fully_charged_quotient_work'],
       'raw_naive_lit_reads':R['naive_complete_assignment_scan_oracle']['full_literal_reads'],
       'mixed_pairs':R['pair_audit'].get('mixed_pair',0),
       'pair_mode_groundtruth_full_assignments':R['pair_audit'].get('pair_groundtruth_assignment_checks',0),
       'complement_survival':R['independent_complement_orbit_checks']['complement_pair_survival_counts'],
       'dpll_leaves':R['baseline_UP_DPLL']['leaves'],
       'quotient_status':R['quotient_Gray_exact']['result'],
       'full_gray_updates':R['full_gray_complete_cost_control']['affected_clause_updates'] if R['full_gray_complete_cost_control'] else None}
       for name,R in results.items()}
    summary={'run':RUN,'raw_sha256':digest,'raw_bytes':len(b),'runtime_seconds':records['runtime_seconds'],
             'control_count':len(results),'replayed_UP_DPLL_UNSAT_leaves':sum(R['baseline_UP_DPLL']['leaves'] for R in results.values() if R['baseline_UP_DPLL']['result']=='UNSAT'),
             'pair_modes_checked':sum(R['pair_audit']['pair_mode_tuples'] for R in results.values()),
             'triple_modes_checked':sum(R['triple_extreme_checks'] for R in results.values()),
             'coherent_assignment_complement_checks':sum(R['independent_complement_orbit_checks']['exhaustive_verified_full_assignments'] for R in results.values()),
             'instances':succinct}
    (DEST/'LSPV4_COMPLEMENT_GRAY248_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print('FINAL',json.dumps({k:v for k,v in summary.items() if k!='instances'}),flush=True)

if __name__=='__main__':run()
