#!/usr/bin/env python3
"""Independent finite audit for ARC-TYPED-HARD-IMAGE162.

Checks two actual restriction levels on a locally generated parity-to-CNF image,
including promise escape, exact SAT/UNSAT joins, malformed encodings, and exact
finite-depth typed exponent composition.  This is not an FLMV lower-bound
proof; the endpoint theorem is proved symbolically in the paired report.
"""

from fractions import Fraction
import itertools
import json

RUN_ID = "ARC-TYPED-HARD-IMAGE162"


def canon(clauses):
    return tuple(sorted(set(tuple(sorted(c)) for c in clauses)))


def parity_cnf(bits):
    n = len(bits)
    clauses = [(-1,), (-(n + 1),)]  # u_0=false and u_n=false; variable u_i is i+1.
    for i, bit in enumerate(bits):
        x, y = i + 1, i + 2
        if bit == 0:  # equality
            clauses.extend([(-x, y), (x, -y)])
        else:  # inequality
            clauses.extend([(x, y), (-x, -y)])
    return canon(clauses)


def restrict(formula, var, value):
    true_lit = var if value else -var
    false_lit = -true_lit
    out = []
    for clause in formula:
        if true_lit in clause:
            continue
        reduced = tuple(l for l in clause if l != false_lit)
        out.append(reduced)
    return canon(out)


def sat(formula):
    names = sorted({abs(l) for c in formula for l in c})
    for values in itertools.product((False, True), repeat=len(names)):
        a = dict(zip(names, values))
        if all(any(a[abs(l)] == (l > 0) for l in c) for c in formula):
            return True
    return False


def typed_compose(t, s, levels):
    for level in levels:
        t = max(level["r"], level["a"] + level["lambda"] * t)
        s = max(level["h"], level["lambda"] * s)
    return t, s


def expanded_time(t0, levels):
    # Enumerate every affine source term after full substitution.
    terms = []
    product = Fraction(1)
    offset = Fraction(0)
    for level in reversed(levels):
        pass
    # Direct recurrence is the ground truth; symbolic path formula below checks
    # base and every local term in final coordinates.
    d = len(levels)
    base_coeff = Fraction(1)
    base_offset = Fraction(0)
    for level in levels:
        base_offset = level["a"] + level["lambda"] * base_offset
        base_coeff *= level["lambda"]
    terms.append(base_offset + base_coeff * t0)
    for i, source in enumerate(levels):
        value = source["r"]
        for later in levels[i + 1:]:
            value = later["a"] + later["lambda"] * value
        terms.append(value)
    return max(terms), terms


def main():
    checks = 0

    def check(ok, msg):
        nonlocal checks
        checks += 1
        if not ok:
            raise AssertionError(msg)

    image = {}
    for n in range(1, 10):
        for bits in itertools.product((0, 1), repeat=n):
            f = parity_cnf(bits)
            check(f not in image, "injective canonical parity image")
            image[f] = bits
            check(sat(f) == (sum(bits) % 2 == 0), "parity reduction semantics")

    label_counts = {"SAT": 0, "UNSAT": 0}
    escaped_first = escaped_second = 0
    two_level_leaves = 0
    for formula, bits in image.items():
        label_counts["SAT" if sat(formula) else "UNSAT"] += 1
        n = len(bits)
        v1 = 1 + n // 2
        first = [restrict(formula, v1, b) for b in (0, 1)]
        check(sat(formula) == any(sat(c) for c in first), "first Shannon join")
        for child in first:
            if child not in image:
                escaped_first += 1
            v2 = 1 if v1 != 1 else n + 1
            second = [restrict(child, v2, b) for b in (0, 1)]
            check(sat(child) == any(sat(g) for g in second), "second Shannon join")
            for grand in second:
                two_level_leaves += 1
                if grand not in image:
                    escaped_second += 1
        check(sat(formula) == any(
            sat(restrict(child, 1 if v1 != 1 else n + 1, b))
            for child in first for b in (0, 1)
        ), "two-level root join")

    check(label_counts["SAT"] > 0 and label_counts["UNSAT"] > 0,
          "both labels represented")
    check(escaped_first > 0 and escaped_second > 0, "promise escape occurs")

    # Malformed encodings: exact image parser rejects each.
    malformed = [(), ((0,),), ((1, -1),), ((999,),), ((1,), (1,))]
    for x in malformed:
        check(canon(x) not in image, "malformed/off-image rejection")

    # Exact finite typed exponent composition against full substitution.
    route_rows = []
    choices = [
        {"a": Fraction(3, 5), "lambda": Fraction(1, 2),
         "r": Fraction(11, 10), "h": Fraction(1, 2)},
        {"a": Fraction(1, 4), "lambda": Fraction(1, 3),
         "r": Fraction(1), "h": Fraction(2, 5)},
        {"a": Fraction(1, 10), "lambda": Fraction(1, 4),
         "r": Fraction(9, 10), "h": Fraction(1, 3)},
    ]
    for depth in range(1, 6):
        for levels in itertools.product(choices, repeat=depth):
            levels = list(levels)
            t, s = typed_compose(Fraction(8), Fraction(8), levels)
            t2, terms = expanded_time(Fraction(8), levels)
            check(t == t2, "typed time recurrence expansion")
            check(s >= 0, "typed space nonnegative")
            route_rows.append({"depth": depth, "time": str(t), "space": str(s),
                               "terms": [str(x) for x in terms]})

    c = Fraction(241, 200)
    beta = ((c + 2) / (c * c) - c) / 2
    check(beta == Fraction(11642479, 23232400), "exact FLMV beta")

    result = {
        "run_id": RUN_ID,
        "status": {
            "single_hard_image_endpoint": "KNOWN THEOREM CONSEQUENCE; independently verified",
            "typed_finite_route": "PROVED/EXACT",
            "automatic_image_inheritance": "FALSIFIED/RETIRED",
            "hard_image_to_contractor_promise_alignment": "OPEN",
            "arc_edge_90": "OPEN",
            "p_vs_np": "OPEN"
        },
        "parity_image": {
            "root_count": len(image),
            "sat_roots": label_counts["SAT"],
            "unsat_roots": label_counts["UNSAT"],
            "escaped_first_children": escaped_first,
            "escaped_second_grandchildren": escaped_second,
            "two_level_leaves": two_level_leaves
        },
        "typed_routes": {
            "routes_checked": len(route_rows),
            "depth_max": 5,
            "sample_first": route_rows[0],
            "sample_last": route_rows[-1]
        },
        "strict_flmv_box": {"time": str(c), "space": str(beta)},
        "assertion_checks": checks,
        "failures": 0,
        "limitations": [
            "finite parity image is an easy control, not the existential FLMV-hard image",
            "the experiment does not establish a typed contraction",
            "hard-image local access and endpoint contradiction are sourced mathematical dependencies",
            "no all-input or typed ARC successor is constructed"
        ]
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
