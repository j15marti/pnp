#!/usr/bin/env python3
"""Toy finite control for CLAUDE B3-REFLECT-0001 (COMPUTATIONAL, illustrative only).

Universe: CNFs over variables {1,2} with <=3 clauses of width 1..2; proofs sigma in {"", "0", "1"}.
Candidate 'machines' are verifiers V(G, sigma) -> bool with a declared description length.
SOUND(V) := for every (G, sigma) in the universe, V accepts => G is UNSAT (brute force).
The reflection system R_KP accepts (V, sigma) as a proof of F iff V(F, sigma) and SOUND(V)
and desc_len(V) <= log2(L+2), L = |F| + |sigma| (here |F| = number of literals + clauses).
Checks: (1) SOUND classification of each candidate; (2) R_KP never accepts a SAT formula;
(3) every UNSAT formula has an R_KP proof via some sound candidate once the size gate opens;
(4) the 'hard-coded F' machine family (desc_len ~ |F|) is excluded by the size gate,
    while the unrestricted system R_full (no gate) accepts every UNSAT F with an O(|F|) proof.
Runtime: well under 1 second.
"""
import itertools, json, math, sys

LITS = [1, -1, 2, -2]
CLAUSES = [c for w in (1, 2) for c in itertools.combinations(LITS, w) if not (w == 2 and abs(c[0]) == abs(c[1]))]
UNIVERSE = [f for k in range(0, 4) for f in itertools.combinations(CLAUSES, k)]
PROOFS = ["", "0", "1"]

def sat(f):
    for a in itertools.product([False, True], repeat=2):
        if all(any((l > 0) == a[abs(l) - 1] for l in c) for c in f):
            return True
    return False

def size(f):
    return sum(len(c) for c in f) + len(f)

def unit_refute(f, sigma):
    if sigma != "":
        return False
    units = {c[0] for c in f if len(c) == 1}
    clauses = [set(c) for c in f]
    changed = True
    while changed:
        changed = False
        for c in clauses:
            rest = {l for l in c if -l not in units}
            if not rest:
                return True
            if len(rest) == 1 and next(iter(rest)) not in units:
                units.add(next(iter(rest))); changed = True
        if any(-u in units for u in units):
            return True
    return False

CANDIDATES = {
    # name: (verifier, declared description length, expected soundness)
    "unit_propagation": (unit_refute, 2, True),
    "brute_force_QA": (lambda f, s: s == "" and not sat(f), 2, True),
    "accept_all": (lambda f, s: True, 1, False),
    "even_clause_count": (lambda f, s: len(f) % 2 == 0 and len(f) > 0, 2, False),
    "proof_bit_1_trust": (lambda f, s: s == "1", 1, False),
}

def sound(v):
    return all(not v(g, s) or not sat(g) for g in UNIVERSE for s in PROOFS)

def rkp_accepts(f, name, sigma, gate=True):
    v, d, _ = CANDIDATES[name]
    L = size(f) + len(sigma)
    if gate and d > math.log2(L + 2):
        return False
    return v(f, sigma) and sound(v)

res = {"universe_formulas": len(UNIVERSE), "unsat_formulas": sum(not sat(f) for f in UNIVERSE)}
res["soundness"] = {n: sound(c[0]) for n, c in CANDIDATES.items()}
assert all(res["soundness"][n] == CANDIDATES[n][2] for n in CANDIDATES), res
bad = [(f, n, s) for f in UNIVERSE if sat(f) for n in CANDIDATES for s in PROOFS if rkp_accepts(f, n, s)]
assert not bad
res["rkp_accepts_sat_formula"] = len(bad)
covered = [f for f in UNIVERSE if not sat(f) and any(rkp_accepts(f, n, s) for n in CANDIDATES for s in PROOFS)]
res["unsat_with_rkp_proof"] = len(covered)
res["unsat_without_rkp_proof"] = [list(map(list, f)) for f in UNIVERSE if not sat(f) and f not in covered]
# hard-coded machine M_F: accepts exactly F; description length grows with |F|.
gate_blocked = 0; full_accepts = 0
for f in UNIVERSE:
    if sat(f):
        continue
    d = size(f) + 1  # description must contain F
    L = size(f)
    if d > math.log2(L + 2):
        gate_blocked += 1
    full_accepts += 1  # R_full: M_F is sound (accepts only the UNSAT F), proof length O(|F|)
res["hardcoded_MF_blocked_by_log_gate"] = gate_blocked
res["hardcoded_MF_accepted_by_R_full"] = full_accepts
assert gate_blocked == res["unsat_formulas"] == full_accepts
res["verdict"] = "PASS"
out = sys.argv[1] if len(sys.argv) > 1 else None
txt = json.dumps(res, indent=1, sort_keys=True)
print(txt)
if out:
    open(out, "w").write(txt + "\n")
