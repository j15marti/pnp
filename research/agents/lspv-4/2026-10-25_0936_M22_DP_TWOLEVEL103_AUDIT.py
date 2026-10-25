#!/usr/bin/env python3
"""Exact two-level M22 Davis-Putnam projection audit (stdlib only).
Run in a checkout of j15marti/pnp for the published U198 fixture;
otherwise Y/H and generated controls still run. Finite tests are not LBs.
"""
import ast
import itertools
import json
from collections import Counter
from pathlib import Path

P = [(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
Q = [(1,2,4),(1,3,6),(2,3,5),(4,5,6)]

def normalize(c):
    if len(set(c)) != len(c) or any(-z in c for z in c):
        return None
    return tuple(sorted(c, key=lambda z: (abs(z), z)))

def canonical(F):
    return tuple(sorted({z for c in F if (z := normalize(c)) is not None}))

def names(F):
    return sorted({abs(z) for c in F for z in c})

def grammar(F):
    V=names(F)
    if len({normalize(c) for c in F}) != len(F):return False
    if any(len(c)!=3 or len(set(map(abs,c)))!=3 or len({z>0 for z in c})!=1 for c in F):return False
    deg=Counter((abs(z),z>0) for c in F for z in c)
    return all(deg[(v,True)]==deg[(v,False)]==2 for v in V)

def mis(F):
    blocked=set(); chosen=[]
    for v in names(F):
        if v in blocked:continue
        chosen.append(v)
        for c in F:
            if any(abs(z)==v for z in c):blocked.update(map(abs,c))
    return chosen

def elim(F, pivot):
    P=[c for c in F if pivot in c]
    Q=[c for c in F if -pivot in c]
    rest=[c for c in F if pivot not in c and -pivot not in c]
    raw=[tuple(z for z in a if z!=pivot)+tuple(z for z in b if z!=-pivot)
         for a in P for b in Q]
    result=canonical(rest+raw)
    return result,{'pivot':pivot,'positive_parents':len(P),'negative_parents':len(Q),
                   'raw_resolvents':len(raw),'retained_resolvents':len(result)-len(rest)}

def round_dp(F):
    chosen=mis(F); G=F; logs=[]
    for v in chosen:
        G,entry=elim(G,v)
        logs.append(entry)
    return G,chosen,logs

def sat_at(F,assignment):
    return all(any(assignment[abs(z)] == (z>0) for z in c) for c in F)

def verify_project(F,G,deleted):
    allvars=names(F); survive=[v for v in allvars if v not in deleted]
    checks=0
    for vbits in itertools.product((False,True),repeat=len(survive)):
        fixed=dict(zip(survive,vbits))
        expected=False
        for dbits in itertools.product((False,True),repeat=len(deleted)):
            a={**fixed,**dict(zip(deleted,dbits))}
            expected |= sat_at(F,a)
        assert sat_at(G,fixed)==expected
        checks+=1
    return checks

def data(F,label,check_finite):
    assert grammar(F)
    F=canonical(F); k=len(names(F)); assert len(F)*3==k*4
    G,one,l1=round_dp(F)
    H,two,l2=round_dp(G)
    assert len(one)>= (k+8)//9
    assert len(two)>= (len(names(G))+24)//25
    assert len(names(G))<=8*k/9 and len(names(H))<=64*k/75
    assert all(e['positive_parents']<=2 and e['negative_parents']<=2 for e in l1)
    assert all(e['positive_parents']<=4 and e['negative_parents']<=4 for e in l2)
    assert max(map(len,G),default=0)<=4 and max(map(len,H),default=0)<=6
    assert len(G)<=len(F) and len(H)<=len(F)+8*len(two)
    checks=0
    if check_finite:
        checks=verify_project(F,G,one)+verify_project(G,H,two)
        assert any(sat_at(F,dict(zip(names(F),bits))) for bits in itertools.product((False,True),repeat=k)) == (label=='SAT')
    def stage(C):
        return {'active_variables':len(names(C)),'clauses':len(C),
                'literal_occurrences':sum(map(len,C)),
                'width_histogram':dict(sorted(Counter(map(len,C)).items()))}
    return {'label':label,'source':stage(F),'first':stage(G),'second':stage(H),
            'first_pivots':len(one),'second_pivots':len(two),
            'first_tautology_or_duplicate_drops':sum(e['raw_resolvents']-e['retained_resolvents'] for e in l1),
            'second_tautology_or_duplicate_drops':sum(e['raw_resolvents']-e['retained_resolvents'] for e in l2),
            'projection_truth_table_rows_checked':checks}

def main():
    Y=[tuple(c) for c in P]+[tuple(-z for z in c) for c in Q]
    H=[tuple(c) for c in P]+[tuple(-z for z in c) for c in P]
    result={'claim':'M22-DP-TWOLEVEL103','checks':'projection equivalence exhaustive on Y/H; imported UNSAT label for U198',
            'controls':[data(Y,'SAT',True),data(H,'SAT',True)]}
    ufile=Path(__file__).resolve().parents[2]/'lspv-2'/'2026-10-24_0011_DOECKER61_original_source.txt'
    if not ufile.exists():
        ufile=Path(__file__).resolve().parent/'DOECKER61_original_source.txt'
    if ufile.exists():
        U=ast.literal_eval('\n'.join(z for z in ufile.read_text().splitlines() if not z.lstrip().startswith('#')))
        assert len(U)==264 and len(names(U))==198
        result['controls'].append(data(U,'published UNSAT',False))
        result['U_provenance']=str(ufile)
    else: result['U_fixture_status']='not mounted locally; run in GitHub checkout'
    print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':main()
