#!/usr/bin/env python3
"""ARC-HIERARCHY164 exact ordinary-3CNF padded block-class audit.

Run: python 2026-10-25_0305_ARC_HIERARCHY164_repro.py
No third-party dependencies. Each case is independent and under 30 seconds.
The Python counters are semantic/bit-probe checks, not FLMV Turing-machine traces.
"""
from __future__ import annotations
import hashlib
import itertools
import json
import platform
import time
from pathlib import Path

SEED = 202610250305
RUN_ID = "ARC-HIERARCHY164"


def encode(clauses: list[tuple[int, int, int]], nv: int) -> str:
    nc = len(clauses)
    h = (2 * max(nv, nc) + 1).bit_length()
    arr = ["1" * h + "0", f"{nv:0{h}b}", f"{nc:0{h}b}"]
    for c in clauses:
        assert len(c) == 3
        for lit in c:
            assert 1 <= abs(lit) <= nv
            code = 2 * (abs(lit) - 1) + (lit < 0)
            arr.append(f"{code:0{h}b}")
    return "".join(arr)


def decode(bits: str) -> tuple[int, list[tuple[int, int, int]], int, int]:
    if not bits or any(x not in "01" for x in bits):
        raise ValueError("non-binary or empty source")
    i = bits.find("0")
    if i <= 0:
        raise ValueError("bad unary width")
    h = i
    offset = h + 1
    if len(bits) < offset + 2 * h:
        raise ValueError("truncated header")
    nv = int(bits[offset:offset + h], 2)
    nc = int(bits[offset + h:offset + 2 * h], 2)
    if nv == 0 or nc == 0 or h != (2 * max(nv, nc) + 1).bit_length():
        raise ValueError("noncanonical header")
    header = 3 * h + 1
    if len(bits) != header + 3 * nc * h:
        raise ValueError("malformed total length")
    clauses = []
    for j in range(nc):
        lits = []
        for k in range(3):
            p = header + (3 * j + k) * h
            code = int(bits[p:p + h], 2)
            var = code // 2 + 1
            if var > nv:
                raise ValueError("literal index exceeds declaration")
            lits.append(-var if code % 2 else var)
        clauses.append(tuple(lits))
    return nv, clauses, h, header


def integral_root(value: int, exponent: int) -> int | None:
    lo, hi = 1, max(2, value)
    while lo < hi:
        mid = (lo + hi) // 2
        if mid ** exponent < value:
            lo = mid + 1
        else:
            hi = mid
    return lo if lo ** exponent == value else None


def validate_promise(nv: int, clauses: list[tuple[int, int, int]], depth: int) -> int | None:
    n = len(clauses)
    m = integral_root(n, 2 ** depth)
    if m is None or m < 3 or nv != n:
        return None
    for j, c in enumerate(clauses):
        leaf = j // m
        low = leaf * m + 1
        high = (leaf + 1) * m
        if any(not (low <= abs(x) <= high) for x in c):
            return None
    return m


def make_root(m: int, depth: int, unsat: bool) -> tuple[int, list[tuple[int, int, int]]]:
    n = m ** (2 ** depth)
    leaves = n // m
    bad_leaf = leaves // 2
    clauses = []
    for leaf in range(leaves):
        base = m * leaf
        if unsat and leaf == bad_leaf:
            if m >= 8:
                # Every assignment to the first 3 variables violates one row.
                for mask in range(8):
                    clauses.append(tuple((base + i + 1) if ((mask >> i) & 1) else -(base + i + 1) for i in range(3)))
                for _ in range(m - 8):
                    clauses.append((base + 4, base + 5, base + 6))
            else:
                clauses.append((base + 1, base + 1, base + 1))
                clauses.append((-base - 1, -base - 1, -base - 1))
                for _ in range(m - 2):
                    clauses.append((base + 2, base + 3, base + 3))
        else:
            for k in range(m):
                # A varied-looking signed row with a planted all-true witness.
                x = base + (k % m) + 1
                y = base + ((k + 1) % m) + 1
                z = base + ((k + 2) % m) + 1
                if k % 3 == 0:
                    clauses.append((x, y, z))
                elif k % 3 == 1:
                    clauses.append((-x, y, z))
                else:
                    clauses.append((x, -y, z))
    assert len(clauses) == n
    return n, clauses


def localize(clauses: list[tuple[int, int, int]], start: int, count: int) -> list[tuple[int, int, int]]:
    out = []
    for c in clauses[start:start + count]:
        out.append(tuple((abs(lit) - start) * (1 if lit > 0 else -1) for lit in c))
    return out


def brute_sat(clauses: list[tuple[int, int, int]], nv: int) -> bool:
    # Complete independent truth-table oracle for tested leaf lengths.
    if nv > 10:
        raise ValueError("the finite oracle is limited to <=10 variables")
    for mask in range(1 << nv):
        for cl in clauses:
            if not any((bool((mask >> (abs(l) - 1)) & 1) == (l > 0)) for l in cl):
                break
        else:
            return True
    return False


def virtual_bit(root: str, nv: int, root_h: int, root_head: int,
                start: int, count: int, position: int, ledger: dict[str, int]) -> str:
    """Generate a child-bit with explicitly charged root-string bit probes.

    In a FLMV TM the root is read-only indexed and this arithmetic is
    performed on counted index/work tapes. The Python ledger records logical
    source bits read, not a physical TM instruction count.
    """
    child_h = (2 * count + 1).bit_length()
    header = "1" * child_h + "0" + f"{count:0{child_h}b}" * 2
    if position < len(header):
        ledger["synthetic_header_bits"] += 1
        return header[position]
    rel = position - len(header)
    record = rel // child_h
    global_clause = start + record // 3
    signed_slot = record % 3
    root_off = root_head + (3 * global_clause + signed_slot) * root_h
    raw = root[root_off:root_off + root_h]
    ledger["root_bits_read"] += len(raw)
    code = int(raw, 2)
    var = code // 2 + 1
    sign = code % 2
    assert start < var <= start + count
    local = var - start
    outcode = 2 * (local - 1) + sign
    ledger["generated_body_bits"] += 1
    return f"{outcode:0{child_h}b}"[rel % child_h]


def audit(m: int, depth: int, unsat: bool) -> dict:
    started = time.monotonic()
    nv, root = make_root(m, depth, unsat)
    data = encode(root, nv)
    got_nv, parsed, h, hd = decode(data)
    assert got_nv == nv and parsed == root
    assert validate_promise(got_nv, parsed, depth) == m
    leaf_count = nv // m
    leaf_truth = []
    for leaf in range(leaf_count):
        source_clauses = localize(root, leaf * m, m)
        assert len(source_clauses) == m
        bits = encode(source_clauses, m)
        nv2, parsed2, _, _ = decode(bits)
        assert nv2 == m and parsed2 == source_clauses
        leaf_truth.append(brute_sat(parsed2, m))
    root_label = all(leaf_truth)
    assert root_label == (not unsat)
    ledger = {"root_bits_read": 0, "synthetic_header_bits": 0,
              "generated_body_bits": 0, "virtual_bits_compared": 0,
              "actual_children_encoded": 0}
    by_depth = []
    for d in range(1, depth + 1):
        clause_count = m ** (2 ** (depth - d))
        child_count = nv // clause_count
        total_len = 0
        max_len = 0
        sat_children = 0
        bad = 0
        for j in range(child_count):
            start = j * clause_count
            child = localize(root, start, clause_count)
            encoded = encode(child, clause_count)
            cnv, parsed_child, _, _ = decode(encoded)
            assert cnv == clause_count and child == parsed_child
            val = all(leaf_truth[start // m:(start + clause_count) // m])
            sat_children += val
            bad += not val
            total_len += len(encoded)
            max_len = max(max_len, len(encoded))
            ledger["actual_children_encoded"] += 1
            # All depth-1 and depth-2 ordinary children are checked bitwise.
            # For depth 3, representative first/middle/last children are probed
            # to keep independent per-program invocations comfortably short.
            full_probe = depth == 2 or d >= 2 or j in {0, child_count // 2, child_count - 1}
            if full_probe:
                for k, expected in enumerate(encoded):
                    received = virtual_bit(data, nv, h, hd, start, clause_count, k, ledger)
                    assert received == expected, (m, depth, unsat, d, j, k)
                    ledger["virtual_bits_compared"] += 1
        by_depth.append({"level": d, "child_clauses": clause_count,
                         "children": child_count, "max_child_bits": max_len,
                         "total_encoded_bits": total_len,
                         "sat_children": sat_children,
                         "unsat_children": bad,
                         "full_virtual_probe_policy": "all" if (depth == 2 or d >= 2) else "first,middle,last"})
    # Hostile shared-name control: change a clause's variable to belong to the next leaf.
    corrupted = root[:]
    cc = list(corrupted[0])
    cc[0] = m + 1
    corrupted[0] = tuple(cc)
    assert validate_promise(nv, corrupted, depth) is None
    assert validate_promise(*decode(encode(corrupted, nv))[:2], depth) is None
    assert len(data[:-1]) != (hd + 3 * nv * h)
    try:
        decode(data[:-1])
        assert False, "truncated grammar accepted"
    except ValueError:
        pass
    res = {"m":m,"depth":depth,"is_sat_expected":not unsat,
           "actual_root_sat":root_label,"root_clauses":nv,"root_variables":nv,
           "root_bits":len(data),"root_header_width":h,"leaf_count":leaf_count,
           "all_leaf_answers_evaluated":True,
           "unsat_leaves":len(leaf_truth)-sum(leaf_truth),
           "first_level":by_depth[0],"levels":by_depth,
           "ledger":ledger,"malformed_rejected":True,
           "cross_leaf_rename_rejected":True,
           "elapsed_seconds":round(time.monotonic()-started,3)}
    return res


def main() -> None:
    code = Path(__file__).read_bytes()
    cases = [(3,2,False),(3,2,True),(8,2,False),(8,2,True),
             (3,3,False),(3,3,True)]
    results=[]
    for m,d,unsat in cases:
        v=audit(m,d,unsat)
        results.append(v)
        print(f"m={m} D={d} {'UNSAT' if unsat else 'SAT'}: "
              f"N={v['root_bits']} leaves={v['leaf_count']} "
              f"probes={v['ledger']['virtual_bits_compared']} "
              f"root-read={v['ledger']['root_bits_read']} time={v['elapsed_seconds']}s")
    outcome={"run_id":RUN_ID,"seed":SEED,"method":"deterministic-exhaustive leaf truth tables; real fixed-width ordinary encodings; virtual source-bit identity checks",
             "python":platform.python_version(),"source_sha256":hashlib.sha256(code).hexdigest(),
             "cases":results,"total_cases":len(results),
             "sat_cases":sum(x["actual_root_sat"] for x in results),
             "unsat_cases":sum(not x["actual_root_sat"] for x in results),
             "total_verified_virtual_bits":sum(x["ledger"]["virtual_bits_compared"] for x in results),
             "total_root_probe_bits":sum(x["ledger"]["root_bits_read"] for x in results),
             "mismatches":0,
             "scope_note":"Positive restricted class only. No FLMV TM instruction or peak-tape-space traces. No hard-image near-linear reduction. No P-versus-NP implication."}
    out=Path(__file__).with_name("2026-10-25_0305_ARC_HIERARCHY164_results.json")
    out.write_text(json.dumps(outcome,indent=2,sort_keys=True)+"\n")
    print("raw",out,"sha256",hashlib.sha256(out.read_bytes()).hexdigest())

if __name__ == "__main__":
    main()