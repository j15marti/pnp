#!/usr/bin/env python3
"""Late additive-layer injection audit (follow-up to FKBASEERASURE1).
Injects f into additive layer D_j: G_{i+1}=D_i^(T_i&G_i), D_j -> D_j^f.
Checks exact identity: out(f)^out(f') = (f^f') & AND_{i>j} T_i, and measures
surviving-difference fraction vs 2^-k, k=#mask layers above the injection.
Toy GF(2^h) parameters; checks local recurrence only. Runtime << 30 s."""
import json, random, sys
sys.path.insert(0, "experiments/review")
import importlib.util
spec = importlib.util.spec_from_file_location("fk", "experiments/review/2026-10-20_FKBASEERASURE1_audit.py")
fk = importlib.util.module_from_spec(spec); spec.loader.exec_module(fk)
rng = random.Random(202610200100)
N, h = 32, 5; poly = fk.IRREDUCIBLES[5]; mask = (1 << N) - 1; r = 5
res = {"N": N, "h": h, "r": r, "seed": 202610200100, "rows": []}
def rmask(): return fk.t_mask(rng.randrange(1 << h), rng.randrange(1 << h), N, h, poly)
for k in range(0, r):
    trials, fails, surv = 4000, 0, 0
    for _ in range(trials):
        Ds = [rng.getrandbits(N) for _ in range(r - 1)]
        Ts = [rmask() for _ in range(r - 1)]
        f, g = rng.getrandbits(N), rng.getrandbits(N)
        j = r - 2 - (k - 1) if k > 0 else None  # injection layer index; k masks above
        def run(src):
            x = rng.getrandbits(N) if False else base
            for i in range(r - 1):
                d = Ds[i] ^ (src if (k == 0 and i == r - 2) or (k > 0 and i == r - 1 - k) else 0)
                x = (d ^ (Ts[i] & x)) & mask
            return x
        base = 0
        diff = run(f) ^ run(g)
        pred = f ^ g
        top = [Ts[i] for i in range(r - 1) if i > (r - 2 if k == 0 else r - 1 - k)]
        for t in top: pred &= t
        fails += diff != pred
        surv += diff.bit_count()
    res["rows"].append({"row_k": k, "trials": trials, "identity_failures": fails,
        "mean_surviving_fraction_of_N/2_diff": surv / trials / (N / 2), "masks_above_injection": max(k-1,0), "ideal_((1-2^-h)/2)^m": ((1-2.0**-h)/2)**max(k-1,0)})
print(json.dumps(res, indent=1))
json.dump(res, open("results/raw/separation/2026-10-20_LATEDLAYER1.json", "w"), indent=1)
