#!/usr/bin/env python3
"""Regenerate the exact 150-variable, 176-clause native strict-C source.

Seeded source generation is only a structural fixture. UNSAT is independently
checked by two complete finite-domain C solvers in the reproducibility ZIP.
"""
import random
import json
import hashlib
from collections import deque

N = 150
SEED = 20
TRIALS = 30 * N
EXPECTED_SHA256 = "ecb0b31b1487f8747b582d97de26e2c77e4e1b5e173d89c4c86097e0fcd402a8"

def gen():
    r = random.Random(SEED)
    primal = [set() for _ in range(N)]
    out = []
    def far(a, b):
        if b in primal[a]:
            return False
        if any(b in primal[z] for z in primal[a]):
            return False
        return not any(b in primal[w] for z in primal[a] for w in primal[z])
    for _ in range(TRIALS):
        a, b, c = r.sample(range(N), 3)
        if not (far(a,b) and far(a,c) and far(b,c)):
            continue
        out.append((a,b,c))
        primal[a].update((b,c))
        primal[b].update((a,c))
        primal[c].update((a,b))
    return out

def incidence_girth(clauses):
    adj = [[] for _ in range(N+len(clauses))]
    for j, triple in enumerate(clauses):
        assert len(set(triple)) == 3
        for v in triple:
            adj[v].append(N+j)
            adj[N+j].append(v)
    girth = float("inf")
    for src in range(len(adj)):
        dist = [-1]*len(adj)
        parent = [-1]*len(adj)
        dist[src] = 0
        q = deque([src])
        while q:
            u = q.popleft()
            for v in adj[u]:
                if dist[v] == -1:
                    dist[v] = dist[u]+1
                    parent[v] = u
                    q.append(v)
                elif parent[u] != v:
                    girth = min(girth, dist[u]+dist[v]+1)
    return int(girth)

if __name__ == "__main__":
    clauses = gen()
    assert len(clauses) == 176
    assert incidence_girth(clauses) == 10
    filename = "candidate_150_176.json"
    with open(filename,"w") as f:
        json.dump({"n":N,"seed":SEED,"clauses":clauses}, f)
    h=hashlib.sha256(open(filename,"rb").read()).hexdigest()
    assert h == EXPECTED_SHA256, (h, EXPECTED_SHA256)
    print("SOURCE MATCH",filename,len(clauses),"clauses",h)
