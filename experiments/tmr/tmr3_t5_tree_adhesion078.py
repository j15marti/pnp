#!/usr/bin/env python3
"""TMR-3/078: exact T5 homomorphism counter via articulation-block two-cover messages.

Input: JSON {"n": number of original vertices, "arcs": [[tail,head], ...]}.
With --audit run deterministic tests. No external packages.
"""
from __future__ import annotations
import argparse, collections, itertools, json, random, sys
from functools import reduce

D = (1, 3)
OUT = tuple(frozenset(((a+1)%5, (a+3)%5)) for a in range(5))

def R(a, b):
    return (b-a)%5 in D

def W(cols):
    return len(OUT[cols[0]] & OUT[cols[1]] & OUT[cols[2]])

def forest_count(n, arcs):
    """General all-input exact counter with 2^(n-c) forest difference branches."""
    if any(u==v for u,v in arcs): return 0
    edges=set(arcs)
    adj=[set() for _ in range(n)]
    for u,v in edges: adj[u].add(v); adj[v].add(u)
    visited=set(); parent_edges=[]; roots=[]
    for root in range(n):
        if root in visited: continue
        roots.append(root); visited.add(root)
        queue=[root]
        for u in queue:
            for v in sorted(adj[u]):
                if v not in visited:
                    visited.add(v); queue.append(v)
                    parent_edges.append((u,v, (1,3) if (u,v) in edges else (4,2)))
    good=0
    for bits in itertools.product((0,1),repeat=len(parent_edges)):
        colors=[None]*n
        for r in roots: colors[r]=0
        for (u,v,offsets),bit in zip(parent_edges,bits):
            colors[v]=(colors[u]+offsets[bit])%5
        if all(R(colors[u],colors[v]) for u,v in edges): good+=1
    return good*5**len(roots)

def biconnected(primal):
    """Undirected Tarjan edge blocks; no input loops."""
    n=len(primal); dfsnum=[-1]*n; low=[0]*n; estack=[]; blocks=[]; tick=0
    sys.setrecursionlimit(max(2000, n*3+100))
    def dfs(u,parent):
        nonlocal tick
        dfsnum[u]=low[u]=tick; tick+=1
        for v in sorted(primal[u]):
            if dfsnum[v]<0:
                estack.append((u,v)); dfs(v,u)
                low[u]=min(low[u],low[v])
                if low[v]>=dfsnum[u]:
                    parts=set()
                    while estack:
                        e=estack.pop(); parts.update(e)
                        if e==(u,v): break
                    blocks.append(frozenset(parts))
            elif v!=parent and dfsnum[v]<dfsnum[u]:
                low[u]=min(low[u],dfsnum[v]); estack.append((u,v))
    for u in range(n):
        if dfsnum[u]<0:
            dfs(u,-1)
            assert not estack
    return blocks

def min_relative_two_cover(triples, vertices, base, stats):
    """Exact minimum 2-cover: iterative budgets and constant branching <=3."""
    possible=sorted(set(vertices)-set(base)); base=frozenset(base)
    def search(selected,budget):
        stats['cover_nodes']+=1
        chosen=base|selected
        for triple in triples:
            missing=2-len(set(triple)&chosen)
            if missing>0: break
        else: return selected
        remain=tuple(x for x in triple if x not in chosen)
        if missing>budget: return None
        for extra in itertools.combinations(remain,missing):
            ans=search(selected|set(extra),budget-missing)
            if ans is not None: return ans
        return None
    for k in range(len(possible)+1):
        ans=search(frozenset(),k)
        if ans is not None:
            return tuple(sorted(ans))
    raise AssertionError('Every triple has three vertices; a 2-cover must exist')

def triple_source(n, arcs):
    """Return (hubs, triples) for disjoint source-to-private-3-sink format, else None."""
    indeg=[set() for _ in range(n)]; outdeg=[set() for _ in range(n)]
    for u,v in arcs:
        indeg[v].add(u); outdeg[u].add(v)
    hubs={u for u in range(n) if not indeg[u]}
    triples=[]
    for v in range(n):
        if v in hubs: continue
        if outdeg[v] or len(indeg[v])!=3 or not indeg[v]<=hubs:
            return None
        triples.append(tuple(sorted(indeg[v])))
    return sorted(hubs),triples

def tree_count(n, arcs):
    """Complete counter; returns (exact number, route, diagnostics)."""
    if not isinstance(n,int) or isinstance(n,bool) or n<0: raise ValueError('n must be nonnegative integer')
    checked=[]
    for pair in arcs:
        if len(pair)!=2 or any(not isinstance(v,int) or isinstance(v,bool) or v<0 or v>=n for v in pair):
            raise ValueError('invalid original arc')
        checked.append(tuple(pair))
    arcs=sorted(set(checked))  # A directed graph has set, not multiset, arcs.
    if any(u==v for u,v in arcs): return 0,'loop',{'n':n}
    source=triple_source(n,arcs)
    if source is None:
        return forest_count(n,arcs),'forest-fallback',{'n':n,'arcs':len(arcs)}
    hubs,triples=source
    renumber={v:i for i,v in enumerate(hubs)}
    triples=[tuple(renumber[u] for u in e) for e in triples]
    h=len(hubs)
    primal=[set() for _ in range(h)]
    for e in triples:
        for u,v in itertools.combinations(e,2):
            primal[u].add(v); primal[v].add(u)
    blocks=biconnected(primal)
    belongs=[[] for _ in range(h)]
    for bid,B in enumerate(blocks):
        for u in B: belongs[u].append(bid)
    edge_block={}
    for bid,B in enumerate(blocks):
        for u in B:
            for v in primal[u] & B:
                if u<v:
                    key=(u,v)
                    assert key not in edge_block
                    edge_block[key]=bid
    block_triples=[[] for B in blocks]
    for e in triples:
        bid=edge_block[tuple(sorted(e[:2]))]
        assert set(e)<=blocks[bid]
        block_triples[bid].append(e)
    stats={'blocks':len(blocks),'triples':len(triples),'cover_nodes':0,'max_cover':0,'evaluated_colorings':0}
    seen_blocks=set()
    # Block-cut incidence graph is a forest; each block has at most one parent articulation.
    def from_articulation(a,parent_bid):
        ans=[1]*5
        for bid in belongs[a]:
            if bid==parent_bid: continue
            msg=from_block(bid,a)
            for c in range(5): ans[c]*=msg[c]
        return tuple(ans)
    def from_block(bid,parent_a):
        assert bid not in seen_blocks, 'Block-cut overlap is not a tree'
        seen_blocks.add(bid)
        vertices=tuple(sorted(blocks[bid])); es=block_triples[bid]
        boundary=() if parent_a is None else (parent_a,)
        cover=min_relative_two_cover(es,vertices,boundary,stats)
        stats['max_cover']=max(stats['max_cover'],len(cover))
        child_messages={u:from_articulation(u,bid) for u in vertices
                        if u!=parent_a and len(belongs[u])>1}
        answers=[]
        parent_colors=(None,) if parent_a is None else range(5)
        for fixed in parent_colors:
            result=0
            for cs in itertools.product(range(5),repeat=len(cover)):
                colors=dict(zip(cover,cs))
                if parent_a is not None: colors[parent_a]=fixed
                outside=[u for u in vertices if u not in colors]
                unary={u:[1]*5 for u in outside}
                constant=1
                for triple in es:
                    free=[u for u in triple if u not in colors]
                    assert len(free)<=1
                    if not free:
                        constant*=W(tuple(colors[u] for u in triple))
                    else:
                        u=free[0]
                        for c in range(5):
                            unary[u][c]*=W(tuple(c if x==u else colors[x] for x in triple))
                if constant:
                    for u,msg in child_messages.items():
                        if u in colors: constant*=msg[colors[u]]
                        else:
                            for c in range(5): unary[u][c]*=msg[c]
                    for u in outside: constant*=sum(unary[u])
                result+=constant
                stats['evaluated_colorings']+=1
            answers.append(result)
        return answers[0] if parent_a is None else tuple(answers)
    total=5**sum(not belongs[u] for u in range(h))
    for bid in range(len(blocks)):
        if bid not in seen_blocks:
            total*=from_block(bid,None)
    return total,'block-tree-gluing',stats

def brute(n,arcs):
    if n>9: raise ValueError('only small n')
    return sum(all(R(x[u],x[v]) for u,v in arcs) for x in itertools.product(range(5),repeat=n))

def chain(r):
    """r triangles sharing successive articulation hubs, each with private sink."""
    arcs=[]; hubs=2*r+1
    for j in range(r):
        sink=hubs+j
        for u in (2*j,2*j+1,2*j+2): arcs.append((u,sink))
    return 3*r+1,arcs

def hub_star(r):
    """r petals each with shared central hub; control for prior 077."""
    arcs=[]; hubs=2*r+1
    for j in range(r):
        sink=hubs+j
        for u in (0,2*j+1,2*j+2): arcs.append((u,sink))
    return 3*r+1,arcs

def audit(seed=202611172124):
    rng=random.Random(seed); checks=0; by_route=collections.Counter()
    for n in range(0,7):
        for i in range(10):
            arcs=[(u,v) for u in range(n) for v in range(n)
                  if u!=v and rng.random()<0.14]
            z,route,_=tree_count(n,arcs); assert z==brute(n,arcs)
            checks+=1;by_route[route]+=1
    for k in range(3,7):
        for i in range(10):
            m=rng.randrange(0,5)
            triples=[tuple(rng.sample(range(k),3)) for _ in range(m)]
            arcs=[(u,k+j) for j,e in enumerate(triples) for u in e]
            z,route,_=tree_count(k+m,arcs)
            expected=sum(__import__('math').prod(W(tuple(x[u] for u in e)) for e in triples)
                         for x in itertools.product(range(5),repeat=k))
            assert z==expected and route=='block-tree-gluing'
            checks+=1;by_route[route]+=1
    for r in (1,2,3,4,5,7,15,40):
        n,arcs=chain(r)
        z,route,stats=tree_count(n,arcs)
        assert z==5*8**r and route=='block-tree-gluing'
        assert stats['blocks']==r and stats['max_cover']<=2
        if r<=2: assert z==brute(n,arcs)
        checks+=1;by_route[route]+=1
    for r in (1,2,3,4,12,30):
        n,arcs=hub_star(r)
        z,route,stats=tree_count(n,arcs)
        assert z==5*8**r and stats['blocks']==r
        if r<=2: assert z==brute(n,arcs)
        checks+=1;by_route[route]+=1
    # Adversarial duplicate sink triples, isolated hubs, disconnected blocks,
    # reversed arcs (fallback), loops, fully labeled empty graph.
    special=[(6,[(0,3),(1,3),(2,3),(0,4),(1,4),(2,4)]),
             (8,[(0,5),(1,5),(2,5),(2,6),(3,6),(4,6)]),
             (5,[(0,3),(1,3),(2,3),(3,4)]),
             (5,[(0,0)]), (4,[]),
             (5,[(0,2),(2,3),(3,4),(0,4),(4,1)]) ]
    for n,arcs in special:
        assert tree_count(n,arcs)[0]==brute(n,arcs)
        checks+=1
    data={'revision':'TMR3_T5_TREE_ADHESION078_v1','seed':seed,'checks':checks,
          'routes':dict(sorted(by_route.items())),'failures':0,
          'chain40':str(tree_count(*chain(40))[0]),
          'star30':str(tree_count(*hub_star(30))[0]),
          'chain40_stats':tree_count(*chain(40))[2]}
    return data

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--audit',action='store_true'); ap.add_argument('--seed',type=int,default=202611172124)
    args=ap.parse_args()
    if args.audit: print(json.dumps(audit(args.seed),sort_keys=True))
    else:
        inp=json.load(sys.stdin)
        z,route,stats=tree_count(inp['n'],inp['arcs'])
        print(json.dumps({'count':str(z),'route':route,'diagnostics':stats},sort_keys=True))
