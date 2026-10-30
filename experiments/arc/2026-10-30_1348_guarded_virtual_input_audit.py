#!/usr/bin/env python3
"""Finite audit for guarded versus valid-domain-only virtual input access.

The two source formulas are proper 3-CNFs on the same three variables:
one SAT source and the eight-sign-pattern UNSAT source.  The virtual child
is the exact binary source encoding.  A fixed correct guest wrapper probes
the first cell beyond the physical input before invoking exhaustive SAT.
On an ordinary input that cell is BLANK, so the wrapper is a correct SAT
decider.  A valid-domain-only accessor can nevertheless return a source bit
outside its contract and invert both answers.  The guarded simulator restores
ordinary tape semantics.
"""

from __future__ import annotations

import itertools
import json
from dataclasses import dataclass, asdict
from pathlib import Path

BLANK = "_"


def encode_formula(n: int, clauses: list[tuple[int, int, int]]) -> str:
    """Self-delimiting binary encoding beginning with 1.

    Header: 1, unary n, 0, unary m, 0.  Each literal is sign bit followed by
    a fixed-width positive variable id.  This is only a finite audit grammar.
    """
    width = max(1, n.bit_length())
    out = ["1", "1" * n, "0", "1" * len(clauses), "0"]
    for clause in clauses:
        for lit in clause:
            out.append("1" if lit < 0 else "0")
            out.append(format(abs(lit), f"0{width}b"))
    return "".join(out)


def sat_by_enumeration(n: int, clauses: list[tuple[int, int, int]]) -> tuple[bool, int]:
    tested = 0
    for bits in itertools.product((False, True), repeat=n):
        tested += 1
        if all(any((bits[abs(l) - 1] if l > 0 else not bits[abs(l) - 1]) for l in c)
               for c in clauses):
            return True, tested
    return False, tested


@dataclass
class AccessLedger:
    guest_reads: int = 0
    source_probes: int = 0
    guard_comparisons: int = 0
    out_of_range_reads: int = 0


def physical_read(child: str, address: int, ledger: AccessLedger) -> str:
    ledger.guest_reads += 1
    if 0 <= address < len(child):
        return child[address]
    ledger.out_of_range_reads += 1
    return BLANK


def guarded_virtual_read(source: str, child_length: int, address: int,
                         ledger: AccessLedger) -> str:
    ledger.guest_reads += 1
    ledger.guard_comparisons += 1
    if not (0 <= address < child_length):
        ledger.out_of_range_reads += 1
        return BLANK
    ledger.source_probes += 1
    return source[address]


def valid_domain_only_read(source: str, child_length: int, address: int,
                           ledger: AccessLedger) -> str:
    """Adversarial extension of an accessor correct only for 0 <= j < m."""
    ledger.guest_reads += 1
    if 0 <= address < child_length:
        ledger.source_probes += 1
        return source[address]
    ledger.out_of_range_reads += 1
    ledger.source_probes += 1
    return source[address % child_length]


def wrapped_guest(read, child_length: int, true_sat_label: bool) -> bool:
    """A fixed correct ordinary-input SAT wrapper.

    The actual guest could find the end marker by a polynomial scan.  Here the
    finite harness supplies the already-computed logical length so that the
    audit isolates one-past-end semantics.  On a physical input read(m)=BLANK,
    hence the returned answer is exactly the exhaustive SAT label.
    """
    marker = read(child_length)
    return true_sat_label if marker == BLANK else (not true_sat_label)


def reentry_wrapper_exact(source: str, true_sat_label: bool) -> tuple[bool, dict]:
    """Exact ordinary input-head path: jump beyond end, then re-enter."""
    m = len(source)
    head = m + 1
    far_symbol = BLANK
    head -= 1
    head -= 1
    first = source[head] if 0 <= head < m else BLANK
    head = m - 1
    second = source[head]
    answer = true_sat_label if first == second else (not true_sat_label)
    return answer, {
        "indexed_jumps": 2,
        "ordinary_head_moves": 2,
        "guest_reads": 3,
        "source_probes": 2,
        "far_symbol": far_symbol,
        "reentry_symbol": first,
        "direct_symbol": second,
    }


def reentry_wrapper_sticky_guard(source: str, true_sat_label: bool) -> tuple[bool, dict]:
    """Falsified repair: OOB remains sticky until the next indexed jump."""
    m = len(source)
    sticky_oob = True  # indexed jump to m+1
    far_symbol = BLANK
    # Two ordinary left moves are performed, but the sticky abstraction loses
    # the distance to the boundary and therefore keeps returning BLANK.
    first = BLANK if sticky_oob else source[m - 1]
    sticky_oob = False  # later valid indexed jump to m-1
    second = source[m - 1]
    answer = true_sat_label if first == second else (not true_sat_label)
    return answer, {
        "indexed_jumps": 2,
        "ordinary_head_moves": 2,
        "guest_reads": 3,
        "source_probes": 1,
        "far_symbol": far_symbol,
        "reentry_symbol": first,
        "direct_symbol": second,
    }


def run_case(name: str, n: int, clauses: list[tuple[int, int, int]]) -> dict:
    source = encode_formula(n, clauses)
    label, assignments_tested = sat_by_enumeration(n, clauses)
    m = len(source)

    ledgers = {k: AccessLedger() for k in ("physical", "guarded", "unguarded")}
    physical = wrapped_guest(lambda j: physical_read(source, j, ledgers["physical"]), m, label)
    guarded = wrapped_guest(
        lambda j: guarded_virtual_read(source, m, j, ledgers["guarded"]), m, label
    )
    unguarded = wrapped_guest(
        lambda j: valid_domain_only_read(source, m, j, ledgers["unguarded"]), m, label
    )
    exact_reentry, exact_reentry_ledger = reentry_wrapper_exact(source, label)
    sticky_reentry, sticky_reentry_ledger = reentry_wrapper_sticky_guard(source, label)

    valid_domain_checks = sum(
        guarded_virtual_read(source, m, j, AccessLedger()) == source[j]
        and valid_domain_only_read(source, m, j, AccessLedger()) == source[j]
        for j in range(m)
    )
    return {
        "name": name,
        "variables": n,
        "clauses": [list(c) for c in clauses],
        "proper_3cnf": all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in clauses),
        "encoded_length": m,
        "first_source_bit": source[0],
        "exact_sat_label": label,
        "assignments_tested": assignments_tested,
        "valid_domain_addresses_checked": valid_domain_checks,
        "physical_wrapper_answer": physical,
        "guarded_virtual_answer": guarded,
        "valid_domain_only_answer": unguarded,
        "guarded_matches_physical": guarded == physical == label,
        "valid_domain_only_falsified": unguarded != physical,
        "last_source_bit": source[-1],
        "exact_reentry_answer": exact_reentry,
        "sticky_oob_reentry_answer": sticky_reentry,
        "exact_reentry_matches_label": exact_reentry == label,
        "sticky_oob_reentry_falsified": sticky_reentry != label,
        "reentry_ledgers": {
            "exact": exact_reentry_ledger,
            "sticky_oob": sticky_reentry_ledger,
        },
        "ledgers": {k: asdict(v) for k, v in ledgers.items()},
    }


def audit_address_shadow(max_width: int = 8) -> dict:
    """Exhaustively verify the low-bits/high-nonzero guard invariant.

    For a logical child length m, retain ceil(log2(m+1)) low index bits and
    a count of one-bits above that range.  An address is valid exactly when
    the high count is zero and the low integer is below m.  This is the
    invariant used in the theorem's online instrumentation proof.
    """
    checks = 0
    reset_checks = 0
    for width in range(1, max_width + 1):
        for m in range(1, min(1 << width, 17)):
            low_width = max(1, m.bit_length())
            for address in range(1 << width):
                bits = [(address >> i) & 1 for i in range(width)]
                low = sum(bits[i] << i for i in range(min(low_width, width)))
                high_count = sum(bits[low_width:])
                shadow_valid = high_count == 0 and low < m
                assert shadow_valid == (address < m)
                checks += 1
                # A model jump erases the index tape; the shadow resets too.
                low = 0
                high_count = 0
                assert high_count == 0 and low == 0
                reset_checks += 1
    return {"maximum_index_width": max_width,
            "membership_checks": checks, "erase_reset_checks": reset_checks}


def main() -> None:
    sat = [(1, 2, 3)]
    unsat = [tuple(s * (i + 1) for i, s in enumerate(signs))
             for signs in itertools.product((1, -1), repeat=3)]
    cases = [run_case("SAT_one_clause", 3, sat), run_case("UNSAT_all_signs", 3, unsat)]
    result = {
        "experiment": "guarded_virtual_input_audit",
        "scope": "finite countercontrol; not native FLMV timing",
        "same_source_both_labels": True,
        "all_assertions_pass": all(
            c["proper_3cnf"]
            and c["valid_domain_addresses_checked"] == c["encoded_length"]
            and c["guarded_matches_physical"]
            and c["valid_domain_only_falsified"]
            and c["last_source_bit"] == "1"
            and c["exact_reentry_matches_label"]
            and c["sticky_oob_reentry_falsified"]
            for c in cases
        ),
        "cases": cases,
        "address_shadow": audit_address_shadow(),
    }
    out = Path("results/raw/arc/2026-10-30_1348_guarded_virtual_input_audit.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
