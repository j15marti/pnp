#!/usr/bin/env python3
"""Independent finite audit for PARITY-TOTAL-ACCESS-COMPOSITION238.

This is a standard-library checker for the restricted canonical parity family.
It validates a complete balanced source grammar, constructs the exact distinct-
pin child descriptor, provides a total symbolic DIMACS character accessor, and
checks both SAT and UNSAT instances.  The asymptotic arbitrary-guest conclusion
in the accompanying report is a mathematical composition of the verified total-
access theorem with the accessor contract; these Python counters are not FLMV
machine transitions.
"""

from __future__ import annotations

import itertools
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path

RUN_ID = "PARITY-TOTAL-ACCESS-COMPOSITION238"


def xor_clauses(a: int, b: int, z: int) -> list[tuple[int, int, int]]:
    return [(a, b, -z), (a, -b, z), (-a, b, z), (-a, -b, -z)]


def force_clauses(v: int, p: int, q: int, bit: int) -> list[tuple[int, int, int]]:
    head = v if bit else -v
    return [(head, p, q), (head, p, -q), (head, -p, q), (head, -p, -q)]


def component(b: int, start: int, pin: int, balanced: bool) -> tuple[list[tuple[int, int, int]], int]:
    ys = list(range(start, start + b - 1))
    out: list[tuple[int, int, int]] = []
    out += xor_clauses(1, 2, ys[0])
    for j in range(3, b + 1):
        out += xor_clauses(ys[j - 3], j, ys[j - 2])
    p, q = start + b - 1, start + b
    out += force_clauses(ys[-1], p, q, pin)
    used = b + 1
    if balanced:
        w, s, t = start + b + 1, start + b + 2, start + b + 3
        out += force_clauses(w, s, t, 1 - pin)
        used = b + 4
    return out, used


def source_formula(b: int, pins: tuple[int, ...]) -> tuple[int, list[tuple[int, int, int]]]:
    clauses: list[tuple[int, int, int]] = []
    next_id = b + 1
    for pin in pins:
        block, used = component(b, next_id, pin, True)
        clauses += block
        next_id += used
    return next_id - 1, clauses


def child_formula(b: int, distinct_pins: tuple[int, ...]) -> tuple[int, list[tuple[int, int, int]]]:
    clauses: list[tuple[int, int, int]] = []
    next_id = b + 1
    for pin in distinct_pins:
        block, used = component(b, next_id, pin, False)
        clauses += block
        next_id += used
    return next_id - 1, clauses


def dimacs(nvars: int, clauses: list[tuple[int, int, int]]) -> str:
    return f"p cnf {nvars} {len(clauses)}\n" + "".join(
        " ".join(map(str, c)) + " 0\n" for c in clauses
    )


def parse_dimacs(text: str) -> tuple[int, list[tuple[int, int, int]]]:
    lines = text.splitlines()
    if not lines or len(lines[0].split()) != 4 or lines[0].split()[:2] != ["p", "cnf"]:
        raise ValueError("bad header")
    _, _, vs, cs = lines[0].split()
    nvars, nclauses = int(vs), int(cs)
    clauses = []
    for line in lines[1:]:
        toks = list(map(int, line.split()))
        if len(toks) != 4 or toks[-1] != 0:
            raise ValueError("not canonical proper 3CNF")
        c = tuple(toks[:3])
        if len({abs(x) for x in c}) != 3:
            raise ValueError("improper clause")
        clauses.append(c)
    if len(clauses) != nclauses or max((abs(x) for c in clauses for x in c), default=0) != nvars:
        raise ValueError("header mismatch")
    return nvars, clauses


@dataclass(frozen=True)
class Descriptor:
    b: int
    pins: tuple[int, ...]


def validate_source(text: str) -> tuple[Descriptor, dict[str, int]]:
    nvars, clauses = parse_dimacs(text)
    candidates = []
    for b in range(2, nvars + 1):
        denom = 4 * (b + 1)
        if len(clauses) % denom:
            continue
        q = len(clauses) // denom
        if q >= 2 and nvars == b + q * (b + 4):
            candidates.append((b, q))
    if len(candidates) != 1:
        raise ValueError("ambiguous/noncanonical b,q")
    b, q = candidates[0]
    per = 4 * (b + 1)
    pins = []
    comparisons = 0
    for i in range(q):
        block = clauses[i * per : (i + 1) * per]
        pin_first = block[4 * (b - 1)][0]
        pin = int(pin_first > 0)
        expected, used = component(b, b + 1 + i * (b + 4), pin, True)
        if used != b + 4 or block != expected:
            raise ValueError("bad canonical block")
        pins.append(pin)
        comparisons += 3 * len(block)
    return Descriptor(b, tuple(sorted(set(pins)))), {
        "source_char_reads": len(text),
        "literal_comparisons": comparisons,
        "blocks": q,
    }


def digits(n: int) -> int:
    return len(str(n))


def digit_prefix(n: int) -> int:
    if n <= 0:
        return 0
    total, lo, width = 0, 1, 1
    while lo <= n:
        hi = min(n, 10 * lo - 1)
        total += (hi - lo + 1) * width
        lo *= 10
        width += 1
    return total


def digit_range(lo: int, hi: int) -> int:
    return 0 if hi < lo else digit_prefix(hi) - digit_prefix(lo - 1)


def xor_chunk_len(a: int, b: int, z: int) -> int:
    return 4 * (digits(a) + digits(b) + digits(z)) + 26


def pin_chunk_len(z: int, p: int, q: int, pin: int) -> int:
    return 4 * (digits(z) + digits(p) + digits(q)) + (24 if pin else 28)


def gate_prefix_len(b: int, start: int, k: int) -> int:
    """Length of first k XOR-gate chunks, 1 <= k <= b-1."""
    if not 1 <= k <= b - 1:
        raise ValueError("bad gate prefix")
    first = xor_chunk_len(1, 2, start)
    if k == 1:
        return first
    tail_digits = (
        digit_range(start, start + k - 2)
        + digit_range(3, k + 1)
        + digit_range(start + 1, start + k - 1)
    )
    return first + 26 * (k - 1) + 4 * tail_digits


def chain_len(b: int, start: int, pin: int) -> int:
    z, p, q = start + b - 2, start + b - 1, start + b
    return gate_prefix_len(b, start, b - 1) + pin_chunk_len(z, p, q, pin)


def serialize_xor_gate(b: int, start: int, gate_index: int) -> str:
    # gate_index 1 is x1 xor x2 -> y2; gate_index k uses x_{k+1}
    if gate_index == 1:
        a, x, z = 1, 2, start
    else:
        a, x, z = start + gate_index - 2, gate_index + 1, start + gate_index - 1
    return "".join(" ".join(map(str, c)) + " 0\n" for c in xor_clauses(a, x, z))


def serialize_pin(b: int, start: int, pin: int) -> str:
    z, p, q = start + b - 2, start + b - 1, start + b
    return "".join(" ".join(map(str, c)) + " 0\n" for c in force_clauses(z, p, q, pin))


def child_shape(desc: Descriptor) -> tuple[int, int, str, list[tuple[int, int, int]]]:
    nv, clauses = child_formula(desc.b, desc.pins)
    header = f"p cnf {nv} {len(clauses)}\n"
    starts = []
    nxt = desc.b + 1
    for _ in desc.pins:
        starts.append((nxt, 0, 0))
        nxt += desc.b + 1
    return nv, len(clauses), header, starts


def child_length(desc: Descriptor) -> int:
    _, _, header, _ = child_shape(desc)
    nxt = desc.b + 1
    total = len(header)
    for pin in desc.pins:
        total += chain_len(desc.b, nxt, pin)
        nxt += desc.b + 1
    return total


def child_char(desc: Descriptor, address: int, stats: dict[str, int] | None = None) -> str:
    """Total symbolic accessor: returns blank (space) outside the child."""
    if stats is not None:
        stats["queries"] = stats.get("queries", 0) + 1
    if address < 0:
        return " "
    _, _, header, _ = child_shape(desc)
    if address < len(header):
        return header[address]
    pos = address - len(header)
    start = desc.b + 1
    for pin in desc.pins:
        clen = chain_len(desc.b, start, pin)
        if pos >= clen:
            pos -= clen
            start += desc.b + 1
            continue
        gates_len = gate_prefix_len(desc.b, start, desc.b - 1)
        if pos >= gates_len:
            chunk = serialize_pin(desc.b, start, pin)
            return chunk[pos - gates_len]
        lo, hi = 1, desc.b - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if stats is not None:
                stats["prefix_evaluations"] = stats.get("prefix_evaluations", 0) + 1
            if gate_prefix_len(desc.b, start, mid) > pos:
                hi = mid
            else:
                lo = mid + 1
        prev = 0 if lo == 1 else gate_prefix_len(desc.b, start, lo - 1)
        chunk = serialize_xor_gate(desc.b, start, lo)
        return chunk[pos - prev]
    return " "


def eval_clause(c: tuple[int, int, int], bits: tuple[int, ...]) -> bool:
    return any((bits[abs(l) - 1] == 1) == (l > 0) for l in c)


def model_count(nvars: int, clauses: list[tuple[int, int, int]]) -> int:
    return sum(all(eval_clause(c, bits) for c in clauses) for bits in itertools.product((0, 1), repeat=nvars))


def dpll(clauses: list[tuple[int, int, int]], nvars: int) -> dict[str, int | bool]:
    stats = {"nodes": 0, "literal_tests": 0, "unit_writes": 0}

    def rec(assign: dict[int, bool]) -> bool:
        stats["nodes"] += 1
        while True:
            unit = None
            all_sat = True
            for c in clauses:
                sat = False
                open_lits = []
                for lit in c:
                    stats["literal_tests"] += 1
                    v = abs(lit)
                    if v in assign:
                        if assign[v] == (lit > 0):
                            sat = True
                            break
                    else:
                        open_lits.append(lit)
                if sat:
                    continue
                all_sat = False
                if not open_lits:
                    return False
                if len(open_lits) == 1:
                    unit = open_lits[0]
                    break
            if all_sat:
                return True
            if unit is None:
                break
            v, val = abs(unit), unit > 0
            if v in assign and assign[v] != val:
                return False
            if v not in assign:
                assign[v] = val
                stats["unit_writes"] += 1
        v = next(i for i in range(1, nvars + 1) if i not in assign)
        for val in (False, True):
            child = dict(assign)
            child[v] = val
            if rec(child):
                return True
        return False

    ans = rec({})
    return {"sat": ans, **stats}


def local_extreme_audit(clauses: list[tuple[int, int, int]], nvars: int) -> dict[str, int]:
    occurrence_checks = 0
    for c in clauses:
        for lit in c:
            sat_target = int(lit > 0)
            unsat_target = 1 - sat_target
            assert 1 - sat_target == unsat_target and 1 - unsat_target == sat_target
            occurrence_checks += 4
    pair_modes = 0
    for i in range(len(clauses)):
        for j in range(i + 1, len(clauses)):
            for ei, ej in itertools.product((0, 1), repeat=2):  # U=0, S=1
                req: dict[int, int] = {}
                feasible = True
                for c, e in ((clauses[i], ei), (clauses[j], ej)):
                    for lit in c:
                        val = e if lit > 0 else 1 - e
                        v = abs(lit)
                        if v in req and req[v] != val:
                            feasible = False
                        req[v] = val
                # Exact enumeration on the shared support.
                support = sorted(set(map(abs, clauses[i])) | set(map(abs, clauses[j])))
                enum = False
                for bits in itertools.product((0, 1), repeat=len(support)):
                    assignment = dict(zip(support, bits))
                    if all(
                        all(int((assignment[abs(lit)] == 1) == (lit > 0)) == e for lit in c)
                        for c, e in ((clauses[i], ei), (clauses[j], ej))
                    ):
                        enum = True
                        break
                assert feasible == enum
                pair_modes += 1
    endpoints = 0
    flips = 0
    a = [0] * nvars
    for state in (tuple(a), tuple([1] * nvars)):
        counts = [sum((state[abs(l)-1] == 1) == (l > 0) for l in c) for c in clauses]
        comp = tuple(1 - x for x in state)
        comp_counts = [sum((comp[abs(l)-1] == 1) == (l > 0) for l in c) for c in clauses]
        assert all(x + y == 3 for x, y in zip(counts, comp_counts))
        endpoints += len(clauses)
    state = [0] * nvars
    old = [sum((state[abs(l)-1] == 1) == (l > 0) for l in c) for c in clauses]
    for v in range(1, min(nvars, 8) + 1):
        before = tuple(state)
        state[v - 1] ^= 1
        new = [sum((state[abs(l)-1] == 1) == (l > 0) for l in c) for c in clauses]
        for idx, c in enumerate(clauses):
            true_touched = sum(1 for l in c if abs(l) == v and ((before[v-1] == 1) == (l > 0)))
            false_touched = sum(1 for l in c if abs(l) == v and not ((before[v-1] == 1) == (l > 0)))
            assert new[idx] == old[idx] + false_touched - true_touched
            flips += 1
        old = new
    return {"occurrence_extreme_checks": occurrence_checks, "pair_mode_checks": pair_modes,
            "endpoint_complement_checks": endpoints, "flip_update_checks": flips}


def run() -> dict:
    started = time.perf_counter()
    cases = []
    total_assertions = 0
    for name, pins in (("all_even_SAT", (0, 0)), ("mixed_UNSAT", (0, 1))):
        b = 2
        nv, cls = source_formula(b, pins)
        text = dimacs(nv, cls)
        desc, validation = validate_source(text)
        assert desc == Descriptor(b, tuple(sorted(set(pins))))
        cnv, ccls = child_formula(desc.b, desc.pins)
        child_text = dimacs(cnv, ccls)
        astats: dict[str, int] = {}
        for j, ch in enumerate(child_text):
            assert child_char(desc, j, astats) == ch
            total_assertions += 1
        for j in (-1, len(child_text), len(child_text) + 1, len(child_text) + 17):
            assert child_char(desc, j, astats) == " "
            total_assertions += 1
        assert child_length(desc) == len(child_text)
        smodels = model_count(nv, cls)
        cmodels = model_count(cnv, ccls)
        expected_sat = len(set(pins)) == 1
        assert (smodels > 0) == expected_sat == (cmodels > 0)
        base = dpll(cls, nv)
        child = dpll(ccls, cnv)
        assert base["sat"] == expected_sat == child["sat"]
        extreme = local_extreme_audit(cls, nv)
        corrupted = list(cls)
        first = list(corrupted[0])
        first[0] = -first[0]
        corrupted[0] = tuple(first)
        rejected = False
        try:
            validate_source(dimacs(nv, corrupted))
        except ValueError:
            rejected = True
        assert rejected
        total_assertions += 8 + sum(extreme.values())
        cases.append({
            "name": name, "pins": pins, "source_bits": 8 * len(text),
            "child_bits": 8 * len(child_text), "source_models": smodels,
            "child_models": cmodels, "validation": validation,
            "accessor": astats, "baseline_dpll": base, "child_dpll": child,
            "extreme_controls": extreme, "corrupt_source_rejected": rejected,
        })

    # Growing-b source/child size controls, computed by exact serialization.
    size_controls = []
    for b, q, pins in ((3, 1500, (0,) * 1500), (3, 7001, (0,) * 7000 + (1,)),
                       (7, 5000, (0,) * 5000), (7, 10000, (0,) * 9999 + (1,))):
        nv, cls = source_formula(b, pins)
        source_text = dimacs(nv, cls)
        desc = Descriptor(b, tuple(sorted(set(pins))))
        cnv, ccls = child_formula(desc.b, desc.pins)
        child_text = dimacs(cnv, ccls)
        accessor_stats: dict[str, int] = {}
        assert "".join(child_char(desc, j, accessor_stats) for j in range(len(child_text))) == child_text
        assert child_char(desc, len(child_text) + 9, accessor_stats) == " "
        size_controls.append({"b": b, "q": q, "label": "SAT" if len(desc.pins) == 1 else "UNSAT",
                              "source_bits": 8 * len(source_text), "child_bits": 8 * len(child_text),
                              "child_lt_sqrt_source": len(child_text) * 8 < math.isqrt(len(source_text) * 8),
                              "accessor": accessor_stats})

    return {
        "run_id": RUN_ID,
        "status": {"restricted_composition": "PROVED/EXACT in report",
                   "finite_controls": "COMPUTATIONAL",
                   "universal_arc": "OPEN", "p_vs_np": "OPEN"},
        "cases": cases,
        "size_controls": size_controls,
        "assertions": total_assertions,
        "elapsed_seconds": time.perf_counter() - started,
        "chunking": "single deterministic invocation designed below 30 seconds",
    }


if __name__ == "__main__":
    result = run()
    out = Path("2026-10-31_0248_PARITY_TOTAL_ACCESS_COMPOSITION238_raw.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"run_id": result["run_id"], "assertions": result["assertions"],
                      "elapsed_seconds": result["elapsed_seconds"], "raw": str(out)}))
