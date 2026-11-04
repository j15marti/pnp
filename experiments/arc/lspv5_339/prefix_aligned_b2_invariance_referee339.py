#!/usr/bin/env python3
"""REFEREE339: prefix-aligned syntax encodings and B2 controls."""

from __future__ import annotations

from collections import deque
import hashlib
import itertools
import json
import math
from pathlib import Path


checks = 0


def check(ok: bool, msg: str) -> None:
    global checks
    checks += 1
    if not ok:
        raise AssertionError(msg)


def emit(mask: int) -> bytes:
    universe = [(1,), (-1,), (2,), (-2,), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    clauses = [universe[i] for i in range(8) if (mask >> i) & 1]
    body = "".join(" ".join(map(str, c)) + " 0\n" for c in clauses)
    return (f"p cnf 2 {len(clauses)}\n" + body).encode("ascii")


def clauses(mask: int) -> tuple[frozenset[int], ...]:
    universe = [(1,), (-1,), (2,), (-2,), (1, 2), (1, -2), (-1, 2), (-1, -2)]
    return tuple(frozenset(universe[i]) for i in range(8) if (mask >> i) & 1)


def sat_label(cs: tuple[frozenset[int], ...]) -> str:
    for a, b in itertools.product((False, True), repeat=2):
        val = {1: a, 2: b}
        if all(any(val[abs(l)] == (l > 0) for l in c) for c in cs):
            return "SAT"
    return "UNSAT"


def resolvents(a: frozenset[int], b: frozenset[int]):
    out = set()
    for lit in a:
        if -lit in b:
            c = (a - {lit}) | (b - {-lit})
            if not any(-x in c for x in c):
                out.add(frozenset(c))
    return out


def min_resolution_nodes(source: tuple[frozenset[int], ...]) -> int | None:
    start = frozenset(source)
    if frozenset() in start:
        return 0
    queue = deque([(start, 0)])
    seen = {start}
    while queue:
        available, cost = queue.popleft()
        rows = list(available)
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                for c in resolvents(rows[i], rows[j]):
                    if c in available:
                        continue
                    if not c:
                        return cost + 1
                    nxt = available | {c}
                    if nxt not in seen:
                        seen.add(nxt)
                        queue.append((nxt, cost + 1))
    return None


def bytes_to_bits(src: bytes) -> str:
    return "".join(f"{b:08b}" for b in src)


def square_encode(bits: str) -> str:
    n = len(bits)
    return "1" * n + "0" + bits + "0" * (n * n)


def square_decode(code: str) -> str:
    if any(ch not in "01" for ch in code):
        raise ValueError("nonbit")
    n = 0
    while n < len(code) and code[n] == "1":
        n += 1
    if n == len(code):
        raise ValueError("missing delimiter")
    expected = (n + 1) ** 2
    if len(code) != expected:
        raise ValueError("wrong total length")
    payload = code[n + 1:n + 1 + n]
    pad = code[n + 1 + n:]
    if any(ch != "0" for ch in pad):
        raise ValueError("nonzero pad")
    return payload


def wbar(records, key: str, cutoff: int) -> int:
    values = [r["W_resolution"] for r in records
              if r["label"] == "UNSAT" and r[key] <= cutoff]
    return max(values, default=0)


records = []
selected = {0, 3, 5, 15, 85, 133, 170, 255}
for mask in range(256):
    src = emit(mask)
    bits = bytes_to_bits(src)
    cs = clauses(mask)
    label = sat_label(cs)
    w = min_resolution_nodes(cs)
    check((w is None) == (label == "SAT"), f"resolution completeness mask={mask}")
    n0 = len(bits)
    n2 = (n0 + 1) ** 2
    if mask in selected:
        encoded = square_encode(bits)
        check(len(encoded) == n2, f"square length mask={mask}")
        check(square_decode(encoded) == bits, f"roundtrip mask={mask}")
    records.append({"mask": mask, "label": label, "W_resolution": w,
                    "e0_bits": n0, "e2_bits": n2,
                    "source_sha256": hashlib.sha256(src).hexdigest()})

check(sum(r["label"] == "SAT" for r in records) == 95, "SAT count")
check(sum(r["label"] == "UNSAT" for r in records) == 161, "UNSAT count")
check(max(r["W_resolution"] or 0 for r in records) == 3, "toy max W")

# Exact prefix-threshold identity on all finite profile breakpoints.
profile = []
for m in sorted({r["e0_bits"] for r in records}):
    n = (m + 1) ** 2
    a = wbar(records, "e0_bits", m)
    b = wbar(records, "e2_bits", n)
    check(a == b, f"profile identity m={m}")
    check(max((r["e0_bits"] for r in records if r["e2_bits"] <= n), default=0) <= m,
          f"prefix alignment m={m}")
    profile.append({"e0_cutoff": m, "e2_cutoff": n, "Wbar": a})

# Arbitrary cutoffs around every square obey floor(sqrt(N))-1.
for r in records:
    for delta in (-1, 0, 1):
        n = max(0, r["e2_bits"] + delta)
        theta = max(0, math.isqrt(n) - 1)
        check(wbar(records, "e2_bits", n) == wbar(records, "e0_bits", theta),
              f"arbitrary cutoff mask={r['mask']},delta={delta}")

# Malformed wrapper controls.
payload = "101001"
honest = square_encode(payload)
malformed = [honest[:-1], honest + "0", honest[:len(payload)] + "1" + honest[len(payload)+1:],
             "1" * len(honest), honest[:-2] + "10", honest + "x"]
for i, bad in enumerate(malformed):
    try:
        square_decode(bad)
        raise AssertionError(f"accepted malformed wrapper {i}")
    except ValueError:
        checks += 1

# Physical clock/XOR calibration for the first tiny delayed length m=4, q=m^2.
q = 16
word = 0
adjacent_xor = 0
for nxt in range(1, 1 << q):
    adjacent_xor += (word ^ nxt).bit_count()
    word = nxt
adjacent_xor += word.bit_count()  # final wrap to zero
check(adjacent_xor == (1 << (q + 1)) - 2, "binary clock adjacent XOR")
check((0 ^ 0).bit_count() == 0, "clock endpoint XOR")

result = {
    "artifact": "PREFIX-ALIGNED-B2-INVARIANCE-REFEREE339",
    "checks": checks,
    "cases": len(records),
    "sat": sum(r["label"] == "SAT" for r in records),
    "unsat": sum(r["label"] == "UNSAT" for r in records),
    "max_toy_resolution_W": max(r["W_resolution"] or 0 for r in records),
    "records": records,
    "profile": profile,
    "selected_roundtrip_masks": sorted(selected),
    "malformed_wrapper_rejections": len(malformed),
    "clock_control": {"m": 4, "q": q, "ticks": 1 << q,
                      "adjacent_xor_sum": adjacent_xor, "endpoint_xor": 0},
    "theorem": {
        "source_identity": "same abstract ordered labelled CNF and same fixed calculus R",
        "square_length": "|e2(F)|=(|e0(F)|+1)^2",
        "prefix_identity": "S_e2(N)=S_e0(max(0,floor(sqrt(N))-1))",
        "Wbar_identity": "Wbar_e2(N)=Wbar_e0(max(0,floor(sqrt(N))-1))",
        "B2": "equivalent under cumulative worst-case time and decider transport",
        "same_machine_profile": "not invariant; sparse delays refute naive T(2N) or T(N^2) rescaling",
    },
    "physical": {
        "encode": "Theta(n^2) explicit construction/output; streaming O(log n) counters",
        "decode": "Theta(N) validation and Theta(sqrt N) payload output",
        "valid_zero_pad_probes": "Omega(n^2) against one-bit malformed neighbors",
        "materialized_peak": "Theta(N); streaming scratch can be polylog with paid reads",
    },
    "status": {"B1_Rmix341": "OPEN", "B2_Rmix341": "OPEN", "B3_Rmix341": "OPEN",
               "superpolynomial_Wbar_Rmix341": "OPEN", "P_vs_NP": "OPEN"},
}
payload_json = json.dumps(result, sort_keys=True, separators=(",", ":"))
result["sha256_without_digest"] = hashlib.sha256(payload_json.encode()).hexdigest()
out = Path("results/raw/arc/lspv5_339/prefix_aligned_b2_invariance_referee339.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
print(json.dumps({k: result[k] for k in (
    "artifact", "checks", "cases", "sat", "unsat",
    "max_toy_resolution_W", "malformed_wrapper_rejections",
    "clock_control", "sha256_without_digest")}, indent=2, sort_keys=True))
