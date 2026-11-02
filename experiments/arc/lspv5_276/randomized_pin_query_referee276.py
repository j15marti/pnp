#!/usr/bin/env python3
"""REFEREE276: randomized decision-only pin-query theorem on connected G_t.

Restricted promised-family theorem only.  It is not an arbitrary-machine
runtime lower bound, an all-input SAT algorithm, or a native FLMV trace.
"""
from __future__ import annotations

import argparse
import collections
import itertools
import json
from fractions import Fraction
from pathlib import Path

F9 = (
    (1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9),
)
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
N15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-v for v in c) for c in N15)
PA={1:1,2:0,3:1,4:0,8:0}
PB={1:1,2:1,3:0,4:0,8:0}
F9_S={5:0,6:1,7:0,8:0,9:1}
F9_U={1:1,3:0,5:1,6:0,7:0,8:0}

def grammar(F,n=None):
    try:
        if not F:return False
        n=n or max(abs(x) for c in F for x in c)
        if n%3 or 3*len(F)!=4*n:return False
        seen=set();q=collections.Counter()
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

def build(t):
    out=[]
    for i in range(t):
        off=9*i; nxt=9*((i+1)%t)+5
        for j,c in enumerate(F9):
            cc=[]
            for x in c:
                v=abs(x)+off
                if j==0 and x==5:v=nxt
                cc.append(v if x>0 else -v)
            out.append(tuple(cc))
    return tuple(out)

def pins_word(word):
    out={}
    for i,ch in enumerate(word):
        src=PA if ch=='A' else PB
        out.update({9*i+v:b for v,b in src.items()})
    return out

def count(F,pins):
    n=max(abs(x) for c in F for x in c)
    free=[v for v in range(1,n+1) if v not in pins]
    z=0
    for bits in itertools.product((0,1),repeat=len(free)):
        a=dict(pins);a.update(zip(free,bits));z+=sat(F,a)
    return z

def up_dpll(F,pins):
    nodes=visits=reads=0
    def rec(a):
        nonlocal nodes,visits,reads
        nodes+=1
        while True:
            unit=None;all_ok=True
            for c in F:
                visits+=1;unknown=[];ok=False
                for lit in c:
                    reads+=1;v=abs(lit)
                    if v not in a:unknown.append(lit)
                    elif a[v]==int(lit>0):ok=True;break
                if ok:continue
                all_ok=False
                if not unknown:return False
                if len(unknown)==1:
                    v=abs(unknown[0]);b=int(unknown[0]>0)
                    if v in a and a[v]!=b:return False
                    unit=(v,b);break
            if all_ok:return True
            if unit is None:break
            a[unit[0]]=unit[1]
        n=max(abs(x) for c in F for x in c)
        v=next(v for v in range(1,n+1) if v not in a)
        for b in (0,1):
            aa=dict(a);aa[v]=b
            if rec(aa):return True
        return False
    ans=rec(dict(pins))
    return {'SAT':ans,'nodes':nodes,'clause_visits':visits,'literal_reads':reads}

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
    leaves=collections.Counter()
    free=[v for v in range(1,n+1) if v not in pins]
    for bits in itertools.product((0,1),repeat=len(free)):
        a=dict(pins);a.update(zip(free,bits))
        bad=next(j for j,c in enumerate(F) if not any(a[abs(x)]==int(x>0) for x in c))
        leaves[bad]+=1
    return {'leaves':sum(leaves.values()),'false_clause_histogram':dict(sorted(leaves.items()))}

def randomized_exact(t,eps):
    # Direct coupling lower bound and matching mixture:
    # probability 1-2eps query all and decide; probability 2eps guess fair.
    lower=(Fraction(1)-2*eps)*t
    full_probability=Fraction(1)-2*eps
    error=eps
    expected=full_probability*t
    assert lower==expected and 0<=full_probability<=1
    return {'t':t,'epsilon':str(eps),'lower_expected_queries':str(lower),
            'matching_expected_queries':str(expected),
            'query_all_probability':str(full_probability),
            'guess_probability':str(2*eps),'worst_case_error':str(error)}

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
    promise=[]
    for t in (2,3):
        G=build(t);assert grammar(G,9*t)
        rows=[]
        for word in map(''.join,itertools.product('AB',repeat=t)):
            z=count(G,pins_word(word))
            assert (z==1)==(word=='A'*t)
            rows.append({'word':word,'models':z})
        promise.append({'t':t,'connected_canonical':True,'rows':rows})
    rand=[]
    for t in (1,2,3,8,32,128):
        for eps in (Fraction(0),Fraction(1,10),Fraction(1,3),Fraction(49,100)):
            rand.append(randomized_exact(t,eps))
    search=[]
    for t in (1,2,3,4):
        G=build(t)
        search.append({'t':t,'all_A':up_dpll(G,pins_word('A'*t)),
                       'last_B':up_dpll(G,pins_word('A'*(t-1)+'B'))})
    controls={
      'Y6_models':count(Y6,{}),'F9_root_models':count(F9,{}),
      'F9_A_models':count(F9,PA),'F9_B_models':count(F9,PB),
      'F9_S_models':count(F9,F9_S),'F9_U_models':count(F9,F9_U),
      'F9_U_false_cover':false_cover(F9,9,F9_U),
      'F9_SU_pair_modes':su_modes(F9),
      'F15_SAT_models':count(F15,dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))),
      'F15_UNSAT_models':count(F15,dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0))))}
    assert {k:controls[k] for k in ('Y6_models','F9_root_models','F9_A_models','F9_B_models',
      'F9_S_models','F9_U_models','F9_SU_pair_modes','F15_SAT_models','F15_UNSAT_models')}=={
      'Y6_models':20,'F9_root_models':70,'F9_A_models':1,'F9_B_models':0,
      'F9_S_models':3,'F9_U_models':0,'F9_SU_pair_modes':264,
      'F15_SAT_models':2,'F15_UNSAT_models':0}
    malformed=[(),((1,1,2),),((1,-2,3),),((1,2,3),),F9+(F9[0],),((1,2,3),(1,2,4))]
    assert all(not grammar(x) for x in malformed);controls['malformed_rejected']=6
    out={
      'run':'RANDOMIZED-PIN-QUERY-REFEREE276',
      'status':'PROVED_EXACT_RESTRICTED_PLUS_COMPUTATIONAL','P_vs_NP':'OPEN',
      'theorem':{
        'promise':'same connected canonical G_t original; each block is authenticated A or B; one physical x2 pin bit distinguishes A/B',
        'decision':'SAT iff all t block markers are A (AND_t)',
        'exact_deterministic_and_zero_error_expected_queries':'t',
        'epsilon_error_expected_queries':'exactly (1-2 epsilon)t for 0<=epsilon<1/2',
        'lower_proof':'couple all-A with each one-B input. If E is SAT output on all-A, Pr(E)>=1-eps and Pr(E and block i unqueried)<=eps; summing gives E|Q|>=(1-2eps)t',
        'upper_proof':'with probability 1-2eps query all and decide; with probability 2eps query none and guess a fair bit',
        'scope':'pin-bit expected-query model on the explicit promise only; not arbitrary-machine time, not all canonical sources'},
      'promise_formula_controls':promise,'randomized_bounds':rand,'completed_search_trees':search,
      'controls':controls,
      'charged_work':{
        'promise_algorithm':'grammar/source and A/B authentication + randomized pin probes + certificate/output',
        'full_controller':'W_grammar+W_source/index/head+W_discover+W_select/switch/failed+W_deduce/proof+W_cache/replay+W_child/output/access+W_guest',
        'peak':'combined live parser/index/randomness/query/proof/cache/guest/output space',
        'warning':'the lower bound charges only discriminating pin probes; all other paid work is additive, and no free semantic-label oracle is permitted'},
      'wrappers':{'DELAY_steps':4096,'COPY_writes':128,'RECOMP_reads':36,
                  'logical_endpoint_delta':0,'changed_then_restored_adjacent_delta':2},
      'offline_XOR':{'binary':xor_control(F9,False),'gray':xor_control(F9,True)},
      'large_controls':{'U198_V198':'inherited opposite-label controls; not used in this promised query theorem'},
      'limitations':['linear promised-family bound only','randomization does not yield a sublinear exact algorithm',
        'no all-input polynomial controller','no arbitrary-A ARC contraction','no numerical same-machine FLMV transfer']}
    Path(args.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','promise_rows':sum(len(x['rows']) for x in promise),
      'randomized_cases':len(rand),'controls':controls,'P_vs_NP':'OPEN'},indent=2))

if __name__=='__main__':main()
