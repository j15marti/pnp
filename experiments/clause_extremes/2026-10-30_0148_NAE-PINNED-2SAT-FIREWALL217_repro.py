#!/usr/bin/env python3
"""Clause-indexed S/U audit plus exact pinned-NAE residual referee.

The new target is the claim that pinning a literal of a ternary NAE clause
creates a binary NAE/disequality edge.  It does not: it creates one ordinary
binary clause.  The script proves this by truth table, then exhaustively
checks the corrected hitting-set-to-2SAT reduction on every partial assignment
of every signed K4 paired class.  The full user-mandated occurrence audit and
fixed-order UP-DPLL accounting are imported from readback-verified run214.
"""
from __future__ import annotations
import hashlib, importlib.util, itertools, json, sys, time
from pathlib import Path

HERE=Path(__file__).resolve().parent
DEP=HERE/'2026-10-29_2248_EXTREME-COMPATIBILITY-FIREWALL214_repro.py'
OUT=HERE/'2026-10-30_0148_NAE-PINNED-2SAT-FIREWALL217_raw.json'
spec=importlib.util.spec_from_file_location('firewall214',DEP)
base=importlib.util.module_from_spec(spec);sys.modules[spec.name]=base;spec.loader.exec_module(base)

K4=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
H1=[(1,3,5),(1,-3,6),(-1,4,5),(-1,-4,6),
    (2,3,-5),(2,-3,-6),(-2,4,-5),(-2,-4,-6)]

def paired_formula(nv,edges,delta):
    bags=[[] for _ in range(nv)]
    for i,(u,v) in enumerate(edges,1):
        bags[u].append(i);bags[v].append(-i if (delta>>(i-1))&1 else i)
    out=[]
    for b in bags: out.extend((tuple(b),tuple(-x for x in b)))
    return out

def nae_ok(designated,a):
    return all(sum(base.lit_true(l,a) for l in c) in (1,2) for c in designated)

def partials(vs):
    for vals in itertools.product((-1,0,1),repeat=len(vs)):
        yield {v:x for v,x in zip(vs,vals) if x>=0}

def reduce_one_nae(clause,rho,source):
    pinned=[];free=[]
    for l in clause:
        if abs(l) in rho:pinned.append(int(base.lit_true(l,rho)))
        else:free.append(l)
    rec={'source_pair':source,'source_clause':list(clause),'pinned_truths':pinned,
         'free_literals':list(free)}
    if not pinned:return 'ternary',None,rec
    if 0 in pinned and 1 in pinned:return 'satisfied',None,rec
    color=pinned[0]
    if not free:return 'conflict',tuple(),rec
    # To avoid all literals having pinned color c, at least one free literal
    # must have truth 1-c.  In signed-literal notation this is a clause of the
    # free literals for c=0 and their complements for c=1.
    residual=tuple(free if color==0 else (-l for l in free))
    rec['residual_clause']=list(residual)
    return ('unit' if len(residual)==1 else 'binary'),residual,rec

def residual_2cnf(designated,rho):
    clauses=[];records=[];unhit=[]
    for p,c in enumerate(designated):
        kind,res,rec=reduce_one_nae(c,rho,p);records.append({'kind':kind,**rec})
        if kind=='ternary':unhit.append(p)
        elif kind in ('unit','binary','conflict'):clauses.append(res)
    return clauses,records,unhit

def naive_disequality_residual(designated,rho):
    clauses=[]
    for p,c in enumerate(designated):
        kind,res,rec=reduce_one_nae(c,rho,p)
        if kind=='ternary':return None
        if kind in ('unit','conflict'):clauses.append(res)
        elif kind=='binary':
            clauses.append(res)
            # Incorrect step under audit: add the opposite binary clause too,
            # thereby replacing one forbidden color-pair by disequality.
            clauses.append(tuple(-l for l in res))
    return clauses

def solve_2sat(clauses):
    if any(len(c)==0 for c in clauses):
        return False,{'reason':'empty residual clause','implication_edges':0,'dfs_visits':0}
    vs=sorted({abs(l) for c in clauses for l in c}); idx={}
    for h,v in enumerate(vs):idx[v]=2*h;idx[-v]=2*h+1
    n=2*len(vs);g=[[] for _ in range(n)];rg=[[] for _ in range(n)];edges=0
    def add(a,b):
        nonlocal edges;g[idx[a]].append(idx[b]);rg[idx[b]].append(idx[a]);edges+=1
    for c in clauses:
        if len(c)==1:add(-c[0],c[0])
        else:
            a,b=c;add(-a,b);add(-b,a)
    seen=[False]*n;order=[];visits=0
    def dfs(u):
        nonlocal visits;seen[u]=True;visits+=1
        for v in g[u]:
            if not seen[v]:dfs(v)
        order.append(u)
    for u in range(n):
        if not seen[u]:dfs(u)
    comp=[-1]*n
    def rdfs(u,k):
        nonlocal visits;comp[u]=k;visits+=1
        for v in rg[u]:
            if comp[v]<0:rdfs(v,k)
    k=0
    for u in reversed(order):
        if comp[u]<0:rdfs(u,k);k+=1
    bad=[v for v in vs if comp[idx[v]]==comp[idx[-v]]]
    return (not bad),{'reason':'opposite literals in one SCC' if bad else 'satisfiable SCC',
                      'contradictory_variables':bad,'implication_edges':edges,
                      'dfs_visits':visits,'components':k}

def exact_extension(designated,vs,rho):
    free=[v for v in vs if v not in rho];checks=0
    for bits in itertools.product((0,1),repeat=len(free)):
        a=dict(rho);a.update(zip(free,bits));checks+=1
        if nae_ok(designated,a):return True,a,checks
    return False,None,checks

def k4_partial_audit():
    totals={'sign_classes':0,'hitting_partials':0,'extendible':0,'inextendible':0,
            'exact_extensions_checked':0,'two_sat_edges':0,'two_sat_dfs_visits':0,
            'naive_false_rejections':0,'naive_false_acceptances':0}
    first_false_reject=None;first_prohibited=None;first_scc_prohibited=None;first_pure_binary=None;by_pins={}
    for delta in range(64):
        form=paired_formula(4,K4,delta);designated=form[::2];vs=base.vars_of(form)
        totals['sign_classes']+=1
        for rho in partials(vs):
            clauses,records,unhit=residual_2cnf(designated,rho)
            if unhit:continue
            totals['hitting_partials']+=1
            exact,witness,checks=exact_extension(designated,vs,rho)
            totals['exact_extensions_checked']+=checks
            sat,cert=solve_2sat(clauses)
            assert sat==exact
            totals['two_sat_edges']+=cert['implication_edges'];totals['two_sat_dfs_visits']+=cert['dfs_visits']
            totals['extendible' if exact else 'inextendible']+=1
            k=str(len(rho));by_pins.setdefault(k,{'total':0,'extendible':0,'inextendible':0})
            by_pins[k]['total']+=1;by_pins[k]['extendible' if exact else 'inextendible']+=1
            naive,_=solve_2sat(naive_disequality_residual(designated,rho))
            if naive!=exact:
                totals['naive_false_rejections' if exact else 'naive_false_acceptances']+=1
                if exact and first_false_reject is None:
                    first_false_reject={'delta':delta,'partial':rho,'correct_residual':[list(c) for c in clauses],
                        'naive_residual':[list(c) for c in naive_disequality_residual(designated,rho)],
                        'exact_witness':witness,'source_records':records}
            if not exact and first_prohibited is None:
                first_prohibited={'delta':delta,'prohibited_partial_cube':rho,
                    'derived_2cnf':[list(c) for c in clauses],'source_records':records,
                    'certificate':cert,'external_extension_checks':checks}
            if not exact and cert.get('contradictory_variables') and first_scc_prohibited is None:
                first_scc_prohibited={'delta':delta,'prohibited_partial_cube':rho,
                    'derived_2cnf':[list(c) for c in clauses],'source_records':records,
                    'certificate':cert,'external_extension_checks':checks}
            if (not exact and clauses and all(len(c)==2 for c in clauses)
                    and first_pure_binary is None):
                first_pure_binary={'delta':delta,'prohibited_partial_cube':rho,
                    'derived_2cnf':[list(c) for c in clauses],'source_records':records,
                    'certificate':cert,'external_extension_checks':checks}
    assert totals['naive_false_rejections']>0 and totals['naive_false_acceptances']==0
    return {'totals':totals,'by_pinned_variable_count':by_pins,
            'first_naive_false_rejection':first_false_reject,
            'first_prohibited_cube':first_prohibited,
            'first_nontrivial_SCC_prohibited_cube':first_scc_prohibited,
            'first_pure_binary_SCC_prohibited_cube':first_pure_binary}

def minimal_truth_table():
    # D=(x,y,z), pin literal x false.  Correct residual is y OR z; the
    # incorrect disequality y!=z rejects 11 and accepts 00.
    rows=[]
    for y,z in itertools.product((0,1),repeat=2):
        correct=(y or z);naive=(y!=z)
        rows.append({'x':0,'y':y,'z':z,'NAE_xyz':bool(correct),
                     'correct_y_OR_z':bool(correct),'incorrect_y_NE_z':bool(naive)})
    assert any(r['NAE_xyz']!=r['incorrect_y_NE_z'] for r in rows)
    return rows

def main():
    t0=time.perf_counter();partial=k4_partial_audit()
    controls={
      'minimal_paired_clause':[(1,2,3),(-1,-2,-3)],
      'paired_K4_balanced':paired_formula(4,K4,0),
      'paired_K4_unbalanced':paired_formula(4,K4,1),
      'endpoint_plateau_H1':H1,
      'xor3_sat':base.parity3(0),
      'xor3_unsat':base.parity3(0)+base.parity3(1),
      'contradictory_padded_units':base.padded_unit(1,2,3)+base.padded_unit(-1,4,5),
      'horn_sat':[(-1,-2,3),(-3,-4,5),(-5,-1,-4),(-2,-4,-6)],
      'strict22_n6_sat':base.strict22(6),
      'planted_dense_sat':base.planted_dense(),
      'all_signs_3var_unsat':[tuple((i+1) if bits[i]==0 else -(i+1) for i in range(3)) for bits in itertools.product((0,1),repeat=3)]}
    reports=[base.audit_formula(n,c) for n,c in controls.items()]
    checks={k:sum(r['checks'][k] for r in reports) for k in reports[0]['checks']}
    out={'run_id':'NAE-PINNED-2SAT-FIREWALL217','timestamp':'2026-10-30T01:48:00-07:00',
      'dependency':{'path':DEP.name,'sha256':hashlib.sha256(DEP.read_bytes()).hexdigest()},
      'status':['PROVED/EXACT: a partial assignment hitting every designated NAE-3 clause yields an exact 2CNF residual',
                'FALSIFIED/RETIRED: pinning one literal turns a ternary NAE clause into a binary NAE/disequality edge',
                'COMPUTATIONAL exhaustive K4 sign/partial controls','P versus NP OPEN'],
      'minimal_truth_table':minimal_truth_table(),'k4_partial_audit':partial,
      'benchmarks':reports,'benchmark_checks':checks,'elapsed_seconds':time.perf_counter()-t0,
      'limitations':['The 2SAT shortcut requires a supplied or discovered hitting partial assignment.',
        'Enumerating all assignments to a large hitting set can be exponential.',
        'The fixed-order UP-DPLL comparison is not industrial CDCL.',
        'No arbitrary exact22 or general SAT bound follows.']}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'output':str(OUT),'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),
      'elapsed_seconds':out['elapsed_seconds'],'k4':partial['totals'],'benchmark_checks':checks},indent=2))

if __name__=='__main__':main()
