"""Independent check of the additive-slot identity and critical-window concentration
(CHMY-ADDITIVE-CRITICALWINDOW2). Independent uniform masks (gamma=0). Runs in a few seconds."""
import random, math, json
random.seed(20261019)
def run(n, r, j, trials):
    N = 1 << n
    ok = 0
    for _ in range(trials):
        G = random.getrandbits(N); D = [random.getrandbits(N) for _ in range(r)]
        T = [random.getrandbits(N) for _ in range(r)]
        f = random.getrandbits(N)
        def fk(mod):
            g = G
            for i in range(1, r):
                d = D[i] ^ (f if (mod and i == j) else 0)
                g = d ^ (T[i] & g)
            return g
        B = (1 << N) - 1
        for i in range(j + 1, r): B &= T[i]
        ok += fk(True) == fk(False) ^ (B & f)
    return ok == trials
res = {"identity": all(run(n, n, j, 200) for n in (4, 5, 6) for j in range(1, n))}
# concentration: |supp B_j| vs N*2^-t, and early-slot differing probability q*2^-t
rows = []
for n in (10, 12):
    N = 1 << n
    for t in range(0, n):
        ys = []
        for _ in range(200):
            B = (1 << N) - 1
            for _ in range(t): B &= random.getrandbits(N)
            ys.append(bin(B).count("1"))
        rows.append((n, t, sum(ys) / len(ys), N / 2 ** t))
res["support_mean_vs_theory"] = [(n, t, round(m, 2), th) for n, t, m, th in rows if t in (0, 3, 6, 9)]
print(json.dumps(res))
