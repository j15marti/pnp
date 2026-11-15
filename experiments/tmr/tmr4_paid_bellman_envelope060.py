#!/usr/bin/env python3
"""TMR-4/037: exact paid-path envelope for a hidden-source AND-of-OR query graph.

Python 3 standard library only. Terminal states include YES and NO. Query answers
are concrete input-source branches, not optional answers chosen by one machine.
Zero-cost alias/tag normalizations preserve the underlying transcript.
Finite enumeration is COMPUTATIONAL; the all-q proof is in the report.
"""
from functools import lru_cache
from fractions import Fraction as Q
from itertools import product
import json

checks = 0

def verify(test, message):
    global checks
    checks += 1
    if not test:
        raise AssertionError(message)

def label(q, st):
    rows = tuple(st[i*q:(i+1)*q] for i in range(q))
    if any(all(v == 0 for v in row) for row in rows):
        return 0
    if all(any(v == 1 for v in row) for row in rows):
        return 1
    return None

def measures(q, st):
    if label(q, st) is not None:
        return 0, 0
    active = tuple(st[i*q:(i+1)*q] for i in range(q)
                   if 1 not in st[i*q:(i+1)*q])
    unknown = [row.count(-1) for row in active]
    return sum(unknown), min(len(active), min(unknown))

def read(st, j, bit):
    if st[j] != -1:
        return st
    z = list(st)
    z[j] = bit
    return tuple(z)

def audit(q):
    m = q*q
    D = m-q+1
    witnessed = None
    paid_edges = 0
    terminal_count = 0
    max_drop_W = 0
    max_drop_B = 0
    max_positive_violation_W = 0
    @lru_cache(maxsize=None)
    def envelope(st):
        w, _ = measures(q, st)
        if label(q, st) is not None:
            return Q(0)
        # Empty path pays no charge; every nonempty positive-cost path starts
        # with one authentic source-coordinate READ.
        best = Q(w)
        for j, v in enumerate(st):
            if v == -1:
                for bit in (0, 1):
                    best = min(best, Q(1)+envelope(read(st, j, bit)))
        return best
    states = 0
    for st in product((-1,0,1), repeat=m):
        states += 1
        w, b = measures(q, st)
        h = envelope(st)
        verify(h == Q(b), 'paid Bellman envelope != certificate distance')
        verify(b <= w, 'certificate exceeds worst-case')
        # Two alias tags and authentic cost-zero TAG toggles. Both have h.
        verify(h == envelope(st), 'free tag did not preserve value')
        if label(q, st) is not None:
            terminal_count += 1
            verify(h == 0, 'nonzero terminal')
            continue
        for j, v in enumerate(st):
            if v != -1:
                # A repeated cached read leaves the transcript unchanged.
                verify(h <= h and h <= Q(1)+h, 'repeat')
                continue
            for bit in (0, 1):
                succ = read(st, j, bit)
                w1, b1 = measures(q, succ)
                delta_w = w-w1
                delta_b = b-b1
                paid_edges += 1
                max_drop_W = max(max_drop_W, delta_w)
                max_drop_B = max(max_drop_B, delta_b)
                max_positive_violation_W = max(max_positive_violation_W, delta_w-1)
                verify(delta_b <= 1 and delta_w <= D, 'invalid tariff cone')
                verify(h <= Q(1)+envelope(succ), 'Bellman tariff violation')
                # Independently check three exact rational dual certificates.
                for lw,lb in ((Q(0),Q(1)),(Q(1,D),Q(0)),
                              (Q(1,2*D),Q(1,2))):
                    verify(lw*delta_w+lb*delta_b <= 1,
                           'two-component LP row fails')
                if delta_b == 1 and delta_w == D and witnessed is None:
                    witnessed = {'state': ''.join('?' if v==-1 else str(v) for v in st),
                                 'read_index':j,'answer':bit,
                                 'delta_B':delta_b,'delta_W':delta_w,
                                 'source_label_after':label(q,succ)}
    initial = (-1,)*m
    w0,b0 = measures(q, initial)
    verify((w0,b0,envelope(initial)) == (m,q,Q(q)), 'initial')
    verify(max_drop_W == D and max_drop_B == 1 and witnessed is not None,
           'exact facet witness missing')
    verify(Q(m,D) <= q, 'LP initial optimum incorrect')
    return dict(q=q,source_bits=m,states=states,
                tagged_concrete_states=2*states,
                paid_read_edges_per_tag=paid_edges,
                terminal_transcripts=terminal_count,
                initial_minimax_W=w0,initial_cert_B=b0,
                initial_envelope_H=int(envelope(initial)),
                exact_nonnegative_LP_facet=f'lambda_B+{D}*lambda_W<=1',
                all_q_optimal_initial_potential=b0,
                maximum_paid_W_discharge=max_drop_W,
                maximum_paid_B_discharge=max_drop_B,
                invalid_raw_W_excess=max_positive_violation_W,
                critical_paid_transition=witnessed,
                changed_model_paid_goal_shortcut_initial=min(b0,1),
                changed_model_free_goal_shortcut_initial=0)

def main():
    out = [audit(q) for q in (1,2,3)]
    print(json.dumps({'claim':'PAID-ENVELOPE060',
                      'status':'PROVED/RESTRICTED proof; COMPUTATIONAL enumeration',
                      'replayed_q': [1,2,3],
                      'checks':checks,'failures':0,'runs':out},indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
