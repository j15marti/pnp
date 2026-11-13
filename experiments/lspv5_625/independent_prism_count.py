"""LSPV-5/625 independent recount of the LSPV-1/620 prism family F_k.
Built ONLY from the prose definition in the /620 report (not its compiler):
prism C_k x K_2, top ring T_i, bottom ring B_i, spokes T_i B_i;
t = T_0, s = B_r with r = floor(k/2); q(T_1)=1, all other q=0;
at t and s only the two ring edges carry the parity equation (spoke omitted
from the equation but still one of the three clause variables).
Each vertex: 4 width-3 clauses forbidding the 4 local patterns that violate
its equation. Brute force over all 2^E assignments (numpy, chunked).
Usage: /usr/bin/python3 independent_prism_count.py 6 7 8  -> JSON on stdout. k<=8 keeps
each run under ~30 s (AGENTS.md runtime rule)."""
import sys, json, itertools, numpy as np

def build(k):
    T = lambda i: i % k
    B = lambda i: k + i % k
    edges = [(T(i), T(i+1)) for i in range(k)] + [(B(i), B(i+1)) for i in range(k)] + [(T(i), B(i)) for i in range(k)]
    V, E = 2*k, 3*k
    inc = [[] for _ in range(V)]
    for e, (a, b) in enumerate(edges):
        inc[a].append(e); inc[b].append(e)
    t, s = T(0), B(k//2)
    q = [0]*V; q[T(1)] = 1
    spoke = lambda v: 2*k + (v if v < k else v-k)
    cons = []  # (vertex, edge triple, parity mask over triple, rhs)
    for v in range(V):
        trip = sorted(inc[v])
        mask = [0 if (v in (t, s) and e == spoke(v)) else 1 for e in trip]
        cons.append((v, trip, mask, q[v]))
    return V, E, cons

def count(k, chunk_bits=20):
    V, E, cons = build(k)
    nclauses = 4*V
    models = 0
    wit = np.zeros((V, 8), dtype=np.int64)  # witnesses for clause (v, forbidden pattern)
    lo_bits = min(E, chunk_bits)
    lo = np.arange(1 << lo_bits, dtype=np.int64)
    for hi in range(1 << (E - lo_bits)):
        x = lo | (np.int64(hi) << lo_bits)
        pats, oks = [], []
        for (v, trip, mask, rhs) in cons:
            b = [(x >> e) & 1 for e in trip]
            pat = b[0] | (b[1] << 1) | (b[2] << 2)
            par = (b[0]*mask[0]) ^ (b[1]*mask[1]) ^ (b[2]*mask[2])
            pats.append(pat); oks.append(par == rhs)
        oks = np.array(oks)
        allok = oks.all(axis=0)
        models += int(allok.sum())
        nbad = (~oks).sum(axis=0)
        for i in range(V):
            sel = (nbad == 1) & (~oks[i])
            if sel.any():
                wit[i] += np.bincount(pats[i][sel], minlength=8)
    # forbidden patterns per vertex = exactly 4 per vertex
    per_clause = []
    for (v, trip, mask, rhs) in cons:
        for p in range(8):
            b = [(p >> j) & 1 for j in range(3)]
            if (b[0]*mask[0]) ^ (b[1]*mask[1]) ^ (b[2]*mask[2]) != rhs:
                per_clause.append(int(wit[v][p]))
    assert len(per_clause) == nclauses
    return {"k": k, "V": V, "E": E, "clauses": nclauses, "models": models,
            "deletion_witnesses_min": min(per_clause), "deletion_witnesses_max": max(per_clause),
            "claimed_models": 2**k, "claimed_deletion": 2**(k-2),
            "match": models == 2**k and min(per_clause) == max(per_clause) == 2**(k-2)}

if __name__ == "__main__":
    ks = [int(a) for a in sys.argv[1:]] or [6, 7]
    print(json.dumps([count(k) for k in ks], indent=1))
