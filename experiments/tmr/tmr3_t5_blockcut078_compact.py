#!/usr/bin/env python3
"""All-input five-symbol CSP counter using authenticated block-cut gluing.
Input: n m, explicit vertex roster 'V 0 1 ... n-1', then m arc pairs.
Run with --selftest for finite original-arc brute-force comparisons.
"""
import itertools
import random
import sys


def parse(s):
    t = s.split()
    if len(t) < 3:
        raise ValueError('short header')
    try:
        n, m = map(int, t[:2])
    except ValueError as ex:
        raise ValueError('bad header') from ex
    if n < 0 or m < 0 or len(t) != 3+n+2*m:
        raise ValueError('wrong roster/edge length')
    if t[2] != 'V' or t[3:3+n] != list(map(str, range(n))):
        raise ValueError('wrong vertex roster')
    edges=set()
    for i in range(m):
        try:
            a, b = int(t[3+n+2*i]), int(t[4+n+2*i])
        except ValueError as ex:
            raise ValueError('bad arc') from ex
        if not (0 <= a < n and 0 <= b < n):
            raise ValueError('endpoint out of range')
        edges.add((a,b))
    return n, tuple(sorted(edges))


def blocks(n,edges):
    adj=[set() for _ in range(n)]
    for a,b in edges:
        adj[a].add(b); adj[b].add(a)
    disc, low, par, estack, out = {}, {}, {}, [], []
    clock, components = 0, 0
    for root in range(n):
        if root in disc: continue
        components+=1
        par[root]=None
        disc[root]=low[root]=clock; clock+=1
        stack=[(root,iter(sorted(adj[root])))]
        while stack:
            u,it=stack[-1]
            try: v=next(it)
            except StopIteration:
                stack.pop()
                p=par[u]
                if p is not None:
                    low[p]=min(low[p],low[u])
                    if low[u]>=disc[p]:
                        verts=set()
                        while True:
                            e=estack.pop(); verts.update(e)
                            if e==(p,u): break
                        out.append(tuple(sorted(verts)))
                continue
            if v not in disc:
                par[v]=u; disc[v]=low[v]=clock; clock+=1
                estack.append((u,v))
                stack.append((v,iter(sorted(adj[v]))))
            elif v != par[u] and disc[v] < disc[u]:
                low[u]=min(low[u],disc[v]); estack.append((u,v))
    owner={}
    for j,verts in enumerate(out):
        for u,v in itertools.combinations(verts,2):
            if v in adj[u]:
                assert (u,v) not in owner
                owner[u,v]=j
    groups=[[] for _ in out]
    for a,b in edges:
        groups[owner[min(a,b),max(a,b)]].append((a,b))
    return out,groups,components


def rooted_count(verts,arcs):
    nb={v:set() for v in verts}
    source=set(arcs)
    for a,b in arcs:
        nb[a].add(b); nb[b].add(a)
    root=verts[0]
    par={root:None}; order=[root]
    for u in order:
        for v in sorted(nb[u]):
            if v not in par:
                par[v]=u; order.append(v)
    assert len(order)==len(verts)
    out=0
    for bits in itertools.product((0,1),repeat=len(verts)-1):
        color={root:0}
        for v,bit in zip(order[1:],bits):
            p=par[v]
            delta=(1,3)[bit] if (p,v) in source else (4,2)[bit]
            color[v]=(color[p]+delta)%5
        out+=all((color[b]-color[a])%5 in (1,3) for a,b in arcs)
    return out


def count(n,edges):
    E=set(edges)
    if any(u==v or (v,u) in E for u,v in edges):
        return 0
    b,groups,c=blocks(n,edges)
    z=5**c
    for verts,arcs in zip(b,groups):
        z*=rooted_count(verts,arcs)
    return z


def selftest():
    rng=random.Random(202611172224)
    checked=0
    for _ in range(110):
        n=rng.randrange(0,7)
        E=[(i,j) for i in range(n) for j in range(n)
           if rng.randrange(15)==0]
        src=f'{n} {len(E)}\nV '+' '.join(map(str,range(n)))+'\n'
        src+=''.join(f'{a} {b}\n' for a,b in E)
        nn, ee=parse(src)
        expected=sum(all((x[b]-x[a])%5 in (1,3) for a,b in ee)
                     for x in itertools.product(range(5),repeat=n))
        assert count(nn,ee)==expected
        checked+=1
    print(f'compact original-arc exact comparisons={checked}; failures=0')


if __name__=='__main__':
    if sys.argv[1:]==['--selftest']:
        selftest()
    else:
        try:
            n,arcs=parse(sys.stdin.read())
        except ValueError as ex:
            print('INVALID:',ex); sys.exit(2)
        print(count(n,arcs))
