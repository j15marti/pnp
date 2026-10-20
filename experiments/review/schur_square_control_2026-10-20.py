"""Schur-square dimension: random [n,k] codes vs Reed-Solomon over F_p (finishes in seconds)."""
import random, json, sys
p = 97
def rank(rows):
    rows = [r[:] for r in rows]; r = 0
    for c in range(len(rows[0]) if rows else 0):
        piv = next((i for i in range(r, len(rows)) if rows[i][c] % p), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][c], p - 2, p)
        rows[r] = [x * inv % p for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] % p:
                f = rows[i][c]; rows[i] = [(a - f * b) % p for a, b in zip(rows[i], rows[r])]
        r += 1
    return r
def square_dim(G):
    k = len(G); return rank([[a * b % p for a, b in zip(G[i], G[j])] for i in range(k) for j in range(i, k)])
random.seed(1); out = []
for n, k in [(40, 6), (40, 10), (60, 8), (60, 12), (80, 12)]:
    rs = [[pow(x, i, p) for x in range(1, n + 1)] for i in range(k)]
    rnd = [min(k * (k + 1) // 2, n)]
    ds = [square_dim([[random.randrange(p) for _ in range(n)] for _ in range(k)]) for _ in range(5)]
    out.append(dict(n=n, k=k, RS=square_dim(rs), RS_pred=min(2 * k - 1, n), random=ds, random_pred=min(k * (k + 1) // 2, n)))
print(json.dumps(out, indent=1))
