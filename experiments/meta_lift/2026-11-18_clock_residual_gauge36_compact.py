#!/usr/bin/env python3
"""Compact independent reproducibility control for CLOCKRESIDUALGAUGE36."""
import random, json
from collections import Counter
R=random.Random(202611180536)
checks=0

def audit(N,t,F,h):
    global checks
    K=len(F); reachable=[{0}]
    for i in range(N):
        reachable.append({t[i][p][b] for p in reachable[-1] for b in (0,1)})
    sig=[None]*(N+1)
    sig[N]=tuple(F)
    for i in range(N-1,-1,-1):
        vals=[(sig[i+1][t[i][p][0]],sig[i+1][t[i][p][1]]) for p in range(K)]
        lookup={v:j for j,v in enumerate(sorted(set(vals)))}
        sig[i]=tuple(lookup[v] for v in vals)
    W=max(len({sig[i][p] for p in reachable[i]}) for i in range(N+1))
    e=0; ep=0
    for i in range(N):
        m={sig[i][p]:sig[i+1][t[i][p][h[i]]] for p in reachable[i]}
        e+=(len(m)!=len(set(m.values())))
        ep+=(len(reachable[i])!=len({t[i][p][h[i]] for p in reachable[i]}))
    bound=(e+1)*(W-1)+e
    d={0:0}
    for i in range(N):
        nd={}
        for p,c in d.items():
            for b in (0,1):
                q=t[i][p][b]
                nd[q]=min(nd.get(q,N+1),c+(b!=h[i]))
        d=nd
    best={}
    for p,c in d.items():best[F[p]]=min(best.get(F[p],N+1),c)
    assert all(c<=bound for c in best.values());checks+=1
    if N<=8:
        brute={}
        for bits in range(1<<N):
            p=0;cost=0
            for i in range(N):
                b=(bits>>i)&1
                p=t[i][p][b];cost+=(b!=h[i])
            brute[F[p]]=min(brute.get(F[p],N+1),cost)
        assert brute==best;checks+=1
    return {'W':W,'e':e,'e_phys':ep,'bound':bound,'best':best}

def fixed(zero,one,N):return [tuple((zero[p],one[p]) for p in range(len(zero))) for _ in range(N)]

if __name__=='__main__':
    strict=audit(8,fixed([0,0,2],[2,2,1],8),[0,0,1],[0]*8)
    reverse=audit(8,fixed([0,1,2],[2,1,1],8),[0,0,1],[0]*8)
    equality=audit(8,fixed([1,1],[0,1],8),[1,0],[0]*8)
    assert (strict['W'],strict['e'],strict['e_phys'])==(2,0,6);checks+=1
    assert (reverse['e'],reverse['e_phys'])==(1,0);checks+=1
    assert equality['best'][1]==8;checks+=1
    models=0;res_more=0
    for N,K in [(6,2),(8,3),(10,4)]:
        for j in range(32):
            t=[tuple((R.randrange(K),R.randrange(K)) for _ in range(K)) for _ in range(N)]
            F=[R.randrange(3) for _ in range(K)]
            h=[R.randrange(2) for _ in range(N)] if j%2 else [0]*N
            v=audit(N,t,F,h);models+=1;res_more+=(v['e']>v['e_phys'])
    print(json.dumps({'status':'PASS','checks':checks,'random_models':models,'residual_more':res_more,'strict':strict,'non_domination':reverse,'equality':equality},sort_keys=True))
