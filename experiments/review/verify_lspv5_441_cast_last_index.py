#!/usr/bin/env python3
"""Independent reconstruction of the LSPV-3/507 last-index selector bug."""

from itertools import product
import json
from pathlib import Path
import resource
import time


GRAPHS = {
    "K4": (4, [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]),
    "K33": (6, [(i, 3 + j) for i in range(3) for j in range(3)]),
    "cube": (8, [(i, j) for i in range(8) for j in range(i + 1, 8)
                  if (i ^ j) and ((i ^ j) & ((i ^ j) - 1)) == 0]),
}


def norm(c):
    return tuple(sorted(set(c), key=lambda x: (abs(x), x)))


def make(name, replace):
    h, edges = GRAPHS[name]
    n = len(edges)
    origin, groups = [], []
    for v in range(h):
        ids = [j + 1 for j, e in enumerate(edges) if v in e]
        row = []
        for b in range(8):
            bits = [(b >> j) & 1 for j in range(3)]
            if (sum(bits) & 1) != (1 if v == 0 else 0):
                row.append(len(origin))
                origin.append(norm([-x if bit else x for x, bit in zip(ids, bits)]))
        groups.append(row)
    c = origin[replace]
    a, b, zlit = c
    u, z = n + 1, n + 2
    A = norm((a, b, u))
    source_index, source = [], []
    for j, clause in enumerate(origin):
        source_index.append(len(source))
        if j == replace:
            source.extend((A, norm((-u, zlit, z)), norm((-u, zlit, -z))))
        else:
            source.append(clause)
    return h, n, origin, groups, source, source_index, c, A


def exact_parity(clauses, variables, rhs):
    for bits in product((False, True), repeat=len(variables)):
        val = dict(zip(variables, bits))
        conjunction = all(any(val[abs(lit)] == (lit > 0) for lit in clause)
                          for clause in clauses)
        parity = (sum(bits) & 1) == rhs
        if conjunction != parity:
            return False
    return True


def main():
    started = time.perf_counter()
    published_failures, repaired_passes, total = [], 0, 0
    for name in GRAPHS:
        count = 4 * GRAPHS[name][0]
        for replace in range(count):
            h, n, origin, groups, source, source_index, C, A = make(name, replace)
            for w in (1, 2, 4):
                total += 1
                selected_bad, selected_fixed = [], []
                for row in groups:
                    bad_row, fixed_row = [], []
                    for j in row:
                        if j == len(source_index) - 1:
                            bad_row.append(source[source_index[j]])
                        elif j == replace:
                            bad_row.append(C)
                        else:
                            bad_row.append(source[source_index[j]])
                        fixed_row.append(C if j == replace else source[source_index[j]])
                    selected_bad.append(bad_row)
                    selected_fixed.append(fixed_row)
                fixed_ok = all(exact_parity(row, sorted({abs(x) for c in row for x in c}),
                                            1 if v == 0 else 0)
                               for v, row in enumerate(selected_fixed))
                if not fixed_ok:
                    raise AssertionError("repair lost an exact vertex parity")
                repaired_passes += 1
                bad_support_ok = all(all(abs(x) <= n for c in row for x in c)
                                     for row in selected_bad)
                if not bad_support_ok:
                    published_failures.append({"graph": name, "replace": replace, "w": w,
                                               "fresh_u": n + 1})
    expected = [{"K4": 15, "K33": 23, "cube": 31}[name] for name in GRAPHS]
    got = sorted({(x["graph"], x["replace"]) for x in published_failures})
    want = sorted(zip(GRAPHS, expected))
    assert total == 216 and repaired_passes == 216
    assert len(published_failures) == 9 and got == want
    result = {
        "status": "INDEPENDENT_STRUCTURAL_REPLAY",
        "total_parameter_cases": total,
        "published_failures": published_failures,
        "one_line_repair_exact_parity_cases": repaired_passes,
        "diagnosis": "Only a final-origin-index replacement selects source A containing fresh u instead of CAST(C); AND3's original-variable support guard rejects it.",
        "wall_seconds": time.perf_counter() - started,
        "max_rss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "historical_R_mix341": "NOT_EXECUTED",
        "p_vs_np": "OPEN",
    }
    out = Path("experiments/review/raw/lspv5_441_cast_last_index_independent.json")
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
