"""ClaudeCircuitSAT ladder: exact deterministic wire-query complexity of CIRCUIT-SAT
over the family F(n,g): g AND-gates (fan-in 2, topologically ordered), each input slot
('wire') names a source in {x_i, not x_i} u {earlier gates}; output = last gate.
A query reveals the source of one wire. D(n,g)=min over adaptive strategies of the
worst-case #queries to decide satisfiability. Exhaustive minimax; stdlib only."""
import itertools, json, sys, time
from functools import lru_cache

def run(n, g, mode):
    lits = 2*n
    # slot j in gate k has options: lits (+ k earlier gates if mode=='dag')
    opts = []
    for k in range(g):
        o = lits + (k if mode == 'dag' else 0)
        opts += [o, o]
    S = len(opts)
    def sat(c):
        for xs in itertools.product((0, 1), repeat=n):
            val = []
            for k in range(g):
                ins = []
                for j in (0, 1):
                    s = c[2*k+j]
                    ins.append((xs[s//2] ^ (s % 2)) if s < lits else val[s-lits])
                val.append(ins[0] & ins[1])
            if val[-1]:
                return 1
        return 0
    circs = list(itertools.product(*[range(o) for o in opts]))
    ans = {c: sat(c) for c in circs}
    nsat = sum(ans.values())
    @lru_cache(None)
    def D(partial):
        # partial: tuple with -1 for unknown
        cs = [c for c in circs if all(p < 0 or p == v for p, v in zip(partial, c))]
        a = {ans[c] for c in cs}
        if len(a) == 1:
            return 0
        best = 10**9
        for s in range(S):
            if partial[s] >= 0: continue
            w = 0
            for v in range(opts[s]):
                p = partial[:s] + (v,) + partial[s+1:]
                w = max(w, D(p))
                if w + 1 >= best: break
            best = min(best, 1 + w)
        return best
    d = D(tuple([-1]*S))
    return dict(n=n, g=g, mode=mode, wires=S, family=len(circs), sat_frac=nsat/len(circs), D=d)

if __name__ == '__main__':
    out = []
    for (n, g, mode) in [(1,1,'dag'),(2,1,'dag'),(3,1,'dag'),(2,2,'tree'),(2,2,'dag'),(1,2,'dag'),(3,2,'tree'),(1,3,'dag')]:
        t = time.time(); r = run(n, g, mode); r['sec'] = round(time.time()-t, 2)
        print(r, flush=True); out.append(r)
        if time.time() - t > 20: break
    json.dump(out, open('wire_query_ladder_results.json', 'w'), indent=1)
