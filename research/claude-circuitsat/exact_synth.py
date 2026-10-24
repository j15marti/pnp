"""Exact B2 (all 2-input gates, fan-in 2, fan-out unbounded) circuit size via SAT.
Kojevnikov-Kulikov-Yaroslavtsev style encoding. Each call is time-capped (~25s)."""
import itertools, sys, json, time, threading
from pysat.solvers import Glucose4

def synth(n, tt, r, limit=25):
    """tt: list of 2^n bits (single output). Is there a B2 circuit with r gates?"""
    N = 1 << n
    cnt = [0]
    def nv(): cnt[0] += 1; return cnt[0]
    # x[i][t]: value of node i (0..n-1 inputs, n..n+r-1 gates) on row t
    val = [[None]*N for _ in range(n+r)]
    cl = []
    for i in range(n):
        for t in range(N): val[i][t] = ('c', (t >> i) & 1)
    for g in range(r):
        for t in range(N): val[n+g][t] = ('v', nv())
    def lit(a, neg=False):
        k, v = a
        return (k, v ^ 1 if neg and k == 'c' else v, ) if k == 'c' else ('v', -v if neg else v)
    # selection s[g][j][k], j<k<n+g
    sel = {}
    for g in range(r):
        opts = []
        for j in range(n+g):
            for k in range(j+1, n+g):
                sel[g, j, k] = nv(); opts.append(sel[g, j, k])
        cl.append(opts)
        for a, b in itertools.combinations(opts, 2): cl.append([-a, -b])
    # function bits f[g][(p,q)] with (0,0)->? gate normal-free: use all 4 bits
    f = {(g, p, q): nv() for g in range(r) for p in (0,1) for q in (0,1)}
    for g in range(r):
        for (j, k) in [(j,k) for j in range(n+g) for k in range(j+1, n+g)]:
            s = sel[g, j, k]
            for t in range(N):
                for p in (0,1):
                    for q in (0,1):
                        for o in (0,1):
                            c = [-s]
                            ok = True
                            for (node, bit) in ((j,p),(k,q),(n+g,o)):
                                kd, v = val[node][t]
                                if kd == 'c':
                                    if v == bit: pass      # literal false -> drop (clause term false)
                                    else: ok = False; break  # term true -> clause satisfied
                                else:
                                    c.append(-v if bit else v)
                            if not ok: continue
                            c.append(f[g,p,q] if o else -f[g,p,q])
                            cl.append(c)
    # output = last gate (wlog, single output; gates not feeding output wasteful but harmless)
    for t in range(N):
        kd, v = val[n+r-1][t]
        cl.append([v if tt[t] else -v])
    # every gate (except last) used
    for g in range(r-1):
        users = [sel[h,j,k] for h in range(g+1, r) for j in range(n+h) for k in range(j+1,n+h) if n+g in (j,k)]
        cl.append(users)
    s = Glucose4(bootstrap_with=cl)
    res = [None]
    def run(): res[0] = s.solve_limited(expect_interrupt=True)
    th = threading.Thread(target=run); th.start(); th.join(limit)
    if th.is_alive():
        s.interrupt(); th.join(); return None
    return res[0]

def size(n, tt, maxr=12, limit=25):
    for r in range(1, maxr+1):
        a = synth(n, tt, r, limit)
        if a is None: return ('>=', r)
        if a: return ('=', r)
    return ('>', maxr)

def tt_of(n, fn): return [int(fn([(t>>i)&1 for i in range(n)])) for t in range(1<<n)]
if __name__ == '__main__':
    fams = {
      'AND': lambda x: all(x), 'XOR': lambda x: sum(x)%2==1,
      'MAJ': lambda x: 2*sum(x) > len(x), 'THR2': lambda x: sum(x)>=2,
      'EXACT1': lambda x: sum(x)==1, 'MOD3==0': lambda x: sum(x)%3==0,
    }
    nmax = int(sys.argv[1]) if len(sys.argv)>1 else 4
    out = {}
    sel_f = sys.argv[2].split(',') if len(sys.argv)>2 else list(fams)
    for name, fn in [(k,v) for k,v in fams.items() if k in sel_f]:
        for n in range(2, nmax+1):
            t0=time.time(); r = size(n, tt_of(n, fn), maxr=10, limit=8)
            out[f'{name}_{n}'] = r; print(name, n, r, round(time.time()-t0,1), flush=True)
    json.dump(out, open(f'exact_synth_results_n{nmax}.json','w'), indent=1)
