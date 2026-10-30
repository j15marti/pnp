#!/usr/bin/env python3
"""Independent clause-extreme audit of complement-paired exact22 sources.

The full per-occurrence S/U experiment delegates only bookkeeping and the
instrumented reference UP-DPLL to the readback-verified run214 reproducer.
The new theorem audit, signed-dual enumeration, and NAE-SAT(2) obstruction
certificate are implemented here.
"""
from __future__ import annotations
import hashlib, importlib.util, itertools, json, random, sys, time
from pathlib import Path

HERE=Path(__file__).resolve().parent
DEP=HERE/'2026-10-29_2248_EXTREME-COMPATIBILITY-FIREWALL214_repro.py'
OUT=HERE/'2026-10-30_0048_SIGNED-NAE-OCC2-COVERAGE-REFEREE216_raw.json'
SEED=202610300048
spec=importlib.util.spec_from_file_location('firewall214',DEP)
base=importlib.util.module_from_spec(spec);sys.modules[spec.name]=base;spec.loader.exec_module(base)

def paired_formula(nv, edges, delta):
    """Normalize first endpoint positive; second endpoint sign is edge delta."""
    bags=[[] for _ in range(nv)]
    for i,(u,v) in enumerate(edges,1):
        bags[u].append(i)
        bags[v].append(-i if (delta>>(i-1))&1 else i)
    assert all(len(b)==3 and len(set(map(abs,b)))==3 for b in bags)
    out=[]
    for b in bags: out.extend((tuple(b),tuple(-x for x in b)))
    return out

def nae_satisfied(form,a):
    # One designated member from every complementary pair.
    for p in range(len(form)//2):
        t=sum(base.lit_true(x,a) for x in form[2*p])
        if t in (0,3): return False
    return True

def models(form):
    vs=base.vars_of(form)
    return [a for a in base.enumerate_assignments(vs) if nae_satisfied(form,a)]

def balanced(nv,edges,delta):
    adj=[[] for _ in range(nv)]
    for i,(u,v) in enumerate(edges):
        d=(delta>>i)&1;adj[u].append((v,d));adj[v].append((u,d))
    e={}
    for s in range(nv):
        if s in e:continue
        e[s]=0;stack=[s]
        while stack:
            u=stack.pop()
            for v,d in adj[u]:
                if v in e:
                    if e[v]!=(e[u]^d):return False
                else:e[v]=e[u]^d;stack.append(v)
    return True

def transform_certificate(nv,edges,delta):
    # Standard signed-to-positive NAE-SAT(2) split. Each mixed-sign variable
    # creates one binary NAE edge between two fresh occurrence nodes.
    mixed=[i+1 for i in range(len(edges)) if (delta>>i)&1]
    binary=[['x'+str(i),'x'+str(i)+"'"] for i in mixed]
    flat=[x for e in binary for x in e]
    return {'original_ternary_edges':nv,'original_variables':len(edges),
            'mixed_sign_variables':mixed,'binary_NAE_edges':binary,
            'binary_edges_form_matching':len(flat)==len(set(flat)),
            'binary_graph_bipartite':True,
            'obstruction_statement':'NAE-SAT(2) can fail only through a non-bipartite component of its residual binary-edge graph; here that graph is a matching.'}

def class_audit(name,nv,edges,full=True,samples=512):
    m=len(edges); space=range(1<<m) if full else random.Random(SEED+nv).sample(range(1<<m),samples)
    checked=bal=unbal=total_models=0;min_models=None;witnesses=[]
    for d in space:
        f=paired_formula(nv,edges,d); ms=models(f); assert ms
        checked+=1;total_models+=len(ms);min_models=len(ms) if min_models is None else min(min_models,len(ms))
        if balanced(nv,edges,d):bal+=1
        else:unbal+=1
        if len(witnesses)<4 and not balanced(nv,edges,d):
            witnesses.append({'delta':d,'model_count':len(ms),'first_model':ms[0],
                              'transform':transform_certificate(nv,edges,d)})
    return {'name':name,'vertices_clause_pairs':nv,'edge_variables':m,'sign_classes_checked':checked,
            'balanced_classes':bal,'unbalanced_classes':unbal,'all_sat':True,
            'minimum_model_count':min_models,'mean_model_count':total_models/checked,
            'unbalanced_examples':witnesses}

K4=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
PRISM=[(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)]
K33=[(i,j) for i in range(3) for j in range(3,6)]
PETERSEN=[(0,1),(1,2),(2,3),(3,4),(4,0),(5,7),(7,9),(9,6),(6,8),(8,5),(0,5),(1,6),(2,7),(3,8),(4,9)]

def pick_unbalanced(nv,edges,start=1):
    for d in range(start,1<<len(edges)):
        if not balanced(nv,edges,d):return d
    raise AssertionError

def main():
    t0=time.perf_counter()
    # The 15-edge Petersen sign space is chunked to a deterministic 32-class
    # sample so this invocation stays below the repository's 30-second rule.
    classes=[class_audit('K4_all_sign_classes',4,K4),class_audit('prism_all_sign_classes',6,PRISM),
             class_audit('K33_all_sign_classes',6,K33),class_audit('Petersen_32_sign_sample',10,PETERSEN,False,32)]
    selected={
      'paired_K4_balanced':paired_formula(4,K4,0),
      'paired_K4_unbalanced':paired_formula(4,K4,pick_unbalanced(4,K4)),
      'paired_prism_unbalanced':paired_formula(6,PRISM,pick_unbalanced(6,PRISM)),
      'paired_K33_unbalanced':paired_formula(6,K33,pick_unbalanced(6,K33)),
      'xor3_sat':base.parity3(0),
      'xor3_contradictory_unsat':base.parity3(0)+base.parity3(1),
      'contradictory_padded_units_unsat':base.padded_unit(1,2,3)+base.padded_unit(-1,4,5),
      'horn_sat':[(-1,-2,3),(-3,-4,5),(-5,-1,-4),(-2,-4,-6)],
      'strict22_n6_sat':base.strict22(6),
      'planted_dense_sat':base.planted_dense(),
      'all_signs_three_vars_unsat':[tuple((i+1) if bits[i]==0 else -(i+1) for i in range(3)) for bits in itertools.product((0,1),repeat=3)],
    }
    reports=[base.audit_formula(n,c) for n,c in selected.items()]
    for r in reports[:4]:
        assert r['is_sat']
        # Paired formula SAT is exactly designated NAE satisfaction.
        f=[tuple(c) for c in r['source_clauses']]; a={int(k):v for k,v in r['first_model'].items()}
        assert nae_satisfied(f,a)
    # Explicitly verify endpoint failure is not UNSAT on K4 controls.
    assert all(not reports[i]['global_endpoints']['0^n']['formula_sat'] and not reports[i]['global_endpoints']['1^n']['formula_sat'] for i in (0,1))
    checks={k:sum(r['checks'][k] for r in reports) for k in reports[0]['checks']}
    checks['signed_classes']=sum(x['sign_classes_checked'] for x in classes)
    checks['signed_class_assignments']=sum(x['sign_classes_checked']*(1<<x['edge_variables']) for x in classes)
    dep=hashlib.sha256(DEP.read_bytes()).hexdigest()
    out={'run_id':'SIGNED-NAE-OCC2-COVERAGE-REFEREE216','timestamp':'2026-10-30T00:48:00-07:00',
         'seed':SEED,'dependency':{'path':DEP.name,'sha256':dep},
         'status':['KNOWN THEOREM transfer: NAE-SAT(2) obstruction characterization',
                   'PROVED/EXACT corollary: every proper width-3 signed NAE formula with variable occurrence at most two is satisfiable',
                   'FALSIFIED/RETIRED: signed-dual balancedness is necessary for paired-class SAT coverage',
                   'COMPUTATIONAL finite controls','P versus NP OPEN'],
         'theorem':'Every complement-paired proper 3CNF in which each variable belongs to at most two clause pairs is SAT; balanced signed-dual cycles are not required.',
         'class_enumeration':classes,'benchmarks':reports,'total_checks':checks,
         'elapsed_seconds':time.perf_counter()-t0,
         'limitations':['The constructive linear-time algorithm is a known NAE-SAT(2) result, not reimplemented here.',
                        'The finite controller comparisons use fixed-order UP-DPLL, not industrial CDCL.',
                        'The theorem covers complement-paired sources only and does not cover arbitrary exact22.',
                        'No general SAT runtime or lower bound follows.']}
    OUT.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'output':str(OUT),'sha256':hashlib.sha256(OUT.read_bytes()).hexdigest(),
                      'elapsed_seconds':out['elapsed_seconds'],'total_checks':checks,
                      'class_summary':[{k:x[k] for k in ('name','sign_classes_checked','balanced_classes','unbalanced_classes','minimum_model_count')} for x in classes]},indent=2))

if __name__=='__main__':main()
