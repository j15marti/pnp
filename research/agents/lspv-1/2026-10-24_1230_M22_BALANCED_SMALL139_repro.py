#!/usr/bin/env python3
"""Finite controls for the fixed-weight M22 satisfiability theorem.
Standard library only. Self-contained, no SAT oracle.
"""
import itertools, json, random, hashlib, time
from collections import Counter
from pathlib import Path

SEED=202610241230
R=random.Random(SEED)

def supports(k):
    return list(itertools.combinations(range(k),3))

def valid_side(k, side):
    if len(side)!=2*k//3 or len(set(side))!=len(side) or any(len(set(tri))!=3 for tri in side): return False
    degrees=Counter(x for tri in side for x in tri)
    return all(degrees[x]==2 for x in range(k))

def sample_side(k, tries=10000):
    for _ in range(tries):
        sockets=list(range(k))*2
        R.shuffle(sockets)
        side=tuple(tuple(sorted(sockets[i:i+3])) for i in range(0,len(sockets),3))
        if valid_side(k,side): return tuple(sorted(side))
    raise RuntimeError('Failed to draw balanced 3-uniform side')

def label_count(k,P,Q,weight=None):
    n_sat=0
    for mask in range(1<<k):
        if weight is not None and mask.bit_count()!=weight: continue
        if all(any(mask>>a&1 for a in triple) for triple in P) and all(any(not(mask>>a&1) for a in triple) for triple in Q):
            n_sat+=1
    return n_sat

def clause_fail_multiplicity(k,P,Q,t):
    hist=Counter(); sumfail=0
    for true_set in itertools.combinations(range(k),t):
        T=set(true_set)
        fail=sum(T.isdisjoint(c) for c in P)+sum(set(c).issubset(T) for c in Q)
        hist[fail]+=1
        sumfail+=fail
    return dict(sorted(hist.items())),sumfail

def full_k6():
    S=supports(6)
    sides=[tuple(g) for g in itertools.combinations(S,4) if valid_side(6,g)]
    assert len(sides)==75
    histq=Counter(); mins={3:10**9,'all':10**9}; maxs={3:0,'all':0};bad=0
    for P in sides:
        pset=set(P)
        for Q in sides:
            q=len(pset-set(Q)); histq[q]+=1
            models3=label_count(6,P,Q,3)
            modelsall=label_count(6,P,Q,None)
            mins[3]=min(mins[3],models3);mins['all']=min(mins['all'],modelsall)
            maxs[3]=max(maxs[3],models3);maxs['all']=max(maxs['all'],modelsall)
            if models3<12 or modelsall==0:bad+=1
    return {'sides':75,'ordered_pairs':len(sides)**2,'q_histogram':dict(sorted(histq.items())),
            'min_models_weight3':mins[3],'max_models_weight3':maxs[3],
            'min_models_total':mins['all'],'max_models_total':maxs['all'],'failures':bad}

def swap_two_disjoint(P):
    for i,A in enumerate(P):
        for j,B in enumerate(P):
            if i>=j or not set(A).isdisjoint(B): continue
            for a in A:
                for b in B:
                    Q=list(P)
                    Q[i]=tuple(sorted((set(A)-{a})|{b}))
                    Q[j]=tuple(sorted((set(B)-{b})|{a}))
                    if valid_side(9,Q) and len(set(P)-set(Q))==2:
                        return tuple(sorted(Q))
    raise AssertionError('Every generated cubic side should admit two disjoint clause supports')

def k9_controls(count):
    vals={'tested':count,'failed':0,'paired':0,'nonpaired':0,'weight4_min':10000,'weight5_min':10000,
          'weight4_max':0,'weight5_max':0,'q_histogram':Counter(),'sum_bad_weight4':Counter(),
          'positive_pair_overlap_checks':0,'repeated_sources':0,'pair_overlap_min':999999,'positive_surplus_min':999999,'fixed_q2':0,'fixed_q0':0}
    seen=set()
    for trial in range(count):
        P=sample_side(9)
        Q= P if trial==0 else (swap_two_disjoint(P) if trial<=100 else sample_side(9))
        if trial==0: vals['fixed_q0']+=1
        if 1<=trial<=100: vals['fixed_q2']+=1
        key=(P,Q)
        if key in seen: vals['repeated_sources']+=1
        seen.add(key)
        q=len(set(P)-set(Q));vals['q_histogram'][q]+=1
        vals['paired' if q==0 else 'nonpaired']+=1
        w4=label_count(9,P,Q,4);w5=label_count(9,P,Q,5)
        vals['weight4_min']=min(vals['weight4_min'],w4)
        vals['weight5_min']=min(vals['weight5_min'],w5)
        vals['weight4_max']=max(vals['weight4_max'],w4)
        vals['weight5_max']=max(vals['weight5_max'],w5)
        hist, sum_bad=clause_fail_multiplicity(9,P,Q,4)
        vals['sum_bad_weight4'][sum_bad]+=1
        assert sum_bad==126,(P,Q,sum_bad)
        overlap=any(len(set(A)&set(B))>=1 for A,B in itertools.combinations(P,2))
        pair_overlap=sum(sum(T.isdisjoint(A) and T.isdisjoint(B)
                   for T in (set(t) for t in itertools.combinations(range(9),4)))
                   for A,B in itertools.combinations(P,2))
        vals['pair_overlap_min']=min(vals['pair_overlap_min'],pair_overlap)
        assert pair_overlap>=9
        positive_surplus=sum(max(sum(T.isdisjoint(A) for A in P)-1,0)
                             for T in (set(t) for t in itertools.combinations(range(9),4)))
        vals['positive_surplus_min']=min(vals['positive_surplus_min'],positive_surplus)
        assert positive_surplus>=6
        if overlap: vals['positive_pair_overlap_checks']+=1
        if not(w4>=6 and w5>=6 and overlap):vals['failed']+=1
    vals['q_histogram']=dict(sorted(vals['q_histogram'].items()))
    vals['sum_bad_weight4']=dict(sorted(vals['sum_bad_weight4'].items()))
    return vals

def fixture():
    P=[tuple(i-1 for i in p) for p in [(1,2,3),(1,4,5),(2,4,6),(3,5,6)]]
    Q=[tuple(i-1 for i in p) for p in [(1,2,4),(1,3,6),(2,3,5),(4,5,6)]]
    assert valid_side(6,P) and valid_side(6,Q) and set(P).isdisjoint(Q)
    assert label_count(6,P,Q)==20
    assert all(any((0b000111>>x)&1 for x in s) for s in P)
    assert all(any(not((0b000111>>x)&1) for x in s) for s in Q)
    return {'valid':True,'unpaired':True,'models_total':20,'model_111000':True,'models_weight3':label_count(6,P,Q,3)}

if __name__=='__main__':
    start=time.monotonic()
    out={'run':'M22-BALANCED-SMALL139','proof_status':'PROVED/EXACT combinatorial theorem; COMPUTATIONAL finite controls only',
         'seed':SEED,'source_fixture':fixture(),'k6_complete':full_k6(),'k9_sample':k9_controls(300),
         'unsat_controls':'Published 198-variable unsatisfiable M22 construction is literature-supported, not exhaustively checked here',
         'limits':'k9 controls are sampled, not an exhaustive census; all-input lower bound remains OPEN'}
    out['seconds']=round(time.monotonic()-start,3)
    path=str(Path(__file__).with_name('M22_BALANCED_SMALL139_results.json'))
    with open(path,'w') as f:json.dump(out,f,indent=2,sort_keys=True)
    print(json.dumps(out,indent=2,sort_keys=True))
    print('script_sha256',hashlib.sha256(open(__file__,'rb').read()).hexdigest())
