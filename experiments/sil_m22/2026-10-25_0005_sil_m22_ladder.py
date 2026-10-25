#!/usr/bin/env python3
"""Small reproducible SIL/M22 reduction-ladder audit.

All counts in this program are combinatorial or declared serialization proxies,
NOT measured RAM/Turing-machine steps or universal lower bounds.
Standard library only. Runs the complete six-variable M22 grammar census and
one exact positive/negative paired-core Davis-Putnam projection.
"""
from itertools import combinations, product
from collections import Counter
from math import ceil, log2
import json


def cnf(P,Q):
    out=[]
    for e in P: out.append(tuple((1,x) for x in e))
    for e in Q: out.append(tuple((-1,x) for x in e))
    return out

def canonical(C):
    lits=set(C)
    if any((-s,x) in lits for s,x in lits):
        return None   # TRUE clause; remove from conjunction
    return tuple(sorted(lits,key=lambda v:(v[1],v[0])))

def valid(P,Q,variables):
    if len(P)!=len(set(P)) or len(Q)!=len(set(Q)): return False
    if any(len(e)!=3 or len(set(e))!=3 for e in P+Q):return False
    return all(sum(x in e for e in P)==2 and
               sum(x in e for e in Q)==2 for x in variables)

def classify(P,Q):
    H=set(P)&set(Q)
    UP=set(P)-H
    UN=set(Q)-H
    D=sorted({x for c in UP for x in c}|{x for c in UN for x in c})
    return dict(h=len(H),q_positive=len(UP),q_negative=len(UN),
                d=len(D),paired=[list(s) for s in sorted(H)],
                pos_defect=[list(s) for s in sorted(UP)],
                neg_defect=[list(s) for s in sorted(UN)],D=D)

def eval_formula(F,assignment):
    return all(any((assignment[x]==1 if sign==1 else assignment[x]==0)
                   for sign,x in C) for C in F)

def models(F,variables):
    return [dict(zip(variables,a)) for a in product((0,1),repeat=len(variables))
            if eval_formula(F,dict(zip(variables,a)))]

def project_dp(F,pivot):
    pos=[c for c in F if (1,pivot) in c]
    neg=[c for c in F if (-1,pivot) in c]
    no=[c for c in F if (1,pivot) not in c and (-1,pivot) not in c]
    output=list(no)
    candidate=len(pos)*len(neg)
    taut=0
    surviving=[]
    for p in pos:
        for n in neg:
            cand=canonical([x for x in p if x!=(1,pivot)]+
                           [x for x in n if x!=(-1,pivot)])
            if cand is None:
                taut+=1
            elif cand not in output:
                output.append(cand);surviving.append(cand)
    return output,dict(pivot=pivot,positive_parents=len(pos),
                       negative_parents=len(neg),candidate_resolvents=candidate,
                       tautological_resolvents=taut,
                       kept_resolvents=len(surviving),
                       removed_parents=len(pos)+len(neg),
                       original_clauses=len(F),remaining_clauses=len(output),
                       original_literals=sum(map(len,F)),
                       remaining_literals=sum(map(len,output)),
                       max_resulting_width=max(map(len,output)))

def logical_fields(F,variables):
    # Explicit declared proxy: fixed 3-bit clause-size fields, and one signed
    # variable-ID record (1+ceil(log2(max ID+1)) bits) per literal, plus
    # two ID-width header fields. Does not claim FLMV machine bit length.
    w=max(1,ceil(log2(max(variables)+1)))
    return 2*w+sum(3+len(c)*(1+w) for c in F)

def census_six():
    vars_=range(1,7)
    triples=list(combinations(vars_,3))
    fam=[]
    for ii in combinations(range(len(triples)),4):
        c=tuple(triples[j] for j in ii)
        if all(sum(v in e for e in c)==2 for v in vars_):fam.append(c)
    p_masks={};n_masks={}
    for p in fam:
        pm=nm=0
        for j,bits in enumerate(product((0,1),repeat=6)):
            z=dict(zip(vars_,bits))
            if all(any(z[x]==1 for x in e) for e in p): pm|=1<<j
            if all(any(z[x]==0 for x in e) for e in p): nm|=1<<j
        p_masks[p]=pm;n_masks[p]=nm
    hist=Counter();models_hist=Counter();unsat=0
    for P in fam:
        for Q in fam:
            q=4-len(set(P)&set(Q))
            ct=(p_masks[P]&n_masks[Q]).bit_count()
            hist[q]+=1;models_hist[ct]+=1
            unsat+=ct==0
    return dict(positive_support_families=len(fam),
                formulas=len(fam)**2,q_histogram=dict(sorted(hist.items())),
                unsatisfiable=unsat,minimum_model_count=min(models_hist),
                maximum_model_count=max(models_hist),
                model_count_histogram=dict(sorted(models_hist.items())))


def main():
    # Names a,b,c,d,e,z -> IDs 1..6; example from M22-WEIGHTED-LEAF-FACTOR110.
    P=[(1,2,6),(3,4,6),(1,2,5),(3,4,5)]
    Q=[(1,2,6),(3,4,6),(1,3,5),(2,4,5)]
    assert valid(P,Q,list(range(1,7)))
    src=cnf(P,Q)
    c=classify(P,Q)
    new,dp=project_dp(src,6)
    orig=models(src,list(range(1,7)))
    reduced=models(new,list(range(1,6)))
    projected={tuple(a[j] for j in range(1,6)) for a in orig}
    assert projected=={tuple(a[j] for j in range(1,6)) for a in reduced}
    assert len(orig)==22 and len(reduced)==16
    assert dp['candidate_resolvents']==4 and dp['tautological_resolvents']==2
    assert dp['kept_resolvents']==2 and dp['remaining_clauses']==6
    assert logical_fields(src,list(range(1,7)))==126
    assert logical_fields(new,list(range(1,6)))==104
    output={
      'source':'project M22 partial6 control, paired core of M22-WEIGHTED-LEAF-FACTOR110',
      'source_valid':True,'source_nvars':6,'source_clauses':len(src),
      'source_literal_occurrences':sum(map(len,src)),
      'classification':c,
      'SIL_trace':['FA5: paired supports become NAE3 (semantic exact E)',
                   'VE5: eliminate private paired-core pivot z, exact P'],
      'VE5_counts':dp,
      'initial_source_models':len(orig),
      'projected_models':len(reduced),
      'declared_serialized_bits_before':logical_fields(src,list(range(1,7))),
      'declared_serialized_bits_after':logical_fields(new,list(range(1,6))),
      'reduced_CNF':[[('' if s==1 else '-')+str(x) for s,x in clause] for clause in new],
      'reduced_is_Cstar':False,
      'available_2_pow_d_cases':2**c['d'],
      'available_3_pow_q_cases':3**c['q_positive'],
      'six_var_full_census':census_six(),
      'scope':'Exact finite classification, exact existential projection, enumerative upper budgets; no universal decision-time lower bound, no measured Turing machine steps.'
    }
    print(json.dumps(output,indent=2))

if __name__=='__main__':main()