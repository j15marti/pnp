#!/usr/bin/env python3
"""TMR-5/WR056 producer: explicit extended-resolution (RUP + definitional
extension) refutation of the bit pigeonhole principle BPHP^{n+1}_n, n = 2^k.

Revision: tmr5-bitphp-er-collapse056.v1   (deterministic; no randomness, no seed)

Construction (two stages, both written out explicitly as proof lines):
  Stage 1 (binary -> unary decoding).  For every pigeon i and hole h introduce
    y[i,h] <-> AND_b (x[i,b] == h_b).  Derive the unary axioms
      P_i     = OR_h y[i,h]              via 2^k - 2 prefix lemmas per pigeon,
      H_{i,i',h} = (-y[i,h] v -y[i',h])  directly by RUP from the BPHP clause.
  Stage 2 (Cook 1976).  From PHP^{h+1}_h on variables p, introduce
    q[i,j] <-> p[i,j] v (p[i,h-1] ^ p[h,j])   (i < h, j < h-1)
  and derive PHP^h_{h-1} on q with three RUP lemmas per hole clause; repeat
  down to h = 1 and derive the empty clause.

Every addition is intended to be a RUP clause with respect to the clause
database current at that point; the separate checker
experiments/tmr/tmr5_er_rup_checker056.py re-verifies everything independently.
"""
import json, sys, itertools

REV = "tmr5-bitphp-er-collapse056.v1"


def bphp(k):
    n = 1 << k
    m = n + 1
    x = lambda i, b: 1 + i * k + b
    clauses = []
    for i in range(m):
        for i2 in range(i + 1, m):
            for h in range(n):
                c = []
                for b in range(k):
                    hb = (h >> (k - 1 - b)) & 1
                    # literal true iff bit differs from h_b
                    c.append(x(i, b) if hb == 0 else -x(i, b))
                    c.append(x(i2, b) if hb == 0 else -x(i2, b))
                clauses.append(c)
    return n, m, m * k, clauses


def produce(k):
    n, m, nv, F = bphp(k)
    x = lambda i, b: 1 + i * k + b
    nxt = [nv + 1]

    def fresh():
        v = nxt[0]
        nxt[0] += 1
        return v

    steps = []
    E = lambda v, cls: steps.append({"t": "e", "v": v, "c": cls})
    A = lambda c: steps.append({"t": "a", "c": c})
    D = lambda c: steps.append({"t": "d", "c": c})

    # ---- Stage 1 ----
    def L(i, b, hb):  # literal true iff x[i,b] == hb
        return x(i, b) if hb == 1 else -x(i, b)

    y = {}
    for i in range(m):
        for h in range(n):
            v = fresh()
            y[i, h] = v
            bits = [(h >> (k - 1 - b)) & 1 for b in range(k)]
            cls = [[-v, L(i, b, bits[b])] for b in range(k)]
            cls.append([v] + [-L(i, b, bits[b]) for b in range(k)])
            E(v, cls)
    for i in range(m):
        derived = []
        for t in range(k - 1, -1, -1):
            for sig in range(1 << t):
                sbits = [(sig >> (t - 1 - b)) & 1 for b in range(t)]
                hs = [h for h in range(n) if (h >> (k - t)) == sig]
                c = [y[i, h] for h in hs] + [-L(i, b, sbits[b]) for b in range(t)]
                A(c)
                derived.append(c)
        for c in derived[:-1]:
            D(c)  # keep only P_i (the last, t = 0)
    for i in range(m):
        for i2 in range(i + 1, m):
            for h in range(n):
                A([-y[i, h], -y[i2, h]])
    for c in F:
        D(c)

    # ---- Stage 2: Cook's reduction ----
    p = y
    h = n
    while h > 1:
        q = {}
        for i in range(h):
            for j in range(h - 1):
                v = fresh()
                q[i, j] = v
                a, b2, c2 = p[i, j], p[i, h - 1], p[h, j]
                E(v, [[-v, a, b2], [-v, a, c2], [v, -a], [v, -b2, -c2]])
        for i in range(h):
            A([q[i, j] for j in range(h - 1)])
        for j in range(h - 1):
            for i in range(h):
                for i2 in range(i + 1, h):
                    la = [-q[i, j], -q[i2, j], -p[i, j]]
                    lb = [-q[i, j], -q[i2, j], -p[i2, j]]
                    A(la)
                    A(lb)
                    A([-q[i, j], -q[i2, j]])
                    D(la)
                    D(lb)
        # delete the old level's axioms (sound: deletion only weakens)
        for i in range(h + 1):
            D([p[i, j] for j in range(h)])
        for j in range(h):
            for i in range(h + 1):
                for i2 in range(i + 1, h + 1):
                    D([-p[i, j], -p[i2, j]])
        p = q
        h -= 1
    A([])
    return {"k": k, "n": n, "m": m, "nvars_F": nv, "F": F, "steps": steps,
            "nvars_total": nxt[0] - 1}


def stats(pr):
    s = pr["steps"]
    ext = [t for t in s if t["t"] == "e"]
    add = [t for t in s if t["t"] == "a"]
    dele = [t for t in s if t["t"] == "d"]
    ext_cl = sum(len(t["c"]) for t in ext)
    lits = sum(len(c) for t in ext for c in t["c"]) + sum(len(t["c"]) for t in add)
    return {"k": pr["k"], "holes_n": pr["n"], "pigeons_m": pr["m"],
            "F_vars": pr["nvars_F"], "F_clauses": len(pr["F"]),
            "F_literals": sum(len(c) for c in pr["F"]),
            "ext_vars": len(ext), "ext_clauses": ext_cl, "rup_lemmas": len(add),
            "deletions": len(dele), "proof_lines": ext_cl + len(add),
            "proof_literals": lits,
            "max_added_width": max(len(t["c"]) for t in add)}


if __name__ == "__main__":
    k = int(sys.argv[1])
    out = sys.argv[2]
    pr = produce(k)
    pr["revision"] = REV
    pr["stats"] = stats(pr)
    with open(out, "w") as f:
        json.dump(pr, f)
    print(json.dumps(pr["stats"]))
