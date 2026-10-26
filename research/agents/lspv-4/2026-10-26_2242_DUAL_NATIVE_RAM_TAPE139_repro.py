#!/usr/bin/env python3
"""LSPV-4 DUAL-NATIVE-RAM-TAPE139: deterministic, dependency-free audit.

This is an exact finite/symbolic MODEL audit, NOT a SAT hardness experiment.
The toy left-gap-right equality language is only a geometric control for the
project's peer-reported exact-(2,2) SAT encoding. A full gadget audit is separate.
"""
import argparse
import json
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import product
from math import ceil, log2
from pathlib import Path

getcontext().prec = 45
RAW_TABLE = [
    ("0.001", "1.80083"), ("0.010", "1.79092"),
    ("0.100", "1.69618"), ("0.250", "1.55242"),
    ("0.500", "1.34070"), ("0.750", "1.15765"),
    ("0.900", "1.06011"), ("0.990", "1.00583"),
]

checks = 0
def check(value, explanation):
    global checks
    checks += 1
    if not value:
        raise AssertionError(explanation)


def tape_scan(a, b):
    """Abstract serial-head comparator on a + 0^(2m) + b."""
    assert len(a) == len(b)
    m = len(a)
    tape = a + (0,) * (2*m) + b
    h = 0
    motions = probes = 0
    for i in range(m):
        motions += abs(h - i)
        h = i
        probes += 1
        lv = tape[h]
        j = 3*m + i
        motions += abs(h - j)
        h = j
        probes += 1
        rv = tape[h]
        if lv != rv:
            return False, motions, probes
    return True, motions, probes


def tape_block(a, b, batch):
    """One sequential read-only input head and B remembered data bits."""
    assert len(a) == len(b)
    m = len(a)
    tape = a + (0,) * (2*m) + b
    h = 0
    motions = probes = 0
    max_live = 0
    for first in range(0, m, batch):
        last = min(m, first+batch)
        motions += abs(h-first)
        h = first
        saved = []
        for i in range(first, last):
            motions += abs(h-i)
            h = i
            saved.append(tape[h]); probes += 1
        max_live = max(max_live, len(saved))
        for i, value in zip(range(first, last), saved):
            j = 3*m+i
            motions += abs(h-j)
            h = j
            probes += 1
            if value != tape[j]:
                return False, motions, probes, max_live
    return True, motions, probes, max_live


def ram_indexed(a, b):
    """Indexed read-only input; 2m bit probes, no claim of unit BIT-time."""
    assert len(a) == len(b)
    m = len(a)
    n = 4*m
    index_bits = max(1, (n-1).bit_length())
    queries = 0
    for i in range(m):
        # Addresses i and 3m+i are generated, never stored as a length-m list.
        queries += 2
        if a[i] != b[i]:
            return False, queries, index_bits
    return True, queries, index_bits


def two_head(a, b):
    """Two independently placed input heads: initializing second head costs O(N)."""
    assert len(a) == len(b)
    m = len(a)
    startup = 3*m
    moves = startup + max(0,m-1)  # two heads can move synchronously
    for i in range(m):
        if a[i] != b[i]:
            return False, startup+i, 2*(i+1)
    return True, moves, 2*m


def test_equality():
    exhaustive = 0
    for m in range(1,6):
        words = list(product((0,1), repeat=m))
        for a in words:
            for b in words:
                expected = a == b
                x = tape_scan(a,b)
                check(x[0] == expected, 'serial bit error')
                for batch in (1, max(1,m//2), m):
                    y = tape_block(a,b,batch)
                    check(y[0] == expected and y[3] <= batch, 'block bit/space error')
                z = ram_indexed(a,b)
                check(z[0] == expected and z[1] <= 2*m, 'RAM bit error')
                w = two_head(a,b)
                check(w[0] == expected and w[2] <= 2*m, 'two-head error')
                exhaustive += 1
    table = []
    for m in (4,8,16,32,64,128,256):
        a = tuple((i*7+i//3)%2 for i in range(m))
        serial = tape_scan(a,a)
        ram = ram_indexed(a,a)
        heads = two_head(a,a)
        for batch in (1, max(1,round(m**.5)), m):
            block = tape_block(a,a,batch)
            check(block[0] and block[2] == 2*m and block[3] <= batch,'block diag')
            table.append({
                'm':m, 'N':4*m,'batch':batch,
                'one_head_serial_moves':serial[1],
                'sequential_block_moves':block[1],
                'work_buffer_bits':block[3],
                'two_input_head_moves':heads[1],
                'RAM_indexed_probes':ram[1],
                'RAM_address_bits':ram[2],
                'RAM_bit_time_bound':ram[1]*ram[2],
            })
        check(serial[0] and serial[2] == 2*m,'serial diag')
        check(ram[0] and ram[1] == 2*m,'RAM diag')
        check(heads[0] and heads[2] == 2*m,'two-head diag')
        check(serial[1] >= m*(m-1), 'quadratic serial control')
    return exhaustive, table


def test_native_and_transfer():
    table = []
    for s,c in RAW_TABLE:
        ds=Decimal(s); dc=Decimal(c)
        tape = Decimal(2)-ds
        gap=tape-dc
        check(gap>0, 'tape BW gap must be positive')
        table.append({'RAM_space_exponent':s,'BW_time_rounded':c,
                      'native_sequential_tape_exponent_floor':str(tape),
                      'tape_minus_BW':str(gap)})
    pairs=[('RAM_indexed_equality','1','0'),
           ('tape_excluded_RAM_unexcluded','1.4','0.5'),
           ('tape_border_RAM_unexcluded','1.5','0.5'),
           ('tape_excluded_RAM_unexcluded_2','1.8','0.1'),
           ('BW_strict_excluded','1.34069','0.5'),
           ('FLMV_strict_excluded','1.1','0.5'),
           ('large_s','1.05','1.4'), ('unknown_K','3','2')]
    rowmap=dict(RAW_TABLE)
    tested=[]
    for name,t,s in pairs:
        dt=Decimal(t);ds=Decimal(s)
        t1=dt+max(Decimal(1),ds)
        p1=max(Decimal(1),ds)
        tape_excl=(dt+ds<Decimal(2))
        BW=any(ds<=Decimal(s0) and dt<Decimal(c0) for s0,c0 in RAW_TABLE)
        check(t1>=2 if dt>=1 else True,'simulated stripe must be non-improving')
        tested.append({'name':name,'t':t,'s':s,'M1_simulated_time_ceiling':str(t1),
                       'M1_simulated_footprint_exponent':str(p1),
                       'tape_product_inequality_violation_if_NATIVE':tape_excl,
                       'excluded_by_a_listed_BW_rectangular_point':BW,
                       'exclusion_from_M1_simulation_alone':t1<2})
    c=Fraction(241,200)
    beta=((c+2)/(c*c)-c)/2
    check(beta==Fraction(11642479,23232400),'FLMV rational mismatch')
    exact={'FLMV_c':str(c),'FLMV_beta':str(beta),
           'margin_t_for_1_1':str(c-Fraction(11,10)),
           'margin_s_for_1_2':str(beta-Fraction(1,2)),
           'Williams_product_phi':'(1+sqrt(5))/2',
           'strict_example_note':'Use margins >0, not rounded equality or o(1) endpoint.'}
    return table,tested,exact


def test_dictionary_counterexample():
    controls=[]
    for depth in (3,4,5,8,10,12,16,18):
        nodes=(1<<depth)-1
        # Breadth-first heap order: rightmost search visits 0,2,6,...,nodes-1.
        indices=[(1<<(j+1))-2 for j in range(depth)]
        comparisons=len(indices)
        physical_moves=sum(abs(x-y) for x,y in zip(indices,indices[1:]))
        check(indices[0]==0 and indices[-1]==nodes-1,'BFS index')
        check(physical_moves==nodes-1,'sequential-head linear distance')
        check(comparisons==depth,'AVL logical comparison count')
        controls.append({'depth':depth,'balanced_nodes':nodes,
                         'logical_comparisons':comparisons,
                         'physical_head_moves_on_BFS_layout':physical_moves,
                         'motion_to_comparison_ratio':round(physical_moves/comparisons,5)})
    return controls


def build():
    e,eq=test_equality()
    bw,trans,exact=test_native_and_transfer()
    dictctrl=test_dictionary_counterexample()
    return {'run':'DUAL-NATIVE-RAM-TAPE139','date_utc':'2026-10-26',
      'status':'PROVED/EXACT scoped plus COMPUTATIONAL; no unrestricted SAT lower bound',
      'primary_sources_checked':[
          'FLMV Corollary 5.8 original PDF p18',
          'Williams 2006 original PDF p10 native indexed-input model',
          'Williams 2013 original PDF p18 Theorem 4.11 and Table I',
          'Buss-Williams ECCC TR11-031 original PDF pp50-51 Figure 2/3',
          'Hennie-Stearns 1966 abstract (two-tape not one-tape)',
          'Santhanam 2001 DOI/abstract only; exact theorem PDF NOT verified'
      ],
      'model_differences':'M1 physical N-input counted; Mk 1 serial read-only input head; RAT input/work indexed with written O(log T) address; log-word RAM only conditionally equivalent to RAT',
      'Buss_Williams_rounded_native_RAT_table':bw,
      'transfer_examples':trans,
      'FLMV_exact':exact,
      'connected_pointer_BFS_counterexample':dictctrl,
      'toy_left_gap_right_equality_not_a_SAT_gadget_audit':{
         'exhaustive_binary_word_pairs':e, 'measurements':eq},
      'finite_assertions':checks,
      'limitations':['Toy strings are only layout/geometry controls, not a checked Q/J signed-(2,2) CNF compiler',
        'The exact22 project SAT gadget proof is reused as a peer-reported conditional mapping',
        'No native input-tape TS lower bound is newly proved for unrestricted SAT',
        'Buss-Williams rounded table entries are independently source-checked, not all proof-search steps rerun',
        'A deliberately nonlocal balanced BST layout does not lower-bound every sequential dictionary implementation',
        'The M1 simulator includes fixed k and compressed excursions beyond end of input']}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,default=Path('2026-10-26_2242_DUAL_NATIVE_RAM_TAPE139_raw.json'))
    args=ap.parse_args()
    obj=build()
    args.output.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(json.dumps({'checks':obj['finite_assertions'],
     'pairs':obj['toy_left_gap_right_equality_not_a_SAT_gadget_audit']['exhaustive_binary_word_pairs'],
     'table_rows':len(obj['Buss_Williams_rounded_native_RAT_table']),
     'sim_rows':len(obj['transfer_examples']),
     'dictionary_controls':len(obj['connected_pointer_BFS_counterexample']),
     'result_path':str(args.output)},sort_keys=True))

if __name__ == '__main__':
    main()