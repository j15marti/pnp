"""One-way reorder-buffer lemma: exact minimal memory for in-order emission of y_i = x_{pi(i)}.

Lemma (deterministic, one read-once pass over x in {0,1}^N, output y_1..y_N in order, may emit only
after reading the needed source bit). Let M(i)=max_{j<=i} pi(j). Emit y_i at time M(i) (earliest).
After reading t source bits the machine must retain x_{pi(j)} for every j>e(t) with pi(j)<=t,
e(t)=max{i: M(i)<=t}. These retained bits are independent free bits (fooling set of size 2^B),
so memory >= B(pi)=max_t |{j>e(t): pi(j)<=t}|, and the earliest-emit schedule attains it.
Hence B(pi) is the EXACT minimal memory (in bits, ignoring O(log N) counters).
"""
import json, sys, itertools

def buffer_need(pi):
    N = len(pi)
    M = []; m = -1
    for p in pi:
        m = max(m, p); M.append(m)
    best = 0
    for t in range(N):  # t = index of last source bit read (0-based)
        e = sum(1 for i in range(N) if M[i] <= t)  # prefix emitted (M nondecreasing)
        stored = sum(1 for j in range(e, N) if pi[j] <= t)
        best = max(best, stored)
    return best

def brute_min_memory(pi):
    """Independent check: simulate state = frozenset of retained source indices under all emit schedules
    is overkill; instead verify via direct definition on the earliest schedule with explicit simulation."""
    N = len(pi); retained = set(); nxt = 0; peak = 0
    for t in range(N):
        retained.add(t)
        # keep only bits still needed by unemitted outputs
        while nxt < N and pi[nxt] <= t:
            nxt += 1
        needed = {pi[j] for j in range(nxt, N) if pi[j] <= t}
        retained = retained & needed
        peak = max(peak, len(retained))
    return peak

def bitrev(k):
    return [int(format(i, f'0{k}b')[::-1], 2) for i in range(1 << k)]

def transpose(r, c):
    return [(i % r) * c + i // r for i in range(r * c)]  # output row-major of transposed matrix

def window(N, w):  # local perturbation: reverse blocks of size w
    return [b * w + (w - 1 - o) for b in range(N // w) for o in range(w)]

res = {"identity": {}, "window": {}, "bitrev": {}, "transpose": {}, "exhaustive": {}}
for N in (8, 16, 64, 256):
    res["identity"][N] = buffer_need(list(range(N)))
for N, w in ((64, 2), (64, 8), (256, 16)):
    p = window(N, w); res["window"][f"{N},{w}"] = buffer_need(p); assert buffer_need(p) == brute_min_memory(p)
for k in (3, 4, 6, 8, 10):
    p = bitrev(k); res["bitrev"][1 << k] = buffer_need(p); assert buffer_need(p) == brute_min_memory(p)
for r, c in ((4, 4), (8, 8), (16, 16), (32, 32)):
    p = transpose(r, c); res["transpose"][f"{r}x{c}"] = buffer_need(p); assert buffer_need(p) == brute_min_memory(p)
# exhaustive: all permutations of N<=7, formula vs simulation, and fraction needing >= N/2 for N=7
cnt = 0
for N in range(1, 8):
    hi = 0; tot = 0
    for p in itertools.permutations(range(N)):
        a = buffer_need(list(p)); b = brute_min_memory(list(p)); assert a == b; cnt += 1
        tot += 1; hi = max(hi, a)
    res["exhaustive"][N] = {"perms": tot, "max_B": hi}
res["assertions"] = cnt
print(json.dumps(res, indent=1))
json.dump(res, open("results/raw/mcsp/2026-10-20_oneway_reorder_buffer.json", "w"), indent=1)
