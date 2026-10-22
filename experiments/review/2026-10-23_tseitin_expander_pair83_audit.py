"""TSEITIN-EXPANDER-PAIR83 audit (pure python, runs in a few seconds).
Paired YES/NO bounded-occurrence expander CNFs: Tseitin parity on a random cubic graph,
charges differing at one vertex. Checks: pair differs in exactly 4 clauses; NO instance is
minimally unsatisfiable (every clause needed) for small n; incidence graph spectral gap;
every-branch deletion bound |R|<=(1+Delta)k; global polarity-XOR signature; GF(2) decider."""
import random, itertools, json, sys

def cubic_graph(n, rng):
    while True:
        pts = [v for v in range(n) for _ in range(3)]
        rng.shuffle(pts)
        edges = set(); ok = True
        for i in range(0, len(pts), 2):
            a, b = pts[i], pts[i+1]
            if a == b or (min(a,b), max(a,b)) in edges: ok = False; break
            edges.add((min(a,b), max(a,b)))
        if ok:
            # connectivity
            adj = {v: [] for v in range(n)}
            for a, b in edges: adj[a].append(b); adj[b].append(a)
            seen = {0}; st = [0]
            while st:
                u = st.pop()
                for w in adj[u]:
                    if w not in seen: seen.add(w); st.append(w)
            if len(seen) == n: return sorted(edges)

def tseitin(n, edges, charge):
    inc = {v: [] for v in range(n)}
    for i, (a, b) in enumerate(edges): inc[a].append(i+1); inc[b].append(i+1)
    clauses = []
    for v in range(n):
        vs = inc[v]
        for bits in itertools.product([0,1], repeat=3):
            if sum(bits) % 2 != charge[v]:   # forbid wrong-parity assignment
                clauses.append(tuple((x if b == 0 else -x) for x, b in zip(vs, bits)))
    return clauses

def sat_bruteforce(clauses, m):
    for mask in range(1 << m):
        if all(any(((mask >> (abs(l)-1)) & 1) == (1 if l > 0 else 0) for l in c) for c in clauses): return True
    return False

def gf2_decide(n, edges, charge):
    rows = []
    for v in range(n):
        r = 0
        for i, (a, b) in enumerate(edges):
            if v in (a, b): r |= 1 << i
        rows.append((r, charge[v]))
    piv = {}
    for r, c in rows:
        while r:
            h = r.bit_length()-1
            if h in piv: pr, pc = piv[h]; r ^= pr; c ^= pc
            else: piv[h] = (r, c); break
        else:
            if c: return False
    return True

def lambda2_incidence(n, edges, clauses, iters=300, rng=random.Random(1)):
    m = len(edges); V = m + len(clauses)
    adj = [[] for _ in range(V)]
    for ci, c in enumerate(clauses):
        for l in c: adj[abs(l)-1].append(m+ci); adj[m+ci].append(abs(l)-1)
    deg = [len(a) for a in adj]
    # lazy normalized walk P=(I+D^-1/2 A D^-1/2)/2 ; deflate top eigenvector sqrt(deg)
    top = [d**0.5 for d in deg]; nt = sum(t*t for t in top)**0.5; top = [t/nt for t in top]
    x = [rng.random()-.5 for _ in range(V)]
    lam = 0
    for _ in range(iters):
        p = sum(a*b for a, b in zip(x, top)); x = [a-p*b for a, b in zip(x, top)]
        y = [0.5*xi + 0.5*sum(x[j]/(deg[i]*deg[j])**0.5 for j in adj[i]) for i, xi in enumerate(x)]
        nx = sum(a*a for a in x)**0.5; ny = sum(a*a for a in y)**0.5
        lam = ny/nx; x = [a/ny for a in y]
    return 2*lam-1, max(deg)

rng = random.Random(83)
res = {"id": "TSEITIN-EXPANDER-PAIR83", "trials": 0, "assertions": 0, "failures": 0}
def check(c):
    res["assertions"] += 1
    if not c: res["failures"] += 1

sig = lambda cl: (sum(1 - (sum(1 for l in c if l < 0) % 2) for c in cl) // 4) % 2
# (1) small n: minimal unsatisfiability, pair difference, GF(2) agreement
for n in (6, 8):
    for _ in range(6):
        E = cubic_graph(n, rng); m = len(E)
        ch = [rng.randint(0,1) for _ in range(n)]
        if sum(ch) % 2: ch[0] ^= 1
        yes = tseitin(n, E, ch); ch2 = ch[:]; ch2[rng.randrange(n)] ^= 1; no = tseitin(n, E, ch2)
        check(sat_bruteforce(yes, m)); check(not sat_bruteforce(no, m))
        check(gf2_decide(n, E, ch) and not gf2_decide(n, E, ch2))
        check(len(set(yes) ^ set(no)) == 8)  # 4 clauses removed + 4 added at flipped vertex
        for i in range(len(no)):
            check(sat_bruteforce(no[:i]+no[i+1:], m))   # minimally unsatisfiable
        # polarity signature: parity of #negated literals over all clauses
        sig = lambda cl: (sum(1 - (sum(1 for l in c if l < 0) % 2) for c in cl) // 4) % 2  # total charge read off clause polarities, one linear scan
        check(sig(yes) != sig(no))
        res["trials"] += 1

# (2) larger n: spectral gap, every-branch deletion bound, GF(2) vs polarity signature
gaps = []; sigagree = 0; T = 0; maxfrac_min = 1
for n in (64, 128, 256):
    for _ in range(3):
        E = cubic_graph(n, rng); m = len(E)
        ch = [rng.randint(0,1) for _ in range(n)]
        if sum(ch) % 2: ch[0] ^= 1
        ch2 = ch[:]; ch2[rng.randrange(n)] ^= 1
        yes, no = tseitin(n, E, ch), tseitin(n, E, ch2)
        gap, Delta = lambda2_incidence(n, E, yes); gaps.append(round(1-gap, 3))
        check(Delta <= 8 and all(sum(1 for c in yes for l in c if abs(l) == v) == 8 for v in range(1, m+1)))
        # every-branch deletion: random assignment to k vars; removed = vars + satisfied clauses
        for _ in range(200):
            k = rng.randint(1, 4); X = rng.sample(range(1, m+1), k); a = {x: rng.randint(0,1) for x in X}
            sat_cl = [c for c in yes if any(abs(l) in a and (a[abs(l)] == (l > 0)) for l in c)]
            check(k + len(sat_cl) <= (1+Delta)*k)
        sig = lambda cl: (sum(1 - (sum(1 for l in c if l < 0) % 2) for c in cl) // 4) % 2  # total charge read off clause polarities, one linear scan
        for cl, c in ((yes, ch), (no, ch2)):
            # each clause at v forbids a pattern with parity != charge[v]; #neg literals encodes charge
            T += 1; sigagree += (gf2_decide(n, E, c) == (sig(cl) == 0))
        res["trials"] += 1
res["spectral_gap_incidence_1_minus_lambda2"] = gaps
res["signature_matches_decider"] = f"{sigagree}/{T}"
check(sigagree == T)
print(json.dumps(res))
sys.exit(1 if res["failures"] else 0)
