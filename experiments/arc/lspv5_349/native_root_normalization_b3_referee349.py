#!/usr/bin/env python3
"""REFEREE349 finite audit: native root-only normalization and trace firewall.

The symbolic theorem is in the companion report.  This executable checks the
smallest internal-wire counterexample, root truth-table normalization on many
circuits, paid fresh-definition semantics, basic typed native records, and the
rejecting-trace/correctness separation.  It does not decide B3.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import resource
import time
from pathlib import Path


CHECKS = 0


def check(ok: bool, msg: str) -> None:
    global CHECKS
    if not ok:
        raise AssertionError(msg)
    CHECKS += 1


def assignments(s: int):
    for a in range(1 << s):
        yield tuple((a >> i) & 1 for i in range(s))


def eval_circuit(gates: list[dict], bits: tuple[int, ...]) -> list[int]:
    vals: list[int] = []
    for i, g in enumerate(gates):
        op = g.get("op")
        if op == "IN":
            j = g.get("i")
            if not isinstance(j, int) or not (0 <= j < len(bits)):
                raise ValueError("bad input")
            vals.append(bits[j])
        elif op == "CONST":
            b = g.get("b")
            if type(b) is not int or b not in (0, 1):
                raise ValueError("bad constant")
            vals.append(b)
        elif op == "NOT":
            p = g.get("p")
            if not isinstance(p, int) or not (0 <= p < i):
                raise ValueError("bad NOT parent")
            vals.append(1 - vals[p])
        elif op in ("AND", "OR", "XOR"):
            p, q = g.get("p"), g.get("q")
            if not all(isinstance(x, int) and 0 <= x < i for x in (p, q)):
                raise ValueError("bad binary parents")
            if op == "AND":
                vals.append(vals[p] & vals[q])
            elif op == "OR":
                vals.append(vals[p] | vals[q])
            else:
                vals.append(vals[p] ^ vals[q])
        else:
            raise ValueError("bad opcode")
    if not vals:
        raise ValueError("empty circuit")
    return vals


def truth_vector(gates: list[dict], support: int, gate: int | None = None) -> list[int]:
    out = []
    for a in assignments(support):
        vals = eval_circuit(gates, a)
        j = len(vals) - 1 if gate is None else gate
        if not isinstance(j, int) or not (0 <= j < len(vals)):
            raise ValueError("bad exported gate")
        out.append(vals[j])
    return out


def implication(parent: list[int], child: list[int]) -> bool:
    return len(parent) == len(child) and all(not p or c for p, c in zip(parent, child))


def random_circuit(rng: random.Random, support: int, gates_n: int) -> list[dict]:
    gates = [{"op": "IN", "i": i} for i in range(support)]
    while len(gates) < max(support, gates_n):
        i = len(gates)
        op = rng.choice(("NOT", "AND", "OR", "XOR", "CONST"))
        if op == "NOT":
            gates.append({"op": op, "p": rng.randrange(i)})
        elif op == "CONST":
            gates.append({"op": op, "b": rng.randrange(2)})
        else:
            gates.append({"op": op, "p": rng.randrange(i), "q": rng.randrange(i)})
    return gates


def normalize_root(gates: list[dict], support: int) -> dict:
    if not (0 <= support <= 3):
        raise ValueError("native fixed-support audit uses at most three inputs")
    return {"kind": "ROOT_TABLE", "support": support, "table": truth_vector(gates, support)}


def eval_table(record: dict, bits: tuple[int, ...]) -> int:
    s = record["support"]
    if len(bits) != s or len(record["table"]) != 1 << s:
        raise ValueError("bad table")
    idx = sum(b << i for i, b in enumerate(bits))
    return record["table"][idx]


def verify_native_record(rec: dict, var_bound: int, prior: int) -> bool:
    """Small typed checker mirroring the five native record shapes."""
    try:
        op = rec["op"]
        parents = rec.get("parents", [])
        if len(parents) > 2 or any(type(p) is not int or not (0 <= p < prior) for p in parents):
            return False
        if op == "RES":
            if len(parents) != 2 or type(rec.get("pivot")) is not int:
                return False
            clause = rec.get("clause")
            return isinstance(clause, list) and all(type(x) is int and 1 <= abs(x) <= var_bound for x in clause)
        if op == "AND3":
            return len(parents) == 2 and 0 <= rec.get("support", 99) <= 3 and len(rec.get("table", [])) == 1 << rec["support"]
        if op == "XOR":
            return len(parents) == 2 and isinstance(rec.get("mask"), str) and len(rec["mask"]) == var_bound and set(rec["mask"]) <= {"0", "1"} and rec.get("rhs") in (0, 1)
        if op == "LOCAL-CONVERT":
            return len(parents) == 1 and 0 <= rec.get("support", 99) <= 3 and len(rec.get("table", [])) == 1 << rec["support"]
        if op == "DEF":
            return len(parents) <= 2 and rec.get("fresh") == var_bound + 1 and rec.get("gate") in ("AND", "OR", "XOR", "NAND", "NOR", "XNOR")
        return False
    except (KeyError, TypeError):
        return False


def normalized_bit_bound(source_bits: int, original_vars: int, q: int, c: int = 3) -> int:
    """Conservative bit bound for q typed root-only native records."""
    v = max(1, original_vars + q)
    id_bits = max(1, math.ceil(math.log2(v + q + 2)))
    per = 8 + 2 * id_bits + 2 * v * (id_bits + 1) + v + (1 << c)
    return source_bits + q * per


def parse_tiny_cnf(source: str) -> tuple[int, list[list[int]]]:
    lines = source.splitlines()
    if not lines or len(lines[0].split()) != 4 or lines[0].split()[:2] != ["p", "cnf"]:
        raise ValueError("header")
    n, m = map(int, lines[0].split()[2:])
    if n < 0 or m < 0 or len(lines) != m + 1:
        raise ValueError("counts")
    clauses = []
    for line in lines[1:]:
        xs = list(map(int, line.split()))
        if not xs or xs[-1] != 0 or any(x == 0 or abs(x) > n for x in xs[:-1]):
            raise ValueError("clause")
        clauses.append(xs[:-1])
    return n, clauses


def sat(source: str) -> bool:
    n, clauses = parse_tiny_cnf(source)
    return any(all(any(((a >> (abs(l)-1)) & 1) == (l > 0) for l in c) for c in clauses) for a in range(1 << n))


def local_trace(machine: str, source: str) -> list[dict]:
    parse_tiny_cnf(source)
    if machine == "REJECT_ALL":
        label = "UNSAT"
    elif machine == "BRUTE_FORCE":
        label = "SAT" if sat(source) else "UNSAT"
    else:
        raise ValueError("machine")
    return [{"state": "START", "machine": machine}, {"state": "HALT", "label": label}]


def trace_locally_valid(machine: str, trace: list[dict]) -> bool:
    return trace == [trace[0], trace[1]] and trace[0] == {"state": "START", "machine": machine} and trace[1].get("state") == "HALT" and trace[1].get("label") in ("SAT", "UNSAT")


def main() -> None:
    started = time.perf_counter()
    # Minimal internal-wire assertion counterexample: root = not(not x) = x.
    gates = [{"op": "IN", "i": 0}, {"op": "NOT", "p": 0}, {"op": "NOT", "p": 1}]
    parent = [0, 1]  # condition x
    root = truth_vector(gates, 1)
    internal = truth_vector(gates, 1, 1)
    check(root == [0, 1], "double-negation root")
    check(internal == [1, 0], "internal negated wire")
    check(implication(parent, root), "root conversion legal")
    check(not implication(parent, internal), "internal assertion illegal")
    check(not any(p and w for p, w in zip(parent, internal)), "x and internal-not-x inconsistent")

    normalized = normalize_root(gates, 1)
    for a in assignments(1):
        check(eval_table(normalized, a) == eval_circuit(gates, a)[-1], "root normalization")

    # Root-only truth-table normalization on explicit circuits of support <=3.
    rng = random.Random(349)
    circuit_records = []
    for support in (1, 2, 3):
        for length in (support + 1, support + 2, 8, 17, 33):
            for rep in range(25):
                c = random_circuit(rng, support, length)
                t = normalize_root(c, support)
                for a in assignments(support):
                    check(eval_table(t, a) == eval_circuit(c, a)[-1], "random root table")
                circuit_records.append({"support": support, "gates": len(c), "table": t["table"]})

    # Exact fresh definition is a value relation, not an assertion that its output is true.
    for x in (0, 1):
        w = 1 - x
        check((x, w) in ((0, 1), (1, 0)), "fresh NOT unique extension")
    check((1, 0) == (1, 1 - 1), "source x extends with w=0")

    native = [
        {"op": "RES", "parents": [0, 1], "pivot": 1, "clause": []},
        {"op": "AND3", "parents": [0, 1], "support": 1, "table": [0, 1]},
        {"op": "XOR", "parents": [0, 1], "mask": "101", "rhs": 1},
        {"op": "LOCAL-CONVERT", "parents": [0], "support": 1, "table": [0, 1]},
        {"op": "DEF", "parents": [0], "fresh": 4, "gate": "AND"},
    ]
    for rec in native:
        check(verify_native_record(rec, 3, 2), f"valid native {rec['op']}")
    malformed = [dict(native[0], parents=[2, 0]), dict(native[1], support=4), dict(native[2], mask="10x"), dict(native[3], table=[1]), dict(native[4], fresh=3), {"op": "ORACLE", "parents": []}]
    for rec in malformed:
        check(not verify_native_record(rec, 3, 2), "malformed native rejected")

    bounds = []
    for n in (1, 4, 16, 64, 256):
        prev = 0
        for q in (1, 2, 4, 16, 64):
            b = normalized_bit_bound(16 * n, n, q)
            check(b >= 16 * n and b >= prev, "polynomial bound monotone")
            prev = b
            bounds.append({"n": n, "q": q, "bits": b})

    sat_unit = "p cnf 1 1\n1 0\n"
    unsat_units = "p cnf 1 2\n1 0\n-1 0\n"
    check(sat(sat_unit), "SAT control")
    check(not sat(unsat_units), "UNSAT control")
    bad_reject = local_trace("REJECT_ALL", sat_unit)
    good_reject = local_trace("BRUTE_FORCE", unsat_units)
    check(trace_locally_valid("REJECT_ALL", bad_reject), "reject-all trace locally valid")
    check(bad_reject[-1]["label"] == "UNSAT" and sat(sat_unit), "trace-only compiler unsound witness")
    check(trace_locally_valid("BRUTE_FORCE", good_reject), "correct reject trace valid")
    check(good_reject[-1]["label"] == "UNSAT" and not sat(unsat_units), "correct reject control")
    malformed_sources = ["", "p cnf 1 1\n1\n", "p cnf 1 2\n1 0\n", "p cnf 1 1\n2 0\n", "p sat 1 1\n1 0\n"]
    for src in malformed_sources:
        try:
            local_trace("BRUTE_FORCE", src)
            check(False, "malformed accepted")
        except (ValueError, IndexError):
            check(True, "malformed rejected")

    elapsed = time.perf_counter() - started
    out = {
        "report": "REFEREE349",
        "status": {"normalization": "PROVED under strict root-only reading of native grammar", "export_counterexample": "PROVED against uncharged internal assertion export", "trace_b3": "PROVED trace-only barrier; B3 OPEN"},
        "authoritative_interpretation": {"local_convert": "only the record root condition is exported", "internal_wire": "private syntax unless introduced as a separately paid fresh DEF", "support_bound": 3},
        "minimal_export_witness": {"source": "(x)", "gates": gates, "parent_table": parent, "root_table": root, "internal_gate_1_table": internal, "root_implied": True, "internal_implied": False},
        "normalization": {"random_circuits": len(circuit_records), "records": circuit_records, "bit_bound_samples": bounds, "formula": "N + q*O((n+q)log(n+q)+2^c), fixed c<=3"},
        "trace_firewall": {"sat_source": sat_unit, "reject_all_trace": bad_reject, "unsat_source": unsat_units, "correct_trace": good_reject, "conclusion": "local rejecting traces do not establish decider correctness"},
        "controls": {"native_valid": len(native), "native_malformed": len(malformed), "malformed_sources": len(malformed_sources)},
        "checks": CHECKS,
    }
    path = Path("results/raw/arc/2026-11-04_1748_LSPV5_349_NATIVE_ROOT_NORMALIZATION_B3.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"checks": CHECKS, "output": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "host_elapsed_seconds": elapsed, "host_peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))


if __name__ == "__main__":
    main()
