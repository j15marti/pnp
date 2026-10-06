#!/usr/bin/env python3
"""
Exact hash-continuation quotient experiment.

Computes the recursive continuation signature of every reachable
answer-preserving self-reduction state and reports:
  * raw signature width,
  * the labeled-subset baseline C(n,d),
  * same-subset semantic fiber width,
  * excess quotient ratio.

Finite computational diagnostic only; not a lower bound.
"""

from functools import lru_cache
from itertools import product
import argparse
import json
import math
import random


class CNF:
    def __init__(self, n, clauses):
        self.n = n
        self.clauses = tuple(tuple(c) for c in clauses)
        self.sat_assignments = tuple(
            a for a in range(1 << n) if self._eval_assignment(a)
        )

    def _eval_assignment(self, a):
        for clause in self.clauses:
            ok = False
            for lit in clause:
                v = abs(lit) - 1
                bit = (a >> v) & 1
                if (lit > 0 and bit) or (lit < 0 and not bit):
                    ok = True
                    break
            if not ok:
                return False
        return True

    @lru_cache(None)
    def sat(self, mask, vals):
        vals &= mask
        for a in self.sat_assignments:
            if (a & mask) == vals:
                return True
        return False


def planted_cnf(n, m, width, seed, family):
    rng = random.Random(seed)
    planted = [rng.randrange(2) for _ in range(n)]
    clauses = []

    if family == "horn":
        planted = [0] * n
        while len(clauses) < m:
            vs = rng.sample(range(n), 3)
            pos = rng.choice([-1, 0, 1, 2])
            clauses.append(tuple(
                (v + 1) if j == pos else -(v + 1)
                for j, v in enumerate(vs)
            ))
        return clauses

    while len(clauses) < m:
        if family == "path":
            i = rng.randrange(max(1, n - 2))
            vs = list(range(i, min(i + 3, n)))
            if len(vs) < 3:
                vs = [n - 3, n - 2, n - 1]
        else:
            vs = rng.sample(range(n), width)

        lits = []
        for v in vs:
            positive = rng.randrange(2)
            lits.append((v + 1) if positive else -(v + 1))

        if any(
            (1 if lit > 0 else 0) == planted[abs(lit) - 1]
            for lit in lits
        ):
            clauses.append(tuple(lits))
    return clauses


def xor3_to_cnf(vs, rhs):
    clauses = []
    for bits in product([0, 1], repeat=3):
        if bits[0] ^ bits[1] ^ bits[2] != rhs:
            clauses.append(tuple(
                (v + 1) if b == 0 else -(v + 1)
                for v, b in zip(vs, bits)
            ))
    return clauses


def planted_xor_cnf(n, equations, seed):
    rng = random.Random(seed)
    planted = [rng.randrange(2) for _ in range(n)]
    clauses = []
    for _ in range(equations):
        vs = tuple(rng.sample(range(n), 3))
        rhs = planted[vs[0]] ^ planted[vs[1]] ^ planted[vs[2]]
        clauses.extend(xor3_to_cnf(vs, rhs))
    return clauses


def transition(model, state, v):
    mask, vals = state
    parent = model.sat(mask, vals)
    cmask = mask | (1 << v)
    zero_vals = vals & ~(1 << v)
    b0 = model.sat(cmask, zero_vals)
    bit = 0 if b0 == parent else 1
    child_vals = zero_vals | (bit << v)
    return int(b0), (cmask, child_vals)


def exact_quotient(model):
    n = model.n
    reachable = [set() for _ in range(n + 1)]
    reachable[0].add((0, 0))

    for d in range(n):
        for state in reachable[d]:
            mask, _ = state
            for v in range(n):
                if not ((mask >> v) & 1):
                    _, child = transition(model, state, v)
                    reachable[d + 1].add(child)

    sig_id = {}
    intern = {}
    next_id = 0
    depth_rows = [None] * (n + 1)

    for d in range(n, -1, -1):
        by_mask = {}
        depth_ids = set()

        for state in reachable[d]:
            mask, vals = state
            parent = int(model.sat(mask, vals))

            if d == n:
                key = ("T", parent)
            else:
                items = []
                for v in range(n):
                    if not ((mask >> v) & 1):
                        b0, child = transition(model, state, v)
                        items.append((v, b0, sig_id[child]))
                key = (parent, tuple(items))

            if key not in intern:
                intern[key] = next_id
                next_id += 1

            sid = intern[key]
            sig_id[state] = sid
            depth_ids.add(sid)
            by_mask.setdefault(mask, set()).add(sid)

        baseline = math.comb(n, d)
        fiber_sizes = [len(x) for x in by_mask.values()]
        depth_rows[d] = {
            "depth": d,
            "reachable_states": len(reachable[d]),
            "signature_width": len(depth_ids),
            "subset_baseline": baseline,
            "excess_width_ratio": len(depth_ids) / baseline,
            "max_same_subset_signature_fiber": max(fiber_sizes, default=0),
            "multi_signature_masks": sum(x > 1 for x in fiber_sizes),
            "sum_excess_signatures": sum(x - 1 for x in fiber_sizes),
        }

    return {
        "sat_assignments": len(model.sat_assignments),
        "depth_metrics": depth_rows,
        "max_same_subset_signature_fiber": max(
            x["max_same_subset_signature_fiber"] for x in depth_rows
        ),
        "max_excess_width_ratio": max(
            x["excess_width_ratio"] for x in depth_rows
        ),
    }


def make_case(n, family, seed):
    if family == "planted-3SAT":
        clauses = planted_cnf(n, 2 * n, 3, seed, "random")
    elif family == "planted-2SAT":
        clauses = planted_cnf(n, 2 * n, 2, seed, "random")
    elif family == "Horn-3CNF":
        clauses = planted_cnf(n, 2 * n, 3, seed, "horn")
    elif family == "path-3CNF":
        clauses = planted_cnf(n, 2 * n, 3, seed, "path")
    elif family == "3XOR-CNF":
        clauses = planted_xor_cnf(n, max(1, n // 2), seed)
    else:
        raise ValueError(f"unknown family: {family}")
    return CNF(n, clauses)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=3)
    ap.add_argument("--n", type=int, nargs="+", default=[8, 10, 12, 14])
    args = ap.parse_args()

    families = [
        "planted-3SAT",
        "planted-2SAT",
        "Horn-3CNF",
        "path-3CNF",
        "3XOR-CNF",
    ]

    results = {
        "status": "COMPUTATIONAL_EXACT_FINITE",
        "seed": args.seed,
        "instances": [],
    }

    for n in args.n:
        for family in families:
            model = make_case(n, family, args.seed)
            row = exact_quotient(model)
            row.update({"n": n, "family": family})
            results["instances"].append(row)

    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
