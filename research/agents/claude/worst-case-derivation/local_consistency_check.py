#!/usr/bin/env python3
"""Finite check of the localization lemma (report 2026-11-16_LOCALIZED_WITNESSING_BRIDGE.md).

Revision: local-consistency-check.v1. Deterministic given SEED. Runs in a few seconds.

Objects. A CNF over variables 1..v is a frozenset of clauses; a clause is a frozenset
of nonzero ints. restrict(F, i, b) sets x_i := b and simplifies (satisfied clauses are
dropped, falsified literals removed). A *decider* is a map D: formula -> {0,1} (1 = SAT).

Local consistency of D at F (the constraint LocCons used in the report):
  closed F (no free variables): D(F) == eval(F)        [eval: SAT iff no empty clause]
  open F, branching variable i = least free variable:   D(F) == D(F|i=0) OR D(F|i=1)

Claims checked exhaustively on the restriction closure cl(F) of every sampled F:
  (C1) the exact decider is locally consistent everywhere;
  (C2) for every perturbed decider D: D is locally consistent on all of cl(F)  =>  D(F)
       is correct (the localization lemma, finite instances);
  (C3) every false-SAT error at F is converted to a local inconsistency by the
       witness-free walk-down (follow a branch where D says 1), within v+1 queries' depth;
  (C4) every false-UNSAT error at F, GIVEN a satisfying assignment y, is converted to a
       local inconsistency by the walk-down along y, within v+1 levels;
  (C5) measured: without y, the number of nodes of cl(F) a breadth-first search must
       query before finding an inconsistency (the 'witness gap' of the report);
  (C6) adversarial path-hiding deciders: for F with a UNIQUE model y, set D := 0 on every
       node of the y-path (all of them satisfiable). The only local inconsistency is then at
       the closed leaf, depth = #branchings. Walk-down with y reaches it; BFS without y must
       query a large part of cl(F). Exact counts are recorded per instance.
Nothing here is asymptotic; it only exercises the finite combinatorics of the lemma.
"""
import itertools, json, random, sys, time, hashlib

SEED = 20261116
REV = "local-consistency-check.v2"


def restrict(F, i, b):
    lit_true = i if b else -i
    out = []
    for c in F:
        if lit_true in c:
            continue
        out.append(frozenset(l for l in c if l != -lit_true))
    return frozenset(out)


def free_vars(F):
    return sorted({abs(l) for c in F for l in c})


def closed_eval(F):
    return 0 if frozenset() in F else 1


def exact_sat(F):
    vs = free_vars(F)
    if frozenset() in F:
        return 0
    if not vs:
        return 1
    i = vs[0]
    return exact_sat(restrict(F, i, 0)) or exact_sat(restrict(F, i, 1))


def closure(F):
    seen = {F}
    stack = [F]
    while stack:
        G = stack.pop()
        if frozenset() in G:
            continue  # contains empty clause: treat as closed (evaluates to UNSAT)
        vs = free_vars(G)
        if not vs:
            continue
        i = vs[0]
        for b in (0, 1):
            H = restrict(G, i, b)
            if H not in seen:
                seen.add(H)
                stack.append(H)
    return seen


def is_closed(G):
    return frozenset() in G or not free_vars(G)


def loc_ok(D, G):
    if is_closed(G):
        return D[G] == closed_eval(G)
    i = free_vars(G)[0]
    return D[G] == (D[restrict(G, i, 0)] | D[restrict(G, i, 1)])


def walk_false_sat(D, F):
    """D(F)=1 but F unsat. Follow children with D=1; return (inconsistent node, depth)."""
    G, depth = F, 0
    while True:
        if not loc_ok(D, G):
            return G, depth
        if is_closed(G):
            raise AssertionError("walk reached consistent closed node with D=1 on unsat path")
        i = free_vars(G)[0]
        kids = [restrict(G, i, b) for b in (0, 1)]
        G = next(K for K in kids if D[K] == 1)  # exists since loc_ok and D(G)=1
        depth += 1


def walk_false_unsat(D, F, y):
    """D(F)=0, y satisfies F. Walk along y; return (inconsistent node, depth)."""
    G, depth = F, 0
    while True:
        if not loc_ok(D, G):
            return G, depth
        if is_closed(G):
            raise AssertionError("consistent closed node with D=0 on satisfying path")
        i = free_vars(G)[0]
        G = restrict(G, i, y[i])
        depth += 1


def bfs_find_inconsistency(D, F):
    order, seen, q, k = [], {F}, [F], 0
    while q:
        G = q.pop(0)
        k += 1
        if not loc_ok(D, G):
            return k
        if is_closed(G):
            continue
        i = free_vars(G)[0]
        for b in (0, 1):
            H = restrict(G, i, b)
            if H not in seen:
                seen.add(H)
                q.append(H)
    return None


def find_model(F, v):
    for bits in itertools.product((0, 1), repeat=v):
        y = {i + 1: bits[i] for i in range(v)}
        if all(any((l > 0 and y[l]) or (l < 0 and not y[-l]) for l in c) for c in F):
            return y
    return None


def random_cnf(rng, v, m, k=3):
    F = []
    for _ in range(m):
        vs = rng.sample(range(1, v + 1), k)
        F.append(frozenset(x if rng.random() < 0.5 else -x for x in vs))
    return frozenset(F)


def main():
    t0 = time.time()
    rng = random.Random(SEED)
    stats = dict(formulas=0, closure_nodes=0, C1_violations=0, C2_cases=0, C2_violations=0,
                 C3_cases=0, C3_maxdepth=0, C4_cases=0, C4_maxdepth=0, C5=[])
    for v in (4, 5, 6, 7):
        for m in (int(3.0 * v), int(4.3 * v), int(5.5 * v)):
            for _ in range(12):
                F = random_cnf(rng, v, m)
                cl = closure(F)
                stats["formulas"] += 1
                stats["closure_nodes"] += len(cl)
                exact = {G: exact_sat(G) for G in cl}
                if any(not loc_ok(exact, G) for G in cl):
                    stats["C1_violations"] += 1
                y = find_model(F, v)
                for trial in range(20):
                    D = dict(exact)
                    nflip = rng.choice([1, 1, 2, 3, max(1, len(cl) // 10)])
                    for G in rng.sample(sorted(cl, key=lambda g: sorted(map(sorted, g))), min(nflip, len(cl))):
                        D[G] ^= 1
                    allok = all(loc_ok(D, G) for G in cl)
                    stats["C2_cases"] += 1
                    if allok and D[F] != exact[F]:
                        stats["C2_violations"] += 1
                    if D[F] != exact[F]:
                        if D[F] == 1:
                            _, d = walk_false_sat(D, F)
                            stats["C3_cases"] += 1
                            stats["C3_maxdepth"] = max(stats["C3_maxdepth"], d)
                            assert d <= v
                        else:
                            _, d = walk_false_unsat(D, F, y)
                            stats["C4_cases"] += 1
                            stats["C4_maxdepth"] = max(stats["C4_maxdepth"], d)
                            assert d <= v
                            k = bfs_find_inconsistency(D, F)
                            stats["C5"].append(dict(v=v, closure=len(cl), bfs_queries=k, walk_depth=d))
    # C6: adversarial path hiding on unique-model formulas
    c6 = []
    rng6 = random.Random(SEED + 6)
    for v in (6, 8, 10, 12):
        found, tries = 0, 0
        while found < 6 and tries < 4000:
            tries += 1
            F = random_cnf(rng6, v, int(4.6 * v))
            models = [b for b in itertools.product((0, 1), repeat=v)
                      if all(any((l > 0 and b[l - 1]) or (l < 0 and not b[-l - 1]) for l in c) for c in F)]
            if len(models) != 1:
                continue
            found += 1
            y = {i + 1: models[0][i] for i in range(v)}
            cl = closure(F)
            exact = {G: exact_sat(G) for G in cl}
            D = dict(exact)
            G, path = F, [F]
            while not is_closed(G):
                G = restrict(G, free_vars(G)[0], y[free_vars(G)[0]])
                path.append(G)
            for G in path:
                assert exact[G] == 1
                D[G] = 0
            bad = [G for G in cl if not loc_ok(D, G)]
            assert bad == [path[-1]], "hiding decider must be consistent except at the leaf"
            node, d = walk_false_unsat(D, F, y)
            assert node == path[-1]
            k = bfs_find_inconsistency(D, F)
            c6.append(dict(v=v, clauses=len(F), closure=len(cl), path_len=len(path) - 1,
                           walk_queries=3 * d + 1, bfs_queries=k))
    stats["C6"] = c6
    c5 = stats.pop("C5")
    by_v = {}
    for r in c5:
        by_v.setdefault(r["v"], []).append(r)
    stats["C5_summary"] = {
        str(v): dict(cases=len(rs), mean_closure=round(sum(r["closure"] for r in rs) / len(rs), 1),
                     mean_bfs_queries=round(sum(r["bfs_queries"] for r in rs) / len(rs), 1),
                     max_bfs_queries=max(r["bfs_queries"] for r in rs),
                     max_walk_depth=max(r["walk_depth"] for r in rs))
        for v, rs in sorted(by_v.items())}
    stats["seconds"] = round(time.time() - t0, 2)
    stats["revision"] = REV
    stats["seed"] = SEED
    stats["python"] = sys.version.split()[0]
    stats["script_sha256"] = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
    ok = stats["C1_violations"] == 0 and stats["C2_violations"] == 0
    stats["all_claims_pass"] = ok
    print(json.dumps(stats, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
