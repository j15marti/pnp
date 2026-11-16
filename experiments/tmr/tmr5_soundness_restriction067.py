#!/usr/bin/env python3
"""TMR-5/067: soundness-route restriction transfer, executed check.

Revision tag: tmr5-soundness-restriction067.v1   Seed: 20261116

Pipeline (all steps executed, no oracle):
  formula slots (n vars, m clause slots) -> encoding bits f
  -> brute-force SAT-decider circuit C_{n,m}(f) (Tseitin gate variables)
  -> CNF Sound(C) = Tseitin(C) & (not out) & Sat(f,a,s)      [Krajicek 2012 ref^M form]
  -> RUP proof of Sound(C), expanded to an explicit resolution DAG
  -> for each authentic UNSAT F: restriction rho_F (f, gate values, s) plus
     literal substitution s+ := a_i, s- := ~a_i
  -> restricted resolution DAG, checked by an INDEPENDENT checker to be a
     resolution refutation of F itself, with line count <= original.
Controls: satisfiable F (transfer must fail: rho falsifies (not out));
          wrong circuit C0 == 0 ('always UNSAT') (Sound(C0) not refutable).
COMPUTATIONAL evidence only; the asymptotic statements are proved in the report.
"""
import itertools, json, random, sys, time, hashlib

SEED = 20261116
REV = "tmr5-soundness-restriction067.v1"


class VarPool:
    def __init__(self):
        self.n = 0
        self.names = {}

    def new(self, name):
        self.n += 1
        self.names[name] = self.n
        return self.n


def build_sound(n, m):
    vp = VarPool()
    P = {(j, i): vp.new(("p", j, i)) for j in range(m) for i in range(n)}
    Q = {(j, i): vp.new(("q", j, i)) for j in range(m) for i in range(n)}
    A = [vp.new(("a", i)) for i in range(n)]
    Sp = {(j, i): vp.new(("sp", j, i)) for j in range(m) for i in range(n)}
    Sm = {(j, i): vp.new(("sm", j, i)) for j in range(m) for i in range(n)}
    Cg = {}
    G = {}
    cls = []
    tag = []  # axiom type for bookkeeping
    assigns = list(itertools.product([0, 1], repeat=n))
    for b in assigns:
        for j in range(m):
            c = vp.new(("c", j, b))
            Cg[(j, b)] = c
            lits = [P[(j, i)] if b[i] else Q[(j, i)] for i in range(n)]
            cls.append([-c] + lits); tag.append("gate")
            for l in lits:
                cls.append([c, -l]); tag.append("gate")
        g = vp.new(("g", b))
        G[b] = g
        for j in range(m):
            cls.append([-g, Cg[(j, b)]]); tag.append("gate")
        cls.append([g] + [-Cg[(j, b)] for j in range(m)]); tag.append("gate")
    out = vp.new(("out",))
    cls.append([-out] + [G[b] for b in assigns]); tag.append("gate")
    for b in assigns:
        cls.append([out, -G[b]]); tag.append("gate")
    cls.append([-out]); tag.append("reject")
    for j in range(m):
        cls.append([Sp[(j, i)] for i in range(n)] + [Sm[(j, i)] for i in range(n)]); tag.append(("sat", j))
        for i in range(n):
            cls.append([-Sp[(j, i)], P[(j, i)]]); tag.append("satdef")
            cls.append([-Sp[(j, i)], A[i]]); tag.append("satdef")
            cls.append([-Sm[(j, i)], Q[(j, i)]]); tag.append("satdef")
            cls.append([-Sm[(j, i)], -A[i]]); tag.append("satdef")
    V = dict(P=P, Q=Q, A=A, Sp=Sp, Sm=Sm, C=Cg, G=G, out=out, assigns=assigns)
    return vp, cls, tag, V


def rup_lines(n, m, V):
    A = V["A"]
    lines = []
    for b in V["assigns"]:
        neqb = [(A[i] if b[i] == 0 else -A[i]) for i in range(n)]
        for j in range(m):
            lines.append(neqb + [V["C"][(j, b)]])
        lines.append(neqb + [V["G"][b]])
        lines.append(list(neqb))
    # resolve prefixes down to empty clause
    for k in range(n - 1, -1, -1):
        for pre in itertools.product([0, 1], repeat=k):
            lines.append([(A[i] if pre[i] == 0 else -A[i]) for i in range(k)])
    return lines


def rup_to_resolution(axioms, rup):
    """Expand RUP lines into explicit resolution steps.
    proof entries: ('ax', clause, idx) | ('res', clause, p1, p2, pivotvar)."""
    proof = []
    for k, c in enumerate(axioms):
        proof.append(("ax", tuple(sorted(set(c))), k))
    db = list(range(len(proof)))
    for L in rup:
        Lset = set(L)
        val = {}
        reason = {}
        for l in L:
            val[abs(l)] = (l < 0)  # assign negation of L
            reason[abs(l)] = None
        trail = [abs(l) for l in L]
        conflict = None
        changed = True
        while changed and conflict is None:
            changed = False
            for idx in db:
                cl = proof[idx][1]
                unassigned = []
                sat = False
                for l in cl:
                    v = abs(l)
                    if v in val:
                        if val[v] == (l > 0):
                            sat = True; break
                    else:
                        unassigned.append(l)
                if sat:
                    continue
                if not unassigned:
                    conflict = idx; break
                if len(unassigned) == 1:
                    l = unassigned[0]
                    val[abs(l)] = (l > 0); reason[abs(l)] = idx
                    trail.append(abs(l)); changed = True
        if conflict is None:
            raise ValueError("RUP check failed for line %r" % (L,))
        cur = conflict
        curset = set(proof[cur][1])
        for v in reversed(trail):
            if reason.get(v) is None:
                continue
            if v in curset or -v in curset:
                r = reason[v]
                rs = set(proof[r][1])
                new = (curset | rs) - {v, -v}
                proof.append(("res", tuple(sorted(new)), cur, r, v))
                cur = len(proof) - 1
                curset = new
        assert curset <= Lset, (curset, Lset)
        db.append(cur)
    return proof, db[-1]


def restriction(n, m, V, F):
    """rho: var -> 0/1 constant or ('lit', literal over a). Requires C(F)=0 for soundness."""
    rho = {}
    pos = {(j, i) for j, cl in enumerate(F) for l in cl if l > 0 for i in [l - 1]}
    neg = {(j, i) for j, cl in enumerate(F) for l in cl if l < 0 for i in [-l - 1]}
    for j in range(m):
        for i in range(n):
            rho[V["P"][(j, i)]] = 1 if (j, i) in pos else 0
            rho[V["Q"][(j, i)]] = 1 if (j, i) in neg else 0
            rho[V["Sp"][(j, i)]] = ("lit", V["A"][i]) if (j, i) in pos else 0
            rho[V["Sm"][(j, i)]] = ("lit", -V["A"][i]) if (j, i) in neg else 0
    anyg = 0
    for b in V["assigns"]:
        gv = 1
        for j in range(m):
            cv = int(any(((i, ) and ((b[i] == 1 and (j, i) in pos) or (b[i] == 0 and (j, i) in neg))) for i in range(n)))
            rho[V["C"][(j, b)]] = cv
            gv &= cv
        rho[V["G"][b]] = gv
        anyg |= gv
    rho[V["out"]] = anyg
    return rho


def image(clause, rho):
    out = set()
    for l in clause:
        v = abs(l)
        r = rho.get(v, ("lit", v))
        if isinstance(r, tuple):
            ll = r[1] if l > 0 else -r[1]
            if -ll in out:
                return None
            out.add(ll)
        else:
            if (r == 1) == (l > 0):
                return None  # satisfied
    return frozenset(out)


def restrict_proof(proof, rho):
    R = []
    for e in proof:
        if e[0] == "ax":
            im = image(e[1], rho)
            R.append(("ax", im))
        else:
            _, cl, p1, p2, v = e
            c1, c2 = R[p1][1], R[p2][1]
            r = rho.get(v, ("lit", v))
            # orient: proof[p1] contains literal x (+v or -v), proof[p2] its negation
            x = v if v in proof[p1][1] else -v
            const = not isinstance(r, tuple)
            if not const:
                ell = r[1] if x > 0 else -r[1]
            else:
                ell = 1 if ((r == 1) == (x > 0)) else 0  # constant truth of x
            # Invariant: R[k] is None only if image(proof[k]) is satisfied/tautological;
            # otherwise R[k][1] is a derived clause contained in image(proof[k]).
            if c1 is None and c2 is None or image(cl, rho) is None:
                R.append(("true", None)); continue
            if const:
                # x constant: neither parent image contains x, so each parent image
                # is contained in the child image; copy any non-TRUE parent.
                R.append(("copy", c1, p1) if c1 is not None else ("copy", c2, p2)); continue
            if c1 is not None and ell not in c1:
                R.append(("copy", c1, p1)); continue
            if c2 is not None and -ell not in c2:
                R.append(("copy", c2, p2)); continue
            if c1 is None:
                # image(p1) TRUE: either child image TRUE, or p1 tautological through
                # not-ell, in which case not-ell lies in the child image: c2 fits.
                R.append(("copy", c2, p2)); continue
            if c2 is None:
                R.append(("copy", c1, p1)); continue
            new = (c1 | c2) - {ell, -ell}
            if any(-l in new for l in new):
                R.append(("true", None)); continue
            R.append(("res", frozenset(new), p1, p2, abs(ell)))
    for k, e in enumerate(R):  # executed invariant check
        if e[1] is not None:
            im = image(proof[k][1], rho)
            assert im is not None and frozenset(e[1]) <= im, ("invariant", k)
    # compress: drop true / copy lines; build explicit proof list
    out = []
    idmap = {}
    for k, e in enumerate(R):
        if e[0] == "ax":
            if e[1] is not None:
                out.append(("ax", sorted(e[1]))); idmap[k] = len(out) - 1
        elif e[0] == "copy":
            idmap[k] = idmap[e[2]]
        elif e[0] == "res":
            out.append(("res", sorted(e[1]), idmap[e[2]], idmap[e[3]])); idmap[k] = len(out) - 1
    final = idmap.get(len(R) - 1)
    if final is None:
        return [], R
    # prune to ancestors of the final line, renumber
    need = set(); stack = [final]
    while stack:
        k = stack.pop()
        if k in need:
            continue
        need.add(k)
        if out[k][0] == "res":
            stack += [out[k][2], out[k][3]]
    order = sorted(need); ren = {k: t for t, k in enumerate(order)}
    pr = []
    for k in order:
        e = out[k]
        pr.append(e if e[0] == "ax" else ("res", e[1], ren[e[2]], ren[e[3]]))
    return pr, R


def independent_check(F, proof):
    """Independent resolution-refutation checker for F (list of int clauses)."""
    Fset = {frozenset(c) for c in F}
    seen = []
    for k, e in enumerate(proof):
        c = frozenset(e[1])
        if any(-l in c for l in c):
            return False, "tautology line %d" % k
        if e[0] == "ax":
            if c not in Fset:
                return False, "axiom %d not a clause of F: %s" % (k, sorted(c))
        else:
            a, b = e[2], e[3]
            if not (a < k and b < k):
                return False, "forward ref %d" % k
            A_, B_ = frozenset(proof[a][1]), frozenset(proof[b][1])
            piv = [l for l in A_ if -l in B_]
            if len(piv) != 1:
                return False, "bad pivot at %d" % k
            l = piv[0]
            if c != (A_ | B_) - {l, -l}:
                return False, "bad resolvent at %d" % k
        seen.append(c)
    if not seen or seen[-1] != frozenset():
        return False, "last line not empty"
    return True, "ok"


def brute_sat(n, F):
    for a in itertools.product([0, 1], repeat=n):
        if all(any((a[abs(l) - 1] == 1) == (l > 0) for l in cl) for cl in F):
            return True
    return False


def rand_formula(rng, n, m):
    F = []
    for _ in range(m):
        w = rng.choice([1, 2, 2, 3, 3, 3]) if n >= 3 else rng.choice([1, 2])
        vs = rng.sample(range(1, n + 1), min(w, n))
        F.append(sorted(v if rng.random() < .5 else -v for v in vs))
    return F


def main():
    t0 = time.time()
    rng = random.Random(SEED)
    raw = {"revision": REV, "seed": SEED, "python": sys.version.split()[0], "configs": []}
    asserts = 0
    fails = 0
    for (n, m, trials) in [(2, 4, 60), (3, 6, 120), (3, 8, 120), (4, 10, 60), (5, 16, 30), (6, 26, 12)]:
        vp, cls, tag, V = build_sound(n, m)
        rup = rup_lines(n, m, V)
        proof, last = rup_to_resolution(cls, rup)
        assert proof[last][1] == (); asserts += 1
        n_ax = len(cls)
        n_res = sum(1 for e in proof if e[0] == "res")
        cfg = {"n": n, "m": m, "sound_vars": vp.n, "sound_clauses": n_ax,
               "rup_lines": len(rup), "resolution_steps": n_res,
               "cases": []}
        unsat_done = sat_done = 0
        tries = 0
        while (unsat_done < trials or sat_done < 10) and tries < 200000:
            tries += 1
            F = rand_formula(rng, n, m)
            s = brute_sat(n, F)
            if s and sat_done >= 10:
                continue
            if (not s) and unsat_done >= trials:
                continue
            rho = restriction(n, m, V, F)
            asserts += 1
            if rho[V["out"]] != int(s):
                fails += 1
            rp, _ = restrict_proof(proof, rho)
            FA = [[(V["A"][abs(l) - 1] if l > 0 else -V["A"][abs(l) - 1]) for l in cl] for cl in F]
            ok, why = independent_check(FA, rp)
            if not s:
                unsat_done += 1
                asserts += 2
                if not ok:
                    fails += 1
                    print("FAIL", n, m, F, why)
                used_lines = len(rp)
                if used_lines > len(proof):
                    fails += 1
                cfg["cases"].append({"F": F, "sat": False, "transfer_ok": ok,
                                     "restricted_lines": used_lines,
                                     "restricted_res_steps": sum(1 for e in rp if e[0] == "res")})
            else:
                sat_done += 1
                asserts += 1
                # control: transfer must NOT yield a refutation of a satisfiable F
                if ok:
                    fails += 1
                cfg["cases"].append({"F": F, "sat": True, "transfer_ok": ok, "reason": why})
        # wrong-circuit control: C0 == constant 0; Sound(C0) is satisfiable, RUP must fail
        C0 = [[-V["out"]]] + [c for c, t in zip(cls, tag) if t in ("satdef",) or isinstance(t, tuple)]
        try:
            rup_to_resolution(C0, rup)
            ctrl = "UNEXPECTED_ACCEPT"; fails += 1
        except ValueError:
            ctrl = "rejected"
        asserts += 1
        cfg["wrong_circuit_control"] = ctrl
        cfg["unsat_cases"] = unsat_done
        cfg["sat_controls"] = sat_done
        cfg["max_restricted_lines"] = max(c["restricted_lines"] for c in cfg["cases"] if not c["sat"])
        cfg["original_lines"] = len(proof)
        raw["configs"].append(cfg)
        print("n=%d m=%d vars=%d axioms=%d rup=%d res=%d unsat=%d sat=%d maxR=%d ctrl=%s" % (
            n, m, vp.n, n_ax, len(rup), n_res, unsat_done, sat_done, cfg["max_restricted_lines"], ctrl))
    raw["assertions"] = asserts
    raw["failures"] = fails
    raw["seconds"] = round(time.time() - t0, 2)
    print("assertions", asserts, "failures", fails, "seconds", raw["seconds"])
    path = sys.argv[1] if len(sys.argv) > 1 else None
    if path:
        with open(path, "w") as fh:
            json.dump(raw, fh, sort_keys=True)
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
