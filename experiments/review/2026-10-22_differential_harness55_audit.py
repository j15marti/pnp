#!/usr/bin/env python3
"""Differential representation harness for DIFFERENTIAL-HARNESS55.

For one fixed easy language slice (D(x)=parity of x, n-bit inputs) compare three
equivalent RP verifiers V_B, V_bit, V_0 on candidate invariants.  An invariant
is language-level only if it agrees on all three.  Finite controls only.
"""
import itertools, json

n_in, m = 3, 6  # input bits, random bits (u: 3 bits, v: 3 bits)
D = lambda x: sum(x) % 2 == 1
H = [(1, 0, 1), (0, 1, 1)]
Hv0 = lambda v: all(sum(a * b for a, b in zip(row, v)) % 2 == 0 for row in H)
B = lambda r: (sum(r[:3]) % 2) ^ int(Hv0(r[3:]))
V = {
    "V_B": lambda x, r: D(x) and B(r) == 1,
    "V_bit": lambda x, r: D(x) and r[0] == 1,
    "V_0": lambda x, r: D(x),
}
X = list(itertools.product((0, 1), repeat=n_in))
R = list(itertools.product((0, 1), repeat=m))

def lang(v): return tuple(any(v(x, r) for r in R) for x in X)
def acc(v, x): return sum(1 for r in R if v(x, r))
def min_pos_cert(v, x):
    """smallest number of fixed coords of a subcube of accepting tapes (exhaustive)."""
    best = None
    for k in range(m + 1):
        for S in itertools.combinations(range(m), k):
            for vals in itertools.product((0, 1), repeat=k):
                if all(v(x, r) for r in R if all(r[i] == b for i, b in zip(S, vals))):
                    if any(all(r[i] == b for i, b in zip(S, vals)) for r in R):
                        return k
    return None
def anf_degree(v, x):
    f = {r: int(bool(v(x, r))) for r in R}
    deg = 0
    for r in R:  # Moebius transform
        c = sum(f[s] for s in R if all(si <= ri for si, ri in zip(s, r))) % 2
        if c: deg = max(deg, sum(r))
    return deg

x_yes = next(x for x in X if D(x))
rep = {}
for name, v in V.items():
    rep[name] = dict(language=lang(v), yes_acc=acc(v, x_yes) / len(R),
                     min_positive_cert=min_pos_cert(v, x_yes),
                     anf_degree=anf_degree(v, x_yes))
langs = {tuple(r["language"]) for r in rep.values()}
assert len(langs) == 1, "languages must coincide"
invariants = {k: len({json.dumps(rep[n][k]) for n in rep}) == 1
              for k in ("yes_acc", "min_positive_cert", "anf_degree")}
out = {"report": {n: {k: v for k, v in r.items() if k != "language"} for n, r in rep.items()},
       "language_invariant_flags": invariants}
print(json.dumps(out, indent=1))
assert not any(invariants.values()), "expected every selected-verifier invariant to vary"
print("OK: same language, all three invariants vary across equivalent verifiers")
