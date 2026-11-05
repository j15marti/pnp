#!/usr/bin/env python3
"""Standalone checker for ternary-shift one-hot CNF binary-resolution traces.

Run python verify_traces.py proof_results.json [--extra trace.json] [--output report.json].
A proof bundle supplies "certificate" and "pruned_example"; a standalone trace
supplies n, edges and steps. --extra accepts "-", standalone JSON, or a prior
report containing its extra trace; a bundled example can therefore be replayed.
The producer is neither imported nor run by this verifier.
"""

import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys


def axioms(n, edges):
    # (positive-variable mask, negative-variable mask); variable v,color c
    # occupies bit 3*v+c, with 1-based pivot IDs in the trace.
    if type(n) is not int or n < 0:
        raise ValueError("invalid number of vertices")
    for v in range(n):
        a = 1 << (3*v)
        b, c = a << 1, a << 2
        yield a | b | c, 0
        yield 0, a | b
        yield 0, a | c
        yield 0, b | c
    for u, v, allowed in edges:
        if any(type(w) is not int or not 0 <= w < n for w in (u, v)):
            raise ValueError("invalid endpoint")
        if any(type(d) is not int or not 0 <= d < 3 for d in allowed):
            raise ValueError("invalid offset")
        if len(set(allowed)) != len(allowed):
            raise ValueError("duplicate allowed shift")
        for left_color in range(3):
            left = 1 << (3*u + left_color)
            if len(allowed) == 1:
                right_color = (left_color + allowed[0]) % 3
                right = 1 << (3*v + right_color)
                yield right, left
                yield left, right
            else:
                for right_color in range(3):
                    if (right_color - left_color) % 3 not in allowed:
                        yield 0, left | (1 << (3*v + right_color))


def verify(case):
    n, steps = case["n"], case["steps"]
    ledger = list(axioms(n, case["edges"]))
    source_size = len(ledger)
    for number, (i, j, p) in enumerate(steps, start=source_size):
        if (any(type(x) is not int for x in (i, j, p))
                or not (0 <= i < number and 0 <= j < number and 1 <= p <= 3*n)):
            raise ValueError(f"invalid reference or pivot at clause {number}")
        pos_i, neg_i = ledger[i]
        pos_j, neg_j = ledger[j]
        bit = 1 << (p - 1)
        if not (pos_i & bit and neg_j & bit):
            raise ValueError(f"missing complementary literals at clause {number}")
        ledger.append(((pos_i ^ bit) | pos_j, neg_i | (neg_j ^ bit)))
    if not steps or ledger[-1] != (0, 0):
        raise ValueError("the final derived clause is nonempty or missing")
    return dict(axioms=source_size, resolution_steps=len(steps),
                maximum_width=max(p.bit_count() + n.bit_count() for p, n in ledger))


def reject_change(case):
    try:
        verify(case)
    except ValueError as error:
        return str(error)
    raise AssertionError("selected corruption still passed")


def check_mutations(case):
    results = {}
    # These substitutions leave all IDs in their legal numeric ranges.
    alternate = deepcopy(case)
    step = alternate["steps"][-1]
    step[2] = step[2] % (3*case["n"]) + 1
    results["changed_in_range_pivot"] = reject_change(alternate)
    alternate = deepcopy(case)
    step = alternate["steps"][-1]
    step[0] = step[1]
    results["changed_in_range_parent"] = reject_change(alternate)
    alternate = deepcopy(case)
    alternate["steps"].pop()
    results["truncated_proof"] = reject_change(alternate)
    # A source constraint can be unused. Locate a semantics-changing
    # mutation which invalidates this particular trace.
    for i, (_, _, shifts) in enumerate(case["edges"]):
        options = ([-d % 3 for d in shifts], [(d+1) % 3 for d in shifts])
        for j, candidate in enumerate(options):
            if set(candidate) == set(shifts):
                continue
            alternate = deepcopy(case)
            alternate["edges"][i][2] = candidate
            try:
                verify(alternate)
            except ValueError as error:
                results["changed_source_edge"] = dict(edge=i, original=shifts,
                    replacement=candidate, mutation=("negate" if j == 0 else "rotate"), error=str(error))
                return results
    raise AssertionError("no rejected source mutation found")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    parser.add_argument("--extra", help="additional trace JSON, or '-' for stdin")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.loads(args.bundle.read_text())
    cases = {"input": data} if "steps" in data else {
        name: data[name] for name in ("certificate", "pruned_example")}
    result = {name: {"verified": verify(case)} for name, case in cases.items()}
    if "certificate" in cases:
        for name, case in cases.items():
            result[name]["rejected_mutations"] = check_mutations(case)
    if args.extra:
        extra = json.loads(sys.stdin.read() if args.extra == "-" else Path(args.extra).read_text())
        if "extra" in extra:
            extra = extra["extra"]["trace"]
        result["extra"] = {"verified": verify(extra), "trace": extra}
        for key in ("description", "retained", "order"):
            if key in extra:
                result["extra"][key] = extra[key]
    report = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(report + "\n")
    else:
        print(report)


if __name__ == "__main__":
    main()
