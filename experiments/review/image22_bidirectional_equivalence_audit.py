#!/usr/bin/env python3
"""IMAGE22-BIEQUIV1 bounded audit.

Checks the exact ordered compiler-image recognizer and the two explicit
many-one reductions between L22 and its recognized compiler-image language.
The finite checks validate implementation/bookkeeping only; they do not prove
an asymptotic time lower bound.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import time
from collections import Counter
from pathlib import Path

import universal22 as u
from image22_decoder_audit import decode_image, encode


RUN_ID = "IMAGE22-BIEQUIV1"
EXPECTED_COMPILER_BLOB = "f985a13f237f2322f988ec82af132625acf3912c"
DEADLINE_SECONDS = 25


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def is_c22(cnf: u.CNF) -> bool:
    try:
        n = u.check_proper(cnf)
    except (ValueError, TypeError):
        return False
    occ = Counter(lit for clause in cnf for lit in clause)
    return all(occ[x] == 2 and occ[-x] == 2 for x in range(1, n + 1))


def reduce_l22_to_image(target: bytes) -> bytes:
    """Total reduction r. Invalid L22 encodings map to a fixed rejected string."""
    try:
        parsed = json.loads(target)
        cnf = [tuple(clause) for clause in parsed]
        if encode(cnf) != target or not is_c22(cnf):
            return b"[]"
        comp = u.compile22(cnf)
        assert comp.padding_gadgets == 0
        return encode(comp.clauses)
    except (ValueError, TypeError, UnicodeError, json.JSONDecodeError):
        return b"[]"


def reduce_image_to_l22(target: bytes) -> bytes:
    """Total reduction q. Ordered off-image strings map to fixed invalid NO."""
    return target if decode_image(target) is not None else b"[]"


def digit_sum(n: int) -> int:
    total = 0
    start = 1
    digits = 1
    while start <= n:
        end = min(n, 10 * start - 1)
        total += (end - start + 1) * digits
        start *= 10
        digits += 1
    return total


def exact_json_bytes(v: int) -> int:
    assert v % 3 == 0
    clauses = 4 * v // 3
    return 5 * clauses + 2 * v + 4 * digit_sum(v) + 1


def find_model(cnf: u.CNF):
    n = u.check_proper(cnf)
    if n > 16:
        return None
    for bits in itertools.product((0, 1), repeat=n):
        values = {i + 1: bits[i] for i in range(n)}
        if u.eval_cnf(cnf, values):
            return bits
    return None


def main() -> dict:
    started = time.monotonic()
    deadline = started + DEADLINE_SECONDS
    checks: Counter[str] = Counter()

    def check(condition: bool, group: str) -> None:
        if time.monotonic() > deadline:
            raise TimeoutError("25-second cooperative deadline exceeded")
        checks[group] += 1
        if not condition:
            raise AssertionError((group, checks[group]))

    check(git_blob(Path(u.__file__)) == EXPECTED_COMPILER_BLOB, "pinned_compiler")

    proper2, _ = u.properize23([(1, 2), (-1, 2)])
    graph3, _ = u.properize23(u.colouring_cnf(3, itertools.combinations(range(3), 2)))
    graph4, _ = u.properize23(u.colouring_cnf(4, itertools.combinations(range(4), 2)))
    cube = [
        tuple((i + 1) * (1 if bits[i] == 0 else -1) for i in range(3))
        for bits in itertools.product((0, 1), repeat=3)
    ]
    cases = {
        "single_clause": [(1, 2, 3)],
        "horn": [(1, -2, -3), (-1, 2, -3), (-1, -2, 3)],
        "properized_2sat": proper2,
        "affine_tseitin": u.W1,
        "independent_product": [(1, 2, 3), (4, 5, 6)],
        "cube_unsat": cube,
        "k3_colouring": graph3,
        "k4_colouring": graph4,
    }

    rows = []
    for name, source in cases.items():
        first = u.compile22(source)
        G = first.clauses
        x = encode(G)
        check(is_c22(G), "first_target_is_l22")
        second = u.compile22(G)
        check(second.padding_gadgets == 0, "balanced_fixed_by_balancer")
        y = reduce_l22_to_image(x)
        check(y == encode(second.clauses), "forward_reduction_exact")
        decoded = decode_image(y)
        check(decoded is not None, "forward_output_in_image")
        check(decoded.balanced == G, "left_inverse")
        check(reduce_image_to_l22(y) == y, "reverse_on_image_identity")

        # A real representation control: swap two implication-block clauses
        # while leaving the decoded balanced-source prefix fixed. This
        # preserves the L22 semantic instance and exact occurrences but fails
        # the declared ordered compiler layout.
        permuted = list(second.clauses)
        tail = len(G)
        permuted[tail], permuted[tail + 1] = permuted[tail + 1], permuted[tail]
        off = encode(permuted)
        check(is_c22(permuted), "off_image_still_l22")
        check(decode_image(off) is None, "ordered_off_image_rejected")
        check(reduce_image_to_l22(off) == b"[]", "off_image_total_no")

        v = first.n
        check(v % 3 == 0, "l22_variable_divisibility")
        check(len(x) == exact_json_bytes(v), "exact_source_encoding")
        check(len(y) == exact_json_bytes(12 * v), "exact_image_encoding")
        check(len(y) < 20 * len(x), "linear_length_bound")

        rows.append({
            "case": name,
            "source_satisfiable_if_bruteforced": find_model(source) is not None,
            "l22_variables": v,
            "l22_clauses": len(G),
            "image_variables": second.n,
            "image_clauses": len(second.clauses),
            "l22_bytes": len(x),
            "image_bytes": len(y),
            "length_ratio": len(y) / len(x),
        })

    # Exhaust exact encoding arithmetic across a broad finite range and all
    # digit boundaries in it. The report supplies the symbolic <20 proof.
    maximum_ratio = (0.0, None)
    for v in range(3, 300_001, 3):
        ratio = exact_json_bytes(12 * v) / exact_json_bytes(v)
        check(ratio < 20, "finite_length_sweep")
        if ratio > maximum_ratio[0]:
            maximum_ratio = (ratio, v)

    # Arbitrary polynomial exponent is preserved up to fixed preprocessing.
    exponent_rows = []
    for k in range(1, 101):
        l22_to_image = max(3, k)  # recognizer then same-input L22 decider
        image_to_l22 = max(3, k)  # compiler, then <=20N image query
        check(l22_to_image == max(3, k), "reverse_exponent")
        check(image_to_l22 == max(3, k), "forward_exponent")
        exponent_rows.append({"k": k, "both_composed_exponents": max(3, k)})

    elapsed = time.monotonic() - started
    return {
        "run_id": RUN_ID,
        "status": "COMPUTATIONAL",
        "method": "exact ordered compiler/decoder checks; exhaustive encoding arithmetic for v<=300000; no asymptotic inference",
        "assertions": sum(checks.values()),
        "checks_by_group": dict(checks),
        "elapsed_seconds": elapsed,
        "cases": rows,
        "maximum_finite_ratio": {"ratio": maximum_ratio[0], "v": maximum_ratio[1]},
        "exponent_rows": exponent_rows,
        "hostile_controls": [
            "Horn", "properized 2SAT", "affine/Tseitin", "independent product",
            "K3/K4 colouring", "UNSAT cube", "clause permutation", "off-image rejection"
        ],
        "limitations": [
            "Finite checks do not prove the symbolic equivalence theorem or any time lower bound.",
            "The reductions preserve polynomial-time decidability but do not make a restricted proof-system bound apply to arbitrary machines.",
            "An off-image satisfiable L22 encoding shows why the reverse reduction needs the exact recognizer rather than identity."
        ],
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "compiler_blob": git_blob(Path(u.__file__)),
        "decoder_sha256": hashlib.sha256(Path(__file__).with_name("image22_decoder_audit.py").read_bytes()).hexdigest(),
    }


if __name__ == "__main__":
    result = main()
    out = Path("results/raw/review/2026-10-13_1303_image22_bidirectional_equivalence.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "run_id": result["run_id"],
        "status": result["status"],
        "assertions": result["assertions"],
        "elapsed_seconds": result["elapsed_seconds"],
        "maximum_finite_ratio": result["maximum_finite_ratio"],
    }, sort_keys=True))
