"""CLAUDE BRIDGE-COLLAPSE-0001: exact minimum tree-like Resolution refutation size.

Computes T(F) = min number of nodes of a decision tree for the false-clause search
problem of an UNSAT CNF F; this equals the minimum number of clauses in a tree-like
Resolution refutation (weakening-free; KNOWN, e.g. Beame-Impagliazzo-Pitassi-Segerlind /
Krajicek 2019 Sec. 5). Minimization is over ALL decision trees (free optimal sequence,
search not charged), exactly as in the W_R objective.

Each invocation handles one instance family member (chunking rule: < ~30 s each).
Usage: python tree_res_exact.py <family> <param> [seed]
"""
import itertools, json, random, sys, time
from functools import lru_cache

def php(m):  # m+1 pigeons, m holes; var p(i,j) = i*m+j
    n = (m + 1) * m
    cl = [[(i * m + j, 1) for j in range(m)] for i in range(m + 1)]
    for j in range(m):
        for a, b in itertools.combinations(range(m + 1), 2):
            cl.append([(a * m + j, 0), (b * m + j, 0)])
    return n, cl

def rand3(n, ratio, seed):
    rng = random.Random(seed)
    while True:
        cl = []
        for _ in range(round(ratio * n)):
            vs = rng.sample(range(n), 3)
            cl.append([(v, rng.randint(0, 1)) for v in vs])
        if not satisfiable(n, cl):
            return cl

def satisfiable(n, cl):
    for a in range(1 << n):
        if all(any(((a >> v) & 1) == s for v, s in c) for c in cl):
            return True
    return False

def complete(n):  # all 2^n full clauses on n vars
    return [[(v, (a >> v) & 1 ^ 1) for v in range(n)] for a in range(1 << n)]

def min_tree(n, cl):
    masks = [(sum(1 << v for v, _ in c), sum(1 << v for v, s in c if s == 0)) for c in cl]
    # clause falsified by (assigned, val) iff all vars assigned and val == "falsifying" pattern
    # falsifying value of literal (v,s) is 1-s ; val bit = 1 means var true
    fals = [(m, sum(1 << v for v, s in c if s == 0)) for c, (m, _) in zip(cl, masks)]
    full = (1 << n) - 1
    @lru_cache(maxsize=None)
    def T(asg, val):
        for m, fv in fals:
            if asg & m == m and val & m == fv:
                return 1
        best = None
        free = full & ~asg
        # only branch on vars of clauses not yet satisfied (others are irrelevant)
        rel = 0
        for (m, fv), c in zip(fals, cl):
            sat = any(asg >> v & 1 and (val >> v & 1) == s for v, s in c)
            if not sat:
                rel |= m & free
        v = 0
        while rel:
            if rel & 1:
                b = 1 << v
                t = 1 + T(asg | b, val) + T(asg | b, val | b)
                if best is None or t < best:
                    best = t
            rel >>= 1; v += 1
        return best
    return T(0, 0), T.cache_info().currsize

if __name__ == "__main__":
    fam, p = sys.argv[1], int(sys.argv[2])
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 0
    t0 = time.time()
    if fam == "php":
        n, cl = php(p)
    elif fam == "complete":
        n, cl = p, complete(p)
    elif fam == "rand3":
        n, cl = p, rand3(p, 6.0, seed)
    else:
        raise SystemExit("unknown family")
    assert not satisfiable(n, cl), "control: formula must be UNSAT"
    size, states = min_tree(n, cl)
    out = dict(family=fam, param=p, seed=seed, n=n, clauses=len(cl), min_tree_res_size=size,
               memo_states=states, seconds=round(time.time() - t0, 2))
    print(json.dumps(out))
