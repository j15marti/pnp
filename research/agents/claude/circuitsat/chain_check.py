"""Verify T2 family: C0 unsat, each rewired C_i (i=2..m) satisfiable. g1=x1&~x1, g_i=g_{i-1}&x_i."""
import itertools, json
def sat(m, rew=None):
    for x in itertools.product([0,1], repeat=m):
        g = x[0] & (1-x[0])
        for i in range(2, m+1):
            a = x[i-1] if rew == i else g
            g = a & x[i-1]
        if g: return True
    return False
res = {m: (sat(m), [sat(m,i) for i in range(2,m+1)]) for m in range(2,11)}
ok = all((not a) and all(b) for a,b in res.values())
print(ok); json.dump(dict(all_ok=ok, ms=list(res)), open("chain_check_results.json","w"))
