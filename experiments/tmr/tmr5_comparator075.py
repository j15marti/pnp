#!/usr/bin/env python3
"""TMR-5/036 COMPARATOR075: explicit physical transition-table comparator for
TMR-4/040 ENDMARKER074, fused-halt reachability, and convention-dependence attack.

Encoder is a line-by-line port of experiments/tmr/tmr3_lastsat073.js (prism,
block, build, encode, decode). The machine simulator is a genuine one-input-head
deterministic transition table over the tape  LEFT_END x_0 ... x_{N-1} RIGHT_END,
scan-before-move, unit cost per transition.  The fallback after a mismatch is a
total correct reference decider (strict parser + DPLL); its cost is NOT modelled
physically and is reported only as a label (ABSTRACT).

Chunking: run one m per invocation with  --m M  (each finishes well under 30 s);
--all runs m=3..12 sequentially and writes the combined JSON.
"""
import json, math, sys, time

LEFT, RIGHT = "<", ">"


# ---------- exact port of TMR-3/039 encoder ----------
def prism(m):
    es, seen, vs = [], set(), [[] for _ in range(2 * m)]
    def add(a, b):
        x, y = min(a, b), max(a, b)
        if (x, y) not in seen:
            seen.add((x, y)); es.append((x, y))
    for row in range(2):
        for i in range(m):
            add(row * m + i, row * m + (i + 1) % m)
    for i in range(m):
        add(i, m + i)
    for i, (u, v) in enumerate(es):
        vs[u].append(i + 1); vs[v].append(i + 1)
    for v in vs:
        v.sort()
    assert len(es) == 3 * m and all(len(v) == 3 for v in vs)
    return es, vs


def block(ids, parity):
    pats = [i for i in range(8) if (((i >> 2) & 1) ^ ((i >> 1) & 1) ^ (i & 1)) != parity]
    if parity:
        pats.sort(key=lambda a: ((1 if a == 0 else 0), a))
    return [[(-v if (i >> (2 - k)) & 1 else v) for k, v in enumerate(ids)] for i in pats]


def build(m):
    es, vs = prism(m)
    f0 = []
    for i, ids in enumerate(vs):
        f0.extend(block(ids, 1 if i == 2 * m - 1 else 0))
    f1 = [r[:] for r in f0]
    f1[-1][2] *= -1
    assert len(f0) == 8 * m and all(v > 0 for v in f0[-1])
    return f0, f1


def encode(cs, b):
    s = "1" * b + "0" + "1" * len(cs) + "0"
    for row in cs:
        for lit in row:
            v = abs(lit)
            assert 1 <= v < 2 ** b
            s += format(v, "0%db" % b) + ("1" if lit < 0 else "0")
    return s


def decode(s):
    """Strict total parser: returns list of clauses or None (malformed => NO)."""
    if not s or any(c not in "01" for c in s):
        return None
    b = s.find("0")
    if b < 1:
        return None
    j = s.find("0", b + 1)
    if j <= b + 1:
        return None
    M = j - b - 1
    start = j + 1
    if len(s) - start != 3 * M * (b + 1):
        return None
    p, cs = start, []
    for _ in range(M):
        row = []
        for _k in range(3):
            v = int(s[p:p + b], 2)
            neg = s[p + b] == "1"
            p += b + 1
            if v == 0:
                return None
            row.append(-v if neg else v)
        if len({abs(x) for x in row}) != 3:
            return None
        cs.append(row)
    return cs


def dpll(cs):
    """Independent complete DPLL with unit propagation; returns True iff SAT."""
    def simplify(cls, lit):
        out = []
        for c in cls:
            if lit in c:
                continue
            if -lit in c:
                c = [x for x in c if x != -lit]
                if not c:
                    return None
            out.append(c)
        return out
    def rec(cls):
        while True:
            if cls is None:
                return False
            if not cls:
                return True
            unit = next((c[0] for c in cls if len(c) == 1), None)
            if unit is None:
                break
            cls = simplify(cls, unit)
        lit = cls[0][0]
        return rec(simplify(cls, lit)) or rec(simplify(cls, -lit))
    return rec([list(c) for c in cs])


def reference(s):
    cs = decode(s)
    return False if cs is None else dpll(cs)


# ---------- physical transition-table machine ----------
class Comparator:
    """One fixed finite deterministic program A_m (for one fixed m).
    States: ('C',i) compare cell i against hardcoded target; ('C',N) expects RIGHT;
    'REW' rewinds to LEFT; 'FB' enters total fallback.  Halting is a transition
    (it consumes the scan of the current cell), exactly TMR-4/040's convention.
    promise=True gives the promise-convention variant A'_m that accepts on the
    scan of the LAST DATA BIT (never inspects the endmarker on the match path)."""

    def __init__(self, target, promise=False):
        self.t, self.N, self.promise = target, len(target), promise

    def delta(self, q, sym):
        """Returns (new_state, move) or ('HALT', accept_bool) -- explicit table."""
        N, t = self.N, self.t
        if q[0] == "C":
            i = q[1]
            if i < N:
                if sym == t[i]:
                    if self.promise and i == N - 1:
                        return ("HALT", True)       # fused last-bit scan + accept
                    return (("C", i + 1), +1)
                return ("REW", -1)
            # i == N : expect right endmarker
            if sym == RIGHT:
                return ("HALT", True)               # fused endmarker scan + accept
            return ("REW", -1)
        if q == "REW":
            if sym == LEFT:
                return ("FB", +1)
            return ("REW", -1)
        raise ValueError(q)

    def table_size(self):
        return (self.N + 1) * 3 + 3  # (states x symbols {0,1,RIGHT}) + REW rows

    def run(self, x):
        tape = LEFT + x + RIGHT          # cell k of x is tape index k+1
        pos, q, T = 1, ("C", 0), 0
        r, rows = -1, []                 # ghost frontier (input index), discharge rows
        while True:
            sym = tape[pos]
            T += 1
            first = (pos - 1) > r
            if first:
                r = pos - 1
            out = self.delta(q, sym)
            if out[0] == "HALT":
                rows.append((1 if first else 0, 1))
                return dict(answer=out[1], T=T, r=r, fallback=False, rows=rows,
                            last_sym=sym)
            q, mv = out
            rows.append((1 if first else 0, 0))
            if q == "FB":
                ans = reference(x)       # ABSTRACT total fallback, cost not modelled
                return dict(answer=ans, T=T, r=r, fallback=True, rows=rows, last_sym=sym)
            pos += mv
            assert 0 <= pos < len(tape)


def audit_m(m):
    t0 = time.time()
    checks = 0
    def ok(c, msg):
        nonlocal checks
        checks += 1
        if not c:
            raise AssertionError(msg)
    f0, f1 = build(m)
    b = math.ceil(math.log2(3 * m + 1))
    xm, xp = encode(f0, b), encode(f1, b)
    N = (24 * m + 1) * (b + 1) + 8 * m + 1
    ok(len(xp) == N and len(xm) == N, "N formula")
    ok(xm[:-1] == xp[:-1] and xm[-1] == "0" and xp[-1] == "1", "last-bit pair")
    ok(reference(xp) is True and reference(xm) is False, "labels via independent DPLL")
    A, P = Comparator(xp), Comparator(xp, promise=True)

    # 1. fused-halt reachability on the positive source
    R = A.run(xp)
    ok(R["answer"] is True and not R["fallback"], "accept on match path")
    ok(R["T"] == N + 1, "T = N+1 exactly")
    ok(R["last_sym"] == RIGHT and R["rows"][-1] == (1, 1), "final row fused (1,1)")
    ok(all(row == (1, 0) for row in R["rows"][:-1]), "every earlier row is (1,0)")
    # tariff checks: lambda=(1,0) and (0,1) and (1/2,1/2) sound; (1,1) violated only by fused row
    viol = [k for k, (a, c) in enumerate(R["rows"]) if a + c > 1]
    ok(viol == [N], "unit-unit tariff violated exactly at the fused final step")
    # 2. promise variant: T = N, never inspects endmarker
    RP = P.run(xp)
    ok(RP["answer"] is True and RP["T"] == N and RP["r"] == N - 1, "promise T=N, r=N-1")

    # 3. hostile battery: every single-bit flip, truncations, extensions, F^-
    hostile = [xm, xp + "0", xp + "1", xp + "00", xp[:-1], xp[: N // 2], "", "0", xp[1:]]
    hostile += [xp[:k] + ("1" if xp[k] == "0" else "0") + xp[k + 1:] for k in range(N)]
    nA = nP = wrongP = fbA = 0
    sat_flips = valid_flips = 0
    for k, x in enumerate(hostile):
        ref = reference(x)
        ra = A.run(x)
        ok(ra["answer"] == ref, "A_m correct on hostile input %d" % k)
        ok(ra["fallback"], "A_m leaves match path on every x != F_m^+")
        nA += 1; fbA += 1
        rp = P.run(x)
        nP += 1
        if rp["answer"] != ref:
            wrongP += 1
            ok(decode(x) is None, "promise variant errs only on malformed strings")
            ok(x.startswith(xp) and len(x) > N, "...and only on strict extensions of F_m^+")
        if k >= 9:
            if decode(x) is not None:
                valid_flips += 1
                sat_flips += 1 if ref else 0
    ok(wrongP == 3, "promise variant wrong exactly on extensions")
    return dict(m=m, b=b, N=N, T_total_convention=R["T"], T_promise=RP["T"],
                fused_final_row=list(R["rows"][-1]), table_rows=A.table_size(),
                hostile_inputs=nA, fallbacks=fbA, promise_wrong=wrongP,
                valid_single_flips=valid_flips, sat_single_flips=sat_flips,
                checks=checks, seconds=round(time.time() - t0, 3))


if __name__ == "__main__":
    if "--m" in sys.argv:
        print(json.dumps(audit_m(int(sys.argv[sys.argv.index("--m") + 1]))))
    else:
        res = [audit_m(m) for m in range(3, 13)]
        out = dict(run="TMR5-COMPARATOR075", results=res,
                   total_checks=sum(r["checks"] for r in res),
                   total_hostile=sum(r["hostile_inputs"] for r in res), failures=0)
        print(json.dumps(out, indent=1))
