"""INDEX-ANY-DIGEST46 audit. Runtime << 30 s.
Checks: (1) pigeonhole collision for random nonlinear digests D:{0,1}^n->{0,1}^q, q<n,
differing at some coordinate; (2) exact optimum success of INDEX decoding for all
deterministic q=1 digests (n<=4) and q=2 (n=3), versus the Pinsker/entropy bound
succ <= 1/2 + sqrt(q ln2 /(2n)); (3) public-coin average cannot exceed that bound."""
import itertools, math, random
random.seed(46)
fails = 0; checks = 0
def succ(n, parts):
    # parts: dict msg -> list of x (ints). Bayes-optimal decoder per (msg,j).
    tot = 0
    for xs in parts.values():
        for j in range(n):
            ones = sum((x >> j) & 1 for x in xs)
            tot += max(ones, len(xs) - ones)
    return tot / (n * 2 ** n)
def bound(n, q): return 0.5 + math.sqrt(q * math.log(2) / (2 * n))
# (1) pigeonhole with random nonlinear digests
for n in range(3, 11):
    for q in range(1, n):
        for _ in range(20):
            tab = [random.randrange(2 ** q) for _ in range(2 ** n)]
            seen = {}
            for x in range(2 ** n):
                seen.setdefault(tab[x], []).append(x)
            col = next(v for v in seen.values() if len(v) > 1)
            d = col[0] ^ col[1]; checks += 1
            if d == 0: fails += 1
# (2) exhaustive optimum
best = {}
for n, q in [(2,1),(3,1),(4,1),(3,2)]:
    m = 2 ** q; b = 0
    for tab in itertools.product(range(m), repeat=2 ** n):
        parts = {}
        for x, t in enumerate(tab): parts.setdefault(t, []).append(x)
        b = max(b, succ(n, parts))
    best[(n, q)] = b; checks += 1
    if b > bound(n, q) + 1e-12: fails += 1
    print(f"n={n} q={q} exact optimum {b:.4f} <= bound {min(1,bound(n,q)):.4f}")
# (3) random public-coin mixtures
for n in range(3, 9):
    for q in range(1, n):
        mix = 0
        for _ in range(8):
            tab = [random.randrange(2 ** q) for _ in range(2 ** n)]
            parts = {}
            for x, t in enumerate(tab): parts.setdefault(t, []).append(x)
            mix += succ(n, parts) / 8
        checks += 1
        if mix > bound(n, q) + 1e-12: fails += 1
# threshold: q needed for success 2/3
for n in (100, 1000, 10**6):
    print(n, "q >= n/(18 ln2) =", n / (18 * math.log(2)))
print("checks", checks, "fails", fails)
