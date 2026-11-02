#!/usr/bin/env python3
"""LSPV-1 PAID_LOGWIDTH313. Finite controls, not Korhonen FPT implementation."""
import itertools as it, json
from collections import Counter
P=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
Q=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
F9=P+[tuple(-x for x in row) for row in Q]
Y6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]+[tuple(-x for x in row) for row in [(1,2,4),(1,3,6),(2,3,5),(4,5,6)]]
def canonical(F,n):
    a=Counter((abs(x),x>0) for row in F for x in row)
    return 3*len(F)==4*n and len({tuple(sorted(r)) for r in F})==len(F) and all(
        len(r)==3 and len({abs(x) for x in r})==3 and all(0<abs(x)<=n for x in r) and
        (all(x>0 for x in r) or all(x<0 for x in r)) for r in F) and all(
        a[v,s]==2 for v in range(1,n+1) for s in (False,True))
def splice(t):
    F=[]
    for i in range(t):
        for j,row in enumerate(F9):
            F.append((9*i+1,9*i+6,9*((i+1)%t)+5) if j==0 else
                 tuple((1 if x>0 else -1)*(9*i+abs(x)) for x in row))
    return F
def count(F,n,p):
    free=[v for v in range(1,n+1) if v not in p]
    answer=0
    for bits in it.product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,bits))}
        answer+=all(any(a[abs(x)]==(x>0) for x in row) for row in F)
    return answer
def graph(F,n,p):
    G={v:set() for v in range(1,n+1) if v not in p}
    for row in F:
        if any(abs(x) in p and p[abs(x)]==(x>0) for x in row):continue
        free=[abs(x) for x in row if abs(x) not in p]
        for u,v in it.combinations(free,2):G[u].add(v);G[v].add(u)
    return G
def width(G,order):
    G={x:set(y) for x,y in G.items()};m=0
    for x in order:
        neigh=list(G[x]);m=max(m,len(neigh)+1)
        for u,v in it.combinations(neigh,2):G[u].add(v);G[v].add(u)
        for y in neigh:G[y].discard(x)
        del G[x]
    return m
def greedy(G):
    H={x:set(y) for x,y in G.items()};r=[]
    while H:
        x=min(H,key=lambda v:(len(H[v]),v));r.append(x)
        n=list(H[x])
        for a,b in it.combinations(n,2):H[a].add(b);H[b].add(a)
        for a in n:H[a].discard(x)
        del H[x]
    return r
def verify_bags(t):
    F=splice(t)
    V=[set(range(9*i+1,9*i+10)) for i in range(t)]
    B=[V[0]|V[i]|V[i+1] for i in range(t-1)]
    assert canonical(F,9*t)
    assert all(any(set(map(abs,row))<=bag for bag in B) for row in F)
    for x in range(1,9*t+1):
        occ=[i for i,bag in enumerate(B) if x in bag]
        assert occ==list(range(min(occ),max(occ)+1))
    return {'t':t,'n':9*t,'m':12*t,'certified_width_upper':max(map(len,B))-1}
def main():
    assert canonical(F9,9) and canonical(Y6,6)
    p={5:0,7:0};g=graph(F9,9,p);gr=greedy(g)
    opt=min(width(g,o) for o in it.permutations(sorted(g)))
    assert width(g,gr)==6 and opt==5
    pS={1:0,3:0,5:1,6:0,7:0,8:0};pU={**pS,1:1}
    G2=splice(2);A={5:1};BQ={5:1,4:0,6:0,10:0,14:0,15:0}
    models={'F9_root':count(F9,9,{}),'F9_gap':count(F9,9,p),
       'F9_S':count(F9,9,pS),'F9_U':count(F9,9,pU),
       'Y6_root':count(Y6,6,{}),'G2_AZ':count(G2,18,A),'G2_BQ':count(G2,18,BQ)}
    assert models=={'F9_root':70,'F9_gap':13,'F9_S':2,'F9_U':0,
                    'Y6_root':20,'G2_AZ':2377,'G2_BQ':0}
    assert not canonical(F9[:-1],9)
    print(json.dumps({'status':'PASS','greedy_closed_width':6,'optimal_closed_width':5,
     'exact_order_searches':5040,'source_models':models,
     'path_decompositions':[verify_bags(t) for t in (2,3,4,8,16)]},indent=2))
if __name__=='__main__':main()
