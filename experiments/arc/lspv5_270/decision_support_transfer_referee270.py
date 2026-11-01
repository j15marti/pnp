#!/usr/bin/env python3
"""Decision-only red team for the connected G_t pin family.

This is a restricted exact theorem/checker, not an all-input SAT solver and
not a native FLMV trace.  It imports no project producer.  Logical XOR is an
offline diagnostic only.
"""
from __future__ import annotations

import argparse
import collections
import itertools
import json
import math
from pathlib import Path

F9 = (
    (1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9),
)
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
N15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-v for v in c) for c in N15)
ELIGIBLE=(2,3,4,6,7,8,9)
PA={1:1,2:0,3:1,4:0,8:0}
PB={1:1,2:1,3:0,4:0,8:0}
PAIR_COVER_WITNESSES=(
    "001101001","011001101","100000111",
    "101100010","110001010","110100100",
)

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
        off=9*i;next5=9*((i+1)%t)+5
        for j,c in enumerate(F9):
            cc=[]
            for x in c:
                v=abs(x)+off
                if j==0 and x==5:v=next5
                cc.append(v if x>0 else -v)
            out.append(tuple(cc))
    return tuple(out)

def local_matrix(pins):
    M=[[0,0],[0,0]]
    for left,right in itertools.product((0,1),repeat=2):
        free=[v for v in range(1,10) if v not in pins and v!=5]
        for bits in itertools.product((0,1),repeat=len(free)):
            a=dict(pins);a.update(zip(free,bits));a[5]=left
            ok=True
            for j,c in enumerate(F9):
                if not any((right if j==0 and x==5 else a[abs(x)])==int(x>0) for x in c):
                    ok=False;break
            M[left][right]+=ok
    return M

def int_mul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in (0,1)) for j in (0,1)] for i in (0,1)]

def bool_mul(A,B):
    return tuple(int(any(A[2*i+k] and B[2*k+j] for k in (0,1))) for i in (0,1) for j in (0,1))

def support(M):return tuple(int(M[i][j]>0) for i in (0,1) for j in (0,1))
IDENT=(1,0,0,1)
def btrace(A):return bool(A[0] or A[3])
def itrace(A):return A[0][0]+A[1][1]

def direct_count(F,pins):
    n=max(abs(x) for c in F for x in c);free=[v for v in range(1,n+1) if v not in pins]
    z=0
    for bits in itertools.product((0,1),repeat=len(free)):
        a=dict(pins);a.update(zip(free,bits));z+=sat(F,a)
    return z

def states84():
    out=[]
    for names in itertools.combinations(ELIGIBLE,2):
        for vals in itertools.product((0,1),repeat=2):
            p=dict(zip(names,vals));M=local_matrix(p)
            out.append({'names':names,'values':vals,'pins':p,'matrix':M,'support':support(M)})
    assert len(out)==84
    return out

def product_distribution(local_support_counts,t):
    dist={IDENT:1}
    for _ in range(t):
        nxt=collections.Counter()
        for A,ca in dist.items():
            for B,cb in local_support_counts.items():nxt[bool_mul(A,B)]+=ca*cb
        dist=dict(nxt)
    return dist

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

def xor_control(F,gray):
    n=max(abs(x) for c in F for x in c);states=[]
    for z in range(1<<n):
        z=z^(z>>1) if gray else z;a={v:(z>>(v-1))&1 for v in range(1,n+1)}
        bits=[a[v] for v in range(1,n+1)]
        for c in F:
            q=sum(a[abs(x)]==int(x>0) for x in c);bits.extend((q&1,(q>>1)&1))
        states.append(bits)
    ds=[sum(x!=y for x,y in zip(a,b)) for a,b in zip(states,states[1:])]
    return {'steps':len(ds),'sum_adjacent_d_logic':sum(ds),'endpoint_d_logic':sum(x!=y for x,y in zip(states[0],states[-1]))}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
    S=states84();counts=collections.Counter(x['support'] for x in S)
    cover=[]
    for bits in PAIR_COVER_WITNESSES:
        a={i+1:int(b) for i,b in enumerate(bits)}
        assert a[5]==0 and sat(F9,a);cover.append(a)
    assert all(any(a[u]==x and a[v]==y for a in cover)
               for u,v in itertools.combinations(ELIGIBLE,2)
               for x,y in itertools.product((0,1),repeat=2))
    # All 84 one-block states: relation support agrees with direct original enumeration.
    for x in S:
        assert btrace(x['support'])==(direct_count(F9,x['pins'])>0)
    # Deterministic cross-checks on two-block sources against integer transfer counts.
    for i,j in ((0,0),(0,83),(7,31),(20,62),(41,82),(83,83)):
        A,B=S[i],S[j]
        p={**A['pins'],**{9+v:b for v,b in B['pins'].items()}}
        M=int_mul(A['matrix'],B['matrix'])
        assert (itrace(M)>0)==btrace(bool_mul(A['support'],B['support']))
        assert direct_count(build(2),p)==itrace(M)
    family=[]
    for t in (1,2,4,8,16,128):
        d=product_distribution(counts,t);total=sum(d.values());yes=sum(v for k,v in d.items() if btrace(k))
        assert total==84**t
        family.append({'t':t,'syntactic_states':str(total),'reachable_product_relations':len(d),
                       'SAT_states':str(yes),'UNSAT_states':str(total-yes)})
    WA=local_matrix(PA);WB=local_matrix(PB)
    assert WA==[[1,1],[0,0]] and WB==[[0,0],[0,0]]
    promise=[]
    for t in (1,2,3,4,8,16,128):
        regions=[{2*i,2*i+1} for i in range(t)]
        witness={2*i for i in range(t)}
        assert all(witness&r for r in regions)
        if t<=8:
            assert not any(all(set(c)&r for r in regions) for q in range(t) for c in itertools.combinations(range(2*t),q))
        promise.append({'t':t,'opposite_inputs':t,'disjoint_difference_regions':t,
                        'minimum_SAT_input_pin_queries':t,'matching_scan_queries':t,
                        'SAT_certificate_bits':t,'UNSAT_certificate_bits':1})
    controls={
      'Y6_models':direct_count(Y6,{}),'F9_root_models':direct_count(F9,{}),
      'F9_A_models':direct_count(F9,PA),'F9_B_models':direct_count(F9,PB),
      'F9_SU_pair_modes':su_modes(F9),
      'F15_SAT_models':direct_count(F15,dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))),
      'F15_UNSAT_models':direct_count(F15,dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0))))}
    assert controls=={'Y6_models':20,'F9_root_models':70,'F9_A_models':1,'F9_B_models':0,
                      'F9_SU_pair_modes':264,'F15_SAT_models':2,'F15_UNSAT_models':0}
    malformed=[(),((1,1,2),),((1,-2,3),),((1,2,3),),F9+(F9[0],),((1,2,3),(1,2,4))]
    assert all(not grammar(x) for x in malformed)
    controls['malformed_rejected']=6
    out={
      'run':'DECISION_SUPPORT_TRANSFER_REFEREE270','status':'PROVED_EXACT_RESTRICTED_PLUS_COMPUTATIONAL',
      'P_vs_NP':'OPEN','local_syntactic_states':84,'distinct_integer_matrices':len({tuple(sum(x['matrix'],[])) for x in S}),
      'distinct_boolean_relations':len(counts),'relation_multiplicities':{''.join(map(str,k)):v for k,v in sorted(counts.items())},
      'six_explicit_pair_cover_witnesses':list(PAIR_COVER_WITNESSES),
      'family_distribution':family,'AB_promise':promise,'WA':WA,'WB':WB,'controls':controls,
      'theorem':{
        'decision':'SAT iff Boolean product of authenticated local 2x2 support relations has nonzero trace',
        'per_instance_work':'O(N_source+t) authentication plus one constant-table lookup and Boolean 2x2 multiply per block',
        'peak_live_space':'O(log N) index/counter plus 4 relation bits and parser/proof state; no lossless pin history',
        'query_tightness':'A/B subpromise is AND_t, so exact deterministic SAT-input pin-query complexity is t and is attained',
        'scope':'recognized connected G_t source and declared coherent pin grammar only'},
      'equivalence_firewall':{
        'CUBEKEY_current_decision_classes':1,'AB_current_decision_classes':2,
        'local_continuation_relation_universe':16,
        'lossless_syntactic_states':"84^t",
        'warning':'class existence is not free acquisition; outside this recognized family no all-input quotient-width theorem is known'},
      'charged_recurrence':'W=grammar+source/index/head+discover+lookup+compose+certificate/output+failed policies+guest; exact fallback remains exponential outside the promise',
      'wrappers':{'DELAY_steps':4096,'DELAY_logical_delta':0,'COPY_and_RECOMP':'charged despite no decision-state change'},
      'offline_XOR':{'binary':xor_control(F9,False),'gray':xor_control(F9,True)},
      'large_controls':{'U198':'inherited independently replayed UNSAT certificate; not used in theorem',
                        'V198':'inherited independently replayed 198-bit witness; not used in theorem'},
      'limitations':['no all-input polynomial controller','no arbitrary-decider superlinear lower bound',
                     'no power-short hereditary A->Phi(A)','no numerical same-machine FLMV transfer']}
    Path(args.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','local_relations':len(counts),'integer_matrices':out['distinct_integer_matrices'],
                      'controls':controls,'P_vs_NP':'OPEN'},indent=2))

if __name__=='__main__':main()
