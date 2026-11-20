"""TWOSATWIDTH1: density audit of the TWOSATDEC schedule and a finite growth
probe of the minimum certifying set size at density 6 (above the 3-SAT
upper bound 4.4898, so draws are UNSAT w.h.p.).

Same protocol as TWOSATDEC: uniform sample without replacement from the
lexicographic proper 3-clause list; a variable set R certifies iff every
assignment of R, after unit propagation, yields an empty clause or an
unsatisfiable width<=2 skeleton (width-3 survivors are not used).
COMPUTATIONAL only. Usage: python3 -I twosat_width_bridge.py
"""
import itertools, random, sys, time, json

def clause_list(q):
    out = []
    for tri in itertools.combinations(range(q), 3):
        for s in range(8):
            out.append(tuple((v, (s >> i) & 1) for i, v in enumerate(tri)))
    return out

def up(clauses, asg):
    asg = dict(asg)
    changed = True
    while changed:
        changed = False
        for c in clauses:
            free, sat = [], False
            for v, p in c:
                if v in asg:
                    if asg[v] == p: sat = True; break
                else: free.append((v, p))
            if sat: continue
            if not free: return None
            if len(free) == 1:
                asg[free[0][0]] = free[0][1]; changed = True
    return asg

def two_sat_unsat(clauses, asg, q):
    # implication graph on residual width<=2 clauses; literal id 2v+p
    adj = {}
    for c in clauses:
        free, sat = [], False
        for v, p in c:
            if v in asg:
                if asg[v] == p: sat = True; break
            else: free.append((v, p))
        if sat or len(free) != 2: continue
        (a, pa), (b, pb) = free
        adj.setdefault(2*a + (1-pa), []).append(2*b + pb)
        adj.setdefault(2*b + (1-pb), []).append(2*a + pa)
    def reach(s, t):
        seen, st = {s}, [s]
        while st:
            x = st.pop()
            if x == t: return True
            for y in adj.get(x, ()):
                if y not in seen: seen.add(y); st.append(y)
        return False
    for v in range(q):
        if v in asg: continue
        if reach(2*v+1, 2*v) and reach(2*v, 2*v+1): return True
    return False

def certifies(clauses, R, q):
    for bits in itertools.product((0, 1), repeat=len(R)):
        a = up(clauses, dict(zip(R, bits)))
        if a is None: continue
        if not two_sat_unsat(clauses, a, q): return False
    return True

def is_sat(clauses, q, asg=None):
    a = up(clauses, asg or {})
    if a is None: return False
    for v in range(q):
        if v not in a:
            for b in (1, 0):
                a2 = dict(a); a2[v] = b
                if is_sat(clauses, q, a2): return True
            return False
    return True

def main():
    sched = [(q, (7*q)//2, (7*q)//2 / q) for q in range(9, 103)]
    worst = max(r for _, _, r in sched)
    print(f"schedule t=floor(3.5q), q=9..102: max density {worst:.6f} (< 3.52: {worst < 3.52})")
    rng = random.Random(20261120)
    rows = []
    t0 = time.time()
    for q in (12, 16, 20, 24, 28, 32, 36, 40):
        L = clause_list(q); t = 6*q
        mins = []
        for _ in range(8):
            F = rng.sample(L, t)
            if is_sat(F, q): mins.append("SAT"); continue
            rmin = None
            for r in range(0, 6):
                if any(certifies(F, R, q) for R in itertools.combinations(range(q), r)):
                    rmin = r; break
            mins.append(rmin if rmin is not None else ">5")
        rows.append({"q": q, "t": t, "min_r": mins})
        print(q, t, mins, f"{time.time()-t0:.1f}s"); sys.stdout.flush()
    json.dump({"seed": 20261120, "density_max": worst, "rows": rows}, sys.stdout); print()

if __name__ == "__main__":
    main()
