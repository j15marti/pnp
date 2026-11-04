#!/usr/bin/env python3
"""REFEREE347 finite controls for extensional UNSAT-invariant collapse."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


def require(ok: bool, msg: str) -> None:
    if not ok:
        raise AssertionError(msg)


def proper_clause(clause: tuple[int, ...], n: int) -> bool:
    if not clause or len(set(clause)) != len(clause):
        return False
    if any(lit == 0 or abs(lit) > n for lit in clause):
        return False
    s = set(clause)
    return not any(-lit in s for lit in s)


def proper_cnf(cnf: tuple[tuple[int, ...], ...], n: int) -> bool:
    return n >= 1 and all(proper_clause(c, n) for c in cnf)


def clause_value(clause: tuple[int, ...], assignment: tuple[int, ...]) -> bool:
    return any((assignment[abs(lit) - 1] == 1) == (lit > 0) for lit in clause)


def cnf_value(cnf: tuple[tuple[int, ...], ...], assignment: tuple[int, ...]) -> bool:
    return all(clause_value(c, assignment) for c in cnf)


def signature(cnf: tuple[tuple[int, ...], ...], n: int) -> str:
    return "".join(
        "1" if cnf_value(cnf, a) else "0"
        for a in itertools.product((0, 1), repeat=n)
    )


def unit_core(n: int) -> tuple[tuple[int, ...], ...]:
    # Every named variable occurs, no tautological or empty source clause is used.
    return ((1,), (-1,)) + tuple(c for i in range(2, n + 1) for c in ((1, i), (1, -i)))


def sat_sibling(n: int) -> tuple[tuple[int, ...], ...]:
    return ((1,),) + tuple(c for i in range(2, n + 1) for c in ((1, i), (1, -i)))


def verify_one_step_empty(cnf: tuple[tuple[int, ...], ...], proof: dict) -> bool:
    try:
        a, b = proof["parents"]
        pivot = proof["pivot"]
        conclusion = tuple(proof["conclusion"])
    except (KeyError, TypeError, ValueError):
        return False
    if not isinstance(a, int) or not isinstance(b, int) or not isinstance(pivot, int):
        return False
    if not (0 <= a < len(cnf) and 0 <= b < len(cnf)) or pivot <= 0:
        return False
    ca, cb = set(cnf[a]), set(cnf[b])
    if pivot in ca and -pivot in cb:
        resolvent = (ca - {pivot}) | (cb - {-pivot})
    elif -pivot in ca and pivot in cb:
        resolvent = (ca - {-pivot}) | (cb - {pivot})
    else:
        return False
    if any(-lit in resolvent for lit in resolvent):
        return False
    return set(conclusion) == resolvent and len(conclusion) == len(set(conclusion))


def all_clauses(n: int) -> list[tuple[int, ...]]:
    out = []
    for state in itertools.product((-1, 0, 1), repeat=n):
        if all(x == 0 for x in state):
            continue
        out.append(tuple((i + 1) * s for i, s in enumerate(state) if s))
    return out


def php(h: int) -> tuple[tuple[int, ...], ...]:
    def v(pigeon: int, hole: int) -> int:
        return (pigeon - 1) * h + hole

    positives = [tuple(v(i, a) for a in range(1, h + 1)) for i in range(1, h + 2)]
    collisions = [
        (-v(i, a), -v(j, a))
        for a in range(1, h + 1)
        for i in range(1, h + 2)
        for j in range(i + 1, h + 2)
    ]
    return tuple(positives + collisions)


def php_deleted_sibling(h: int) -> tuple[tuple[int, ...], ...]:
    f = list(php(h))
    target = (-1, -(h + 1))
    f.remove(target)
    return tuple(f)


def k4_tseitin(charges: tuple[int, int, int, int]) -> tuple[tuple[int, ...], ...]:
    edges = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))
    incident = [[i + 1 for i, e in enumerate(edges) if v in e] for v in range(4)]
    clauses: list[tuple[int, ...]] = []
    for v, vars_ in enumerate(incident):
        for bits in itertools.product((0, 1), repeat=3):
            if sum(bits) % 2 == charges[v]:
                continue
            clauses.append(tuple(-var if bit else var for var, bit in zip(vars_, bits)))
    return tuple(clauses)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    checks = 0

    def check(ok: bool, msg: str) -> None:
        nonlocal checks
        require(ok, msg)
        checks += 1

    cores = []
    for n in range(1, 13):
        u = unit_core(n)
        s = sat_sibling(n)
        check(proper_cnf(u, n), f"proper U_{n}")
        check(signature(u, n) == "0" * (1 << n), f"U_{n} false")
        check(verify_one_step_empty(u, {"parents": [0, 1], "pivot": 1, "conclusion": []}), f"U_{n} proof")
        check(proper_cnf(s, n), f"proper S_{n}")
        check(signature(s, n).count("1") == (1 << (n - 1)), f"S_{n} models")
        cores.append({
            "n": n,
            "source_clauses": len(u),
            "signature_sha256": hashlib.sha256(signature(u, n).encode()).hexdigest(),
            "resolution_paid_nodes": 1,
            "json_source_bytes": len(json.dumps(u, separators=(",", ":")).encode()),
        })

    clauses2 = all_clauses(2)
    exhaustive = {"formulas": 0, "sat": 0, "unsat": 0, "unsat_zero_signature": 0}
    for mask in range(1 << len(clauses2)):
        f = tuple(clauses2[i] for i in range(len(clauses2)) if (mask >> i) & 1)
        sig = signature(f, 2)
        exhaustive["formulas"] += 1
        check(len(sig) == 4, "two-variable signature length")
        if "1" in sig:
            exhaustive["sat"] += 1
        else:
            exhaustive["unsat"] += 1
            exhaustive["unsat_zero_signature"] += 1
            check(sig == signature(unit_core(2), 2), "UNSAT extensional quotient")

    php_controls = []
    for h in (1, 2, 3):
        f, sibling = php(h), php_deleted_sibling(h)
        n = h * (h + 1)
        sig = signature(f, n)
        ssig = signature(sibling, n)
        check(sig == "0" * (1 << n), f"PHP_{h} UNSAT")
        check("1" in ssig, f"PHP_{h} deletion SAT")
        php_controls.append({"h": h, "variables": n, "clauses": len(f), "sibling_models": ssig.count("1")})

    odd = k4_tseitin((1, 0, 0, 0))
    even = k4_tseitin((0, 0, 0, 0))
    odd_sig, even_sig = signature(odd, 6), signature(even, 6)
    check(odd_sig == "0" * 64, "odd K4 Tseitin UNSAT")
    check(even_sig.count("1") == 8, "even K4 Tseitin models")

    malformed = [
        ((), 0),
        (((0,),), 1),
        (((2,),), 1),
        (((1, 1),), 1),
        (((1, -1),), 1),
        (((),), 1),
        (((1,), (-1,)), -1),
    ]
    for f, n in malformed:
        check(not proper_cnf(f, n), "malformed rejected")

    bad_proofs = [
        {"parents": [0, 1], "pivot": 2, "conclusion": []},
        {"parents": [0, 99], "pivot": 1, "conclusion": []},
        {"parents": [0, 1], "pivot": 1, "conclusion": [1]},
        {"parents": [0, 0], "pivot": 1, "conclusion": []},
        {"parents": [0, 1], "conclusion": []},
    ]
    for proof in bad_proofs:
        check(not verify_one_step_empty(unit_core(3), proof), "bad proof rejected")

    result = {
        "run": "REFEREE347",
        "theorem": {
            "name": "extensional_unsat_collapse",
            "statement": "Any nonnegative lower-bound invariant depending only on the Boolean function and valid for every proper n-variable CNF is at most 1 on constant false, because U_n has a one-node Resolution refutation.",
            "status": "PROVED_EXACT",
            "scope": "proper nonempty-clause CNFs; fixed R containing ordinary Resolution; semantic equivalence on aligned named variables",
        },
        "unit_core_family": cores,
        "exhaustive_two_variable": exhaustive,
        "php_controls": php_controls,
        "k4_tseitin": {"odd_models": odd_sig.count("1"), "even_models": even_sig.count("1"), "clauses_each": len(odd)},
        "malformed_rejected": len(malformed),
        "bad_proofs_rejected": len(bad_proofs),
        "checks": checks,
        "cost_ledger": {
            "unit_core_construction": "O(n) clauses and O(n log n) signed-ID bits",
            "one_step_verification": "two parent reads, one pivot check, and explicit empty output",
            "truth_tables": "offline exponential diagnostics only; not charged as a SAT algorithm",
            "separator_conclusion": "minimizing over all semantically equivalent representations permits U_n and collapses the measure; source-preserving translation must be charged separately",
        },
        "bridges": {"B1": "OPEN", "B2": "OPEN", "B3": "OPEN", "P_vs_NP": "OPEN"},
    }
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(payload)
    print(json.dumps({"output": str(path.resolve()), "checks": checks, "sha256": hashlib.sha256(payload.encode()).hexdigest(), "summary": exhaustive}))


if __name__ == "__main__":
    main()
