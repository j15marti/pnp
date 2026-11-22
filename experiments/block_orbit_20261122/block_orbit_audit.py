"""Degree-cover residual solver and independent finite oracle. Python 3 standard library.

Standalone block-orbit continuation audit. Run this file with Python 3.
Core degree-cover routines adapted from j15marti/pnp commit
5ec5f7417142d1a5d065fdc533cbba417822d004,
experiments/dynamic_synthesis_hub_cover_20261122.py, blob
1fd99d6715d15bb8883bc9b839680512620b9a74.
The new audit checks block gluing, support masks, erasure, and witnesses.
No polynomial claim is made for the independent oracle.
"""
import json
import random
from collections import Counter
from itertools import combinations, permutations, product

P = tuple(permutations(range(3)))
SIGN = {p: sum(p[i] > p[j] for i, j in combinations(range(3), 2)) % 2 for p in P}
STATS = Counter()

def compatible(u, f, v, g, match):
    if u > v:
        u, f, v, g = v, g, u, f
    p = match.get((u, v))
    return p is None or all(f[a] != g[p[a]] for a in range(3))

def blocks(vertices, adj):
    """Tarjan edge blocks, including bridges; isolated vertices handled separately."""
    depth, low, stack, out = {}, {}, [], []
    def visit(v, parent):
        depth[v] = low[v] = len(depth)
        for u in sorted(adj[v]):
            if u == parent:
                continue
            if u not in depth:
                stack.append((v, u))
                visit(u, v)
                low[v] = min(low[v], low[u])
                if low[u] >= depth[v]:
                    edges = []
                    while True:
                        edge = stack.pop()
                        edges.append(edge)
                        if edge == (v, u):
                            break
                    out.append(edges)
            elif depth[u] < depth[v]:
                stack.append((v, u))
                low[v] = min(low[v], depth[u])
    for v in sorted(vertices):
        if v not in depth:
            visit(v, None)
    return out

def exceptional(block):
    degree = Counter(x for e in block for x in e)
    size = len(degree)
    return len(block) == size*(size-1)//2 or all(d == 2 for d in degree.values())

def eliminate(vertices, adj, lists, match):
    """Exact Boolean variable elimination on clique/cycle block graphs."""
    graph = {v: set(adj[v]) for v in vertices}
    factors = [((v,), {(p,) for p in lists[v]}) for v in vertices]
    for u in vertices:
        for v in adj[u]:
            if u < v:
                factors.append(((u, v), {(f,g) for f in lists[u] for g in lists[v]
                                          if compatible(u,f,v,g,match)}))
    while graph:
        choices = [v for v in graph if len(graph[v]) <= 2 or
                   (len(graph[v]) <= 3 and all(b in graph[a] for a,b in combinations(graph[v],2)))]
        assert choices, 'GDP block elimination invariant failed'
        v = min(choices)
        neighbors = tuple(sorted(graph[v]))
        STATS['max_elimination_width'] = max(STATS['max_elimination_width'],len(neighbors))
        picked = [(s,t) for s,t in factors if v in s]
        factors = [(s,t) for s,t in factors if v not in s]
        table = set()
        for row in product(*(lists[u] for u in neighbors)):
            a = dict(zip(neighbors,row))
            for color in lists[v]:
                a[v] = color
                if all(tuple(a[u] for u in scope) in values for scope,values in picked):
                    table.add(row)
                    break
        if not table:
            return False
        factors.append((neighbors,table))
        for a,b in combinations(neighbors,2):
            graph[a].add(b)
            graph[b].add(a)
        for u in neighbors:
            graph[u].remove(v)
        del graph[v]
    return all(() in table for scope,table in factors)

def residual(vertices, lists, match):
    adj = {v:set() for v in vertices}
    for u,v in match:
        if u in adj and v in adj:
            adj[u].add(v)
            adj[v].add(u)
    assert all(len(lists[v]) >= len(adj[v]) for v in vertices)
    unseen = set(vertices)
    while unseen:
        root = min(unseen)
        component, todo = {root}, [root]
        unseen.remove(root)
        while todo:
            for v in adj[todo.pop()]:
                if v in unseen:
                    unseen.remove(v)
                    component.add(v)
                    todo.append(v)
        if any(not exceptional(b) for b in blocks(component,adj)):
            STATS['non_GDP_components_accepted'] += 1
            continue
        STATS['GDP_components_decided'] += 1
        if not eliminate(component,adj,lists,match):
            return False
    return True

def solve(q, match):
    adj = [set() for _ in range(q)]
    for u,v in match:
        adj[u].add(v)
        adj[v].add(u)
    signs = {}
    for root in range(q):
        if root in signs:
            continue
        signs[root] = 0
        todo = [root]
        while todo:
            u = todo.pop()
            for v in sorted(adj[u]):
                z = signs[u] ^ SIGN[match[min(u,v),max(u,v)]]
                if v in signs:
                    if signs[v] != z:
                        return False
                else:
                    signs[v] = z
                    todo.append(v)
    lists = {v: tuple(p for p in P if SIGN[p] == signs[v]) for v in range(q)}
    hubs = tuple(v for v in range(q) if len(adj[v]) >= 4)
    rest = set(range(q))-set(hubs)
    for row in product(*(lists[v] for v in hubs)):
        fixed = dict(zip(hubs,row))
        if any(not compatible(u,fixed[u],v,fixed[v],match) for u,v in combinations(hubs,2)):
            continue
        remaining = {v: tuple(f for f in lists[v] if all(compatible(u,g,v,f,match)
                       for u,g in fixed.items())) for v in rest}
        if residual(rest,remaining,match):
            return True
    return False

def oracle(q, match):
    """Independent six-permutation backtracking, with no parity or DP theorem."""
    chosen = {}
    def dfs(v):
        if v == q:
            return True
        for f in P:
            if all(compatible(u,g,v,f,match) for u,g in chosen.items()):
                chosen[v] = f
                if dfs(v+1):
                    return True
                del chosen[v]
        return False
    return dfs(0)

def relabel(q, match, rng):
    labels = [rng.choice(P) for _ in range(q)]
    result = {}
    for (u,v),p in match.items():
        perm = [0]*3
        for a in range(3):
            perm[labels[u][a]] = labels[v][p[a]]
        result[u,v] = tuple(perm)
    return result

import hashlib
import time
from pathlib import Path

ROTATIONS = ((0,1,2),(1,2,0),(2,0,1))
NEW = Counter()

def adjacency(q, match):
    a = {v:set() for v in range(q)}
    for u,v in match:
        a[u].add(v); a[v].add(u)
    return a

def edge_blocks(q, match):
    a=adjacency(q,match)
    return blocks(set(range(q)),a)

def local_instance(edges, match):
    vertices=tuple(sorted({v for e in edges for v in e}))
    ren={v:i for i,v in enumerate(vertices)}
    local={tuple(sorted((ren[u],ren[v]))):match[min(u,v),max(u,v)]
           for u,v in edges}
    return vertices,local

def block_decision(q, match):
    for edges in edge_blocks(q,match):
        vertices,local=local_instance(edges,match)
        NEW['block_calls']+=1
        if not solve(len(vertices),local):
            return False
    return True

def normalized_lists(q, match):
    a=adjacency(q,match)
    signs={}
    for root in range(q):
        if root in signs: continue
        signs[root]=0
        todo=[root]
        while todo:
            u=todo.pop()
            for v in a[u]:
                value=signs[u]^SIGN[match[min(u,v),max(u,v)]]
                if v in signs and signs[v]!=value:
                    return None
                if v not in signs:
                    signs[v]=value; todo.append(v)
    return {v:tuple(p for p in P if SIGN[p]==signs[v]) for v in range(q)}

def local_witness(q, match):
    lists=normalized_lists(q,match)
    if lists is None: return None
    a=adjacency(q,match)
    hubs=tuple(v for v in range(q) if len(a[v])>=4)
    rest=set(range(q))-set(hubs)
    for row in product(*(lists[v] for v in hubs)):
        fixed=dict(zip(hubs,row))
        if any(not compatible(u,fixed[u],v,fixed[v],match)
               for u,v in combinations(hubs,2)): continue
        remaining={v:tuple(f for f in lists[v]
                    if all(compatible(u,g,v,f,match) for u,g in fixed.items()))
                   for v in rest}
        if not residual(rest,remaining,match): continue
        chosen=dict(fixed)
        live=set(rest)
        while live:
            v=min(live); next_live=live-{v}
            found=False
            for f in remaining[v]:
                trial={u:tuple(g for g in remaining[u]
                        if compatible(v,f,u,g,match)) for u in next_live}
                NEW['witness_decision_calls']+=1
                if residual(next_live,trial,match):
                    chosen[v]=f
                    live=next_live
                    remaining=trial
                    found=True
                    break
            assert found,'Witness self-reduction lost all extensions'
        assert all(compatible(u,chosen[u],v,chosen[v],match) for u,v in match)
        return chosen
    return None

def block_witness(q, match):
    raw=edge_blocks(q,match)
    data=[]; memberships={v:[] for v in range(q)}
    for i,edges in enumerate(raw):
        vertices,local=local_instance(edges,match)
        w=local_witness(len(vertices),local)
        if w is None: return None
        mapped={v:w[j] for j,v in enumerate(vertices)}
        data.append((vertices,mapped))
        for v in vertices: memberships[v].append(i)
    chosen={}; done=set()
    def visit(i,attachment=None):
        if i in done:return
        done.add(i)
        vertices,w=data[i]
        if attachment is None:
            color_map=(0,1,2)
        else:
            source=w[attachment]; target=chosen[attachment]
            color_map=tuple(target[source.index(c)] for c in range(3))
        for v in vertices:
            f=tuple(color_map[c] for c in w[v])
            if v in chosen: assert chosen[v]==f
            chosen[v]=f
        for v in vertices:
            for child in memberships[v]:
                if child not in done:visit(child,v)
    for i in range(len(data)):
        if i not in done:visit(i)
    for v in range(q):chosen.setdefault(v,P[0])
    assert all(compatible(u,chosen[u],v,chosen[v],match) for u,v in match)
    return chosen

def count_with_lists(q, match, lists, fixed=None):
    fixed=fixed or {}
    chosen={}; counts=0
    def visit(v):
        nonlocal counts
        if v==q:
            counts+=1; return
        for f in ((fixed[v],) if v in fixed else lists[v]):
            if f not in lists[v]:continue
            if all(compatible(u,g,v,f,match) for u,g in chosen.items()):
                chosen[v]=f;visit(v+1);del chosen[v]
    visit(0)
    return counts

def support(q,match,boundary,pins):
    lists=normalized_lists(q,match)
    if lists is None:return set()
    out=set()
    for f in lists[boundary]:
        fixed=dict(pins);fixed[boundary]=f
        if count_with_lists(q,match,lists,fixed):
            out.add(f)
    return out

def glue(template_a,template_b):
    qa,ea=template_a;qb,eb=template_b
    map_b={0:0,**{v:qa+v-1 for v in range(1,qb)}}
    edges=set(ea)|{tuple(sorted((map_b[u],map_b[v]))) for u,v in eb}
    return qa+qb-1,tuple(sorted(edges))

def prism_chain(b,terminal=None):
    assert b>=1
    prism=((0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4),(2,5))
    q=0; match={}; attach=None
    for i in range(b):
        if attach is None:
            labels=list(range(6));q=6
        else:
            labels=[attach]+list(range(q,q+5));q+=5
        for u,v in prism:
            edge=tuple(sorted((labels[u],labels[v])))
            match[edge]=P[0]
        attach=labels[5]
    if terminal is not None:
        labels=[attach]+list(range(q,q+3));q+=3
        for u,v in combinations(range(4),2):
            match[tuple(sorted((labels[u],labels[v])))]=P[0] if terminal=='UNSAT' else ROTATIONS[1]
    return q,match

def source_dimensions(q,k):
    n=33*q+9*k;m=21*q+9*k;w=n.bit_length()
    N=n+2+2*((m+1).bit_length()-1)+3*m*w
    return {'q':q,'k':k,'n':n,'m':m,'N':N}

def main_new():
    started=time.perf_counter();rng=random.Random(2026112201)
    # Check every permutation edge under every even global color rotation.
    for p,f,g,r in product(P,P,P,ROTATIONS):
        rf=tuple(r[c] for c in f);rg=tuple(r[c] for c in g)
        assert compatible(0,f,1,g,{(0,1):p})==compatible(0,rf,1,rg,{(0,1):p})
        assert SIGN[rf]==SIGN[f] and SIGN[rg]==SIGN[g]
        NEW['rotation_checks']+=1
    templates=[
        (2,((0,1),)),
        (3,((0,1),(1,2),(0,2))),
        (4,tuple(combinations(range(4),2))),
        (6,((0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4),(2,5))),
        (5,tuple(sorted({tuple(sorted((i,(i+1)%4))) for i in range(4)}
                       |{(i,4) for i in range(4)}))),
    ]
    labels=Counter()
    for ia,ta in enumerate(templates):
        for ib,tb in enumerate(templates):
            if ta[0]+tb[0]-1>10:continue
            q,edges=glue(ta,tb)
            for mode in range(12):
                choices=P if mode%4==1 else ROTATIONS
                match={e:P[0] if mode==0 else rng.choice(choices) for e in edges}
                match=relabel(q,match,rng)
                got=block_decision(q,match)
                truth=oracle(q,match)
                assert got==truth,(ia,ib,mode,match)
                w=block_witness(q,match)
                assert (w is not None)==truth
                NEW['compound_oracle_cases']+=1
                labels['SAT' if truth else 'UNSAT']+=1
                # For every block, test its normalized unary projections and count product.
                global_lists=normalized_lists(q,match)
                if global_lists is None:continue
                raw=edge_blocks(q,match)
                numerator=1
                for bedges in raw:
                    vs,lmatch=local_instance(bedges,match)
                    blists={i:global_lists[v] for i,v in enumerate(vs)}
                    total=count_with_lists(len(vs),lmatch,blists)
                    one=[count_with_lists(len(vs),lmatch,blists,{0:f}) for f in blists[0]]
                    assert one[0]==one[1]==one[2] and sum(one)==total
                    numerator*=total
                    NEW['uniform_projection_checks']+=1
                total=count_with_lists(q,match,global_lists)
                assert numerator==total*3**(len(raw)-1)
                NEW['count_factorization_checks']+=1
    # Every 3-bit unary support mask is realizable by pinned leaves.
    masks={}
    for bits in range(8):
        allowed={ROTATIONS[c] for c in range(3) if bits>>c&1}
        forbidden=[c for c in range(3) if not bits>>c&1]
        match={(0,i+1):P[0] for i in range(len(forbidden))}
        pins={i+1:ROTATIONS[c] for i,c in enumerate(forbidden)}
        actual=support(len(forbidden)+1,match,0,pins)
        assert actual==allowed
        masks[bits]=actual
        NEW['support_masks']+=1
    for a,b in permutations(range(8),2):
        c=next(iter(masks[a]^masks[b]))
        assert bool(masks[a]&{c})!=bool(masks[b]&{c})
        NEW['context_distinctions']+=1
    # Two individually feasible pinned triangles need joint supports at their articulation.
    bow={(0,1):P[0],(0,2):P[0],(1,2):P[0],
         (0,3):P[0],(0,4):P[0],(3,4):P[0]}
    pins={1:ROTATIONS[1],2:ROTATIONS[2],3:ROTATIONS[0],4:ROTATIONS[2]}
    left=support(3,{e:p for e,p in bow.items() if max(e)<3},0,
                 {1:pins[1],2:pins[2]})
    right=support(3,{(0,1):P[0],(0,2):P[0],(1,2):P[0]},0,
                  {1:pins[3],2:pins[4]})
    assert left=={ROTATIONS[0]} and right=={ROTATIONS[1]} and not left&right
    assert not count_with_lists(5,bow,normalized_lists(5,bow),pins)
    # All 24 deletion orders: fixed-boundary support only grows and adds <=3 values.
    for order in permutations(pins):
        state=dict(pins);before=support(5,bow,0,state);added=0
        for v in order:
            del state[v];after=support(5,bow,0,state)
            assert before<=after
            added+=len(after-before);before=after
            NEW['erasure_steps']+=1
        assert added<=3 and len(before)==3
        NEW['erasure_orders']+=1
    families=[]
    for b in (1,2,4,8,16):
        for terminal in (None,'SAT','UNSAT'):
            q,match=prism_chain(b,terminal)
            a=adjacency(q,match)
            rs=[]
            for edges in edge_blocks(q,match):
                degree=Counter(v for e in edges for v in e)
                rs.append(sum(d>=4 for d in degree.values()))
            global_hubs=sum(len(a[v])>=4 for v in a)
            assert min(map(len,a.values()))==3 and all(r==0 for r in rs)
            assert global_hubs==(b-1 if terminal is None else b)
            assert block_decision(q,match)==(terminal!='UNSAT')
            witness=block_witness(q,match)
            assert (witness is not None)==(terminal!='UNSAT')
            if b<=2:
                assert oracle(q,match)==(terminal!='UNSAT')
                NEW['small_chain_oracle_cases']+=1
            row=source_dimensions(q,len(match))
            row.update({'prisms':b,'terminal':terminal,'global_hubs':global_hubs,
                        'max_block_hubs':max(rs),'blocks':len(rs),
                        'A':1+sum(3**r for r in rs),
                        'global_product_assignments':3**global_hubs})
            families.append(row)
    result={'status':'PASS','seed':2026112201,
            'counts':dict(sorted(NEW.items())),'compound_labels':dict(labels),
            'pinned_counterexample':{'left_support':[0],'right_support':[1],'joint_SAT':False},
            'families':families,'core_stats':dict(STATS),
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'elapsed_seconds':time.perf_counter()-started,
            'scope':'Finite quotient semantics, gluing/witnesses, normalized support and count identities. No native exact-one parser, physical tape, general SAT bound, or proof-kernel verification.'}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main_new()

