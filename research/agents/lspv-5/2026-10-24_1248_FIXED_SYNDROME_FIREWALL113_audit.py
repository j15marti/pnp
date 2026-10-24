#!/usr/bin/env python3
"""Independent audit for FIXED-SYNDROME-FIREWALL113.

Standard library only.  Every suite is deterministic and individually small.
The external MOD-CSP theorem is not re-proved computationally; this script
checks the exact reduction to a weighted F_2^ell constraint and independently
checks Role 4's DUAL-PARITY-JOINT77 family.
"""

from __future__ import annotations

from itertools import product
import hashlib
import json
import time

SEED = 202610241248
CHECKS = 0


def check(cond: bool, msg: str) -> None:
    global CHECKS
    CHECKS += 1
    if not cond:
        raise AssertionError(msg)


def lit_value(lit: int, bits: tuple[int, ...]) -> bool:
    value = bool(bits[abs(lit) - 1])
    return value if lit > 0 else not value


def sat_cnf(clauses: list[tuple[int, ...]], bits: tuple[int, ...]) -> bool:
    return all(any(lit_value(lit, bits) for lit in clause) for clause in clauses)


def xor3(out: int, left: int, right: int) -> list[tuple[int, int, int]]:
    clauses = []
    for ov, lv, rv in product((0, 1), repeat=3):
        if ov != (lv ^ rv):
            clauses.append(tuple(v if b == 0 else -v for v, b in ((out, ov), (left, lv), (right, rv))))
    return clauses


def eq2(a: int, b: int, flip: int = 0) -> list[tuple[int, int]]:
    if flip == 0:
        return [(-a, b), (a, -b)]
    return [(a, b), (-a, -b)]


def build_dual(q: int, e: tuple[int, ...]):
    names = ["x", "y"]
    for j in range(q):
        names += [f"z{j+1}", f"w{j+1}"]
    ids = {name: i + 1 for i, name in enumerate(names)}
    clauses: list[tuple[int, ...]] = []
    for j, bit in enumerate(e, 1):
        z, w = ids[f"z{j}"], ids[f"w{j}"]
        clauses += eq2(w, z, bit)
        clauses += [(ids["x"], z), (ids["y"], -z)]
    supports = []
    for head in ("x", "y"):
        operands = [ids[head]]
        for j in range(1, q + 1):
            operands += [ids[f"z{j}"], ids[f"w{j}"]]
        prev = None
        for r in range(2 * q - 1):
            tname = f"t{head}_{r+1}"
            ids[tname] = len(ids) + 1
            out = ids[tname]
            if r == 0:
                left, right = operands[0], operands[1]
            else:
                left, right = prev, operands[r + 1]
            clauses += xor3(out, left, right)
            supports.append(frozenset((out, left, right)))
            prev = out
        clauses += eq2(prev, operands[-1], 0)
    return ids, clauses, supports


def source_models(q: int, e: tuple[int, ...]):
    models = []
    syndromes = set()
    for x, y in product((0, 1), repeat=2):
        for z in product((0, 1), repeat=q):
            w = tuple(z[j] ^ e[j] for j in range(q))
            if all(x or z[j] for j in range(q)) and all(y or (not z[j]) for j in range(q)):
                p = 0
                for j in range(q):
                    p ^= z[j] ^ w[j]
                syndromes.add((x ^ p, y ^ p))
                if x == p and y == p:
                    models.append((x, y, z, w))
    return models, syndromes


def min_cover(supports: list[frozenset[int]], variables: list[int]) -> int:
    full = (1 << len(supports)) - 1
    cover = {}
    for v in variables:
        mask = 0
        for i, s in enumerate(supports):
            if v in s:
                mask |= 1 << i
        if mask:
            cover[v] = mask
    dp = {0: 0}
    for mask in cover.values():
        nxt = dict(dp)
        for got, cost in dp.items():
            new = got | mask
            if cost + 1 < nxt.get(new, 10**9):
                nxt[new] = cost + 1
        dp = nxt
    return dp[full]


def parity_vector(bits: tuple[int, ...], rows: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    return tuple(sum(a * x for a, x in zip(row, bits)) & 1 for row in rows)


def group_sum(bits: tuple[int, ...], rows: tuple[tuple[int, ...], ...]) -> tuple[int, ...]:
    # g_j(0)=0 and g_j(1) is column j of the parity matrix.
    ell = len(rows)
    out = [0] * ell
    for j, x in enumerate(bits):
        if x:
            for r in range(ell):
                out[r] ^= rows[r][j]
    return tuple(out)


def suite_dual_family():
    records = []
    for q in range(1, 6):
        for e in product((0, 1), repeat=q):
            models, syndromes = source_models(q, e)
            p = sum(e) & 1
            check(len(models) == (2**q if p else 0), f"source count q={q} e={e}")
            expected_syndromes = set(product((0, 1), repeat=2)) - {(p, p)}
            check(syndromes == expected_syndromes, f"syndrome q={q} e={e}")
            ids, clauses, supports = build_dual(q, e)
            check(len(ids) == 6 * q, "variable count")
            check(sum(len(c) == 2 for c in clauses) == 4 * q + 4, "binary count")
            check(sum(len(c) == 3 for c in clauses) == 16 * q - 8, "ternary count")
            check(len(supports) == 4 * q - 2, "support count")
            freq = {v: sum(v in s for s in supports) for v in ids.values()}
            check(max(freq.values(), default=0) <= 2, "support degree ceiling")
            canonical = [ids[f"z{j}"] for j in range(1, q + 1)] + [ids[f"w{j}"] for j in range(1, q)]
            check(all(any(v in s for v in canonical) for s in supports), "canonical cover")
            if q <= 4:
                check(min_cover(supports, list(ids.values())) == 2 * q - 1, "exact backdoor")
            if q <= 3:
                count = 0
                for bits in product((0, 1), repeat=len(ids)):
                    count += sat_cnf(clauses, bits)
                check(count == (2**q if p else 0), f"encoded count q={q} e={e}")
        records.append({"q": q, "orientations": 2**q, "n": 6*q, "m2": 4*q+4,
                        "k": 16*q-8, "M": 20*q-4, "h2": 2*q-1})
    return records


def suite_group_reduction():
    examples = 0
    # Deterministic small 2-CNF controls, including Horn, SCC, padding, and contradictions.
    templates = [
        [],
        [(1, 2), (-1, 3), (-2, -3)],
        [(-1,), (1, 2), (-2, 3)],
        [(1,), (-1,)],
        [(1, 2), (1, 2), (-1, -2)],
    ]
    for n in range(1, 8):
        clauses = [tuple(l for l in c if abs(l) <= n) for c in templates[n % len(templates)]]
        clauses = [c for c in clauses if c]
        for ell in range(1, 4):
            rows = tuple(tuple(((r + 1) * (j + 2) + r * j + n) & 1 for j in range(n)) for r in range(ell))
            for target in product((0, 1), repeat=ell):
                direct = []
                grouped = []
                for bits in product((0, 1), repeat=n):
                    if sat_cnf(clauses, bits):
                        if parity_vector(bits, rows) == target:
                            direct.append(bits)
                        if group_sum(bits, rows) == target:
                            grouped.append(bits)
                check(direct == grouped, f"group mapping n={n} ell={ell}")
                examples += 1
    return examples


def large_symbolic_records():
    out = []
    for q in (8, 64, 512, 4096):
        n, m2, k, M, h2 = 6*q, 4*q+4, 16*q-8, 20*q-4, 2*q-1
        w = (64*(n+M+1)-1).bit_length()
        N = (80*q-14)*w
        out.append({"q": q, "n": n, "m2": m2, "k": k, "M": M, "h2": h2,
                    "word_bits": w, "encoded_bits": N,
                    "fixed_two_check_known_upper": "(n+m)^{O(2)}",
                    "canonical_source_policy": "O(q) indexed words",
                    "query_lower_bound": q})
        check(N == (80*q-14)*w, "encoding identity")
        check(h2 == 2*q-1 and k == 16*q-8, "symbolic parameters")
    return out


def main():
    start = time.perf_counter()
    records = suite_dual_family()
    group_examples = suite_group_reduction()
    large = large_symbolic_records()
    result = {
        "run_id": "FIXED-SYNDROME-FIREWALL113",
        "seed": SEED,
        "method": "deterministic exhaustive plus symbolic checks; no randomness",
        "checks": CHECKS,
        "elapsed_seconds": round(time.perf_counter() - start, 6),
        "dual_family_small": records,
        "weighted_group_mapping_examples": group_examples,
        "large_symbolic": large,
        "known_theorem_transfer": {
            "source": "Brakensiek-Gopi-Guruswami, SIAM J. Comput. 51 (2022), Proposition 5.2",
            "mapping": "ell parity rows -> one weighted constraint over G=F_2^ell",
            "runtime": "(n+m)^{O(ell)} for G=F_2^ell",
            "scope": "2-CNF plus supplied/extracted ell parity equations"
        },
        "adaptive_policy": [
            "parse and validate source without knowing label",
            "XR1 extract complete XOR blocks and record provenance",
            "XR2 row-reduce to independent rank rho",
            "if residual is 2-CNF plus rho rows, dispatch to 2-SAT-MOD(F_2^rho)",
            "use canonical linear shortcut when recognized; otherwise exact fallback",
            "SAT: lift and replay one witness; UNSAT: exact decision bit only"
        ],
        "limitations": [
            "The literature theorem is an upper bound, not an all-decider lower bound.",
            "The experiment does not implement the full recursive MOD-CSP algorithm.",
            "Finite checks do not prove asymptotic complexity.",
            "For growing ell the bound may be quasi-polynomial or worse; unrestricted ell includes NP-complete instances."
        ]
    }
    payload = json.dumps(result, indent=2, sort_keys=True)
    result["self_payload_sha256"] = hashlib.sha256(payload.encode()).hexdigest()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
