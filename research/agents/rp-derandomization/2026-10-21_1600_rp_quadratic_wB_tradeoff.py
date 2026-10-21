#!/usr/bin/env python3
"""Block-size tradeoff falsifier for the quadratic-phase RP verifier.
Verifier accepts iff Q(r)=sum_{i<j} M_ij r_i r_j = 0 over F2 (r in {0,1}^n), M random.
Blocks of b consecutive bits. State at a boundary = Myhill-Nerode class of the
residual function on remaining bits (exact minimal layered width w).
B = max over (layer,q,q') of normalized Fourier L1 of 1[T(q,r)=q'] on a block.
Reports w*B vs 2^(n/2). Runtime: seconds."""
import itertools, random, json, sys
def residual_tables(n, M):
    # f[x] for all x in {0,1}^n; bit i of x = r_i (r_0 first block)
    f = []
    for x in range(1 << n):
        s = 0
        for i in range(n):
            if (x >> i) & 1:
                for j in range(i + 1, n):
                    if (x >> j) & 1 and M[i][j]:
                        s ^= 1
        f.append(s)
    return f
def run(n, b, seed):
    rnd = random.Random(seed)
    M = [[rnd.randint(0, 1) for _ in range(n)] for _ in range(n)]
    f = residual_tables(n, M)
    L = n // b
    # prefix a in {0,1}^{ib}: residual = tuple over suffix y of f[a | y<<ib]
    classes = []  # per boundary: dict prefix -> class id
    for i in range(L + 1):
        pb = i * b
        sig = {}
        cl = {}
        for a in range(1 << pb):
            t = tuple(f[a | (y << pb)] for y in range(1 << (n - pb)))
            cl[a] = sig.setdefault(t, len(sig))
        classes.append((cl, len(sig)))
    w = max(c[1] for c in classes)
    B = 0.0
    for i in range(L):
        cl_i, k_i = classes[i]
        cl_n, k_n = classes[i + 1]
        # representative prefix per class
        rep = {}
        for a, c in cl_i.items():
            rep.setdefault(c, a)
        for q, a in rep.items():
            for q2 in range(k_n):
                g = [1 if cl_n[a | (r << (i * b))] == q2 else 0 for r in range(1 << b)]
                # normalized Walsh-Hadamard L1
                tot = 0.0
                for s in range(1 << b):
                    c = sum(g[r] * (-1) ** bin(r & s).count("1") for r in range(1 << b)) / (1 << b)
                    tot += abs(c)
                B = max(B, tot)
    return w, B
res = []
for n in (8, 10, 12):
    for b in (1, 2, 4, n // 2):
        if n % b: continue
        ws, Bs = zip(*(run(n, b, s) for s in range(3)))
        w, B = max(ws), max(Bs)
        res.append(dict(n=n, b=b, ell=n // b, w=w, B=round(B, 3), wB=round(w * B, 2), two_pow_half_n=round(2 ** (n / 2), 1)))
        print(res[-1], flush=True)
json.dump(res, open(sys.argv[1] if len(sys.argv) > 1 else "/dev/null", "w"), indent=1)
