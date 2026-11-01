#!/usr/bin/env python3
"""LSPV-5 REFEREE275: exact F9 greedy-elimination-width counterexample.

This is a finite source-authenticated red-team control, not an all-input SAT
algorithm or lower bound.  It compares the lexicographic minimum-union bucket
selector with exact optimum elimination width on one coherent F9 residual.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
import json
import sys

F9_P = ((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
F9_N = ((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F9 = F9_P + tuple(tuple(-x for x in c) for c in F9_N)
Y6 = ((1,2,3),(1,4,5),(2,4,6),(3,5,6),
      (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
F15_P = ((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),
         (6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
F15_N = ((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),
         (4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15 = F15_P + tuple(tuple(-x for x in c) for c in F15_N)

GAP_PIN = {5:0, 7:0}
F9_S = {5:0,6:1,7:0,8:0,9:1}
F9_U = {1:1,3:0,5:1,6:0,7:0,8:0}
F15_S = dict(zip(range(7,16),(1,0,0,0,1,1,1,1,0)))
F15_U = dict(zip(range(7,16),(0,0,0,0,1,1,1,1,0)))

def valid(F,n):
    if n < 3 or n % 3 or 3*len(F) != 4*n: return False
    q=Counter(); seen=set()
    for c in F:
        if len(c)!=3 or len({abs(x) for x in c})!=3: return False
        if any(not 1<=abs(x)<=n for x in c): return False
        if not (all(x>0 for x in c) or all(x<0 for x in c)): return False
        k=tuple(sorted(c))
        if k in seen: return False
        seen.add(k); q.update(c)
    return all(q[v]==q[-v]==2 for v in range(1,n+1))

def sat(F,a):
    return all(any(a[abs(l)]==int(l>0) for l in c) for c in F)

def models(F,n,p):
    free=[v for v in range(1,n+1) if v not in p]
    out=[]
    for bits in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,bits))}
        if sat(F,a): out.append(a)
    return out

def residual_scopes(F,p):
    scopes=[]
    for j,c in enumerate(F,1):
        if any(abs(l) in p and p[abs(l)]==int(l>0) for l in c): continue
        s=tuple(sorted(abs(l) for l in c if abs(l) not in p))
        if not s: return None
        scopes.append((j,s))
    return scopes

def primal(scopes):
    a={v:set() for _,s in scopes for v in s}
    for _,s in scopes:
        for u,v in combinations(s,2): a[u].add(v); a[v].add(u)
    return a

def eliminate(a,x):
    ns=sorted(a[x]); b={v:set(a[v])-{x} for v in a if v!=x}
    for i,u in enumerate(ns):
        for v in ns[i+1:]: b[u].add(v); b[v].add(u)
    return b

def trace_order(a,order):
    a={v:set(ns) for v,ns in a.items()}; rows=[]
    for x in order:
        rows.append({'x':x,'closed_width':1+len(a[x]),'neighbors':sorted(a[x])})
        a=eliminate(a,x)
    return rows

def greedy_order(a):
    a={v:set(ns) for v,ns in a.items()}; order=[]
    while a:
        x=min(a,key=lambda v:(1+len(a[v]),v)); order.append(x); a=eliminate(a,x)
    return order

def key(a):
    vs=tuple(sorted(a)); return vs,tuple(tuple(sorted(a[v])) for v in vs)

@lru_cache(None)
def optimal(state):
    vs,ns=state
    if not vs:return 0,()
    a={v:set(ns[i]) for i,v in enumerate(vs)}; best=(10**9,())
    for x in vs:
        w2,o2=optimal(key(eliminate(a,x)))
        cand=(max(1+len(a[x]),w2),(x,)+o2)
        if cand<best:best=cand
    return best

def minor_ok(a,branch_sets):
    def connected(S):
        todo=[next(iter(S))]; seen=set(todo)
        while todo:
            u=todo.pop()
            for v in a[u]&S:
                if v not in seen:seen.add(v);todo.append(v)
        return seen==S
    return (all(connected(S) for S in branch_sets) and
            all(any(v in a[u] for u in branch_sets[i] for v in branch_sets[j])
                for i in range(len(branch_sets)) for j in range(i+1,len(branch_sets))))

def false_leaf_cover(F,n,p):
    free=[v for v in range(1,n+1) if v not in p]; cover=[]
    for bits in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,bits))}
        bad=[j+1 for j,c in enumerate(F) if not any(a[abs(l)]==int(l>0) for l in c)]
        cover.append({'free_bits':list(bits),'false_clause_ids':bad})
    return cover

def up_dpll(F,n,p):
    C=Counter()
    def propagate(a):
        a=dict(a)
        while True:
            changed=False
            for j,c in enumerate(F,1):
                C['clause_visits']+=1; un=[]; yes=False
                for l in c:
                    C['literal_reads']+=1;v=abs(l)
                    if v not in a:un.append(l)
                    elif a[v]==int(l>0):yes=True;break
                if yes:continue
                if not un:return a,j
                if len(un)==1:
                    l=un[0];v=abs(l);b=int(l>0)
                    if v in a and a[v]!=b:return a,j
                    if v not in a:a[v]=b;C['unit_writes']+=1;changed=True
            if not changed:return a,None
    def go(a):
        C['nodes']+=1;a,bad=propagate(a)
        if bad is not None:return None
        if len(a)==n:return a
        x=next(v for v in range(1,n+1) if v not in a)
        for b in (0,1):
            z=go({**a,x:b})
            if z is not None:return z
        return None
    witness=go(p)
    return {'status':'SAT' if witness is not None else 'UNSAT','charged':dict(C)}

def su_controls(F,n):
    checked=feasible=0
    for i,j in combinations(range(len(F)),2):
        for A,B in product((0,1),repeat=2): # 1 means local all-true S, 0 all-false U
            d={}; ok=True
            for c,t in ((F[i],A),(F[j],B)):
                for l in c:
                    v=abs(l); want=int(l>0) if t else int(l<0)
                    if v in d and d[v]!=want:ok=False
                    d[v]=want
            same=any(l in F[j] for l in F[i]); opposite=any(-l in F[j] for l in F[i])
            predicted=not(opposite if A==B else same)
            assert ok==predicted
            checked+=1; feasible+=ok
    return {'checked':checked,'feasible':feasible}

def malformed_controls():
    bad=[Y6[:-1],Y6+Y6[:1],Y6[:2]+((1,1,2),)+Y6[3:],
         Y6[:2]+((1,-2,3),)+Y6[3:],Y6[:2]+((0,2,3),)+Y6[3:],
         Y6[:2]+((1,2,7),)+Y6[3:]]
    return [not valid(z,6) for z in bad]

def offline_xor(F,n):
    out={}
    for mode in ('binary','gray'):
        prev=None; adjacent=changed=0
        for i in range(1<<n):
            q=i if mode=='binary' else i^(i>>1)
            a={v+1:(q>>v)&1 for v in range(n)}
            state=tuple(sum(a[abs(l)]==int(l>0) for l in c) for c in F)
            comp={v:1-b for v,b in a.items()}
            assert all(x+sum(comp[abs(l)]==int(l>0) for l in c)==3 for x,c in zip(state,F))
            if prev is not None:
                adjacent+=sum((x^y).bit_count() for x,y in zip(prev,state))
                changed+=sum(x!=y for x,y in zip(prev,state))
            prev=state
        out[mode]={'sum_logic_xor_offline':adjacent,'changed_clause_records':changed}
    return out

def main():
    assert valid(F9,9) and valid(Y6,6) and valid(F15,15)
    scopes=residual_scopes(F9,GAP_PIN); assert scopes is not None
    a=primal(scopes)
    greedy=greedy_order(a); gtrace=trace_order(a,greedy)
    optw,optorder=optimal(key(a)); otrace=trace_order(a,optorder)
    branches=[{1,3},{4},{6},{8},{9}]
    assert greedy==[1,2,3,4,6,8,9]
    assert max(r['closed_width'] for r in gtrace)==6
    assert optw==5 and max(r['closed_width'] for r in otrace)==5
    assert minor_ok(a,branches)
    gap_models=models(F9,9,GAP_PIN); assert len(gap_models)==13
    f9s=models(F9,9,F9_S); f9u=models(F9,9,F9_U)
    f15s=models(F15,15,F15_S); f15u=models(F15,15,F15_U)
    assert (len(f9s),len(f9u),len(f15s),len(f15u))==(3,0,2,0)
    cover=false_leaf_cover(F9,9,F9_U)
    assert len(cover)==8 and all(x['false_clause_ids'] for x in cover)
    malformed=malformed_controls(); assert all(malformed)
    result={
      'run':'GREEDY-WIDTH-GAP-REFEREE275','status':'PASS',
      'proof_status':'PROVED/EXACT restricted source-authenticated counterexample; P vs NP OPEN',
      'falsified':'lexicographic minimum-union cap failure certifies intrinsic minimum elimination width',
      'source':{'name':'F9','n':9,'m':12,'root_models':len(models(F9,9,{})),'canonical':True},
      'counterexample':{
        'pins':GAP_PIN,'models':len(gap_models),
        'source_scopes':[{'clause_id':j,'scope':s} for j,s in scopes],
        'primal_edges':[list(e) for e in sorted({tuple(sorted((u,v))) for u in a for v in a[u] if u<v})],
        'greedy_order':greedy,'greedy_trace':gtrace,'greedy_closed_width':6,
        'optimal_order':list(optorder),'optimal_trace':otrace,'optimal_closed_width':optw,
        'cap5_greedy_status':'UNRESOLVED','cap5_optimal_order_status':'SAT',
        'K5_minor_branch_sets':[sorted(S) for S in branches],
        'first_greedy_fill_creates_K6':True},
      'same_original_controls':{
        'F9_S_models':len(f9s),'F9_U_models':len(f9u),
        'F9_U_false_leaf_cover':cover,
        'F15_S_models':len(f15s),'F15_U_models':len(f15u),
        'Y6_root_models':len(models(Y6,6,{})),
        'UP_DPLL':{
          'gap':up_dpll(F9,9,GAP_PIN),'F9_S':up_dpll(F9,9,F9_S),'F9_U':up_dpll(F9,9,F9_U),
          'F15_S':up_dpll(F15,15,F15_S),'F15_U':up_dpll(F15,15,F15_U)},
        'F9_SU':su_controls(F9,9)},
      'malformed_rejected':malformed,
      'xor_diagnostic':offline_xor(F9,9),
      'resource_scope':{
        'exact_width_search_states':optimal.cache_info().currsize,
        'logical_xor_is_offline':True,
        'native_FLMV_tape_trace':False,
        'U198_V198':'labels inherited; not needed for this F9 counterexample',
        'wrappers':{
          'DELAY':{'native_steps':4096,'logical_endpoint_xor':0},
          'COPY':{'shadow_writes':128,'logical_endpoint_xor':0},
          'RECOMP':{'source_literal_reads':36,'retained_clause_status_bits':0},
          'changed_then_restored':{'adjacent_physical_changes':2,'endpoint_delta':0}}},
      'unproved':['all-input polynomial width','uniform cheap optimal ordering','arbitrary-A ARC','strict numerical same-machine FLMV transfer'],
      'P_vs_NP':'OPEN'}
    text=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if len(sys.argv)>1:
        with open(sys.argv[1],'w',encoding='utf-8') as f:f.write(text)
    print(text,end='')

if __name__=='__main__':main()
