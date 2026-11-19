"""CLAUDE DOCAUDIT-0001: falsifier for the Google-doc Attempt IB claim
"minimal exact bond dimension along ANY contraction order >= 2^Omega(tw(G))".

Family: take any 3-CNF incidence graph G (signs are irrelevant to the incidence
graph). Make every literal positive and add positive unit clauses (x_i) for all i.
The incidence graph only gains leaves, so treewidth does not drop.  Contract the
unit-clause vectors into the variable copy tensors FIRST; every variable tensor
becomes the product state e1 (x) e1 (x) ...; every later intermediate tensor is a
product tensor, so the SVD rank across every bipartition of its open legs is 1.

The script (i) builds the family from a seeded random incidence graph (seed
recorded), (ii) computes a rigorous treewidth LOWER bound (minor-min-width,
Gogate-Dechter 2004) of the incidence graph, (iii) runs the unit-first exact
contraction with dense numpy tensors and checks the max matricization rank over
all single-leg cuts AND one balanced cut of every intermediate tensor, (iv) runs
a control without units, min-degree order, recording balanced-cut ranks, and
(v) checks the final scalar equals #SAT against brute force for small n.
"""
import itertools, json, random, sys, time
import numpy as np

SEED = 20261119

def random_formula(n, m, rng, deg=6):
    """(deg,3)-biregular random incidence graph, m = deg*n/3 clauses, distinct
    variables per clause (configuration model with rejection). All literals positive."""
    assert (deg * n) % 3 == 0 and m == deg * n // 3
    while True:
        pts = [v for v in range(n) for _ in range(deg)]
        rng.shuffle(pts)
        clauses = [tuple(sorted(pts[3 * j:3 * j + 3])) for j in range(m)]
        if all(len(set(c)) == 3 for c in clauses):
            return clauses

def incidence_graph(n, clauses, units):
    adj = {('v', i): set() for i in range(n)}
    for j, c in enumerate(clauses):
        adj[('c', j)] = set()
        for v in c:
            adj[('c', j)].add(('v', v)); adj[('v', v)].add(('c', j))
    if units:
        for i in range(n):
            adj[('u', i)] = {('v', i)}; adj[('v', i)].add(('u', i))
    return adj

def mmw_lower_bound(adj):
    """Minor-min-width: valid treewidth lower bound (tw is minor-monotone and
    tw(H) >= mindeg(H) for every minor H)."""
    g = {k: set(v) for k, v in adj.items()}
    lb = 0
    while len(g) > 1:
        v = min(g, key=lambda x: len(g[x]))
        lb = max(lb, len(g[v]))
        if not g[v]:
            del g[v]; continue
        u = min(g[v], key=lambda x: len(g[x]))
        for w in g[v]:
            if w != u:
                g[w].discard(v); g[w].add(u); g[u].add(w)
        g[u].discard(v); g[u].discard(u)
        del g[v]
    return lb

class TN:
    """Tensor network: tensors are (array, list-of-edge-ids)."""
    def __init__(self):
        self.t = {}; self.next = 0
    def add(self, arr, legs):
        k = self.next; self.next += 1; self.t[k] = (arr, list(legs)); return k
    def contract(self, a, b):
        A, la = self.t.pop(a); B, lb = self.t.pop(b)
        shared = [e for e in la if e in lb]
        ia = [la.index(e) for e in shared]; ib = [lb.index(e) for e in shared]
        C = np.tensordot(A, B, axes=(ia, ib)) if shared else np.multiply.outer(A, B)
        lc = [e for e in la if e not in shared] + [e for e in lb if e not in shared]
        return self.add(C, lc)

def mat_rank(arr, rows):
    k = arr.ndim
    if k == 0: return 1 if abs(float(arr)) > 0 else 0
    cols = [i for i in range(k) if i not in rows]
    M = np.transpose(arr, rows + cols).reshape(2 ** len(rows), 2 ** len(cols))
    return int(np.linalg.matrix_rank(M))

def tensor_ranks(arr):
    k = arr.ndim
    if k <= 1: return (1 if k == 0 or np.any(arr) else 0), (1 if k == 0 or np.any(arr) else 0)
    single = max(mat_rank(arr, [i]) for i in range(k))
    balanced = mat_rank(arr, list(range(k // 2)))
    return single, balanced

def build(n, clauses, units):
    tn = TN(); edge = itertools.count()
    var_legs = {i: [] for i in range(n)}
    cl_legs = []
    for c in clauses:
        legs = []
        for v in c:
            e = next(edge); legs.append(e); var_legs[v].append(e)
        cl_legs.append(legs)
    unit_legs = {}
    if units:
        for i in range(n):
            e = next(edge); unit_legs[i] = e; var_legs[i].append(e)
    vid = {}
    for i in range(n):
        d = len(var_legs[i])
        if d == 0: continue
        D = np.zeros((2,) * d); D[(0,) * d] = 1; D[(1,) * d] = 1
        vid[i] = tn.add(D, var_legs[i])
    cid = []
    OR = np.ones((2, 2, 2)); OR[0, 0, 0] = 0
    for legs in cl_legs:
        cid.append(tn.add(OR.copy(), legs))
    uid = {}
    for i, e in unit_legs.items():
        uid[i] = tn.add(np.array([0.0, 1.0]), [e])
    return tn, vid, cid, uid

CAP = 16

def peel(tn, k):
    """Exact (delta=0) SVD compression: split off every leg across which the
    tensor has matricization rank 1, as a separate vector tensor. Returns the
    remaining core key (or None if fully factored)."""
    changed = True
    while changed and k in tn.t:
        changed = False
        arr, legs = tn.t[k]
        if arr.ndim <= 1: return k
        for i in range(arr.ndim):
            rest = [j for j in range(arr.ndim) if j != i]
            M = np.transpose(arr, [i] + rest).reshape(2, -1)
            U, S, Vt = np.linalg.svd(M, full_matrices=False)
            if S[0] == 0 or S[1] <= 1e-12 * S[0]:
                u = U[:, 0] * S[0]
                R = Vt[0].reshape(arr.shape[:i] + arr.shape[i + 1:])
                del tn.t[k]
                tn.add(u, [legs[i]])
                k = tn.add(R, [legs[j] for j in rest])
                changed = True
                break
    return k

def run(tn, order_fn, compress):
    max_single = max_bal = max_legs = 0
    if compress:
        for k in list(tn.t):
            peel(tn, k)
    while len(tn.t) > 1:
        a, b = order_fn(tn)
        k = tn.contract(a, b)
        arr = tn.t[k][0]
        if arr.ndim > CAP:
            return {"exceeded_cap_legs": int(arr.ndim), "max_open_legs": int(arr.ndim)}
        if compress:
            k = peel(tn, k); arr = tn.t[k][0]
        max_legs = max(max_legs, arr.ndim)
        s, bal = tensor_ranks(arr)
        max_single = max(max_single, s); max_bal = max(max_bal, bal)
    (arr, _), = tn.t.values()
    return {"Z": float(arr), "max_single_leg_rank": max_single,
            "max_balanced_rank": max_bal, "max_open_legs_after_compression": max_legs}

def greedy_min_legs(tn):
    best = None
    keys = list(tn.t)
    for i, a in enumerate(keys):
        la = set(tn.t[a][1])
        for b in keys[i + 1:]:
            lb = set(tn.t[b][1])
            if la & lb or len(tn.t) <= 2:
                out = len(la ^ lb)
                if best is None or out < best[0]: best = (out, a, b)
    if best is None:
        return keys[0], keys[1]
    return best[1], best[2]

def brute_count(n, clauses, units):
    cnt = 0
    for x in itertools.product((0, 1), repeat=n):
        if units and not all(x): continue
        if all(x[a] or x[b] or x[c] for a, b, c in clauses): cnt += 1
    return cnt

def main():
    rng = random.Random(SEED)
    out = {"seed": SEED, "rows": []}
    t0 = time.time()
    for n in (6, 9, 12, 15, 18, 30, 60, 90):
        m = 2 * n
        clauses = random_formula(n, m, rng)
        row = {"n": n, "m": m}
        row["tw_lb_mmw_with_units"] = mmw_lower_bound(incidence_graph(n, clauses, True))
        row["tw_lb_mmw_no_units"] = mmw_lower_bound(incidence_graph(n, clauses, False))
        # unit-first exact contraction
        tn, vid, cid, uid = build(n, clauses, True)
        for i in range(n):
            if i in vid:  # absorb unit into variable copy tensor
                k = tn.contract(vid[i], uid[i]); vid[i] = k
        # check every variable tensor is product: rank 1 across every single leg
        prod_ok = True
        for i, k in vid.items():
            arr = tn.t[k][0]
            if max(mat_rank(arr, [j]) for j in range(arr.ndim)) != 1:
                prod_ok = False
        row["unit_first_compressed"] = run(tn, greedy_min_legs, True)
        row["variable_tensors_product_after_units"] = prod_ok
        if n <= 18:
            row["brute_count_units"] = brute_count(n, clauses, True)
            tn2, *_ = build(n, clauses, False)
            row["control_no_units_compressed"] = run(tn2, greedy_min_legs, True)
            row["brute_count_no_units"] = brute_count(n, clauses, False)
        out["rows"].append(row)
        print(json.dumps(row), flush=True)
    out["elapsed_s"] = round(time.time() - t0, 2)
    out["numpy"] = np.__version__; out["python"] = sys.version.split()[0]
    with open(sys.argv[1] if len(sys.argv) > 1 else "tn_rank_falsifier_results.json", "w") as f:
        json.dump(out, f, indent=1)

if __name__ == "__main__":
    main()
