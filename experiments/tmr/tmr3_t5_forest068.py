#!/usr/bin/env python3
"""Exact T5 homomorphism counter, spanning-forest binary increments.
Usage: python tmr3_t5_forest068.py --audit
       python tmr3_t5_forest068.py graph.txt
Graph file: n m on first line, then m zero-based u v edge lines.
No third-party dependencies. Python reference, not a TM microstep trace.
"""
import itertools, json, random, sys
from collections import deque

SEED = 202611171228

def ok(a,b):
    return (b-a)%5 in (1,3)

def parse(s):
    lines=s.splitlines()
    if not lines: raise ValueError('empty input')
    tokens=[line.split() for line in lines]
    if any(len(t)!=2 or any(not z.isascii() or not z.isdecimal() for z in t) for t in tokens):
        raise ValueError('each line requires two unsigned integers')
    n,m=map(int,tokens[0]); edges=[tuple(map(int,x)) for x in tokens[1:]]
    if len(edges)!=m or any(u>=n or v>=n for u,v in edges):
        raise ValueError('mismatch or vertex outside declared range')
    return n,tuple(sorted(set(edges)))

def count(n,edges):
    edges=set(edges)
    if any(u==v or (v,u) in edges for u,v in edges): return 0
    adj=[[] for _ in range(n)]
    for u,v in edges:
        adj[u].append((v,1)); adj[v].append((u,-1))
    seen=[False]*n; parent=[-1]*n; direction=[0]*n; order=[]; c=0
    for root in range(n):
        if seen[root]: continue
        c+=1; seen[root]=True; q=deque([root]); order.append(root)
        while q:
            u=q.popleft()
            for v,d in adj[u]:
                if not seen[v]:
                    seen[v]=True; parent[v]=u; direction[v]=d
                    q.append(v); order.append(v)
    labels=[-1]*n
    def dfs(i):
        if i==n: return 1
        v=order[i]
        colors=(0,) if parent[v]<0 else tuple((labels[parent[v]]+direction[v]*d)%5 for d in (1,3))
        ans=0
        for color in colors:
            labels[v]=color
            if all(labels[w]<0 or (ok(color,labels[w]) if d==1 else ok(labels[w],color))
                   for w,d in adj[v]):
                ans+=dfs(i+1)
        labels[v]=-1
        return ans
    return (5**c)*dfs(0)

def brute(n,edges):
    return sum(all(ok(a[u],a[v]) for u,v in edges)
               for a in itertools.product(range(5),repeat=n))

def audit():
    rng=random.Random(SEED); checks=0; random_cases=0
    def same(n,edges):
        nonlocal checks
        a=count(n,edges); b=brute(n,edges)
        assert a==b,(n,edges,a,b); checks+=1
        return a
    for n in range(8):
        same(n,[])
        same(n,[(i,i+1) for i in range(n-1)])
        if n>=3: same(n,[(i,(i+1)%n) for i in range(n)])
        if n>=2: same(n,[(0,1),(1,0)])
        if n: same(n,[(0,0)])
    for n in range(1,9):
        for rep in range(100 if n<7 else 25):
            p=rng.uniform(.04,.75)
            edges=[(u,v) for u in range(n) for v in range(n) if rng.random()<p]
            same(n,edges); random_cases+=1
    for n in range(1,20):
        for rep in range(12):
            edges=[]; roots=n
            for v in range(1,n):
                if rng.randrange(4):
                    p=rng.randrange(v); edges.append((p,v) if rng.randrange(2) else (v,p))
                    roots-=1
            assert count(n,edges)==5**roots*2**(n-roots); checks+=1
    for n in range(3,8):
        for mask in range(1<<n):
            edges=[(i,(i+1)%n) if mask>>i&1 else ((i+1)%n,i) for i in range(n)]
            same(n,edges)
    for bad in ('','a b','3 1\n0','3 1\n0 4','3 1\n0 1\n0 2','3 -1','2 1\n1 x'):
        try:parse(bad)
        except ValueError:checks+=1
        else:raise AssertionError('accepted malformed source')
    examples={'oriented_triangle':(3,[(0,1),(1,2),(2,0)]),
              'transitive_triangle':(3,[(0,1),(1,2),(0,2)]),
              'directed_five_cycle':(5,[(i,(i+1)%5) for i in range(5)]),
              'T5_template':(5,[(u,v) for u in range(5) for v in range(5) if ok(u,v)])}
    print(json.dumps({'revision':'tmr3-t5-forest068-v2','seed':SEED,'checks':checks,
                      'random_graphs':random_cases,'failures':0,
                      'example_counts':{key:count(*pair) for key,pair in examples.items()}},
                     indent=2,sort_keys=True))

if __name__=='__main__':
    if len(sys.argv)==2 and sys.argv[1]=='--audit':audit()
    elif len(sys.argv)==2:
        with open(sys.argv[1],encoding='ascii') as f:n,e=parse(f.read())
        print(json.dumps({'satisfiable':count(n,e)>0,'homomorphism_count':count(n,e)},sort_keys=True))
    else:raise SystemExit('usage: script.py --audit | graph.txt')
