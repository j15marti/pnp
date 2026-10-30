#!/usr/bin/env python3
"""CONNECTED-AND-CONNECTOR231: exact22 two-core conjunction and audit.
Python >=3.10, standard library only. No solver, answer advice, or package import.
Theorems are in accompanying TeX; finite tables independently enumerated here.
Usage: python 2026-10-29_1322_LSPV-2_CONNECTED_AND_CONNECTOR231_repro.py > results.json
"""
from collections import Counter, defaultdict
from itertools import product
import hashlib
import json
import random
import sys

# W1 original source, index 0..19, as supplied in Polynomial_Coverage_Proof_Study.
W1=[
(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
G=[tuple(-l if i in (6,11) and abs(l)==4 else l for l in c)
   for i,c in enumerate(W1)]
D=4  # G[D] = (-p, -g9, -g11), p=g4
E=6  # G[E] = (-p, -g8, -g11)
assert G[D]==(-4,-9,-11) and G[E]==(-4,-8,-11)


def eval_clause(c,mask):
    return any(((mask>>(abs(l)-1))&1)==int(l>0) for l in c)


def validate(cs,require_connected=True):
    vs={abs(l) for c in cs for l in c};occ=Counter(l for c in cs for l in c)
    assert vs and vs==set(range(1,max(vs)+1)),('dense',len(vs))
    assert len(cs)==len(set(tuple(sorted(c)) for c in cs)),'duplicate clause'
    assert all(len(c)==3 and len({abs(l) for l in c})==3 for c in cs)
    assert all(occ[v]==occ[-v]==2 for v in vs),'signed quotas'
    assert 3*len(cs)==4*len(vs)
    if require_connected:
        seen={('v',1)};stack=[('v',1)]
        byvar=defaultdict(list)
        for i,c in enumerate(cs):
            for l in c:byvar[abs(l)].append(i)
        while stack:
            t,i=stack.pop()
            ns=[('c',j) for j in byvar[i]] if t=='v' else [('v',abs(l)) for l in cs[i]]
            for z in ns:
                if z not in seen:seen.add(z);stack.append(z)
        assert len(seen)==len(vs)+len(cs),('disconnected',len(seen),len(vs)+len(cs))
    return (len(vs),len(cs))


def simple_models(cs,n=None):
    n=n or max(abs(l) for c in cs for l in c)
    for mask in range(1<<n):
        if all(eval_clause(c,mask) for c in cs): yield mask


def local_profile():
    # P(x,A;u,v) for one G with D,E erased and clauses
    # (not x or B), (not p or A), where u=-g8, v=(-p or -g11).
    table={};counter={};witness={}
    good=[]
    for mask in range(1<<15):
        if all(eval_clause(c,mask) for i,c in enumerate(G) if i not in (D,E)):
            good.append(mask)
    for x,A in product((0,1),repeat=2):
        freq=Counter();win={}
        for mask in good:
            p=(mask>>3)&1
            B=int(eval_clause((-9,-11),mask))
            if (not x or B) and (A or not p):
                u=int(eval_clause((-8,),mask))
                v=int(eval_clause((-4,-11),mask))
                freq[(u,v)]+=1;win.setdefault((u,v),mask)
        table[(x,A)]=set(freq)
        counter[f'{x}{A}']={f'{u}{v}':freq[u,v] for u,v in sorted(freq)}
        for k,m in win.items():witness[(x,A,k[0],k[1])]=m
    expected={
      (0,0):{(0,1)},
      (0,1):{(0,0),(0,1),(1,0),(1,1)},
      (1,0):set(),
      (1,1):{(0,0),(1,0),(1,1)}
    }
    assert table==expected,(table,expected)
    # Entire 16-input Boolean gate table, including 7 invalid assignments.
    for x,A,y,B in product((0,1),repeat=4):
        linked=any((v1 or u2) and (v2 or u1)
            for u1,v1 in table[(x,A)] for u2,v2 in table[(y,B)])
        assert linked==bool((not x or A) and (not y or B)),(x,A,y,B)
    # Some v=1 witness exists for every allowed (x,A).
    for p in ((0,0),(0,1),(1,1)):
        assert any(v for u,v in table[p])
    return table,witness,{'enumerated_G_masks':1<<15,'punctured_G_masks':len(good),
                 'profile_counts':counter,'abstract_gate_checks':16,
                 'source_G_models':sum(1 for _ in simple_models(G)),
                 'source_W1_models':sum(1 for _ in simple_models(W1))}


def graph_remaining_G_connected():
    # Incidence edges removed are (p,D), (g8,E).
    vertices=[('v',i) for i in range(1,16)]+[('c',j) for j in range(20)]
    adj={v:[] for v in vertices}
    for j,c in enumerate(G):
        for l in c:
            v=abs(l)
            if (j==D and v==4) or (j==E and v==8):continue
            adj[('v',v)].append(('c',j));adj[('c',j)].append(('v',v))
    seen={vertices[0]};stack=[vertices[0]]
    while stack:
        for y in adj[stack.pop()]:
            if y not in seen:seen.add(y);stack.append(y)
    assert len(seen)==35,(len(seen),len(vertices))
    return len(seen)


def shift_clause(c,delta):return tuple((1 if l>0 else -1)*(abs(l)+delta) for l in c)

def select_slot(cs,mode):
    opts=[(i,s,abs(l)) for i,c in enumerate(cs) for s,l in enumerate(c) if l<0]
    assert opts
    if mode=='first':return opts[0]
    if mode=='last':return opts[-1]
    if isinstance(mode,int):return opts[mode%len(opts)]
    raise ValueError(mode)


def source_A(cs,ci,slot,model):
    return int(any(model[abs(l)]==int(l>0) for j,l in enumerate(cs[ci]) if j!=slot))


def join(H,K,modelH=None,modelK=None,mode='first',witness=None):
    nh,mh=validate(H);nk,mk=validate(K)
    # The result has an exact one-to-one source-variable projection.
    h=list(H);k=[shift_clause(c,nh) for c in K]
    ix,slx,x=select_slot(h,mode)
    iy,sly,y=select_slot(k,mode)
    b1=nh+nk;b2=b1+15
    g1=[shift_clause(c,b1) for c in G]
    g2=[shift_clause(c,b2) for c in G]
    p1=b1+4;p2=b2+4
    # The two source-to-guard negative-literal exchanges.
    h[ix]=tuple(-p1 if j==slx else l for j,l in enumerate(h[ix]))
    k[iy]=tuple(-p2 if j==sly else l for j,l in enumerate(k[iy]))
    g1[D]=tuple(-x if j==0 else l for j,l in enumerate(g1[D]))
    g2[D]=tuple(-y if j==0 else l for j,l in enumerate(g2[D]))
    # The guard-to-guard exchange of one negative occurrence of g8.
    u1=b1+8;u2=b2+8
    g1[E]=tuple(-u2 if j==1 else l for j,l in enumerate(g1[E]))
    g2[E]=tuple(-u1 if j==1 else l for j,l in enumerate(g2[E]))
    out=h+k+g1+g2
    nn,mm=validate(out)
    assert nn==nh+nk+30 and mm==mh+mk+40
    info={'source_sizes':(nh,nk),'source_clause_slots':((ix,slx),(iy,sly)),
          'cross_boundary':(u1,u2),'added_variables':30,'added_clauses':40}
    if modelH is None or modelK is None:return out,None,info
    model={**modelH,**{v+nh:b for v,b in modelK.items()}}
    def attach(src,ix,sl,x,b,mod):
        localx=model[x];A=source_A(src,ix,sl,model)
        assert (not localx or A),(localx,A)
        options=[(u,v) for u,v in ((0,1),(1,1)) if (localx,A,u,v) in witness]
        assert options
        u,v=options[0];mask=witness[(localx,A,u,v)]
        return {b+j:int(bool(mask&(1<<(j-1)))) for j in range(1,16)}
    model.update(attach(H,ix,slx,x,b1,mode))
    model.update(attach(k,iy,sly,y,b2,mode))
    assert all(any(model[abs(l)]==int(l>0) for l in c) for c in out)
    return out,model,info


def var_scope_rank(cs,plusminus='all'):
    basis={}
    for c in cs:
        a=0
        for l in c:
            if plusminus=='all' or (plusminus=='positive' and l>0) or (plusminus=='negative' and l<0):a^=1<<(abs(l)-1)
        while a:
            p=a.bit_length()-1
            if p not in basis:basis[p]=a;break
            a^=basis[p]
    return len(basis)


def bits_dimacs(cs):
    text=f'p cnf {max(abs(l) for c in cs for l in c)} {len(cs)}\n'
    text+=''.join(' '.join(map(str,c))+' 0\n' for c in cs)
    return len(text.encode('ascii'))*8


def connected_components_count(cs):
    seen=set();byvar=defaultdict(set)
    for c in cs:
        names=[abs(l) for l in c]
        for v in names:byvar[v].update(names)
    components=0
    for start in byvar:
        if start in seen:continue
        components+=1;stack=[start];seen.add(start)
        while stack:
            for w in byvar[stack.pop()]:
                if w not in seen:seen.add(w);stack.append(w)
    return components


def renamed(cs,seed):
    # Adversarial name permutation, literal order and clause-order changes.
    n=max(abs(l) for c in cs for l in c);rng=random.Random(seed)
    names=list(range(1,n+1));rng.shuffle(names)
    mp={v:names[v-1] for v in range(1,n+1)}
    out=[]
    for c in cs:
        z=[(1 if l>0 else -1)*mp[abs(l)] for l in c];rng.shuffle(z);out.append(tuple(z))
    rng.shuffle(out);validate(out)
    return out,mp


def walk_corpus():
    table,witness,base=local_profile()
    assert base['source_W1_models']==0 and base['source_G_models']==272
    # Original user-provided hard-for-repair mutation is in an accompanying
    # audit file. Here G is the independently checked SAT source; the provided
    # selected mutation is imported by the optional replayer, not assumed.
    validate(W1);validate(G)
    assert graph_remaining_G_connected()==35
    G_model=next(simple_models(G))
    local_model={i:int(bool(G_model&(1<<(i-1)))) for i in range(1,16)}
    info={'gadget':base,'naked_bridge_graph_connected_vertices':35,'cases':[],
          'input_library_sha':{},'bridge_profiles':{},'seed':20261029}
    # Exhaustive interface to actual 15-variable SAT source G.
    models=list(simple_models(G))
    # Source clause selected by first slot x=1 at clause0 (-1,3,-14).
    sel=select_slot(G,'first');sgn=(sel[0],sel[1]);assert G[sgn[0]][sgn[1]]<0
    inputs=sorted({(((m>>(sel[2]-1))&1), int(any(eval_clause((l,),m) for j,l in enumerate(G[sel[0]]) if j!=sel[1]))) for m in models})
    assert all((not x or a) for x,a in inputs)
    info['source_gate_values_G']=[list(t) for t in inputs]
    prof=set()
    for s1,s2 in product(inputs,repeat=2):
        for u1,v1 in table[s1]:
            for u2,v2 in table[s2]:
                if (v1 or u2) and (v2 or u1):prof.add((u1,u2))
    info['bridge_profiles']['GxG_u_negative_bits']=[list(t) for t in sorted(prof)]
    # Independent W1 UNSAT source and SAT source G, two concrete labels.
    for k in (1,2,4,8,16,32):
        for label in ('SAT','UNSAT'):
            cs=list(G if label=='SAT' else W1)
            model=dict(local_model) if label=='SAT' else None
            join_count=0;last_info=None
            for j in range(1,k):
                # For UNSAT, join W1 with SAT G blocks. No UNSAT models needed.
                cs,model,last_info=join(cs,G,model,local_model,mode=j%3,witness=witness)
                join_count+=1
            n,m=validate(cs)
            assert n==45*k-30 and m==60*k-40
            assert connected_components_count(cs)==1
            if model is not None:assert len(model)==n and all(any(model[abs(l)]==int(l>0) for l in c) for c in cs)
            metrics={'k':k,'label':label,'n':n,'m':m,'component_count':1,
                   'model_verified':model is not None,'source_W1_truth_table_UNSAT':label=='UNSAT',
                   'join_count':join_count,'bit_length':bits_dimacs(cs)}
            if k<=8:
                r=var_scope_rank(cs,'all')
                metrics.update({'GF2_scope_rank':r,'GF2_scope_dependency_excess':m-r,
                    'GF2_positive_rank':var_scope_rank(cs,'positive'),
                    'GF2_negative_rank':var_scope_rank(cs,'negative')})
            info['cases'].append(metrics)
    # Algebraic ranks for base and one bridge have independent controls.
    info['basis']={
        'W1':{'n':15,'m':20,'rank':var_scope_rank(W1),'signed_positive_rank':var_scope_rank(W1,'positive')},
        'G':{'n':15,'m':20,'rank':var_scope_rank(G),'signed_positive_rank':var_scope_rank(G,'positive')},
        'G_JOIN_G':{'n':60,'m':80}}
    return info

if __name__=='__main__':
    result=walk_corpus()
    print(json.dumps(result,sort_keys=True,indent=2))