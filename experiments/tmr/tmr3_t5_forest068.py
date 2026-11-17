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


def cycle_rank_count(n, edges, max_rank=8, return_matrix=False):
    """Exact Z5 cycle-space residue DP using two updates per input arc.
    Raises OverflowError if the cycle rank exceeds max_rank.
    """
    edges=tuple(sorted(set(edges)))
    if any(u==v or (v,u) in edges for u,v in edges): return 0, 0
    parent=list(range(n))
    def find(v):
        while parent[v]!=v: v=parent[v]
        return v
    forest=[[] for _ in range(n)]; chords=[]; roots=n
    by_edge={e:i for i,e in enumerate(edges)}
    for i,(u,v) in enumerate(edges):
        ru,rv=find(u),find(v)
        if ru==rv: chords.append(i)
        else:
            parent[ru]=rv; roots-=1
            forest[u].append(v); forest[v].append(u)
    rank=len(chords)
    if rank>max_rank: raise OverflowError('cycle rank exceeds requested limit')
    columns=[[0]*rank for _ in edges]
    for row,edge_id in enumerate(chords):
        u,v=edges[edge_id]
        columns[edge_id][row]=1
        previous={v:None}; queue=deque([v])
        while queue and u not in previous:
            a=queue.popleft()
            for b in forest[a]:
                if b not in previous: previous[b]=a; queue.append(b)
        assert u in previous
        a=u
        while previous[a] is not None:
            b=previous[a]  # Reverse of required v -> u traversal: a -> b.
            if (a,b) in by_edge: columns[by_edge[(a,b)]][row]=-1
            else: columns[by_edge[(b,a)]][row]=1
            a=b
    if return_matrix: return roots, columns
    zero=(0,)*rank; states={zero:1}
    for col in columns:
        updated={}
        for state,count in states.items():
            for d in (1,3):
                next_state=tuple((state[j]+d*col[j])%5 for j in range(rank))
                updated[next_state]=updated.get(next_state,0)+count
        states=updated
    return (5**roots)*states.get(zero,0), rank


def fourier_poly_count(n, edges, max_rank=8):
    """Exact character-sum cycle counter: 5**r time, polynomial space.
    Computes in Z[z]/(z**4+z**3+z**2+z+1), no floating point.
    """
    edges=tuple(sorted(set(edges)))
    if any(u==v or (v,u) in edges for u,v in edges): return 0
    roots, columns=cycle_rank_count(n,edges,max_rank,True)
    r=len(columns[0]) if columns else 0
    mono=((1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(-1,-1,-1,-1))
    def multiply(a,b):
        z=[0]*7
        for i,x in enumerate(a):
            for j,y in enumerate(b): z[i+j]+=x*y
        for i in (6,5,4):
            t=z[i]
            for j in range(5):z[i-4+j]-=t
        return z[:4]
    accum=[0]*4
    for lam in itertools.product(range(5),repeat=r):
        p=[1,0,0,0]
        for column in columns:
            q=sum(x*y for x,y in zip(lam,column))%5
            factor=[mono[q][k]+mono[(3*q)%5][k] for k in range(4)]
            p=multiply(p,factor)
        for k in range(4):accum[k]+=p[k]
    assert accum[1:]==[0,0,0] and accum[0]%(5**r)==0
    return (5**roots)*(accum[0]//(5**r))

def brute(n,edges):
    return sum(all(ok(a[u],a[v]) for u,v in edges)
               for a in itertools.product(range(5),repeat=n))

def audit():
    rng=random.Random(SEED); checks=0; random_cases=0; cycle_dp_checks=0; fourier_checks=0
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
    for n in range(0,10):
        for rep in range(35):
            es=[]
            for v in range(1,n):
                if rng.randrange(4):
                    p=rng.randrange(v); es.append((p,v) if rng.randrange(2) else (v,p))
            for trial in range(3):
                if n>1 and rng.randrange(3)==0:
                    u,v=rng.sample(range(n),2)
                    if (u,v) not in es and (v,u) not in es:
                        es.append((u,v) if rng.randrange(2) else (v,u))
            got,rank=cycle_rank_count(n,es)
            assert got==count(n,es),(n,es,got,rank); checks+=1; cycle_dp_checks+=1
            f=fourier_poly_count(n,es)
            assert f==got,(n,es,got,f); checks+=1; fourier_checks+=1
    for bad in ('','a b','3 1\n0','3 1\n0 4','3 1\n0 1\n0 2','3 -1','2 1\n1 x'):
        try:parse(bad)
        except ValueError:checks+=1
        else:raise AssertionError('accepted malformed source')
    examples={'oriented_triangle':(3,[(0,1),(1,2),(2,0)]),
              'transitive_triangle':(3,[(0,1),(1,2),(0,2)]),
              'directed_five_cycle':(5,[(i,(i+1)%5) for i in range(5)]),
              'T5_template':(5,[(u,v) for u in range(5) for v in range(5) if ok(u,v)])}
    print(json.dumps({'revision':'tmr3-t5-forest068-v4','seed':SEED,'checks':checks,
                      'random_graphs':random_cases,'cycle_dp_crosschecks':cycle_dp_checks,'fourier_crosschecks':fourier_checks,'failures':0,
                      'example_counts':{key:count(*pair) for key,pair in examples.items()}},
                     indent=2,sort_keys=True))

if __name__=='__main__':
    if len(sys.argv)==2 and sys.argv[1]=='--audit':audit()
    elif len(sys.argv)==2:
        with open(sys.argv[1],encoding='ascii') as f:n,e=parse(f.read())
        print(json.dumps({'satisfiable':count(n,e)>0,'homomorphism_count':count(n,e)},sort_keys=True))
    else:raise SystemExit('usage: script.py --audit | graph.txt')
