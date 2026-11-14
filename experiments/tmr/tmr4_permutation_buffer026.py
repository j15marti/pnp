#!/usr/bin/env python3
"""Finite checks for a streaming truth-table bit-permutation transport barrier.
Pure Python 3, no external packages. Exhaustive tests are finite only.
"""
import json
from collections import defaultdict
from pathlib import Path


def index_swap(j, n):
    low = j & 1
    high = (j >> (n - 1)) & 1
    return (j & ~(1 | (1 << (n - 1)))) | (low << (n - 1)) | high


def permute_table(bits, n):
    N = 1 << n
    return sum(((bits >> index_swap(j, n)) & 1) << j for j in range(N))


def min_gate_yes_sets(n, max_gates=2):
    N = 1 << n
    mask = (1 << N) - 1
    variables = [sum(((j >> i) & 1) << j for j in range(N)) for i in range(n)]
    initial = tuple([0, mask] + variables)
    layers = [set(initial)]
    def descend(wires, steps_left, depth):
        layers[depth].update(wires)
        if not steps_left:
            return
        L = len(wires)
        generated = set()
        for a in range(L):
            generated.add((~wires[a]) & mask)
            for b in range(a, L):
                generated.add(wires[a] & wires[b])
                generated.add(wires[a] | wires[b])
        for gate in generated:
            descend(wires + (gate,), steps_left - 1, depth + 1)
    for _ in range(max_gates):
        layers.append(set())
    descend(initial, max_gates, 0)
    for i in range(1, max_gates+1):
        layers[i].update(layers[i-1])
    return layers


def greedy_frontier(n):
    N = 1 << n
    order = [index_swap(j, n) for j in range(N)]
    ready = 0
    outstanding = []
    for k in range(N + 1):
        while ready < N and order[ready] < k:
            ready += 1
        outstanding.append(k-ready)
    return outstanding, order


def run():
    out = {'run': 'TMR4-TRANS26', 'status': 'COMPUTATIONAL',
           'model': 'one-way source, append-only ordered output, exact truth-table permutation',
           'gate_basis': 'fan-in-2 AND OR, unary NOT, free constants, output any wire',
           'classifications': [], 'prefix_tests': [], 'reread_controls': [], 'checks': 0, 'failed_assertions': 0}
    for n in (2, 3, 4):
        N = 1 << n
        P = [index_swap(j, n) for j in range(N)]
        assert sorted(P) == list(range(N))
        assert all(index_swap(index_swap(j,n),n)==j for j in range(N))
        layers = min_gate_yes_sets(n, 2)
        counts = [len(x) for x in layers]
        for s, accepting in enumerate(layers):
            yes_tests = no_tests = 0
            for t in range(1 << N):
                u = permute_table(t,n)
                assert (t in accepting) == (u in accepting), (n,s,t,u)
                if t in accepting:
                    yes_tests += 1
                else:
                    no_tests += 1
                out['checks'] += 1
            out['classifications'].append({'n':n,'N':N,'s':s,'yes':yes_tests,'no':no_tests,
                                            'all_truth_tables':1 << N,'yes_layers':counts})
        assert counts == sorted(counts)
    for n in (2,3,4,5):
        N = 1 << n
        half = N // 2
        outstanding, order = greedy_frontier(n)
        assert max(outstanding) == half - 1
        assert outstanding[half] == half - 1
        assert order[:2] == [0,half]
        # Explicit two-way reread proxy: no source data stored, only an index and head coordinate.
        reread_moves = sum(abs(order[j] - (order[j-1] if j else 0)) for j in range(N))
        out['reread_controls'].append({'n':n,'N':N,'charged_input_head_moves':reread_moves,
                                       'index_bits':n,'data_buffer_bits':0})
        observed = set()
        for free in range(1 << (half-1)):
            # x[0]=0, x[half..N-1]=0; vary x[1..half-1]
            source = free << 1
            target = permute_table(source, n)
            # first two output positions: y_0=x_0, y_1=x_half, both zero
            assert target & 3 == 0
            suffix = target >> 2
            assert suffix not in observed
            observed.add(suffix)
            out['checks'] += 1
        assert len(observed) == 1 << (half-1)
        out['prefix_tests'].append({'n':n,'N':N,'free_bits_before_middle':half-1,
                                    'distinguishable_future_suffixes':len(observed),
                                    'greedy_peak_outstanding_bits':max(outstanding),
                                    'greedy_at_half':outstanding[half],
                                    'first_target_source_indices':order[:min(8,N)]})
    out['total_exact_truth_table_classifications'] = sum(z['all_truth_tables'] for z in out['classifications'])
    out['total_distinct_future_suffixes_checked'] = sum(z['distinguishable_future_suffixes'] for z in out['prefix_tests'])
    return out


if __name__ == '__main__':
    result = run()
    path = Path(__file__).resolve().parent / 'TMR4_PERMUTATION_BUFFER026_RAW.json'
    path.write_text(json.dumps(result, sort_keys=True, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'checks':result['checks'], 'classifications':result['total_exact_truth_table_classifications'],
                      'future_suffixes':result['total_distinct_future_suffixes_checked'],
                      'failures':result['failed_assertions'],
                      'file':str(path)}, sort_keys=True))
