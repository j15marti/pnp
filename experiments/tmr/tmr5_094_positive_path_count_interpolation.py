#!/usr/bin/env python3
"""TMR-5/094: self-contained exact interpolation firewall for T5 counting."""
from collections import Counter
from itertools import product, permutations
from math import comb
import json, random, hashlib

S=(1,3)
A=[[int((j-i)%5 in S) for j in range(5)] for i in range(5)]
P=2305843009213693951   # 2^61-1, prime; much larger than tested Vandermonde bases

def multiply(B,C):
    return [[sum(B[i][k]*C[k][j] for k in range(5)) for j in range(5)] for i in range(5)]

def powers():
    M=[[int(i==j) for j in range(5)] for i in range(5)]
    res={}
    for l in range(1,7):
        M=multiply(M,A)
        res[l]=M
    return res

def direct_walks(l):
    W=[[0]*5 for _ in range(5)]
    for s in range(5):
        for steps in product(S, repeat=l):
            W[s][(s+sum(steps))%5]+=1
    return W

def determinant(M):
    n=len(M);ans=0
    for perm in permutations(range(n)):
        parity=sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))%2
        ans+=(-1 if parity else 1)*__import__('math').prod(M[i][perm[i]] for i in range(n))
    return ans

def histogram_list(m):
    return [h for h in product(range(m+1),repeat=4) if sum(h)<=m for h in [h+(m-sum(h),)]]

def vandermonde_inverse_mod(nodes):
    n=len(nodes)
    rows=[]
    for i in range(n):
        rows.append([pow(z,i,P) for z in nodes]+[int(i==j) for j in range(n)])
    for col in range(n):
        pivot=next((k for k in range(col,n) if rows[k][col]),None)
        if pivot is None: raise AssertionError('Unexpected modular collision')
        rows[col],rows[pivot]=rows[pivot],rows[col]
        x=pow(rows[col][col],P-2,P)
        rows[col]=[(v*x)%P for v in rows[col]]
        for r in range(n):
            if r==col:continue
            factor=rows[r][col]
            if factor:
                rows[r]=[(a-factor*b)%P for a,b in zip(rows[r],rows[col])]
    return [r[n:] for r in rows]

def evaluate_direct(n,edges,t,w):
    return sum(__import__('math').prod(pow(w[(labels[v]-labels[u])%5],t,P) for u,v in edges)%P
               for labels in product(range(5),repeat=n))%P

def histogram_counts(n,edges):
    ans=Counter()
    for a in product(range(5),repeat=n):
        c=Counter((a[v]-a[u])%5 for u,v in edges)
        ans[tuple(c.get(j,0) for j in range(5))]+=1
    return ans

def native_instance_one_edge():
    # Original edge (0,1), three internally vertex-disjoint paths of lengths 4,5,6.
    n=2;edges=[]
    for length in (4,5,6):
        cur=0
        for _ in range(length-1):
            edges.append((cur,n));cur=n;n+=1
        edges.append((cur,1))
    adj=[[] for _ in range(n)]
    for u,v in edges:
        adj[u].append((v,1));adj[v].append((u,-1))
    order=[0,1]+[v for v in range(2,n)]
    assign=[-1]*n
    def rec(idx):
        if idx==n:return 1
        u=order[idx];count=0
        for x in range(5):
            if all(assign[v]<0 or (A[x][assign[v]] if d==1 else A[assign[v]][x])
                   for v,d in adj[u]):
                assign[u]=x
                count+=rec(idx+1)
                assign[u]=-1
        return count
    return n,len(edges),rec(0)

def run():
    powers_ = powers()
    assert all(powers_[l]==direct_walks(l) for l in range(1,7))
    w=tuple(powers_[4][0][d]*powers_[5][0][d]*powers_[6][0][d] for d in range(5))
    assert w==(120,280,100,210,150)
    assert all(powers_[l][i][j]>0 for l in (4,5,6) for i in range(5) for j in range(5))
    primes=(2,3,5,7)
    def val(x,p):
        k=0
        while x%p==0: x//=p;k+=1
        return k
    E=[[val(v,p) for v in w] for p in primes]+[[1]*5]
    det=determinant(E)
    assert det==1
    assert all(w[d]==__import__('math').prod(p**E[j][d] for j,p in enumerate(primes)) for d in range(5))
    gadget_checks=0
    for u,v,a,b,c in product(range(5),repeat=5):
        sat=bool(A[u][a] and A[a][b] and A[b][c] and A[u][c] and A[c][v])
        assert sat==((a==(u+1)%5) and (b==(u+2)%5) and (c==(u+3)%5)
                     and ((v-u)%5 in (1,4)))
        gadget_checks+=1
    # TMR-5/094 independent reconstruction checks, finite m=1,2,3.
    rng=random.Random(20261118)
    cases=0;reconstructions=0
    for m in (1,2,3):
        hs=histogram_list(m)
        assert len(hs)==comb(m+4,4)
        zs=[__import__('math').prod(w[d]**h[d] for d in range(5)) for h in hs]
        assert len(set(zs))==len(zs)
        assert max(zs)<P
        inv=vandermonde_inverse_mod(zs)
        for _ in range(12):
            n=rng.randint(3,5)
            options=[(u,v) for u in range(n) for v in range(n) if u!=v]
            edges=rng.sample(options,m)
            ys=[evaluate_direct(n,edges,t,w) for t in range(len(hs))]
            recovered=[sum(inv[j][i]*ys[i] for i in range(len(hs)))%P
                       for j in range(len(hs))]
            expected=histogram_counts(n,edges)
            assert all(recovered[j]==expected.get(h,0) for j,h in enumerate(hs))
            zr=sum(recovered[j] for j,h in enumerate(hs) if h[0]==h[2]==h[4]==0)
            actual=sum(all((labels[v]-labels[u])%5 in S for u,v in edges)
                       for labels in product(range(5),repeat=n))
            assert zr==actual
            cases+=1;reconstructions+=len(hs)
    native=native_instance_one_edge()
    assert native==(14,15,4300)
    result={
        'name':'TMR-5/094 positive-only counting firewall',
        'T5_adjacency_rows':{str(l):powers_[l][0] for l in (4,5,6)},
        'positive_parallel_path_weights':w,
        'prime_exponent_matrix':E,
        'determinant_with_sum_row':det,
        'gadget_private_assignments':gadget_checks,
        'Vandermonde_random_instance_cases':cases,
        'histogram_coefficients_reconstructed':reconstructions,
        'independent_native_three_path_one_edge':{'vertices':native[0], 'arcs':native[1],'homomorphisms':native[2]},
        'assertion_failures':0,
    }
    return result

if __name__=='__main__':
    txt=json.dumps(run(), sort_keys=True, indent=2)+'\n'
    with open('/mnt/data/tmr5_094_positive_path_count_results.json','w') as f:f.write(txt)
    print(txt)
