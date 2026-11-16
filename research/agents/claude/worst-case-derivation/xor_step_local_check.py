"""Exhaustive check of the constant-size local lemmas used to simulate the
R_mix341 XOR rule in Extended Frege with prefix-parity extension variables.
Deterministic, no seed. Finite check of constant-size implications only."""
import itertools, json
res = {}
# Step lemma: q_i = qp_i xor c_i*x (i=1,2,3), c3=c1^c2, hyp qp3=qp1^qp2  =>  q3=q1^q2
ok = True; cases = 0
for c1, c2 in itertools.product((0, 1), repeat=2):
    c3 = c1 ^ c2
    for x, p1, p2, p3, q1, q2, q3 in itertools.product((0, 1), repeat=7):
        cases += 1
        prem = q1 == p1 ^ (c1 & x) and q2 == p2 ^ (c2 & x) and q3 == p3 ^ (c3 & x) and p3 == p1 ^ p2
        if prem and q3 != q1 ^ q2: ok = False
res["step_lemma"] = {"holds": ok, "assignments_checked": cases}
# Base: all prefix parities at index 0 are constant 0, so 0 = 0 xor 0 (trivial).
# Final: q1_n=b1, q2_n=b2, q3_n=q1_n^q2_n  =>  q3_n = b1^b2
ok2 = all((not (q1 == b1 and q2 == b2 and q3 == q1 ^ q2)) or q3 == b1 ^ b2
          for b1, b2, q1, q2, q3 in itertools.product((0, 1), repeat=5))
res["final_lemma"] = {"holds": ok2}
# End-to-end semantic sanity: the chained prefix parity equals parity over the support.
import random
rng = random.Random(20261116); e2e = True
for _ in range(2000):
    n = rng.randint(1, 12)
    m1 = [rng.randint(0, 1) for _ in range(n)]; m2 = [rng.randint(0, 1) for _ in range(n)]
    xs = [rng.randint(0, 1) for _ in range(n)]
    def pref(m):
        q = 0
        for c, x in zip(m, xs): q ^= c & x
        return q
    m3 = [a ^ b for a, b in zip(m1, m2)]
    if pref(m3) != pref(m1) ^ pref(m2): e2e = False
res["end_to_end_random"] = {"holds": e2e, "trials": 2000, "seed": 20261116}
print(json.dumps(res, indent=1))
