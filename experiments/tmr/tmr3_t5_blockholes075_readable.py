"""TMR-3/075: authenticated exact T5 counting with complete-block holes.
Input on stdin: unary n, 0, unary m, 0, then m low-first (u,v) pairs.
Prints the exact number of original T5 labellings and chosen method.
"""
import sys
from itertools import combinations
from collections import defaultdict
from math import comb


def parse(src):
    if set(src) - {'0', '1'}:
        raise ValueError('nonbinary input')
    p = 0
    def unary():
        nonlocal p
        i = p
        while p < len(src) and src[p] == '1': p += 1
        if p == len(src): raise ValueError('unterminated unary integer')
        p += 1
        return p-i-1
    n, m = unary(), unary()
    w = max(1, (max(2, n)-1).bit_length())
    if len(src)-p != 2*w*m: raise ValueError('incorrect length')
    edges = set()
    for _ in range(m):
        u = sum((src[p+i] == '1') << i for i in range(w))
        v = sum((src[p+w+i] == '1') << i for i in range(w))
        p += 2*w
        if u >= n or v >= n: raise ValueError('out of range')
        edges.add((u, v))
    return n, edges


def recognise(n, edges):
    incoming = [set() for _ in range(n)]
    outgoing = [set() for _ in range(n)]
    for u,v in edges:
        incoming[v].add(u); outgoing[u].add(v)
    hubs = [i for i in range(n) if not incoming[i] and outgoing[i]]
    sinks = [i for i in range(n) if not outgoing[i] and len(incoming[i]) == 3]
    k = len(hubs)
    if k < 3 or k+len(sinks) != n: return None
    ids = {v:i for i,v in enumerate(hubs)}
    present = []
    for v in sinks:
        if any(u not in ids for u in incoming[v]): return None
        present.append(tuple(sorted(ids[u] for u in incoming[v])))
    if len(present) != len(set(present)): return None
    present = set(present)
    pair_cover = set()
    for a,b,c in present:
        pair_cover.update(((a,b), (a,c), (b,c)))
    if len(pair_cover) != comb(k,2): return None
    missing = {t for t in combinations(range(k),3) if t not in present}
    adj = [set() for _ in range(k)]
    for a,b,c in missing:
        adj[a].update((b,c));adj[b].update((a,c));adj[c].update((a,b))
    unseen = set(range(k)); blocks = []
    while unseen:
        v = min(unseen); unseen.remove(v); q = [v]
        for x in q:
            for y in adj[x]:
                if y in unseen: unseen.remove(y);q.append(y)
        blocks.append(set(q))
    for block in blocks:
        if sum(t[0] in block for t in missing) != comb(len(block),3):
            return None
    return k, len(present), len(missing), [len(b) for b in blocks]


def exact_block_count(k, m, d, sizes):
    A = {(0,0):1}
    for s in sizes:
        nextA = defaultdict(int)
        for a in range(s+1):
            missing_mono = comb(a,3)+comb(s-a,3)
            multiplicity = comb(s,a)
            for (p,j), v in A.items():
                nextA[p+a,j+missing_mono] += v*multiplicity
        A = nextA
    answer = 5*(1 << m)
    for (p,j), weight in A.items():
        if 0 < p < k:
            answer += 5*weight*(1 << (comb(p,3)+comb(k-p,3)-j))
    return answer


def fallback(n, edges):
    # Root one spanning tree per weak component at colour 0;
    # 2 legal increments per tree edge and 5 translations per component.
    undirected = [set() for _ in range(n)]
    for u,v in edges:
        undirected[u].add(v);undirected[v].add(u)
    seen = set();parent = [-1]*n;order=[];roots=0
    for root in range(n):
        if root in seen: continue
        roots += 1; seen.add(root);q=[root]
        for u in q:
            for v in sorted(undirected[u]):
                if v not in seen:
                    seen.add(v);parent[v]=u;q.append(v)
        order.extend(q)
    nonroots = [v for v in order if parent[v] >= 0]
    answer = 0; mask = 0
    while mask < (1 << len(nonroots)):
        color = [0]*n
        for i,v in enumerate(nonroots):
            step = 3 if (mask >> i)&1 else 1
            if (parent[v],v) in edges:
                color[v] = (color[parent[v]] + step) % 5
            else:
                color[v] = (color[parent[v]] - step) % 5
        if all((color[v]-color[u])%5 in (1,3) for u,v in edges):
            answer += 1
        mask += 1
    return answer*(5**roots)


def solve(src):
    n, edges = parse(src)
    if any(u == v or (v,u) in edges for u,v in edges):
        return 0, 'contradiction'
    result = recognise(n, edges)
    if result:
        return exact_block_count(*result), 'block-complete'
    return fallback(n, edges), 'forest-fallback'


if __name__ == '__main__':
    data = sys.stdin.read().strip()
    try:
        count, method = solve(data)
    except ValueError as exc:
        print('INVALID SOURCE:', exc, file=sys.stderr)
        sys.exit(2)
    print(count)
    print(method, file=sys.stderr)
