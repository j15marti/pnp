#!/usr/bin/env python3
"""Bounded falsification harness for MARKED-CUTSET-BLOCK1.

The program is deliberately small and self-contained.  It tests exact SAT
semantics and exact encoded child lengths for a certificate-verifying partial
compiler.  Its Python memory use is *not* evidence for the bit-machine space
bound proved in the accompanying report.
"""

from __future__ import annotations

import itertools
import json
import math
import random
import signal
import time
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

Clause = Tuple[int, ...]
Formula = Tuple[Clause, ...]


def uleb(n: int) -> bytes:
    if n < 0:
        raise ValueError("uleb requires nonnegative input")
    out = bytearray()
    while True:
        b = n & 0x7F
        n >>= 7
        out.append(b | (0x80 if n else 0))
        if not n:
            return bytes(out)


def zigzag(x: int) -> int:
    if x == 0:
        raise ValueError("literal zero is invalid")
    return 2 * abs(x) - (1 if x > 0 else 0)


def encode_cnf(f: Formula) -> bytes:
    maxvar = max((abs(x) for c in f for x in c), default=0)
    out = bytearray(b"CNF1")
    out += uleb(maxvar)
    out += uleb(len(f))
    for c in f:
        out += uleb(len(c))
        for lit in c:
            out += uleb(zigzag(lit))
    return bytes(out)


MAGIC: Clause = (1, -1, 1, -1)
CUT_END: Clause = (1, -1, 1)


def cut_marker(v: int) -> Clause:
    return (1, -1, v)


def block_marker(lo: int, hi: int) -> Clause:
    return (2, -2, lo, -lo, hi)


def is_block_marker(c: Clause) -> Optional[Tuple[int, int]]:
    if len(c) != 5 or c[0:2] != (2, -2) or c[3] != -c[2]:
        return None
    lo, hi = c[2], c[4]
    if lo < 3 or hi < lo:
        return None
    return lo, hi


def clause_value(c: Clause, a: Dict[int, bool]) -> bool:
    return any(a.get(abs(l), False) == (l > 0) for l in c)


def tautology(c: Clause) -> bool:
    s = set(c)
    return any(-x in s for x in s)


def brute_sat(f: Formula) -> bool:
    # Tautological metadata variables need not be enumerated.
    core = tuple(c for c in f if not tautology(c))
    vars_ = sorted({abs(x) for c in core for x in c})
    for bits in itertools.product((False, True), repeat=len(vars_)):
        a = dict(zip(vars_, bits))
        if all(clause_value(c, a) for c in core):
            return True
    return False


def restrict_clause(c: Clause, assignment: Dict[int, bool]) -> Optional[Clause]:
    out: List[int] = []
    for lit in c:
        v = abs(lit)
        if v not in assignment:
            out.append(lit)
        elif assignment[v] == (lit > 0):
            return None
    return tuple(out)


@dataclass
class Analysis:
    status: str
    reason: str
    input_bits: int
    cut_size: int = 0
    blocks: int = 0
    planned_calls: int = 0
    aggregate_child_bits: int = 0
    max_child_bits: int = 0
    answer: Optional[bool] = None
    oracle_calls: int = 0


def parse_marked(f: Formula):
    if not f or f[0] != MAGIC:
        raise ValueError("missing magic")
    i = 1
    cut: List[int] = []
    while i < len(f) and f[i] != CUT_END:
        c = f[i]
        if len(c) != 3 or c[0:2] != (1, -1) or c[2] < 3:
            raise ValueError("bad cut marker")
        if cut and c[2] <= cut[-1]:
            raise ValueError("cut identifiers not strictly increasing")
        cut.append(c[2])
        i += 1
    if i == len(f):
        raise ValueError("missing cut terminator")
    i += 1
    cutset = set(cut)

    global_clauses: List[Clause] = []
    while i < len(f) and is_block_marker(f[i]) is None:
        c = f[i]
        if 1 in {abs(x) for x in c} or 2 in {abs(x) for x in c}:
            raise ValueError("tag variable in data")
        if any(abs(x) not in cutset for x in c):
            raise ValueError("non-cut variable before first block")
        global_clauses.append(c)
        i += 1

    blocks: List[Tuple[Tuple[int, int], Formula]] = []
    previous_hi = 2
    while i < len(f):
        interval = is_block_marker(f[i])
        if interval is None:
            raise ValueError("data without block marker")
        lo, hi = interval
        if lo <= previous_hi:
            raise ValueError("overlapping or unordered block intervals")
        previous_hi = hi
        i += 1
        data: List[Clause] = []
        while i < len(f) and is_block_marker(f[i]) is None:
            c = f[i]
            av = {abs(x) for x in c}
            if 1 in av or 2 in av:
                raise ValueError("tag variable in data")
            outside = [v for v in av if v not in cutset and not (lo <= v <= hi)]
            if outside:
                raise ValueError("cross-block variable")
            if all(v in cutset for v in av):
                raise ValueError("cut-only clause inside block")
            data.append(c)
            i += 1
        blocks.append(((lo, hi), tuple(data)))
    return tuple(cut), tuple(global_clauses), tuple(blocks)


def compile_and_execute(f: Formula) -> Analysis:
    nbits = 8 * len(encode_cnf(f))
    maxvar = max((abs(x) for c in f for x in c), default=0)
    if maxvar > nbits * nbits:
        return Analysis("UNKNOWN", "identifier budget", nbits, oracle_calls=0)
    try:
        cut, global_clauses, blocks = parse_marked(f)
    except ValueError as exc:
        return Analysis("UNKNOWN", str(exc), nbits, oracle_calls=0)

    if len(cut) > math.floor(math.log2(max(2, nbits)) / 10):
        return Analysis("UNKNOWN", "cut budget", nbits, len(cut), len(blocks), oracle_calls=0)
    if len(blocks) > math.floor(math.sqrt(nbits)):
        return Analysis("UNKNOWN", "block-count budget", nbits, len(cut), len(blocks), oracle_calls=0)

    # PRE-A dry run: finish every structural and exact child-size check before
    # the first simulated child execution.  No children are deduplicated.
    plan: List[Tuple[bool, Tuple[Formula, ...]]] = []
    agg = 0
    mx = 0
    cap = math.floor(math.sqrt(nbits) * math.log2(max(2, nbits)))
    for bits in itertools.product((False, True), repeat=len(cut)):
        a = dict(zip(cut, bits))
        branch_false = False
        for c in global_clauses:
            rc = restrict_clause(c, a)
            if rc == ():
                branch_false = True
                break
        children: List[Formula] = []
        if not branch_false:
            for _, data in blocks:
                residual: List[Clause] = []
                for c in data:
                    rc = restrict_clause(c, a)
                    if rc is None:
                        continue
                    if rc == ():
                        branch_false = True
                        residual = []
                        break
                    residual.append(rc)
                if branch_false:
                    children = []
                    break
                if residual:
                    child = tuple(residual)
                    cbits = 8 * len(encode_cnf(child))
                    if cbits > cap:
                        return Analysis("UNKNOWN", "child-size budget", nbits, len(cut), len(blocks), oracle_calls=0)
                    children.append(child)
                    agg += cbits
                    mx = max(mx, cbits)
        plan.append((branch_false, tuple(children)))

    # Execute every planned child once, even after a false child, so the
    # observed multiplicity is the conservative full-plan multiplicity.
    answer = False
    executed = 0
    for branch_false, children in plan:
        vals = []
        for child in children:
            vals.append(brute_sat(child))
            executed += 1
        answer = answer or ((not branch_false) and all(vals))
    return Analysis(
        "ANSWER", "accepted", nbits, len(cut), len(blocks),
        sum(len(cs) for _, cs in plan), agg, mx, answer, executed,
    )


def marked_formula(cut: Sequence[int], global_clauses: Sequence[Clause],
                   blocks: Sequence[Tuple[int, int, Sequence[Clause]]]) -> Formula:
    out: List[Clause] = [MAGIC]
    out.extend(cut_marker(v) for v in cut)
    out.append(CUT_END)
    out.extend(global_clauses)
    for lo, hi, data in blocks:
        out.append(block_marker(lo, hi))
        out.extend(data)
    return tuple(out)


def random_positive(rng: random.Random) -> Formula:
    # Empty marked blocks provide concise, semantically inert size overhead so
    # the exact asymptotic cut budget is meaningful even in finite tests.
    cut = (3,)
    blocks = []
    base = 10
    for j in range(18):
        v = base + 3 * j
        data: List[Clause] = []
        if j < 3:
            for _ in range(rng.randint(1, 3)):
                width = rng.randint(1, 3)
                first = v if rng.random() < 0.5 else -v
                clause = (first,) + tuple(rng.sample([3, -3, -first], width - 1))
                # Complementary pairs are allowed and are harmless tautologies.
                data.append(clause)
        blocks.append((v, v + 1, data))
    global_clauses = []
    if rng.random() < 0.5:
        global_clauses.append((3,) if rng.random() < 0.5 else (-3,))
    return marked_formula(cut, global_clauses, blocks)


def run() -> dict:
    rng = random.Random(0xC075E7)
    started = time.perf_counter()
    semantic_cases = 0
    resource_cases = 0
    unknown_controls = 0
    max_ratio = 0.0

    for _ in range(400):
        f = random_positive(rng)
        result = compile_and_execute(f)
        if result.status != "ANSWER":
            raise AssertionError((result.reason, result.input_bits, f))
        expected = brute_sat(f)
        if result.answer != expected:
            raise AssertionError(("semantic mismatch", result, f))
        if result.oracle_calls != result.planned_calls:
            raise AssertionError("multiplicity mismatch")
        finite_cap = math.floor(math.sqrt(result.input_bits) * math.log2(max(2, result.input_bits)))
        if result.max_child_bits > finite_cap:
            raise AssertionError("child cap violated")
        if result.planned_calls > 2 ** result.cut_size * result.blocks:
            raise AssertionError("call bound violated")
        if result.aggregate_child_bits:
            max_ratio = max(max_ratio, result.aggregate_child_bits / (result.input_bits ** 1.1))
        semantic_cases += 1
        resource_cases += 1

    base = random_positive(rng)
    malformed = [
        base[1:],                                      # no magic
        base[:2] + base[3:],                           # malformed prefix/end
        marked_formula((3,), (), ((10, 11, ((12,),)),)),  # cross interval
        marked_formula((3,), (), ((10, 20, ()), (20, 30, ()))),  # overlap
        marked_formula((3,), (), ((10, 11, ((3,),)),)),  # cut-only in block
        marked_formula((3,), ((10,),), ((10, 11, ()),)),  # non-cut global
    ]
    # Too many block markers relative to exact input bits.
    malformed.append(marked_formula((), (), tuple((10 + 3*j, 11 + 3*j, ()) for j in range(220))))
    # One residual child occupying essentially the whole parent violates sqrt(N).
    huge = tuple((10,) for _ in range(4000))
    malformed.append(marked_formula((), (), ((10, 11, huge),)))

    for f in malformed:
        result = compile_and_execute(f)
        if result.status != "UNKNOWN" or result.oracle_calls != 0:
            raise AssertionError(("control accepted/called", result))
        unknown_controls += 1

    # Duplicate/delay-style inert blocks and clauses must never change an answer.
    for _ in range(40):
        f = random_positive(rng)
        cut, g, blocks = parse_marked(f)
        decorated = list(blocks)
        lo = blocks[-1][0][1] + 3
        decorated.append(((lo, lo + 1), ((lo, -lo),)))
        f2 = marked_formula(cut, g, tuple((iv[0], iv[1], data) for iv, data in decorated))
        r1, r2 = compile_and_execute(f), compile_and_execute(f2)
        if r1.status != "ANSWER" or r2.status != "ANSWER" or r1.answer != r2.answer:
            raise AssertionError(("delay/duplicate control", r1, r2))
        semantic_cases += 1

    elapsed = time.perf_counter() - started
    return {
        "status": "PASS",
        "seed": hex(0xC075E7),
        "semantic_cases": semantic_cases,
        "resource_cases": resource_cases,
        "unknown_zero_call_controls": unknown_controls,
        "max_aggregate_over_N_1_1": max_ratio,
        "elapsed_seconds": elapsed,
        "timeout_seconds": 25,
        "space_disclaimer": "Python memory is not a bit-machine space certificate.",
    }


def timeout_handler(_signum, _frame):
    raise TimeoutError("25-second test budget exceeded")


if __name__ == "__main__":
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(25)
    print(json.dumps(run(), indent=2, sort_keys=True))
