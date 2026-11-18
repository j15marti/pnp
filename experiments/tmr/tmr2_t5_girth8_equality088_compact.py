#!/usr/bin/env python3
"""TMR-2/088 compact, standalone standard-library exact-count auditor.
All values are original T5 labels. Computational finite evidence, not a P/NP proof.
"""
from itertools import product
from collections import deque
import hashlib,json
E=[tuple(map(int,s.split())) for s in '''0 17;0 18;1 17;2 24;3 27;5 18;5 28;6 31;7 23;7 25;8 21;8 29;9 23;10 21;10 25;10 28;11 27;12 32;13 24;13 27;14 19;14 23;15 19;18 6;19 1;19 13;20 1;20 16;21 11;22 8;22 12;25 2;26 3;26 5;26 9;26 16;28 15;29 14;30 6;30 14;31 4;31 11;32 4;32 9'''.split(';')]
source=('p t5 33 44\n'+''.join(f'v {i}\n' for i in range(33))+''.join(f'a {u} {v}\n' for u,v in E)).encode()
assert hashlib.sha256(source).hexdigest()=='0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac'
R=lambda a,b:(b-a)%5 in (1,3)

def adj(n,arcs):
    A=[set() for _ in range(n)]
    for a,b in arcs:A[a].add(b);A[b].add(a)
    return A

def girth(n,arcs):
    A=adj(n,arcs);best=n+1
    for src in range(n):
        dist={src:0};par={src:-1};q=deque([src])
        while q:
            u=q.popleft()
            for v in A[u]:
                if v not in dist:dist[v]=dist[u]+1;par[v]=u;q.append(v)
                elif par[u]!=v:best=min(best,dist[u]+dist[v]+1)
    return best if best<=n else None

def order(n,arcs):
    A=adj(n,arcs);left=set(range(n));seq=[];w=0
    while left:
        def score(v):
            ns=A[v]&left
            return (sum(b not in A[a] for a in ns for b in ns if a<b),len(ns),v)
        v=min(left,key=score);ns=A[v]&left;w=max(w,len(ns))
        for a in ns:A[a].update(ns);A[a].discard(a)
        left.remove(v);seq.append(v)
    return seq,w

def count(n,arcs,pins):
    dom=[range(5) for _ in range(n)]
    for u,v in pins.items():dom[u]=(v,)
    seq,width=order(n,arcs)
    factors=[]
    for u,v in arcs:
        s=tuple(sorted((u,v)))
        factors.append((s,{(a,b):int(R(a,b) if u<v else R(b,a))
                          for a in dom[s[0]] for b in dom[s[1]]}))
    visits=0
    for v in seq:
        bucket=[(s,t) for s,t in factors if v in s]
        factors=[f for f in factors if v not in f[0]]
        rest=tuple(sorted({u for s,_ in bucket for u in s}-{v}));table={}
        for tup in product(*(dom[u] for u in rest)):
            d=dict(zip(rest,tup));z=0
            for x in dom[v]:
                visits+=1;d[v]=x;val=1
                for s,t in bucket:
                    val*=t.get(tuple(d[u] for u in s),0)
                    if not val:break
                z+=val
            if z:table[tup]=z
        factors.append((rest,table))
    assert len(factors)==1 and factors[0][0]==()
    return factors[0][1].get((),0),width,visits

base=E[1:]
assert girth(33,E)==girth(33,base)==8
B=[count(33,base,{0:0,17:d})[0] for d in range(5)]
assert B==[378,0,756,0,378]
rev=[B[-d%5] for d in range(5)]
assert [B[d]*rev[d] for d in range(5)]==[142884,0,0,0,0]
# Glue TWO copies of H-e at terminals 0,17; reverse all second-copy arcs.
arcs=[];n=2
for k in range(2):
    mp={0:0,17:1}
    for i in range(33):
        if i not in mp:mp[i]=n;n+=1
    for u,v in base:arcs.append((mp[v],mp[u]) if k else (mp[u],mp[v]))
assert n==64
arcs.append((1,64));n=65
assert len(arcs)==87 and girth(n,arcs)==8
K=[count(n,arcs,{0:0,64:d})[0] for d in range(5)]
assert K==[0,142884,0,142884,0]
print(json.dumps({'source_sha256':hashlib.sha256(source).hexdigest(),
 'critical_edge':(0,17),'H_minus_edge_cofactor':B,
 'equality_cofactor':[B[d]*rev[d] for d in range(5)],
 'edge_gadget_n':65,'edge_gadget_arcs':87,'edge_gadget_girth':8,
 'edge_gadget_cofactor':K,'factor':142884,
 'one_gadget_bucket_width_upper':order(n,arcs)[1],
 'same_skeleton_base_counts':(0,5),
 'five_gadget_lift_counts':(0,5*142884**5),
 'scope':'Exact finite computational certificate. P versus NP OPEN.'},indent=2))
