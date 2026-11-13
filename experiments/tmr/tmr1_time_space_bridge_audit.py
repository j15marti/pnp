#!/usr/bin/env python3
"""TMR-1/002: exact integer audits of same-machine time/space extraction.
All calculations are mathematical budgets, NOT simulated SAT machines.
Python standard library only. Deterministic, no random seed.
"""
import json
from itertools import combinations_with_replacement
from pathlib import Path

OUT = Path(__file__).with_name('2026-11-13_1402_TMR1_TS_BRIDGE_RAW.json')


def source_length(n: int) -> int:
    assert n >= 1
    variables = 5 * n
    width = max(1, (variables - 1).bit_length())
    return 13 * n + 2 + 24 * n * (1 + width)


def minimum_time_for_product(G: int, tapes: int) -> int:
    """Smallest positive integer T with T*(b*(T+1)+1) >= G."""
    assert G >= 1 and tapes >= 1
    low, high = 1, max(2, G)
    while low < high:
        mid = (low + high) // 2
        if mid * (tapes * (mid + 1) + 1) >= G:
            high = mid
        else:
            low = mid + 1
    return low


def audit():
    counts = {'integer_minimality': 0, 'same_machine_domination': 0,
              'polynomial_witnesses': 0, 'length_grammar': 0,
              'full_grid_implication': 0}
    rows = []
    for n in list(range(1, 129)) + [256, 512, 1024, 2048]:
        L = source_length(n)
        assert L >= n
        counts['length_grammar'] += 1
        for tapes in [1, 2, 4, 8]:
            G = L * n  # normalized c=1 illustration only
            T = minimum_time_for_product(G, tapes)
            assert T * (tapes * (T + 1) + 1) >= G
            assert T == 1 or (T-1) * (tapes * T + 1) < G
            counts['integer_minimality'] += 2
            assert T <= L  # no superlinear time can be forced here
            counts['same_machine_domination'] += 1
            if n in [1, 2, 4, 16, 64, 128, 256, 512, 1024, 2048]:
                rows.append({'n': n, 'L_bits': L, 'work_tapes': tapes,
                             'product_target_G': G,
                             'min_time_given_only_T_S_tradeoff': T,
                             'full_sweep_time_lower_bound': L,
                             'minT_to_L_ratio': round(T/L, 8)})
    for L in [5, 8, 16, 32, 64]:
        for q in range(1, 9):
            for tapes in [1, 2, 4]:
                G = L ** q
                # A polynomially bounded abstract resource pair is feasible
                T = L ** ((q + 1)//2)
                S = tapes * (T + 1)
                assert T*(S+1) >= G
                counts['polynomial_witnesses'] += 1
    for G in range(1, 80):
        for tapes in [1, 2, 4]:
            t0 = minimum_time_for_product(G, tapes)
            for T in range(1, 35):
                for S in range(0, min(40, tapes*(T+1)+1)):
                    if T*(S+1)>=G:
                        assert T>=t0
                    counts['full_grid_implication'] += 1
    # Independent TMR-5 observation-only MAY graph optimality audit.
    # Shortest graph path is independently computed by Bellman relaxation, not by tau.
    for L in range(1, 6):
        for r in range(1, 4):
            for masks in combinations_with_replacement(range(1, 1 << L), r):
                def tau(U):
                    if U == 0:
                        return 0
                    return min(J.bit_count() for J in range(1 << L)
                               if all((U & (1 << i)) == 0 or (J & masks[i])
                                      for i in range(r)))
                potential = [tau(U) for U in range(1 << r)]
                for U in range(1 << r):
                    for j in range(L):
                        V = U
                        for i in range(r):
                            if masks[i] & (1 << j):
                                V &= ~(1 << i)
                        cost = int(V != U)
                        assert potential[U] <= cost + potential[V]
                        counts.setdefault('all_may_edge_inequalities', 0)
                        counts['all_may_edge_inequalities'] += 1
                # reverse shortest distance from empty using independent relaxation
                dist = [10**9] * (1 << r)
                dist[0] = 0
                changed = True
                while changed:
                    changed = False
                    for U in range(1 << r):
                        for j in range(L):
                            V = U
                            for i in range(r):
                                if masks[i] & (1 << j):
                                    V &= ~(1 << i)
                            d = int(V != U) + dist[V]
                            if d < dist[U]:
                                dist[U] = d
                                changed = True
                assert dist == potential
                counts.setdefault('may_graph_optimality_families', 0)
                counts['may_graph_optimality_families'] += 1
    summary = {
        'claim': 'TMR1-TS-BRIDGE-002',
        'date_pacific': '2026-11-13',
        'scope': 'Exact integer budget implications, not native TM execution or a SAT lower bound',
        'sample_sizes_n': 132,
        'work_tape_counts': [1,2,4,8],
        'counts': counts,
        'checks_total': sum(counts.values()),
        'failures': 0,
        'rows': rows,
        'peer_review': 'TMR5-O1: all potentials on the full MAY graph are bounded by its minimum read-path cost tau<=L',
        'theorem': ('On a fixed b-tape TM, S<=b(T+1). If T^alpha(S+1)^beta>=G(L) '
                    'with fixed alpha,beta>=0, alpha+beta>0, then '
                    'T >= (G(L)/(2b+1)^beta)^(1/(alpha+beta)) for T>=1.'),
        'scope_note': 'TMR3 sweep model also has T>=L independently; its product is not an unrestricted time lower bound.',
    }
    OUT.write_text(json.dumps(summary, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'checks':summary['checks_total'],'failures':summary['failures'],
                      'rows': [r for r in rows if r['n'] in [1,64,2048] and r['work_tapes']==2]},indent=2))

if __name__ == '__main__':
    audit()
