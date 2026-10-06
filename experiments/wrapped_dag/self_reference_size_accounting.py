#!/usr/bin/env python3
"""
Self-reference size-accounting test for a wrapper-as-SAT diagonal attempt.

Desired diagonal form:
    Phi is SAT iff A(Phi) rejects.

Declared time-unrolled encoding model:
    m >= alpha*T + b
    T >= m^K

Thus a necessary condition is:
    m >= alpha*m^K + b.

This is an accounting test for ordinary time-unrolled Cook-Levin/Tseitin
encodings, not a theorem ruling out every conceivable succinct encoding.
"""

import json


def rows(ms=(8,16,32,64,128,256,512,1024,4096,16384),
         Ks=(1,2,3,5,10), alpha_num=1, alpha_den=1, base=1):
    out = []
    for K in Ks:
        for m in ms:
            T = m ** K
            encoded_num = alpha_num * T + base * alpha_den
            out.append({
                "K": K,
                "m": m,
                "required_runtime_steps_T": T,
                "fits_inside_m": encoded_num <= m * alpha_den,
                "size_ratio_tableau_over_formula": encoded_num / (m * alpha_den),
            })
    return out


def fixed_point_iteration(K, start=2, rounds=6, cap=10**120):
    seq = [start]
    m = start
    for _ in range(rounds):
        if m > cap:
            seq.append(f">{cap}")
            break
        nxt = m ** K + 1
        if nxt > cap:
            seq.append(f">{cap}")
            break
        seq.append(nxt)
        m = nxt
    return seq


def run():
    return {
        "status": "ACCOUNTING_EXACT_FOR_DECLARED_MODEL",
        "necessary_inequality": "m >= alpha*m^K + b",
        "assumptions": {
            "alpha": 1,
            "b": 1,
            "meaning": "at least one encoding unit per simulated step plus positive base overhead",
        },
        "rows": rows(),
        "fixed_point_examples": {
            str(K): fixed_point_iteration(K)
            for K in (1,2,3,5)
        },
        "interpretation": [
            "For K=1 with alpha=1 and positive base overhead, m >= m+b is impossible.",
            "For K>1, alpha*m^K+b exceeds m for every m>=1 in this declared model.",
            "A standard time-unrolled self-containing tableau therefore cannot close the diagonal loop.",
            "A more succinct encoding would require a separate generic compression theorem and cannot be assumed for arbitrary computations."
        ],
    }


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
