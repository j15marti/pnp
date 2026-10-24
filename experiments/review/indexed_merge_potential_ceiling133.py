#!/usr/bin/env python3
"""INDEXED-MERGE-POTENTIAL-CEILING133 finite red-team audit.

Compares a source-recognized indexed two-pointer decision with one-level
ordinary pinned-child enumeration on the same J_q(A,B) proper-3CNF inputs.
It also evaluates the exact telescoping ceiling for any post-acquisition
potential with bounded decrease per charged bit operation.

This is a finite implementation audit plus exact finite identities.  It is
not an all-input ARC contraction or an unrestricted SAT lower bound.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from itertools import product
from math import comb, isqrt, log2
import hashlib
import json


Event = tuple[str, object]


def scan(events: tuple[Event, ...]):
    active: set[int] = set()
    opened: set[int] = set()
    cuts = [tuple()]
    clauses: list[tuple[int, int, int]] = []
    width = 0
    for op, arg in events:
        if op == "O":
            v = int(arg)
            assert v > 0 and v not in opened
            opened.add(v)
            active.add(v)
        elif op == "C":
            clause = tuple(arg)
            assert len(clause) == 3 and len({abs(x) for x in clause}) == 3
            assert all(abs(x) in active for x in clause)
            clauses.append(clause)
        elif op == "D":
            v = int(arg)
            assert v in active
            active.remove(v)
        else:
            raise AssertionError(op)
        cuts.append(tuple(sorted(active)))
        width = max(width, len(active))
    assert not active
    return cuts, width, clauses, len(opened)


def build_stream(clauses):
    first, last = {}, {}
    for i, clause in enumerate(clauses):
        for lit in clause:
            v = abs(lit)
            first.setdefault(v, i)
            last[v] = i
    out: list[Event] = []
    for i, clause in enumerate(clauses):
        for v in sorted(v for v in first if first[v] == i):
            out.append(("O", v))
        out.append(("C", tuple(clause)))
        for v in sorted((v for v in last if last[v] == i), reverse=True):
            out.append(("D", v))
    ans = tuple(out)
    scan(ans)
    return ans


def encode_bits(events):
    _, _, clauses, n = scan(events)
    m = len(clauses)
    word = (64 * (n + m + 1) - 1).bit_length()
    return (2 + 4 * n + 4 * m) * word


def ordinary_bits(events):
    """Independent ordinary-CNF serialization used by the target decider."""
    _, _, clauses, n = scan(events)
    m = len(clauses)
    word = (64 * (n + m + 1) - 1).bit_length()
    return (4 * m + 2) * word


def dpll(clauses):
    def go(cs):
        while True:
            if not cs:
                return True
            if any(not c for c in cs):
                return False
            unit = next((c[0] for c in cs if len(c) == 1), None)
            if unit is None:
                break
            cs = tuple(tuple(z for z in c if z != -unit)
                       for c in cs if unit not in c)
        lit = cs[0][0]
        for chosen in (lit, -lit):
            rem = tuple(tuple(z for z in c if z != -chosen)
                        for c in cs if chosen not in c)
            if go(rem):
                return True
        return False
    return go(tuple(map(tuple, clauses)))


def pin(out, v, bit, next_id):
    a, b = next_id, next_id + 1
    out.extend((("O", a), ("O", b)))
    z = v if bit else -v
    for sa, sb in product((1, -1), repeat=2):
        out.append(("C", (z, sa * a, sb * b)))
    out.extend((("D", b), ("D", a)))
    return next_id + 2


def make_child(block, left, right, left_bits, right_bits):
    mapping: dict[int, int] = {}
    out: list[Event] = []
    next_id = 1
    alive: set[int] = set()
    right_set = set(right)

    def local(v):
        nonlocal next_id
        if v not in mapping:
            mapping[v] = next_id
            next_id += 1
        return mapping[v]

    for v in left:
        out.append(("O", local(v)))
        alive.add(v)
    for v, bit in zip(left, left_bits):
        next_id = pin(out, local(v), bit, next_id)
    for op, arg in block:
        if op == "O":
            v = int(arg)
            out.append(("O", local(v)))
            alive.add(v)
        elif op == "C":
            out.append(("C", tuple(local(abs(x)) if x > 0
                                    else -local(abs(x)) for x in arg)))
        else:
            v = int(arg)
            if v not in right_set:
                out.append(("D", local(v)))
                alive.remove(v)
    assert alive == right_set
    for v, bit in zip(right, right_bits):
        next_id = pin(out, local(v), bit, next_id)
    for v in sorted(right, reverse=True):
        out.append(("D", local(v)))
    child = tuple(out)
    scan(child)
    return child


def optimal_union_path(cuts, block_max):
    length = len(cuts) - 1
    inf = 10**100
    dp = [inf] * (length + 1)
    prev = [-1] * (length + 1)
    dp[0] = 0
    for j in range(1, length + 1):
        for i in range(max(0, j - block_max), j):
            edge = 1 << len(set(cuts[i]) | set(cuts[j]))
            val = dp[i] + edge
            if val < dp[j]:
                dp[j], prev[j] = val, i
    path = [length]
    while path[-1]:
        path.append(prev[path[-1]])
    path.reverse()
    return tuple(path), dp[length]


@dataclass
class ChildStats:
    generated_pairs: int = 0
    consistent_pairs: int = 0
    incompatible_pairs: int = 0
    solver_calls: int = 0
    cache_hits: int = 0
    generated_tagged_scoped_bits: int = 0
    peak_tagged_scoped_bits: int = 0
    generated_ordinary_child_bits: int = 0
    peak_ordinary_child_bits: int = 0
    peak_live_source_width: int = 0
    planner_edges_examined: int = 0


def scoped_one_level(events):
    cuts, width, _, _ = scan(events)
    bmax = max(1, isqrt(len(events)))
    path, union_cost = optimal_union_path(cuts, bmax)
    stats = ChildStats(peak_live_source_width=width)
    stats.planner_edges_examined = sum(min(j, bmax)
                                       for j in range(1, len(events) + 1))
    memo = {}
    reachable = {()}
    for low, high in zip(path, path[1:]):
        left, right = cuts[low], cuts[high]
        common = set(left) & set(right)
        future = set()
        for ua in reachable:
            for vb in product((0, 1), repeat=len(right)):
                stats.generated_pairs += 1
                if any(ua[left.index(v)] != vb[right.index(v)] for v in common):
                    stats.incompatible_pairs += 1
                    continue
                stats.consistent_pairs += 1
                child = make_child(events[low:high], left, right, ua, vb)
                tagged_bits = encode_bits(child)
                ordinary = ordinary_bits(child)
                stats.generated_tagged_scoped_bits += tagged_bits
                stats.peak_tagged_scoped_bits = max(
                    stats.peak_tagged_scoped_bits, tagged_bits)
                stats.generated_ordinary_child_bits += ordinary
                stats.peak_ordinary_child_bits = max(
                    stats.peak_ordinary_child_bits, ordinary)
                if child in memo:
                    stats.cache_hits += 1
                    sat = memo[child]
                else:
                    stats.solver_calls += 1
                    sat = dpll(scan(child)[2])
                    memo[child] = sat
                if sat:
                    future.add(tuple(vb))
        reachable = future
        if not reachable:
            return False, path, union_cost, stats
    return () in reachable, path, union_cost, stats


def pin_clauses(lit, a, b):
    return [(lit, sa * a, sb * b) for sa, sb in product((1, -1), repeat=2)]


def jq_formula(q, A, B):
    assert q % 2 == 0 and len(A) == len(B) == q // 2
    assert tuple(sorted(A)) == tuple(A) and tuple(sorted(B)) == tuple(B)
    clauses = []
    block = 0
    for positive, names in ((True, A), (False, B)):
        for name in names:
            a, b = q + 2 * block + 1, q + 2 * block + 2
            clauses.extend(pin_clauses(name if positive else -name, a, b))
            block += 1
    assert block == q
    return clauses


def jq_source_bits(q):
    """Role-4 fixed ordinary encoding: declared n=3q even if names repeat."""
    w = (64 * (7 * q + 1) - 1).bit_length()
    return (16 * q + 2) * w


def merge_trace(q, A, B):
    """Sorted intersection with a transparent post-acquisition bit ledger.

    The source has already been fully syntax-checked once, but its read-only
    bits were not retained.  Each comparison rereads two w-bit identifier
    fields.  The charged upper-bound subroutine scans every name bit, uses
    fixed-width address and pointer registers, and charges unchanged writes.
    """
    r = q // 2
    w = (64 * (7 * q + 1) - 1).bit_length()
    b = max(1, (r + 1).bit_length())
    i = j = 0
    old_a = old_b = 0
    data_flips = 0
    comparisons = 0
    increments = 0
    found = None
    while i < r and j < r:
        a, bb = A[i], B[j]
        data_flips += (old_a ^ a).bit_count() + (old_b ^ bb).bit_count()
        old_a, old_b = a, bb
        comparisons += 1
        if a == bb:
            found = a
            break
        if a < bb:
            old_i = i
            i += 1
            data_flips += (old_i ^ i).bit_count()
        else:
            old_j = j
            j += 1
            data_flips += (old_j ^ j).bit_count()
        increments += 1
    # Explicit upper-bound schedule per comparison.  These categories are
    # disjoint by declaration; unchanged register writes are included.
    source_reads = 2 * comparisons * w
    workspace_reads = comparisons * (2 * w + 2 * b + 8)
    workspace_writes = comparisons * (2 * w + 2 * b + 8)
    control_address_selection = comparisons * (12 * w + 12 * b + 32) + 1
    primitive_work_upper = (source_reads + workspace_reads +
                            workspace_writes + control_address_selection)
    peak_live_bits_upper = 4 * w + 2 * b + 24
    return {
        "label": found is None,
        "collision": found,
        "comparisons": comparisons,
        "pointer_increments": increments,
        "word_bits": w,
        "pointer_bits": b,
        "source_bit_reads": source_reads,
        "workspace_bit_reads_upper": workspace_reads,
        "workspace_bit_writes_upper_including_unchanged": workspace_writes,
        "control_address_selection_upper": control_address_selection,
        "primitive_bit_work_upper": primitive_work_upper,
        "tracked_data_register_flips": data_flips,
        "complete_state_flips_interval": [data_flips, primitive_work_upper],
        "peak_live_writable_bits_upper": peak_live_bits_upper,
        "cumulative_bit_time_upper": primitive_work_upper * peak_live_bits_upper,
    }


def cases(q):
    r = q // 2
    odds = tuple(range(1, q + 1, 2))
    evens = tuple(range(2, q + 1, 2))
    assert len(odds) == len(evens) == r
    # Same metadata: SAT with a late no-collision scan; UNSAT with immediate
    # collision and a broad shared-name frontier; UNSAT with one late collision.
    late_b = tuple(list(evens[:-1]) + [odds[-1]]) if r > 1 else odds
    return (
        ("SAT_complements_interleaved", odds, evens),
        ("UNSAT_identical_halves", odds, odds),
        ("UNSAT_single_late_collision", odds, tuple(sorted(late_b))),
    )


def main():
    rows = []
    checks = 0
    for q in (2, 4, 6, 8, 10):
        for name, A, B in cases(q):
            clauses = jq_formula(q, A, B)
            events = build_stream(clauses)
            expected = not bool(set(A) & set(B))
            assert dpll(clauses) is expected
            checks += 1
            direct = merge_trace(q, A, B)
            assert direct["label"] is expected
            assert direct["comparisons"] <= q - 1
            checks += 2
            scoped_label, path, union_cost, stats = scoped_one_level(events)
            assert scoped_label is expected
            checks += 1
            rank = comb(q, q // 2)
            # Telescoping test for L=1.  Raw rank is too large for the actual
            # fast path from q=10 onward in this conservative accounting only
            # at larger q, so record rather than overclaim finite separation.
            rows.append({
                "q": q,
                "case": name,
                "A": A,
                "B": B,
                "label": expected,
                "source_bits": jq_source_bits(q),
                "source_events": len(events),
                "source_width": scan(events)[1],
                "compatibility_matrix_rank": rank,
                "log2_rank": log2(rank),
                "direct_post_acquisition": direct,
                "scoped_union_path": path,
                "scoped_union_assignment_cost": union_cost,
                "scoped_one_level": asdict(stats),
                "rank_over_direct_work_upper": rank / direct["primitive_bit_work_upper"],
            })

    # Symbolic finite checks: R_q eventually outruns every sampled polynomial
    # q^d, while log R_q remains linear.  This illustrates the theorem only;
    # the asymptotic fact is proved analytically in the report.
    growth = []
    for degree in (1, 2, 3, 4, 6):
        first = next(q for q in range(2, 514, 2)
                     if comb(q, q // 2) > q ** degree)
        growth.append({"degree": degree, "first_even_q_rank_gt_q_to_d": first})
        checks += 1

    result = {
        "run_id": "INDEXED-MERGE-POTENTIAL-CEILING133",
        "status": "COMPUTATIONAL finite audit; exact symbolic lemmas in report",
        "checks": checks,
        "rows": rows,
        "rank_vs_polynomial_growth": growth,
        "ledger_basis": {
            "work": "one declared source/work bit read, bit write, or control/address/selection bit step",
            "space": "one simultaneously live writable bit; read-only source excluded",
            "writes": "unchanged writes charged",
            "flips": "data-register flips exact; complete-state flips reported as a rigorous interval",
            "bit_time": "conservative work times peak-live-bits upper bound",
        },
        "limitations": [
            "The indexed path is a promise-family upper bound after paid grammar validation, not an all-input ARC edge.",
            "The scoped path is a specified eager ordinary-child strategy, not mandatory for arbitrary SAT deciders.",
            "Finite measurements do not establish asymptotic SAT hardness.",
        ],
    }
    prehash = json.dumps(result, sort_keys=True, separators=(",", ":"))
    result["prehash_sha256"] = hashlib.sha256(prehash.encode()).hexdigest()
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
