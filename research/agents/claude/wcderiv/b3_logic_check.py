#!/usr/bin/env python3
"""Exhaustive propositional check of the B3 bookkeeping identities in
CLAUDE WCDERIV-0001.  Atoms (truth values of open statements):
  PNP  : P = NP              (so SAT in P  <=>  PNP)
  BR   : W_R(N) <= poly(N)   (R polynomially bounded on 3-CNF)
  BS   : W_S(N) <= poly(N)   for a system S with  S <=_p R  (R p-simulates S)
Constraint used: S <=_p R, hence BS -> BR (a short S-proof gives a short R-proof).
B3(X) := PNP -> BX.   LB(X) := not BX.
The script enumerates all admissible assignments and checks each claim.
Runs in well under one second."""
import itertools, json, sys

def imp(a, b):
    return (not a) or b

claims = {
    "T1: B3(R) <-> (not PNP or BR)": lambda P, R, S: imp(P, R) == ((not P) or R),
    "T1': LB(R) -> (B3(R) <-> not PNP)": lambda P, R, S: imp(not R, imp(P, R) == (not P)),
    "T2: B3(R) and LB(R) -> not PNP": lambda P, R, S: imp(imp(P, R) and not R, not P),
    "T3: LB(R) -> LB(S)  (given S <=_p R)": lambda P, R, S: imp(not R, not S),
    "T4: B3(S) -> B3(R)  (monotone upward)": lambda P, R, S: imp(imp(P, S), imp(P, R)),
    "T5: not PNP -> B3(X) for every X": lambda P, R, S: imp(not P, imp(P, R) and imp(P, S)),
}
# a deliberately false claim as a hostile control: B3 does NOT transfer downward
control = ("CONTROL (must FAIL): B3(R) -> B3(S)", lambda P, R, S: imp(imp(P, R), imp(P, S)))

out, ok = {}, True
rows = [(P, R, S) for P, R, S in itertools.product([False, True], repeat=3) if imp(S, R)]
for name, f in claims.items():
    good = all(f(*r) for r in rows)
    out[name] = good
    ok &= good
cname, cf = control
cex = [r for r in rows if not cf(*r)]
out[cname] = {"holds": not cex, "counterexamples": [dict(PNP=a, BR=b, BS=c) for a, b, c in cex]}
ok &= bool(cex)
out["admissible_rows"] = len(rows)
out["ALL_PASS"] = ok
print(json.dumps(out, indent=1))
sys.exit(0 if ok else 1)
