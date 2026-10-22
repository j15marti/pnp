"""CONE-GAP79 experiment: exact static cone vs union of dynamic probes.
Psi_F = OR_z V(F,z); V adaptive depth-2 probe tree per witness z (k witness bits).
Exact cone = essential variables of F -> Psi_F (brute force over all 2^N sources).
Chunked by (N,k) and seed; each call < 30s."""
import random, json, sys, itertools
def run(N, k, seeds, mode):
    out = []
    for s in range(seeds):
        r = random.Random(1000*N + 10*k + s)
        # per witness: root address a, two child addresses b0,b1, leaf truth table over (F_a,F_b)
        V = []
        for z in range(2**k):
            a = r.randrange(N); b = (r.randrange(N), r.randrange(N))
            if mode == "sparse":   # accept only on a rare pattern
                leaf = {(0,0):0,(0,1):0,(1,0):0,(1,1):r.random()<0.5}
                tt = {(x,y): leaf[(x,y)] for x in (0,1) for y in (0,1)}
            else:
                tt = {(x,y): r.random()<0.5 for x in (0,1) for y in (0,1)}
            V.append((a,b,tt))
        union = set()
        for a,b,_ in V: union |= {a, b[0], b[1]}
        def psi(F):
            for a,b,tt in V:
                if tt[(F[a], F[b[F[a]]])]: return 1
            return 0
        tab = [psi([(m>>i)&1 for i in range(N)]) for m in range(2**N)]
        ess = [i for i in range(N) if any(tab[m] != tab[m^(1<<i)] for m in range(2**N))]
        out.append((len(union), len(ess), max(len({a,b[0],b[1]}) for a,b,_ in V) and 3))
    return out
if __name__ == "__main__":
    res = {}
    for mode in ("dense","sparse"):
        for N in (6,8,10,12):
            for k in (1,2,3):
                o = run(N,k,40,mode)
                gaps = [u-e for u,e,_ in o]
                res[f"{mode}_N{N}_k{k}"] = {"mean_union":sum(u for u,_,_ in o)/len(o),"mean_cone":sum(e for _,e,_ in o)/len(o),"max_gap":max(gaps),"frac_gap_pos":sum(g>0 for g in gaps)/len(o),"probes_per_witness":3}
    json.dump(res, open(sys.argv[1],"w"), indent=1); print(json.dumps(res)[:3000])
