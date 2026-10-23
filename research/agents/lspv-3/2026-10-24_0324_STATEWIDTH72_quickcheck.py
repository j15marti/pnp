#!/usr/bin/env python3
"""Restricted reproducibility check for STATEWIDTH72; standard library only."""
import itertools
import json

def sat_of_codes(codes):
    # An exact-width-three clause forbids one Boolean triple.
    return len(set(codes)) < 8

def bp(codes):
    mask = 0
    for code in codes:
        for shift in (2, 1, 0):
            bit = (code >> shift) & 1
            if shift == 2:
                partial = bit
            elif shift == 1:
                partial = (partial << 1) | bit
            else:
                mask |= 1 << ((partial << 1) | bit)
    return mask != 255

def nae_ok(clauses, assignment):
    return all(len({assignment[v] ^ sign for v, sign in clause}) > 1
               for clause in clauses)

def token(clauses):
    incidence = {}
    for j, clause in enumerate(clauses):
        assert len(clause) >= 3
        assert len({v for v, _ in clause}) == len(clause)
        for v, _ in clause:
            incidence.setdefault(v, []).append(j)
    assert all(len(x) <= 2 for x in incidence.values())
    assignment = [0] * (max(incidence) + 1)
    bad = lambda j: len({assignment[v] ^ s for v, s in clauses[j]}) == 1
    flips = 0
    for start in range(len(clauses)):
        if not bad(start):
            continue
        at, incoming = start, -1
        visited = set()
        while True:
            assert at not in visited
            visited.add(at)
            variable = min(v for v, _ in clauses[at] if v != incoming)
            assignment[variable] ^= 1
            flips += 1
            assert not bad(at) and flips <= len(clauses) ** 2
            neighbor = next((j for j in incidence[variable] if j != at), None)
            if neighbor is None or not bad(neighbor):
                break
            at, incoming = neighbor, variable
    assert nae_ok(clauses, assignment)
    return flips

def run():
    checked_bp = 0
    for length in range(1, 6):
        for codes in itertools.product(range(8), repeat=length):
            assert bp(codes) == sat_of_codes(codes)
            checked_bp += 1
    unsat_permutations = 0
    for codes in itertools.permutations(range(8)):
        assert not bp(codes) and not sat_of_codes(codes)
        unsat_permutations += 1
    edges = list(itertools.combinations(range(4), 2))
    tested_signed = 0
    max_flips = 0
    for signs in itertools.product((0, 1), repeat=2 * len(edges)):
        clauses = [[] for _ in range(4)]
        for v, (u, w) in enumerate(edges):
            clauses[u].append((v, signs[2*v]))
            clauses[w].append((v, signs[2*v+1]))
        max_flips = max(max_flips, token(clauses))
        tested_signed += 1
    odd_cycle = [[(0, 0), (1, 0)], [(1, 0), (2, 0)], [(2, 0), (0, 0)]]
    assert not any(nae_ok(odd_cycle, a)
                   for a in itertools.product((0, 1), repeat=3))
    return {'status':'COMPUTATIONAL', 'bp_exhaustive':checked_bp,
            'bp_unsat_permutations':unsat_permutations,
            'K4_signed_signings':tested_signed, 'K4_max_flips':max_flips,
            'binary_cycle_unsat':True, 'failures':0}

if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, indent=2))
