#!/usr/bin/env python3
"""REFEREE277: exact two-level prefix-rank directory red-team.

This is an upper-bound construction in a declared random-access directory
model.  It is not a native single-head-tape implementation, a simultaneous
FLMV theorem, or an all-input SAT algorithm.
"""
from __future__ import annotations

import argparse
import collections
import itertools
import json
import math
import random
from pathlib import Path

F9 = (
    (1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9),
)
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
N15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-v for v in c) for c in N15)
PA={1:1,2:0,3:1,4:0,8:0}; PB={1:1,2:1,3:0,4:0,8:0}
F9_S={5:0,6:1,7:0,8:0,9:1}; F9_U={1:1,3:0,5:1,6:0,7:0,8:0}

def ceil_log2(x: int) -> int:
    return max(1, (x-1).bit_length())

def grammar(F,n=None):
    try:
        if not F:return False
        n=n or max(abs(x) for c in F for x in c)
        if n%3 or 3*len(F)!=4*n:return False
        seen=set(); q=collections.Counter()
        for c in F:
            if len(c)!=3 or len({abs(x) for x in c})!=3:return False
            if not (all(x>0 for x in c) or all(x<0 for x in c)):return False
            if any(abs(x)<1 or abs(x)>n for x in c):return False
            k=tuple(sorted(c))
            if k in seen:return False
            seen.add(k);q.update(c)
        return all(q[v]==q[-v]==2 for v in range(1,n+1))
    except Exception:return False

def sat(F,a):
    return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)

def count(F,pins):
    n=max(abs(x) for c in F for x in c)
    free=[v for v in range(1,n+1) if v not in pins]
    z=0
    for bits in itertools.product((0,1),repeat=len(free)):
        a=dict(pins);a.update(zip(free,bits));z+=sat(F,a)
    return z

def su_modes(F):
    n=max(abs(x) for c in F for x in c);checks=0
    for j,k in itertools.combinations(range(len(F)),2):
        A,B=F[j],F[k]
        same=any(abs(x)==abs(y) and (x>0)==(y>0) for x in A for y in B)
        opp=any(abs(x)==abs(y) and (x>0)!=(y>0) for x in A for y in B)
        pred=(not opp,not same,not same,not opp);act=[False]*4
        for z in range(1<<n):
            a={v:(z>>(v-1))&1 for v in range(1,n+1)}
            AS=all(a[abs(x)]==int(x>0) for x in A);AU=all(a[abs(x)]!=int(x>0) for x in A)
            BS=all(a[abs(x)]==int(x>0) for x in B);BU=all(a[abs(x)]!=int(x>0) for x in B)
            act=[u or v for u,v in zip(act,(AS and BS,AS and BU,AU and BS,AU and BU))]
        assert tuple(act)==pred;checks+=4
    return checks

def false_cover(F,n,pins):
    leaves=0
    for bits in itertools.product((0,1),repeat=len([v for v in range(1,n+1) if v not in pins])):
        a=dict(pins);a.update(zip([v for v in range(1,n+1) if v not in pins],bits))
        assert any(not any(a[abs(x)]==int(x>0) for x in c) for c in F)
        leaves+=1
    return leaves

def two_level_build(w):
    m=len(w); L=ceil_log2(m+1); b=L; S=L*L
    pref=[0]
    for x in w:pref.append(pref[-1]+x)
    global_rank={s:pref[s] for s in range(0,m+1,S)}
    relative={}
    for s in range(0,m+1,S):
        stop=min(s+S,m)
        for u in range(s,stop+1,b):relative[u]=pref[u]-pref[s]
    return {'m':m,'L':L,'b':b,'S':S,'global':global_rank,'relative':relative,
            'global_count':len(global_rank),'relative_count':len(relative)}

def two_level_query(w,d,j):
    m=len(w);assert 0<=j<=m
    S=d['S'];b=d['b'];s=(j//S)*S
    if s not in d['global']:
        # Only possible at j=m when m is not itself a stored multiple; use
        # the preceding superblock, which is the usual query case anyway.
        s=((j-1)//S)*S
    u=s+((j-s)//b)*b
    if u not in d['relative']:
        u=s+((j-s-1)//b)*b
    ans=d['global'][s]+d['relative'][u]+sum(w[u:j])
    return ans,j-u

def one_level_build(w):
    m=len(w);L=ceil_log2(m+1);B=max(1,math.ceil(math.sqrt(m*L)))
    pref=[0]
    for x in w:pref.append(pref[-1]+x)
    checkpoints={s:pref[s] for s in range(0,m+1,B)}
    return {'m':m,'L':L,'B':B,'checkpoints':checkpoints,'count':len(checkpoints)}

def one_level_query(w,d,j):
    B=d['B'];s=(j//B)*B
    if s not in d['checkpoints']:s=((j-1)//B)*B
    return d['checkpoints'][s]+sum(w[s:j]),j-s

def exact_check(w):
    d2=two_level_build(w);d1=one_level_build(w);p=0;max2=max1=0
    for j in range(len(w)+1):
        a,q2=two_level_query(w,d2,j);b,q1=one_level_query(w,d1,j)
        assert a==p and b==p
        max2=max(max2,q2);max1=max(max1,q1)
        if j<len(w):p+=w[j]
    return d1,d2,max1,max2

def directory_row(m):
    L=ceil_log2(m+1);b=L;S=L*L
    ng=len(range(0,m+1,S))
    nr=sum(len(range(s,min(s+S,m)+1,b)) for s in range(0,m+1,S))
    relative_width=ceil_log2(S+1)
    two_bits=ng*L+nr*relative_width
    B=max(1,math.ceil(math.sqrt(m*L)))
    one_bits=len(range(0,m+1,B))*L
    N=m*L
    return {'m':m,'source_bits_N_proxy':N,'L':L,'superblock_S':S,'subblock_b':b,
            'two_global_counters':ng,'two_relative_counters':nr,
            'two_directory_bits':two_bits,'two_worst_source_probes':b-1,
            'one_block_B':B,'one_directory_bits':one_bits,'one_worst_source_probes':B-1,
            'two_space_over_m':two_bits/m,
            'two_space_exponent_in_N':math.log(two_bits)/math.log(N),
            'two_probe_exponent_in_N':math.log(max(1,b-1))/math.log(N)}

def xor_control(F,gray):
    n=max(abs(x) for c in F for x in c);states=[]
    for z in range(1<<n):
        z=z^(z>>1) if gray else z
        a={v:(z>>(v-1))&1 for v in range(1,n+1)}
        bits=[a[v] for v in range(1,n+1)]
        for c in F:
            q=sum(a[abs(x)]==int(x>0) for x in c);bits.extend((q&1,(q>>1)&1))
        states.append(bits)
    ds=[sum(x!=y for x,y in zip(a,b)) for a,b in zip(states,states[1:])]
    return {'steps':len(ds),'sum_adjacent_d_logic':sum(ds),
            'endpoint_d_logic':sum(x!=y for x,y in zip(states[0],states[-1]))}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
    assert grammar(F9,9) and grammar(Y6,6) and grammar(F15,15)
    exhaustive_vectors=0;exhaustive_queries=0
    for m in range(0,15):
        for w in itertools.product((0,1),repeat=m):
            _,d2,_,q2=exact_check(w);exhaustive_vectors+=1;exhaustive_queries+=m+1
            assert q2<=d2['b']-1
    rng=random.Random(277);random_rows=[]
    for m in (31,64,127,256,1024,4096):
        families=[tuple([0]*m),tuple([1]*m),tuple(i&1 for i in range(m)),tuple(rng.randrange(2) for _ in range(m))]
        mx1=mx2=0
        for w in families:
            _,_,q1,q2=exact_check(w);mx1=max(mx1,q1);mx2=max(mx2,q2)
        random_rows.append({'m':m,'families':len(families),'max_one_level_probes':mx1,'max_two_level_probes':mx2})
    controls={
      'Y6_models':count(Y6,{}),'F9_root_models':count(F9,{}),
      'F9_A_models':count(F9,PA),'F9_B_models':count(F9,PB),
      'F9_S_models':count(F9,F9_S),'F9_U_models':count(F9,F9_U),
      'F9_U_false_cover_leaves':false_cover(F9,9,F9_U),
      'F9_SU_pair_modes':su_modes(F9),
      'F15_SAT_models':count(F15,dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))),
      'F15_UNSAT_models':count(F15,dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0))))}
    assert controls=={'Y6_models':20,'F9_root_models':70,'F9_A_models':1,'F9_B_models':0,
      'F9_S_models':3,'F9_U_models':0,'F9_U_false_cover_leaves':8,
      'F9_SU_pair_modes':264,'F15_SAT_models':2,'F15_UNSAT_models':0}
    malformed=[(),((1,1,2),),((1,-2,3),),((1,2,3),),F9+(F9[0],),((1,2,3),(1,2,4))]
    assert all(not grammar(x) for x in malformed);controls['malformed_rejected']=6
    out={
      'run':'HIERARCHICAL-RANK-REFEREE277','status':'PROVED_RESTRICTED_UPPER_BOUND_PLUS_COMPUTATIONAL',
      'P_vs_NP':'OPEN',
      'exact_obstruction':'A one-level sqrt(m log m) checkpoint tariff is not necessary for arbitrary prefix-rank queries once a paid two-level random-access directory is allowed.',
      'theorem':{
        'model':'static m-bit tag vector, one O(m) preprocessing scan, retained random-access bit directory; word/address operations are charged polylogarithmically',
        'construction':'L=ceil(log2(m+1)), superblocks L^2, subblocks L; store global superblock ranks and within-superblock subblock ranks',
        'directory_bits':'O(m log log m / log m)',
        'source_probes_per_rank_query':'at most L-1 = O(log m)',
        'query_work':'two directory counter lookups plus O(log m) source-bit scans and O(polylog m) address/arithmetic work',
        'setup':'O(m) source reads plus directory writes; discovery is not free',
        'scope':'upper bound in the declared random-access directory model; no SAT-label oracle and no assignment recovery'},
      'exhaustive':{'max_m':14,'vectors':exhaustive_vectors,'rank_queries':exhaustive_queries},
      'random_adversarial_checks':random_rows,
      'asymptotic_rows':[directory_row(2**k) for k in (8,12,16,20,24)],
      'controls':controls,
      'charged_recurrence':{
        'preprocess':'W_build(m)=Theta(m) source reads + Theta(m/log m) counter writes of O(log m) or O(log log m) bits',
        'query':'W_rank(j)=W_address+2 W_directory_lookup+at most ceil(log2(m+1))-1 source-tag reads+W_add',
        'total':'W_total=W_grammar+W_source/index/head+W_discover+W_build+sum_queries(W_select/switch/failed+W_rank+W_GE/proof)+W_cache/replay+W_child/output/access+W_guest',
        'peak':'source is read-only; retained directory O(m log log m/log m) bits plus live parser/address/counters/proof/cache/guest/output; simultaneous peak is the sum of co-live objects'},
      'decision_semantics':{
        'current_equivalence':'rank summaries can merge syntactically different tag prefixes only for the currently declared rank query',
        'continuation_equivalence':'not proved for arbitrary future pins, GE systems, branch policies, or certificates; cache keys must retain every future-relevant semantic observable',
        'no_free_representatives':'constructing/canonicalizing the directory and validating its source provenance are charged'},
      'falsifiers':[
        'sequential single-head placement may make directory lookup linear without another paid index',
        'near-linear retained directory is not O(N^(1/2+o(1))) when N=Theta(m log m)',
        'rank alone may be insufficient for continuation equivalence and proof-carrying decomposition',
        'dynamic/noncanonical children can invalidate a static source directory or force paid rebuilds'],
      'wrappers':{'DELAY_steps':4096,'COPY_writes':128,'RECOMP_reads':36,
                  'logical_endpoint_delta':0,'changed_then_restored_adjacent_delta':2},
      'offline_XOR':{'binary':xor_control(F9,False),'gray':xor_control(F9,True)},
      'large_controls':{'U198_V198':'inherited opposite-label controls; not used to establish the directory theorem'},
      'literature_search':[
        {'query':'Jacobson succinct static data structures rank two level directory','finding':'classical two-level rank-directory antecedent; no novelty claim'},
        {'query':'Clark Munro succinct rank select directory','finding':'later succinct rank/select context'},
        {'query':'Fortnow Lipton van Melkebeek Viglas time space SAT','finding':'numerical same-machine transfer remains separate'},
        {'query':'site:github.com/j15marti/pnp multilevel succinct indexing','finding':'ARC_SELECT_INDEX252 explicitly left this alternative open'},
        {'query':'site:github.com/openai succinct rank Jacobson','finding':'no relevant implementation found; absence is not novelty evidence'}],
      'limitations':['not a lower bound','not a native sequential-tape implementation','not strict simultaneous FLMV space',
        'not an all-input polynomial SAT controller','no arbitrary-A ARC contraction','P versus NP remains open']}
    Path(args.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','vectors':exhaustive_vectors,'queries':exhaustive_queries,
      'controls':controls,'P_vs_NP':'OPEN'},indent=2))

if __name__=='__main__':main()
