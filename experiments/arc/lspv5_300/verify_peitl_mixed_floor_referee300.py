#!/usr/bin/env python3
"""Independent no-producer-import referee for REFEREE300."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from pathlib import Path


def parse_cnf_text(text):
    n = declared = None
    clauses = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line[0] == "c":
            continue
        parts = line.split()
        if parts[0] == "p":
            assert n is None and len(parts) == 4 and parts[1] == "cnf"
            n, declared = map(int, parts[2:])
            assert n >= 0 and declared >= 0
        else:
            assert n is not None and parts[-1] == "0"
            clause = tuple(map(int, parts[:-1]))
            assert len(clause) == len(set(clause))
            assert all(x and abs(x) <= n and -x not in clause for x in clause)
            clauses.append(clause)
    assert declared == len(clauses)
    return n, clauses


def read_cnf(path: Path):
    return parse_cnf_text(path.read_text())


def sat_count(n, clauses):
    total = 0
    for bits in itertools.product((0, 1), repeat=n):
        if all(any(bits[abs(l) - 1] == (l > 0) for l in c) for c in clauses):
            total += 1
    return total


def truth(n, clause):
    out = 0
    for a in range(1 << n):
        if any(((a >> (abs(l) - 1)) & 1) == (l > 0) for l in clause):
            out |= 1 << a
    return out


def support(n, table):
    return sum(
        any(((table >> a) & 1) != ((table >> (a ^ (1 << i))) & 1) for a in range(1 << n))
        for i in range(n)
    )


def affine(n, mask, rhs):
    out = 0
    for a in range(1 << n):
        if ((a & mask).bit_count() & 1) == rhs:
            out |= 1 << a
    return out


def floor_reachable(n, clauses):
    m = len(clauses)
    clause_name = {}
    for digits in itertools.product((-1, 0, 1), repeat=n):
        c = tuple((i + 1) * d for i, d in enumerate(digits) if d)
        clause_name[truth(n, c)] = c
    affine_name = {
        affine(n, mask, rhs): (mask, rhs)
        for mask in range(1 << n)
        for rhs in (0, 1)
    }
    bank = [set() for _ in range(1 << m)]
    for i, c in enumerate(clauses):
        bank[1 << i].add(truth(n, c))
    for count in range(2, m + 1):
        for whole in range(1, 1 << m):
            if whole.bit_count() != count:
                continue
            # Canonical unordered bipartitions.
            least = whole & -whole
            left = (whole - 1) & whole
            while left:
                right = whole ^ left
                if left & least and right:
                    for a in bank[left]:
                        for b in bank[right]:
                            c = a & b
                            if support(n, c) <= 3:
                                bank[whole].add(c)
                            if a in affine_name and b in affine_name:
                                ma, ra = affine_name[a]
                                mb, rb = affine_name[b]
                                bank[whole].add(affine(n, ma ^ mb, ra ^ rb))
                            if a in clause_name and b in clause_name:
                                ca, cb = clause_name[a], clause_name[b]
                                for p in ca:
                                    if -p not in cb:
                                        continue
                                    resolvent = (set(ca) | set(cb)) - {p, -p}
                                    if not any(-x in resolvent for x in resolvent):
                                        bank[whole].add(truth(n, tuple(resolvent)))
                left = (left - 1) & whole
    return 0 in bank[-1], len(bank[-1])


def replay_witness(n, clauses, node):
    if node["op"] == "SOURCE":
        index = node["source_index"]
        got = truth(n, clauses[index])
        assert node["source_set"] == 1 << index and node["truth_table"] == got
        return node["source_set"], got, 0
    left_set, left, left_nodes = replay_witness(n, clauses, node["left"])
    right_set, right, right_nodes = replay_witness(n, clauses, node["right"])
    assert not left_set & right_set
    got = node["truth_table"]
    if node["op"] == "AND3":
        assert got == left & right and support(n, got) <= 3
    elif node["op"] == "XOR":
        affine_name = {
            affine(n, mask, rhs): (mask, rhs)
            for mask in range(1 << n) for rhs in (0, 1)
        }
        assert left in affine_name and right in affine_name
        ml, rl = affine_name[left]
        mr, rr = affine_name[right]
        assert got == affine(n, ml ^ mr, rl ^ rr)
    elif node["op"].startswith("RES("):
        clause_name = {}
        for digits in itertools.product((-1, 0, 1), repeat=n):
            clause = tuple((i + 1) * d for i, d in enumerate(digits) if d)
            clause_name[truth(n, clause)] = clause
        pivot = int(node["op"][4:-1])
        assert left in clause_name and right in clause_name
        cl, cr = clause_name[left], clause_name[right]
        assert pivot in cl and -pivot in cr
        resolvent = (set(cl) | set(cr)) - {pivot, -pivot}
        assert not any(-x in resolvent for x in resolvent)
        assert got == truth(n, tuple(resolvent))
    else:
        raise AssertionError(node["op"])
    assert node["source_set"] == left_set | right_set
    return node["source_set"], got, left_nodes + right_nodes + 1


def parity_k4(charges):
    edges = list(itertools.combinations(range(4), 2))
    number = {edge: i + 1 for i, edge in enumerate(edges)}
    clauses = []
    for vertex in range(4):
        incident = [number[e] for e in edges if vertex in e]
        for local in itertools.product((0, 1), repeat=3):
            if (sum(local) & 1) != charges[vertex]:
                clauses.append(tuple(-v if bit else v for v, bit in zip(incident, local)))
    return len(edges), clauses


def main(raw_path: str):
    raw = json.loads(Path(raw_path).read_text())
    root = Path("results/raw/arc/lspv5_300_peitl")
    checks = 0
    selected = {}
    for record in raw["records"]:
        path = root / record["file"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == record["sha256"]
        n, clauses = read_cnf(path)
        assert n == record["variables"] and clauses == [tuple(c) for c in record["signed_clauses"]]
        assert sat_count(n, clauses) == 0 == record["models"]
        deletion = [sat_count(n, clauses[:i] + clauses[i + 1 :]) for i in range(len(clauses))]
        assert deletion == record["deletion_model_counts"] and all(deletion)
        flips = []
        for ci, clause in enumerate(clauses):
            for li, lit in enumerate(clause):
                changed_clause = list(clause)
                changed_clause[li] = -lit
                changed = list(clauses)
                changed[ci] = tuple(changed_clause)
                flips.append(sat_count(n, changed))
        assert flips == record["sign_flip_model_counts"] and all(flips)
        checks += 4 + len(deletion) + len(flips)
        if "mixed_source_floor_dp" in record:
            got = floor_reachable(n, clauses)
            want = (
                record["mixed_source_floor_dp"]["false_at_source_floor"],
                record["mixed_source_floor_dp"]["terminal_functions"],
            )
            assert got == want
            if got[0]:
                source_set, table, nodes = replay_witness(
                    n, clauses, record["mixed_source_floor_dp"]["contradiction_witness"]
                )
                assert source_set == (1 << len(clauses)) - 1 and table == 0
                assert nodes == len(clauses) - 1
                checks += 3
            selected[record["file"]] = got
            checks += 2
    assert len(raw["records"]) == 19
    odd_n, odd = parity_k4((1, 0, 0, 0))
    even_n, even = parity_k4((0, 0, 0, 0))
    assert sat_count(odd_n, odd) == raw["both_label_parity_controls"]["odd_charge_models"] == 0
    assert sat_count(even_n, even) == raw["both_label_parity_controls"]["even_charge_models"] == 8
    malformed = {
        "missing_header": "1 0\n",
        "bad_keyword": "p sat 1 1\n1 0\n",
        "count_mismatch": "p cnf 1 2\n1 0\n",
        "out_of_range_variable": "p cnf 1 1\n2 0\n",
        "missing_terminator": "p cnf 1 1\n1\n",
        "duplicate_literal": "p cnf 1 1\n1 1 0\n",
        "tautological_clause": "p cnf 1 1\n1 -1 0\n",
        "negative_dimensions": "p cnf -1 0\n",
    }
    rejected = {}
    for name, text in malformed.items():
        try:
            parse_cnf_text(text)
        except (AssertionError, IndexError):
            rejected[name] = True
        else:
            rejected[name] = False
    assert rejected == raw["malformed_controls"] and all(rejected.values())
    checks += 18
    assert all(raw["assertions"].values())
    out = {
        "verified": True,
        "checks": checks,
        "files": 19,
        "mixed_floor_replays": selected,
        "raw_sha256": hashlib.sha256(Path(raw_path).read_bytes()).hexdigest(),
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1])
