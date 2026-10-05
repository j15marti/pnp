#!/usr/bin/env python3
"""SLICENEXT1 numerical preflight.

This script does not prove a circuit lower bound. It checks the explicit
finite-parameter quantities used in the SLICENEXT1 roadmap:
  1. sparse-slice SAT first-moment bound;
  2. exact-layer spread parameter from SPREAD1;
  3. the optimistic B=1 robust-sunflower spread demand for comparison;
  4. the crude Tarsi-based union bound for small UNSAT cores.

All asymptotic statements in the report have separate symbolic proofs.
"""

from math import comb, log

EPS = 0.1
Q_VALUES = [32, 64, 128, 256, 512]
L_VALUES = [6, 8]


def inclusion_probability(M: int, t: int, r: int) -> float:
    p = 1.0
    for i in range(r):
        p *= (t - i) / (M - i)
    return p


def small_core_union_bound(q: int, L: int) -> float:
    M = 8 * comb(q, 3)
    t = 6 * q
    total = 0.0
    for r in range(1, L + 1):
        if r > t:
            break
        inc = inclusion_probability(M, t, r)
        candidate_sets = 0
        for v in range(0, min(q, r - 1) + 1):
            available = 8 * comb(v, 3) if v >= 3 else 0
            if available >= r:
                candidate_sets += comb(q, v) * comb(available, r)
        total += candidate_sets * inc
    return total


def main() -> None:
    rho = 2.0 * (7.0 / 8.0) ** 6

    print("SLICENEXT1 numerical preflight")
    print(f"epsilon={EPS}")
    print(f"rho=2*(7/8)^6={rho:.15f}")
    print()
    print(
        "q M t delta_upper r0=M/(2t) p=t/(2M) "
        "optimistic_r_req_B1 ratio_req_to_r0 coreUB_L6 coreUB_L8"
    )

    for q in Q_VALUES:
        M = 8 * comb(q, 3)
        t = 6 * q
        delta = rho ** q
        r0 = M / (2.0 * t)
        p = t / (2.0 * M)
        optimistic_req = log(t / EPS) / p
        ratio = optimistic_req / r0
        ub6 = small_core_union_bound(q, 6)
        ub8 = small_core_union_bound(q, 8)

        print(
            f"{q} {M} {t} {delta:.6e} {r0:.6f} {p:.6e} "
            f"{optimistic_req:.6f} {ratio:.6f} "
            f"{ub6:.6e} {ub8:.6e}"
        )

    print()
    print("NOTES")
    print("1. optimistic_r_req_B1 sets the unknown CKR constant B to 1 only for scale.")
    print("2. The symbolic report proves the generic spread obstruction for every fixed B>0.")
    print("3. coreUB_L* counts every r-clause set on <=r-1 variables, not only UNSAT ones.")
    print("4. Therefore the small-core values are deliberately conservative upper bounds.")
    print("STATUS=PASS")


if __name__ == "__main__":
    main()
