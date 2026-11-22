"""Exact finite checks of cycle coordinates and actual stopped-read records.

Run: python experiments/dynamic_accounting_cycle_stop_20261122.py
This tests the new ledger, not the inherited source parser or a native tape.
No randomness, external solver, or third-party library is used.
"""
from collections import Counter
from fractions import Fraction
from itertools import product
import hashlib
import json
from pathlib import Path


def forest(q, edges):
    parent = list(range(q))
    def root(u):
        while parent[u] != u:
            u = parent[u]
        return u
    tree, chords = [], []
    for i, (u, v) in enumerate(edges):
        a, b = root(u), root(v)
        if a == b:
            chords.append(i)
        else:
            parent[a] = b
            tree.append(i)
    return tree, chords


def potentials(q, edges, tree, bits):
    adj = [[] for _ in range(q)]
    for i in tree:
        u, v = edges[i]
        adj[u].append((v, bits[i]))
        adj[v].append((u, bits[i]))
    s = [None] * q
    for u in range(q):
        if s[u] is not None:
            continue
        s[u] = 0
        pending = [u]
        while pending:
            v = pending.pop()
            for w, z in adj[v]:
                if s[w] is None:
                    s[w] = s[v] ^ z
                    pending.append(w)
    return s


def coordinates(q, edges, tree, chords, bits):
    s = potentials(q, edges, tree, bits)
    return tuple(bits[i] for i in tree), tuple(
        bits[i] ^ s[edges[i][0]] ^ s[edges[i][1]] for i in chords)


def invert(q, edges, tree, chords, tree_bits, syndrome):
    bits = [0] * len(edges)
    for i, z in zip(tree, tree_bits):
        bits[i] = z
    s = potentials(q, edges, tree, bits)
    for i, z in zip(chords, syndrome):
        u, v = edges[i]
        bits[i] = z ^ s[u] ^ s[v]
    return tuple(bits)


def scan(syndrome):
    # E contains forward read events only; return movement is separately paid.
    record, events = [], []
    for address, bit in enumerate(syndrome, 1):
        events.append(address)
        record.append(bit)
        if bit:
            return tuple(record), tuple(events), "UNSAT"
    return tuple(record), tuple(events), "SAT"


def check(name, q, edges):
    tree, chords = forest(q, edges)
    r = len(chords)
    counts, records, coordinate_pairs = Counter(), Counter(), set()
    fibers = {}
    total_reads = 0
    for bits in product((0, 1), repeat=len(edges)):
        t, y = coordinates(q, edges, tree, chords, bits)
        assert invert(q, edges, tree, chords, t, y) == bits
        assert (t, y) not in coordinate_pairs
        coordinate_pairs.add((t, y))
        counts[y] += 1
        rec, events, verdict = scan(y)
        assert events == tuple(range(1, len(rec) + 1))
        assert len(set(events)) == len(events)
        assert verdict == ("UNSAT" if any(y) else "SAT")
        assert all(z == 0 for z in rec[:-1])
        assert not rec or rec[-1] == 1 or len(rec) == r
        records[rec] += 1
        fibers.setdefault(rec, set()).add(y)
        total_reads += len(events)
    cases = 2 ** len(edges)
    assert len(counts) == 2 ** r
    assert set(counts.values()) == {2 ** len(tree)}
    code = list(records)
    assert all(not (len(a) < len(b) and b[:len(a)] == a)
               for a in code for b in code)
    assert sum((Fraction(1, 2 ** len(a)) for a in code), Fraction()) == 1
    # Verify dyadic probability exactly, so -log2(p)=length without float logs.
    assert all(Fraction(n, cases) == Fraction(1, 2 ** len(a))
               for a, n in records.items())
    expected = Fraction(total_reads, cases)
    assert expected == 2 * (1 - Fraction(1, 2 ** r))
    assert all(len(ys) == 2 ** (r - len(rec))
               for rec, ys in fibers.items())
    conditional_entropy = sum(
        (Fraction(records[rec], cases) * (r - len(rec)) for rec in records),
        Fraction())
    assert conditional_entropy == r - expected
    if r:
        for y in [(0,) * r, (0,) * (r - 1) + (1,)]:
            assert len(scan(y)[1]) == r
    return {"name": name, "vertices": q, "edges": len(edges),
            "rank": r, "edge_signings": cases,
            "expected_reads_and_entropy_bits": str(expected),
            "full_syndrome_conditional_entropy_bits": str(conditional_entropy),
            "largest_observation_fiber": max(map(len, fibers.values())),
            "stopped_record_multiplicities": {
                ''.join(map(str, a)): records[a] for a in sorted(code)},
            "uniform_syndromes": len(counts), "kraft_sum": "1",
            "balanced_pair_reads": r if r else None}


def main():
    cases = []
    for r in range(1, 6):
        edges = []
        for i in range(r):
            a, b = 2 * i + 1, 2 * i + 2
            edges.extend([(0, a), (a, b), (0, b)])
        cases.append(check(f"friendship_{r}", 2 * r + 1, edges))
    cases.append(check("intersecting_cycles", 4,
                       [(0, 1), (1, 2), (2, 3), (0, 2), (0, 3)]))
    cases.append(check("disconnected_triangle_edge_isolate", 6,
                       [(0, 1), (1, 2), (0, 2), (3, 4)]))
    cases.append(check("forest_rank_zero", 4, [(0, 1), (1, 2)]))
    payload = {"status": "COMPUTATIONAL", "seed": None,
               "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "total_edge_signings": sum(c["edge_signings"] for c in cases),
               "checks": cases,
               "limitations": "No source-parser, native-tape, or kernel execution; no unrestricted complexity conclusion."}
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
