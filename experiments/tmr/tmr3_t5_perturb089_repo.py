"""TMR-3/089: exact T5 counting on all bipartite source digraphs.
Parameter: min vertex cover tau of missing cross edges in each component.
Runtime O(poly(N)*5^tau), space poly(N) on one sequential machine.
"""
from collections import deque
from itertools import product


def beat(x, y):
    return (y - x) % 5 in (1, 3)


def count(n, arcs):
    arcs = list(arcs)
    E = set(arcs)
    if any(u == v or (v, u) in E for u, v in E):
        return 0
    if any(not (0 <= u < n and 0 <= v < n) for u, v in E):
        raise ValueError("vertex out of range")
    adj = [set() for _ in range(n)]
    for u, v in E:
        adj[u].add(v)
        adj[v].add(u)
    side = [-1] * n
    comps = []
    for start in range(n):
        if side[start] != -1:
            continue
        side[start] = 0
        queue = deque([start]); U = []; V = []
        while queue:
            u = queue.popleft()
            (U if side[u] == 0 else V).append(u)
            for v in adj[u]:
                if side[v] == -1:
                    side[v] = 1 - side[u]; queue.append(v)
                elif side[v] == side[u]:
                    return sum(all(beat(colors[u], colors[v]) for u, v in E)
                               for colors in product(range(5), repeat=n))
        comps.append((U, V))

    def onto(nodes, S, domains):
        ans = 0; T = S
        while True:
            x = 1
            for u in nodes:
                x *= (domains[u] & T).bit_count()
            ans += x * (-1 if (S.bit_count() - T.bit_count()) % 2 else 1)
            if not T: return ans
            T = (T - 1) & S

    def solve(U, V):
        if not V: return 5
        missing = {u: [v for v in V if v not in adj[u]] for u in U}
        mv = {}; mu = {}
        for start in U:
            pred = {}; seen = {start}; queue = deque([start]); free = None
            while queue and free is None:
                u = queue.popleft()
                for v in missing[u]:
                    if v in pred: continue
                    pred[v] = u
                    if v not in mv:
                        free = v; break
                    nxt = mv[v]
                    if nxt not in seen: seen.add(nxt); queue.append(nxt)
            if free is not None:
                v = free
                while True:
                    u = pred[v]; old = mu.get(u)
                    mv[v] = u; mu[u] = v
                    if old is None: break
                    v = old
        seenU = set(U) - set(mu); seenV = set(); queue = deque(seenU)
        while queue:
            u = queue.popleft()
            for v in missing[u]:
                if mu.get(u) == v or v in seenV: continue
                seenV.add(v)
                if v in mv and mv[v] not in seenU:
                    seenU.add(mv[v]); queue.append(mv[v])
        C = sorted((set(U) - seenU) | seenV)
        assert len(C) == len(mv)
        assert all(u in C or v in C for u in U for v in missing[u])
        A = [u for u in U if u not in C]
        B = [v for v in V if v not in C]
        answer = 0
        assignments = ((0,) + z for z in product(range(5), repeat=len(C) - 1)) if C else [()]
        for vals in assignments:
            pin = dict(zip(C, vals))
            if any(not beat(pin[u], pin[v]) for u, v in E if u in pin and v in pin):
                continue
            domains = {}
            for v in A+B:
                domains[v] = sum(1 << y for y in range(5)
                    if all(beat(c, y) if (u, v) in E else
                           beat(y, c) if (v, u) in E else True
                           for u, c in pin.items()))
            if any(domains[v] == 0 for v in domains): continue
            if not A or not B:
                t = 1
                for v in A+B: t *= domains[v].bit_count()
                answer += t; continue
            cu = {}; cv = {}
            for u in A:
                signature = tuple((u, v) in E for v in B)
                cu.setdefault(signature, []).append(u)
            for v in B:
                signature = tuple((v, u) in E for u in A)
                cv.setdefault(signature, []).append(v)
            if len(cu) + len(cv) > 5: continue
            classes, other = (list(cu.values()), B) if len(cu) <= len(cv) else (list(cv.values()), A)
            Slist = [s for s in range(1, 32) if s.bit_count() <= 2]
            for family in product(Slist, repeat=len(classes)):
                t = 1
                for nodes, S in zip(classes, family): t *= onto(nodes, S, domains)
                if not t: continue
                for v in other:
                    opts = domains[v]
                    for nodes, S in zip(classes, family):
                        forward = (nodes[0], v) in E
                        opts &= sum(1 << y for y in range(5)
                            if all(beat(x, y) if forward else beat(y, x)
                                   for x in range(5) if (S >> x) & 1))
                    t *= opts.bit_count()
                    if not t: break
                answer += t
        return answer * (5 if C else 1)

    result = 1
    for U, V in comps: result *= solve(U, V)
    return result


def test():
    from random import Random
    r = Random(890210)
    for p, q in ((1, 1), (1, 2), (2, 2), (2, 3), (3, 3)):
        for _ in range(90):
            arcs = []
            for u in range(p):
                for v in range(p, p+q):
                    k = r.randrange(3)
                    if k == 1: arcs.append((u, v))
                    elif k == 2: arcs.append((v, u))
            expected = sum(all(beat(colors[u], colors[v]) for u,v in arcs)
                           for colors in product(range(5), repeat=p+q))
            assert count(p+q, arcs) == expected
    assert count(4, [(0,2),(0,3),(1,2)]) == 40
    assert count(6, [(u,3+v) if u==v else (3+v,u)
                     for u in range(3) for v in range(3)]) == 0
    assert count(3, [(0,1),(1,2),(2,0)]) == 15
    print('453 checks OK')

if __name__ == '__main__':
    test()
