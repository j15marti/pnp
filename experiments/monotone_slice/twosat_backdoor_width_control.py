#!/usr/bin/env python3
"""TWOSATWIDTH1 control: minimal free-exact-2-SAT decision depth r_min above threshold.

Same generator and certificate semantics as TWOSATDEC21..94 (random.Random.sample on the
lexicographic proper 3-clause list; a variable set S certifies iff every assignment of S,
after unit propagation, yields an empty clause or an unsatisfiable width<=2 skeleton;
surviving width-3 clauses are ignored).  Only the density changes: t = round(delta*q).

Purpose: finite COMPUTATIONAL control for the PROVED reduction
    r_min(F) >= w(F |- empty) - 3      (resolution width; see TWOSATWIDTH1 note),
which with Ben-Sasson--Wigderson gives r_min = Omega(q) whp for constant delta > 4.4898.
Finite q cannot show asymptotics; this only checks the protocol runs in the UNSAT regime and
reports r_min growth.  Usage: python3 -I twosat_backdoor_width_control.py DELTA Q N [RMAX] [BUDGET] [SEED]
"""
import itertools, random, sys, time

SEED = 20261120


def clause_list(q):
    out = []
    for tri in itertools.combinations(range(q), 3):
        for s in range(8):
            # bit b of s is the sign of tri[b]; pol 1 = positive literal
            out.append(tuple((v + 1) if (s >> b) & 1 else -(v + 1) for b, v in enumerate(tri)))
    return out


def unit_prop(clauses, assign):
    """assign: dict var->bool.  Returns (conflict, reduced clauses list) or extends assign."""
    changed = True
    cur = clauses
    while changed:
        changed = False
        nxt = []
        for c in cur:
            sat = False
            rest = []
            for l in c:
                v = abs(l)
                if v in assign:
                    if assign[v] == (l > 0):
                        sat = True
                        break
                else:
                    rest.append(l)
            if sat:
                continue
            if not rest:
                return True, None
            if len(rest) == 1:
                l = rest[0]
                assign[abs(l)] = l > 0
                changed = True
                continue
            nxt.append(tuple(rest))
        cur = nxt
    return False, cur


def twosat_unsat(cls2):
    """Implication-graph SCC test on width-2 clauses. True iff unsatisfiable."""
    adj = {}
    for a, b in cls2:
        adj.setdefault(-a, []).append(b)
        adj.setdefault(-b, []).append(a)
        adj.setdefault(a, [])
        adj.setdefault(b, [])
    index, low, onst, st, comp = {}, {}, set(), [], {}
    cnt = [0]
    c_id = [0]
    for root in list(adj):
        if root in index:
            continue
        stack = [(root, iter(adj[root]))]
        index[root] = low[root] = cnt[0]; cnt[0] += 1; st.append(root); onst.add(root)
        while stack:
            v, it = stack[-1]
            pushed = False
            for w in it:
                if w not in index:
                    index[w] = low[w] = cnt[0]; cnt[0] += 1; st.append(w); onst.add(w)
                    stack.append((w, iter(adj[w]))); pushed = True
                    break
                elif w in onst:
                    low[v] = min(low[v], index[w])
            if pushed:
                continue
            stack.pop()
            if stack:
                low[stack[-1][0]] = min(low[stack[-1][0]], low[v])
            if low[v] == index[v]:
                while True:
                    w = st.pop(); onst.discard(w); comp[w] = c_id[0]
                    if w == v:
                        break
                c_id[0] += 1
    return any(comp[l] == comp.get(-l) for l in comp if -l in comp)


def branch_closed(clauses, S, bits):
    assign = {v: bool((bits >> i) & 1) for i, v in enumerate(S)}
    conflict, red = unit_prop(clauses, assign)
    if conflict:
        return True
    return twosat_unsat([c for c in red if len(c) == 2])


def certifies(clauses, S):
    return all(branch_closed(clauses, S, b) for b in range(1 << len(S)))


def dpll_sat(clauses, assign=None):
    assign = dict(assign or {})
    conflict, red = unit_prop(clauses, assign)
    if conflict:
        return False
    if not red:
        return True
    v = abs(red[0][0])
    for val in (True, False):
        a = dict(assign); a[v] = val
        if dpll_sat(red, a):
            return True
    return False


def main():
    delta = float(sys.argv[1]); q = int(sys.argv[2]); N = int(sys.argv[3])
    rmax = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    budget = float(sys.argv[5]) if len(sys.argv) > 5 else 25.0
    seed = int(sys.argv[6]) if len(sys.argv) > 6 else SEED
    t0 = time.time()
    L = clause_list(q)
    t = round(delta * q)
    rng = random.Random(seed)
    print(f"TWOSATWIDTH1 seed={seed} delta={delta} q={q} t={t} M={len(L)} N={N} rmax={rmax}")
    for idx in range(N):
        F = rng.sample(L, t)
        sat = dpll_sat(F)
        if sat:
            print(f"idx={idx} SAT"); continue
        found = None; exhausted = None
        for r in range(0, rmax + 1):
            hit = None
            for S in itertools.combinations(range(1, q + 1), r):
                if time.time() - t0 > budget:
                    break
                if certifies(F, S):
                    hit = S; break
            else:
                pass
            if hit is not None:
                found = (r, hit); break
            if time.time() - t0 > budget:
                exhausted = r; break
        if found:
            print(f"idx={idx} UNSAT r_min={found[0]} witness={found[1]}")
        elif exhausted is not None:
            print(f"idx={idx} UNSAT r_min>={exhausted} (budget hit during r={exhausted}; lower bound only)")
        else:
            print(f"idx={idx} UNSAT r_min>{rmax}")
        if time.time() - t0 > budget:
            print("budget exhausted; stopping"); break
    print(f"runtime {time.time()-t0:.2f}s")


if __name__ == "__main__":
    main()
