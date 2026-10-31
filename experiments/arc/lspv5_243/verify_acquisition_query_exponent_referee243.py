#!/usr/bin/env python3
"""Independent verifier for REFEREE243.  Imports no producer code."""

from __future__ import annotations

import itertools
import json
import math
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RAW = ROOT / "results/raw/arc/2026-10-31_0748_LSPV5_ACQUISITION_QUERY_EXPONENT_REFEREE243_raw.json"
OUT = ROOT / "results/summaries/arc/2026-10-31_0748_LSPV5_ACQUISITION_QUERY_EXPONENT_REFEREE243_verification.json"


def edge_list(kind, q):
    if kind == "cycle":
        return [(i, (i + 1) % q) for i in range(q)]
    return [(i, j) for i in range(q) for j in range(i + 1, q)]


class Emitter:
    def __init__(self):
        self.v = 0
        self.cs = []

    def new(self):
        self.v += 1
        return self.v

    def c3(self, *c):
        assert len(c) == 3 and len({abs(x) for x in c}) == 3
        self.cs.append(tuple(c))

    def c2(self, a, b):
        p = self.new(); self.c3(a, b, p); self.c3(a, b, -p)

    def unit(self, a):
        u, v = self.new(), self.new()
        for su, sv in itertools.product((1, -1), repeat=2):
            self.c3(a, su * u, sv * v)

    def OR(self, z, a, b):
        self.c2(-a, z); self.c2(-b, z); self.c3(a, b, -z)

    def AND(self, z, a, b):
        self.c2(a, -z); self.c2(b, -z); self.c3(-a, -b, z)

    def text(self):
        return f"p cnf {self.v} {len(self.cs)}\n" + "".join("%d %d %d 0\n" % c for c in self.cs)


def source_text(kind, q, neg):
    e = Emitter(); x = [e.new() for _ in range(q)]
    for u, v in edge_list(kind, q):
        for _ in range(q + 1): e.c3(x[u], x[v], e.new())
    abc = [e.new(), e.new(), e.new()]
    if neg:
        for vals in itertools.product((0, 1), repeat=3):
            e.c3(*(z if val == 0 else -z for z, val in zip(abc, vals)))
    else: e.c3(*abc)
    return e.text(), e.cs, e.v


def vc_text(kind, q, t):
    e = Emitter(); ins = [e.new() for _ in range(q)]
    for u, v in edge_list(kind, q): e.c2(ins[u], ins[v])
    p = 1
    while p < q: p <<= 1
    w = ins[:]
    while len(w) < p:
        z = e.new(); e.unit(-z); w.append(z)
    comps = 0; k = 2
    while k <= p:
        j = k // 2
        while j:
            nw = w[:]
            used = set()
            for i in range(p):
                z = i ^ j
                if i in used or z in used: continue
                lo, hi = e.new(), e.new()
                e.AND(lo, w[i], w[z]); e.OR(hi, w[i], w[z])
                asc = (min(i, z) & k) == 0
                a, b = sorted((i, z))
                nw[a], nw[b] = (lo, hi) if asc else (hi, lo)
                used.add(i); used.add(z); comps += 1
            w = nw; j //= 2
        k *= 2
    if t < q: e.unit(-w[p - t - 1])
    return e.text(), {"variables": e.v, "clauses": len(e.cs), "comparators": comps, "padded_wires": p}


def tau(kind, q): return (q + 1) // 2 if kind == "cycle" else q - 1


def validate(data):
    checks = 0
    assert data["run_id"] == "ACQUISITION-QUERY-EXPONENT-REFEREE243"; checks += 1
    for row in data["graph_acquisition_rows"]:
        kind, q, t = row["kind"], row["q"], row["tau"]
        assert t == tau(kind, q); checks += 1
        sp, _, _ = source_text(kind, q, False)
        sn, _, _ = source_text(kind, q, True)
        yp, ym = vc_text(kind, q, t)
        np, nm = vc_text(kind, q, t - 1)
        assert len(sp) == row["source_sat_chars"]; checks += 1
        assert len(sn) == row["source_unsat_chars"]; checks += 1
        assert len(yp) == row["query_tau_chars"]; checks += 1
        assert len(np) == row["query_tau_minus_1_chars"]; checks += 1
        assert ym == row["query_tau_meta"]; checks += 1
        assert nm == row["query_tau_minus_1_meta"]; checks += 1
        N, M = max(len(sp), len(sn)), max(len(yp), len(np))
        assert N == row["source_N"] and M == row["query_M"]; checks += 1
        assert abs(math.log(M) / math.log(N) - row["finite_log_exponent"]) < 1e-14; checks += 1
        assert row["backdoor_size"] == t + 1; checks += 1

    for row in data["bent_degree_rows"]:
        r, d = row["r"], row["degree"]
        zero = 0
        for x in range(1 << r):
            for y in range(1 << r):
                f = ((x & y).bit_count() & 1)
                mon = 1
                for i in range(d): mon &= (y >> i) & 1
                zero += (f ^ mon) == 0
        expect = (1 << (2*r - 1)) + (1 << (r - 1))
        assert zero == row["zero_set_size"] == expect; checks += (1 << (2*r))
        assert row["walsh_abs"] == 1 << r; checks += 1
        assert row["linear_bias"] == f"1/{2**r+1}"; checks += 1
        assert row["nonlinear_gap"] == f"{(1 << (2*r))-expect}/{1 << (2*r)}"; checks += 1
        if r <= 4:
            pts = [(x, y) for x in range(1 << r) for y in range(1 << r)
                   if (((x & y).bit_count() & 1) ^ math.prod((y >> i) & 1 for i in range(d))) == 0]
            for u in range(1 << r):
                for v in range(1 << r):
                    if u == v == 0: continue
                    s = sum(1 if (((u & x).bit_count() + (v & y).bit_count()) & 1) == 0 else -1 for x, y in pts)
                    assert abs(s) * (2**r + 1) == len(pts)
                    checks += len(pts)

    controls = data["original_clause_controls"]
    assert controls["H7_unique_middle_SAT"]["models"] == [[1, 0, 1]]; checks += 1
    assert controls["H8_UNSAT"]["models"] == []; checks += 1
    assert controls["H7_unique_middle_SAT"]["pair_modes"] == 7 * 6 * 4; checks += 1
    assert controls["H8_UNSAT"]["pair_modes"] == 8 * 7 * 4; checks += 1

    def dpll(cnf):
        stats = {"states": 0, "literal_probes": 0}
        def go(a):
            stats["states"] += 1
            while True:
                forced = None; complete = True
                for clause in cnf:
                    live = []; ok = False
                    for lit in clause:
                        stats["literal_probes"] += 1
                        v = abs(lit)
                        if v not in a: live.append(lit)
                        elif a[v] == (lit > 0): ok = True; break
                    if ok: continue
                    complete = False
                    if not live: return False
                    if len(live) == 1: forced = live[0]; break
                if complete: return True
                if forced is None: break
                a[abs(forced)] = forced > 0
            v = next(v for v in (1, 2, 3) if v not in a)
            return go({**a, v: False}) or go({**a, v: True})
        yes = go({})
        return {"label": "SAT" if yes else "UNSAT", **stats}

    for key in ("H7_unique_middle_SAT", "H8_UNSAT"):
        assert dpll(controls[key]["clauses"]) == controls[key]["up_dpll"]
        checks += controls[key]["up_dpll"]["states"] + controls[key]["up_dpll"]["literal_probes"]
    return checks


def main():
    started = time.perf_counter()
    data = json.loads(RAW.read_text())
    checks = validate(data)
    corruptions = 0
    for mutation in ("run", "zero", "source"):
        clone = json.loads(json.dumps(data))
        if mutation == "run": clone["run_id"] = "bad"
        elif mutation == "zero": clone["bent_degree_rows"][0]["zero_set_size"] += 1
        else: clone["graph_acquisition_rows"][0]["source_N"] += 1
        try: validate(clone)
        except AssertionError: corruptions += 1
    assert corruptions == 3
    out = {"run_id": data["run_id"], "status": "PASS", "independent_check_units": checks,
           "corruptions_rejected": corruptions, "runtime_seconds": time.perf_counter()-started,
           "imports_producer": False}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True)+"\n")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__": main()
