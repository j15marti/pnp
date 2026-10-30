#!/usr/bin/env python3
"""HITTING-TREE-COMPOSITION-REFEREE222.

Exact full-boundary dynamic programming for a supplied and verified tree of
hitting CNF modules, plus clause-indexed S/U diagnostics and charged fallback.
Selected events are Python implementation counters, not machine-independent
time or space lower bounds.
"""
from __future__ import annotations

import itertools, json, random, time, tracemalloc
from collections import Counter, defaultdict, deque

RUN = "HITTING-TREE-COMPOSITION-REFEREE222"
SEED = 202610300648


def bits(mask, variables):
    return {v: (mask >> (v - 1)) & 1 for v in variables}


def lit_true(lit, a):
    return a[abs(lit)] == int(lit > 0)


def tcount(clause, a):
    return sum(lit_true(l, a) for l in clause)


def nvars(clauses):
    return max((abs(l) for c in clauses for l in c), default=0)


def models_brute(clauses):
    n = nvars(clauses)
    out = []
    for m in range(1 << n):
        a = bits(m, range(1, n + 1))
        if all(tcount(c, a) for c in clauses):
            out.append(m)
    return out


def clause_status(clauses, mask):
    n = nvars(clauses); a = bits(mask, range(1, n + 1))
    ts = [tcount(c, a) for c in clauses]
    return {"mask": mask, "x1_first": "".join(str(a[i]) for i in range(1, n + 1)),
            "t_by_original_clause": ts, "N0_N1_N2_N3": [ts.count(i) for i in range(4)],
            "SAT": 0 not in ts}


def local_targets(clauses):
    out = []
    for j, c in enumerate(clauses):
        occ = []
        for p, lit in enumerate(c):
            s = int(lit > 0); u = 1 - s
            occ.append({"occurrence": f"x_{{{abs(lit)},{j}}}", "position": p,
                        "literal": lit, "sign": "+" if lit > 0 else "-",
                        "S_all_literals_true": s, "invert_S_is_U": 1 - s,
                        "U_all_literals_false": u, "invert_U_is_S": 1 - u})
        out.append({"clause_index": j, "clause": list(c), "occurrences": occ})
    return out


def requirements(c, mode):
    return {abs(l): int((l > 0) == (mode == "S")) for l in c}


def pair_matrix(clauses):
    rows = []
    for j, k in itertools.combinations(range(len(clauses)), 2):
        cj, ck = clauses[j], clauses[k]
        shared = sorted(set(map(abs, cj)) & set(map(abs, ck)))
        same, opp = [], []
        for v in shared:
            sj = next(l > 0 for l in cj if abs(l) == v)
            sk = next(l > 0 for l in ck if abs(l) == v)
            (same if sj == sk else opp).append(v)
        modes = {}
        for mode in ("SS", "SU", "US", "UU"):
            q = {}; bad = []
            for c, z in ((cj, mode[0]), (ck, mode[1])):
                for v, val in requirements(c, z).items():
                    if v in q and q[v] != val: bad.append(v)
                    q[v] = val
            modes[mode] = {"feasible": not bad, "conflicting_variables": sorted(set(bad))}
        rows.append({"clause_indices": [j, k], "same_sign_shared": same,
                     "opposite_sign_shared": opp, "modes": modes})
    return rows


def flip_trails(clauses):
    n = nvars(clauses); out = []
    for start in (0, (1 << n) - 1):
        cur = start; trail = [clause_status(clauses, cur)]
        for v in range(1, min(n, 6) + 1):
            before = trail[-1]; cur ^= 1 << (v - 1); after = clause_status(clauses, cur)
            pred = list(before["t_by_original_clause"])
            a0 = bits(before["mask"], range(1, n + 1))
            for j, c in enumerate(clauses):
                for l in c:
                    if abs(l) == v: pred[j] += 1 if not lit_true(l, a0) else -1
            assert pred == after["t_by_original_clause"]
            trail.append(after)
        out.append({"start": start, "trail": trail})
    return out


def clash(c, d):
    return any(-l in d for l in c)


def hitting(clauses):
    return all(clash(c, d) for c, d in itertools.combinations(clauses, 2))


def false_clause_on(vars_, vals):
    return tuple(v if vals[v] == 0 else -v for v in vars_)


def force_literal(x, positive, a, b):
    # Four proper hitting clauses, equivalent to x (positive) or not x.
    head = x if positive else -x
    return [(head, sa * a, sb * b) for sa in (1, -1) for sb in (1, -1)]


def parity3(vs, charge):
    out = []
    for bs in itertools.product((0, 1), repeat=3):
        if sum(bs) % 2 != charge:
            out.append(tuple(v if b == 0 else -v for v, b in zip(vs, bs)))
    return out


def verify_tree(modules, edges, meter=None):
    if meter is None: meter = Counter()
    ids = sorted(modules); meter["verify_nodes"] += len(ids)
    if len(edges) != max(0, len(ids) - 1): return False, "not_tree_edge_count", {}
    adj = {i: [] for i in ids}
    for u, v in edges:
        meter["verify_edges"] += 1
        if u not in adj or v not in adj or u == v: return False, "bad_edge", {}
        adj[u].append(v); adj[v].append(u)
    seen = set(); q = [ids[0]] if ids else []
    while q:
        u = q.pop()
        if u in seen: continue
        seen.add(u); q.extend(adj[u])
    if len(seen) != len(ids): return False, "disconnected", {}
    node_vars = {i: set(abs(l) for c in modules[i] for l in c) for i in ids}
    for i in ids:
        meter["verify_clauses"] += len(modules[i])
        if not hitting(modules[i]): return False, f"module_{i}_not_hitting", {}
    allv = set().union(*node_vars.values()) if ids else set()
    for x in allv:
        carriers = {i for i in ids if x in node_vars[i]}; meter["verify_running"] += len(carriers)
        if not carriers: continue
        got = set(); qq = [next(iter(carriers))]
        while qq:
            u = qq.pop()
            if u in got or u not in carriers: continue
            got.add(u); qq.extend(adj[u])
        if got != carriers: return False, f"running_intersection_x{x}", {}
    boundary = {i: set().union(*(node_vars[i] & node_vars[j] for j in adj[i])) if adj[i] else set()
                for i in ids}
    return True, "ok", {"adj": adj, "node_vars": node_vars, "boundary": boundary}


def local_hitting_count(clauses, boundary, private, beta, meter):
    residual = []
    for c in clauses:
        meter["local_clause_reads"] += len(c)
        if any(abs(l) in boundary and beta[abs(l)] == int(l > 0) for l in c):
            continue
        r = tuple(l for l in c if abs(l) in private)
        if not r: return 0, None
        residual.append(r)
    assert hitting(residual)
    total = 1 << len(private)
    rejected = sum(1 << (len(private) - len(c)) for c in residual)
    count = total - rejected
    first = None
    if count:
        pv = sorted(private)
        for bs in itertools.product((0, 1), repeat=len(pv)):
            meter["local_witness_trials"] += 1
            a = dict(zip(pv, bs)) | beta
            if all(any(lit_true(l, a) for l in c) for c in clauses):
                first = {v: a[v] for v in pv}; break
    return count, first


def tree_count(modules, edges):
    meter = Counter(); ok, why, meta = verify_tree(modules, edges, meter)
    if not ok: return {"accepted": False, "reason": why, "events": sum(meter.values()), "meter": dict(meter)}
    adj, nv, bd = meta["adj"], meta["node_vars"], meta["boundary"]
    root = min(modules); parent = {root: None}; order = [root]
    for u in order:
        for v in adj[u]:
            if v != parent[u]: parent[v] = u; order.append(v)
    messages, witnesses = {}, {}
    for u in reversed(order):
        p = parent[u]; sep = sorted(nv[u] & nv[p]) if p is not None else []
        full = sorted(bd[u]); private = nv[u] - bd[u]
        msg, wit = {}, {}
        for abits in itertools.product((0, 1), repeat=len(sep)):
            alpha = dict(zip(sep, abits)); total = 0; chosen = None
            rest = [v for v in full if v not in alpha]
            for rbits in itertools.product((0, 1), repeat=len(rest)):
                meter["boundary_rows"] += 1
                beta = alpha | dict(zip(rest, rbits))
                lc, lw = local_hitting_count(modules[u], set(full), private, beta, meter)
                term = lc
                childw = []
                for c in adj[u]:
                    if c == p: continue
                    s = sorted(nv[u] & nv[c]); key = tuple(beta[v] for v in s)
                    meter["joins"] += 1; term *= messages[c][key]
                    childw.append(witnesses[c].get(key))
                total += term
                if term and chosen is None:
                    chosen = beta | (lw or {})
                    for cw in childw:
                        if cw: chosen.update(cw)
            keya = tuple(abits); msg[keya] = total; wit[keya] = chosen
        messages[u], witnesses[u] = msg, wit
    count = messages[root][()]; witness = witnesses[root][()]
    clauses = [c for u in sorted(modules) for c in modules[u]]
    if witness is not None:
        assert all(any(witness[abs(l)] == int(l > 0) for l in c) for c in clauses)
    return {"accepted": True, "reason": "ok", "count": count, "sat": count > 0,
            "witness": witness, "full_boundary_sizes": {str(u): len(bd[u]) for u in bd},
            "events": sum(meter.values()), "meter": dict(meter)}


def up_dpll(clauses):
    meter = Counter()
    def rec(cs, a):
        meter["nodes"] += 1
        while True:
            reduced = []; unit = None
            for c in cs:
                meter["literal_reads"] += len(c)
                if any(abs(l) in a and a[abs(l)] == int(l > 0) for l in c): continue
                r = tuple(l for l in c if abs(l) not in a)
                if not r: meter["conflicts"] += 1; return None
                if len(r) == 1: unit = r[0]
                reduced.append(r)
            cs = reduced
            if unit is None: break
            v, val = abs(unit), int(unit > 0); meter["propagations"] += 1
            if v in a and a[v] != val: return None
            a = dict(a); a[v] = val
        if not cs: return a
        v = abs(cs[0][0]); meter["branches"] += 1
        for val in (0, 1):
            b = dict(a); b[v] = val
            w = rec(cs, b)
            if w is not None: return w
        return None
    tracemalloc.start(); t0 = time.perf_counter(); w = rec(tuple(clauses), {})
    elapsed = time.perf_counter() - t0; _, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
    return {"sat": w is not None, "witness": w, "nodes": meter["nodes"],
            "events": sum(meter.values()), "meter": dict(meter), "seconds": elapsed,
            "peak_bytes": peak}


def resolvent_cubes(clauses, limit=32):
    n = nvars(clauses); out = []
    for j, k in itertools.combinations(range(len(clauses)), 2):
        for x in sorted(set(map(abs, clauses[j])) & set(map(abs, clauses[k]))):
            lj = next(l for l in clauses[j] if abs(l) == x)
            lk = next(l for l in clauses[k] if abs(l) == x)
            if lj != -lk: continue
            r = set(clauses[j]) | set(clauses[k]); r.discard(lj); r.discard(lk)
            if any(-l in r for l in r): continue
            r = tuple(sorted(r, key=lambda z:(abs(z),z)))
            pins = {abs(l): int(l < 0) for l in r}
            checked = 0
            free = [v for v in range(1, n + 1) if v not in pins]
            for bs in itertools.product((0, 1), repeat=len(free)):
                a = pins | dict(zip(free, bs)); checked += 1
                assert not (all(tcount(c, a) for c in clauses))
            out.append({"parents": [j,k], "pivot": x, "resolvent": list(r),
                        "prohibited_cube": {str(v): z for v,z in pins.items()},
                        "checked_completions": checked})
            if len(out) >= limit: return out
    return out


def random_chain(rng, k, idx):
    sep = list(range(1, k)); nxt = k - 1
    modules = {}; edges = [(i, i+1) for i in range(k-1)]
    for i in range(k):
        vs = []
        if i: vs.append(sep[i-1])
        if i < k-1: vs.append(sep[i])
        while len(vs) < 3:
            nxt += 1; vs.append(nxt)
        all8 = [tuple(v if b == 0 else -v for v,b in zip(vs, bs))
                for bs in itertools.product((0,1), repeat=3)]
        take = rng.randint(1,8); modules[i] = rng.sample(all8, take)
    return {"name": f"RANDOM_CHAIN_{idx}", "modules": modules, "edges": edges}


def named_cases():
    app = force_literal(1, True, 2, 3); amm = force_literal(1, False, 4, 5)
    bpp = force_literal(1, True, 4, 5)
    mid = [(6,7,8)]
    invalid = {0: app, 1: mid, 2: amm}
    # A duplicate destroys hitting in module 0.
    duplicate = {0: app + [app[0]], 1: bpp}
    return [
      {"name":"A_PLUS_B_PLUS", "modules":{0:app,1:bpp}, "edges":[(0,1)]},
      {"name":"A_MINUS_B_PLUS", "modules":{0:amm,1:bpp}, "edges":[(0,1)]},
      {"name":"RUNNING_INTERSECTION_VIOLATION", "modules":invalid, "edges":[(0,1),(1,2)]},
      {"name":"DUPLICATE_MODULE_REJECT", "modules":duplicate, "edges":[(0,1)]},
    ]


def audit_case(case, full_diag=True):
    modules, edges = case["modules"], case["edges"]
    clauses = [tuple(c) for u in sorted(modules) for c in modules[u]]
    exact = models_brute(clauses); base = up_dpll(clauses)
    tracemalloc.start(); t0=time.perf_counter(); dp=tree_count(modules, edges)
    dt=time.perf_counter()-t0; _,peak=tracemalloc.get_traced_memory(); tracemalloc.stop()
    if dp["accepted"]: assert dp["count"] == len(exact)
    else: assert base["sat"] == bool(exact)
    dp["total_events_with_fallback"] = dp["events"] if dp["accepted"] else dp["events"] + base["events"]
    dp["fallback_nodes"] = 0 if dp["accepted"] else base["nodes"]
    n=nvars(clauses)
    out={"name":case["name"],"n":n,"m":len(clauses),"modules":{str(k):[list(c) for c in v] for k,v in modules.items()},
         "edges":[list(e) for e in edges],"exact_model_count":len(exact),"exact_first_model":exact[0] if exact else None,
         "baseline":base,"tree_controller":dp|{"seconds":dt,"peak_bytes":peak},
         "endpoints":{"0^n":clause_status(clauses,0),"1^n":clause_status(clauses,(1<<n)-1)}}
    if full_diag:
        out |= {"local_targets":local_targets(clauses),"pair_matrix":pair_matrix(clauses),
                "flip_trails":flip_trails(clauses),"resolvent_cubes":resolvent_cubes(clauses)}
    return out


def hostile_controls():
    xor_even=[tuple(i+1 if b==0 else -(i+1) for i,b in enumerate(bs))
              for bs in itertools.product((0,1),repeat=3) if sum(bs)%2==1]
    tseitin=[]
    for vs,ch in [((1,2,3),1),((1,4,5),0),((2,4,6),0),((3,5,6),0)]: tseitin += parity3(vs,ch)
    horn=[(-1,-2,3),(-3,-4,-5),(-1,-4,-6),(2,-3,-6)]
    return [("XOR_EVEN",xor_even),("TSEITIN_K4_ODD",tseitin),("HORN",horn)]


def main():
    t0=time.perf_counter(); rng=random.Random(SEED)
    named=[audit_case(c,True) for c in named_cases()]
    random_cases=[]
    for i in range(60):
        c=random_chain(rng,1+i%5,i); random_cases.append(audit_case(c,i<6))
    hostile=[]
    for name,clauses in hostile_controls():
        base=up_dpll(clauses); exact=models_brute(clauses)
        hostile.append({"name":name,"n":nvars(clauses),"m":len(clauses),"models":len(exact),
                        "baseline":base,"endpoints":{"0^n":clause_status(clauses,0),
                        "1^n":clause_status(clauses,(1<<nvars(clauses))-1)},
                        "local_targets":local_targets(clauses),"pair_matrix":pair_matrix(clauses),
                        "flip_trails":flip_trails(clauses),"resolvent_cubes":resolvent_cubes(clauses)})
    # Minimal scalar-summary collision.
    np, nm = named[0], named[1]
    scalar={"A_plus_total":4,"A_minus_total":4,"B_plus_total":4,
            "A_plus_boundary_x0_x1":[0,4],"A_minus_boundary_x0_x1":[4,0],
            "B_plus_boundary_x0_x1":[0,4],"join_Aplus_Bplus":np["exact_model_count"],
            "join_Aminus_Bplus":nm["exact_model_count"],
            "running_intersection_bad_naive_product":4*7*4,
            "running_intersection_bad_exact_count":named[2]["exact_model_count"]}
    out={"run_id":RUN,"timestamp":"2026-10-30T06:48:00-07:00","seed":SEED,
         "claims":{"exact":"Verified running-intersection tree plus full boundary tables composes exact counts.",
                   "falsified":"Scalar module counts do not compose, and dropping running intersection can make DP unsound.",
                   "scope":"Supplied/verified module tree; arbitrary decomposition discovery and general SAT remain open."},
         "scalar_falsifier":scalar,"named_cases":named,"random_chains":random_cases,"hostile_controls":hostile,
         "summary":{"named":len(named),"random_chains":len(random_cases),"hostile":len(hostile),
                    "all_valid_tree_counts_exact":all((not c["tree_controller"]["accepted"]) or c["tree_controller"]["count"]==c["exact_model_count"] for c in named+random_cases),
                    "accepted_random":sum(c["tree_controller"]["accepted"] for c in random_cases),
                    "random_assignment_checks":sum(1<<c["n"] for c in random_cases),
                    "elapsed_seconds":time.perf_counter()-t0}}
    with open("2026-10-30_0648_HITTING-TREE-COMPOSITION-REFEREE222_raw.json","w") as f: json.dump(out,f,indent=2,sort_keys=True)
    summary={"run_id":RUN,"summary":out["summary"],"scalar_falsifier":scalar,
             "named":[{"name":c["name"],"n":c["n"],"m":c["m"],"models":c["exact_model_count"],
                       "accepted":c["tree_controller"]["accepted"],"reason":c["tree_controller"]["reason"],
                       "dp_events":c["tree_controller"]["events"],
                       "controller_total_events":c["tree_controller"]["total_events_with_fallback"],
                       "base_events":c["baseline"]["events"],
                       "base_nodes":c["baseline"]["nodes"]} for c in named],
             "hostile":[{"name":c["name"],"models":c["models"],"events":c["baseline"]["events"]} for c in hostile]}
    with open("2026-10-30_0648_HITTING-TREE-COMPOSITION-REFEREE222_summary.json","w") as f: json.dump(summary,f,indent=2,sort_keys=True)
    print(json.dumps(summary,indent=2,sort_keys=True))


if __name__=="__main__": main()
