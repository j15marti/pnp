"""COVER-SPLIT-RANK76 audit: the two-party cover matrix M[A,B]=1 iff A|B == U (U has m points)
is the disjointness matrix up to complementing columns, hence has full real rank 2^m.
Also verifies the fooling set {(A, U\\A)}. Runtime << 30 s (m<=8 -> 256x256)."""
import json
P = 1000003  # full rank mod P implies full rank over Q

def rank_mod(M):
    M = [r[:] for r in M]; rk = 0; n = len(M)
    for c in range(n):
        piv = next((i for i in range(rk, n) if M[i][c] % P), None)
        if piv is None: continue
        M[rk], M[piv] = M[piv], M[rk]
        inv = pow(M[rk][c], P - 2, P)
        M[rk] = [x * inv % P for x in M[rk]]
        for i in range(n):
            if i != rk and M[i][c] % P:
                f = M[i][c]; M[i] = [(x - f * y) % P for x, y in zip(M[i], M[rk])]
        rk += 1
    return rk

res = {}
fails = 0
for m in range(1, 9):
    n = 1 << m
    full = n - 1
    M = [[int((a | b) == full) for b in range(n)] for a in range(n)]
    rank = rank_mod(M)
    # fooling set: (A, ~A) are covers; (A,~A') for A!=A' with both orders cannot both cover
    ok = all(((a | (full ^ a)) == full) for a in range(n))
    for a in range(n):
        for b in range(n):
            if a != b and ((a | (full ^ b)) == full) and ((b | (full ^ a)) == full):
                ok = False
    res[m] = {"rank": rank, "size": n, "fooling_ok": bool(ok)}
    fails += (rank != n) + (not ok)
print(json.dumps({"results": res, "failures": fails}))
json.dump({"results": res, "failures": fails}, open("results/review/2026-10-22_2448_COVER_SPLIT_RANK76.json", "w"), indent=1)
