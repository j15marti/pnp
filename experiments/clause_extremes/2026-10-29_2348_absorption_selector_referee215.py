#!/usr/bin/env python3
"""Source-resolvent absorption selector with full clause-extreme controls.

Depends only on the previous readback-verified run214 stdlib reproducer in the
same directory.  Exact enumeration is confined to small formulas / local unions.
"""
from __future__ import annotations
import hashlib, importlib.util, itertools, json, statistics, sys, time, tracemalloc
from pathlib import Path

HERE=Path(__file__).resolve().parent
BASE=HERE/'2026-10-29_2248_EXTREME-COMPATIBILITY-FIREWALL214_repro.py'
spec=importlib.util.spec_from_file_location('firewall214',BASE)
b=importlib.util.module_from_spec(spec); sys.modules[spec.name]=b; spec.loader.exec_module(b)
OUT=HERE/'2026-10-29_2348_ABSORPTION-SELECTOR-REFEREE215_raw.json'
SEED=202610292348

W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
S15='-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14'
def parse(s): return [tuple(map(int,x.split())) for x in s.split(';')]

BENCH={
 'W1_strict22_unsat':parse(W1), 'S15_strict22_sat':parse(S15),
 'diamond_post_UP_sat':[(1,2,3),(1,-2,4)],
 'duplicate_mixed_sat':[(1,2,3)]*4+[(1,2,-3)]*4,
 'xor3_sat':b.parity3(1), 'xor3_contradictory_unsat':b.parity3(0)+b.parity3(1),
 'dense_xor_K6_sat':b.dense_overlapping_xor(6),
 'padded_units_unsat':b.padded_unit(1,2,3)+b.padded_unit(-1,4,5),
 'horn_sat':[(-1,-2,3),(-3,-4,5),(-5,-1,-4),(-2,-4,-6)],
 'strict22_n6_sat':b.strict22(6), 'planted_dense_sat':b.planted_dense(),
}

def sign_map(c): return {abs(x):x>0 for x in c}

def resolve_pair(c,d):
    sc,sd=sign_map(c),sign_map(d); shared=set(sc)&set(sd)
    opp=sorted(v for v in shared if sc[v]!=sd[v])
    same=sorted(v for v in shared if sc[v]==sd[v])
    if len(opp)!=1: return None, same, opp
    p=opp[0]; lp=next(x for x in c if abs(x)==p)
    tail=[x for x in c if abs(x)!=p]+[x for x in d if abs(x)!=p]
    if any(-x in tail for x in tail): return None,same,opp
    R=tuple(sorted(set(tail),key=lambda x:(abs(x),x<0)))
    return R,same,opp

def counter_units(c):
    return c.nodes+c.branches+c.clause_scans+c.literal_reads+c.propagations+c.conflicts+c.extreme_guard_pair_checks

def up_probe(F, initial, target_lit=None):
    c=b.Counters(); a=dict(initial); ok=b.unit_propagate(F,a,c)
    inferred=False
    if not ok: inferred=True
    elif target_lit is not None and abs(target_lit) in a:
        inferred=(a[abs(target_lit)]==int(target_lit>0))
    return inferred,c,a,not ok

def absorption(F,R):
    probes=[]; total=0
    for target in R:
        initial={abs(l):int(l<0) for l in R if l!=target}
        inferred,c,a,conflict=up_probe(F,initial,target)
        total+=counter_units(c)
        probes.append({'target_literal':target,'falsified_other_literals':initial,
                       'conflict':conflict,'target_inferred':inferred and not conflict,
                       'absorbed_at_target':inferred,'work_units':counter_units(c),
                       'closure':a})
    return all(p['absorbed_at_target'] for p in probes),probes,total

def candidates(F):
    recs=[]; pair_tests=0; lit_ops=0
    for j,k in itertools.combinations(range(len(F)),2):
        pair_tests+=9
        R,same,opp=resolve_pair(F[j],F[k])
        if R is None: continue
        lit_ops+=4
        pa,pp,pw=absorption([F[j],F[k]],R)
        fa,fp,fw=absorption(F,R)
        recs.append({'parents':[j,k],'same_shared':same,'opposite_shared':opp,
                     's':len(same),'o':len(opp),'resolvent':list(R),'width':len(R),
                     'parent_absorbed':pa,'parent_absorption_probes':pp,
                     'parent_absorption_work':pw,'full_formula_absorbed':fa,
                     'full_absorption_probes':fp,'full_absorption_work':fw,
                     'local_selector_keep':len(same)>=1,'full_selector_keep':not fa,
                     'prohibited_cube':{str(abs(l)):int(l<0) for l in R}})
    return recs,{'pair_literal_tests':pair_tests,'candidate_literal_ops':lit_ops,
                 'full_absorption_work':sum(x['full_absorption_work'] for x in recs)}

def primary_audit(name,F):
    vs=b.vars_of(F); assigns=list(b.enumerate_assignments(vs)); checks={'pair':0,'triple':0,'complement':0,'cube':0}
    local=[b.local_clause_record(j,c) for j,c in enumerate(F)]
    pairs=[]
    for j,k in itertools.combinations(range(len(F)),2):
        p=b.pair_matrix(j,F[j],k,F[k]); u=sorted(set(map(abs,F[j]+F[k])))
        checks['pair']+=b.exact_pair_verify(F[j],F[k],p['matrix'],u); pairs.append(p)
    triples=[]
    for js in itertools.combinations(range(min(8,len(F))),3):
        u=sorted({abs(l) for j in js for l in F[j]})
        for modes in itertools.product('SU',repeat=3):
            _,conf=b.merge_demands([(f'C{j}:{m}',b.demands(F[j],m)) for j,m in zip(js,modes)])
            found=None
            for a in b.enumerate_assignments(u):
                checks['triple']+=1
                if all(b.clause_vector(F[j],a)==((1,1,1) if m=='S' else (0,0,0)) for j,m in zip(js,modes)):
                    found=a;break
            assert (found is not None)==(not conf)
            triples.append({'source_clause_indices':list(js),'modes':''.join(modes),'feasible':not conf,'witness':found})
    zero={v:0 for v in vs}; one={v:1 for v in vs}
    trails=[]
    for label,start,order in [('0_to_1',zero,vs),('1_to_0',one,list(reversed(vs)))]:
        a=dict(start); steps=[]
        for step,v in enumerate([None]+order):
            if v is not None:a[v]^=1
            steps.append({'step':step,'flip':v,'assignment':''.join(str(a[x]) for x in vs),**b.status(F,a)})
        trails.append({'name':label,'steps':steps})
    models=[]
    for a in assigns:
        st=b.status(F,a); comp={v:1-a[v] for v in vs}; sc=b.status(F,comp)
        assert sc['true_literal_counts']==[3-x for x in st['true_literal_counts']]
        checks['complement']+=len(F)
        if st['formula_sat']:models.append(a)
    recs,prep=candidates(F)
    for r in recs:
        j,k=r['parents']; u=sorted(set(map(abs,F[j]+F[k])))
        for a in b.enumerate_assignments(u):
            if b.extends_cube(a,r['prohibited_cube']):
                checks['cube']+=1
                assert not (sum(b.clause_vector(F[j],a)) and sum(b.clause_vector(F[k],a)))
    return {'name':name,'variables':vs,'source_clauses':[list(x) for x in F],
            'local_clause_extremes':local,'pair_matrix':pairs,'bounded_triple_modes':triples,
            'global_endpoints':{'0^n':b.status(F,zero),'1^n':b.status(F,one)},
            'flip_trails':trails,'is_sat':bool(models),'model_count':len(models),
            'first_model':models[0] if models else None,'resolvent_candidates':recs,
            'preprocessing':prep,'checks':checks}

def solve_measured(F,derived,prework):
    clauses=F+[tuple(r) for r in derived if tuple(r) not in F]
    times=[]; peak=0; last=None
    for _ in range(5):
        tracemalloc.start(); t=time.perf_counter_ns(); last=b.dpll(clauses,False); times.append((time.perf_counter_ns()-t)/1000)
        _,p=tracemalloc.get_traced_memory();tracemalloc.stop();peak=max(peak,p)
    model,c=last
    return {'model':model,'counters':b.asdict(c),'solver_work':counter_units(c),
            'preprocess_work':prework,'total_work':counter_units(c)+prework,
            'derived_count':len(clauses)-len(F),'derived_literal_storage':sum(len(r) for r in derived),
            'peak_assignment_cells':c.peak_assigned,'tracemalloc_peak_bytes_5':peak,
            'median_us_5':statistics.median(times)}

def add_solver_comparison(rep):
    F=[tuple(x) for x in rep['source_clauses']]; recs=rep['resolvent_candidates']; prep=rep['preprocessing']
    uniq_all={tuple(r['resolvent']) for r in recs}
    uniq_local={tuple(r['resolvent']) for r in recs if r['local_selector_keep']}
    uniq_full={tuple(r['resolvent']) for r in recs if r['full_selector_keep']}
    structural=prep['pair_literal_tests']+prep['candidate_literal_ops']
    rep['solver_comparison']={
      'baseline':solve_measured(F,[],0),
      'all_direct_resolvents':solve_measured(F,sorted(uniq_all),structural),
      'local_same_overlap_selector':solve_measured(F,sorted(uniq_local),structural),
      'full_nonabsorbed_selector':solve_measured(F,sorted(uniq_full),structural+prep['full_absorption_work'])}
    truth=rep['is_sat']
    assert all((x['model'] is not None)==truth for x in rep['solver_comparison'].values())

def main():
    t=time.perf_counter(); reports=[]
    for name,F in BENCH.items():
        r=primary_audit(name,[tuple(x) for x in F]); add_solver_comparison(r); reports.append(r)
    candidate_count=sum(len(r['resolvent_candidates']) for r in reports)
    theorem_checks=0
    for r in reports:
        for x in r['resolvent_candidates']:
            theorem_checks+=1
            assert x['parent_absorbed']==(x['s']==0)
    totals={k:sum(r['checks'][k] for r in reports) for k in reports[0]['checks']}
    totals['parent_absorption_theorem']=theorem_checks
    out={'run_id':'ABSORPTION-SELECTOR-REFEREE215','timestamp':'2026-10-29T23:48:00-07:00','seed':SEED,
         'dependency':{'path':BASE.name,'sha256':hashlib.sha256(BASE.read_bytes()).hexdigest()},
         'status':['PROVED/EXACT parent-pair absorption theorem','COMPUTATIONAL finite controls','P versus NP OPEN'],
         'theorem':'For two proper 3-clause parents with exactly one opposite shared pivot and s same-polarity shared tail variables, their direct resolvent is absorbed by the two-parent formula iff s=0.',
         'candidate_count':candidate_count,'total_checks':totals,'elapsed_seconds':time.perf_counter()-t,
         'limitations':['finite solver comparisons are not industrial CDCL or machine lower bounds','full-formula absorption probes are charged','first-generation direct source resolvents only','exact enumeration only on small controls'],
         'benchmarks':reports}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'output':str(OUT),'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),
                      'elapsed_seconds':out['elapsed_seconds'],'candidate_count':candidate_count,'checks':totals},indent=2))

if __name__=='__main__':main()
