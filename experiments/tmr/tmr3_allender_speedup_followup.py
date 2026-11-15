#!/usr/bin/env python3
"""Exact finite audits for an Allender checkpoint-speedup follow-up.

Python 3.10+, standard library only. Run:
    python audit_speedup.py --output results.json
These tests verify arithmetic and small path-count identities, not asymptotic
hierarchy containments, physical Turing-machine costs, or P versus NP.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path
import platform
import random

CHECKS: Counter[str] = Counter()
SEED = 20261115

def check(condition: bool, category: str) -> None:
    if not condition:
        raise AssertionError(f"Failed check: {category}")
    CHECKS[category] += 1

def mm(a: list[list[int]], b: list[list[int]]) -> list[list[int]]:
    q = len(a)
    return [[sum(a[i][k]*b[k][j] for k in range(q)) for j in range(q)] for i in range(q)]

def product(mats: list[list[list[int]]], q: int) -> list[list[int]]:
    answer = [[int(i == j) for j in range(q)] for i in range(q)]
    for mat in mats:
        answer = mm(answer, mat)
    return answer

def run() -> dict:
    exponent_rows = []
    for k in range(2, 257):
        m = k - 1
        old = 1 + F(1, 4*m)
        new = 1 + F(2, 5*m)
        check(old**m < F(4, 3), 'old_rational_margin')
        check(new**m < F(97, 65), 'new_rational_margin')
        check(F(3, 2) - new**m > F(1, 130), 'new_uniform_exponent_slack')
        check((new-1)/(old-1) == F(8, 5), 'coefficient_improvement')
        if k in (2, 3, 5, 10, 20, 50, 100):
            exponent_rows.append({'k':k,'old_d':str(old),'new_d':str(new),
                                  'new_d_power':str(new**m),
                                  'root_ceiling_approx':1.5**(1/m)})

    # Parameters for the CONDITIONAL fixed-depth speedup implication.
    # K is synthetic, never a measured arithmetic-circuit depth.
    linear_cases = 0
    for numerator in range(1, 64):
        delta = F(numerator, 64)
        sigma = 1-delta
        b = 1 + delta/4
        for K in range(2, 65):
            m = K-1
            d = 1 + delta/(8*m)
            alpha = b*d
            padded_sigma = b*sigma
            check(padded_sigma < 1, 'padded_space_sublinear')
            check(alpha+padded_sigma < 2, 'one_checkpoint_layer_budget')
            check(d**m < b, 'conditional_hierarchy_contradiction')
            check(d**m < 1/(1-delta/8), 'conditional_geometric_bound')
            check(b-1/(1-delta/8) == delta*(4-delta)/(4*(8-delta)), 'exact_conditional_slack')
            linear_cases += 1

    # Fair-coin comparison with inclusive majority:
    # A = f + (2^q-y) accepting paths out of 2^(q+1), for 0<=y<=2^q.
    # Exact equality can be checked with two exact threshold-oracle answers.
    count_cases = 0
    for q in range(0, 8):
        bound = 1 << q
        for f in range(bound+1):
            eq_candidates = []
            for y in range(bound+1):
                A = f + bound-y
                check((A >= bound) == (f >= y), 'threshold_ties')
                ge = A >= bound
                ge_next = False if y == bound else (f+bound-(y+1) >= bound)
                exact = ge and not ge_next
                check(exact == (f == y), 'exact_count_candidate')
                if exact:
                    eq_candidates.append(y)
                count_cases += 1
            check(eq_candidates == [f], 'unique_count_value')
            for bit in range(q+1):
                accept_candidates = sum((y >> bit) & 1 for y in eq_candidates)
                check(accept_candidates == ((f >> bit) & 1), 'count_bit_oracle_leaf')

    # Direct coin-string enumeration versus matrix multiplication and an
    # independently enumerated checkpoint sum-product.
    rng = random.Random(SEED)
    graph_cases = 0
    for q in (2, 3, 4):
        for length in range(1, 9):
            for trial in range(5):
                edges = [[[rng.randrange(q) for _ in range(2)] for _ in range(q)]
                         for _ in range(length)]
                mats = []
                for layer in edges:
                    mat = [[0]*q for _ in range(q)]
                    for state in range(q):
                        for nxt in layer[state]:
                            mat[state][nxt] += 1
                    mats.append(mat)
                direct = [[0]*q for _ in range(q)]
                for start in range(q):
                    for coins in itertools.product((0, 1), repeat=length):
                        state = start
                        for step, coin in enumerate(coins):
                            state = edges[step][state][coin]
                        direct[start][state] += 1
                check(direct == product(mats, q), 'path_count_coin_vs_matrix')
                for block in (2, 3, 4):
                    chunks = [product(mats[i:i+block], q) for i in range(0, length, block)]
                    for start in range(q):
                        for end in range(q):
                            total = 0
                            for checkpoints in itertools.product(range(q), repeat=len(chunks)-1):
                                vertices = (start,)+checkpoints+(end,)
                                weight = 1
                                for i, chunk in enumerate(chunks):
                                    weight *= chunk[vertices[i]][vertices[i+1]]
                                total += weight
                            check(total == direct[start][end], 'checkpoint_sum_product')
                graph_cases += 1

    # Hostile controls: majority-call composition, multiplicity loss,
    # endpoint equality, and checkpoint budget outside the allowed region.
    p = F(17, 32)
    check(p > F(1, 2) and p*p < F(1, 2), 'weak_PP_AND_fails')
    check(product([[[2, 0],[0, 2]]], 2)[0][0] == 2, 'parallel_edges_count_twice')
    check(product([[[1, 0],[0, 1]]], 2)[0][0] != 2, 'booleanization_fails')
    check(F(13,10)+F(9,10) > 2, 'checkpoint_budget_rejects_blowup')
    check(F(3,2) ** 1 == F(3,2), 'strict_boundary_required')

    return {
        'status':'COMPUTATIONAL', 'failures':0,
        'assertions':sum(CHECKS.values()), 'assertions_by_category':dict(CHECKS),
        'parameters':{'k_range':[2,256],'synthetic_K_range':[2,64],
                      'delta_grid':'1/64,...,63/64','count_random_bits_range':[0,7],
                      'path_states':[2,3,4],'path_lengths':[1,8],
                      'path_trials_per_pair':5,'checkpoint_block_sizes':[2,3,4],
                      'random_seed':SEED},
        'cases':{'linear_margin_parameter_pairs':linear_cases,
                 'threshold_count_pairs':count_cases,'layered_graphs':graph_cases},
        'exponent_examples':exponent_rows,
        'python':platform.python_version(),
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'limitations':['No physical Turing-machine compiler was executed.',
                      'No uniform arithmetic-circuit depth K was measured.',
                      'Finite identities do not prove hierarchy class containments.',
                      'No SAT algorithm or MajMajSAT-to-SAT reduction was constructed.',
                      'The fixed-depth refinement requires independent mathematical review.']
    }

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('results.json'))
    args = parser.parse_args()
    data = run()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'assertions':data['assertions'],'failures':data['failures'],
                      'cases':data['cases'],'output':str(args.output)}, indent=2))

if __name__ == '__main__':
    main()
