#!/usr/bin/env python3
"""WCD-DEPTH-0001: depth-tracking version of the R^- -> Res(+) simulation.

Checks exhaustively that one R^- node adds at most 3 to Res(+) depth
(depth = number of resolution steps on a path; semantic weakening adds 0,
as in ECCC TR26-018), then tabulates the resulting depth-capped bounds.
Single stage, pure Python, well under 30 s. JSON on stdout.
"""
import itertools, json, math, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resxor"))
import rminus_resxor_transfer as B

T0 = time.time()

class DChecker(B.Checker):
    def __init__(self, n, axioms):
        super().__init__(n, axioms); self.depth = [0] * len(axioms)
    def weaken(self, i, D):
        k = super().weaken(i, D); self.depth.append(self.depth[i]); return k
    def resolve(self, i, j, f):
        k = super().resolve(i, j, f); self.depth.append(1 + max(self.depth[i], self.depth[j])); return k

def xor_depth(nmax=4):
    worst = 0; cnt = 0
    for n in range(1, nmax + 1):
        for f in range(1, 1 << n):
            for g in range(1, 1 << n):
                if f == g: continue
                for a in (0, 1):
                    for b in (0, 1):
                        c = DChecker(n, [[(f, a)], [(g, b)]])
                        i = c.weaken(1, [(f, a ^ 1), (f ^ g, a ^ b)])
                        k = c.resolve(0, i, f) if a == 0 else c.resolve(i, 0, f)
                        assert c.lines[k] == frozenset({(f ^ g, a ^ b)})
                        worst = max(worst, c.depth[k]); cnt += 1
    return {"instances": cnt, "max_added_depth": worst}

def local_depth():
    """Same decision-tree derivations as the size script, with depth tracked."""
    n = 3; worst = 0; cnt = 0
    for ftt in range(1 << 8):
        S = B.maxterms(n, ftt)
        if not S: continue
        targets = []
        for signs in itertools.product((None, 0, 1), repeat=n):
            T = [B.lit(v, s) for v, s in enumerate(signs) if s is not None]
            targets.append((T, [v for v, s in enumerate(signs) if s is not None]))
        for m in range(1, 8):
            for b in (0, 1): targets.append(([(m, b)], []))
        for T, tv in targets:
            ttT = B.tt_line(n, T)
            if ftt & ~ttT & B.full(n): continue
            c = DChecker(n, S); U = [v for v in range(n) if v not in tv]
            def rec(rho):
                goal = list(T) + [B.lit(v, 1 - val) for v, val in rho.items()]
                if len(rho) == len(U):
                    gt = B.tt_line(n, goal)
                    for idx in range(c.ax):
                        if B.tt_line(n, c.lines[idx]) & ~gt & B.full(n) == 0:
                            return idx if c.lines[idx] == frozenset(goal) else c.weaken(idx, goal)
                    raise AssertionError
                v = U[len(rho)]
                return c.resolve(rec({**rho, v: 1}), rec({**rho, v: 0}), 1 << v)
            k = rec({})
            assert c.lines[k] == frozenset(T)
            worst = max(worst, c.depth[k]); cnt += 1
    return {"derivations": cnt, "max_added_depth": worst}

def main():
    out = {"id": "WCD-DEPTH-0001"}
    out["xor"] = xor_depth(); out["local"] = local_depth()
    out["depth_factor"] = max(1, out["xor"]["max_added_depth"], out["local"]["max_added_depth"])
    # Shape of the capped bound log2 S >= c * w^2 / d (TR26-018 Cor 1.3, constant c not explicit):
    # exponent of n in log2(size) for w = Theta(n) and cap d = n^delta.
    out["exponent_of_n_in_log_size"] = {f"d=n^{d}": round(2 - d, 2) for d in (1.0, 1.25, 1.5, 1.75, 1.9, 2.0)}
    # Polynomial depth charges collapse: D <= S, so S * D^k <= S^(k+1).
    out["poly_charge_collapse"] = "S <= S*D^k <= S^(k+1) because D <= S"
    # Product-charge bound: min of S*D subject to D >= c*w^2/log2 S and S >= w(w+1)/2 (c set to 1 for shape only).
    tab = {}
    for w in (10**2, 10**3, 10**4):
        S0 = w * (w + 1) // 2
        tab[str(w)] = {"S_min": S0, "S_times_D_at_S_min_c1": int(S0 * w * w / math.log2(S0))}
    out["product_charge_shape_c1"] = tab
    out["seconds"] = round(time.time() - T0, 2)
    json.dump(out, sys.stdout, indent=1, sort_keys=True); print()

if __name__ == "__main__":
    main()
