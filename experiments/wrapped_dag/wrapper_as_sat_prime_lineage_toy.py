#!/usr/bin/env python3
"""
Toy WRAPPER-AS-SAT construction with multisign prime lineage and recursive control.

Base SAT instance:
    F(x1,x2,x3) = x1 AND x2
with x3 free.

The wrapper has a free seed s selecting the first SAT restriction test x1=s.
Because F requires x1=1:
    beta1 = SAT(F | x1=s) = s.

Self-reduction preserves satisfiability by always choosing x1=1, but records
different lineage:
    seed 1 -> T
    seed 0 -> NOT_FALSE.

The two histories reconverge at the same nominal node.  Lineage then selects
the next actual SAT restriction:
    T         -> test x2=1
    NOT_FALSE -> test x2=0.
Again beta2 equals the test bit, and self-reduction selects x2=1.

Prime labels:
    x1: T=2, F=3, NOT_TRUE=5, NOT_FALSE=7
    x2: T=11, F=13, NOT_TRUE=17, NOT_FALSE=19

A small rolling hash and an exact prime product are functionally constrained.

Tests:
1. single-route existential-seed wrapper projects exactly to F;
2. either lineage route can satisfy the wrapper individually;
3. paired fixed-seed wrapper (both routes simultaneously) still projects to F;
4. falsely equating the two post-merge lineage states makes the paired formula UNSAT;
5. for fixed satisfying x and seed, the auxiliary extension is unique.

This is a finite structural example, not a P-vs-NP lower bound.
"""

from itertools import product
import json


class CNF:
    def __init__(self):
        self.varmap = {}
        self.rev = {}
        self.clauses = []

    def v(self, name):
        if name not in self.varmap:
            i = len(self.varmap) + 1
            self.varmap[name] = i
            self.rev[i] = name
        return self.varmap[name]

    def add(self, *lits):
        self.clauses.append(tuple(lits))

    def unit(self, name, value=True):
        i = self.v(name)
        self.add(i if value else -i)

    def equiv(self, a, b):
        if isinstance(a, str):
            a = self.v(a)
        if isinstance(b, str):
            b = self.v(b)
        self.add(-a, b)
        self.add(a, -b)

    def equiv_not(self, a, b):
        if isinstance(a, str):
            a = self.v(a)
        if isinstance(b, str):
            b = self.v(b)
        self.add(-a, -b)
        self.add(a, b)

    def onehot(self, names):
        ids = [self.v(x) for x in names]
        self.add(*ids)
        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                self.add(-ids[i], -ids[j])


def simplify(clauses, assignment):
    out = []
    for clause in clauses:
        satisfied = False
        live = []
        for lit in clause:
            v = abs(lit)
            if v in assignment:
                if (lit > 0 and assignment[v]) or (lit < 0 and not assignment[v]):
                    satisfied = True
                    break
            else:
                live.append(lit)
        if satisfied:
            continue
        if not live:
            return None
        out.append(tuple(live))
    return out


def dpll(clauses, assignment=None):
    assignment = {} if assignment is None else dict(assignment)
    clauses = simplify(clauses, assignment)
    if clauses is None:
        return None

    while True:
        unit = next((c[0] for c in clauses if len(c) == 1), None)
        if unit is None:
            break
        v = abs(unit)
        val = unit > 0
        if v in assignment and assignment[v] != val:
            return None
        assignment[v] = val
        clauses = simplify(clauses, assignment)
        if clauses is None:
            return None

    if not clauses:
        return assignment

    v = abs(clauses[0][0])
    for val in (True, False):
        branch = dict(assignment)
        branch[v] = val
        result = dpll(clauses, branch)
        if result is not None:
            return result
    return None


def encode_onehot_code(cnf, labels, values, bits):
    cnf.onehot(labels)
    for label, value in zip(labels, values):
        lv = cnf.v(label)
        for k, bit_name in enumerate(bits):
            bv = cnf.v(bit_name)
            cnf.add(-lv, bv if ((value >> k) & 1) else -bv)


def encode_pair_product(cnf, labels1, vals1, labels2, vals2, bits):
    for l1, v1 in zip(labels1, vals1):
        a = cnf.v(l1)
        for l2, v2 in zip(labels2, vals2):
            b = cnf.v(l2)
            p = v1 * v2
            for k, bit_name in enumerate(bits):
                pb = cnf.v(bit_name)
                cnf.add(-a, -b, pb if ((p >> k) & 1) else -pb)


def encode_and(cnf, out, a, b):
    o = cnf.v(out)
    av = cnf.v(a)
    bv = cnf.v(b)
    cnf.add(-o, av)
    cnf.add(-o, bv)
    cnf.add(o, -av, -bv)


def build_trace(cnf, prefix, seed_fixed=None):
    cnf.v("x1")
    cnf.v("x2")
    cnf.v("x3")

    seed = cnf.v(f"{prefix}_s")
    if seed_fixed is not None:
        cnf.add(seed if seed_fixed else -seed)

    # Stage 1: actual toy SAT query SAT(F | x1=seed) = seed.
    cnf.equiv(f"{prefix}_t1", seed)
    cnf.equiv(f"{prefix}_b1", f"{prefix}_t1")
    cnf.unit(f"{prefix}_a1", True)

    L1 = [
        f"{prefix}_L1_T",
        f"{prefix}_L1_F",
        f"{prefix}_L1_NT",
        f"{prefix}_L1_NF",
    ]
    cnf.onehot(L1)
    cnf.equiv(L1[0], f"{prefix}_b1")
    cnf.unit(L1[1], False)
    cnf.unit(L1[2], False)
    cnf.equiv_not(L1[3], f"{prefix}_b1")

    p1_bits = [f"{prefix}_p1_{k}" for k in range(3)]
    encode_onehot_code(cnf, L1, [2, 3, 5, 7], p1_bits)

    # Nominal reconvergence. NOT_FALSE takes a detour, then both revisit QUERY.
    cnf.unit(f"{prefix}_M1", True)
    cnf.equiv(f"{prefix}_detour", L1[3])
    cnf.unit(f"{prefix}_Qreturn", True)

    # Stage 2: lineage controls the next real SAT restriction.
    # T -> test x2=1. NOT_FALSE -> test x2=0.
    cnf.equiv(f"{prefix}_t2", L1[0])
    cnf.equiv(f"{prefix}_b2", f"{prefix}_t2")
    cnf.unit(f"{prefix}_a2", True)

    L2 = [
        f"{prefix}_L2_T",
        f"{prefix}_L2_F",
        f"{prefix}_L2_NT",
        f"{prefix}_L2_NF",
    ]
    cnf.onehot(L2)
    cnf.equiv(L2[0], f"{prefix}_b2")
    cnf.unit(L2[1], False)
    cnf.unit(L2[2], False)
    cnf.equiv_not(L2[3], f"{prefix}_b2")

    p2_bits = [f"{prefix}_p2_{k}" for k in range(5)]
    encode_onehot_code(cnf, L2, [11, 13, 17, 19], p2_bits)

    # Hash h1 = p1 mod 16.
    h1_bits = [f"{prefix}_h1_{k}" for k in range(4)]
    encode_onehot_code(cnf, L1, [2, 3, 5, 7], h1_bits)

    # Hash h2 = (3*h1 + p2) mod 16.
    h2_bits = [f"{prefix}_h2_{k}" for k in range(4)]
    for l1, v1 in zip(L1, [2, 3, 5, 7]):
        a = cnf.v(l1)
        for l2, v2 in zip(L2, [11, 13, 17, 19]):
            b = cnf.v(l2)
            hv = (3 * v1 + v2) % 16
            for k, bit_name in enumerate(h2_bits):
                hb = cnf.v(bit_name)
                cnf.add(-a, -b, hb if ((hv >> k) & 1) else -hb)

    # Exact prime product for both lineage coordinates.
    product_bits = [f"{prefix}_P_{k}" for k in range(8)]
    encode_pair_product(
        cnf,
        L1, [2, 3, 5, 7],
        L2, [11, 13, 17, 19],
        product_bits,
    )

    encode_and(cnf, f"{prefix}_out", f"{prefix}_a1", f"{prefix}_a2")
    cnf.unit(f"{prefix}_out", True)

    # Projection onto original variables recovers F = x1 AND x2.
    cnf.equiv("x1", f"{prefix}_a1")
    cnf.equiv("x2", f"{prefix}_a2")

    return {
        "L1": L1,
        "L2": L2,
        "Pbits": product_bits,
    }


def sat(cnf, fixed=None):
    fixed = {} if fixed is None else fixed
    assignment = {cnf.v(k): v for k, v in fixed.items()}
    return dpll(cnf.clauses, assignment)


def complete_model(cnf, fixed=None):
    fixed = {} if fixed is None else fixed
    assignment = {cnf.v(k): v for k, v in fixed.items()}
    model = dpll(cnf.clauses, assignment)
    if model is None:
        return None
    model = dict(model)
    for v in range(1, len(cnf.varmap) + 1):
        if v in model:
            continue
        for val in (False, True):
            trial = dict(model)
            trial[v] = val
            if dpll(cnf.clauses, trial) is not None:
                model[v] = val
                break
    return model


def unique_extension(cnf, fixed):
    model = complete_model(cnf, fixed)
    if model is None:
        return False
    fixed_ids = {cnf.v(k) for k in fixed}
    block = []
    for v, val in model.items():
        if v in fixed_ids:
            continue
        block.append(-v if val else v)
    second = dpll(
        cnf.clauses + [tuple(block)],
        {cnf.v(k): v for k, v in fixed.items()},
    )
    return second is None


def bits_to_int(model, cnf, names):
    return sum(
        1 << k
        for k, name in enumerate(names)
        if bool(model.get(cnf.v(name), False))
    )


def route_summary(seed):
    cnf = CNF()
    info = build_trace(cnf, "R", seed)
    model = complete_model(cnf)

    def bit(name):
        return bool(model.get(cnf.v(name), False))

    L1 = next(name.split("_")[-1] for name in info["L1"] if bit(name))
    L2 = next(name.split("_")[-1] for name in info["L2"] if bit(name))

    return {
        "seed": seed,
        "t1": bit("R_t1"),
        "beta1": bit("R_b1"),
        "chosen_x1": bit("R_a1"),
        "lineage1": L1,
        "prime1": bits_to_int(model, cnf, [f"R_p1_{k}" for k in range(3)]),
        "detour": bit("R_detour"),
        "t2": bit("R_t2"),
        "beta2": bit("R_b2"),
        "chosen_x2": bit("R_a2"),
        "lineage2": L2,
        "prime2": bits_to_int(model, cnf, [f"R_p2_{k}" for k in range(5)]),
        "prime_product": bits_to_int(model, cnf, [f"R_P_{k}" for k in range(8)]),
        "hash1": bits_to_int(model, cnf, [f"R_h1_{k}" for k in range(4)]),
        "hash2": bits_to_int(model, cnf, [f"R_h2_{k}" for k in range(4)]),
        "output": bit("R_out"),
    }


def projection_table(cnf):
    rows = []
    for x1, x2, x3 in product([False, True], repeat=3):
        rows.append({
            "x": [int(x1), int(x2), int(x3)],
            "extension_exists": sat(cnf, {"x1": x1, "x2": x2, "x3": x3}) is not None,
            "F": bool(x1 and x2),
        })
    return rows


def main():
    single = CNF()
    single_info = build_trace(single, "R")

    force_T = CNF()
    build_trace(force_T, "R")
    force_T.unit("R_L1_T", True)

    force_NF = CNF()
    build_trace(force_NF, "R")
    force_NF.unit("R_L1_NF", True)

    pair = CNF()
    pair0 = build_trace(pair, "A", 0)
    pair1 = build_trace(pair, "B", 1)

    bad_merge = CNF()
    bad0 = build_trace(bad_merge, "A", 0)
    bad1 = build_trace(bad_merge, "B", 1)
    for a, b in zip(bad0["L1"], bad1["L1"]):
        bad_merge.equiv(a, b)

    result = {
        "status": "COMPUTATIONAL_EXACT_FINITE",
        "base_formula": "F(x1,x2,x3) = x1 AND x2; x3 free",
        "routes": [route_summary(0), route_summary(1)],
        "single_existential_seed": {
            "variables": len(single.varmap),
            "clauses": len(single.clauses),
            "satisfiable": sat(single) is not None,
            "force_T_route_satisfiable": sat(force_T) is not None,
            "force_NOT_FALSE_route_satisfiable": sat(force_NF) is not None,
            "projection": projection_table(single),
        },
        "paired_all_routes": {
            "variables": len(pair.varmap),
            "clauses": len(pair.clauses),
            "satisfiable": sat(pair) is not None,
            "projection": projection_table(pair),
        },
        "paired_with_false_merge": {
            "variables": len(bad_merge.varmap),
            "clauses": len(bad_merge.clauses),
            "satisfiable": sat(bad_merge) is not None,
            "projection": projection_table(bad_merge),
        },
        "unique_extensions": {
            "seed0_at_x110_x3_0": unique_extension(
                (lambda c: (build_trace(c, "R", 0), c)[1])(CNF()),
                {"x1": True, "x2": True, "x3": False},
            ),
            "seed1_at_x110_x3_0": unique_extension(
                (lambda c: (build_trace(c, "R", 1), c)[1])(CNF()),
                {"x1": True, "x2": True, "x3": False},
            ),
        },
        "interpretation": [
            "Both seeds end at the same semantic SAT output but carry different exact lineage, prime products, hashes, and control paths.",
            "Existential seed choice does not force simultaneous route support: either route can be selected and satisfied individually.",
            "Conjoining both fixed-seed executions is still equisatisfiable with the base formula.",
            "Equating the two distinct lineage states at the nominal merge makes the paired formula unsatisfiable.",
            "Existential projection of the correct wrapper variables recovers exactly F=x1 AND x2.",
            "This establishes formula-internal nonmergeability in the paired construction, not an unrestricted SAT time lower bound."
        ],
    }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
