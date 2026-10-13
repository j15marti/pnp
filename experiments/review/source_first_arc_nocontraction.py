#!/usr/bin/env python3
"""Bounded audit of a one-variable source-first ARC through universal22 U.

This is a finite construction/encoding audit, not an asymptotic lower bound.
Every run has a cooperative 25-second deadline.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import time
from collections import Counter, defaultdict
from pathlib import Path

START = time.monotonic()
ASSERTIONS = 0

W1 = [(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
      (5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
      (-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
      (2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
Q = W1[:7] + W1[8:]
PORTS = (1, 7, 13)


def check(ok: bool, label: str) -> None:
    global ASSERTIONS
    if time.monotonic() - START > 25:
        raise TimeoutError("cooperative 25-second budget")
    ASSERTIONS += 1
    if not ok:
        raise AssertionError(label)


def proper(cnf):
    check(bool(cnf), "nonempty")
    check(all(len(c) == 3 and len(set(map(abs, c))) == 3 for c in cnf), "proper")
    check(len({tuple(sorted(c)) for c in cnf}) == len(cnf), "distinct")


def pad7(lit, first):
    a,b,c,d,e = range(first, first + 5)
    return [(lit,-a,-b),(a,c,-d),(a,d,-e),(b,e,-c),
            (b,-d,-e),(-a,c,d),(-b,-c,e)]


def dense_rename(cnf):
    old = sorted({abs(l) for c in cnf for l in c})
    ren = {x:i+1 for i,x in enumerate(old)}
    return [tuple(ren[abs(l)] if l > 0 else -ren[abs(l)] for l in c) for c in cnf]


def balance(source):
    proper(source)
    n = max(abs(l) for c in source for l in c)
    counts = Counter(l for c in source for l in c)
    out = list(source)
    nxt = n + 1
    gadgets = 0
    for x in range(1, n + 1):
        r = max(counts[x], counts[-x], 2)
        for lit, deficit in ((x, r-counts[x]), (-x, r-counts[-x])):
            for _ in range(deficit):
                out.extend(pad7(lit, nxt))
                nxt += 5
                gadgets += 1
    return out, gadgets


def compile22(source):
    bal, gadgets = balance(source)
    positions = defaultdict(lambda: {1:[], -1:[]})
    for i,c in enumerate(bal):
        for j,l in enumerate(c):
            positions[abs(l)][1 if l > 0 else -1].append((i,j))
    out = [list(c) for c in bal]
    offset = 0
    cycles = []
    for x in range(1, max(positions) + 1):
        pos = positions[x]
        r = len(pos[1])
        check(r == len(pos[-1]) and r >= 2, "balanced intermediate")
        ids = list(range(offset + 1, offset + r + 1))
        offset += r
        for j,z in enumerate(ids):
            for sign in (1,-1):
                ci,cj = pos[sign][j]
                out[ci][cj] = sign*z
        cycles.extend((ids[j], ids[(j+1) % r]) for j in range(r))
    R = offset
    check(R % 3 == 0, "R divisible by 3")
    for j,(u,v) in enumerate(cycles):
        q,p = divmod(j,3)
        out.append([-u, v, R + 15*q + PORTS[p]])
    for q in range(R // 3):
        for c in Q:
            out.append([(R+15*q+abs(l))*(1 if l > 0 else -1) for l in c])
    target = [tuple(c) for c in out]
    proper(target)
    occ = Counter(l for c in target for l in c)
    n = max(map(abs, occ))
    check(all(occ[x] == occ[-x] == 2 for x in range(1,n+1)), "exact (2,2)")
    check(n == 9*len(bal) and len(target) == 12*len(bal), "compiler size identity")
    return target, gadgets


def restrict(source, x, bit):
    raw = []
    for c in source:
        if any(abs(l) == x and int(l > 0) == bit for l in c):
            continue
        d = tuple(l for l in c if abs(l) != x)
        raw.append(d)
    return dense_rename(raw)


def properize(raw):
    old_n = max(abs(l) for c in raw for l in c)
    out = []
    z = old_n
    for c in raw:
        if len(c) == 3:
            out.append(c)
        elif len(c) == 2:
            z += 1
            out.extend([c + (z,), c + (-z,)])
        else:
            raise ValueError("audit supports only binary/ternary residuals")
    proper(out)
    return out


def sat(cnf):
    n = max(abs(l) for c in cnf for l in c)
    for bits in itertools.product((0,1), repeat=n):
        if all(any(bits[abs(l)-1] == int(l > 0) for l in c) for c in cnf):
            return True
    return False


def enc(cnf):
    return json.dumps(cnf, separators=(",",":"))


def audit_source(name, source, brute=False):
    proper(source)
    counts = Counter(l for c in source for l in c)
    check(all(counts[x] == counts[-x] >= 2 for x in range(1, max(map(abs,counts))+1)),
          "balanced source")
    parent, pg = compile22(source)
    check(pg == 0, "balanced source has no padding")
    rows = []
    for x in range(1, max(map(abs,counts))+1):
        p = counts[x]
        for bit in (0,1):
            raw = restrict(source, x, bit)
            repaired = properize(raw)
            child, g = compile22(repaired)
            check(len(raw) == len(source)-p, "raw restriction clause count")
            check(len(repaired) == len(source), "properization restores clause count")
            check(len(child) >= len(parent), "no compiled clause contraction")
            if brute and x <= 2:
                check(sat(raw) == sat(repaired), "properization SAT equivalence")
            rows.append({
                "variable":x, "bit":bit, "signed_occurrences":p,
                "raw_clauses":len(raw), "properized_clauses":len(repaired),
                "rebalance_gadgets":g,
                "parent_target_variables":max(abs(l) for c in parent for l in c),
                "parent_target_clauses":len(parent),
                "parent_encoded_bytes":len(enc(parent).encode()),
                "child_target_variables":max(abs(l) for c in child for l in c),
                "child_target_clauses":len(child),
                "child_encoded_bytes":len(enc(child).encode()),
                "strict_target_clause_contraction":len(child) < len(parent),
                "strict_encoded_contraction":len(enc(child)) < len(enc(parent)),
            })
    return {"name":name, "source_clauses":len(source), "parent_gadgets":pg,
            "rows":rows}


def main(out):
    yes = [(1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3)]
    data = [audit_source("balanced_yes", yes, brute=True),
            audit_source("W1_unsat", W1, brute=True)]
    rows = [r for d in data for r in d["rows"]]
    check(all(not r["strict_target_clause_contraction"] for r in rows), "no clause contraction")
    result = {
        "run_id":"SOURCEARC-NOCONTRACT1", "status":"COMPUTATIONAL",
        "claim":"finite audit of the exact one-variable/properize/recompile route",
        "all_checks_passed":True, "assertions":ASSERTIONS,
        "sources":data,
        "summary":{
            "branches":len(rows),
            "branches_with_strict_target_clause_contraction":sum(r["strict_target_clause_contraction"] for r in rows),
            "branches_with_strict_encoded_contraction":sum(r["strict_encoded_contraction"] for r in rows),
            "minimum_child_parent_clause_ratio":min(r["child_target_clauses"]/r["parent_target_clauses"] for r in rows),
            "minimum_child_parent_byte_ratio":min(r["child_encoded_bytes"]/r["parent_encoded_bytes"] for r in rows),
        },
        "elapsed_seconds":time.monotonic()-START,
        "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "asymptotic_lower_bound_certified":False,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps(result["summary"], sort_keys=True))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    main(args.out)
