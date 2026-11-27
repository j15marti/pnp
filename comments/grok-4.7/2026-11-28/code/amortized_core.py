#!/usr/bin/env python3
"""Grok 4.7 work 2026-11-28: amortized leave-one-block-out (LOBO) and
insertion-based minimal block cores for GF(2) Nullstellensatz row spans,
addressing the FP54 'next lemma' (631f951).  Also spot-checks of FP54 parity
identities and the T3 Fano guard example (4130afa).  Python 3, stdlib only.
Rows are Python ints (bitsets over multilinear monomial columns); column 0 is
the constant monomial 1.  Cost metric: number of row XORs (each XOR is one
M-bit vector operation) plus number of row insertions."""
import itertools, json, random, sys, time

# ---------------- incremental GF(2) basis with snapshots -----------------
class Basis:
    __slots__ = ("piv", "own", "xors", "ins")
    def __init__(self):
        self.piv = {}   # pivot bit -> row
        self.own = {}   # pivot bit -> OR-mask of contributing blocks
        self.xors = 0; self.ins = 0
    def copy_state(self):
        return (dict(self.piv), dict(self.own))
    def restore(self, st):
        self.piv, self.own = dict(st[0]), dict(st[1])
    def reduce(self, v, mask=0):
        piv = self.piv
        while v:
            h = v.bit_length() - 1
            r = piv.get(h)
            if r is None:
                return v, mask
            v ^= r; mask |= self.own[h]; self.xors += 1
        return 0, mask
    def insert(self, v, mask):
        self.ins += 1
        v, mask = self.reduce(v, mask)
        if v:
            h = v.bit_length() - 1
            self.piv[h] = v; self.own[h] = mask
    def contains_one(self):
        # 1 = bit 0.  Reduce target 1 (track OR-mask of used rows' blocks)
        v, mask = self.reduce(1, 0)
        return v == 0, mask

def full_test(blocks, allowed):
    """Fresh GE on rows of the allowed blocks; returns (in_span, core_mask, xors, ins)."""
    B = Basis()
    for i in allowed:
        for r in blocks[i]:
            B.insert(r, 1 << i)
    ok, m = B.contains_one()
    return ok, m, B.xors, B.ins

# ---------------- algorithms -----------------
def lobo_naive(blocks):
    b = len(blocks); res = []; X = I = 0
    for D in range(b):
        ok, _, x, i = full_test(blocks, [j for j in range(b) if j != D])
        res.append(ok); X += x; I += i
    return res, X, I

def lobo_naive_skip(blocks):
    """Naive, but first compute one certificate core C (OR-mask); every D not in C is YES for free."""
    b = len(blocks)
    ok, C, X, I = full_test(blocks, range(b))
    if not ok:
        return [False]*b, X, I
    res = []
    for D in range(b):
        if not (C >> D) & 1:
            res.append(True); continue
        ok2, _, x, i = full_test(blocks, [j for j in range(b) if j != D])
        res.append(ok2); X += x; I += i
    return res, X, I

def lobo_dc(blocks):
    """Divide and conquer: each block's rows are inserted O(log b) times."""
    b = len(blocks); res = [None]*b
    B = Basis()
    def rec(lo, hi):            # rows of all blocks outside [lo,hi) are in B
        if hi - lo == 1:
            res[lo] = B.contains_one()[0]; return
        mid = (lo + hi) // 2
        st = B.copy_state()
        for j in range(mid, hi):
            for r in blocks[j]: B.insert(r, 1 << j)
        rec(lo, mid)
        B.restore(st)
        for j in range(lo, mid):
            for r in blocks[j]: B.insert(r, 1 << j)
        rec(mid, hi)
        B.restore(st)
    rec(0, b)
    return res, B.xors, B.ins

def min_core_deletion(blocks):
    """Classical deletion filter: b fresh GEs."""
    b = len(blocks); keep = set(range(b)); X = I = 0
    for D in range(b):
        ok, _, x, i = full_test(blocks, sorted(keep - {D}))
        X += x; I += i
        if ok: keep.discard(D)
    return sorted(keep), X, I

def min_core_insertion(blocks):
    """Insertion-based: rounds = |K|+1, each round one incremental prefix pass."""
    b = len(blocks); K = []; cand = list(range(b)); X = I = 0; rounds = 0
    while True:
        rounds += 1
        B = Basis()
        for j in K:
            for r in blocks[j]: B.insert(r, 1 << j)
        if B.contains_one()[0]:
            X += B.xors; I += B.ins; break
        t = None
        for pos, j in enumerate(cand):
            for r in blocks[j]: B.insert(r, 1 << j)
            if B.contains_one()[0]:
                t = pos; break
        X += B.xors; I += B.ins
        if t is None:
            raise RuntimeError("1 not in span")
        K.append(cand[t]); cand = cand[:t]
    return sorted(K), X, I, rounds

def verify_core(blocks, K):
    ok = full_test(blocks, K)[0]
    minimal = all(not full_test(blocks, [j for j in K if j != d])[0] for d in K)
    return ok, minimal

# ---------------- Nullstellensatz rows for 3-CNF -----------------
def monomial_index(n, d):
    idx = {}
    for k in range(d + 1):
        for S in itertools.combinations(range(n), k):
            idx[frozenset(S)] = len(idx)
    return idx

def clause_poly(cl):
    """Falsification indicator prod_{lit} (lit false) as dict{frozenset: 1} over GF(2).
    positive x: false iff x=0 -> (1+x); negative x: false iff x=1 -> x."""
    poly = {frozenset(): 1}
    for lit in cl:
        v = abs(lit) - 1
        new = {}
        if lit > 0:
            factors = [frozenset(), frozenset([v])]
        else:
            factors = [frozenset([v])]
        for m in poly:
            for f in factors:
                mm = m | f
                new[mm] = new.get(mm, 0) ^ 1
        poly = {m: 1 for m, c in new.items() if c}
    return poly

def rows_for_clause(cl, n, d, idx):
    p = clause_poly(cl); dp = max(len(m) for m in p)
    rows = []
    for k in range(0, d - dp + 1):
        for S in itertools.combinations(range(n), k):
            S = frozenset(S); acc = {}
            for m in p:
                mm = m | S
                acc[mm] = acc.get(mm, 0) ^ 1
            v = 0
            for mm, c in acc.items():
                if c: v ^= 1 << idx[mm]
            if v: rows.append(v)
    return rows

def random_3cnf(n, m, rng):
    cls = []
    for _ in range(m):
        vs = rng.sample(range(1, n + 1), 3)
        cls.append(tuple(v if rng.random() < 0.5 else -v for v in vs))
    return cls

def is_unsat(cls, n):
    for a in range(1 << n):
        if all(any(((a >> (abs(l)-1)) & 1) == (l > 0) for l in c) for c in cls):
            return False
    return True

def php_cnf(p):  # pigeons p+1 into p holes: as general CNF (wide clauses) -> use only for d large
    raise NotImplementedError

# ---------------- spot checks -----------------
def check_fp54():
    out = {}
    # e1*e2 = e3 and defect = 1+e2+e3 for 4 truth bits; clause SAT iff e1 or e2 for 3 bits
    ok = True
    for u in itertools.product([0, 1], repeat=4):
        Q = sum(u)
        e = [sum(1 for S in itertools.combinations(range(4), j) if all(u[i] for i in S)) % 2 for j in range(5)]
        ok &= (e[1]*e[2]) % 2 == e[3]
        ok &= ((1 + e[2] + e[3]) % 2) == (0 if Q == 2 else 1)
        ok &= ((e[1] == 0 and e[2] == 1) == (Q == 2))
    for u in itertools.product([0, 1], repeat=3):
        e1 = sum(u) % 2; e2 = sum(u[i]*u[j] for i, j in itertools.combinations(range(3), 2)) % 2
        ok &= ((e1 == 1 or e2 == 1) == (sum(u) > 0))
    out["fp54_identities_all_16_and_8_rows"] = ok
    # polynomial identity e1*e2 = e3 in the Boolean quotient (formal multilinearisation)
    prod = {}
    for i in range(4):
        for j, k in itertools.combinations(range(4), 2):
            m = frozenset([i, j, k]); prod[m] = prod.get(m, 0) ^ 1
    prod = {m for m, c in prod.items() if c}
    out["fp54_formal_e1e2_equals_e3"] = prod == {frozenset(S) for S in itertools.combinations(range(4), 3)}
    return out

def check_fano():
    L = [(1,2,3),(1,4,5),(1,6,7),(2,4,6),(2,5,7),(3,4,7),(3,5,6)]
    cover = [0]*128; excl = [0]*7
    for a in range(128):
        hit = [g for g, t in enumerate(L) if len({(a >> (x-1)) & 1 for x in t}) == 1]
        cover[a] = len(hit)
        if len(hit) == 1: excl[hit[0]] += 1
    return {"fano_uncovered": sum(1 for c in cover if c == 0),
            "fano_exclusive_per_guard": excl,
            "fano_kraft_sum": 7 * 0.25}

# ---------------- experiment -----------------
def experiment(seed=20261128):
    rng = random.Random(seed)
    results = []
    configs = [(10, 60, 5), (10, 60, 6), (12, 80, 5), (12, 80, 6), (12, 90, 7), (14, 100, 6)]
    for (n, m, d) in configs:
        for trial in range(3):
            # draw UNSAT formula
            while True:
                cls = random_3cnf(n, m, rng)
                if is_unsat(cls, n): break
            idx = monomial_index(n, d)
            blocks = [rows_for_clause(c, n, d, idx) for c in cls]
            R = sum(len(bl) for bl in blocks)
            t0 = time.time(); ok_all, C, xa, ia = full_test(blocks, range(m)); tfull = time.time() - t0
            rec = {"n": n, "m": m, "d": d, "trial": trial, "columns": len(idx), "rows": R,
                   "refuted_degree_d": ok_all, "full_GE_xors": xa, "full_GE_ins": ia,
                   "first_core_ORmask_size": bin(C).count("1") if ok_all else None}
            if ok_all:
                t0 = time.time(); r_dc, xd, idc = lobo_dc(blocks); tdc = time.time() - t0
                t0 = time.time(); r_sk, xs, isk = lobo_naive_skip(blocks); tsk = time.time() - t0
                do_naive = R * m <= 4_000_000
                if do_naive:
                    t0 = time.time(); r_nv, xn, inv = lobo_naive(blocks); tnv = time.time() - t0
                else:
                    r_nv, xn, inv, tnv = None, None, None, None
                rec.update({
                    "lobo_yes": sum(r_dc), "lobo_no(necessary blocks)": m - sum(r_dc),
                    "dc_equals_skip": r_dc == r_sk, "dc_equals_naive": (r_dc == r_nv) if do_naive else "not run",
                    "naive_xors": xn, "naive_ins": inv, "naive_s": tnv,
                    "skip_xors": xs, "skip_ins": isk, "skip_s": round(tsk, 3),
                    "dc_xors": xd, "dc_ins": idc, "dc_s": round(tdc, 3),
                    "dc_ins_over_R_log2b": round(idc / (R * max(1, (m - 1).bit_length())), 3),
                })
                t0 = time.time(); K, xi, ii, rounds = min_core_insertion(blocks); ti = time.time() - t0
                okK, minK = verify_core(blocks, K)
                rec.update({"insertion_core_size": len(K), "insertion_rounds": rounds,
                            "insertion_xors": xi, "insertion_ins": ii, "insertion_s": round(ti, 3),
                            "insertion_core_spans_1": okK, "insertion_core_inclusion_minimal": minK})
                if do_naive:
                    t0 = time.time(); Kd, xdl, idl = min_core_deletion(blocks); tdl = time.time() - t0
                    rec.update({"deletion_core_size": len(Kd), "deletion_xors": xdl, "deletion_ins": idl,
                                "deletion_s": round(tdl, 3)})
            results.append(rec)
            print(json.dumps(rec), file=sys.stderr, flush=True)
    return results

if __name__ == "__main__":
    out = {"seed": 20261128, "python": sys.version.split()[0]}
    out.update(check_fp54()); out.update(check_fano())
    out["experiments"] = experiment()
    json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "amortized_core.out.json", "w"), indent=1)
    print("done")
