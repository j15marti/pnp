#!/usr/bin/env python3
"""PRIMECRT1: exact prime/CRT Boolean semantics and provenance controls.

Deterministic experiment for the LSPV-5 PRIME-LQP branch.
Uses only the Python standard library.
"""
from itertools import product
import json
import math
import random

SEED = 20261002

def first_primes(n):
    ps = []
    x = 2
    while len(ps) < n:
        ok = True
        r = int(x ** 0.5)
        for p in ps:
            if p > r:
                break
            if x % p == 0:
                ok = False
                break
        if ok:
            ps.append(x)
        x += 1
    return ps

def crt_encode(bits, primes):
    Q = math.prod(primes)
    x = 0
    for b, p in zip(bits, primes):
        M = Q // p
        inv = pow(M, -1, p)
        x = (x + b * M * inv) % Q
    return x

def crt_decode(x, primes):
    return tuple(x % p for p in primes)

def eval_expr(e, assignment):
    op = e[0]
    if op == "var":
        return assignment[e[1]]
    if op == "not":
        return 1 - eval_expr(e[1], assignment)
    a = eval_expr(e[1], assignment)
    b = eval_expr(e[2], assignment)
    if op == "and":
        return a & b
    if op == "or":
        return a | b
    if op == "xor":
        return a ^ b
    raise ValueError(op)

def truth_table(e, n=5):
    return tuple(eval_expr(e, a) for a in product([0, 1], repeat=n))

def symbol_seq(e):
    op = e[0]
    if op == "var":
        return [10 + e[1]]
    if op == "not":
        return [1] + symbol_seq(e[1])
    code = {"and": 2, "or": 3, "xor": 4}[op]
    return [code] + symbol_seq(e[1]) + symbol_seq(e[2])

def godel_code(seq):
    ps = first_primes(len(seq))
    return math.prod(pow(p, c) for p, c in zip(ps, seq))

def context_apply(name, e):
    x2 = ("var", 2)
    if name == "not":
        return ("not", e)
    if name == "and_x2":
        return ("and", e, x2)
    if name == "or_x2":
        return ("or", e, x2)
    if name == "xor_x2":
        return ("xor", e, x2)
    raise ValueError(name)

def main():
    n = 5
    primes = first_primes(2 ** n)
    Q = math.prod(primes)

    x0 = ("var", 0)
    x1 = ("var", 1)
    pairs = [
        ("double_not", x0, ("not", ("not", x0))),
        ("absorption", x0, ("and", x0, ("or", x0, x1))),
        ("de_morgan", ("not", ("and", x0, x1)),
         ("or", ("not", x0), ("not", x1))),
    ]

    pair_results = []
    for name, a, b in pairs:
        ta, tb = truth_table(a, n), truth_table(b, n)
        ca, cb = crt_encode(ta, primes), crt_encode(tb, primes)
        sa, sb = symbol_seq(a), symbol_seq(b)
        pa, pb = godel_code(sa), godel_code(sb)
        contexts = {}
        for ctx in ["not", "and_x2", "or_x2", "xor_x2"]:
            contexts[ctx] = (
                truth_table(context_apply(ctx, a), n)
                == truth_table(context_apply(ctx, b), n)
            )
        pair_results.append({
            "name": name,
            "truth_equal": ta == tb,
            "crt_equal": ca == cb,
            "provenance_sequence_equal": sa == sb,
            "godel_code_equal": pa == pb,
            "all_tested_contexts_equal": all(contexts.values()),
            "contexts": contexts,
            "godel_bit_lengths": [pa.bit_length(), pb.bit_length()],
        })

    small_primes = first_primes(5)
    smallQ = math.prod(small_primes)
    states = {
        bits: crt_encode(bits, small_primes)
        for bits in product([0, 1], repeat=5)
    }
    small_ok = True
    for ba, a in states.items():
        small_ok &= (
            crt_decode((1 - a) % smallQ, small_primes)
            == tuple(1 - x for x in ba)
        )
        small_ok &= ((a * a - a) % smallQ == 0)
        for bb, b in states.items():
            small_ok &= (
                crt_decode((a * b) % smallQ, small_primes)
                == tuple(x & y for x, y in zip(ba, bb))
            )
            small_ok &= (
                crt_decode((a + b - a * b) % smallQ, small_primes)
                == tuple(x | y for x, y in zip(ba, bb))
            )

    rng = random.Random(SEED)
    random_ok = True
    for _ in range(500):
        ba = tuple(rng.randrange(2) for _ in range(32))
        bb = tuple(rng.randrange(2) for _ in range(32))
        a = crt_encode(ba, primes)
        b = crt_encode(bb, primes)
        random_ok &= (
            crt_decode((1 - a) % Q, primes)
            == tuple(1 - x for x in ba)
        )
        random_ok &= (
            crt_decode((a * b) % Q, primes)
            == tuple(x & y for x, y in zip(ba, bb))
        )
        random_ok &= (
            crt_decode((a + b - a * b) % Q, primes)
            == tuple(x | y for x, y in zip(ba, bb))
        )
        if not random_ok:
            break

    ps = first_primes(1000)
    growth = []
    for T in [5, 10, 20, 50, 100, 200, 500, 1000]:
        log2P = sum(8 * math.log2(p) for p in ps[:T])
        growth.append({
            "T": T,
            "upper_code_bits_C8": math.ceil(log2P),
            "bits_over_Tlog2T": log2P / (T * math.log2(max(T, 2))),
        })

    result = {
        "experiment": "PRIMECRT1",
        "seed": SEED,
        "n_variables": 5,
        "truth_table_coordinates": 32,
        "truth_table_modulus_bits": Q.bit_length(),
        "truth_table_modulus_prime_count": 32,
        "small_exhaustive_k": 5,
        "small_exhaustive_states": 32,
        "small_boolean_algebra_verified": bool(small_ok),
        "n5_random_state_trials": 500,
        "n5_random_state_boolean_algebra_verified": bool(random_ok),
        "equivalent_expression_pairs": pair_results,
        "prime_semiring_evaluation_collision": {
            "lhs": "x*y+z",
            "rhs": "w",
            "assignment": {"x": 2, "y": 3, "z": 5, "w": 11},
            "lhs_value": 2 * 3 + 5,
            "rhs_value": 11,
            "collision": (2 * 3 + 5 == 11),
        },
        "negation_dual_indeterminate_plain_prime_failure": {
            "positive_prime": 2,
            "negative_prime": 3,
            "product": 6,
            "required_annihilation_value": 0,
            "preserves_annihilation": False,
        },
        "positional_prime_code_growth": growth,
    }
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
