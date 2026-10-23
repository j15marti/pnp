"""SAT-based exact B2 circuit size (Knuth/Kojevnikov-style encoding). Usage: sat_exact_synthesis.py FAMILY PARAM R [timeout_s]
Decides: does an r-gate fan-in-2 B2 circuit compute f (up to output negation)? Prints SAT/UNSAT/TIMEOUT. Run with /usr/bin/python3."""
import sys, itertools, threading
from pysat.solvers import Glucose4
def tt_family(fam, p):
    if fam == "triangle":
        edges = list(itertools.combinations(range(p), 2)); idx = {e: i for i, e in enumerate(edges)}
        n = len(edges); tris = [[idx[(a,b)], idx[(a,c)], idx[(b,c)]] for a,b,c in itertools.combinations(range(p),3)]
        f = lambda x: any(all((x>>i)&1 for i in t) for t in tris)
    elif fam == "maj": n = p; f = lambda x: bin(x).count("1")*2 > n
    elif fam == "parity": n = p; f = lambda x: bin(x).count("1") & 1
    elif fam == "threshold2": n = p; f = lambda x: bin(x).count("1") >= 2
    else: raise SystemExit("family")
    return n, [1 if f(x) else 0 for x in range(1 << n)]
def solve(n, tt, r, timeout):
    if tt[0]: tt = [1 - v for v in tt]          # normalise: output negation free
    rows = range(1, 1 << n); cnt = [0]
    def new(): cnt[0] += 1; return cnt[0]
    N = n + r; x = {(i, t): new() for i in range(n, N) for t in rows}
    inp = lambda i, t: (t >> i) & 1
    s = {(i, j, k): new() for i in range(n, N) for k in range(N) for j in range(k) if k < i}
    op = {(i, a, b): new() for i in range(n, N) for a in (0, 1) for b in (0, 1) if (a, b) != (0, 0)}
    cl = []
    for i in range(n, N):
        sel = [v for (ii, j, k), v in s.items() if ii == i]
        cl.append(sel)
        for u, v in itertools.combinations(sel, 2): cl.append([-u, -v])
        for (ii, j, k), sv in s.items():
            if ii != i: continue
            for t in rows:
                for a in (0, 1):
                    for b in (0, 1):
                        lits = [-sv]
                        for idx, val in ((j, a), (k, b)):
                            if idx < n: 
                                if inp(idx, t) != val: break
                            else: lits.append(-x[(idx, t)] if val else x[(idx, t)])
                        else:
                            if (a, b) == (0, 0): lits.append(-x[(i, t)]); cl.append(lits)
                            else:
                                cl.append(lits + [-op[(i, a, b)], x[(i, t)]])
                                cl.append(lits + [op[(i, a, b)], -x[(i, t)]])
    for t in rows: cl.append([x[(N-1, t)] if tt[t] else -x[(N-1, t)]])
    for i in range(n, N):   # every non-output gate must be used (symmetry/size pruning)
        if i < N - 1: cl.append([v for (ii, j, k), v in s.items() if j == i or k == i])
    sol = Glucose4(bootstrap_with=cl); res = [None]
    timer = threading.Timer(timeout, lambda: sol.interrupt()); timer.start()
    out = sol.solve_limited(expect_interrupt=True); timer.cancel()
    return {True: "SAT", False: "UNSAT", None: "TIMEOUT"}[out]
if __name__ == "__main__":
    fam, p, r = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); to = float(sys.argv[4]) if len(sys.argv) > 4 else 25
    n, tt = tt_family(fam, p); print(fam, p, "n=%d r=%d" % (n, r), solve(n, tt, r, to), flush=True)
