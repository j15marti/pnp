#!/usr/bin/env python3
"""Finite audit for ARC-ADAPTIVE-CONJUNCTION-TRACE172.

Every individual run is deterministic and intended to finish in well under
30 seconds.  The experiment checks:
  * exhaustive two-level monotonicity for all 256 boundary supports and a
    fixed library of actual conjunctive restrictions;
  * four state-dependent policies on serialized ordinary proper-3CNF sources;
  * the sharp d+2 fixed-policy trace family;
  * the exact finite collision count for the source-to-trace map; and
  * a nonconjunctive replacement control that escapes the theorem's scope.
"""

from __future__ import annotations

import hashlib
import json
import math
import time
from collections import Counter
from pathlib import Path

RUN_ID = "ARC-ADAPTIVE-CONJUNCTION-TRACE172"
OUT = Path(__file__).with_name(
    "2026-10-25_1148_ARC_ADAPTIVE_CONJUNCTION_TRACE172_raw.json"
)


def word_satisfies_clause(word: int, clause: tuple[int, ...]) -> bool:
    for lit in clause:
        bit = (word >> (abs(lit) - 1)) & 1
        if (lit > 0 and bit) or (lit < 0 and not bit):
            return True
    return False


def support_formula(mask: int) -> list[tuple[int, int, int]]:
    """Proper 3CNF on x1,x2,x3 whose boundary support is exactly mask."""
    clauses: list[tuple[int, int, int]] = []
    for word in range(8):
        if (mask >> word) & 1:
            continue
        # This clause is false on exactly this word.
        clauses.append(tuple((-(i + 1) if (word >> i) & 1 else i + 1)
                             for i in range(3)))
    return clauses


def pin_gadget(lit: int, next_var: int) -> tuple[list[tuple[int, int, int]], int]:
    a, b = next_var, next_var + 1
    clauses = [
        (lit, a, b),
        (lit, a, -b),
        (lit, -a, b),
        (lit, -a, -b),
    ]
    return clauses, next_var + 2


def serialize(clauses: list[tuple[int, ...]], nvars: int) -> str:
    body = "\n".join(" ".join(map(str, c)) + " 0" for c in clauses)
    return f"p cnf {nvars} {len(clauses)}\n{body}\n"


def parse(text: str) -> tuple[list[tuple[int, ...]], int]:
    clauses: list[tuple[int, ...]] = []
    nvars = 0
    declared = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p "):
            _, kind, nv, nc = line.split()
            assert kind == "cnf"
            nvars, declared = int(nv), int(nc)
            continue
        vals = tuple(map(int, line.split()))
        assert vals[-1] == 0
        clause = vals[:-1]
        assert len(clause) == 3
        assert len({abs(x) for x in clause}) == 3
        clauses.append(clause)
    assert declared == len(clauses)
    assert all(1 <= abs(x) <= nvars for c in clauses for x in c)
    return clauses, nvars


def simplify(clauses: tuple[tuple[int, ...], ...], var: int, val: bool):
    out = []
    for c in clauses:
        satisfied = any(abs(l) == var and ((l > 0) == val) for l in c)
        if satisfied:
            continue
        nc = tuple(l for l in c if abs(l) != var)
        if not nc:
            return None
        out.append(nc)
    return tuple(out)


def dpll(clauses: list[tuple[int, ...]], nvars: int) -> bool:
    def rec(cs: tuple[tuple[int, ...], ...]) -> bool:
        if not cs:
            return True
        units = [c[0] for c in cs if len(c) == 1]
        if units:
            lit = units[0]
            nxt = simplify(cs, abs(lit), lit > 0)
            return False if nxt is None else rec(nxt)
        var = abs(min(cs, key=len)[0])
        for val in (False, True):
            nxt = simplify(cs, var, val)
            if nxt is not None and rec(nxt):
                return True
        return False

    assert all(abs(l) <= nvars for c in clauses for l in c)
    return rec(tuple(tuple(c) for c in clauses))


def boundary_support(clauses: list[tuple[int, ...]]) -> int:
    mask = 0
    for word in range(8):
        if all(word_satisfies_clause(word, c) for c in clauses
               if all(abs(l) <= 3 for l in c)):
            # Pin gadgets have auxiliaries but semantically force their boundary
            # literal.  Directly test the boundary literal appearing in each.
            forced = []
            for i in range(0, len(clauses)):
                c = clauses[i]
                b_lits = [l for l in c if abs(l) <= 3]
                if len(b_lits) == 1 and any(abs(l) > 3 for l in c):
                    forced.append(b_lits[0])
            if all(word_satisfies_clause(word, (lit,)) for lit in forced):
                mask |= 1 << word
    return mask


def choose_lit(policy: str, mask: int, clauses, step: int, prev: int) -> int:
    if policy == "syntax_hash":
        payload = serialize(clauses, 3 + 2 * step).encode()
        h = int.from_bytes(hashlib.sha256(payload).digest()[:4], "big")
        var = 1 + ((h + step) % 3)
        return var if ((h >> (step % 16)) & 1) else -var
    if policy == "label_adaptive":
        var = 1 + (step % 3)
        return var if prev else -var
    if policy == "support_balance":
        best = None
        for var in range(1, 4):
            pos = sum((mask >> w) & 1 for w in range(8) if (w >> (var - 1)) & 1)
            neg = sum((mask >> w) & 1 for w in range(8) if not ((w >> (var - 1)) & 1))
            score = (abs(pos - neg), var)
            if best is None or score < best[0]:
                best = (score, var, pos, neg)
        _, var, pos, neg = best
        return var if pos <= neg else -var
    if policy == "cache_replay":
        var = 1 + ((mask.bit_count() + step + prev) % 3)
        return var if ((mask ^ (mask >> 3) ^ step) & 1) else -var
    raise ValueError(policy)


def restrict_mask(mask: int, lit: int) -> int:
    out = 0
    for w in range(8):
        if (mask >> w) & 1 and word_satisfies_clause(w, (lit,)):
            out |= 1 << w
    return out


def actual_policy_audit(depth: int = 4):
    checks = 0
    traces = Counter()
    policies = ["syntax_hash", "label_adaptive", "support_balance", "cache_replay"]
    sat_roots = unsat_roots = 0
    for source in range(256):
        base = support_formula(source)
        root_text = serialize(base, 3)
        parsed, nv = parse(root_text)
        root_sat = dpll(parsed, nv)
        checks += 4
        assert root_sat == bool(source)
        sat_roots += int(root_sat)
        unsat_roots += int(not root_sat)
        for policy in policies:
            clauses = list(base)
            nvars = 3
            mask = source
            prev = int(root_sat)
            labels = [prev]
            for step in range(depth):
                lit = choose_lit(policy, mask, clauses, step, prev)
                gadget, nvars = pin_gadget(lit, nvars + 1)
                clauses.extend(gadget)
                text = serialize(clauses, nvars)
                reparsed, nv2 = parse(text)
                got = int(dpll(reparsed, nv2))
                mask = restrict_mask(mask, lit)
                expected = int(bool(mask))
                assert got == expected
                assert got <= prev
                labels.append(got)
                prev = got
                checks += 7
            traces[(policy, "".join(map(str, labels)))] += 1
    return checks, traces, sat_roots, unsat_roots


def exhaustive_two_level():
    # All literal halfspaces, all eight proper 3-clauses, true, and false.
    filters = []
    for lit in (-3, -2, -1, 1, 2, 3):
        filters.append(sum(1 << w for w in range(8)
                           if word_satisfies_clause(w, (lit,))))
    for forbidden in range(8):
        clause = tuple((-(i + 1) if (forbidden >> i) & 1 else i + 1)
                       for i in range(3))
        filters.append(sum(1 << w for w in range(8)
                           if word_satisfies_clause(w, clause)))
    filters.extend([0, 255])
    checks = 0
    patterns = Counter()
    for source in range(256):
        v0 = int(bool(source))
        for q1 in filters:
            s1 = source & q1
            v1 = int(bool(s1))
            for q2 in filters:
                s2 = s1 & q2
                v2 = int(bool(s2))
                assert v0 >= v1 >= v2
                patterns[f"{v0}{v1}{v2}"] += 1
                checks += 3
    return checks, patterns, len(filters)


def sharp_and_collision(depth: int = 3):
    lits = [-1, -2, -3]  # require boundary word bits 000 in sequence
    trace_counts = Counter()
    checks = 0
    for source in range(256):
        mask = source
        labels = [int(bool(mask))]
        for lit in lits:
            mask = restrict_mask(mask, lit)
            labels.append(int(bool(mask)))
            checks += 2
        word = "".join(map(str, labels))
        assert "01" not in word
        trace_counts[word] += 1
    expected = {("1" * k) + ("0" * (depth + 1 - k))
                for k in range(depth + 2)}
    assert set(trace_counts) == expected
    collision = sum(n * n for n in trace_counts.values())
    cs_lower = math.ceil(256 * 256 / (depth + 2))
    assert collision >= cs_lower
    return checks, trace_counts, collision, cs_lower


def nonconjunctive_scope_control():
    unsat = support_formula(0)
    sat = [(1, 2, 3)]
    labels = [int(dpll(unsat, 3)), int(dpll(sat, 3))]
    assert labels == [0, 1]
    return labels, 2


def main():
    started = time.perf_counter()
    checks1, patterns, nfilters = exhaustive_two_level()
    checks2, traces, sat_roots, unsat_roots = actual_policy_audit()
    checks3, fibers, collision, cs_lower = sharp_and_collision()
    escape, checks4 = nonconjunctive_scope_control()
    elapsed = time.perf_counter() - started
    result = {
        "run_id": RUN_ID,
        "status": "COMPUTATIONAL",
        "seed": None,
        "chunking": "single deterministic chunk; designed for <30 seconds",
        "elapsed_seconds": round(elapsed, 6),
        "assertion_groups": checks1 + checks2 + checks3 + checks4,
        "exhaustive_two_level": {
            "source_supports": 256,
            "filter_library_size": nfilters,
            "ordered_filter_pairs_per_source": nfilters * nfilters,
            "label_patterns": dict(sorted(patterns.items())),
        },
        "ordinary_proper_3cnf_adaptive": {
            "source_supports": 256,
            "policies": 4,
            "depth": 4,
            "sat_roots": sat_roots,
            "unsat_roots": unsat_roots,
            "trace_counts": {f"{p}:{t}": n for (p, t), n in sorted(traces.items())},
        },
        "sharp_fixed_policy_depth3": {
            "fibers": dict(sorted(fibers.items())),
            "image_size": len(fibers),
            "ordered_collision_count": collision,
            "cauchy_schwarz_lower_bound": cs_lower,
        },
        "nonconjunctive_replacement_control": escape,
        "failures": 0,
        "interpretation": (
            "Finite logical audit only; not an FLMV step trace, an ARC "
            "contraction, or a lower bound."
        ),
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
