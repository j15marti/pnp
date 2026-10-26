"""ClaudeCircuitSAT ladder, run 1 (2026-10-26).
Encoding CSAT_{n,k}: gate j (1..k) has truth table tt_j in {0,1}^4 and two
addresses a_j,b_j in {0..n+j-2} (any earlier wire).  Output = gate k.
Part A: exact sensitivity of the chain instance (k sensitive bits).
Part B: exact minimum fan-in-2 (full B2 basis) circuit size of CSAT_{2,1}
        over its 6 encoding bits, by exhaustive search up to 3 gates.
Runtime well under 30 s."""
import itertools, json, math, sys

def csat(n, k, tts, addrs):
    best = False
    for x in range(1 << n):
        w = [(x >> i) & 1 for i in range(n)]
        for j in range(k):
            a, b = addrs[j]
            w.append(tts[j][2 * w[a] + w[b]])
        if w[-1]:
            return True
    return False

# Part A
A = []
for n in range(2, 6):
    k = n - 1
    tts = [[0, 0, 0, 1] for _ in range(k)]
    addrs = [((0, 1) if j == 0 else (n + j - 1, j + 1)) for j in range(k)]
    assert csat(n, k, tts, addrs)
    sens = 0
    for j in range(k):
        t2 = [list(t) for t in tts]; t2[j][3] = 0
        if not csat(n, k, t2, addrs): sens += 1
    A.append({"n": n, "k": k, "sensitive_tt_bits": sens})

# Part B: function of 6 vars (tt0..tt3, a, b) for n=2,k=1; wires: x1,x2 -> a,b select.
N = 6; M = 1 << N; FULL = (1 << M) - 1
def var(i): return sum(1 << m for m in range(M) if (m >> i) & 1)
vs = [var(i) for i in range(N)]
target = 0
for m in range(M):
    t = [(m >> i) & 1 for i in range(4)]; a = (m >> 4) & 1; b = (m >> 5) & 1
    # inputs x in {0,1}^2: exists x with tt[2*x_a+x_b]
    if any(t[2 * ((x >> a) & 1) + ((x >> b) & 1)] for x in range(4)):
        target |= 1 << m
ops = [lambda p, q: p & q, lambda p, q: p & ~q & FULL, lambda p, q: ~p & q & FULL,
       lambda p, q: ~(p | q) & FULL, lambda p, q: p | q, lambda p, q: (p | ~q) & FULL,
       lambda p, q: (~p | q) & FULL, lambda p, q: ~(p & q) & FULL, lambda p, q: p ^ q,
       lambda p, q: ~(p ^ q) & FULL]
def reach(wires, left):
    if target in wires: return True
    if left == 0: return False
    L = len(wires)
    for i in range(L):
        for j in range(i + 1, L):
            for o in ops:
                v = o(wires[i], wires[j])
                if v in wires: continue
                if reach(wires + [v], left - 1): return True
    return False
res = {}
mn = None
for g in range(0, 4):
    ok = reach(list(vs), g)
    res[g] = ok
    if ok and mn is None: mn = g
    print("gates<=", g, ok, flush=True)
out = {"partA": A, "partB_CSAT_2_1": {"target_is_input_var": target in vs, "reachable_by_gates": res, "min_gates_found": mn}}
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(out)
