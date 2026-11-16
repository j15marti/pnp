#!/usr/bin/env python3
"""TMR-3/060: physical marker-phase and Williams source-edge finite audit.

This validates the marker postlude transition-by-transition and an independently
parsed monotone circuit source. It does NOT execute the full length-only clock,
HPV compiler, or a native TM transition table for the CVP evaluator. The
universal block-clock construction is a symbolic lemma in the report.
"""
from __future__ import annotations
import json
import random
from pathlib import Path

REVISION = "tmr3-block-marker060-v1"
SEED = 202611152022
rng = random.Random(SEED)
checks = 0
cases = 0
invalids = 0
crossings = 0
edges = 0

def ck(condition, message="assertion"):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(f"{message}: #{checks}")

def encode(gates):
    n = len(gates)
    word = "1" * n + "0"
    for j, (op, a, b) in enumerate(gates):
        word += format(op, "02b")
        word += "".join("1" if op >= 2 and k == a else "0" for k in range(n))
        word += "".join("1" if op >= 2 and k == b else "0" for k in range(n))
    return word

def parse(word):
    if not word or set(word) - {"0", "1"}:
        return None
    n = len(word) - len(word.lstrip("1"))
    if not n or n >= len(word) or word[n] != "0" or len(word) != 2*n*n+3*n+1:
        return None
    gates = []
    for j in range(n):
        p = n+1+j*(2+2*n)
        op = int(word[p:p+2], 2)
        a = [k for k, z in enumerate(word[p+2:p+2+n]) if z == "1"]
        b = [k for k, z in enumerate(word[p+2+n:p+2+2*n]) if z == "1"]
        if op < 2:
            if a or b:
                return None
            gates.append((op, -1, -1))
        else:
            if len(a) != 1 or len(b) != 1 or a[0] >= j or b[0] >= j:
                return None
            gates.append((op, a[0], b[0]))
    return gates

def evaluate(gates):
    values = []
    for op, a, b in gates:
        values.append(op if op < 2 else ((values[a] & values[b]) if op == 2 else (values[a] | values[b])))
    return values[-1]

def marker_trace(bit, b):
    """Three complete b-step phases; MARK moves only in the second phase."""
    global crossings, edges
    position = 0
    active = []
    actual_crossings = []
    for phase in (1, 2, 3):
        active.append(position//b+1)
        for local in range(1, b+1):
            global_time = (phase-1)*b+local
            old = position//b+1
            if phase == 2 and (local < b or bit == 1):
                position += 1
            new = position//b+1
            ck(new == old or global_time % b == 0, "illegal nonboundary head crossing")
            if new != old:
                actual_crossings.append(global_time)
    ck(active[0] == 1 and active[1] == 1, "incorrect prefix block")
    ck(active[2] == 1+bit, "terminal active block differs from circuit value")
    ck(position == b-1+bit, "terminal MARK position")
    ck(actual_crossings == ([2*b] if bit else []), "crossing schedule")
    # Williams Section 3.2: (MARK,0,2)->(MARK,3) is a source edge
    # iff the second MARK tape block is first active in time block 3.
    source_edge = active[2] == 2 and 2 not in active[:2]
    ck(source_edge == bool(bit), "first-visit source-edge predicate")
    last_move_label = active[2]-active[1]
    ck(last_move_label == bit, "movement label of second block")
    crossings += len(actual_crossings)
    edges += int(source_edge)
    return active, actual_crossings

for n in range(1, 11):
    examples = [[(j % 2, -1, -1) for j in range(n)],
                [(1, -1, -1) for _ in range(n)],
                [(0, -1, -1) for _ in range(n)]]
    for rep in range(60):
        gates = []
        for j in range(n):
            if j == 0 or rng.randrange(5) == 0:
                gates.append((rng.randrange(2), -1, -1))
            else:
                gates.append((rng.choice((2, 3)), rng.randrange(j), rng.randrange(j)))
        examples.append(gates)
    for gates in examples:
        word = encode(gates)
        decoded = parse(word)
        ck(decoded == gates, "source parser")
        ck(len(word) == 2*n*n+3*n+1, "source length")
        value = evaluate(decoded)
        ck(value in (0, 1), "Boolean terminal value")
        # In the actual universal construction b(N)>>N. This test only
        # validates the block boundary subroutine, not the clock length.
        b = max(8, len(word)+3)
        active, seq = marker_trace(value, b)
        ck(active == [1, 1, 1+value], "three-block index")
        ck(seq == ([2*b] if value else []), "last crossing")
        cases += 1
        ck(parse(word + "0") is None, "reject changed encoded length")
        invalids += 1
for malformed in ("", "0", "10", "110", "11x0", "111000000", "1110"):
    ck(parse(malformed) is None, "reject malformed original input")
    invalids += 1

result = {
    "revision": REVISION, "seed": SEED,
    "scope": "finite exact MARK head crossings, first-visit Williams source edge, source parser and Boolean output; no native TM clock or block normalizer",
    "valid_source_cases": cases,
    "malformed_rejections": invalids,
    "positive_source_edges": edges,
    "physical_block_crossings": crossings,
    "assertions": checks, "failures": 0,
    "theorem_scope": "symbolic separately; no P-versus-NP conclusion",
}
Path("results/raw/tmr").mkdir(parents=True, exist_ok=True)
path = Path("results/raw/tmr/2026-11-15_2022_TMR3_BLOCK_MARKER060_RAW.json")
path.write_text(json.dumps(result, sort_keys=True, indent=2)+"\n", encoding="utf-8")
print(json.dumps(result, sort_keys=True))
