"""Independent check of Lemma 60A (round-adaptive source batching): exactness + pass count.
Runs in well under 30s. Adaptive client: next-round queries depend on prior answers."""
import random, math

def run(N, R, Qr, B, seed):
    rnd = random.Random(seed)
    source = set(rnd.sample(range(10 * N), N))        # keyed parent source (N records)
    stream = sorted(source)                            # scanned linearly each pass
    passes = 0; seen = 0; state = seed
    for r in range(R):
        qs = [(state * 7919 + 31 * i + r) % (10 * N) for i in range(Qr)]   # fixed before round scans
        ans = {}
        for s in range(0, len(qs), B):
            blk = set(qs[s:s + B]); passes += 1        # dictionary of <=B keys, one full parent pass
            hit = {x for x in stream if x in blk}
            for q in blk: ans[q] = q in hit
        for q in qs: assert ans[q] == (q in source)    # exactness
        state = (state + sum(ans.values()) + 1) % 10**9  # adaptivity across rounds
        seen += Qr
    return passes, seen

bad = 0
for seed in range(40):
    N = random.Random(seed).choice([200, 500, 1000]); R = random.Random(seed+1).randint(1, 6)
    Qr = random.Random(seed+2).randint(1, 60); B = random.Random(seed+3).randint(1, 30)
    p, Q = run(N, R, Qr, B, seed)
    bound = Q / B + R
    if p > bound + 1e-9 or p != R * math.ceil(Qr / B): bad += 1
print("trials=40 violations=", bad)
