#!/usr/bin/env python3
"""Checkpointed clause-minimal UNSAT core of the native strict-C 150/176 girth-10 source.

Usage (python3.13, pysat 1.9.dev24):
  strict_c_girth10_core_mus.py step      # one bounded stage (~25 s budget), resumable
  strict_c_girth10_core_mus.py finalize  # verify witnesses on the predicate, emit core CNF
  strict_c_girth10_core_mus.py proof     # Glucose4 DRUP proof of core CNF (check with drat-trim)

Pinned source: research/agents/critical-graphs/2026-11-19_regenerate_nativeC_girth10_150.py
(seed 20, SHA256 ecb0b31b...). Encoding: one-hot over Z5 per variable plus, for each
physical clause, the 95 rejected tuples of the ORIGINAL strict-C predicate as 3-clauses.
Symmetry fact used (PROVED, checked below on all 125 tuples): C(x,y,z) holds iff
{x,y,z} = {a,a+1,a+2} mod 5 for some a, so every subformula is invariant under the
translation x -> x+t; hence fixing original variable 0 to value 0 is SAT-preserving
for every subset of clauses.  Deterministic; no randomness beyond the pinned source.
"""
import hashlib
import importlib.util
import itertools
import json
import os
import sys
import time

from pysat.solvers import Cadical153, Glucose4

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location(
    "regen", os.path.join(REPO, "research/agents/critical-graphs/2026-11-19_regenerate_nativeC_girth10_150.py"))
regen = importlib.util.module_from_spec(spec)
spec.loader.exec_module(regen)

OUT = os.path.join(REPO, "results", "raw", "strict_c_girth10_core")
STATE = os.path.join(OUT, "mus_state.json")
Q = 5
BUDGET = 25.0


def R(a, b):
    return (b - a) % Q in (1, 3)


def C(x, y, z):
    return (R(x, y) and R(y, z) and R(z, x)) or (R(x, z) and R(z, y) and R(y, x))


REJECT = [t for t in itertools.product(range(Q), repeat=3) if not C(*t)]
assert len(REJECT) == 95
for _t in itertools.product(range(Q), repeat=3):
    assert C(*_t) == any(set(_t) == {a % Q, (a + 1) % Q, (a + 2) % Q} for a in range(Q))
    assert C(*_t) == C(*((v + 1) % Q for v in _t))


def lit(v, c):
    return v * Q + c + 1


def base_cnf(n):
    cl = []
    for v in range(n):
        cl.append([lit(v, c) for c in range(Q)])
        for c1 in range(Q):
            for c2 in range(c1 + 1, Q):
                cl.append([-lit(v, c1), -lit(v, c2)])
    return cl


def group_cnf(tri):
    a, b, c = tri
    return [[-lit(a, i), -lit(b, j), -lit(c, k)] for (i, j, k) in REJECT]


def decode(model, n):
    s = set(l for l in model if l > 0)
    w = []
    for v in range(n):
        vals = [c for c in range(Q) if lit(v, c) in s]
        assert len(vals) == 1
        w.append(vals[0])
    return w


def source():
    clauses = [tuple(t) for t in regen.gen()]
    src = json.dumps({"n": regen.N, "seed": regen.SEED, "clauses": [list(t) for t in clauses]}).encode()
    sha = hashlib.sha256(src).hexdigest()
    assert sha == regen.EXPECTED_SHA256, sha
    return regen.N, clauses, sha


def build(n, clauses):
    sel = [n * Q + 1 + j for j in range(len(clauses))]
    s = Cadical153(bootstrap_with=base_cnf(n))
    s.add_clause([lit(0, 0)])  # translation symmetry break
    for j, t in enumerate(clauses):
        for c in group_cnf(t):
            s.add_clause(c + [-sel[j]])
    return s, sel


def step():
    t0 = time.time()
    n, clauses, sha = source()
    os.makedirs(OUT, exist_ok=True)
    st = json.load(open(STATE)) if os.path.exists(STATE) else None
    s, sel = build(n, clauses)
    if st is None:
        ok = s.solve(assumptions=sel)
        assert not ok
        cur = sorted(sel.index(x) for x in s.get_core())
        st = {"source_sha256": sha, "current": cur, "first_core_size": len(cur), "necessary": [],
              "witnesses": {}, "calls": [{"kind": "full", "result": "UNSAT", "s": round(time.time() - t0, 2),
                                          "core": len(cur)}]}
    while time.time() - t0 < BUDGET:
        untested = [j for j in st["current"] if j not in st["necessary"]]
        if not untested:
            break
        j = untested[0]
        trial = [k for k in st["current"] if k != j]
        t1 = time.time()
        if s.solve(assumptions=[sel[k] for k in trial]):
            w = decode(s.get_model(), n)
            st["necessary"].append(j)
            st["witnesses"][str(j)] = w
            st["calls"].append({"kind": "drop", "clause": j, "result": "SAT", "s": round(time.time() - t1, 2)})
        else:
            core = sorted(sel.index(x) for x in s.get_core())
            assert set(st["necessary"]) <= set(core)
            st["current"] = core
            st["calls"].append({"kind": "drop", "clause": j, "result": "UNSAT", "s": round(time.time() - t1, 2),
                                "core": len(core)})
        json.dump(st, open(STATE, "w"), sort_keys=True)
    s.delete()
    json.dump(st, open(STATE, "w"), sort_keys=True)
    left = len([j for j in st["current"] if j not in st["necessary"]])
    print(f"current={len(st['current'])} necessary={len(st['necessary'])} untested={left} "
          f"calls={len(st['calls'])} stage_s={time.time() - t0:.1f}")
    return left


def chunk():
    """One adaptive chunk-deletion call (dichotomic deletion MUS), direct CNF, no selectors.
    State chunk_state.json: S (current UNSAT set), necessary, k (chunk size), calls."""
    t0 = time.time()
    n, clauses, sha = source()
    path = os.path.join(OUT, "chunk_state.json")
    os.makedirs(OUT, exist_ok=True)
    st = json.load(open(path)) if os.path.exists(path) else {
        "source_sha256": sha, "S": list(range(len(clauses))), "necessary": [], "k": int(sys.argv[2]),
        "witnesses": {}, "calls": []}
    untested = [j for j in st["S"] if j not in st["necessary"]]
    if not untested:
        print("DONE size", len(st["S"]))
        return
    ch = untested[:st["k"]]
    trial = [j for j in st["S"] if j not in ch]
    s = Cadical153(bootstrap_with=base_cnf(n))
    s.add_clause([lit(clauses[trial[0]][0], 0)])  # translation symmetry break
    for j in trial:
        for c in group_cnf(clauses[j]):
            s.add_clause(c)
    r = s.solve()
    if r:
        w = decode(s.get_model(), n)
        assert all(C(*(w[v] for v in clauses[j])) for j in trial)
        if len(ch) == 1:
            st["necessary"].append(ch[0])
            st["witnesses"][str(ch[0])] = w
        st["k"] = max(1, len(ch) // 2)
    else:
        st["S"] = trial
        st["k"] = min(2 * len(ch), 64)
    s.delete()
    st["calls"].append({"chunk": ch, "result": "SAT" if r else "UNSAT", "s": round(time.time() - t0, 1)})
    json.dump(st, open(path, "w"), sort_keys=True)
    print(f"chunk={len(ch)} {'SAT' if r else 'UNSAT'} S={len(st['S'])} necessary={len(st['necessary'])} "
          f"k={st['k']} s={time.time() - t0:.1f}")


def probe():
    """Conflict-budgeted necessity probe in the FULL source: SAT for F minus j certifies that
    j is in EVERY UNSAT subformula's... no: it certifies j is necessary in F, and hence in every
    UNSAT subset of F containing it (removing j from a subset leaves a subset of the SAT F-j).
    Resumable; writes probe_state.json."""
    t0 = time.time()
    n, clauses, sha = source()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "probe_state.json")
    st = json.load(open(path)) if os.path.exists(path) else {"source_sha256": sha, "budget": int(sys.argv[2]),
                                                               "sat": {}, "undecided": [], "unsat": [], "next": 0}
    s, sel = build(n, clauses)
    m = len(clauses)
    while st["next"] < m and time.time() - t0 < BUDGET:
        j = st["next"]
        s.conf_budget(st["budget"])
        r = s.solve_limited(assumptions=[sel[k] for k in range(m) if k != j])
        if r is True:
            w = decode(s.get_model(), n)
            assert all(C(*(w[v] for v in clauses[k])) for k in range(m) if k != j)
            st["sat"][str(j)] = w
        elif r is False:
            st["unsat"].append(j)
        else:
            st["undecided"].append(j)
        st["next"] = j + 1
    s.delete()
    json.dump(st, open(path, "w"), sort_keys=True)
    print(f"next={st['next']} sat={len(st['sat'])} unsat={len(st['unsat'])} undecided={len(st['undecided'])} "
          f"stage_s={time.time() - t0:.1f}")


def necessary_core_check():
    """If the set N of probe-certified necessary clauses is itself UNSAT, N is a MUS."""
    t0 = time.time()
    n, clauses, sha = source()
    st = json.load(open(os.path.join(OUT, "probe_state.json")))
    N = sorted(int(j) for j in st["sat"])
    s, sel = build(n, clauses)
    r = s.solve(assumptions=[sel[k] for k in N])
    res = {"N_size": len(N), "N": N, "N_status": "SAT" if r else "UNSAT", "s": round(time.time() - t0, 1)}
    if r:
        res["N_witness"] = decode(s.get_model(), n)
    else:
        res["core_of_N"] = sorted(sel.index(x) for x in s.get_core())
    json.dump(res, open(os.path.join(OUT, "necessary_check.json"), "w"), sort_keys=True)
    print({k: v for k, v in res.items() if k not in ("N", "N_witness", "core_of_N")})


def finalize():
    n, clauses, sha = source()
    st = json.load(open(STATE))
    core = st["current"]
    assert sorted(st["necessary"]) == sorted(core), "MUS not complete"
    for j in core:
        w = st["witnesses"][str(j)]
        assert all(C(*(w[v] for v in clauses[k])) for k in core if k != j)
        assert not C(*(w[v] for v in clauses[j]))
    cvars = sorted({v for j in core for v in clauses[j]})
    ren = {v: i for i, v in enumerate(cvars)}
    tri = [tuple(ren[v] for v in clauses[j]) for j in core]
    nc = len(cvars)
    cnf = base_cnf(nc) + [c for t in tri for c in group_cnf(t)]
    with open(os.path.join(OUT, "core.cnf"), "w") as f:
        f.write(f"p cnf {nc * Q} {len(cnf)}\n")
        f.writelines(" ".join(map(str, c)) + " 0\n" for c in cnf)
    with open(os.path.join(OUT, "core_source.json"), "w") as f:
        json.dump({"n": nc, "clauses": [list(t) for t in tri], "original_vars": cvars,
                   "original_clause_indices": core, "parent_sha256": sha}, f)
    regen.N = nc
    girth = regen.incidence_girth(tri)
    deg = [0] * nc
    for t in tri:
        for v in t:
            deg[v] += 1
    # connectivity of incidence graph
    par = list(range(nc))

    def fd(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for a, b, c in tri:
        par[fd(a)] = fd(b)
        par[fd(b)] = fd(c)
    comps = len({fd(v) for v in range(nc)})
    rec = {"core_size": len(core), "core_vars": nc, "incidence_girth": girth, "components": comps,
           "degree_hist": {str(d): deg.count(d) for d in sorted(set(deg))},
           "first_core_size": st["first_core_size"], "sat_calls": sum(c["result"] == "SAT" for c in st["calls"]),
           "unsat_calls": sum(c["result"] == "UNSAT" for c in st["calls"]),
           "total_solver_s": round(sum(c["s"] for c in st["calls"]), 1),
           "deletion_witnesses_verified": len(core), "cnf_vars": nc * Q, "cnf_clauses": len(cnf),
           "core_source_sha256": hashlib.sha256(open(os.path.join(OUT, "core_source.json"), "rb").read()).hexdigest(),
           "core_cnf_sha256": hashlib.sha256(open(os.path.join(OUT, "core.cnf"), "rb").read()).hexdigest()}
    json.dump(rec, open(os.path.join(OUT, "finalize.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps(rec, sort_keys=True))


def proof():
    t0 = time.time()
    lines = open(os.path.join(OUT, "core.cnf")).read().split("\n")[1:]
    cnf = [list(map(int, l.split()))[:-1] for l in lines if l.strip()]
    with Glucose4(bootstrap_with=cnf, with_proof=True) as g:
        assert not g.solve()
        pr = g.get_proof()
    with open(os.path.join(OUT, "core.drup"), "w") as f:
        f.write("\n".join(pr) + "\n")
    print("drup_lines", len(pr), "s", round(time.time() - t0, 1))


if __name__ == "__main__":
    {"step": step, "chunk": chunk, "probe": probe, "ncheck": necessary_core_check, "finalize": finalize, "proof": proof}[sys.argv[1]]()
