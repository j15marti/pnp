#!/usr/bin/env python3
"""LSPV-5/409 B3 identity-system quantifier control.

This finite checker models the decider-indexed identity proof system Q_A and a
trace-only unsound control on established cubic Tseitin strict 3-CNFs.  It is
not the historical R_mix341 checker and proves no complexity separation.
"""

from __future__ import annotations

import hashlib
import json
import math
import resource
import time
from pathlib import Path

OUT = Path("results/raw/review/2026-11-07_0455_LSPV5_B3_IDENTITY409.json")


def graphs() -> dict[str, tuple[int, list[tuple[int, int]]]]:
    k4 = (4, [(i, j) for i in range(4) for j in range(i + 1, 4)])
    k33 = (6, [(i, j) for i in range(3) for j in range(3, 6)])
    cube_edges = []
    for v in range(8):
        for bit in (1, 2, 4):
            w = v ^ bit
            if v < w:
                cube_edges.append((v, w))
    return {"K4": k4, "K3,3": k33, "cube": (8, cube_edges)}


def tseitin(nv: int, edges: list[tuple[int, int]], odd: bool) -> list[tuple[int, int, int]]:
    incident = [[] for _ in range(nv)]
    for idx, (u, v) in enumerate(edges, 1):
        incident[u].append(idx)
        incident[v].append(idx)
    assert all(len(es) == 3 for es in incident)
    clauses = []
    for v, es in enumerate(incident):
        charge = int(odd and v == 0)
        for assignment in range(8):
            if assignment.bit_count() % 2 == charge:
                continue
            clause = tuple(-edge if assignment >> i & 1 else edge
                           for i, edge in enumerate(es))
            assert len({abs(x) for x in clause}) == 3
            clauses.append(clause)
    assert len(clauses) == 4 * nv
    return clauses


def encode_dimacs(clauses: list[tuple[int, int, int]]) -> bytes:
    nvars = max(abs(x) for c in clauses for x in c)
    lines = [f"p cnf {nvars} {len(clauses)}"]
    lines.extend(" ".join(map(str, c)) + " 0" for c in clauses)
    return ("\n".join(lines) + "\n").encode()


def parse_dimacs(source: bytes) -> list[tuple[int, ...]] | None:
    try:
        lines = source.decode("ascii").splitlines()
        if not lines or len(lines[0].split()) != 4:
            return None
        p, kind, ns, ms = lines[0].split()
        if p != "p" or kind != "cnf":
            return None
        nvars, nclauses = int(ns), int(ms)
        clauses = []
        for line in lines[1:]:
            xs = [int(x) for x in line.split()]
            if not xs or xs[-1] != 0:
                return None
            clause = tuple(xs[:-1])
            if not clause or any(x == 0 or abs(x) > nvars for x in clause):
                return None
            clauses.append(clause)
        if len(clauses) != nclauses:
            return None
        return clauses
    except (UnicodeDecodeError, ValueError):
        return None


def model_count(source: bytes) -> int | None:
    clauses = parse_dimacs(source)
    if clauses is None:
        return None
    nvars = max(abs(x) for c in clauses for x in c)
    count = 0
    for assignment in range(1 << nvars):
        if all(any(((assignment >> (abs(lit) - 1)) & 1) == (lit > 0)
                   for lit in clause) for clause in clauses):
            count += 1
    return count


def q_accepts(source: bytes, proof: bytes) -> bool:
    """Finite Q_A: proof is source itself and A is exhaustive UNSAT."""
    return source == proof and model_count(source) == 0


def trace_only_accepts(program: str, source: bytes, trace: list[dict]) -> bool:
    digest = hashlib.sha256(source).hexdigest()
    return (program == "reject_all" and trace == [
        {"state": "start", "source_sha256": digest},
        {"state": "reject", "source_sha256": digest},
    ])


def finite_sources() -> list[dict]:
    rows = []
    for name, (nv, edges) in graphs().items():
        for odd in (False, True):
            clauses = tseitin(nv, edges, odd)
            source = encode_dimacs(clauses)
            models = model_count(source)
            expected = 0 if odd else 1 << (len(edges) - nv + 1)
            assert models == expected
            proof = source
            q_ok = q_accepts(source, proof)
            assert q_ok == odd
            trace = [
                {"state": "start", "source_sha256": hashlib.sha256(source).hexdigest()},
                {"state": "reject", "source_sha256": hashlib.sha256(source).hexdigest()},
            ]
            trace_ok = trace_only_accepts("reject_all", source, trace)
            assert trace_ok
            rows.append({
                "graph": name,
                "vertices": nv,
                "edges": len(edges),
                "charge": "odd" if odd else "even",
                "variables": len(edges),
                "clauses": len(clauses),
                "proper_strict_3cnf": all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in clauses),
                "models": models,
                "encoded_bytes": len(source),
                "encoded_bits_N": 8 * len(source),
                "source_sha256": hashlib.sha256(source).hexdigest(),
                "Q_A_identity_proof_bits": 8 * len(proof),
                "Q_A_accepts": q_ok,
                "reject_all_trace_accepts": trace_ok,
            })
    return rows


def padded_clock_controls() -> list[dict]:
    nv, edges = graphs()["K4"]
    core = tseitin(nv, edges, True)
    rows = []
    for padding in range(9):
        clauses = list(core)
        next_var = len(edges) + 1
        for i in range(padding):
            a = next_var + 3 * i
            clauses.append((a, a + 1, a + 2))
        source = encode_dimacs(clauses)
        # The unchanged odd-Tseitin core is already UNSAT.  Do not spend
        # exponential host time enumerating assignments to irrelevant padding.
        assert clauses[:len(core)] == core
        nbits = 8 * len(source)
        fast_upper = 4 * nv - 1
        # Existing [P2-B6] clock control: exact forced prefix 2^N.
        clock_nodes = (1 << nbits) + fast_upper + 1
        margins = {str(k): nbits - k * math.log2(nbits + 1) for k in range(1, 5)}
        assert all(v > 0 for v in margins.values())
        rows.append({
            "padding_clauses": padding,
            "encoded_bits_N": nbits,
            "Q_A_identity_bits": nbits,
            "declared_mixed_fast_upper": fast_upper,
            "R_clock_exact_paid_nodes_decimal": str(clock_nodes),
            "R_clock_log2_lower": nbits,
            "log2_margin_over_Nplus1_to_k": margins,
        })
    return rows


def negative_controls(rows: list[dict]) -> dict[str, bool]:
    nv, edges = graphs()["K4"]
    odd = encode_dimacs(tseitin(nv, edges, True))
    even = encode_dimacs(tseitin(nv, edges, False))
    digest = hashlib.sha256(even).hexdigest()
    good_trace = [{"state": "start", "source_sha256": digest},
                  {"state": "reject", "source_sha256": digest}]
    out = {
        "identity_source_mismatch_rejected": not q_accepts(odd, even),
        "identity_SAT_source_rejected": not q_accepts(even, even),
        "identity_malformed_rejected": not q_accepts(b"p cnf bad\n", b"p cnf bad\n"),
        "trace_only_unsound_on_SAT_witnessed": trace_only_accepts("reject_all", even, good_trace) and model_count(even) > 0,
        "trace_wrong_digest_rejected": not trace_only_accepts("reject_all", odd, good_trace),
        "trace_truncation_rejected": not trace_only_accepts("reject_all", even, good_trace[:1]),
        "unknown_program_rejected": not trace_only_accepts("oracle", even, good_trace),
        "odd_sources_Q_accept_even_sources_Q_reject": all(r["Q_A_accepts"] == (r["charge"] == "odd") for r in rows),
    }
    out["all_controls_pass"] = all(out.values())
    return out


def main() -> None:
    started = time.perf_counter()
    sources = finite_sources()
    clock = padded_clock_controls()
    negatives = negative_controls(sources)
    assert negatives["all_controls_pass"]
    payload = {
        "run": "LSPV-5/409",
        "timestamp_pacific": "2026-11-07 04:55 PST",
        "status": "PROVED/RESTRICTED symbolic quantifier theorem + COMPUTATIONAL controls",
        "historical_checker": "NOT RUN; independent finite checker only",
        "tracker_precedence": "[P2-B6]/LSPV-1/462 clock calculus is prior work, not a new result here",
        "symbolic_claims": {
            "identity_system": "If A is a correct polynomial UNSAT decider, Q_A accepts (F,pi) iff pi=encode(F) and A(F)=UNSAT; every UNSAT F has a proof of N bits.",
            "exact_boundary": "For fixed R, B3 is equivalent to polynomial W-size simulation of Q_A; asserting that simulation without a rule-specific proof merely restates B3.",
            "noncircular_sufficient_condition": "A uniform polynomial-time compiler from Q_A proofs to explicit legal source-authenticated R proofs of polynomial output length, with fixed bounded native weights, implies B3.",
            "bare_trace_control": "Local validity of a REJECT trace is not source-UNSAT reflection; reject_all accepts the even-charge SAT controls.",
        },
        "established_tseitin_controls": sources,
        "inherited_clock_controls": clock,
        "negative_controls": negatives,
        "resources": {
            "elapsed_seconds": time.perf_counter() - started,
            "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "construction_parsing_truth_tables_hashing_bigints_serialization_charged": True,
            "historical_trace_bits_and_native_verification_not_measured": True,
        },
        "p_vs_np": "OPEN",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": "PASS",
        "finite_sources": len(sources),
        "padding_controls": len(clock),
        "sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
    }))


if __name__ == "__main__":
    main()
