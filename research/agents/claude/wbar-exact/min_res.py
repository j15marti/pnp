"""Exact minimum resolution refutation cost for small CNFs, with the best
derivation chosen for free (no search cost charged).

cost = number of resolution steps (distinct derived clauses; source clauses free).
  tree_min : tree-like resolution (= min decision-tree internal nodes, DP).
  dag_min  : general (DAG-like) resolution, exact iterative deepening over
             sets of derived clauses, enumerated in canonical greedy order.
Usage: python3 min_res.py IN.json OUT.jsonl START STOP   (chunk of formulas)
Each chunk is designed to finish within ~30 s."""
import json, sys, functools, time
n = 4
def idx(pos, neg): return pos | (neg << n)
VALID = [c for c in range(1 << (2 * n)) if (c & 15) & (c >> n) == 0]
def width(c): return bin(c).count("1")
RES = {}
for a in VALID:
    for b in VALID:
        pa, na, pb, nb = a & 15, a >> n, b & 15, b >> n
        clash = (pa & nb) | (na & pb)
        if clash and clash & (clash - 1) == 0:
            p, q = (pa | pb) & ~clash, (na | nb) & ~clash
            if p & q == 0:
                RES[(a, b)] = idx(p, q)
RESL = {a: [(b, RES[(a, b)]) for b in VALID if (a, b) in RES] for a in VALID}
WITNESS = []    # last found derivation (canonical order), ends with bottom
SLICE2 = None   # optional second-level slice (stage mode, 10 args)
CONS = {c: 0 for c in VALID}
for (a, b), c in RES.items():
    CONS[c] |= 1 << a
SUBSUMERS = {c: sum(1 << d for d in VALID if d & c == d) for c in VALID}

def tree_min(F):
    Fs = list(F)
    @functools.lru_cache(None)
    def t(c):  # min steps to derive a subclause of c
        if any(d & c == d for d in Fs): return 0
        best = 10 ** 9
        pos, neg = c & 15, c >> n
        for v in range(n):
            if (pos | neg) >> v & 1: continue
            best = min(best, 1 + t(c | (1 << v)) + t(c | (1 << (v + n))))
        return best
    return t(0)

def dag_min(F, upper, mu=True, level=None, slice_=None):
    """If mu=True (F minimally unsatisfiable), every refutation uses all |F|
    source clauses, hence has >= |F|-1 steps (in-degree-2 DAG counting), and
    at each node the axioms that no derived clause so far can consume must be
    consumed by the r remaining steps: r >= u - 1 (u counted below)."""
    F = list(F)
    Fmask = sum(1 << c for c in F)
    nodes = [0]
    def resolvents(c, avail_list):
        m = 0
        for b in avail_list:
            r = RES.get((c, b))
            if r is not None: m |= 1 << r
        return m
    def search(avail_mask, avail_list, J, seq, Jhist, r, slice_=None):
        nodes[0] += 1
        if (J >> 0) & 1:                             # bottom derivable now: 1 step
            WITNESS[:] = seq + [0]
            return True
        if r <= 1: return False
        wmin = min(width(c) for c in avail_list)
        if wmin > r: return False                   # width drops <= 1 per step
        if mu:
            # CONS[c] over-approximates the clauses that can be a premise of c,
            # so u under-approximates the still-unconsumable axioms (admissible)
            # dangling derived clauses: no later derived clause can consume them.
            # r remaining steps must consume u + dang items plus r-1 of their
            # own outputs with capacity 2r, so r >= u + dang - 1.
            cons = 0; dang = 0
            for i in range(len(seq) - 1, -1, -1):
                if not (cons >> seq[i]) & 1: dang += 1
                cons |= CONS[seq[i]]
            u = bin(Fmask & ~cons).count("1")
            if u + dang - 1 > r: return False
        cands = J & ~avail_mask
        c = 0; bi = -1
        while cands:
            low = cands & -cands; c = low.bit_length() - 1; cands ^= low
            bi += 1
            if slice_ is not None and not (slice_[0] <= bi < slice_[1]): continue
            if SLICE2 is not None and len(seq) == 1 and not (SLICE2[0] <= bi < SLICE2[1]): continue
            if SUBSUMERS[c] & avail_mask: continue  # subsumed: never needed
            # canonical greedy order: c must not have been derivable before the
            # last earlier step whose clause index exceeds c
            j = len(seq) - 1
            while j >= 0 and seq[j] < c: j -= 1
            if j >= 0 and (Jhist[j] >> c) & 1: continue
            nl = avail_list + [c]
            nJ = J | resolvents(c, nl)
            if search(avail_mask | (1 << c), nl, nJ, seq + [c], Jhist + [J], r - 1):
                return True
        return False
    am = sum(1 << c for c in F)
    J0 = 0
    for i, a in enumerate(F):
        J0 |= resolvents(a, F[i:])
    lo = max(1, min(width(c) for c in F), (len(F) - 1) if mu else 0)
    if level is not None:   # stage mode: decide only "exists proof of length level" on a top slice
        return search(am, F, J0, [], [], level, slice_), nodes[0]
    if lo >= upper:
        return upper, nodes[0]
    for L in range(lo, upper):
        if search(am, F, J0, [], [], L):
            return L, nodes[0]
    return upper, nodes[0]          # no proof shorter than the tree optimum

def is_mu(F):
    def sat(cl):
        for x in range(1 << n):
            if all((x & (c & 15)) or (~x & (c >> n) & 15) for c in cl): return True
        return False
    return (not sat(F)) and all(sat(F[:i] + F[i + 1:]) for i in range(len(F)))

if __name__ == "__main__" and sys.argv[1] == "--stage":
    # --stage IN OUT k L b0 b1 : is there a refutation of length L whose first
    # canonical step is top-level candidate number b in [b0, b1)?
    data = json.load(open(sys.argv[2]))
    k, L, b0, b1 = map(int, sys.argv[4:8])
    if len(sys.argv) > 9:
        SLICE2 = (int(sys.argv[8]), int(sys.argv[9]))
    F = [idx(p, q) for p, q in data["formulas"][k]["clauses"]]
    assert is_mu(F)
    t0 = time.time()
    found, nodes = dag_min(F, 99, level=L, slice_=(b0, b1))
    with open(sys.argv[3], "a") as out:
        out.write(json.dumps({"k": k, "L": L, "slice": [b0, b1],
                              "slice2": list(SLICE2) if SLICE2 else None, "found": found,
                              "nodes": nodes, "sec": round(time.time() - t0, 3)}) + "\n")
    sys.exit(0)

if __name__ == "__main__":
    data = json.load(open(sys.argv[1]))
    start, stop = int(sys.argv[3]), int(sys.argv[4])
    with open(sys.argv[2], "a") as out:
        for k in range(start, min(stop, len(data["formulas"]))):
            rec = data["formulas"][k]
            F = [idx(p, q) for p, q in rec["clauses"]]
            assert is_mu(F), k
            t0 = time.time()
            tm = tree_min(F)
            dm, nodes = dag_min(F, tm)
            out.write(json.dumps({"k": k, "m": len(F), "orbit": rec["orbit_size"],
                                  "tree_min": tm, "dag_min": dm, "nodes": nodes,
                                  "sec": round(time.time() - t0, 3)}) + "\n")
            out.flush()
