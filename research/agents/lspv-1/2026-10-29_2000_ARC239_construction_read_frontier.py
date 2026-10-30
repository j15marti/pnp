#!/usr/bin/env python3
"""ARC239: exact construction-read/storage/continuation frontier controls.

Uses only Python's standard library. Reproducibility: deterministic, no external
network or SAT solver. Input sources are explicit b-bit unary-constraint signs.

This program checks a new three-coordinate theorem for fixed offline read sets,
plus the (weaker) all-adaptive offline-preparation read bound. Computational
checks do not prove the mathematical theorems.
"""
from __future__ import annotations
import functools
import itertools
import json
from collections import Counter
from math import comb, log2
from pathlib import Path

OUT = Path(__file__).with_name('2026-10-29_2000_ARC239_raw.json')


def parity(x: int) -> int:
    return x.bit_count() & 1


def volume(p: int, q: int) -> int:
    return 0 if q < 0 else sum(comb(p, k) for k in range(min(q, p) + 1))


def linear_constructor(p: int):
    """Build Hamming-radius-1 code C=ker H of length p.

    First r syndrome columns are unit vectors. Every nonzero r-bit syndrome
    occurs among all p columns. Kernel basis is systematic on positions r..p-1.
    No source-specific advice is used; H depends only on p.
    """
    if p == 0:
        return {'r': 0, 'cols': [], 'gens': [], 'lookup': {0: None}}
    r = (p + 1).bit_length() - 1
    assert 2 ** r - 1 <= p
    cols = [1 << i for i in range(r)]
    cols += [v for v in range(1, 1 << r) if (v & (v - 1)) != 0]
    cols += [1] * (p - len(cols))
    assert len(cols) == p
    assert set(cols) == set(range(1, 1 << r))
    gens = []
    for j in range(r, p):
        word = 1 << j
        for i in range(r):
            if (cols[j] >> i) & 1:
                word |= 1 << i
        syncheck = 0
        for k in range(p):
            if (word >> k) & 1:
                syncheck ^= cols[k]
        assert syncheck == 0
        gens.append(word)
    lookup = {col: j for j, col in enumerate(cols)}
    lookup[0] = None
    assert len(gens) == p-r
    return {'r': r, 'cols': cols, 'gens': gens, 'lookup': lookup}


def syndrome(cols, mask: int) -> int:
    out = 0
    while mask:
        low = mask & -mask
        j = low.bit_length() - 1
        out ^= cols[j]
        mask ^= low
    return out


def check_constructed(b: int, p: int, sample_sources=None):
    """Source has b bits, R=first p, U=rest; Q=(b-p)+1.

    Source access counted separately from summary arithmetic. Entire b bit
    source is not given to the online procedure except by indexed probes.
    """
    assert 0 <= p <= b
    data = linear_constructor(p)
    r, cols, gens, lookup = (data[k] for k in ('r', 'cols', 'gens', 'lookup'))
    L = p - r
    U = b - p
    Q = U + int(p > 0)
    if sample_sources is None:
        sample_sources = range(1 << b)
    comparisons = 0
    max_probes = 0
    source_reads = 0
    class RawSource:
        # Online decoder has no direct access to the source vector. Its only
        # source-dependent interface is this counted, named-coordinate probe.
        def __init__(self, secret):
            self.__secret = secret
            self.calls = 0
        def read(self, i):
            assert 0 <= i < b
            self.calls += 1
            return (self.__secret >> i) & 1

    for a in sample_sources:
        preproc_source = RawSource(a)
        aR = sum(preproc_source.read(i) << i for i in range(p))
        assert preproc_source.calls == p
        # Preprocessing reads exactly p source coordinates and stores L XORs.
        s = sum(parity(g & aR) << j for j, g in enumerate(gens))
        source_reads += preproc_source.calls
        for w in range(1 << b):
            online_source = RawSource(a)
            wR = w & ((1 << p)-1)
            wU = w >> p
            syn = syndrome(cols, wR)
            e = lookup[syn]
            c = wR ^ (0 if e is None else (1 << e))
            assert syndrome(cols, c) == 0
            # C is systematic on nonpivot positions: kernel coefficient for g_j
            # is precisely c's bit at the jth nonpivot coordinate.
            combination = parity(s & (c >> r))
            source_probe = online_source.read(e) if e is not None else 0
            rest_probe = 0
            for j in range(U):
                if (wU >> j) & 1:
                    rest_probe ^= online_source.read(p+j)
            ans = combination ^ source_probe ^ rest_probe
            assert ans == parity(a & w), (b, p, a, w)
            num_probes = wU.bit_count() + (e is not None)
            assert num_probes == online_source.calls <= Q
            max_probes = max(max_probes, num_probes)
            comparisons += 1
    # Source probing P >= b-Q and P/L/Q fixed-read theorem is fulfilled.
    assert p+Q >= b
    q = Q-U
    assert (1 << L) * volume(p, q) >= (1 << p)
    assert L == p - ((p+1).bit_length()-1)
    return {'b': b, 'offline_source_reads': p, 'storage_bits': L,
            'online_worst_source_probes': Q, 'actual_max_source_probes': max_probes,
            'source_query_pairs_checked': comparisons, 'offline_reads_across_sources': source_reads,
            'fourier_fixed_read_volume': volume(p, q),
            'fourier_fixed_read_lower_L': p-(volume(p, q).bit_length()-1),
            'stored_bits_equal_lower_bound': L == p-(volume(p, q).bit_length()-1)}


def mindepth_for_fiber(fiber, mask, b):
    """Exact optimal adaptive coordinate decision-tree depth for a finite fiber."""
    @functools.lru_cache(None)
    def dp(S):
        if not S or all(parity(mask & a) == parity(mask & S[0]) for a in S):
            return 0
        best = b+1
        for i in range(b):
            S0 = tuple(a for a in S if not ((a >> i) & 1))
            S1 = tuple(a for a in S if ((a >> i) & 1))
            if not S0 or not S1:
                continue
            best = min(best, 1 + max(dp(S0), dp(S1)))
        return best
    return dp(tuple(sorted(fiber)))


def exact_preprocessor_search(b: int, p: int, L: int):
    """All nonlinear L-bit summary maps on a fixed p-position read set."""
    assert p<=b and L<=1 and p<=3 and b<=4
    num_inputs = 1 << p
    num_outputs = 1 << L
    dist = Counter()
    worst_min = b + 1
    maps = 0
    for choices in itertools.product(range(num_outputs), repeat=num_inputs):
        fibers = [[] for _ in range(num_outputs)]
        for a in range(1 << b):
            fibers[choices[a & (num_inputs - 1)]].append(a)
        Q = 0
        for fiber in fibers:
            if not fiber: continue
            for w in range(1 << b):
                Q = max(Q, mindepth_for_fiber(fiber, w, b))
        assert p+Q >= b
        assert (1 << L) * volume(p, Q-(b-p)) >= (1 << p)
        dist[Q] += 1
        worst_min = min(worst_min,Q)
        maps += 1
    return {'b': b, 'p': p, 'L': L, 'maps_exhaustively_tested': maps,
            'minimum_query_probes_over_maps': worst_min,
            'query_probe_distribution': dict(sorted(dist.items()))}


def adaptive_preprocessor_control():
    """An offline read set that changes with source a, never given for free."""
    b=3
    def encoder(a):
        first = a & 1
        second_i = 1 if first==0 else 2
        second = (a >> second_i)&1
        return first ^ second
    fibers = {s: [a for a in range(1<<b) if encoder(a)==s] for s in (0,1)}
    Q = max(mindepth_for_fiber(f, w, b)
            for f in fibers.values() for w in range(1<<b))
    assert 2 + Q >= b
    return {'b': b, 'offline_adaptive_depth': 2, 'summary_bits': 1,
            'online_exact_worst_case_minimum_Q': Q,
            'preprocessing_transcripts': 'first bit a0; then a1 if a0=0 else a2; retain their XOR',
            'source_fibers': {str(s):fibers[s] for s in fibers}}


def contextual_values():
    # target t=u^v; each certified individual u or v leaves both target values,
    # but both together establish target. Duplicating u has no added value.
    sources=[(u,v) for u in (0,1) for v in (0,1)]
    def phi(facts):
        return (len({u^v for u,v in sources if all((u,v)[j]==val for j,val in facts.items())})-1)
    empty, after_u, after_v, both = (phi(x) for x in ({},{0:0},{1:0},{0:0,1:0}))
    assert (empty,after_u,after_v,both)==(1,1,1,0)
    def h2(p):
        return 0.0 if p in (0,1) else -p*log2(p)-(1-p)*log2(1-p)
    # Eight equally likely worlds. Z is 1 in one world. A certified event
    # selecting that world plus one Z=0 world raises *realized* target entropy.
    H_before=h2(1/8)
    H_after=h2(1/2)
    assert H_after>H_before
    return {'phi_empty':empty,'phi_after_u0':after_u,'phi_after_v0':after_v,
            'realized_entropy_value_negative':round(H_before-H_after,9),
            'entropy_prior':round(H_before,9), 'entropy_after_certified_event':H_after,
            'phi_after_both':both,'initial_values':{'u0':0,'v0':0},
            'conditional_value_of_v_after_u':1,'duplicate_u_value':0,
            'storage_penalty_example':{'mu':1,'irrelevant_fact_target_gain':0,
                                       'memory_charge_bits':1,'net_potential_decrease':-1}}


def main():
    exhaustive=[]
    for b in range(1,9):
        for p in range(b+1):
            exhaustive.append(check_constructed(b,p))
    # Full nonlinear fixed-read-preprocessor enumeration at small sizes.
    nonlinear=[exact_preprocessor_search(3,2,1), exact_preprocessor_search(4,3,1)]
    results={'status':'COMPUTATIONAL controls for PROVED/EXACT restricted lemmas',
             'source_model':'b independent unary sign bits; fixed offline raw read set except adaptive hostile control',
             'seed':'none; all enumerations deterministic',
             'fixed_read_Hamming_constructor_cases':len(exhaustive),
             'exhaustive_source_query_pairs':sum(row['source_query_pairs_checked'] for row in exhaustive),
             'exhaustive_constructor_by_b':[{'b':b, 'cases':b+1,
                       'comparisons':sum(x['source_query_pairs_checked'] for x in exhaustive if x['b']==b)}
                       for b in range(1,9)],
             'strong_example':check_constructed(15,11,range(0,1<<15,997)),
             'nonlinear_preprocessors':nonlinear,
             'adaptive_offline_control':adaptive_preprocessor_control(),
             'contextual_synergy_and_redundancy':contextual_values(),
             'frontier_table':exhaustive,
             'limitations': ['Only source-coordinate probes Q, not random-access total runtime or tape head movement',
                'Nonlinear arbitrary-adaptive offline preparation has only the unconditional p+Q>=b bound',
                'Stronger L frontier requires a predeclared fixed set of p offline read coordinates',
                'No ordinary general-SAT or strict exact-(2,2) reduction']}
    OUT.write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in results.items() if k in
                      ('status','fixed_read_Hamming_constructor_cases','exhaustive_source_query_pairs',
                       'nonlinear_preprocessors','adaptive_offline_control','strong_example')},indent=2))

if __name__ == '__main__':
    main()
