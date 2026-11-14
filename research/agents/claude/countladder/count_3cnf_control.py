"""COUNTLADDER-0001 control: 3-CNF conversion of not-Count_q^N, satisfiability check,
and mechanical check of the suffix-OR substitution lemma.  Runs in a few seconds."""
import itertools, json, sys, time

def count_cnf(N, q):
    """CNF of the negation of Count_q^N: Y_e is a q-block, the blocks form a perfect partition."""
    blocks = list(itertools.combinations(range(N), q))
    var = {e: i + 1 for i, e in enumerate(blocks)}
    cls = []
    for v in range(N):
        cls.append([var[e] for e in blocks if v in e])            # v covered
    for e, f in itertools.combinations(blocks, 2):
        if set(e) & set(f):
            cls.append([-var[e], -var[f]])                        # no overlap
    return len(blocks), cls

def to_3cnf(nv, cls):
    """Chain conversion: (l1 v l2 v z1), (~z_j v l_{j+2} v z_{j+1}), ..., (~z_k v l_{w-1} v l_w)."""
    out, nxt, chains = [], nv + 1, []
    for c in cls:
        if len(c) <= 3:
            out.append(list(c)); continue
        w = len(c); zs = list(range(nxt, nxt + w - 3)); nxt += w - 3
        out.append([c[0], c[1], zs[0]])
        for j in range(len(zs) - 1):
            out.append([-zs[j], c[j + 2], zs[j + 1]])
        out.append([-zs[-1], c[w - 2], c[w - 1]])
        chains.append((c, zs))
    return nxt - 1, out, chains

def dpll(nv, cls):
    assign = {}
    def unit(cl, a):
        a = dict(a)
        changed = True
        while changed:
            changed = False
            for c in cl:
                if any(a.get(abs(l)) == (l > 0) for l in c):
                    continue
                free = [l for l in c if abs(l) not in a]
                if not free: return None
                if len(free) == 1:
                    a[abs(free[0])] = free[0] > 0; changed = True
        return a
    def rec(a):
        a = unit(cls, a)
        if a is None: return None
        for c in cls:
            if not any(a.get(abs(l)) == (l > 0) for l in c):
                l = next(l for l in c if abs(l) not in a)
                for val in (l > 0, l < 0):
                    r = rec({**a, abs(l): val})
                    if r is not None: return r
                return None
        return a
    return rec(assign)

def check_substitution(c, zs):
    """Substitute z_j := OR of suffix literals c[j+2:]; every converted clause must then be
    implied by c alone (head) or be a tautology (chain/tail).  Brute force over the literals."""
    w = len(c)
    ok = True
    for bits in itertools.product([False, True], repeat=w):
        lit = bits
        z = [any(lit[j + 2:]) for j in range(len(zs))]
        orig = any(lit)
        head = lit[0] or lit[1] or z[0]
        if head != orig: ok = False
        for j in range(len(zs) - 1):
            if not ((not z[j]) or lit[j + 2] or z[j + 1]): ok = False
        if not ((not z[-1]) or lit[w - 2] or lit[w - 1]): ok = False
    return ok

if __name__ == "__main__":
    t0 = time.time(); rows = []
    for q, N in [(3, 4), (3, 5), (3, 6), (3, 7), (2, 5), (2, 6), (5, 6)]:
        nv, cls = count_cnf(N, q)
        nv3, c3, chains = to_3cnf(nv, cls)
        assert all(len(c) <= 3 for c in c3)
        sol = dpll(nv3, c3)
        sub_ok = all(check_substitution(c, zs) for c, zs in chains if len(c) <= 12)
        rows.append(dict(q=q, N=N, vars=nv3, clauses=len(c3), sat=sol is not None,
                         expected_sat=(N % q == 0), substitution_lemma_ok=sub_ok))
        print(rows[-1], flush=True)
    for r in rows: assert r["sat"] == r["expected_sat"], r
    out = dict(script="count_3cnf_control.py", rows=rows, seconds=round(time.time() - t0, 2))
    json.dump(out, open(sys.argv[1], "w"), indent=1) if len(sys.argv) > 1 else None
    print("ALL CHECKS PASSED", out["seconds"])
