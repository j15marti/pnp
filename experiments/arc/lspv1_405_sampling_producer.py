#!/usr/bin/env python3
"""LSPV-1/405: audit dyadic worst-case sampling and ultra-sparse gaps.
Finite tests are diagnostics, not a theorem about R_mix341 or P versus NP.
"""
from __future__ import annotations
import bisect, hashlib, json
from pathlib import Path


def model_count(clauses, n):
    if any(not clause or any(l == 0 or abs(l) > n for l in clause) for clause in clauses):
        raise ValueError('malformed canonical clause')
    return sum(all(any(((a >> (abs(l) - 1)) & 1) == (l > 0) for l in c)
                   for c in clauses) for a in range(1 << n))


def check():
    tests = 0
    dyadic = [1 << j for j in range(17)]
    for n in range(1, dyadic[-1]+1):
        j = bisect.bisect_left(dyadic, n)
        next_m = dyadic[j]
        assert n <= next_m < 2*n if n > 1 else next_m == 1
        tests += 1
        for k in (0, 1, 2, 3, 5):
            assert (next_m + 1)**k <= (2*n + 1)**k
            tests += 1
    # Fast-growing sample sequence m_(j+1)=2**m_j.  Only logarithms of
    # enormous staircase values are materialized, not 2**65536.
    m = [2, 4, 16, 65536]
    for j in range(len(m)-1):
        assert m[j+1] == 2**m[j]
        tests += 1
    ratios = []
    for j in range(1, 4):
        # f(m_j+1)=m_(j+1)=2**m_j and f(m_j)=m_j.
        # We record exact log2 f; no imaginary machine executes f.
        log2f = m[j]
        next_log = m[j]
        assert next_log > 3 * (m[j].bit_length()) if j >= 2 else True
        tests += 1
        ratios.append({'j':j, 'sample_n':m[j], 'query_n':m[j]+1,
                       'log2_staircase_value':log2f,
                       'log2_query_upper':(m[j]+1).bit_length()})
    labels = {'unsat_units':model_count([[1],[-1]], 1),
              'sat_clause':model_count([[1,2]], 2),
              'even_parity':model_count([[1,2],[-1,-2]], 2)}
    assert labels == {'unsat_units':0,'sat_clause':3,'even_parity':2}
    tests += 3
    malformed = 0
    for clauses,n in [([[0]],1), ([[]],1), ([[3]],2)]:
        try: model_count(clauses,n)
        except ValueError: malformed += 1
    assert malformed == 3
    tests += 3
    return {'schema':'LSPV1_SPARSE_REFLECTION_SAMPLING405/v1',
            'status':'COMPUTATIONAL finite arithmetic and CNF label controls only',
            'theorem':'sample-gap characterization proved symbolically in report',
            'dyadic_cutoffs':len(dyadic), 'dyadic_N_checked':dyadic[-1],
            'assertions':tests, 'sparse_ratios':ratios,
            'labels':labels, 'malformed_rejected':malformed,
            'no_B3_proof':True, 'no_R_mix341_lower_bound':True}


if __name__ == '__main__':
    out = check()
    p = Path('lspv1_405_sparse_raw.json')
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(f"PASS checks={out['assertions']} sha256={hashlib.sha256(p.read_bytes()).hexdigest()}")
