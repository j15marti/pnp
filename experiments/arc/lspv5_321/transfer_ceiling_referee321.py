#!/usr/bin/env python3
"""Exact finite controls for TRANSFER-CEILING-REFEREE321.

No asymptotic lower bound is inferred from these checks.  They verify the
algebraic ceiling and standard both-label/malformed controls used in the report.
"""
from __future__ import annotations

import itertools
import json
import math
import resource
import time
from decimal import Decimal, getcontext, ROUND_CEILING
from pathlib import Path

RUN = "EXPONENTIAL-OVERHEAD-TRANSFER-CEILING-REFEREE321"
TASK = "6ad42a2a9a088191ab9042245f3b4393"


def sat_count(nvars, clauses):
    count = 0
    witness = None
    for bits in itertools.product((False, True), repeat=nvars):
        if all(any(bits[abs(l)-1] == (l > 0) for l in c) for c in clauses):
            count += 1
            witness = witness or [int(x) for x in bits]
    return count, witness


def php(h):
    # h+1 pigeons into h holes.
    v = lambda p, j: p*h + j + 1
    clauses = []
    for p in range(h+1):
        clauses.append([v(p, j) for j in range(h)])
    for j in range(h):
        for p in range(h+1):
            for q in range(p+1, h+1):
                clauses.append([-v(p, j), -v(q, j)])
    return h*(h+1), clauses


def tseitin_k4(charge):
    edges = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    idx = {e:i+1 for i,e in enumerate(edges)}
    clauses = []
    for vertex in range(4):
        inc = [idx[e] for e in edges if vertex in e]
        # Clause blocks each local assignment of the wrong parity.
        for bits in itertools.product((0,1), repeat=3):
            if (sum(bits) & 1) != charge[vertex]:
                clauses.append([(-x if bit else x) for x,bit in zip(inc,bits)])
    return 6, clauses


def parse_dimacs(text):
    header = None
    clauses = []
    pending = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith('c'):
            continue
        if line.startswith('p'):
            if header is not None:
                raise ValueError('duplicate header')
            parts = line.split()
            if len(parts) != 4 or parts[1] != 'cnf':
                raise ValueError('bad header')
            header = (int(parts[2]), int(parts[3]))
            if min(header) < 0:
                raise ValueError('negative header')
            continue
        if header is None:
            raise ValueError('missing header')
        for tok in line.split():
            lit = int(tok)
            if lit == 0:
                clauses.append(pending)
                pending = []
            else:
                if abs(lit) > header[0]:
                    raise ValueError('literal range')
                pending.append(lit)
    if header is None or pending or len(clauses) != header[1]:
        raise ValueError('incomplete or count mismatch')
    return header[0], clauses


def main():
    started = time.perf_counter()
    checks = 0

    # Pure algebra: exp_2(H) <= 64^d P with d <= q is compatible with
    # q=d=ceil(H/6).  Hence this inequality alone cannot exclude linear q(H).
    haken_rows = []
    for h in (8,16,32,64,128,256,512):
        m = (h+1) + h*((h+1)*h//2)
        q = (h+5)//6
        rhs_log2_lower = 6*q + math.log2(m+4*q+1)
        assert rhs_log2_lower >= h
        checks += 1
        haken_rows.append({
            'normalized_H_bits': h,
            'candidate_q_equals_d': q,
            'source_clauses': m,
            'rhs_log2_lower': rhs_log2_lower,
            'N_scale_proxy_h3_log2h': h**3*math.ceil(math.log2(h+2)),
        })

    # Braun threshold in base 2.  Choosing e=ceil(H_bits) satisfies the
    # exponential-overhead inequality with e polynomial in the input scale.
    getcontext().prec = 90
    ln2 = Decimal(2).ln()
    braun_rows = []
    for ell in (32,33,34,36,40):
        n = 1 << ell
        h_bits = Decimal(n)/(Decimal(32768)*(Decimal(ell)**2)*ln2)
        e = int(h_bits.to_integral_value(rounding=ROUND_CEILING))
        assert Decimal(e) >= h_bits
        checks += 1
        n_scale = n**3 * ell**2
        braun_rows.append({
            'ell': ell,
            'n': n,
            'H_bits_decimal': str(h_bits),
            'candidate_escape_e': e,
            'N_scale_proxy_n3_ell2': str(n_scale),
            'escape_le_N_proxy': e <= n_scale,
        })

    # Same-source both-label controls: standard PHP and one deleted-pigeon
    # source clause.  The latter has an explicit SAT witness.
    php_rows = []
    for h in (1,2,3):
        nv, f = php(h)
        u_count, _ = sat_count(nv, f)
        s_count, wit = sat_count(nv, f[1:])
        assert u_count == 0 and s_count > 0 and wit is not None
        checks += 2
        php_rows.append({'h':h,'vars':nv,'clauses':len(f),
                         'unsat_models':u_count,'deletion_sat_models':s_count,
                         'deletion_witness':wit})

    odd_n, odd = tseitin_k4([1,0,0,0])
    even_n, even = tseitin_k4([0,0,0,0])
    odd_count, _ = sat_count(odd_n, odd)
    even_count, even_wit = sat_count(even_n, even)
    assert (odd_count, even_count) == (0,8)
    checks += 2

    valid = "p cnf 2 2\n1 0\n-1 2 0\n"
    assert parse_dimacs(valid)[0] == 2
    checks += 1
    malformed = [
        "1 0\n",
        "p sat 1 1\n1 0\n",
        "p cnf 1 1\n2 0\n",
        "p cnf 1 2\n1 0\n",
        "p cnf 1 1\n1\n",
        "p cnf 1 1\np cnf 1 1\n1 0\n",
        "p cnf x 1\n1 0\n",
        "p cnf -1 0\n",
    ]
    rejected = 0
    for text in malformed:
        try:
            parse_dimacs(text)
        except (ValueError, TypeError):
            rejected += 1
    assert rejected == len(malformed)
    checks += rejected

    elapsed = time.perf_counter()-started
    payload = {
        'run': RUN,
        'task_id': TASK,
        'timestamp_pst': '2026-11-03 13:48',
        'status': {'transfer_ceiling':'PROVED/EXACT', 'finite_controls':'COMPUTATIONAL',
                   'full_R_lower_bound':'OPEN','B1':'OPEN','B2':'OPEN','B3':'OPEN','P_vs_NP':'OPEN'},
        'haken_normalized_rows': haken_rows,
        'braun_rows': braun_rows,
        'php_controls': php_rows,
        'tseitin_control': {'odd_models':odd_count,'even_models':even_count,
                            'even_witness':even_wit},
        'malformed_rejected': rejected,
        'assertion_groups': checks,
        'resource_ledger': {
            'wall_seconds': elapsed,
            'max_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            'proof_optimizer_work_charged_to_W': False,
            'offline_diagnostic': True,
        },
    }
    out = Path('transfer_ceiling_referee321.json')
    out.write_text(json.dumps(payload, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'output':str(out),'checks':checks,
                      'wall_seconds':elapsed,'max_rss_kib':payload['resource_ledger']['max_rss_kib']}))


if __name__ == '__main__':
    main()
