"""Exhaustive check of the wire-read adversary family (ClaudeCircuitSAT.tex, Thm 2)
and the unique-witness black-box family (Thm 3). Runs in well under 30 s."""
import itertools

def build(m, bad):
    # gates a_i = AND(x1, y_i); y_i = NOT x1 if i==bad else x1; output AND of all a_i
    return [(i == bad) for i in range(m)]

def sat(flags):
    for x in (0, 1):
        if all((x and ((not x) if f else x)) for f in flags):
            return True
    return False

for m in range(1, 9):
    base = build(m, None)
    assert sat(base)
    for b in range(m):
        inst = build(m, b)
        assert not sat(inst)
        diff = [i for i in range(m) if inst[i] != base[i]]
        assert diff == [b]          # one wire (y_b) differs
print("Thm 2 family verified for m<=8")

# Thm 3: unique-witness circuits AND of literals fixing a in {0,1}^n; any deterministic
# black-box algorithm that stops before querying all 2^n points misses some witness.
for n in range(1, 5):
    pts = list(itertools.product((0, 1), repeat=n))
    # zero-circuit answers 0 on every query; instance a answers 1 only at a
    assert all(sum(1 for q in pts if q == a) == 1 for a in pts)
print("Thm 3 family verified for n<=4")

# exact minimum gate count (AND/OR, free NOT) of all 3-var functions that are
# satisfiable with exactly one model: ledger step n -> min #wires
def min_gates(n):
    N = 1 << n
    mask = (1 << N) - 1
    lits = []
    for i in range(n):
        t = 0
        for p in range(N):
            if (p >> i) & 1: t |= 1 << p
        lits += [t, mask ^ t]
    best = {t: 0 for t in lits}
    layer = set(lits)
    g = 0
    while len(best) < 2 ** N - 2 and g < 8:
        g += 1
        new = {}
        known = list(best)
        for a in known:
            for b in known:
                for r in (a & b, a | b):
                    for rr in (r, mask ^ r):
                        if rr not in best and rr not in new: new[rr] = g
        best.update(new)
        if not new: break
    return best
for n in (2, 3):
    b = min_gates(n)
    uniq = [t for t in b if bin(t).count("1") == 1]
    print(n, "unique-model funcs:", len(uniq), "max min-gates:", max(b[t] for t in uniq),
          "min wires (2/gate):", 2 * max(b[t] for t in uniq))
