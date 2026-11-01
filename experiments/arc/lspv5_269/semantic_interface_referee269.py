#!/usr/bin/env python3
"""Independent referee for CONNECTED-TRANSFER-MATRIX305.

This is a finite/restricted exact experiment, not an all-input SAT solver and
not a native FLMV machine trace.  It imports no project producer.  Logical XOR
is computed only as an offline diagnostic.
"""
from __future__ import annotations

import argparse
import collections
import itertools
import json
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

def grammar(F,n=None):
    try:
        if not F:return False
        n=n or max(abs(x) for c in F for x in c)
        if n%3 or 3*len(F)!=4*n:return False
        keys=set();q=collections.Counter()
        for c in F:
            if len(c)!=3 or len({abs(x) for x in c})!=3:return False
            if not (all(x>0 for x in c) or all(x<0 for x in c)):return False
            if any(abs(x)<1 or abs(x)>n for x in c):return False
            k=tuple(sorted(c))
            if k in keys:return False
            keys.add(k);q.update(c)
        return all(q[v]==q[-v]==2 for v in range(1,n+1))
    except Exception:return False

def sat(F,a):return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)

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

def connected(F,n):
    g=[set() for _ in range(n+1)]
    for c in F:
        vs=list(map(abs,c))
        for u in vs:
            g[u].update(v for v in vs if v!=u)
    seen={1};stack=[1]
    while stack:
        for v in g[stack.pop()]:
            if v not in seen:seen.add(v);stack.append(v)
    return len(seen)==n

def local_matrix(pins):
    W=[[0,0],[0,0]];leaf=[]
    for a,b in itertools.product((0,1),repeat=2):
        free=[v for v in range(1,10) if v not in pins and v!=5]
        for bits in itertools.product((0,1),repeat=len(free)):
            d=dict(pins);d.update(zip(free,bits));d[5]=a
            bad=[]
            for j,c in enumerate(F9):
                ok=False
                for x in c:
                    val=b if j==0 and x==5 else d[abs(x)]
                    if val==int(x>0):ok=True;break
                if not ok:bad.append(j)
            if not bad:W[a][b]+=1
            leaf.append({'boundary':[a,b],'internal':list(bits),'bad_clause_ids':bad})
    return W,leaf

def mm(A,B):return [[sum(A[i][k]*B[k][j] for k in (0,1)) for j in (0,1)] for i in (0,1)]
def mpow(A,t):
    R=[[1,0],[0,1]]
    while t:
        if t&1:R=mm(R,A)
        A=mm(A,A);t//=2
    return R
def trace(A):return A[0][0]+A[1][1]

def direct_count(F,pins):
    n=max(abs(x) for c in F for x in c);free=[v for v in range(1,n+1) if v not in pins];models=[]
    for bits in itertools.product((0,1),repeat=len(free)):
        a=dict(pins);a.update(zip(free,bits))
        if sat(F,a):models.append([a[v] for v in range(1,n+1)])
    return models

def block_pins(t,bad_first=False):
    d={}
    for i in range(t):
        p=PB if bad_first and i==0 else PA
        d.update({9*i+v:b for v,b in p.items()})
    return d

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
            vals=(AS and BS,AS and BU,AU and BS,AU and BU)
            act=[u or v for u,v in zip(act,vals)]
        assert tuple(act)==pred;checks+=4
    return checks

def logical_state(F,z):
    n=max(abs(x) for c in F for x in c);a={v:(z>>(v-1))&1 for v in range(1,n+1)}
    bits=[a[v] for v in range(1,n+1)]
    for c in F:
        q=sum(a[abs(x)]==int(x>0) for x in c);bits.extend((q&1,(q>>1)&1))
    return bits
def xor_path(F,gray):
    n=max(abs(x) for c in F for x in c);states=[]
    for z in range(1<<n):
        q=z^(z>>1) if gray else z;states.append(logical_state(F,q))
    ds=[sum(x!=y for x,y in zip(a,b)) for a,b in zip(states,states[1:])]
    return {'sum_adjacent_d_logic':sum(ds),'endpoint_d_logic':sum(x!=y for x,y in zip(states[0],states[-1])),'steps':len(ds)}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
    W,all_leaves=local_matrix({});WA,la=local_matrix(PA);WB,lb=local_matrix(PB)
    assert W==[[34,47],[23,36]] and WA==[[1,1],[0,0]] and WB==[[0,0],[0,0]]
    assert [trace(mpow(W,t)) for t in range(1,5)]==[70,4614,312970,21248098]
    leaf32=[x for x in lb if len(x['internal'])==3]
    assert len(leaf32)==32 and all(x['bad_clause_ids'] for x in leaf32)
    fam=[]
    for t in (1,2,3,4,8,16,64,128):
        G=build(t);assert grammar(G,9*t) and connected(G,9*t)
        row={'t':t,'n':9*t,'m':12*t,'trace_count':trace(mpow(W,t)),'grammar':True,'connected':True}
        if t<=2:row['direct_root_count']=len(direct_count(G,{}));assert row['direct_root_count']==row['trace_count']
        if t<=3:
            p=direct_count(G,block_pins(t));q=direct_count(G,block_pins(t,True))
            assert len(p)==1 and len(q)==0;row.update(P_models=1,Q_models=0,P_witness=p[0])
        fam.append(row)
    controls={}
    controls['Y6_models']=len(direct_count(Y6,{}));assert controls['Y6_models']==20
    f9_sat=direct_count(F9,{1:0,2:0,8:1,9:1});assert len(f9_sat)==2
    f9_unsat=direct_count(F9,{8:0,3:0,7:0,6:0,1:1,5:1});assert not f9_unsat
    controls.update(F9_SAT_models=2,F9_parity_only_UNSAT_models=0)
    f15s=direct_count(F15,dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0))))
    f15u=direct_count(F15,dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0))))
    assert len(f15s)==2 and not f15u;controls.update(F15_SAT_models=2,F15_UNSAT_models=0)
    malformed=[(),((1,1,2),),((1,-2,3),),((1,2,3),),F9+(F9[0],),((1,2,3),(1,2,4))]
    assert all(not grammar(x) for x in malformed);controls['malformed_rejected']=len(malformed)
    controls['F9_SU_pair_modes']=su_modes(F9);assert controls['F9_SU_pair_modes']==264
    out={
      'run':'SEMANTIC_INTERFACE_TRANSFER_REFEREE269','status':'PROVED_RESTRICTED_PLUS_COMPUTATIONAL',
      'P_vs_NP':'OPEN','matrix':W,'matrix_PA':WA,'matrix_PB':WB,'family':fam,
      'Q_local_complete_UNSAT_cover':leaf32,'controls':controls,
      'semantic_cache_firewall':{'coarse_signature_collision':True,'exact_matrices_differ':WA!=WB,
        'sound_key_requires':'authenticated exact boundary relation/count matrix plus source/proof/output provenance'},
      'charged_recurrence':{
        'formula':'C_validate+C_discover+C_acquire+C_cert+sum_i C_local(i,2^(2b))+O(t*2^(3b)*M(L))+C_output',
        'peak':'simultaneous source/index/head/decomposition/matrix/proof/cache/guest/output workspace',
        'polynomial_condition':'paid certified b=O(log N) decomposition and polynomial local relation acquisition',
        'all_input_condition_proved':False},
      'wrappers':{'DELAY_steps':4096,'DELAY_logical_delta':0,'COPY_bits':len(F9)*3*4,'RECOMP_source_literal_reads':len(F9)*3,
        'claim':'charged work may occur at zero logical XOR; logical XOR is offline only'},
      'offline_XOR':{'binary':xor_path(F9,False),'gray':xor_path(F9,True)},
      'limitations':['recognized cyclic family only','no all-input interface-width/acquisition bound','no arbitrary A->Phi(A)','no numerical same-machine FLMV transfer']}
    Path(args.out).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','W':W,'WA':WA,'WB':WB,'family_cases':len(fam),'controls':controls,'P_vs_NP':'OPEN'},indent=2))

if __name__=='__main__':main()
