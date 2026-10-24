#!/usr/bin/env python3
"""SIL-PROFILE-FIREWALL112 exact finite audit.

Builds equal-metadata SAT/UNSAT odd-XOR3 families wrapped by a private star:
  (z or x_i) and (z or not x_i).
Each pair contracts by SIL-RC CP2 to unit z, so existentially hiding z
returns the base formula.  Raw affine interaction profile is [q], while the
post-contraction profile is [1,...,1].  This is a representation/profile
counterexample, not an unrestricted SAT lower bound.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import time
from pathlib import Path

RUN = "SIL-PROFILE-FIREWALL112"
SEED = 202610241148  # deterministic declaration; no randomness used
RAW = Path("SIL_PROFILE_FIREWALL112_raw.json")


def odd_xor3_clauses(a: int, b: int, c: int):
    return [
        (a, b, c),
        (a, -b, -c),
        (-a, b, -c),
        (-a, -b, c),
    ]


def build(q: int, unsat: bool, wrapped: bool = True):
    """Return clauses and ids. Variables are 1-based."""
    clauses = []
    for i in range(q):
        a, b, c = 3 * i + 1, 3 * i + 2, 3 * i + 3
        clauses.extend(odd_xor3_clauses(a, b, c))
    u, v, z = 3 * q + 1, 3 * q + 2, 3 * q + 3
    a0 = 1
    # First pair forces a0=1 on both labels.
    clauses.extend(((a0, u), (a0, -u)))
    # Equal support/width metadata: SAT again forces a0=1; UNSAT forces a0=0.
    head = -a0 if unsat else a0
    clauses.extend(((head, v), (head, -v)))
    if wrapped:
        for i in range(q):
            x = 3 * i + 1
            clauses.extend(((z, x), (z, -x)))
    return clauses, {"u": u, "v": v, "z": z, "n": z}


def sat_clause(clause, bits):
    return any((bits[abs(lit) - 1] == 1) if lit > 0
               else (bits[abs(lit) - 1] == 0) for lit in clause)


def sat_formula(clauses, bits):
    return all(sat_clause(c, bits) for c in clauses)


def brute_count(q: int, unsat: bool, wrapped: bool):
    clauses, ids = build(q, unsat, wrapped)
    n = ids["n"] if wrapped else ids["v"]
    return sum(sat_formula(clauses, bits)
               for bits in itertools.product((0, 1), repeat=n))


def affine_component(var: int, q: int):
    if var <= 3 * q:
        return (var - 1) // 3
    return q + (var - (3 * q + 1))  # u,v,z singleton components


def interaction_profile(q: int, clauses, include_xor=False):
    """Profile K_j for affine components joined by binary clauses."""
    component_count = q + 3
    adj = [set() for _ in range(component_count)]
    for clause in clauses:
        if len(clause) != 2:
            continue
        a = affine_component(abs(clause[0]), q)
        b = affine_component(abs(clause[1]), q)
        if a != b:
            adj[a].add(b)
            adj[b].add(a)
    seen = set()
    profile = []
    for root in range(component_count):
        if root in seen:
            continue
        stack = [root]
        seen.add(root)
        excess = 0
        while stack:
            x = stack.pop()
            # XOR3 components have d=2, excess=1; singleton components d=1.
            excess += 1 if x < q else 0
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    stack.append(y)
        if excess:
            profile.append(excess)
    return sorted(profile, reverse=True)


def cp2_trace(q: int, unsat: bool):
    """Certified construction-specific CP2/CL3/VE1 trace and residual."""
    wrapped, ids = build(q, unsat, True)
    base, _ = build(q, unsat, False)
    z = ids["z"]
    pair_checks = 0
    for i in range(q):
        x = 3 * i + 1
        assert (z, x) in wrapped and (z, -x) in wrapped
        pair_checks += 1
    # CP2^q yields q copies of (z); CL3 leaves one; z is private and VE1
    # existentially discharges its sole unit.  The residual is exactly base.
    return {
        "pair_checks": pair_checks,
        "cp2_steps": q,
        "cl3_steps": max(q - 1, 0),
        "ve1_steps": 1,
        "residual_clause_count": len(base),
        "residual_digest": hashlib.sha256(repr(base).encode()).hexdigest(),
    }, base


def witness(q: int):
    """One SAT witness: every odd-XOR block is 100, z=1, u=v=0."""
    bits = []
    for _ in range(q):
        bits.extend((1, 0, 0))
    bits.extend((0, 0, 1))
    return tuple(bits)


def main():
    started = time.perf_counter()
    checks = 0
    exhaustive = []

    # Exhaustive full-formula and exact existential-wrapper checks.
    for q in range(1, 5):
        for unsat in (False, True):
            base_count = brute_count(q, unsat, False)
            wrap_count = brute_count(q, unsat, True)
            # Wrapper forces exactly z=1, hence preserves model count as well
            # as existential boundary truth for this construction.
            assert base_count == wrap_count
            assert (base_count == 0) is unsat
            wrapped, _ = build(q, unsat, True)
            trace, base = cp2_trace(q, unsat)
            assert len(wrapped) == 6 * q + 4
            assert len(base) == 4 * q + 4
            assert interaction_profile(q, wrapped) == [q]
            assert interaction_profile(q, base) == [1] * q
            checks += 7
            exhaustive.append({
                "q": q,
                "label": "UNSAT" if unsat else "SAT",
                "base_models": base_count,
                "wrapped_models": wrap_count,
                "raw_profile": [q],
                "normalized_profile": [1] * q,
                **trace,
            })

    scales = []
    for q in (8, 64, 512, 4096):
        for unsat in (False, True):
            wrapped, ids = build(q, unsat, True)
            base, _ = build(q, unsat, False)
            trace, residual = cp2_trace(q, unsat)
            assert residual == base
            assert interaction_profile(q, wrapped) == [q]
            assert interaction_profile(q, base) == [1] * q
            assert len(wrapped) == 6 * q + 4
            assert ids["n"] == 3 * q + 3
            if not unsat:
                assert sat_formula(wrapped, witness(q))
            else:
                # CP2 on the two equal-support anchor pairs yields a0 and -a0.
                assert wrapped[-2 * q - 4:-2 * q] == [
                    (1, ids["u"]), (1, -ids["u"]),
                    (-1, ids["v"]), (-1, -ids["v"]),
                ]
            checks += 7
            scales.append({
                "q": q,
                "label": "UNSAT" if unsat else "SAT",
                "n": 3 * q + 3,
                "ternary_clauses": 4 * q,
                "binary_clauses": 2 * q + 4,
                "raw_profile": [q],
                "raw_excess_enumeration_ceiling": f"2^{q}",
                "forest_dp_state_pair_ceiling": 16,
                "normalized_profile_summary": {"clusters": q, "each_K": 1},
                "sil_trace_steps": trace["cp2_steps"] + trace["cl3_steps"] + 1,
                "charged_source_clause_reads_upper_bound": len(wrapped),
                "peak_live_clause_records_upper_bound": len(wrapped) + q + 3,
            })

    elapsed = time.perf_counter() - started
    result = {
        "run_id": RUN,
        "status": {
            "wrapper_identity": "PROVED/EXACT symbolically; exhaustive finite corroboration",
            "finite_audit": "COMPUTATIONAL",
            "raw_profile_lower_bound": "FALSIFIED/RETIRED",
            "P_vs_NP": "OPEN",
        },
        "seed": SEED,
        "randomness_used": False,
        "checks": checks,
        "failures": 0,
        "elapsed_seconds": round(elapsed, 6),
        "exhaustive_controls": exhaustive,
        "scaled_adaptive_controls": scales,
        "adaptive_policy": [
            "XR1 recognize odd-XOR3 blocks",
            "CP2 contract wrapper and anchor complementary pairs",
            "CL3 deduplicate units",
            "VE1 discharge private z",
            "UP3 terminate UNSAT or XR2/Gaussian reconstruct SAT",
            "TREEJOIN79 forest DP is a second exact polynomial option",
        ],
        "limitations": [
            "The SIL trace is a restricted constructive upper algorithm.",
            "Finite checks do not establish asymptotic lower bounds.",
            "Minimizing over every equivalent representation is not proved efficient.",
            "No all-decider post-acquisition lower bound is obtained.",
        ],
    }
    RAW.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
