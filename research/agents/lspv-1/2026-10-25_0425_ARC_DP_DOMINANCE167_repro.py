#!/usr/bin/env python3
"""ARC-DP-DOMINANCE167: exact envelope algebra and finite scoped-SAT controls.

Python's statement counts are not FLMV bit-time or physical switching counts.
Standard library only. No all-input normalizer is constructed.
"""
from __future__ import annotations

import itertools
import json
import random
from fractions import Fraction as F
from pathlib import Path

SEED = 202610250425
C = F(241, 200)
D = F(11642479, 23232400)


def row_bounds(K, mu, delta, d, r, eta):
    assert isinstance(d, int) and d >= 2
    q = F(1, 2**d)
    time = max(r, mu + d * delta, mu * (1 - q) + d * delta + mu * q * K)
    space = max(eta, mu / 2, delta, mu * q * K)
    return time, space, delta < mu * q


def dp_bounds(mu, delta, r, eta):
    return max(r, mu + delta), max(eta, delta)


def ceil_log2_int(x):
    assert x > 0
    return (x - 1).bit_length()


def sup_width_cap(K, d):
    # Only mu=1, positive delta, strict time/space and hereditary margin.
    q = F(1, 2**d)
    if K * q >= D or F(K - 1) * q >= C - 1:
        return None
    return min(q, (C - 1 - (K - 1) * q) / d)


def serialize(n, clauses):
    parts = [f"p cnf {n} {len(clauses)}\n"]
    for clause in clauses:
        parts.append(" ".join(str(x) for x in clause) + " 0\n")
    return "".join(parts).encode("ascii")


def parse(payload):
    lines = payload.decode("ascii").splitlines()
    assert lines and len(lines[0].split()) == 4
    head = lines[0].split()
    assert head[:2] == ["p", "cnf"]
    n, m = int(head[2]), int(head[3])
    assert 0 <= n <= 100000 and m >= 0
    assert len(lines) == m + 1
    clauses = []
    for line in lines[1:]:
        toks = [int(x) for x in line.split()]
        assert toks and toks[-1] == 0
        assert all(x != 0 and abs(x) <= n for x in toks[:-1])
        clauses.append(tuple(toks[:-1]))
    return n, tuple(clauses)


def exact_sat(n, clauses):
    for word in itertools.product((False, True), repeat=n):
        if all(any(word[abs(lit)-1] == (lit > 0) for lit in cl)
               for cl in clauses):
            return True
    return False


def restrict(clauses, var, value):
    ans = []
    for clause in clauses:
        if any(abs(lit) == var and ((lit > 0) == value) for lit in clause):
            continue
        ans.append(tuple(lit for lit in clause if abs(lit) != var))
    return tuple(ans)


def events_all_open(n, clauses):
    events = [("OPEN", v) for v in range(1, n+1)]
    events += [("CLAUSE", c) for c in clauses]
    events += [("CLOSE", v) for v in range(n, 0, -1)]
    return events


def dp_scoped(events, stats):
    live, relation, open_once = [], {()}, set()
    for typ, val in events:
        stats["events"] += 1
        stats["row_entries_visited"] += len(relation)
        if typ == "OPEN":
            assert val not in open_once
            open_once.add(val)
            live.append(val)
            relation = {row + (bit,) for row in relation for bit in (False, True)}
        elif typ == "CLAUSE":
            assert all(abs(x) in live and x != 0 for x in val)
            index = {v: i for i, v in enumerate(live)}
            relation = {row for row in relation if any(
                row[index[abs(x)]] == (x > 0) for x in val)}
        elif typ == "CLOSE":
            assert val in live
            idx = live.index(val)
            relation = {row[:idx]+row[idx+1:] for row in relation}
            del live[idx]
        else:
            raise AssertionError("invalid event kind")
        stats["max_live"] = max(stats["max_live"], len(live))
        stats["max_relation"] = max(stats["max_relation"], len(relation))
    assert not live
    return () in relation


def force_unsat_cube():
    return tuple(tuple((i+1 if bit else -(i+1)) for i, bit in enumerate(bits))
                 for bits in itertools.product((0, 1), repeat=3))


def randomized_case(rng, n, m, truth):
    forced = [rng.choice((False, True)) for _ in range(n)]
    clauses = []
    for _ in range(m):
        names = rng.sample(range(1, n+1), 3)
        lits = [name if rng.choice((False, True)) else -name for name in names]
        if truth and not any(forced[abs(x)-1] == (x > 0) for x in lits):
            lits[0] = abs(lits[0]) if forced[abs(lits[0])-1] else -abs(lits[0])
        clauses.append(tuple(lits))
    if not truth:
        clauses.extend(force_unsat_cube())
    return tuple(clauses)


def assert_parse_rejects(blob):
    try:
        parse(blob)
    except (AssertionError, UnicodeError, ValueError):
        return
    raise AssertionError("malformed DIMACS unexpectedly accepted")


def sample_report():
    rng = random.Random(SEED)
    stats = {
        "seed": SEED, "exact_rational_assertions": 0,
        "root_count": 0, "sat_roots": 0, "unsat_roots": 0,
        "first_level_children": 0, "second_level_children": 0,
        "ordinary_encoded_bits_per_direction": 0,
        "events": 0, "row_entries_visited": 0,
        "max_live": 0, "max_relation": 0, "semantic_assertions": 0,
    }

    # Exact arithmetic: all valid finite row words are DP-Pareto dominated.
    for i in range(2400):
        K = rng.randint(1, 1000)
        mu = F(rng.randint(1, 9), rng.randint(2, 9))
        d = rng.randint(2, 16)
        delta = mu * F(rng.randint(0, 31), 2**d * 32)
        r = F(rng.randint(1, 32), 16)
        eta = F(rng.randint(0, 20), 20)
        rt, rs, valid = row_bounds(F(K), mu, delta, d, r, eta)
        pt, ps = dp_bounds(mu, delta, r, eta)
        assert pt <= rt and ps <= rs and valid
        stats["exact_rational_assertions"] += 3

    cofinal = []
    for K in [1, 2, 3, 5, 10, 20, 100, 1000, 10000, 10**6]:
        depth = ceil_log2_int(16 * K)
        delta = F(1, 64*K)
        rt, rs, valid = row_bounds(F(K), F(1), delta, depth, F(9, 8), F(1, 2))
        pt, ps = dp_bounds(F(1), delta, F(9, 8), F(1, 2))
        assert valid and rt <= F(9,8) and rs == F(1,2)
        assert (pt, ps) == (F(9,8), F(1,2))
        assert rt < C and rs < D
        stats["exact_rational_assertions"] += 6
        cofinal.append({"K": K, "depth": depth, "delta": str(delta),
                        "row_time": str(rt), "row_space": str(rs),
                        "direct_DP_time": str(pt), "direct_DP_space": str(ps)})

    caps = []
    for K in [2,3,10,20,100,1000,10000]:
        cand = [(cap, d) for d in range(2, 72)
                if (cap := sup_width_cap(K,d)) is not None and cap > 0]
        cap, best_d = max(cand)
        assert cap < F(41,200*(K-1))
        stats["exact_rational_assertions"] += 1
        caps.append({"K": K, "best_depth": best_d,
                     "delta_supremum": str(cap),
                     "delta_supremum_float": float(cap),
                     "K_times_cap": float(K*cap)})

    # True ordinary SAT encodings, both labels, two actually serialized
    # levels. The second level is real Shannon restriction, not a proxy.
    easy = [
        (3, ((1,2,3),)),                # SAT
        (3, force_unsat_cube()),        # UNSAT
        (3, ((1,),(-1,))),             # UNSAT and shared-variable control
        (3, ((-1,2),(1,),(-2,))),      # Horn UNSAT
        (3, ((1,-2),(-1,),(2,))),      # dual Horn UNSAT
        (4, ((1,2),(-1,-2),(-2,3),(2,-3),(-3,4),(3,-4),(-4,-1),(4,1))),
    ]
    for i in range(48):
        n = 4 + i % 5
        easy.append((n, randomized_case(rng, n, 5+i%15, truth=(i%2 == 0))))
    for n, clauses in easy:
        root_encoded = serialize(n, clauses)
        nr, root = parse(root_encoded)
        assert nr == n and root == clauses
        root_truth = exact_sat(n, root)
        got = dp_scoped(events_all_open(n, root), stats)
        assert got == root_truth
        stats["semantic_assertions"] += 2
        stats["root_count"] += 1
        stats["sat_roots" if root_truth else "unsat_roots"] += 1
        stats["ordinary_encoded_bits_per_direction"] += len(root_encoded) * 8
        grandchildren = []
        for b in (False, True):
            one = restrict(root, 1, b)
            payload1 = serialize(n, one)
            _, read1 = parse(payload1)
            assert read1 == one
            first_truth = exact_sat(n, read1)
            assert dp_scoped(events_all_open(n, read1), stats) == first_truth
            stats["semantic_assertions"] += 2
            stats["first_level_children"] += 1
            stats["ordinary_encoded_bits_per_direction"] += 8*len(payload1)
            second_labels = []
            for c in (False, True):
                two = restrict(read1, 2, c)
                payload2 = serialize(n, two)
                _, read2 = parse(payload2)
                assert read2 == two
                child_truth = exact_sat(n, read2)
                assert dp_scoped(events_all_open(n, read2), stats) == child_truth
                stats["semantic_assertions"] += 2
                stats["second_level_children"] += 1
                stats["ordinary_encoded_bits_per_direction"] += 8*len(payload2)
                second_labels.append(child_truth)
                grandchildren.append(child_truth)
            assert first_truth == any(second_labels)
            stats["semantic_assertions"] += 1
        assert root_truth == any(grandchildren)
        stats["semantic_assertions"] += 1

    assert exact_sat(1, ((1,),)) and exact_sat(1, ((-1,),))
    assert not exact_sat(1, ((1,),(-1,)))
    assert_parse_rejects(b"p cnf 2 1\n3 0\n")
    assert_parse_rejects(b"p cnf 2 2\n1 0\n")
    for malformed in [
        [("CLOSE",1)],
        [("OPEN",1),("OPEN",1),("CLOSE",1)],
        [("OPEN",1),("CLAUSE",(2,)),("CLOSE",1)],
    ]:
        try:
            dp_scoped(malformed, {"events":0,"row_entries_visited":0,"max_live":0,"max_relation":0})
        except AssertionError:
            pass
        else:
            raise AssertionError("malformed scoped event accepted")
    stats["semantic_assertions"] += 8
    assert stats["sat_roots"] >= 20 and stats["unsat_roots"] >= 20
    assert stats["first_level_children"] == 2*stats["root_count"]
    assert stats["second_level_children"] == 4*stats["root_count"]

    return {
        "identifier": "ARC-DP-DOMINANCE167", "status": "COMPUTATIONAL", "seed": SEED,
        "normalizer_exists": False,
        "flmv_tm_trace_measured": False,
        "source": "Standalone deterministic Python standard library",
        "c_star": str(C), "d_star": str(D),
        "cofinal_conditional_certificates": cofinal,
        "cofinal_width_suprema": caps,
        "counts": stats,
        "notes": "Direct on-the-fly exact frontier DP Pareto-dominates the declared fused row-envelope; all proved machine bounds are conditional on a real paid normalizer. Exhaustive truth-table calls validate finite SAT controls, not computational lower bounds."
    }

if __name__ == "__main__":
    result = sample_report()
    output = Path(__file__).with_name("2026-10-25_0425_ARC_DP_DOMINANCE167_results.json")
    output.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print(json.dumps({"counts":result["counts"], "cofinal_width_suprema":result["cofinal_width_suprema"]}, indent=2))
    print(f"saved {output}")
