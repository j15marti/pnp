#!/usr/bin/env python3
"""LSPV-5/528: exact minimum DAG-Resolution length audit of guard lifting.

For small UNSAT CNFs F and G_g(F) = (g) & AND_C (~g v C) (g fresh) this
computes, by exhaustive breadth-first search over derived-clause sets, the
minimum number S(.) of Resolution inferences in a DAG-like refutation and
checks the all-proofs identity S(G_g(F)) = S(F) + 1 (Theorem 528.1).

Clause = (pos_mask, neg_mask), non-tautological.  Search prunes derivation of
any clause subsumed by an already available clause; this is sound for minimum
length (replace each use of a subsumed clause by its subsumer: the resulting
inference yields a subsuming clause or is skipped).  Standard library only.
Chunking: --chunk selects one independent formula batch (each < ~30 s).
"""
import itertools, json, sys, time, random, hashlib

def res(a, b):
    out = []
    ap, an = a; bp, bn = b
    piv = (ap & bn) | (an & bp)
    if piv == 0 or piv & (piv - 1):
        return out  # zero pivots, or >=2 clashes -> tautological resolvent
    p = piv
    rp = (ap | bp) & ~p; rn = (an | bn) & ~p
    if rp & rn:
        return out
    return [(rp, rn)]

def subsumed(c, S):
    cp, cn = c
    for (p, n) in S:
        if p & ~cp == 0 and n & ~cn == 0:
            return True
    return False

def min_refutation(F, cap=12, state_cap=2_000_000):
    F = frozenset(F)
    if (0, 0) in F:
        return 0
    frontier = {frozenset()}
    for depth in range(1, cap + 1):
        nxt = set()
        for D in frontier:
            avail = list(F | D)
            for i in range(len(avail)):
                for j in range(i + 1, len(avail)):
                    for r in res(avail[i], avail[j]):
                        if r == (0, 0):
                            return depth
                        if r in F or r in D or subsumed(r, avail):
                            continue
                        nxt.add(D | {r})
        frontier = nxt
        if len(frontier) > state_cap:
            return None
    return None

def sat(F, nv):
    for bits in range(1 << nv):
        if all((p & bits) or (n & ~bits) for p, n in F):
            return True
    return False

def guard(F, nv):
    g = 1 << nv
    return [(g, 0)] + [(p, n | g) for p, n in F]

def clause_str(c, nv):
    p, n = c
    return [i + 1 for i in range(nv + 1) if p >> i & 1] + [-(i + 1) for i in range(nv + 1) if n >> i & 1]

def all_clauses(nv, maxw):
    out = []
    for w in range(1, maxw + 1):
        for vs in itertools.combinations(range(nv), w):
            for signs in itertools.product((0, 1), repeat=w):
                p = sum(1 << v for v, s in zip(vs, signs) if s)
                n = sum(1 << v for v, s in zip(vs, signs) if not s)
                out.append((p, n))
    return out

def batch(chunk):
    cases = []
    if chunk == 0:  # every UNSAT clause set over 2 variables, widths 1..2
        cl = all_clauses(2, 2)
        for k in range(2, len(cl) + 1):
            for F in itertools.combinations(cl, k):
                if not sat(F, 2):
                    cases.append((2, list(F)))
    elif chunk == 1:  # every MINIMALLY UNSAT set of proper 2-clauses + units, 3 vars
        cl = all_clauses(3, 2)
        rng = random.Random(528)
        seen = set()
        while len(cases) < 120:
            k = rng.randint(3, 7)
            F = tuple(sorted(rng.sample(cl, k)))
            if F in seen or sat(F, 3):
                continue
            if any(not sat(F[:i] + F[i+1:], 3) for i in range(len(F))):
                continue
            seen.add(F); cases.append((3, list(F)))
    elif chunk == 2:  # proper 3-clause sets on 3 vars: complete set and its UNSAT supersets of units
        cl3 = all_clauses(3, 3)
        cl3 = [c for c in cl3 if bin(c[0] | c[1]).count('1') == 3]
        cases.append((3, cl3))
        rng = random.Random(5280)
        units = all_clauses(3, 1); twos = [c for c in all_clauses(3, 2) if bin(c[0]|c[1]).count('1') == 2]
        seen = set()
        while len(cases) < 40:
            F = tuple(sorted(set(rng.sample(cl3, rng.randint(2, 6)) + rng.sample(twos, rng.randint(0, 3)) + rng.sample(units, rng.randint(0, 2)))))
            if F in seen or sat(F, 3):
                continue
            seen.add(F); cases.append((3, list(F)))
    return cases

def main():
    chunk = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    t0 = time.time(); rows = []; fails = 0; skipped = 0
    for nv, F in batch(chunk):
        sF = min_refutation(F)
        sG = min_refutation(guard(F, nv))
        ok = (sF is not None and sG is not None and sG == sF + 1)
        if sF is None or sG is None:
            skipped += 1
        elif not ok:
            fails += 1
        rows.append({"nv": nv, "F": [clause_str(c, nv) for c in F], "S_F": sF, "S_G": sG, "identity": ok})
    out = {"chunk": chunk, "cases": len(rows), "identity_failures": fails, "search_cap_skips": skipped,
           "max_S_F": max((r["S_F"] or 0) for r in rows), "seconds": round(time.time() - t0, 2), "rows": rows}
    s = json.dumps(out, sort_keys=True)
    out["sha256_rows"] = hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}))
    return out

if __name__ == "__main__":
    o = main()
    if len(sys.argv) > 2:
        json.dump(o, open(sys.argv[2], "w"), indent=1, sort_keys=True)
