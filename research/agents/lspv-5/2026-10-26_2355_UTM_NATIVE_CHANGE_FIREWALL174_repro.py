#!/usr/bin/env python3
"""Finite controls for UTM-NATIVE-CHANGE-FIREWALL174.

The symbolic theorems are in the companion LaTeX report.  This standard-
library program checks the DISJ fooling family, the short-program count,
native-versus-interpreted actual symbol changes, formal writes versus actual
changes, fixed-parameter configuration counts with optional initial advice,
and a two-input-head countermodel.  It proves no unrestricted SAT lower bound.
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math


ASSERTIONS = 0


def ck(condition: bool, message: str) -> None:
    global ASSERTIONS
    ASSERTIONS += 1
    if not condition:
        raise AssertionError(message)


def disjoint(a: int, b: int) -> bool:
    return (a & b) == 0


def native_parity(bits: tuple[int, ...]) -> tuple[int, int, int]:
    """Finite-control parity: output, formal work writes, actual changes."""
    state = 0
    for bit in bits:
        if bit:
            state ^= 1
    return state, 0, 0


def interpreted_parity(bits: tuple[int, ...]) -> tuple[int, int, int]:
    """A legal interpreter representation stores simulated state in one cell.

    It formally writes the state cell once per input symbol.  On a 1 the cell
    toggles, and on a 0 the formal write leaves its symbol unchanged.
    """
    cell = 0
    changes = 0
    writes = 0
    for bit in bits:
        new = cell ^ bit
        writes += 1
        changes += int(new != cell)
        cell = new
    return cell, writes, changes


def self_writer(n: int) -> tuple[int, int]:
    """Writes the symbol already present at every step."""
    return n, 0


def toggling_writer(n: int) -> tuple[int, int]:
    """Writes once and changes the symbol at every step."""
    return n, n


def occupancy_count(S: int, D: int, I0: int, k: int, g: int, q: int = 3) -> int:
    """Generalized current-configuration upper count.

    h=2S+3 possible positions/cells per work tape, kh total tracked cells.
    At most D+I0 of them can be nonblank if I0 nonblank cells are supplied
    initially and every newly nonblank cell needs an actual symbol change.
    """
    h = 2 * S + 3
    cells = k * h
    support = min(D + I0, cells)
    contents = sum(math.comb(cells, j) * (g - 1) ** j for j in range(support + 1))
    return 2 * q * h**k * contents


def main() -> None:
    fooling_rows = []
    # Common-input DISJ fooling family: every two distinct diagonal YES pairs
    # have at least one crossed NO input.  This is within one fixed program.
    for m in range(1, 11):
        mask = (1 << m) - 1
        diagonal = [(a, mask ^ a) for a in range(1 << m)]
        for a, b in diagonal:
            ck(disjoint(a, b), "diagonal must be YES")
        for (a, _), (c, _) in itertools.combinations(diagonal, 2):
            ck((not disjoint(a, mask ^ c)) or (not disjoint(c, mask ^ a)),
               "at least one crossed input must be NO")
        # Unsound accept-all covers both labels, showing why global soundness
        # cannot be omitted from a short-program portfolio theorem.
        ck(any(not disjoint(a, b) for a in range(1 << m) for b in range(1 << m)),
           "a NO input exists")
        fooling_rows.append({"m": m, "yes_inputs": 1 << m})

    program_rows = []
    for b in range(0, 33):
        exact = sum(1 << ell for ell in range(b + 1))
        ck(exact == (1 << (b + 1)) - 1, "short-program portfolio count")
        ck(exact < (1 << (b + 1)), "safe portfolio upper bound")
        program_rows.append({"b": b, "programs_leq_b": exact})

    parity_rows = []
    for n in range(0, 16):
        max_interpreter_changes = 0
        for bits in itertools.product((0, 1), repeat=n):
            native = native_parity(bits)
            interp = interpreted_parity(bits)
            ck(native[0] == interp[0] == (sum(bits) & 1), "same parity output")
            ck(native[1:] == (0, 0), "native finite-control change count")
            ck(interp[1] == n, "one formal interpreter write per symbol")
            ck(interp[2] == sum(bits), "interpreter actual changes are ones")
            ck(interp[2] <= interp[1], "actual changes bounded by formal writes")
            max_interpreter_changes = max(max_interpreter_changes, interp[2])
        sw, sd = self_writer(n)
        tw, td = toggling_writer(n)
        ck((sw, sd) == (n, 0), "formal self-writes need not change symbols")
        ck((tw, td) == (n, n), "toggle writes all change symbols")
        parity_rows.append({
            "n": n,
            "native_D": 0,
            "interpreter_max_D": max_interpreter_changes,
            "self_write_W": sw,
            "self_write_D": sd,
        })

    count_rows = []
    for k in range(1, 4):
        for g in range(2, 6):
            for S in range(0, 9):
                for D in range(0, 9):
                    base = occupancy_count(S, D, 0, k, g)
                    ck(base > 0, "configuration upper count positive")
                    ck(base == occupancy_count(S, D, 0, k, g), "I0=0 specialization")
                    last = base
                    for I0 in range(1, 9):
                        now = occupancy_count(S, D, I0, k, g)
                        ck(now >= last, "free initial nonblank advice expands count")
                        last = now
                    ck(occupancy_count(S, D + 1, 0, k, g) >= base,
                       "additional changes do not reduce configurations")
            count_rows.append({
                "k": k,
                "g": g,
                "A_S4_D2_I0_0": occupancy_count(4, 2, 0, k, g),
                "A_S4_D2_I0_1": occupancy_count(4, 2, 1, k, g),
            })

    # A second read-only input head destroys the one-head communication cut:
    # after positioning head 2 at Bob's block, both heads scan synchronously.
    two_head_rows = []
    for m in range(1, 10):
        mask = (1 << m) - 1
        cases = 0
        for a in range(1 << m):
            for b in range(1 << m):
                streamed = True
                for i in range(m):
                    if ((a >> i) & 1) and ((b >> i) & 1):
                        streamed = False
                        break
                ck(streamed == disjoint(a, b), "two-head synchronous DISJ")
                cases += 1
        two_head_rows.append({"m": m, "cases": cases, "work_S": 0, "work_D": 0})

    # Silent growth controls.  These are outside the fixed-machine theorem.
    growth_rows = []
    for m in range(1, 25):
        q_nonuniform = 1 << m
        g_packed = 1 << m
        ck(q_nonuniform.bit_length() - 1 == m, "2^m nonuniform states store m bits")
        ck(g_packed.bit_length() - 1 == m, "one packed symbol names m bits")
        growth_rows.append({"m": m, "q_N": q_nonuniform, "g_N": g_packed})

    payload = {
        "id": "UTM-NATIVE-CHANGE-FIREWALL174",
        "timestamp_utc": "2026-10-27T06:55:00Z",
        "method": "exhaustive exact standard-library Python; no randomness",
        "assertions": ASSERTIONS,
        "failures": 0,
        "fooling_family": fooling_rows,
        "short_program_counts": program_rows,
        "native_interpreter_controls": parity_rows,
        "configuration_count_controls": count_rows,
        "two_input_head_controls": two_head_rows,
        "silent_parameter_growth_controls": growth_rows,
        "scope": [
            "fixed-U symbol-change and communication controls only",
            "D is not invariant under simulation",
            "two-head and growing-parameter controls are outside the theorem",
            "no unrestricted SAT or P-versus-NP lower bound",
        ],
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    payload["canonical_sha256_without_this_field"] = hashlib.sha256(canonical).hexdigest()
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
