#!/usr/bin/env python3
"""Bounded, seeded finite checks; no minimum proof-degree or asymptotic experiments.
Run: timeout 30s python audit_universal22.py --stage local --out ../results/local.json
Stages are deliberately separate; each cooperatively stops within 25 seconds.
"""
from __future__ import annotations
import argparse,hashlib,itertools,json,random,time
from collections import Counter
from pathlib import Path
import universal22 as u

START=time.monotonic(); COUNTS=Counter(); SEED=20261013

def check(ok:bool,group:str):
    if time.monotonic()-START>25: raise TimeoutError('Cooperative 25-second budget: split work.')
    COUNTS[group]+=1
    if not ok: raise AssertionError(f'{group}: {COUNTS[group]}')

def projection_check(comp:u.Compiled):
    check(comp.n==9*(len(comp.source)+7*comp.padding_gadgets),'size_formula')
    check(len(comp.clauses)==12*(len(comp.source)+7*comp.padding_gadgets),'size_formula')
    check(comp.padding_gadgets<=9*len(comp.source),'linear_blowup')
    check(u.check_proper(comp.clauses)==comp.n,'proper_target')
    occ=Counter(l for c in comp.clauses for l in c)
    check(all(occ[x]==occ[-x]==2 for x in range(1,comp.n+1)),'exact_22')
    for c,(kind,j) in zip(comp.clauses,comp.kinds):
        got=u.subst(u.clause_poly(c),comp.projection)
        if kind=='source': expected=u.clause_poly(comp.source[j])
        elif kind=='implication' and j<=comp.source_n: expected={(j,):1,(j,j):-1}
        else: expected={}
        check(got==expected,'formal_integer_axiom_projection')

def local():
    out={}
    for lit in (1,-1):
        gadget=u.pad7(lit,2); occ=Counter(l for c in gadget for l in c)
        check(occ[lit]==1 and occ[-lit]==0,'single_external_occurrence')
        check(all(occ[x]==occ[-x]==2 for x in range(2,7)),'gadget_aux_balance')
        rows=[]
        for bit in (0,1):
            vals={x:0 for x in range(2,7)}|{1:bit}
            check(u.eval_cnf(gadget,vals),'zero_extension')
            rows.append(sum(u.eval_cnf(gadget,{1:bit}|dict(zip(range(2,7),bs)))
                            for bs in itertools.product((0,1),repeat=5)))
        out[str(lit)]={'models_for_x0_x1':rows}
        for c in gadget:
            image=u.subst(u.clause_poly(c),{1:1}|{x:0 for x in range(2,7)})
            check(image=={},'padding_polynomial_zero')
    models=0;deleted=[False]*20
    for bs in itertools.product((0,1),repeat=15):
        vals=dict(enumerate(bs,1)); violations=[i for i,c in enumerate(u.W1) if not u.eval_cnf([c],vals)]
        check(bool(violations),'W1_unsat')
        if len(violations)==1: deleted[violations[0]]=True
        if u.eval_cnf(u.Q,vals):
            models+=1;check(all(vals[p]==0 for p in u.PORTS),'Q_ports')
    check(all(deleted),'W1_all_clause_deletions_have_witness')
    check(models==244,'Q_model_fingerprint')
    # Colouring encoding: prod(1-x_i) = -(sum x_i - 1)+sum pairs - triple.
    p=u.clause_poly((1,2,3));rhs={():1,(1,):-1,(2,):-1,(3,):-1,
                               (1,2):1,(1,3):1,(2,3):1,(1,2,3):-1}
    check(p==rhs,'colouring_axiom_adapter')
    for prime in (2,3,5,7,11):
        check(u.reduced_mod(p,prime)==u.reduced_mod(rhs,prime),'all_tested_fields')
        # PCR padded clause: x*xbar = x*(x+xbar-1) - (x*x-x).
        r=u.add(u.mul({(1,):1},{(1,):1,(2,):1,():-1}),{(1,1):1,(1,):-1},-1)
        check(u.reduced_mod(r,prime)=={(1,2):1},'PCR_padding_derivation')
    out['Q_models']=models
    return out

def cnfs():
    rng=random.Random(SEED); cases={
      'single_positive_clause':[(1,2,3)],
      'single_negative_clause':[(-1,-2,-3)],
      'cube_unsat':[tuple((i+1)*(1 if bs[i]==0 else -1) for i in range(3))
                    for bs in itertools.product((0,1),repeat=3)],
      'Horn':[(1,-2,-3),(-1,2,-3),(-1,-2,3)],
      'independent_product':[(1,2,3),(4,5,6)],
      'balanced_W1':u.W1}
    for n in (3,4,5,6):
        pool=[tuple(x*s for x,s in zip(vs,ss)) for vs in itertools.combinations(range(1,n+1),3)
              for ss in itertools.product((-1,1),repeat=3)]
        for j in range(4):
            cs=rng.sample(pool,min(len(pool),2*n+j))
            if set(abs(x) for c in cs for x in c)==set(range(1,n+1)): cases[f'seeded_n{n}_{j}']=cs
    rows=[]
    for name,source in cases.items():
        comp=u.compile22(source); projection_check(comp)
        n=comp.source_n; sat_count=0
        if n<=6:
            for bs in itertools.product((0,1),repeat=n):
                vals=dict(enumerate(bs,1));truth=u.eval_cnf(source,vals);sat_count+=truth
                check(u.eval_cnf(comp.clauses,u.lift(comp,vals))==truth,'all_assignments_zero_lift')
            # Actual sign switching and permutation, not just encoding tags.
            perm=list(range(1,n+1));rng.shuffle(perm);phases=[rng.choice((-1,1)) for _ in range(n)]
            switched=[tuple(perm[abs(l)-1]*phases[abs(l)-1]*(1 if l>0 else -1) for l in c) for c in source]
            other=u.compile22(switched);projection_check(other)
            count2=sum(u.eval_cnf(switched,dict(enumerate(bs,1))) for bs in itertools.product((0,1),repeat=n))
            check(count2==sat_count,'real_renaming_and_phase_control')
        else:sat_count=None
        rows.append({'case':name,'source_n':n,'source_m':len(source),'source_models':sat_count,
          'g':comp.padding_gadgets,'target_n':comp.n,'target_m':len(comp.clauses)})
    return {'cases':rows,'number_cases':len(rows)}

def graphs():
    cases={'triangle':(3,[(0,1),(1,2),(0,2)]),
      'K4':(4,list(itertools.combinations(range(4),2))),
      'K3_3':(6,[(i,j) for i in range(3) for j in range(3,6)]),
      'odd_wheel':(6,[(0,i) for i in range(1,6)]+[(i,1+i%5) for i in range(1,6)]),
      'path':(5,[(i,i+1) for i in range(4)]),
      'K7_degree6':(7,list(itertools.combinations(range(7),2)))}
    rows=[]
    for name,(nv,es) in cases.items():
        cnf=u.colouring_cnf(nv,es);proper,pmap=u.properize23(cnf);comp=u.compile22(proper)
        projection_check(comp)
        check(len(proper)==7*nv+6*len(es),'graph_proper_counts')
        check(comp.padding_gadgets==15*nv+18*len(es),'graph_padding_counts')
        check(comp.n==1008*nv+1188*len(es),'graph_target_counts')
        check(len(comp.clauses)==1344*nv+1584*len(es),'graph_target_counts')
        # Restrict all properization variables to zero and recover original axioms.
        fromcollections=Counter()
        for c in proper:
            pp=u.subst(u.clause_poly(c),pmap)
            if pp:fromcollections[tuple(sorted(pp.items()))]+=1
        expected=Counter(tuple(sorted(u.clause_poly(c).items())) for c in cnf)
        check(fromcollections==expected,'binary_properization_projection')
        num=0;witness=None
        for colours in itertools.product(range(3),repeat=nv):
            truth=all(colours[a]!=colours[b] for a,b in es)
            vals={3*v+k+1:int(colours[v]==k) for v in range(nv) for k in range(3)}
            check(u.eval_cnf(cnf,vals)==truth,'colouring_CNF_semantics')
            if truth:num+=1;witness=vals
        if witness:
            pv={x:witness[y] if y else 0 for x,y in pmap.items()}
            check(u.eval_cnf(comp.clauses,u.lift(comp,pv)),'colouring_target_witness')
        rows.append({'graph':name,'vertices':nv,'edges':len(es),'colourings':num,
                     'proper_m':len(proper),'g':comp.padding_gadgets,
                     'target_n':comp.n,'target_m':len(comp.clauses),
                     'asymptotic_hardness_certified':False})
    return {'cases':rows,'note':'Small graphs validate reductions only. K7 is not a sparse-random theorem instance.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--stage',choices=['local','cnfs','graphs'],required=True)
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
    result={'run_id':'PC22_ALLFIELD1','stage':args.stage,'seed':SEED,'status':'RUNNING'}
    try:
        result['data']=globals()[args.stage]()
        result.update(status='COMPUTATIONAL',all_checks_passed=True)
    except Exception as exc:
        result.update(status='FAILED_TEST',all_checks_passed=False,error=repr(exc));raise
    finally:
        result.update(assertions=sum(COUNTS.values()),checks_by_group=dict(COUNTS),
                      elapsed_seconds=time.monotonic()-START,
                      code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                      compiler_sha256=hashlib.sha256(Path(u.__file__).read_bytes()).hexdigest())
        args.out.parent.mkdir(parents=True,exist_ok=True);args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['stage','all_checks_passed','assertions','elapsed_seconds']}))
