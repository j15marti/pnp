"""Independent exact recheck of the FLOOR3 multiport survival bounds (single coordinate, per-layer
Bernoulli(p) masks, independent across layers). Exact rational arithmetic; no sampling."""
import itertools, json
from fractions import Fraction as Fr

def prob_Q(h, J, ps):
    tot = Fr(0)
    for bits in itertools.product((0, 1), repeat=h):  # bits[i-1] = T_i(a)
        w = Fr(1)
        for i, b in enumerate(bits):
            w *= ps[i] if b else 1 - ps[i]
        q = 0
        for j in J:
            B = 1
            for i in range(j + 1, h + 1):
                B &= bits[i - 1]
            q ^= B
        if q:
            tot += w
    return tot

res = {"checked": 0, "violations": 0, "lower_attained": [], "upper_attained": []}
for h in range(2, 9):
    for gam in (Fr(0), Fr(1, 10), Fr(1, 4)):
        for sign in (1, -1):
            p = Fr(1, 2) + sign * gam
            ps = [p] * h
            for r in range(1, h + 1):
                for J in itertools.combinations(range(1, h + 1), r):
                    t = h - max(J)
                    P = prob_Q(h, J, ps)
                    lo, hi = (Fr(1, 2) - gam) ** (t + 1), (Fr(1, 2) + gam) ** t
                    res["checked"] += 1
                    if not (lo <= P <= hi):
                        res["violations"] += 1
                    if gam == 0 and P == lo and len(J) == 2: res["lower_attained"].append([h, list(J)]) if len(res["lower_attained"]) < 3 else None
                    if gam == 0 and P == hi and len(J) == 1: res["upper_attained"].append([h, list(J)]) if len(res["upper_attained"]) < 3 else None
# mixed per-layer biases (independent, non-identical)
import random
random.seed(20261020)
mix = 0
for _ in range(3000):
    h = random.randint(2, 8); g = Fr(random.randint(0, 20), 100)
    ps = [Fr(1, 2) + random.choice((-1, 1)) * Fr(random.randint(0, int(g * 100)), 100) for _ in range(h)]
    J = tuple(sorted(random.sample(range(1, h + 1), random.randint(1, h))))
    t = h - max(J); P = prob_Q(h, J, ps)
    lo = min(Fr(1, 2) - g, min(1 - x for x in ps) )  # keep conservative
    lo, hi = (Fr(1, 2) - g) ** (t + 1), (Fr(1, 2) + g) ** t
    mix += 1
    if not (lo <= P <= hi): res["violations"] += 1
res["mixed_bias_trials"] = mix
# cross-layer correlation control: T2=T3 kills Q for J={1,2}, h=3
tot = Fr(0)
for t1, t2 in itertools.product((0, 1), repeat=2):
    T = (t1, t2, t2); q = 0
    for j in (1, 2):
        B = 1
        for i in range(j + 1, 4): B &= T[i - 1]
        q ^= B
    tot += Fr(1, 4) * q
res["correlated_control_prob"] = str(tot)
print(json.dumps(res, indent=1))
json.dump(res, open("results/raw/separation/2026-10-20_CHMY_MULTIPORT_INDEP_RECHECK.json", "w"), indent=1)
