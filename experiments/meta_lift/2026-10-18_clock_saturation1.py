#!/usr/bin/env python3
"""CLOCKSAT1: exact finite controls for clock-indexed two-probe diagonal gates.
Pure Python 3, stdlib only. The toy decoder is not a complexity lower bound.
"""
import json

M_BITS, D_BITS, S_BITS, C_MAX, WITNESSES, SIGMA = 8, 2, 2, 2, 4, 1
M = 1 << M_BITS

def toy_decoder(d, c, i, z):
    # Simulated preprocessing of a depth-two adaptive decision tree.
    steps = (d + 1) * (i % 13 + 1)
    workspace = (d + i // 7) % 12
    if steps > M_BITS ** c or workspace > M_BITS ** SIGMA:
        return 0  # clock / space timeout default, including per-coordinate fallback
    if d == 0:
        return 0
    if d == 1:
        return (z >> ((i + d) % S_BITS)) & 1
    if d == 2:
        first = (z >> ((i + 1) % S_BITS)) & 1
        second = (z >> ((i + d + first) % S_BITS)) & 1
        return first ^ second
    if d == 3:
        first = (z >> ((i + 1) % S_BITS)) & 1
        second = (z >> ((i + first) % S_BITS)) & 1
        return first & (1 - second)
    raise AssertionError("decoder out of range")

PAIR_COUNT = (1 << D_BITS) * (1 << S_BITS)
assert WITNESSES * C_MAX * PAIR_COUNT <= M

def address(w, c, d, z):
    return (w * C_MAX * PAIR_COUNT
            + (c - 1) * PAIR_COUNT
            + d * (1 << S_BITS) + z)

def build_target(mask):
    x = [0] * M
    for w in range(WITNESSES):
        if (mask >> w) & 1:
            for c in range(1, C_MAX + 1):
                for d in range(1 << D_BITS):
                    for z in range(1 << S_BITS):
                        i = address(w, c, d, z)
                        x[i] = 1 - toy_decoder(d, c, i, z)
    return x

def audit():
    adversarial_checks = 0
    failures = 0
    easy_controls = 0
    for mask in range(1 << WITNESSES):
        x = build_target(mask)
        if mask == 0:
            for c in range(1, C_MAX + 1):
                # The zero decoder can represent the all-zero target.
                if all(toy_decoder(0, c, i, 0) == x[i] for i in range(M)):
                    easy_controls += 1
        else:
            for c in range(1, C_MAX + 1):
                for d in range(1 << D_BITS):
                    for z in range(1 << S_BITS):
                        adversarial_checks += 1
                        i = next(address(w, c, d, z) for w in range(WITNESSES)
                                 if (mask >> w) & 1)
                        # Check the critical mismatch, then the entire vector.
                        assert x[i] != toy_decoder(d, c, i, z)
                        if all(x[j] == toy_decoder(d, c, j, z)
                               for j in range(M)):
                            failures += 1
    assert adversarial_checks == 480
    assert easy_controls == 2
    assert failures == 0
    return {
        "report": "CLOCKSAT1",
        "date": "2026-10-18",
        "model": "Toy adaptive two-probe decoders, explicit per-coordinate timeouts",
        "M": M,
        "description_bits": D_BITS,
        "seed_bits": S_BITS,
        "clock_exponents": list(range(1, C_MAX + 1)),
        "witness_addresses": WITNESSES,
        "source_masks_exhaustively_tested": 1 << WITNESSES,
        "nonempty_source_adversarial_checks": adversarial_checks,
        "failures": failures,
        "allzero_easy_clock_controls": easy_controls,
        "status": "COMPUTATIONAL finite audit only",
        "limitations": ("No asymptotic lower bound; source masks have four "
                        "witness positions; generalized proof is symbolic.")
    }

if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
