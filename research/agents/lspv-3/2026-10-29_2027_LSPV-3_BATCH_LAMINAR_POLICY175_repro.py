#!/usr/bin/env python3
"""LSPV-3 BATCH-LAMINAR-POLICY175, GitHub standalone independent control.
Exact DP is checked against exhaustive subset-span optimization; stdlib only.
This concise GitHub reproducer is not asserted byte-identical to the
long-form 240-instance same-run reproducer cited in the accompanying report.
"""
import argparse, json, random, hashlib
from collections import Counter

def parity(x): return x.bit_count() & 1

def laminar(masks):
    return all((a&b) in (0,a,b) for j,a in enumerate(masks) for b in masks[j+1:])

def family(m,rng):
    items={1<<i for i in range(m)}
    def rec(arr):
        if len(arr)<2:return
        if rng.randrange(5):items.add(sum(1<<i for i in arr))
        rng.shuffle(arr);j=rng.randrange(1,len(arr))
        rec(arr[:j]);rec(arr[j:])
    rec(list(range(m)))
    result=sorted(items,key=lambda x:(x.bit_count(),x))
    assert laminar(result)
    return result

def optimal_plan(m,source_masks,weights,targets):
    """Tree DP with at most m+1 terminal signatures for any target count."""
    if not laminar(source_masks):raise ValueError("nonlaminar")
    masks=set(source_masks)|{1<<i for i in range(m)}
    weights=dict(weights); full=(1<<m)-1
    if full not in masks:
        masks.add(full);weights[full]=None
    nodes=sorted(masks,key=lambda x:(x.bit_count(),x))
    children={x:[] for x in nodes}
    for u in nodes:
        if u==full:continue
        p=min((v for v in nodes if v!=u and v&u==u),
              key=lambda v:v.bit_count())
        children[p].append(u)
    columns=[sum(((t>>i)&1)<<j for j,t in enumerate(targets))
             for i in range(m)]
    labels=sorted(set([0]+columns))
    dp={};back={}
    for u in nodes:
        if u.bit_count()==1:
            i=u.bit_length()-1
            dp[u]={a:weights[u]*(a!=columns[i]) for a in labels}
            back[u]={a:columns[i] for a in labels}
        else:
            G={b:sum(dp[v][b] for v in children[u]) for b in labels}
            if weights[u] is None:
                dp[u]={0:G[0]};back[u]={0:0}
            else:
                dp[u]={};back[u]={}
                for a in labels:
                    b=min(labels,key=lambda b:(G[b]+weights[u]*(a!=b),b))
                    dp[u][a]=G[b]+weights[u]*(a!=b)
                    back[u][a]=b
    picked=[];coefs={}
    def traceback(u,a):
        b=back[u][a]
        if b!=a:
            assert weights[u] is not None
            picked.append(u);coefs[u]=a^b
        for v in children[u]:traceback(v,b)
    traceback(full,0)
    for i,c in enumerate(columns):
        actual=0
        for u,z in coefs.items():
            if u&(1<<i):actual^=z
        assert actual==c
    price=sum(weights[u] for u in picked)
    assert price==dp[full][0]
    return price,picked,coefs,len(labels)

def span_contains(maskset,targets):
    basis={}
    for v in maskset:
        while v:
            b=v.bit_length()-1
            if b in basis:v^=basis[b]
            else:basis[b]=v;break
    for v in targets:
        while v:
            b=v.bit_length()-1
            if b not in basis:return False
            v^=basis[b]
    return True

def brute(masks,prices,targets):
    optimum=sum(prices.values())+1
    for z in range(1<<len(masks)):
        chosen=[u for j,u in enumerate(masks) if z&(1<<j)]
        price=sum(prices[u] for u in chosen)
        if price<optimum and span_contains(chosen,targets):optimum=price
    return optimum

def check(cases=240,seed=1751029):
    rng=random.Random(seed);out=Counter()
    for n in range(cases):
        m=2+n%5
        masks=family(m,rng)
        weights={u:rng.randrange(1,41) for u in masks}
        targets=[rng.randrange(1<<m) for _ in range(1+n%8)]
        if n%4==0:targets+=targets[:2]
        if n%5==0:targets+=[0]
        cost,picked,z,labels=optimal_plan(m,masks,weights,targets)
        assert cost==brute(masks,weights,targets),(n,cost)
        out['cases']+=1;out['target_rows']+=len(targets)
        out['exhaustively_evaluated_subsets']+=1<<len(masks)
        for theta in (0,(1<<m)-1,rng.randrange(1<<m)):
            observed={u:parity(u&theta) for u in picked}
            pred=[0]*len(targets)
            for u,coeff in z.items():
                for j in range(len(targets)):
                    if coeff&(1<<j):pred[j]^=observed[u]
            assert pred==[parity(theta&t) for t in targets]
            out['source_answers_checked']+=1
    assert not laminar([3,6])
    try:optimal_plan(3,[1,2,4,3,6],{1:1,2:1,4:1,3:2,6:2},[1])
    except ValueError:out['crossing_rejected']+=1
    else:raise AssertionError('crossing accepted')
    masks=[1,2,4,8,3,12,15]
    prices={1:50,2:50,4:50,8:50,3:1,12:1,15:1000}
    a,p,z,_=optimal_plan(4,masks,prices,[15])
    assert a==2 and set(p)=={3,12}
    out['xor_synergy']+=1
    prices.update({1:3,2:3,4:3,8:3,15:20})
    assert optimal_plan(4,masks,prices,[3,12,15])[0]==2
    out['batch_caching']+=1
    assert optimal_plan(4,masks,prices,[0,0])[0]==0
    out['zero_targets']+=1
    big_m,big_k=64,128
    big_masks=family(big_m,rng)
    big_weights={u:rng.randrange(1,10001) for u in big_masks}
    big_targets=[rng.getrandbits(big_m) for _ in range(big_k)]
    cost,chosen,coeff,labels=optimal_plan(big_m,big_masks,big_weights,big_targets)
    theta=rng.getrandbits(big_m)
    obs={u:parity(u&theta) for u in chosen}
    ans=[0]*big_k
    for u,alpha in coeff.items():
        for j in range(big_k):
            if alpha&(1<<j):ans[j]^=obs[u]
    assert ans==[parity(theta&t) for t in big_targets]
    out['large_labels']=labels
    out['large_target_rows']=big_k
    out['large_variables']=big_m
    out['large_probe_cost']=cost
    out['large_selected']=len(chosen)
    return dict(out)

if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--cases",type=int,default=240)
    p.add_argument("--seed",type=int,default=1751029)
    args=p.parse_args();res=check(args.cases,args.seed)
    print(json.dumps({"status":"COMPUTATIONAL, independent compact GitHub control",
                       "seed":args.seed,"results":res},indent=2,sort_keys=True))
