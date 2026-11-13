#!/usr/bin/env python3
"""CLAUDE B3-CONSERVATION-0001 finite sanity checks (runs < 1 s).

Part A: exhaustive propositional skeleton of Lemmas 1-3 over atoms
  S   = "SAT in P"
  P1  = PB(R)   (Wbar_R polynomially bounded)
  P2  = PB(R')  with R <=_W R' (weight-compatible p-simulation), so P1 -> P2.
Part B: numerical sanity of the quantifier-negation step (Lemma 0):
  not(exists C,k forall N: W(N) <= C(N+1)^k)  implies
  forall C,k,N0 exists N >= N0: W(N) > C(N+1)^k,
  checked by the explicit padding constant C' on finite random prefixes.
These checks verify only the logical skeleton; they prove nothing about SAT.
"""
import itertools, json, random, sys
from fractions import Fraction

def imp(a, b): return (not a) or b

checks = 0
for S, P1, P2 in itertools.product([False, True], repeat=3):
    if not imp(P1, P2):            # simulation hypothesis R <=_W R'
        continue
    B3_R, B3_R2 = imp(S, P1), imp(S, P2)
    LB_R, LB_R2 = not P1, not P2
    assert B3_R == ((not S) or P1); checks += 1          # Lemma 1
    if LB_R: assert B3_R == (not S); checks += 1          # Lemma 2
    assert imp(B3_R, B3_R2); checks += 1                  # Lemma 3 (B3 up)
    assert imp(LB_R2, LB_R); checks += 1                  # Lemma 3 (LB down)
    assert imp(LB_R and B3_R, not S); checks += 1         # Route B closure
    assert imp(not S, B3_R and B3_R2); checks += 1        # SAT notin P gives every B3

# Part B: padding constant (exact rational arithmetic).  For a finite prefix W(0..M) and a pair (C,k,N0),
# C' = max(C, max_{N<N0} W(N)/(N+1)^k) satisfies C'(N+1)^k >= W(N) for N<N0,
# so any violation of C' must occur at N >= N0 and is also a violation of C.
rng = random.Random(20261113)
pad_checks = 0
for _ in range(2000):
    M = rng.randint(5, 60); k = rng.randint(0, 3); C = Fraction(rng.randint(1, 50), 10)
    N0 = rng.randint(0, M)
    W = [rng.randint(0, 10 * (N + 1) ** (k + rng.randint(0, 2))) for N in range(M + 1)]
    Cp = max([C] + [Fraction(W[N], (N + 1) ** k) for N in range(N0)])
    viol = [N for N in range(M + 1) if W[N] > Cp * (N + 1) ** k]
    for N in viol:
        assert N >= N0 and W[N] > C * (N + 1) ** k
    pad_checks += 1

out = {"run": "CLAUDE_B3-CONSERVATION-0001", "skeleton_assertions": checks,
       "padding_cases": pad_checks, "status": "PASS",
       "scope": "logical skeleton only; no SAT/proof-complexity claim"}
json.dump(out, sys.stdout, indent=2); print()
