#!/usr/bin/env python3
"""TMR-5: finite independent verification of polynomial-output MCSP-NO repeat control.
No machine compiler, asymptotic proof, or SAT reduction is asserted by these tests.
"""
import json
from fractions import Fraction

checks = 0

def verify(ok, explanation):
    global checks
    checks += 1
    if not ok:
        raise AssertionError(explanation)


def at_most_two_gate_tables(h):
    """Exact fan-in-two AND/OR and one-input NOT gate DAGs with <=2 gates."""
    L = 1 << h
    universe = (1 << L) - 1
    variables = []
    for j in range(h):
        word = 0
        for i in range(L):
            word |= ((i >> j) & 1) << i
        variables.append(word)
    zero = set([0, universe, *variables])
    seen = set(zero)
    for first in zero:
        seen.add(universe ^ first)
        for second in zero:
            seen.add(first & second)
            seen.add(first | second)
    one_gate = set(seen)
    for g in one_gate:
        for p in zero:
            seen.add(g & p)
            seen.add(g | p)
        seen.add(universe ^ g)
    return seen


def derive_passes(source_length, q):
    """Full-sweep power-of-two halving; binary root extraction is a fixed-q operation.
    Simulates the sweep charges, not a compiled finite-state head machine.
    """
    active = [True] * source_length
    live = source_length
    halving_rounds = 0
    sweep_cells = 0
    while live > 1:
        parity = 0
        next_live = 0
        for j in range(source_length):
            sweep_cells += 1
            if active[j]:
                parity ^= 1
                if parity == 0:
                    active[j] = False
                else:
                    next_live += 1
        verify(next_live*2==live, 'halving invariant')
        live = next_live
        halving_rounds += 1
    verify(halving_rounds % q == 0, 'source length has wrong power for fixed q')
    return 1 << (halving_rounds//q), sweep_cells


def stream_repeat(x, passes):
    """One stored copy, one work-head full sweep per output pass.
    Flags record which sweep number is complete; all movement is counted.
    """
    L = len(x)
    flags = [False] * L
    out = []
    source_reads = L
    work_moves = L  # write x during the input stream
    output_writes = 0
    rounds = 0
    for _ in range(passes):
        first_unmarked = None
        for j in range(L):
            if first_unmarked is None and not flags[j]:
                first_unmarked = j
            out.append(x[j])
            output_writes += 1
            work_moves += 1
        verify(first_unmarked is not None, 'repeat counter exhausted prematurely')
        flags[first_unmarked] = True
        work_moves += L  # paid rewind, even after the last pass
        rounds += 1
    return ''.join(out), source_reads, work_moves, output_writes, rounds

rows = []
for q,m in [(1,2),(1,3),(1,4),(2,1),(2,2),(3,1)]:
    h = q*m
    L = 1 << h
    N = L * (1 << m)
    low = at_most_two_gate_tables(h)
    hard_mask = next((z for z in range(1 << L) if z not in low), None)
    verify(hard_mask is not None, 'no 2-gate hard table at tested size')
    x = ''.join(str((hard_mask >> j) & 1) for j in range(L))
    calculated_passes, length_charge = derive_passes(L,q)
    verify(calculated_passes==(1<<m), 'length-derived replication count')
    y, reads, moves, writes, rounds = stream_repeat(x, calculated_passes)
    verify(len(y)==N and y==x*(1<<m), 'streaming repetition mismatch')
    verify(all(y[u*L:(u+1)*L]==x for u in range(1<<m)), 'restriction mismatch')
    verify(rounds == (1<<m) and reads==L and writes==N, 'bad charge accounting')
    verify(moves <= 3*N, 'more than linear work-head movement')
    # For each indexed request, the fixed left-initialized evaluator reads x[0..(i mod L)].
    restarted = sum((i % L)+1 for i in range(N))
    verify(restarted == N*(L+1)//2, 'restart source traversal sum')
    verify(restarted > N, 'no restart separation')
    # Preserve two easy controls, to show the source-copy machine does not decide MCSP.
    for easy in ('0'*L, '1'*L):
        eout, *_ = stream_repeat(easy, 1<<m)
        verify(eout == easy*(1<<m), 'easy-copy control')
    rows.append({"q":q,"m":m,"source_bits_L":L,"table_bits_N":N,
                 "at_most_two_gate_count":len(low),"source_hard_gate_cap":2,
                 "first_hard_source":x,"source_reads":reads,"output_writes":writes,
                 "charged_work_moves_upper_proxy":moves,"length_halving_sweep_cells":length_charge,"separate_index_source_reads":restarted,
                 "restart_to_shared_total_work_ratio_lower":round(restarted/(moves+writes+reads+length_charge),5)})

# These are rational parameter checks, not witnesses for asymptotic counting.
windows = []
for mu in [Fraction(1,10),Fraction(1,3),Fraction(49,100),Fraction(51,100),Fraction(3,4),Fraction(9,10),Fraction(99,100)]:
    q = next(z for z in range(1,200) if Fraction(z,z+1)>mu)
    beta=Fraction(q,q+1)
    verify(beta>mu, 'threshold above source length exponent')
    verify(q==1 or Fraction(q-1,q)<=mu, 'q not minimal')
    windows.append({"mu":str(mu),"q":q,"beta":str(beta),"margin":str(beta-mu)})

print(json.dumps({"experiment":"TMR5/029 POLYREPEAT048",
 "status":"COMPUTATIONAL; asymptotic proof separate",
 "assertions":checks,"failed":0,"rows":rows,"windows":windows,
 "qualification":"Uniform source-to-table streaming transducer, NO classification existential by circuit counting; not a 3SAT reduction or MCSP decision algorithm"},indent=2))
