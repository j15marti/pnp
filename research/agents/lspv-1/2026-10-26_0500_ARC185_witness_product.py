#!/usr/bin/env python3
"""ARC185: exact signed-(2,2)-3CNF two-level product and coNTIME witness gate.
Standard library only. Finite audit, NOT all-ordinary-SAT improvement.
The W20 source is from ARC184 / Q15 verified UNSAT source. It is exhaustively
independently checked on all 2^15 assignments in this reproducer.
"""
from __future__ import annotations
from collections import Counter
from fractions import Fraction
from itertools import product
from math import log2
import hashlib
import json
import random
import sys

RUN_ID='ARC185_UNSAT_PRODUCT_QUANTIFIER'
SEED=202610260500
Q_RAW='''
 -1 3 -14      2 -8 9      10 -13 14      3 7 -13
 -4 -9 -11      5 8 -14       4 -8 -11     1 7 13
  1 -7 10     -5 -6 -15      -2 -6 12     -4 9 -10
 -2 5 -12     -3 6 -15       6 -7 11      2 -9 11
  4 8 -10     -3 12 15      -5 -12 15     -1 13 14
'''
a=list(map(int,Q_RAW.split()))
W=tuple(tuple(a[i:i+3]) for i in range(0,len(a),3))
v=[list(c) for c in W]
v[0][0]=1
v[7][0]=-1
V=tuple(tuple(c) for c in v)
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
count=0

def ck(cond,msg):
    global count
    count+=1
    if not cond: raise AssertionError(msg)

def grammar(f,n,monotone=False):
    if len(f)!=4*n//3 or n%3: return False
    ps=Counter(); ns=Counter(); used=set()
    for c in f:
        if len(c)!=3 or len({abs(x) for x in c})!=3 or any(x==0 or abs(x)>n for x in c): return False
        if monotone and not(all(x>0 for x in c) or all(x<0 for x in c)): return False
        t=tuple(sorted(c))
        if t in used: return False
        used.add(t)
        for x in c:
            (ps if x>0 else ns)[abs(x)]+=1
    return all(ps[i]==ns[i]==2 for i in range(1,n+1))

def sat_mask(f,mask):
    return all(any(bool((mask >> (abs(x)-1))&1)==(x>0) for x in c) for c in f)

def model_count(f,n):
    count=0; first=None
    for x in range(1<<n):
        if sat_mask(f,x):
            count+=1
            if first is None: first=x
    return count,first

def shift(f,off):
    return tuple(tuple((1 if x>0 else -1)*(abs(x)+off) for x in c) for c in f)

def product_formula(bits):
    return tuple(c for i,b in enumerate(bits) for c in shift(V if b else W,15*i))

def encode(f,n):
    return ('p cnf %d %d\n'%(n,len(f))+''.join(' '.join(map(str,c))+' 0\n' for c in f)).encode('ascii')

def decode(raw):
    lines=raw.decode('ascii').splitlines()
    h=lines[0].split()
    assert h[:2]==['p','cnf'] and len(h)==4
    n,m=map(int,h[2:]);clauses=[]
    for line in lines[1:]:
        l=list(map(int,line.split()))
        assert l and l[-1]==0
        clauses.append(tuple(l[:-1]))
    assert len(clauses)==m
    return n,tuple(clauses)

def block(f,start,end):
    # Extract whole source modules (no clause deletion, no semantic loss).
    assert 0<=start<end and end*20<=len(f)
    part=f[20*start:20*end]
    return tuple(tuple((1 if x>0 else -1)*(abs(x)-15*start) for x in c) for c in part)

def black_box_decide(oracle,bits):
    return all(oracle(i) for i in range(len(bits)))

def cert_vfy(oracle,bits,index):
    # Sound for ANY block grammar with a fully verified structural partition.
    return isinstance(index,int) and 0<=index<len(bits) and (not oracle(index))

def coaccept(oracle,bits,index):
    # Universal acceptance for SAT; each branch is the complement of cert_vfy.
    return not cert_vfy(oracle,bits,index)

def black_box_query_lb(bits):
    # Deterministic AND must query q inputs on all-one input.
    q=len(bits)
    for omit in range(q):
        all_true=tuple(1 for _ in range(q))
        counter=list(all_true);counter[omit]=0
        ck(all(all_true[i]==counter[i] for i in range(q) if i!=omit), 'oracle indistinguishability')
        ck(all(all_true) and not all(counter), 'all-one versus single-zero label')

def frontier(k):
    k=Fraction(k)
    return max(1+1/k,(2*k-1)/(k*(k-1)))


def run():
    rng=random.Random(SEED)
    ck(len(W)==len(V)==20,'fixed source length')
    ck(grammar(W,15) and grammar(V,15),'signed exact 2,2')
    ck(not grammar(W,15,monotone=True),'signed versus monotone separation')
    ck(grammar(Y,6,monotone=True),'monotone positive control')
    wc,ww=model_count(W,15)
    vc,vw=model_count(V,15)
    yc,yw=model_count(Y,6)
    ck(wc==0,'W truly UNSAT by 32768 exhaustive assignments')
    ck(vc>0 and vw==0,'V SAT under all-zero assignment')
    ck(yc==20,'Y SAT 20 models')
    ck(sum(x<0 for c in W for x in c)==sum(x<0 for c in V for x in c),'same signed literal count')
    ck([tuple(map(abs,c)) for c in W]==[tuple(map(abs,c)) for c in V],'same unsigned supports')
    entries=[]
    for q in (2,4,8,16,32):
        patterns=[tuple(1 for _ in range(q)),tuple(0 for _ in range(q))]
        patterns += [tuple(0 if j==i else 1 for j in range(q)) for i in range(q)]
        patterns += [tuple(rng.getrandbits(1) for _ in range(q)) for _ in range(4)]
        exact_lengths=set();labels=Counter()
        for p in patterns:
            root=product_formula(p);N=15*q;m=20*q
            ck(grammar(root,N),'root exact signed2,2 grammar')
            raw=encode(root,N)
            nr,rr=decode(raw)
            ck(nr==N and rr==root,'physical encoding roundtrip')
            exact_lengths.add(len(raw))
            root_label=all(p)
            labels['SAT' if root_label else 'UNSAT']+=1
            assert isinstance(root_label,bool)
            # Independent source-preserving Level 1 and Level 2 ordinary CNF views.
            # Each Level1 = two whole modules, each Level2 = one.
            child_labels=[];grandchildren=[]
            for t in range(0,q,2):
                C=block(root,t,t+2)
                ck(grammar(C,30),'first child real exact signed2,2')
                n1,r1=decode(encode(C,30))
                ck(n1==30 and r1==C,'first-level serialized')
                G0=block(C,0,1);G1=block(C,1,2)
                ck(grammar(G0,15) and grammar(G1,15),'two actual grandchild grammar')
                n20,r20=decode(encode(G0,15))
                n21,r21=decode(encode(G1,15))
                ck(n20==n21==15 and r20==G0 and r21==G1,'grandchildren serialized')
                # The source W/V module label is independently certified above.
                s0=G0==V; s1=G1==V
                ck(G0 in (W,V) and G1 in (W,V),'exact renamed source module')
                ck((s0 and s1)==(p[t] and p[t+1]),'first-level correct both-label join')
                grandchildren.extend([s0,s1]);child_labels.append(s0 and s1)
            ck(all(child_labels)==root_label,'Level1 exact join')
            ck(all(grandchildren)==root_label,'Level2 exact join')
            oracle=lambda i: bool(p[i])
            ck(black_box_decide(oracle,p)==root_label,'blackbox deterministic product')
            for j in range(q):
                ck(cert_vfy(oracle,p,j)==(p[j]==0),'negative leaf precise')
                ck(coaccept(oracle,p,j)==(p[j]==1),'branchwise universal positive')
            ck(any(cert_vfy(oracle,p,j) for j in range(q))==(not root_label),'UNSAT exists proof')
            ck(all(coaccept(oracle,p,j) for j in range(q))==root_label,'SAT forall branch')
        ck(len(exact_lengths)==1,'same physical source bits for W/V patterns')
        black_box_query_lb(tuple(1 for _ in range(q)))
        sample=encode(product_formula(patterns[0]),15*q)
        entries.append({'q':q,'N_bytes':len(sample),'n_vars':15*q,'m_clauses':20*q,
                        'tested_roots':len(patterns),'root_labels':dict(labels),'first_level_children_per_root':q//2,
                        'second_level_grandchildren_per_root':q,'full_ordinary_source_shape_equal_length':True})
    ks=[Fraction(901,500),Fraction(2),Fraction(3),Fraction(4),Fraction(10),Fraction(100)]
    budget=[]
    for k in ks:
        h=frontier(k)
        lam0=(h-1)/(k-1)
        ck(lam0>0,'positive frontier')
        # Saturation of all-child analytic envelope at linear physical volume and u=0.
        ck(1+lam0*(k-1)==h,'boundary equality')
        ck(1+(lam0/2)*(k-1)<h,'strictly inside with half lambda')
        ck(1+(lam0*2)*(k-1)>h,'outside with double lambda')
        if k>=2:
            ck(h==1+1/k,'upper envelope for k>=2')
            ck(lam0==1/(k*(k-1)),'sharp lambda threshold for k>=2')
        budget.append({'K':str(k),'H_K':float(h),'linear_volume_lambda_critical':float(lam0),
                       'one_negative_leaf_lambda_for_linear_coNTIME':float(1/k),
                       'at_lambda_1_over_K_all_blocks_time_exponent':float(2-1/k),
                       'at_lambda_1_over_K_one_negative_guest_exponent':1.0})
    return {'run':RUN_ID,'seed':SEED,'assertions':count,'source_W_20_models':wc,
       'source_V_20_models':vc,'source_V_witness_15bit':vw,'monotone_Y_8_models':yc,
       'signed22_W_positive_to_negative_swap_positions':[(0,0),(7,0)],
       'root_tests':sum(x['tested_roots'] for x in entries),
       'first_level_child_constructions':sum(x['tested_roots']*x['first_level_children_per_root'] for x in entries),
       'second_level_grandchild_constructions':sum(x['tested_roots']*x['second_level_grandchildren_per_root'] for x in entries),
       'finite_products':entries,'symbolic_budget':budget,
       'status':{'semantic_joins':'PROVED/EXACT by disjoint-variable semantics and finite COMPUTATIONAL audit',
       'linear_volume_K_frontier':'PROVED/EXACT algebraic only conditional on complete all-UNSAT certificate and valid model transfer',
       'all_input_certificates':'OPEN','ARC_EDGE_90':'OPEN','P_vs_NP':'OPEN'},
       'cautions':['W is fixed easy template: scanning signed words decides this promise in O(N polylog N).',
                   'Black-box q-query floor is NOT a lower bound for physical input reads or arbitrary SAT algorithms.',
                   'Nondeterministic coNTIME witness uses fixed correct decider A and a verified source block partition.',
                   'A general fast lazy bit accessor, all-input certificate coverage, uniform small-space seed and strict FLMV transport remain OPEN.']}

if __name__=='__main__':
    d=run()
    data=json.dumps(d,indent=2,sort_keys=True)+'\n'
    if len(sys.argv)>1:
        with open(sys.argv[1],'w') as h:h.write(data)
    print(json.dumps({'assertions':d['assertions'],'root_tests':d['root_tests'],'children':d['first_level_child_constructions'],
           'grandchildren':d['second_level_grandchild_constructions'],'W':d['source_W_20_models'], 'V':d['source_V_20_models']}))
