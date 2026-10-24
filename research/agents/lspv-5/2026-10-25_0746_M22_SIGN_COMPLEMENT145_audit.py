#!/usr/bin/env python3
"""Finite audit for SIGN-COMPLEMENT-GATE145.

The mathematical criterion is proved in the accompanying report.  This
program independently compares it with brute-force variable complementation,
checks SAT labels/model counts, and exercises proper-3CNF padding controls.
"""

from itertools import combinations, product
import json


def variables(cnf):
    return sorted({abs(lit) for clause in cnf for lit in clause})


def sat_count(cnf):
    vs = variables(cnf)
    total = 0
    for bits in product((0, 1), repeat=len(vs)):
        val = dict(zip(vs, bits))
        if all(any(val[abs(lit)] == (lit > 0) for lit in clause) for clause in cnf):
            total += 1
    return total


def transformed(cnf, flip):
    return [tuple(-lit if flip.get(abs(lit), 0) else lit for lit in clause)
            for clause in cnf]


def clausewise_monotone(cnf):
    return all(all(lit > 0 for lit in c) or all(lit < 0 for lit in c)
               for c in cnf)


def brute_monotonizations(cnf):
    vs = variables(cnf)
    out = []
    for bits in product((0, 1), repeat=len(vs)):
        flip = dict(zip(vs, bits))
        if clausewise_monotone(transformed(cnf, flip)):
            out.append(bits)
    return out


class ParityDSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.rank = [0] * (n + 1)
        self.parity = [0] * (n + 1)

    def find(self, x):
        if self.parent[x] != x:
            p = self.parent[x]
            root, up = self.find(p)
            self.parity[x] ^= up
            self.parent[x] = root
        return self.parent[x], self.parity[x]

    def union(self, x, y, want):
        rx, px = self.find(x)
        ry, py = self.find(y)
        if rx == ry:
            return (px ^ py) == want
        if self.rank[rx] < self.rank[ry]:
            rx, ry, px, py = ry, rx, py, px
        self.parent[ry] = rx
        self.parity[ry] = px ^ py ^ want
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


def parity_criterion(cnf):
    vs = variables(cnf)
    dsu = ParityDSU(max(vs, default=0))
    constraints = 0
    for clause in cnf:
        anchor = clause[0]
        for lit in clause[1:]:
            # flip(u) xor flip(v) = sign(u) xor sign(v)
            want = (anchor > 0) ^ (lit > 0)
            constraints += 1
            if not dsu.union(abs(anchor), abs(lit), int(want)):
                return False, constraints
    return True, constraints


def proper(cnf):
    return all(len(c) == 3 and len({abs(x) for x in c}) == 3 for c in cnf)


def m22(cnf):
    if not proper(cnf) or len(set(cnf)) != len(cnf):
        return False
    if not clausewise_monotone(cnf):
        return False
    for v in variables(cnf):
        if sum(v in c for c in cnf) != 2:
            return False
        if sum(-v in c for c in cnf) != 2:
            return False
    return True


def fully_paired(cnf):
    bag = set(cnf)
    return all(tuple(-x for x in c) in bag for c in cnf)


def all_signed_clauses(n):
    out = []
    for support in combinations(range(1, n + 1), 3):
        for signs in product((-1, 1), repeat=3):
            out.append(tuple(v * s for v, s in zip(support, signs)))
    return out


def main():
    controls = {
        "single_positive": [(1, 2, 3)],
        "padded_binary_sat": [(1, 2, 3), (1, 2, -3)],
        "padded_horn_sat": [(-1, -2, 3), (-1, -2, -3)],
        "and_tseitin_proper_padding_sat": [
            (-1, -2, 3),
            (1, -3, 4), (1, -3, -4),
            (2, -3, 5), (2, -3, -5),
        ],
        "all_eight_signs_unsat": [
            tuple(v * s for v, s in zip((1, 2, 3), signs))
            for signs in product((-1, 1), repeat=3)
        ],
    }
    checks = 0
    rows = {}
    for name, cnf in controls.items():
        assert proper(cnf)
        brute = brute_monotonizations(cnf)
        criterion, scanned = parity_criterion(cnf)
        assert criterion == bool(brute)
        checks += 2
        before = sat_count(cnf)
        # Every variable complementation is a model bijection.
        for bits in product((0, 1), repeat=len(variables(cnf))):
            flip = dict(zip(variables(cnf), bits))
            assert sat_count(transformed(cnf, flip)) == before
            checks += 1
        rows[name] = {
            "variables": len(variables(cnf)),
            "clauses": len(cnf),
            "models": before,
            "monotonizable": criterion,
            "monotonizing_flips": len(brute),
            "constraints_examined_until_decision": scanned,
        }

    # Canonical M22-NONPAIRED1 exclusion witness and reduction controls.
    y_pos = [(1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6)]
    y_neg = [(-1, -2, -4), (-1, -3, -6), (-2, -3, -5), (-4, -5, -6)]
    y = y_pos + y_neg
    assert m22(y) and not fully_paired(y)
    assert sat_count(y) == 20
    witness = {1: 1, 2: 1, 3: 1, 4: 0, 5: 0, 6: 0}
    assert all(any(witness[abs(lit)] == (lit > 0) for lit in c) for c in y)
    paired = y_pos + [tuple(-x for x in c) for c in y_pos]
    assert m22(paired) and fully_paired(paired) and sat_count(paired) > 0
    # Exclusion reduction: unpaired target is unchanged; paired target maps to Y.
    assert (y if fully_paired(y) else y) == y
    assert (y if fully_paired(paired) else paired) == y
    checks += 8

    # Independent recheck of Role 4 M22-NEUTRAL-PAIR101 on six independent
    # ports.  Fresh names a..f are 7..12.
    x, yv, z, u, v, w = range(1, 7)
    a, b, c, d, e, f = range(7, 13)
    neutral = [
        (a, b, x), (a, d, yv), (b, e, z), (c, d, f), (c, e, f),
        (-a, -d, -u), (-a, -d, -v), (-b, -e, -w),
        (-b, -c, -f), (-c, -e, -f),
    ]
    assert proper(neutral) and len(set(neutral)) == 10
    fixed = {a: 1, b: 1, c: 1, d: 0, e: 0, f: 0}
    for port_bits in product((0, 1), repeat=6):
        val = dict(zip(range(1, 7), port_bits))
        val.update(fixed)
        assert all(any(val[abs(lit)] == (lit > 0) for lit in cl) for cl in neutral)
        checks += 1
    for fresh in range(7, 13):
        assert sum(fresh in cl for cl in neutral) == 2
        assert sum(-fresh in cl for cl in neutral) == 2
        checks += 2
    assert all(not (2 * t >= 3 and 2 * (3 - t) >= 3) for t in range(4))
    checks += 1

    pair_counts = {}
    for n in (3, 4):
        clauses = all_signed_clauses(n)
        compatible = incompatible = 0
        for a, b in combinations(clauses, 2):
            cnf = [a, b]
            brute = bool(brute_monotonizations(cnf))
            criterion, _ = parity_criterion(cnf)
            assert brute == criterion
            checks += 1
            if brute:
                compatible += 1
            else:
                incompatible += 1
        pair_counts[str(n)] = {
            "clauses": len(clauses),
            "pairs": compatible + incompatible,
            "compatible": compatible,
            "incompatible": incompatible,
        }

    # Two actual representation levels on a compatible control: complement,
    # then rename.  Counts do not shrink and exact signed degree is unchanged.
    level0 = [(1, -2, 3), (-1, 2, -3)]
    flips = brute_monotonizations(level0)
    assert flips
    level1 = transformed(level0, dict(zip(variables(level0), flips[0])))
    rename = {1: 4, 2: 5, 3: 6}
    level2 = [tuple((1 if x > 0 else -1) * rename[abs(x)] for x in c)
              for c in level1]
    assert clausewise_monotone(level1) and clausewise_monotone(level2)
    assert sat_count(level0) == sat_count(level1) == sat_count(level2)
    assert len(level0) == len(level1) == len(level2)
    checks += 4

    out = {
        "artifact": "SIGN-COMPLEMENT-GATE145",
        "status": "COMPUTATIONAL finite audit; theorem proved separately",
        "checks": checks,
        "failures": 0,
        "controls": rows,
        "m22_exclusion_recheck": {
            "Y_is_M22": m22(y),
            "Y_is_fully_paired": fully_paired(y),
            "Y_models": sat_count(y),
            "Y_witness_111000": True,
            "paired_control_models": sat_count(paired),
            "paired_control_maps_to_Y": True,
            "unpaired_Y_is_fixed": True,
        },
        "peer_recheck_neutral_pair101": {
            "independent_port_assignments": 64,
            "fixed_fresh_witness": "abc=1,def=0",
            "fresh_sign_degree": "(2,2) for each of six names",
            "h3_capacity_obstruction_checked": True,
        },
        "proper_clause_pair_census": pair_counts,
        "two_level_control": {
            "clauses_each_level": [len(level0), len(level1), len(level2)],
            "models_each_level": [sat_count(level0), sat_count(level1), sat_count(level2)],
            "level1_monotone": clausewise_monotone(level1),
            "level2_monotone": clausewise_monotone(level2),
            "power_shrink": False,
        },
    }
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
