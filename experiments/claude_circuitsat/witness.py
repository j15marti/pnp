"""Print one fully wire-sensitive UNSAT witness for (n,g). Re-implements the evaluator in pure python (no numpy)."""
import sys, itertools
n, g = int(sys.argv[1]), int(sys.argv[2])
full = (1 << (1 << n)) - 1
base = [sum(1 << x for x in range(1 << n) if (x >> j) & 1) for j in range(n)]
radix = [2*(n+i) for i in range(g) for _ in (0, 1)]
def sat(enc):
    tt = list(base)
    for i in range(g):
        v = []
        for w in (0, 1):
            d = enc[2*i+w]; t = tt[d >> 1]
            v.append(full ^ t if d & 1 else t)
        tt.append(v[0] & v[1])
    return tt[-1] != 0
for enc in itertools.product(*[range(r) for r in radix]):
    if sat(enc): continue
    ok = True
    for a in range(2*g):
        if not any(sat(enc[:a]+(v,)+enc[a+1:]) for v in range(radix[a]) if v != enc[a]):
            ok = False; break
    if ok:
        names = [f"x{j}" for j in range(n)] + [f"g{i}" for i in range(g)]
        out = []
        for i in range(g):
            fan = [("~" if enc[2*i+w] & 1 else "") + names[enc[2*i+w] >> 1] for w in (0, 1)]
            out.append(f"g{i} = {fan[0]} & {fan[1]}")
        print("; ".join(out)); break
