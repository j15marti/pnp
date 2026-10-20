"""SAT-LABEL-CERTIFICATE-COVER28: exact check of the certificate lower bound.
Source = indicator vector over all 8*C(n,3) three-literal clauses on distinct vars.
x_a = all clauses satisfied by assignment a.  Claim: x_a is satisfied only by a,
and adding any missing clause (falsified by a) makes it UNSAT.  Hence every
certificate for SAT(x_a)=1 must fix all C(n,3) missing-clause bits to 0.
"""
import itertools, json, time
t0 = time.time()
res = []
for n in range(3, 8):
    clauses = [(v, s) for vs in itertools.combinations(range(n), 3)
               for s in itertools.product((0, 1), repeat=3) for v in [vs]]
    def sat_by(cl, b):  # clause satisfied by assignment bits b (tuple)
        vs, s = cl
        return any(b[v] == sg for v, sg in zip(vs, s))
    assigns = list(itertools.product((0, 1), repeat=n))
    a = tuple([0] * n)
    x = [c for c in clauses if sat_by(c, a)]
    missing = [c for c in clauses if not sat_by(c, a)]
    sols = [b for b in assigns if all(sat_by(c, b) for c in x)]
    ok_unique = sols == [a]
    ok_cover = all(not any(all(sat_by(c, b) for c in x + [m]) for b in assigns) for m in missing)
    from math import comb
    res.append(dict(n=n, N=len(clauses), missing=len(missing), C_n_3=comb(n, 3),
                    unique=ok_unique, every_missing_kills=ok_cover))
    assert ok_unique and ok_cover and len(missing) == comb(n, 3)
res_all = dict(run="SAT-LABEL-CERTIFICATE-COVER28", cases=res, seconds=round(time.time() - t0, 2))
json.dump(res_all, open("results/raw/synthesis/2026-10-21_SAT_LABEL_CERTIFICATE_COVER28.json", "w"), indent=1)
print(json.dumps(res_all, indent=1))
