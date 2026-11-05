#!/usr/bin/env python3
"""REFEREE348: local streaming recognizer proof-system firewall.

This is a finite executable audit of the mathematical construction in the
companion report.  The special branch is an explicitly serialized, one-byte
per transition recognizer trace for canonical unary pigeonhole CNFs.  The
fallback branch is a complete assignment-table certificate for arbitrary
UNSAT CNFs.  Neither branch is a claim about R_mix341.
"""

from __future__ import annotations

import hashlib
import json
import math
import resource
import time
from pathlib import Path


CHECKS = 0


def check(condition: bool, message: str) -> None:
    global CHECKS
    if not condition:
        raise AssertionError(message)
    CHECKS += 1


def var_id(pigeon: int, hole: int, h: int) -> int:
    return (pigeon - 1) * h + hole


def php_clauses(h: int) -> tuple[int, list[list[int]]]:
    if h < 1:
        raise ValueError("h must be positive")
    clauses: list[list[int]] = []
    for pigeon in range(1, h + 2):
        clauses.append([var_id(pigeon, hole, h) for hole in range(1, h + 1)])
    for hole in range(1, h + 1):
        for p in range(1, h + 2):
            for q in range(p + 1, h + 2):
                clauses.append([-var_id(p, hole, h), -var_id(q, hole, h)])
    return h * (h + 1), clauses


def encode_dimacs(n: int, clauses: list[list[int]]) -> str:
    lines = [f"p cnf {n} {len(clauses)}"]
    for clause in clauses:
        lines.append(" ".join(map(str, clause + [0])))
    return "\n".join(lines) + "\n"


def canonical_php_source(h: int) -> str:
    n, clauses = php_clauses(h)
    return encode_dimacs(n, clauses)


def parse_dimacs(source: str) -> tuple[int, list[list[int]]]:
    if not isinstance(source, str) or not source.endswith("\n"):
        raise ValueError("source must be newline-terminated text")
    lines = source.splitlines()
    if not lines:
        raise ValueError("empty source")
    head = lines[0].split()
    if len(head) != 4 or head[:2] != ["p", "cnf"]:
        raise ValueError("bad header")
    try:
        n, m = int(head[2]), int(head[3])
    except ValueError as exc:
        raise ValueError("nonnumeric header") from exc
    if n < 0 or m < 0 or len(lines) != m + 1:
        raise ValueError("bad declared dimensions")
    clauses: list[list[int]] = []
    for line in lines[1:]:
        fields = line.split()
        if not fields:
            raise ValueError("blank clause line")
        try:
            ints = [int(x) for x in fields]
        except ValueError as exc:
            raise ValueError("nonnumeric literal") from exc
        if ints[-1] != 0 or any(x == 0 for x in ints[:-1]):
            raise ValueError("bad clause terminator")
        clause = ints[:-1]
        if any(abs(x) < 1 or abs(x) > n for x in clause):
            raise ValueError("literal out of range")
        clauses.append(clause)
    return n, clauses


def satisfies(clauses: list[list[int]], assignment: int) -> bool:
    for clause in clauses:
        if not any(((assignment >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause):
            return False
    return True


def falsified_clause(clauses: list[list[int]], assignment: int) -> int | None:
    for j, clause in enumerate(clauses):
        if not any(((assignment >> (abs(lit) - 1)) & 1) == (lit > 0) for lit in clause):
            return j
    return None


def build_scan_proof(source: str, h: int) -> list[dict[str, int | str]]:
    proof: list[dict[str, int | str]] = [{"op": "START", "h": h, "pos": -1}]
    for pos, byte in enumerate(source.encode("ascii")):
        proof.append({"op": "SCAN", "h": h, "pos": pos, "byte": byte})
    proof.append({"op": "ACCEPT_PHP", "h": h, "pos": len(source.encode("ascii"))})
    return proof


def verify_scan_proof(source: str, proof: list[dict[str, int | str]]) -> bool:
    try:
        parse_dimacs(source)
        if not proof or proof[0].get("op") != "START":
            return False
        h = proof[0].get("h")
        if not isinstance(h, int) or h < 1 or proof[0].get("pos") != -1:
            return False
        expected = canonical_php_source(h).encode("ascii")
        actual = source.encode("ascii")
        if len(proof) != len(actual) + 2:
            return False
        for pos, node in enumerate(proof[1:-1]):
            if node != {"op": "SCAN", "h": h, "pos": pos, "byte": actual[pos]}:
                return False
            if pos >= len(expected) or actual[pos] != expected[pos]:
                return False
        final = proof[-1]
        return (
            actual == expected
            and final == {"op": "ACCEPT_PHP", "h": h, "pos": len(actual)}
        )
    except (ValueError, UnicodeEncodeError, IndexError, TypeError):
        return False


def build_table_proof(source: str) -> list[dict[str, int | str]]:
    n, clauses = parse_dimacs(source)
    proof: list[dict[str, int | str]] = [{"op": "TABLE_START", "n": n, "idx": -1}]
    for assignment in range(1 << n):
        j = falsified_clause(clauses, assignment)
        if j is None:
            raise ValueError("SAT source has no complete UNSAT table certificate")
        proof.append({"op": "TABLE", "idx": assignment, "clause": j})
    proof.append({"op": "ACCEPT_TABLE", "n": n, "idx": 1 << n})
    return proof


def verify_table_proof(source: str, proof: list[dict[str, int | str]]) -> bool:
    try:
        n, clauses = parse_dimacs(source)
        if not proof or proof[0] != {"op": "TABLE_START", "n": n, "idx": -1}:
            return False
        if len(proof) != (1 << n) + 2:
            return False
        for assignment, node in enumerate(proof[1:-1]):
            if node.get("op") != "TABLE" or node.get("idx") != assignment:
                return False
            j = node.get("clause")
            if not isinstance(j, int) or not (0 <= j < len(clauses)):
                return False
            if j != falsified_clause(clauses, assignment):
                return False
        return proof[-1] == {"op": "ACCEPT_TABLE", "n": n, "idx": 1 << n}
    except (ValueError, TypeError):
        return False


def verify_local_system(source: str, proof: list[dict[str, int | str]]) -> bool:
    if not proof:
        return False
    return verify_scan_proof(source, proof) if proof[0].get("op") == "START" else verify_table_proof(source, proof)


def deleted_collision_sibling(h: int) -> tuple[str, int]:
    n, clauses = php_clauses(h)
    target = [-var_id(1, 1, h), -var_id(2, 1, h)]
    delete_at = clauses.index(target)
    sibling = clauses[:delete_at] + clauses[delete_at + 1 :]
    assignment = 0
    assignment |= 1 << (var_id(1, 1, h) - 1)
    assignment |= 1 << (var_id(2, 1, h) - 1)
    for p in range(3, h + 2):
        assignment |= 1 << (var_id(p, p - 1, h) - 1)
    check(satisfies(sibling, assignment), f"PHP deletion witness h={h}")
    return encode_dimacs(n, sibling), assignment


def xor3_clauses(a: int, b: int, c: int, parity: int) -> list[list[int]]:
    out = []
    for mask in range(8):
        if (((mask >> 0) & 1) ^ ((mask >> 1) & 1) ^ ((mask >> 2) & 1)) != parity:
            vals = [(mask >> i) & 1 for i in range(3)]
            out.append([v if val == 0 else -v for v, val in zip((a, b, c), vals)])
    return out


def k4_tseitin(charges: tuple[int, int, int, int]) -> str:
    edges = {(0, 1): 1, (0, 2): 2, (0, 3): 3, (1, 2): 4, (1, 3): 5, (2, 3): 6}
    incident = []
    for v in range(4):
        incident.append([idx for (u, w), idx in edges.items() if v in (u, w)])
    clauses: list[list[int]] = []
    for v in range(4):
        clauses.extend(xor3_clauses(*incident[v], charges[v]))
    return encode_dimacs(6, clauses)


def mutate_scan_proofs(source: str, proof: list[dict[str, int | str]]) -> list[list[dict[str, int | str]]]:
    bad: list[list[dict[str, int | str]]] = []
    p = [dict(x) for x in proof]
    p[1]["byte"] = (int(p[1]["byte"]) + 1) % 128
    bad.append(p)
    p = [dict(x) for x in proof]
    p[2]["pos"] = int(p[2]["pos"]) + 1
    bad.append(p)
    p = [dict(x) for x in proof]
    p[-1]["pos"] = int(p[-1]["pos"]) - 1
    bad.append(p)
    p = [dict(x) for x in proof]
    p[0]["h"] = int(p[0]["h"]) + 1
    bad.append(p)
    p = [dict(x) for x in proof]
    del p[len(p) // 2]
    bad.append(p)
    p = [dict(x) for x in proof]
    p[-1]["op"] = "ACCEPT_TABLE"
    bad.append(p)
    return bad


def serialized_bits(proof: list[dict[str, int | str]]) -> int:
    return 8 * len(json.dumps(proof, separators=(",", ":"), sort_keys=True).encode())


def main() -> None:
    started = time.perf_counter()
    php_records = []
    for h in range(1, 9):
        source = canonical_php_source(h)
        n, clauses = parse_dimacs(source)
        proof = build_scan_proof(source, h)
        check(n == h * (h + 1), f"PHP variable count h={h}")
        check(len(clauses) == (h + 1) + h * math.comb(h + 1, 2), f"PHP clause count h={h}")
        check(verify_scan_proof(source, proof), f"scan proof h={h}")
        check(verify_local_system(source, proof), f"unified verifier h={h}")
        check(all(not satisfies(clauses, a) for a in range(1 << n)) if n <= 6 else True,
              f"small PHP UNSAT h={h}")
        for bad in mutate_scan_proofs(source, proof):
            check(not verify_scan_proof(source, bad), f"corrupt scan rejected h={h}")
        php_records.append({
            "h": h,
            "variables": n,
            "clauses": len(clauses),
            "source_bytes": len(source.encode()),
            "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
            "trace_nodes": len(proof),
            "serialized_proof_bits": serialized_bits(proof),
            "max_parent_arity": 1,
            "opcode_count": 3,
        })

    deletion_records = []
    for h in range(1, 6):
        sibling, witness = deleted_collision_sibling(h)
        n, clauses = parse_dimacs(sibling)
        check(satisfies(clauses, witness), f"deletion sibling SAT h={h}")
        check(not verify_scan_proof(sibling, build_scan_proof(sibling, h)), f"deletion sibling not special h={h}")
        # The exhibited satisfying assignment is a direct soundness blocker:
        # its TABLE node could name no falsified authentic clause.  Avoid an
        # exponential offline scan for the larger finite siblings.
        check(falsified_clause(clauses, witness) is None, f"SAT sibling blocks fallback h={h}")
        deletion_records.append({"h": h, "witness": witness, "source_sha256": hashlib.sha256(sibling.encode()).hexdigest()})

    unit_unsat = encode_dimacs(1, [[1], [-1]])
    horn_unsat = encode_dimacs(4, [[1], [-1, 2], [-2, 3], [-3, 4], [-4]])
    odd_k4 = k4_tseitin((1, 0, 0, 0))
    even_k4 = k4_tseitin((0, 0, 0, 0))
    controls = []
    for name, source in (("unit_unsat", unit_unsat), ("horn_unsat", horn_unsat), ("odd_k4", odd_k4)):
        proof = build_table_proof(source)
        check(verify_table_proof(source, proof), f"fallback {name}")
        check(verify_local_system(source, proof), f"unified fallback {name}")
        controls.append({"name": name, "source": source, "proof": proof})

    even_n, even_clauses = parse_dimacs(even_k4)
    even_models = [a for a in range(1 << even_n) if satisfies(even_clauses, a)]
    check(len(even_models) == 8, "even K4 has eight models")
    try:
        build_table_proof(even_k4)
        check(False, "even K4 must reject fallback")
    except ValueError:
        check(True, "even K4 rejects fallback")

    sat_unit = encode_dimacs(1, [[1]])
    try:
        build_table_proof(sat_unit)
        check(False, "SAT unit must reject fallback")
    except ValueError:
        check(True, "SAT unit rejects fallback")

    malformed = [
        "",
        "p cnd 1 1\n1 0\n",
        "p cnf 1 2\n1 0\n",
        "p cnf -1 0\n",
        "p cnf 1 1\n2 0\n",
        "p cnf 1 1\n1\n",
        "p cnf 1 1\n1 0 0\n",
        "p cnf 1 1\n1 0",
    ]
    for i, bad_source in enumerate(malformed):
        try:
            parse_dimacs(bad_source)
            check(False, f"malformed parsed {i}")
        except ValueError:
            check(True, f"malformed rejected {i}")
        check(not verify_local_system(bad_source, [{"op": "START", "h": 1, "pos": -1}]),
              f"malformed system rejected {i}")

    result = {
        "run": "REFEREE348",
        "timestamp_pst": "2026-11-04 16:48 PST",
        "status": {
            "proved": "finite-opcode, unary-parent, exact-source local checking does not preserve Resolution hardness across sound complete systems",
            "restricted": "P_trace348 versus ordinary Resolution on canonical unary PHP",
            "open": ["full R_mix341 B1", "full R_mix341 B2", "full R_mix341 B3", "superpolynomial Wbar_Rmix341", "P versus NP"],
        },
        "system": {
            "name": "P_trace348",
            "fixed_opcodes": ["START", "SCAN", "ACCEPT_PHP", "TABLE_START", "TABLE", "ACCEPT_TABLE"],
            "max_parent_arity": 1,
            "php_node_payload": "O(log N) bits: fixed opcode, h, source position, one source byte",
            "fallback_payload": "O(n+log m) bits: assignment index and authenticated falsified-clause index",
            "soundness": "special branch accepts exactly canonical PHP; fallback covers every assignment with a falsified authentic source clause",
            "completeness": "every UNSAT CNF has a complete assignment-table certificate",
        },
        "php": php_records,
        "deletion_sat_siblings": deletion_records,
        "fallback_controls": controls,
        "paired_controls": {
            "sat_unit": sat_unit,
            "even_k4": even_k4,
            "even_k4_models": len(even_models),
        },
        "malformed_count": len(malformed),
        "charged_asymptotics": {
            "canonical_php_source": "N_h=Theta(h^3 log h) encoded bits",
            "php_trace_nodes": "Theta(N_h)=Theta(h^3 log h) for the exhibited one-byte trace",
            "php_trace_bits": "O(N_h log N_h) with explicit repeated positions; JSON test encoding is larger but polynomial",
            "php_verification": "O(N_h polylog N_h) bit work including source parse, source reads, transition checks and expected-source generation",
            "php_peak": "O(log N_h) writable streaming state plus read-only source/proof; O(N_h) or proof-size if materialized",
            "fallback": "2^n table nodes plus source parsing, every clause lookup/check, proof output and checking",
            "optimizer": "not charged to W; exhibited certificates are constructed directly",
        },
        "falsified": [
            "exact-source authentication alone restores cross-system hardness",
            "finite opcodes and bounded parent arity restore cross-system hardness",
            "polylog payload and nodewise local transitions restore cross-system hardness",
            "fully charging polynomial recognition converts Haken Resolution hardness into unrestricted machine hardness",
        ],
        "checks": CHECKS,
        "wall_seconds": time.perf_counter() - started,
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    out = Path("results/raw/arc/2026-11-04_1648_LSPV5_348_LOCAL_STREAMING_PHP.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"checks": CHECKS, "output": str(out), "sha256": hashlib.sha256(out.read_bytes()).hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
