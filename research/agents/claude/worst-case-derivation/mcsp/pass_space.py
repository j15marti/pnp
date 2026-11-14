#!/usr/bin/env python3
"""WCD-PASS-0001. Two computations.

(1) MC-T1. An r-pass machine with S bits of memory that reads the table left to right gives, at any
    cut, a two-party protocol with 2r-1 messages of S bits. So (2r-1)*S >= D(cut) >= log2 rank(M_cut),
    where M_cut[prefix][suffix] = 1 iff prefix+suffix is an easy table. Rank is computed mod a large
    prime, which never exceeds the rational rank, so the bound is valid. One-pass classes for comparison.
(2) 2 -> 3. Count the ternary Boolean operations that preserve every clause of width 2, and of width 3
    (polymorphisms). A non-projection that preserves all constraints is what makes a constraint
    language tractable (Schaefer; Bulatov; Zhuk).
Pure Python, single stage, a few seconds. JSON on stdout.
"""
import itertools, json, math, sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcsp_bridge import by_size, nerode
T0 = time.time(); P = (1 << 61) - 1

def rank_mod(rows):
    rows = [r[:] for r in rows]; rk = 0; ncol = len(rows[0])
    for c in range(ncol):
        piv = next((i for i in range(rk, len(rows)) if rows[i][c] % P), None)
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]
        inv = pow(rows[rk][c], P - 2, P); rows[rk] = [(v * inv) % P for v in rows[rk]]
        for i in range(len(rows)):
            if i != rk and rows[i][c] % P:
                f = rows[i][c]; rows[i] = [(a - f * b) % P for a, b in zip(rows[i], rows[rk])]
        rk += 1
        if rk == len(rows): break
    return rk

def cut_table(N, easy, cuts):
    out = {}
    ner = nerode(N, easy)
    for t in cuts:
        R, C = 1 << t, 1 << (N - t)
        M = [[1 if (p | (q << t)) in easy else 0 for q in range(C)] for p in range(R)]
        if R > C: M = [list(col) for col in zip(*M)]
        rk = rank_mod(M)
        out[t] = {"rank": rk, "two_way_bits_lower_bound": round(math.log2(rk), 2),
                  "one_pass_classes": ner[t], "one_pass_bits_lower_bound": round(math.log2(ner[t]), 2)}
    return out

def polymorphisms(width):
    """ternary operations g:{0,1}^3->{0,1} preserving every clause of the given width"""
    rels = []
    for signs in itertools.product((0, 1), repeat=width):
        rels.append([a for a in itertools.product((0, 1), repeat=width) if any(a[i] == signs[i] for i in range(width))])
    keep = []
    for g in range(256):
        op = lambda a, b, c: (g >> (a | (b << 1) | (c << 2))) & 1
        ok = True
        for rel in rels:
            rs = set(rel)
            for t1 in rel:
                for t2 in rel:
                    for t3 in rel:
                        if tuple(op(t1[i], t2[i], t3[i]) for i in range(width)) not in rs: ok = False; break
                    if not ok: break
                if not ok: break
            if not ok: break
        if ok: keep.append(g)
    proj = {0xAA, 0xCC, 0xF0}      # the three projections
    maj = 0xE8
    return {"count": len(keep), "non_projections": len([g for g in keep if g not in proj]),
            "majority_preserves": maj in keep}

def main():
    out = {"id": "WCD-PASS-0001"}
    s3 = by_size(3, 6); easy3 = {t for t, v in s3.items() if v <= 4}
    out["k3_threshold4"] = cut_table(8, easy3, range(2, 7))
    easy4 = set(by_size(4, 5))
    out["k4_threshold5"] = cut_table(16, easy4, range(4, 13))
    best = max(v["two_way_bits_lower_bound"] for v in out["k4_threshold5"].values())
    out["k4_tradeoff"] = {"max_two_way_bits": best,
                          "min_S_bits_by_passes": {str(r): math.ceil(best / (2 * r - 1)) for r in (1, 2, 3, 4)}}
    out["polymorphisms_ternary"] = {"clauses_width_2": polymorphisms(2), "clauses_width_3": polymorphisms(3)}
    out["seconds"] = round(time.time() - T0, 2)
    json.dump(out, sys.stdout, indent=1, sort_keys=True); print()
if __name__ == "__main__": main()
