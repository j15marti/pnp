#!/usr/bin/env python3
"""Exact finite audit for POSTPROCESSING-FIREWALL6."""

from fractions import Fraction
import json


def canonical_distributions(repeats):
    """alpha=1/2 public exposure; transcript includes public seeds."""
    denom = 1 << repeats
    p0, p1 = {}, {}
    for seeds in range(denom):
        state0 = (seeds, 0)
        state1 = (seeds, seeds)
        p0[state0] = p0.get(state0, Fraction(0)) + Fraction(1, denom)
        p1[state1] = p1.get(state1, Fraction(0)) + Fraction(1, denom)
    return p0, p1


def tv(p, q):
    return sum(abs(p.get(x, 0) - q.get(x, 0))
               for x in set(p) | set(q)) / 2


def compressed_tv(p, q, states, truth_table):
    p_one = sum(p.get(state, 0) for i, state in enumerate(states)
                if (truth_table >> i) & 1)
    q_one = sum(q.get(state, 0) for i, state in enumerate(states)
                if (truth_table >> i) & 1)
    return abs(p_one - q_one)


def main():
    records = []
    total_compressors = 0
    checks = 0
    for r in (1, 2, 3):
        p, q = canonical_distributions(r)
        states = sorted(set(p) | set(q))
        input_tv = tv(p, q)
        expected = 1 - Fraction(1, 2) ** r
        assert input_tv == expected
        checks += 1
        max_output_tv = Fraction(0)
        maximizers = 0
        for table in range(1 << len(states)):
            out_tv = compressed_tv(p, q, states, table)
            assert out_tv <= input_tv
            checks += 1
            if out_tv > max_output_tv:
                max_output_tv = out_tv
                maximizers = 1
            elif out_tv == max_output_tv:
                maximizers += 1
        assert max_output_tv == input_tv
        checks += 1
        total_compressors += 1 << len(states)
        records.append({
            "repetitions": r,
            "union_transcript_states": len(states),
            "boolean_compressors_enumerated": 1 << len(states),
            "input_tv": {"numerator": input_tv.numerator,
                         "denominator": input_tv.denominator},
            "maximum_compressed_tv": {"numerator": max_output_tv.numerator,
                                      "denominator": max_output_tv.denominator},
            "maximizing_compressors": maximizers,
        })

    result = {
        "artifact": "POSTPROCESSING-FIREWALL6",
        "status": "COMPUTATIONAL_EXACT_FINITE",
        "canonical_alpha": "1/2",
        "records": records,
        "total_boolean_compressors": total_compressors,
        "assertions": checks,
        "failures": 0,
        "scope": [
            "finite exhaustive Boolean postprocessors for r=1,2,3",
            "symbolic theorem covers arbitrary deterministic or randomized source-oblivious postprocessing",
            "direct extra source access is outside the Markov-postprocessing hypothesis",
        ],
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
