# Frontier-DP ladder: for a Boolean function f on n vars (truth table), the number of
# distinct residual subfunctions after fixing the first k variables of an ordering pi
# is the OBDD level width; maxwidth(pi)=max_k. min over pi = "frontier-state lower bound"
# for any left-to-right DP over pi. Runs < 30s per n via small sizes.
import itertools, random, json, sys
def tt_from_cnf(n, clauses):
    t = 0
    for a in range(1 << n):
        ok = all(any(((a >> (abs(l)-1)) & 1) == (1 if l > 0 else 0) for l in c) for c in clauses)
        if ok: t |= 1 << a
    return t
def widths(n, tt, pi):
    # residual after fixing pi[0..k-1]: table over assignments of the rest
    res = []
    rest_cache = {}
    out = []
    for k in range(n+1):
        fixed, free = pi[:k], pi[k:]
        seen = set()
        for fa in range(1 << k):
            base = 0
            for i, v in enumerate(fixed):
                if (fa >> i) & 1: base |= 1 << v
            sig = 0
            for ra in range(1 << (n-k)):
                a = base
                for i, v in enumerate(free):
                    if (ra >> i) & 1: a |= 1 << v
                if (tt >> a) & 1: sig |= 1 << ra
            seen.add(sig)
        out.append(len(seen))
    return max(out)
def minwidth(n, tt, limit):
    best = None
    perms = list(itertools.permutations(range(n)))
    random.Random(0).shuffle(perms)
    for pi in perms[:limit]:
        w = widths(n, tt, list(pi))
        if best is None or w < best: best = w
    return best
def eq(n):  # n = 2m vars; x_i == y_i
    m = n//2; t = 0
    for a in range(1 << n):
        if all(((a >> i) & 1) == ((a >> (m+i)) & 1) for i in range(m)): t |= 1 << a
    return t
res = {}
n = int(sys.argv[1]); lim = int(sys.argv[2]); seeds = int(sys.argv[3])
rows = []
for s in range(seeds):
    r = random.Random(1000*n+s)
    m = round(4.26*n); cl = [[r.choice([-1,1])*v for v in r.sample(range(1,n+1),3)] for _ in range(m)]
    tt = tt_from_cnf(n, cl)
    rows.append((bin(tt).count("1"), minwidth(n, tt, lim)))
print(json.dumps({"n": n, "perm_sample": lim, "rows": rows}))
if n % 2 == 0:
    m = n//2; tt = eq(n)
    sep = list(range(n)); inter = [x for i in range(m) for x in (i, m+i)]
    print(json.dumps({"EQ_n": n, "sep": widths(n, tt, sep), "interleaved": widths(n, tt, inter)}))
