#!/usr/bin/env python3
"""Independent spot checks of two claims in the reviewed window.
(1) T3-10 (bf4d3a1): Fano-minus-line block, triples (0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)
    with NAE on each: every satisfying 7-bit word has x0=x1=x2, both colours occur; and
    every unordered pair lies in at most one triple (pair uniqueness used for the width-2 RUP stall).
(2) T3 coupled colouring (7338d0c): base B = k x k grid + chord between opposite corners has
    odd girth 2k-1 and is triangle-free; Mycielskian M(B) is triangle-free and NOT 3-colourable
    (CaDiCaL on the standard one-hot CNF) for k = 4, 6.
"""
import itertools, collections
from pysat.solvers import Solver
T = [(0,3,4),(0,5,6),(1,3,5),(1,4,6),(2,3,6),(2,4,5)]
sat = [w for w in range(128) if all(len({(w>>i)&1 for i in tr}) == 2 for tr in T)]
mono = all(((w>>0)&1) == ((w>>1)&1) == ((w>>2)&1) for w in sat)
cols = {(w & 1) for w in sat}
pairs = collections.Counter(p for tr in T for p in itertools.combinations(tr, 2))
print("Fano-minus-line: satisfying words", len(sat), "omitted line monochromatic:", mono,
      "both colours:", cols == {0, 1}, "max pair multiplicity:", max(pairs.values()))
def grid_chord(k):
    V = [(i, j) for i in range(k) for j in range(k)]
    E = set()
    for (i, j) in V:
        if i + 1 < k: E.add(((i, j), (i + 1, j)))
        if j + 1 < k: E.add(((i, j), (i, j + 1)))
    E.add(((0, 0), (k - 1, k - 1)))
    return V, E
def odd_girth(V, E):
    adj = collections.defaultdict(set)
    for a, b in E: adj[a].add(b); adj[b].add(a)
    best = None
    for s in V:   # shortest odd closed walk through s via BFS on the bipartite double cover
        dist = {(s, 0): 0}; dq = collections.deque([(s, 0)])
        while dq:
            u, p = dq.popleft()
            for w in adj[u]:
                if (w, 1 - p) not in dist:
                    dist[(w, 1 - p)] = dist[(u, p)] + 1; dq.append((w, 1 - p))
        if (s, 1) in dist and (best is None or dist[(s, 1)] < best): best = dist[(s, 1)]
    return best
def mycielski(V, E):
    idx = {v: i for i, v in enumerate(V)}; n = len(V)
    EE = set()
    for a, b in E:
        a, b = idx[a], idx[b]
        EE.add((a, b)); EE.add((a, n + b)); EE.add((b, n + a))
    for i in range(n): EE.add((n + i, 2 * n))
    return 2 * n + 1, EE
def triangle_free(N, E):
    adj = collections.defaultdict(set)
    for a, b in E: adj[a].add(b); adj[b].add(a)
    return not any(adj[a] & adj[b] for a, b in E)
for k in (4, 6):
    V, E = grid_chord(k)
    N, EE = mycielski(V, E)
    var = lambda v, c: 3 * v + c + 1
    cls = []
    for v in range(N):
        cls.append([var(v, c) for c in range(3)])
        cls += [[-var(v, a), -var(v, b)] for a, b in itertools.combinations(range(3), 2)]
    for a, b in EE:
        cls += [[-var(a, c), -var(b, c)] for c in range(3)]
    with Solver(name='cadical153', bootstrap_with=cls) as s:
        r = s.solve()
    print(f"k={k}: base odd girth {odd_girth(V, E)} (claim {2*k-1}), base triangle-free "
          f"{triangle_free(len(V), {(V.index(a), V.index(b)) for a, b in E})}, M(B) vertices {N} "
          f"(claim {2*k*k+1}), triangle-free {triangle_free(N, EE)}, 3-colourable {r}")
