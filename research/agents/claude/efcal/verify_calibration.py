"""CLAUDE/EFCAL-0001: exhaustive check of the propositional calibration identities.
Atoms: P = "SAT in P", S = "Wbar_R superpolynomial", E = "EF superpolynomial (worst-case CNF)".
Definitions: B1 := S ; B3 := (P -> not S).  Under the simulation hypothesis H: S <-> E.
Checks (all 8 / 16 valuations):
 (1) B1 and B3  <->  S and not P
 (2) not P -> B3                     (B3 is vacuously true if P != NP)
 (3) S -> (B3 <-> not P)             (given a proved lower bound, B3 is exactly P != NP)
 (4) under H: B1 <-> E and B3 <-> (P -> not E)
Runs in milliseconds."""
import itertools, json, sys
imp = lambda a, b: (not a) or b
res = {"checks": 0, "fail": []}
for P, S, E in itertools.product([False, True], repeat=3):
    B1, B3 = S, imp(P, not S)
    tests = {
        "1": (B1 and B3) == (S and not P),
        "2": imp(not P, B3),
        "3": imp(S, B3 == (not P)),
    }
    if S == E:  # hypothesis H
        tests["4"] = (B1 == E) and (B3 == imp(P, not E))
    for k, v in tests.items():
        res["checks"] += 1
        if not v:
            res["fail"].append([k, P, S, E])
res["status"] = "PASS" if not res["fail"] else "FAIL"
json.dump(res, sys.stdout, indent=1); print()
