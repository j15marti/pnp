"""Verify the Omega(s) gate-type-probe adversary family: U_s unsat, each single gate-type flip AND->OR satisfiable."""
import json
def build(s, flip=None):
    # inputs: x. wires: nx = NOT x ; g0 = AND(x,nx); g_i = AND(g_{i-1}, x), i=1..s ; out = g_s
    def ev(x):
        nx = 1-x; g = x & nx
        for i in range(1,s+1):
            g = (g | x) if flip == i else (g & x)
        return g
    return ev
res = {}
for s in range(1,41):
    unsat = all(build(s)(x)==0 for x in (0,1))
    allflip = all(any(build(s,i)(x) for x in (0,1)) for i in range(1,s+1))
    res[s] = unsat and allflip
print(json.dumps({"all_ok": all(res.values()), "s_range":[1,40]}))
