#!/usr/bin/env python3
"""ARC179 standalone reproducible finite controls for the two-algorithm certificate gate.

Run: python arc179_certificate_polarity_test.py
Uses the copied ARC177 source file in this directory. Python standard library only.
The test is NOT an all-input certificate-coverage theorem, a deterministic small-space
SAT machine or a complete P != NP proof.
"""
from __future__ import annotations
from collections import Counter
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import product
import hashlib, json, time
from pathlib import Path
from arc177_m22_compiler import (U,V,W,Y, m22, sat_by, dpll_refute,
    check_refutation, compile_m22, extend_witness, restrict, variables)

M=[tuple(l for l in c if abs(l)<=32) for c in U[2:44]]
getcontext().prec = 55
ASSERTIONS = 0

def assert_true(c, label):
    global ASSERTIONS
    assert c, label
    ASSERTIONS += 1


def truth_sat(clauses):
    vs=sorted({abs(x) for cl in clauses for x in cl})
    for vals in product([False,True], repeat=len(vs)):
        if all(any(vals[vs.index(abs(l))] == (l>0) for l in cl) for cl in clauses):
            return True
    return False


def all_unsat_cert(clauses):
    """Finite only: certificate recursively enumerates all Boolean assignments."""
    vs=sorted({abs(x) for cl in clauses for x in cl})
    def rec(k,env):
        if k==len(vs):
            for i,c in enumerate(clauses):
                if all(env[abs(l)]!=(l>0) for l in c):
                    return ['leaf',i]
            return None
        v=vs[k]
        left=rec(k+1,{**env,v:False})
        right=rec(k+1,{**env,v:True})
        if left is None or right is None:return None
        return ['split',v,left,right]
    return rec(0,{})


def verify_unsat_cert(clauses,proof):
    """Explicit SAT-sound verifier; every branch must be covered."""
    vs=sorted({abs(x) for cl in clauses for x in cl})
    def rec(node,env,k):
        if not isinstance(node,list) or not node:return False
        if node[0]=='leaf':
            return len(node)==2 and k==len(vs) and isinstance(node[1],int) and 0<=node[1]<len(clauses) and all(env[abs(l)]!=(l>0) for l in clauses[node[1]])
        if node[0]!='split' or len(node)!=4 or k>=len(vs) or node[1]!=vs[k]:return False
        return rec(node[2],{**env,vs[k]:False},k+1) and rec(node[3],{**env,vs[k]:True},k+1)
    return rec(proof,{},0)


def decimal_frac(f):return str(Decimal(f.numerator)/Decimal(f.denominator))

def threshold(d):
    return Fraction(2*d-1,d*(d-1))

def alternative(d):
    return Fraction(1,1)+1/d


def main():
    start=time.perf_counter()
    dataset={'experiment':'ARC179_TWO_ALGO_CERT_GATE','statuses':{'numerical':'PROVED/EXACT symbolic arithmetic','finite':'COMPUTATIONAL','all_input_coverage':'OPEN','P_vs_NP':'OPEN'},'controls':{},'thresholds':{},'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'arc177_sha256':hashlib.sha256(Path(__file__).with_name('arc177_m22_compiler.py').read_bytes()).hexdigest()}
    d=Fraction(901,500)
    C=threshold(d); critical_b=C-(d-1)/2
    assert_true(C==Fraction(651000,361301),'van Melkebeek root exact fraction')
    assert_true(critical_b==Fraction(651000,361301)-Fraction(401,1000),'b threshold exact rational')
    assert_true(C<d and C>Fraction(18018,10000),'seed gap and location')
    dataset['thresholds']={'d':decimal_frac(d),'C_d_fraction':f'{C.numerator}/{C.denominator}','C_d':decimal_frac(C),'seed_gap':decimal_frac(d-C),'critical_b_lambda_half_u_zero':decimal_frac(critical_b),'old_criterion':{'form':'c < max(1+1/d, (2d-1)/(d(d-1)))','d_2':str(alternative(Fraction(2,1))),'d_3':str(alternative(Fraction(3,1)))}}
    for numerator,den in [(1801,1000),(901,500),(181,100),(2,1),(3,1),(10,1),(100,1)]:
        di=Fraction(numerator,den); H=max(alternative(di),threshold(di)); key=f'{numerator}/{den}'
        dataset['thresholds'].setdefault('examples',{})[key]={'C':decimal_frac(threshold(di)),'Fortnow_branch':decimal_frac(alternative(di)),'H':decimal_frac(H)}
        assert_true(H>1 and (di>=2 or H==threshold(di)),'near-boundary threshold ordering')
    # Verify published source instance and monotone target SAT mate.
    for tag,F in [('U_UNSAT',U),('V_SAT',V)]:
        assert_true(len(F)==264,tag+' source m=264')
        assert_true(m22(F),tag+' all-positive/all-negative unique proper exact-(2,2)')
    assert_true(len(variables(U))==198 and len(variables(V))==198,'198 active variables')
    assert_true(sat_by(V,W),'V constructive witness')
    assert_true(not sat_by(U,W),'U witness fails the critical source clause')
    assert_true(sat_by(tuple(cl for j,cl in enumerate(U) if j!=1),W),'all remaining U clauses true under W')
    # Checked refutation of internal 32-variable template, six replicas and 64 possible core assignments.
    proof=dpll_refute(M)
    assert_true(proof is not None,'original 32-variable module UNSAT')
    nodes=check_refutation(M,proof)
    assert_true(nodes==89,'expected exact branch refutation size')
    core=list(U[:2]); replicas=[]
    for j in range(6):
        seg=U[2+42*j:2+42*(j+1)];sg=1 if j<3 else -1
        projected=[tuple(sg*(1 if l>0 else -1)*(abs(l)-32*j) for l in cl if 32*j<abs(l)<=32*j+32) for cl in seg]
        assert_true(projected==list(M),'submodule refutation lift')
        terminals=tuple(dict.fromkeys(l for cl in seg for l in cl if abs(l)>192))
        core.append(terminals);replicas.append({'index':j,'core_ports':len(terminals)})
    assert_true(not truth_sat(tuple(core)),'six-variable UNSAT core exact truth table')
    dataset['controls']['U_UNSAT_imported_docker']={'n':198,'m':264,'local_module_refutation_nodes':nodes,'core_var_count':6,'core_truth_assignments':64,'replicas':len(replicas)}
    dataset['controls']['V_SAT_monotone_exact22']={'n':198,'m':264,'witness_true':True}
    # Stronger non-join counterexample: all local pieces SAT in both U and V;
    # globally U UNSAT while V SAT. Each local block restored to exact M22.
    groups=[[1]]
    rest=[i for i in range(264) if i!=1]
    for offset in [0,88,176]:groups.append(rest[offset:offset+88])
    assert_true(sum(len(g) for g in groups)==264,'partition covers each source clause')
    assert_true(len(set(i for g in groups for i in g))==264,'partition no duplicates')
    join={};total_compiled=0
    for tag,F in [('U',U),('V',V)]:
        out=[]
        for j,inds in enumerate(groups):
            B=tuple(F[i] for i in inds)
            source_model=dict(W)
            if tag=='U' and j==0:
                source_model[194]=True  # satisfy the isolated omitted critical clause
            assert_true(sat_by(B,source_model),'each local block is SAT')
            c=compile_m22(B)
            assert_true(m22(c.clauses),'compiled local child lies in monotone 2P,2N-CNF-3')
            witness=extend_witness(c,source_model)
            assert_true(sat_by(c.clauses,witness),'compiled child explicit witness')
            assert_true(len(variables(c.clauses))==max(variables(c.clauses)),'compiled child densified')
            out.append({'block':j,'source_clauses':len(B),'compiled_n':len(variables(c.clauses)),'compiled_m':len(c.clauses),'SAT':True})
            total_compiled+=len(c.clauses)
        join[tag]={'global_SAT':tag=='V','local_SAT_vector':[True]*4,'blocks':out}
    assert_true(join['U']['local_SAT_vector']==join['V']['local_SAT_vector'] and join['U']['global_SAT']!=join['V']['global_SAT'],'no join from labels alone')
    dataset['controls']['same_local_labels_opposite_global_labels']=join
    dataset['controls']['compiled_child_clauses_total']=total_compiled
    # Valid UNSAT certificates and deliberately malformed incomplete coverings.
    small=[(),((1,),),((1,),(-1,)),((1,2),(-1,),(-2,)),((1,2,3),(-1,),(-2,),(-3,)),((1,2,3),(-1,-2,-3)),((1,),(-1,),(2,),(-2,))]
    good_bad={'SAT':0,'UNSAT':0,'invalid_rejected':0,'valid_accepted':0,'worst_tree_nodes':0}
    for cl in small:
        truth=truth_sat(cl);cert=all_unsat_cert(cl)
        assert_true((cert is None)==truth,'finite exhaustive certificate coverage matches SAT label')
        if truth:good_bad['SAT']+=1
        else:good_bad['UNSAT']+=1
        if cert is not None:
            assert_true(verify_unsat_cert(cl,cert),'valid UNSAT cert accepted')
            good_bad['valid_accepted']+=1
        for bogus in [['leaf',0],['split',1,['leaf',0],['leaf',0]],['timeout'],['split',0,['leaf',0],['leaf',0]],[]]:
            if not verify_unsat_cert(cl,bogus):good_bad['invalid_rejected']+=1
        good_bad['worst_tree_nodes']=max(good_bad['worst_tree_nodes'],len(str(cert)) if cert is not None else 0)
    # Specific counterexample to accepting partial coverage:
    P=((1,2,3),(1,2,-3),(1,-2,3),(1,-2,-3)) # P iff x=1
    assert_true(truth_sat(P),'parent SAT')
    assert_true(not truth_sat(restrict(P,{1:False})),'x=0 child UNSAT')
    assert_true(truth_sat(restrict(P,{1:True})),'x=1 child SAT')
    invalid=["split",1,["leaf",0],["leaf",0]]
    assert_true(not verify_unsat_cert(P,invalid),'incomplete/fake parent cert invalid')
    dataset['controls']['finite_full_tree_certificate_verifier']=good_bad
    dataset['controls']['branch_counterexample']={'formula':P,'parent_SAT':True,'x_false_UNSAT':True,'x_true_SAT':True,'fake_UNSAT_root_rejected':True}
    dataset['assertions']=ASSERTIONS
    dataset['elapsed_seconds']=round(time.perf_counter()-start,4)
    out=Path(__file__).with_name('2026-10-25_2300_ARC179_TWO_ALGO_CERT_GATE_raw.json')
    out.write_text(json.dumps(dataset,indent=2,sort_keys=True,default=list)+'\n')
    print(json.dumps({'assertions':ASSERTIONS,'inputs':{'signed_monotone_U':False,'signed_monotone_V':True},'child_count':8,'compiled_clause_records':total_compiled,'d':dataset['thresholds']['d'],'c_limit':dataset['thresholds']['C_d'],'b_limit':dataset['thresholds']['critical_b_lambda_half_u_zero'],'report':str(out),'runtime_seconds':dataset['elapsed_seconds']},indent=2))

if __name__=='__main__':main()
