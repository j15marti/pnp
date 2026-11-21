#!/usr/bin/env python3
"""T5-PAYLOAD-SUPPORT1: legal one-bit changes in the encoded count map.

Standard library only. All counts are exact. The general circuit lower bound
uses the accompanying proof; finite tests alone do not establish it.
Run from the repository root:
    python experiments/t5_bounds_payload_support_20261121.py
"""

from collections import Counter
from hashlib import sha256
from itertools import product
from pathlib import Path
import json


TRIPLES = {frozenset((i, (i + 1) % 5, (i + 2) % 5)) for i in range(5)}


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def relation(a, b, c):
    return len({a, b, c}) == 3 and frozenset((a, b, c)) in TRIPLES


def encode(n, clauses):
    check(type(n) is int and n >= 0, "invalid variable declaration")
    w = n.bit_length()
    for row in clauses:
        check(len(row) == 3 and len(set(row)) == 3, "non-strict clause")
        check(all(type(v) is int and 1 <= v <= n for v in row), "bad ID")
    gamma = bin(len(clauses) + 1)[2:]
    header = "1" * n + "0" + "0" * (len(gamma) - 1) + gamma
    payload = "".join(format(v, f"0{w}b") for row in clauses for v in row)
    return header + payload


def decode(bits):
    if not isinstance(bits, str) or any(c not in "01" for c in bits):
        raise ValueError("nonbinary encoding")
    n = 0
    while n < len(bits) and bits[n] == "1":
        n += 1
    if n == len(bits):
        raise ValueError("unterminated variable declaration")
    pos = n + 1
    leading = 0
    while pos + leading < len(bits) and bits[pos + leading] == "0":
        leading += 1
    start = pos + leading
    end = start + leading + 1
    if end > len(bits):
        raise ValueError("truncated gamma code")
    m = int(bits[start:end], 2) - 1
    w = n.bit_length()
    if len(bits) - end != 3 * m * w or (n == 0 and m != 0):
        raise ValueError("wrong payload length")
    clauses = []
    pos = end
    for _ in range(m):
        row = tuple(int(bits[pos + s * w:pos + (s + 1) * w], 2)
                    for s in range(3))
        pos += 3 * w
        if len(set(row)) != 3 or any(v < 1 or v > n for v in row):
            raise ValueError("invalid strict clause")
        clauses.append(row)
    return n, clauses


def count_used_names(n, clauses):
    """Generic finite enumeration on used names, with exact unused factor."""
    names = sorted({v for row in clauses for v in row})
    check(len(names) <= 7, "finite audit would be too large")
    positions = {v: i for i, v in enumerate(names)}
    # Duplicate conjunction rows are removed only by exact tuple equality.
    rows = list(dict.fromkeys(tuple(positions[v] for v in row) for row in clauses))
    core = sum(all(relation(values[a], values[b], values[c]) for a, b, c in rows)
               for values in product(range(5), repeat=len(names)))
    return core * 5 ** (n - len(names)), core, len(names)


def count_all_names(n, clauses):
    """Independent direct enumeration of all five-valued assignments."""
    check(n <= 7, "full enumeration limited to n <= 7")
    rows = [tuple(v - 1 for v in row) for row in clauses]
    return sum(all(relation(values[a], values[b], values[c]) for a, b, c in rows)
               for values in product(range(5), repeat=n))


def recognized_count(bits):
    """Exact star-family shortcut; None means UNKNOWN, never UNSAT."""
    try:
        n, clauses = decode(bits)
    except ValueError:
        return None
    w = n.bit_length()
    if w < 3 or n != (1 << w) - 1 or len(clauses) < 2:
        return None
    baseline = encode(n, [(3, 5, 6)] * len(clauses))
    changed = sum(a != b for a, b in zip(bits, baseline))
    if changed == 0:
        return 30 * 5 ** (n - 3)
    if changed == 1:
        return 10 * 5 ** (n - 3)
    return None


def audit_parameters(w, m):
    n = (1 << w) - 1
    check(w >= 3 and m >= 2, "theorem parameter condition")
    header_size = n + 2 + 2 * ((m + 1).bit_length() - 1)
    expected_nbits = header_size + 3 * m * w
    z0 = 30 * 5 ** (n - 3)
    z1 = 10 * 5 ** (n - 3)
    rows = []
    full_checks = 0
    base_row = (3, 5, 6)
    check(all(v.bit_count() == 2 for v in base_row), "baseline ID weight")
    check(all((a ^ b).bit_count() == 2 for a in base_row for b in base_row if a != b),
          "baseline ID pair distance")
    clauses = [base_row] * m
    encoded = encode(n, clauses)
    check(len(encoded) == expected_nbits, "wrong exact N")
    check(decode(encoded) == (n, clauses), "baseline roundtrip")
    got0, core0, used0 = count_used_names(n, clauses)
    check(got0 == z0 and core0 == 30 and used0 == 3, "baseline count")
    check(recognized_count(encoded) == got0, "baseline shortcut")
    if w == 3 and m == 2:
        check(count_all_names(n, clauses) == got0, "full baseline count")
        full_checks += 1
    for slot in range(3):
        for clause_index, j in product(range(m), range(w)):
            changed = clauses.copy()
            replacement = list(base_row)
            replacement[slot] = base_row[slot] ^ (1 << j)
            check(len(set(base_row) | {replacement[slot]}) == 4, "not four distinct names")
            changed[clause_index] = tuple(replacement)
            encoded1 = encode(n, changed)
            check(decode(encoded1) == (n, changed), "mutant roundtrip")
            pos = header_size + (3 * clause_index + slot) * w + (w - 1 - j)
            differences = [i for i, (a, b) in enumerate(zip(encoded, encoded1)) if a != b]
            check(len(encoded1) == len(encoded) and differences == [pos], "not one input bit")
            got1, core1, used1 = count_used_names(n, changed)
            check(got1 == z1 and core1 == 50 and used1 == 4, "mutant count")
            check(recognized_count(encoded1) == got1, "mutant shortcut")
            check(got0 % 8 == 6 and got1 % 8 == 2, "common count bit did not change")
            check(got0 > 0 and got1 > 0, "count-only witnesses must both be SAT")
            if w == 3 and m == 2:
                check(count_all_names(n, changed) == got1, "full mutant count")
                full_checks += 1
            rows.append({"clause_index": clause_index, "slot": slot,
                         "id_bit_lsb_index": j, "input_bit_position": pos,
                         "old_id": base_row[slot], "new_id": replacement[slot],
                         "base_sha256": sha256(encoded.encode()).hexdigest(),
                         "mutant_sha256": sha256(encoded1.encode()).hexdigest()})
    check({r["input_bit_position"] for r in rows} == set(range(header_size, expected_nbits)),
          "some payload bits missing")
    return {"w": w, "n": n, "m": m, "N": expected_nbits,
            "header_bits": header_size, "payload_bits": 3 * m * w,
            "gate_lower_bound": 3 * m * w - 1,
            "baseline_clause": base_row, "baseline_encoding": encoded,
            "same_baseline_for_every_bit": True,
            "baseline_count": z0, "mutant_count": z1,
            "output_bit_lsb_index": 2, "full_enumeration_checks": full_checks,
            "one_bit_pairs": rows}


def controls():
    # The second unchanged row is necessary. With m=1, renaming one name
    # preserves the count, and this construction has no bit sensitivity.
    n = 7
    single_before = [(1, 2, 7)]
    single_after = [(1, 2, 6)]
    count0 = count_used_names(n, single_before)[0]
    check(count_used_names(n, single_after)[0] == count0, "m=1 control")
    # C-slot permutation preserves meaning and is a permitted syntax change.
    a = [(1, 2, 7), (1, 2, 6)]
    b = [(7, 1, 2), (6, 2, 1)]
    check(count_used_names(n, a)[0] == count_used_names(n, b)[0], "C-slot symmetry")
    # No count-to-decision transfer: all support witnesses are SAT. Add an
    # unrelated strict-C UNSAT input solely as a counter sanity check.
    unsat = [(1, 2, 3), (1, 2, 4), (1, 3, 4), (2, 3, 4)]
    check(count_all_names(4, unsat) == 0, "UNSAT counter control")
    malformed = encode(7, [(1, 2, 7), (1, 2, 7)])
    h = len(malformed) - 18
    malformed = malformed[:h] + "000" + malformed[h + 3:]
    try:
        decode(malformed)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid zero ID was accepted")
    # A syntactically valid two-bit change is rejected rather than classified
    # as UNSAT, even though a separate exact evaluation proves it is SAT.
    off_star = [(2, 4, 6), (3, 5, 6)]
    off_star_bits = encode(7, off_star)
    check(sum(a != b for a, b in zip(off_star_bits, encode(7, [(3, 5, 6)] * 2))) == 2,
          "off-star control is not a two-bit change")
    off_star_count = count_used_names(7, off_star)[0]
    check(off_star_count > 0 and recognized_count(off_star_bits) is None,
          "UNKNOWN merged with UNSAT")
    multiplicities = Counter(sum(relation(a, b, c) for c in range(5))
                             for a, b in product(range(5), repeat=2))
    check(dict(multiplicities) == {0: 5, 1: 10, 2: 10}, "shared-pair fibers")
    # This is arithmetic bookkeeping, not a compulsory runtime claim.
    frontier = []
    for t in range(7):
        leaves = 4 ** t
        assignments = 2 ** (15 - 2 * t)
        check(leaves * assignments == 2 ** 15, "branch conservation")
        frontier.append({"levels": t, "leaves": leaves,
                         "assignments_per_leaf": assignments,
                         "total_assignments": leaves * assignments})
    return {"m1_count_unchanged": count0, "slot_permutation_count": count_used_names(n, a)[0],
            "unsat_count": 0, "invalid_id_rejected": True,
            "off_star_status": "UNKNOWN", "off_star_independent_count": off_star_count,
            "shared_pair_fiber_histogram": dict(sorted(multiplicities.items())),
            "boolean_15_variable_branch_control": frontier}


def main():
    parameter_list = [(w, m) for w in range(3, 7) for m in (2, (1 << w) - 1)]
    parameter_list.append((4, 20))
    rows = [audit_parameters(w, m) for w, m in parameter_list]
    result = {"lemma": "T5-PAYLOAD-SUPPORT1", "status": "PASS",
              "scope": "Finite valid-encoding sensitivity audit; no unrestricted superpolynomial bound",
              "relation": "symmetric strict C, all permutations of 012,123,234,340,401",
              "encoding": "1^n 0 gamma(m+1), then m triples of one-based w-bit IDs",
              "seed": None, "mode": "exhaustive over all payload bit positions for the listed n,m",
              "code_sha256": sha256(Path(__file__).read_bytes()).hexdigest(),
              "total_one_bit_pairs": sum(len(r["one_bit_pairs"]) for r in rows),
              "full_enumeration_checks": sum(r["full_enumeration_checks"] for r in rows),
              "cases": rows, "controls": controls()}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
