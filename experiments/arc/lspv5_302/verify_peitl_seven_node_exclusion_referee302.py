#!/usr/bin/env python3
"""Independent no-project-import verifier for REFEREE302."""

from __future__ import annotations

import hashlib
import json
import resource
import sys
from pathlib import Path


def parse_dimacs(text):
    n = declared = None
    clauses = []
    for original in text.splitlines():
        line = original.strip()
        if not line or line.startswith("c"):
            continue
        p = line.split()
        if p[0] == "p":
            if n is not None or len(p) != 4 or p[1] != "cnf":
                raise ValueError("bad header")
            n, declared = int(p[2]), int(p[3])
            if n < 0 or declared < 0:
                raise ValueError("bad dimensions")
        else:
            if n is None or p[-1] != "0" or p.count("0") != 1:
                raise ValueError("bad clause")
            c = tuple(map(int, p[:-1]))
            if len(c) != len(set(c)) or any(not x or abs(x) > n or -x in c for x in c):
                raise ValueError("bad literal")
            clauses.append(c)
    if n is None or declared != len(clauses):
        raise ValueError("count mismatch")
    return n, clauses


def clause_table(clause, n):
    table = 0
    for a in range(1 << n):
        if any(((a >> (abs(lit) - 1)) & 1) == int(lit > 0) for lit in clause):
            table |= 1 << a
    return table


def model_count(clauses, n):
    return sum(
        all(any(((a >> (abs(lit) - 1)) & 1) == int(lit > 0) for lit in c) for c in clauses)
        for a in range(1 << n)
    )


def support(table, n):
    return sum(
        any(((table >> a) & 1) != ((table >> (a ^ (1 << i))) & 1) for a in range(1 << n))
        for i in range(n)
    )


def affine_table(mask, rhs, n):
    return sum(1 << a for a in range(1 << n) if ((a & mask).bit_count() & 1) == rhs)


def aliases(n):
    clauses = {}
    for code in range(3**n):
        z, c = code, []
        for v in range(1, n + 1):
            digit, z = z % 3, z // 3
            if digit:
                c.append(v if digit == 1 else -v)
        clauses[clause_table(c, n)] = tuple(c)
    affine = {
        affine_table(mask, rhs, n): (mask, rhs)
        for mask in range(1 << n)
        for rhs in (0, 1)
    }
    return clauses, affine


def mixed(a, b, n, clause_names, affine_names):
    out = set()
    conjunction = a & b
    if support(conjunction, n) <= 3:
        out.add(conjunction)
    if a in affine_names and b in affine_names:
        ma, ra = affine_names[a]
        mb, rb = affine_names[b]
        out.add(affine_table(ma ^ mb, ra ^ rb, n))
    if a in clause_names and b in clause_names:
        ca, cb = clause_names[a], clause_names[b]
        for pivot in ca:
            if -pivot not in cb:
                continue
            raw = (set(ca) | set(cb)) - {pivot, -pivot}
            if not any(-lit in raw for lit in raw):
                out.add(clause_table(raw, n))
    return out


def source_trees(clauses, n, names):
    m = len(clauses)
    bank = [set() for _ in range(1 << m)]
    for i, c in enumerate(clauses):
        bank[1 << i].add(clause_table(c, n))
    tests = 0
    for size in range(2, m + 1):
        for whole in range(1, 1 << m):
            if whole.bit_count() != size:
                continue
            least = whole & -whole
            left = (whole - 1) & whole
            while left:
                right = whole ^ left
                if left & least and right:
                    for a in bank[left]:
                        for b in bank[right]:
                            tests += 1
                            bank[whole].update(mixed(a, b, n, *names))
                left = (left - 1) & whole
    return bank, tests


def unicycle(clauses, n):
    m, full = len(clauses), (1 << len(clauses)) - 1
    names = aliases(n)
    trees, tree_tests = source_trees(clauses, n, names)
    source_tables = [clause_table(c, n) for c in clauses]
    cache = {}

    def extend(shared, mask):
        key = (shared, mask)
        if key in cache:
            return cache[key]
        atoms = [shared] + [source_tables[i] for i in range(m) if mask >> i & 1]
        bank = [set() for _ in range(1 << len(atoms))]
        for i, table in enumerate(atoms):
            bank[1 << i].add(table)
        for size in range(2, len(atoms) + 1):
            for whole in range(1, 1 << len(atoms)):
                if whole.bit_count() != size:
                    continue
                least = whole & -whole
                left = (whole - 1) & whole
                while left:
                    right = whole ^ left
                    if left & least and right:
                        for a in bank[left]:
                            for b in bank[right]:
                                bank[whole].update(mixed(a, b, n, *names))
                    left = (left - 1) & whole
        cache[key] = bank[-1]
        return bank[-1]

    root_tests = 0
    for shared_mask in range(1, full + 1):
        rest = full ^ shared_mask
        tail = rest
        while True:
            cycle_rest = rest ^ tail
            left = cycle_rest
            while True:
                right = cycle_rest ^ left
                if left <= right:
                    for shared in trees[shared_mask]:
                        for a in extend(shared, left):
                            for b in extend(shared, right):
                                root_tests += 1
                                for cycle in mixed(a, b, n, *names):
                                    if 0 in extend(cycle, tail):
                                        return {"found": True}
                if left == 0:
                    break
                left = (left - 1) & cycle_rest
            if tail == 0:
                break
            tail = (tail - 1) & rest
    return {
        "found": False,
        "root_tests": root_tests,
        "cache_size": len(cache),
        "tree_tests": tree_tests,
        "terminal": len(trees[full]),
        "floor_false": 0 in trees[full],
    }


def canon(clause):
    return tuple(sorted(set(clause), key=lambda x: (abs(x), x < 0)))


def replay(clauses, certificate):
    lines = [canon(c) for c in clauses]
    for step in certificate:
        left, right = step["left_line"] - 1, step["right_line"] - 1
        if left < 0 or right < 0 or left >= len(lines) or right >= len(lines):
            return False
        pivot = step["pivot"]
        if pivot not in lines[left] or -pivot not in lines[right]:
            return False
        raw = (set(lines[left]) | set(lines[right])) - {pivot, -pivot}
        if any(-lit in raw for lit in raw) or canon(raw) != canon(step["clause"]):
            return False
        lines.append(canon(raw))
    return bool(lines) and lines[-1] == ()


def main():
    raw_path, out_path = map(Path, sys.argv[1:3])
    raw = json.loads(raw_path.read_text())
    source_bytes = Path(raw["input"]["path"]).read_bytes()
    n, clauses = parse_dimacs(source_bytes.decode())
    checks = 0
    assert hashlib.sha256(source_bytes).hexdigest() == raw["input"]["sha256"]; checks += 1
    assert model_count(clauses, n) == 0; checks += 1
    deletions = [model_count(clauses[:i] + clauses[i + 1 :], n) for i in range(len(clauses))]
    assert deletions == raw["input"]["deletion_model_counts"] and all(deletions); checks += len(deletions)
    flips = []
    for i, clause in enumerate(clauses):
        for j in range(len(clause)):
            changed = [list(c) for c in clauses]
            changed[i][j] *= -1
            flips.append(model_count(changed, n))
    assert flips == raw["input"]["sign_flip_model_counts"] and all(flips); checks += len(flips)
    search = unicycle(clauses, n)
    assert search == {"found": False, "root_tests": 16907, "cache_size": 3621, "tree_tests": 2231, "terminal": 50, "floor_false": False}; checks += 6
    assert replay(clauses, raw["resolution_upper_certificate"]); checks += 9
    assert not replay(clauses, raw["resolution_upper_certificate"][:-1]); checks += 1
    bad = [
        "1 0\n", "p sat 1 1\n1 0\n", "p cnf 1 2\n1 0\n", "p cnf 1 1\n2 0\n",
        "p cnf 1 1\n1\n", "p cnf 1 1\n1 1 0\n", "p cnf 1 1\n1 -1 0\n", "p cnf -1 0\n",
    ]
    for text in bad:
        try:
            parse_dimacs(text)
            raise AssertionError("malformed accepted")
        except ValueError:
            checks += 1
    assert raw["mixed_cost_interval"] == [8, 9]
    assert all(raw["assertions"].values()); checks += 2
    result = {
        "verified": True,
        "checks": checks,
        "mixed_cost_interval": [8, 9],
        "search": search,
        "raw_sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest(),
        "python": sys.version.split()[0],
        "peak_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
    }
    out_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
