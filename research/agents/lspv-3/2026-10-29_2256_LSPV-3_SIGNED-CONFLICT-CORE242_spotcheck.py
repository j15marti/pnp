#!/usr/bin/env python3
"""SIGNED-CONFLICT-CORE242 compact independent theorem/target checker, stdlib."""
import itertools
import json

def truth(clause, a):
    return tuple(int(a[abs(z)] == int(z > 0)) for z in clause)

def sat(formula, a):
    return all(any(truth(c, a)) for c in formula)

def local(clause, mode):
    return {abs(z): int(z > 0) if mode == "S" else int(z < 0) for z in clause}

def four_way(c, d):
    sc = {abs(z): z > 0 for z in c}
    sd = {abs(z): z > 0 for z in d}
    same = [v for v in sc.keys() & sd.keys() if sc[v] == sd[v]]
    opposite = [v for v in sc.keys() & sd.keys() if sc[v] != sd[v]]
    return {m: not (opposite if m in ("SS", "UU") else same)
            for m in ("SS", "SU", "US", "UU")}

def source_extremes(formula):
    out = []
    for j, clause in enumerate(formula):
        S, U = local(clause, "S"), local(clause, "U")
        assert all(S[v] == 1 - U[v] for v in S)
        out.append({"j": j, "C": clause, "S": S, "S_inv_to_U": U,
                    "U": U, "U_inv_to_S": S,
                    "occurrences": [{"source_variable": abs(z), "clause": j,
                                     "literal": z, "sign": "+" if z > 0 else "-",
                                     "S": S[abs(z)], "U": U[abs(z)]}
                                    for z in clause]})
    return out

def conflict(c, d):
    return any(-z in d for z in c)

def repair(F, cover, n):
    core = [c for j, c in enumerate(F) if j not in cover]
    a = {v: 0 for v in range(1, n + 1)}
    prefs = {}
    for c in core:
        for z in c:
            v = abs(z)
            preferred = int(z > 0)
            assert v not in prefs or prefs[v] == preferred
            prefs[v] = preferred
    a.update(prefs)
    assert all(sum(truth(c, a)) == len(c) for c in core)
    protected, flips = set(), []
    for j in sorted(cover):
        clause = F[j]
        if any(truth(clause, a)):
            v = next(abs(z) for z in clause if a[abs(z)] == int(z > 0))
        else:
            v = next(abs(z) for z in clause if abs(z) not in protected)
            a[v] ^= 1
            flips.append(v)
            assert any(truth(clause, a))
        protected.add(v)
    assert sat(F, a)
    return a, flips

def sharp(r):
    sets = [tuple(range(i*r+1, (i+1)*r+1)) for i in range(r)]
    plus = list(itertools.combinations(range(1, r*r+1), r))
    negatives = [tuple(-v for v in block) for block in sets]
    F = tuple(plus + negatives)
    cover = set(range(len(plus), len(F)))
    assert all(not conflict(F[i], F[j])
                   for i, j in itertools.combinations(range(len(plus)), 2))
    assert all(any(conflict(c, d) for d in negatives) for c in
               (tuple(block) for block in sets))
    return F, cover

def main():
    checks = 0
    # Independent exact four-mode enumeration for all 8 signings, one support.
    clauses = [tuple(s*(i+1) for i, s in enumerate(signs))
               for signs in itertools.product((-1, 1), repeat=3)]
    for c, d in itertools.combinations(clauses, 2):
        expected = four_way(c, d)
        for m, predicted in expected.items():
            actual = any(
                len([sum(truth(c, a)), sum(truth(d, a))]) == 2
                and sum(truth(c, a)) == (3 if m[0] == "S" else 0)
                and sum(truth(d, a)) == (3 if m[1] == "S" else 0)
                for vals in itertools.product((0, 1), repeat=3)
                for a in [{i+1: vals[i] for i in range(3)}])
            assert predicted == actual
            checks += 1
    for r in (2, 3):
        F, cover = sharp(r)
        n = r*r
        models = [a for vals in itertools.product((0, 1), repeat=n)
                  for a in [{i+1: vals[i] for i in range(n)}]
                  if sat(F, a)]
        assert not models
        assert len(cover) == r
        assert all(not conflict(F[i], F[j])
                   for i, j in itertools.combinations(
                       [j for j in range(len(F)) if j not in cover], 2))
        if r == 3:
            # All 2^9 projected candidates are certified false by an original clause.
            assert sum(1 for vals in itertools.product((0, 1), repeat=n)
                       if any(not any(truth(c, {i+1: vals[i]
                                              for i in range(n)})) for c in F)) == 512
        G = F[:-1]
        a, flips = repair(G, cover - {len(F)-1}, n)
        assert len(flips) <= r-1 and sat(G, a)
        # Signed occurrences and global complement are distinct operations.
        source = source_extremes(G)
        assert len(source) == len(G)
        for a_bits in itertools.product((0, 1), repeat=n):
            a = {i+1: a_bits[i] for i in range(n)}
            b = {i+1: 1-a_bits[i] for i in range(n)}
            for c in G:
                assert sum(truth(c, a)) + sum(truth(c, b)) == r
        print(json.dumps({"r": r, "n": n, "m_unsat": len(F), "cover_unsat": r,
                          "unsat_models": len(models), "after_one_exception_removed":
                          "SAT", "repair_flips": flips}))
    print(json.dumps({"independent_four_mode_pair_checks": checks,
                      "status": "COMPUTATIONAL checks of symbolically PROVED restricted lemmas",
                      "P_vs_NP": "OPEN"}))

if __name__ == "__main__":
    main()
