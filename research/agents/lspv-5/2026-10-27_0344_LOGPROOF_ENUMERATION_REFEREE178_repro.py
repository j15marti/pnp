#!/usr/bin/env python3
"""Finite controls for LOGPROOF-ENUMERATION-REFEREE178.

The paired report contains the symbolic theorem.  This dependency-free audit
checks exact candidate counts, globally-sound verifier portfolios, mandatory
fresh resets, a nonuniform selected-verifier counterexample, proof-bit access,
and strict endpoint arithmetic.  It does not prove the FLMV theorem.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product
from math import floor, log2
from pathlib import Path
import hashlib
import json


def candidates(L: int):
    return tuple(format(x, f"0{ell}b") if ell else ""
                 for ell in range(L + 1) for x in range(1 << ell))


def fresh_enumerator(table, labels, cand, machines):
    """Return UNSAT exactly when some fresh verifier call accepts."""
    out = []
    for x in range(len(labels)):
        accepts = any(table[(v, x, p)] for v in range(machines) for p in cand)
        out.append("UNSAT" if accepts else "SAT")
    return tuple(out)


def main() -> None:
    assertions = 0
    failures: list[str] = []

    def check(ok: bool, label: str) -> None:
        nonlocal assertions
        assertions += 1
        if not ok:
            failures.append(label)

    count_rows = []
    for L in range(17):
        cs = candidates(L)
        exact = (1 << (L + 1)) - 1
        check(len(cs) == exact, f"candidate count L={L}")
        check(len(set(cs)) == exact, f"candidate uniqueness L={L}")
        check(all(len(x) <= L for x in cs), f"candidate cap L={L}")
        count_rows.append((L, exact))

    # Exhaust every combined verifier table for small domains.  If every
    # verifier is globally SAT-sound and the portfolio is jointly complete on
    # UNSAT, fresh enumeration is a correct total decider.
    exhaustive_rows = []
    cases = [
        (("SAT", "UNSAT"), 1, 1),
        (("SAT", "UNSAT"), 2, 1),
        (("SAT", "SAT", "UNSAT"), 2, 0),
        (("SAT", "UNSAT", "UNSAT"), 2, 0),
    ]
    for labels, machines, L in cases:
        cand = candidates(L)
        keys = tuple((v, x, p) for v in range(machines)
                     for x in range(len(labels)) for p in cand)
        qualified = 0
        for bits in product((0, 1), repeat=len(keys)):
            table = dict(zip(keys, bits))
            sound = all(not table[(v, x, p)]
                        for v in range(machines)
                        for x, label in enumerate(labels) if label == "SAT"
                        for p in cand)
            complete = all(any(table[(v, x, p)]
                               for v in range(machines) for p in cand)
                           for x, label in enumerate(labels) if label == "UNSAT")
            if sound and complete:
                qualified += 1
                got = fresh_enumerator(table, labels, cand, machines)
                check(got == labels,
                      f"portfolio correctness {labels,machines,L,bits}")
        check(qualified > 0, f"nonempty qualified {labels,machines,L}")
        exhaustive_rows.append((labels, machines, L, len(keys), qualified))

    # Fresh-start is load-bearing.  Each isolated call is sound on SAT and
    # proof '1' is complete on UNSAT.  Reusing dirty state across candidates
    # accepts the SAT input after the sequence 0,1.
    def stateful_call(label: str, proof: str, dirty: int):
        if proof == "0":
            return 0, 1
        if proof == "1":
            return int(label == "UNSAT" or dirty == 1), dirty
        return 0, dirty

    reset_rows = []
    for label in ("SAT", "UNSAT"):
        fresh = []
        for proof in ("0", "1"):
            accept, _ = stateful_call(label, proof, 0)
            fresh.append(accept)
        predicted = "UNSAT" if any(fresh) else "SAT"
        check(predicted == label, f"fresh reset correctness {label}")
        dirty = 0
        stale = []
        for proof in ("0", "1"):
            accept, dirty = stateful_call(label, proof, dirty)
            stale.append(accept)
        stale_predicted = "UNSAT" if any(stale) else "SAT"
        if label == "SAT":
            check(stale_predicted != label, "no-reset false acceptance")
        reset_rows.append((label, fresh, stale, predicted, stale_predicted))

    # Input-selected verifiers that are not globally sound do not compose.
    # V0 certifies U0 and V1 certifies U1, but both also accept the SAT input.
    labels = ("SAT", "UNSAT", "UNSAT")
    selected = {
        (0, 0): 1, (0, 1): 1, (0, 2): 0,
        (1, 0): 1, (1, 1): 0, (1, 2): 1,
    }
    check(selected[(0, 1)] == 1 and selected[(1, 2)] == 1,
          "selected UNSAT witnesses exist")
    check(selected[(0, 0)] == 1 and selected[(1, 0)] == 1,
          "selected verifiers globally unsound")
    portfolio_answer = tuple("UNSAT" if any(selected[(v, x)] for v in (0, 1))
                             else "SAT" for x in range(3))
    check(portfolio_answer[0] == "UNSAT", "unsound portfolio accepts SAT")

    # A logarithmic proof may be materialized once and answered through paid
    # indexed bit queries.  Out-of-range queries are malformed, not free bits.
    proof_access_rows = []
    for L in range(0, 13):
        for proof in candidates(L):
            stored = tuple(int(b) for b in proof)
            for q in range(-1, L + 2):
                ans = stored[q] if 0 <= q < len(stored) else None
                if 0 <= q < len(proof):
                    check(ans == int(proof[q]), f"proof bit {L,proof,q}")
                else:
                    check(ans is None, f"malformed proof query {L,proof,q}")
            proof_access_rows.append((L, len(proof)))

    # Exact visible-prefix count for a sequential proof head.  If the reach J
    # is below the physical cap P, strings ending by J expose their endmarker
    # and longer strings expose J+1 bits.  If J reaches P, every capped string
    # is fully distinguished.  The published 2^(A+1)-1 expression is safe but
    # overcounts by roughly two when the physical cap binds.
    visible_rows = []
    for P in range(0, 13):
        all_proofs = candidates(P)
        for J in range(0, 16):
            views = set()
            for proof in all_proofs:
                if len(proof) <= J:
                    views.add(("E", proof))
                else:
                    views.add(("P", proof[:J + 1]))
            exact = ((1 << (J + 2)) - 1) if J < P else ((1 << (P + 1)) - 1)
            A = min(P + 1, J + 1)
            coarse = (1 << (A + 1)) - 1
            check(len(views) == exact, f"visible exact {P,J}")
            check(exact <= coarse, f"visible coarse {P,J}")
            if J >= P:
                check(exact < coarse, f"physical-cap strict overcount {P,J}")
            else:
                check(exact == coarse, f"reach-cap equality {P,J}")
            visible_rows.append((P, J, exact, coarse))

    # Exact portfolio volume and finite exponent controls.
    volume_rows = []
    for e in range(4, 17):
        N = 1 << e
        for ai in range(0, 7):
            for bi in range(0, 7):
                a, b = Fraction(ai, 10), Fraction(bi, 10)
                L = floor(float(a) * log2(N))
                M = max(1, floor(N ** float(b)))
                volume = M * ((1 << (L + 1)) - 1)
                check(volume <= 2 * M * (N ** float(a)) + 1,
                      f"portfolio volume {e,ai,bi}")
                volume_rows.append((e, ai, bi, L, M, volume))

    c_star = Fraction(241, 200)
    s_star = Fraction(11642479, 23232400)
    endpoint_rows = []
    for ri in range(0, 161):
        for ai in range(0, 61):
            for bi in range(0, 61):
                r = Fraction(ri, 100)
                a = Fraction(ai, 100)
                b = Fraction(bi, 100)
                t = max(Fraction(1), r + a + b)
                strict = t < c_star
                check(strict == (200 * t.numerator < 241 * t.denominator),
                      f"strict arithmetic {ri,ai,bi}")
                endpoint_rows.append((ri, ai, bi, float(t), strict))
    check(Fraction(1) < c_star, "parser floor inside time box")
    check(s_star > Fraction(1, 2), "space endpoint above half")
    check(not (c_star < c_star), "equality not excluded")

    payload = {
        "id": "LOGPROOF-ENUMERATION-REFEREE178",
        "timestamp_utc": "2026-10-27T10:44:00Z",
        "assertions": assertions,
        "failures": len(failures),
        "first_failures": failures[:20],
        "status": {
            "single_verifier_enumeration": "PROVED/EXACT conditional on declared verifier",
            "uniform_global_sound_portfolio": "PROVED/EXACT conditional",
            "no_reset_enumeration": "FALSIFIED",
            "input_selected_nonuniform_verifier": "FALSIFIED as a uniform inference",
            "all_unsat_logproof_coverage": "OPEN",
            "arc_edge_90": "OPEN",
            "p_vs_np": "OPEN",
        },
        "count_rows": count_rows,
        "exhaustive_rows": exhaustive_rows,
        "reset_rows": reset_rows,
        "selected_portfolio_answer": portfolio_answer,
        "proof_access_row_count": len(proof_access_rows),
        "proof_access_sha256": hashlib.sha256(json.dumps(proof_access_rows, separators=(",", ":")).encode()).hexdigest(),
        "visible_prefix_rows": visible_rows,
        "volume_row_count": len(volume_rows),
        "volume_sha256": hashlib.sha256(json.dumps(volume_rows, separators=(",", ":")).encode()).hexdigest(),
        "endpoint_row_count": len(endpoint_rows),
        "endpoint_sha256": hashlib.sha256(json.dumps(endpoint_rows, separators=(",", ":")).encode()).hexdigest(),
        "c_star": [c_star.numerator, c_star.denominator],
        "s_star": [s_star.numerator, s_star.denominator],
        "limitations": [
            "Finite tests validate combinatorics and countercontrols, not the FLMV theorem.",
            "The symbolic consequence assumes one native indexed model, uniform total clocks, global SAT soundness, and all-UNSAT completeness.",
            "No all-UNSAT logarithmic certificate grammar is constructed.",
        ],
    }
    out = Path("2026-10-27_0344_LOGPROOF_ENUMERATION_REFEREE178_raw.json")
    out.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    print(json.dumps({"assertions": assertions, "failures": len(failures),
                      "output": str(out), "sha256": digest}, sort_keys=True))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
