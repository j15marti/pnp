#!/usr/bin/env python3
"""Independent checker for GUARDED-AFFINE-CYCLE263 data. No producer import.
Checks original source clause index/signs, complete paired resolutions, XOR-row
semantics, guarded dependency, mixed UNSAT derivations and exact assignments.
"""
import json,sys,copy
from itertools import product
from collections import Counter

CHECKS=Counter()
def req(q,kind):
    CHECKS[kind]+=1
    if not q:raise AssertionError(f'failed {kind}')

def normalize(c):return tuple(sorted(set(c),key=lambda v:(abs(v),v)))
def resolve(a,b,p):
    req(p in a and -p in b,'legal_resolution_pivot')
    c=normalize([v for v in a if v!=p]+[v for v in b if v!=-p])
    req(not any(-v in c for v in c),'no_tautology')
    return c

def clause_sat(c,assignment):return any(assignment[abs(v)]==int(v>0) for v in c)
def model(F,assignment):return all(clause_sat(c,assignment) for c in F)

def check_row(F,row):
    req(len(row['parents'])==4,'four_source_pairs')
    g=row['guard'];vs=tuple(row['variables'])
    req(len(set(vs))==3 and abs(g) not in vs,'proper_guarded_triple')
    wrong=[]
    for a,b in row['parents']:
        ca,cb=F[a],F[b]
        shared={abs(l) for l in ca}&{abs(l) for l in cb}
        cands=[v for v in shared if (v in ca and -v in cb) or (-v in ca and v in cb)]
        req(len(cands)==1,'private_pivot_found')
        v=cands[0];p=v if v in ca else -v
        deriv=resolve(ca,cb,p)
        req(len(deriv)==4 and g in deriv,'source_clause_guard_present')
        triple=[lit for lit in deriv if lit!=g]
        req({abs(l) for l in triple}==set(vs),'correct_triple_support')
        bad={abs(l):int(l<0) for l in triple}
        wrong.append(tuple(bad[v] for v in vs))
    req(len(set(wrong))==4,'four_distinct_bad_assignments')
    req(all((sum(b)%2)!=row['rhs'] for b in wrong),'parity_row_sound')
    req(set(wrong)=={t for t in product((0,1),repeat=3) if sum(t)%2!=row['rhs']},'parity_row_complete')
    # independently validate 16 guard+payload assignments of the four resolvents
    for gv in (0,1):
        for bits in product((0,1),repeat=3):
            a=dict(zip(vs,bits));a[abs(g)]=gv
            active=(gv!=int(g>0))
            formula_res= (not active) or (sum(bits)%2==row['rhs'])
            literal_value = all((gv==int(g>0)) or (tuple(bits)!=wrong_i) for wrong_i in wrong)
            req(formula_res==literal_value,'guarded_truth_table')

def check_blocker(F,rows,blocker):
    if blocker is None:return
    ids=blocker['row_ids'];req(bool(ids),'nonempty_dependency')
    req(all(0<=i<len(rows) for i in ids),'valid_row_ids')
    lhs=set();rhs=0
    guards=set()
    for idx in ids:
        row=rows[idx]
        for v in row['variables']:
            if v in lhs:lhs.remove(v)
            else:lhs.add(v)
        rhs ^=row['rhs'];guards.add(row['guard'])
    req(not lhs and rhs==1,'linear_dependency_0_equals_1')
    req(not any(-g in guards for g in guards),'guard_coherence')
    req(set(blocker['clause'])==guards,'correct_exported_guard_blocker')
    # Adding the blocker is source preserving, since its falsification activates
    # the contradictory set of already authenticated original-source equations.
    for g in guards:
        req(any(row['guard']==g for row in rows),'guard_provenance')

def check_certificate(F,rows,blocker,cert):
    if cert is None:return
    req(blocker is not None,'mixed_proof_has_blocker')
    req(cert['proof_system']=='source_resolution_plus_guarded_GF2','typed_proof_system')
    guardset=set(blocker['clause'])
    req(len(cert['source_guard_forces'])==len(guardset),'full_guard_coverage')
    for unit in cert['source_guard_forces']:
        lit=unit['literal'];req(-lit in guardset,'opposite_guard_forcing')
        aa,bb,cc,dd=[F[j] for j in unit['source_ids']]
        v1,v2,u=unit['pivots']
        first=resolve(aa,bb,v1)
        second=resolve(cc,dd,v2)
        third=resolve(first,second,u)
        req([list(first),list(second),list(third)]==unit['resolved_intermediate'],'replayed_forcing_DAG')
        req(third==(lit,),'valid_derived_guard_unit')
    current=normalize(blocker['clause'])
    for step in cert['from_blocker_to_empty']:
        req(set(step['prior'])==set(current),'current_source_clause')
        req(step['pivot'] in current and step['unit']==-step['pivot'],'legal_guard_refutation')
        current=resolve(current,(step['unit'],),step['pivot'])
        req(set(current)==set(step['result']),'guard_refutation_replay')
    req(current==(), 'empty_refutation_endpoint')

def check_extremes(F,data):
    n=max(abs(l) for c in F for l in c)
    proper=[(i,c) for i,c in enumerate(F) if len(c)==3 and len({abs(l) for l in c})==3]
    expected=sum((len(c) for _,c in proper),0)
    req(len(data['original_occurrence_targets'])==expected,'original_occurrence_count')
    for e in data['original_occurrence_targets']:
        j,k=e['clause'],e['occurrence'];l=F[j][k]
        req(e['signed_literal']==l and e['variable']==abs(l),'signed_occurrence_match')
        req((e['S'],e['invert_S'],e['U'],e['invert_U'])==(int(l>0),int(l<0),int(l<0),int(l>0)),'extreme_targets_inversions')
    pair_counts=0
    for row in data['clause_pair_extreme_matrix']:
        j,k=row['j'],row['k'];a={abs(l):int(l>0) for l in F[j]};b={abs(l):int(l>0) for l in F[k]}
        same=any(a[v]==b[v] for v in a.keys()&b.keys())
        opp=any(a[v]!=b[v] for v in a.keys()&b.keys())
        req((row['SS'],row['SU'],row['US'],row['UU'])==(not opp,not same,not same,not opp),'four_mode_compatibility')
        pair_counts+=1
    req(pair_counts==len(proper)*(len(proper)-1)//2,'pair_cardinality')
    def state_check(s):
        bits=s['bits'];req(len(bits)==n,'state_width')
        a={v:int(bits[v-1]) for v in range(1,n+1)}
        t=[sum(a[abs(l)]==int(l>0) for l in c) for c in F]
        req(t==s['true_literal_counts'],'source_state_true_counts')
        three=[t[j] for j,c in enumerate(F) if len(c)==3]
        req(s['N0_to_N3']==[three.count(r) for r in range(4)],'N0_N3_correct')
        req(s['SAT']==all(x>0 for x in t),'source_state_sat')
        return a,t
    for key in ('global_0','global_1','complement_of_last_flip'):state_check(data[key])
    for s in data['flips']:state_check(s)
    req(set(data['global_0']['bits'])=={'0'} and set(data['global_1']['bits'])=={'1'},'globally_coherent_endpoints')
    a,b=data['flips'][-1],data['complement_of_last_flip']
    req(all(int(x)+int(y)==1 for x,y in zip(a['bits'],b['bits'])),'correct_complement')
    for j,c in proper:
        req(a['true_literal_counts'][j]+b['true_literal_counts'][j]==3,'clause_complement_identity')

def brute_label(F):
    n=max(abs(v) for c in F for v in c)
    for bits in product((0,1),repeat=n):
        a={i+1:v for i,v in enumerate(bits)}
        CHECKS['enumerated_coherent_assignments']+=1
        if model(F,a):return True
    return False

def check_all(path):
    with open(path) as f:dat=json.load(f)
    totals=Counter()
    for name,case in dat['cases'].items():
        F=[tuple(c) for c in case['F']]
        rows=case['source_rows'];b=case['blocker']
        for row in rows:check_row(F,row)
        check_blocker(F,rows,b)
        check_certificate(F,rows,b,case['certified_mixed_UNSAT'])
        check_extremes(F,case['original_extremes'])
        baseline=case['baseline_sat_assignment'];hybrid=case['hybrid_sat_assignment']
        req((baseline is None)==(hybrid is None),'both_policies_same_label')
        for witness in (baseline,hybrid):
            if witness is None:continue
            a={int(k):int(v) for k,v in witness.items()}
            req(model(F,a),'fully_checked_original_source_witness')
        if baseline is None:
            if case['certified_mixed_UNSAT'] is None:
                req(max(abs(l) for c in F for l in c)<=15,'finite_exhaustion_scope')
                req(not brute_label(F),'independent_source_unsat_exhaustion')
        if name=='missing_source_parent':
            req(len(rows)<4 and b is None,'incomplete_block_rejected')
        if name=='opposed_guard_tautology':
            req(b is None,'opposed_guards_cannot_refute')
            req(bool(case['rejected_dependencies']),'tautological_dependency_rejected')
        totals['cases']+=1
        totals['sat']+=baseline is not None
        totals['unsat']+=baseline is None
        totals['certified_UNSAT']+=case['certified_mixed_UNSAT'] is not None
        totals['authenticated_rows']+=len(rows)
        totals['blockers']+=b is not None
        totals['fourmode_checks']+=4*len(case['original_extremes']['clause_pair_extreme_matrix'])
        req(case['baseline_selected_work']>0 and case['hybrid_selected_work']>0,'actual_work_charged')
    # Negative controls must be rejected by the independent checker, rather
    # than merely observed to produce a different solver answer.
    victim=next(c for c in dat['cases'].values() if c['blocker'] is not None and c['certified_mixed_UNSAT'] is not None)
    Fv=[tuple(c) for c in victim['F']]
    def must_reject(fn):
        try:fn()
        except AssertionError:
            CHECKS['corrupt_certificate_rejected']+=1
            return
        raise AssertionError('corrupt proof was silently accepted')
    bad=copy.deepcopy(victim['source_rows'][0]);bad['rhs']^=1
    must_reject(lambda:check_row(Fv,bad))
    bad=copy.deepcopy(victim['source_rows'][0]);bad['guard']=-bad['guard']
    must_reject(lambda:check_row(Fv,bad))
    bad=copy.deepcopy(victim['blocker']);bad['clause'][0]=-bad['clause'][0]
    must_reject(lambda:check_blocker(Fv,victim['source_rows'],bad))
    bad=copy.deepcopy(victim['certified_mixed_UNSAT']);bad['source_guard_forces'][0]['source_ids'][0]=0
    must_reject(lambda:check_certificate(Fv,victim['source_rows'],victim['blocker'],bad))
    req(totals['cases']==dat['summary']['cases'],'aggregate_case_count')
    req(totals['sat']==dat['summary']['SAT'] and totals['unsat']==dat['summary']['UNSAT'],'aggregate_labels')
    return dict(checks=sum(CHECKS.values()),counters=dict(CHECKS),totals=dict(totals),result='PASS')

if __name__=='__main__':
    inp=sys.argv[1] if len(sys.argv)>1 else 'guarded_affine263_raw.json'
    ans=check_all(inp)
    with open(sys.argv[2] if len(sys.argv)>2 else 'independent_check263.json','w') as f:json.dump(ans,f,indent=2,sort_keys=True)
    print(json.dumps(ans,indent=2,sort_keys=True))