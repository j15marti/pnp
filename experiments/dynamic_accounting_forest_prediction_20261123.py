"""Forest prediction versus exact source verification. Python 3.10+, no randomness.

The finite scan is a compiled fixture, not a uniform tape implementation.
Run from repository root; stdout is the immutable raw JSON evidence.
"""
from collections import defaultdict
from itertools import combinations
from pathlib import Path
import hashlib
import json
import sys
from dynamic_accounting_signed_cycle_20261123 import raw_source, source_oracle
from dynamic_construction_join_palette_20261122 import recover


def prepare(q):
    edges = list(combinations(range(q), 2))
    k = len(edges)
    tree = {i for i, (u, v) in enumerate(edges) if u == 0}
    n, m = 33*q+111*k, 21*q+87*k
    width = n.bit_length()
    header = n+2+2*((m+1).bit_length()-1)
    base = raw_source(q, edges, 0)
    owners = {}
    for e in range(k):
        other = raw_source(q, edges, 1 << e)
        for pos, (a, b) in enumerate(zip(base, other)):
            if a != b:
                assert pos >= header
                row = (pos-header)//(3*width)
                assert row not in owners or owners[row] == e
                owners[row] = e
    order = sorted(range(m), key=lambda row:
                   (0 if row not in owners else 1 if owners[row] in tree else 2, row))
    fixed_rows = sum(row not in owners for row in range(m))
    first_chord_row = next(i for i, row in enumerate(order)
                           if row in owners and owners[row] not in tree)
    stop = header+3*width*first_chord_row
    assert fixed_rows >= 4*3*(q+2*k)

    def encode(word):
        original = raw_source(q, edges, word)
        rows = [original[header+3*width*i:header+3*width*(i+1)] for i in range(m)]
        reordered = [rows[i] for i in order]
        numeric = [tuple(int(row[j*width:(j+1)*width], 2)-1 for j in range(3))
                   for row in reordered]
        assert recover(n, numeric) is not None
        assert sorted(reordered) == sorted(rows)
        return original[:header]+''.join(reordered)

    zero = encode(0)
    sites = {}
    for e in range(k):
        variant = encode(1 << e)
        positions = [i for i, (a, b) in enumerate(zip(zero, variant)) if a != b]
        assert positions
        for pos in positions:
            assert pos not in sites
            sites[pos] = (e, int(zero[pos]))
        assert all((pos < stop) == (e in tree) for pos in positions)
    assert min(sites) >= len(zero)/4
    return edges, tree, encode, zero, sites, stop, (n, m, width, header)


def scan(data, zero, sites, stop, yes, record=None):
    """A fixed-size finite-control scan, exact image guard and terminated output.

    Known-label dictionaries abbreviate finite control for this fixed q.
    Each input access and unit head movement is charged. Retained input is charged.
    """
    nbits = len(zero)
    known, events = {}, []
    head = steps = cm = 0
    tape = list(data)+['_']
    incoming = iter(record) if record is not None else None
    snapshot = None

    def step(move, write=None):
        nonlocal head, steps, cm
        if write is not None:
            tape[head] = write
        head += move
        steps += 1
        cm += 2+max(nbits-1, head)

    for pos in range(nbits):
        assert head == pos
        if pos == stop:
            snapshot = dict(known)
        if tape[pos] not in '01':
            step(0)
            return 'UNKNOWN', events, snapshot, None
        if pos in sites:
            e, polarity = sites[pos]
            if e not in known:
                value = tape[pos] if incoming is None else next(incoming)
                known[e] = int(value)^polarity
                events.append((steps+1, pos, e, int(value)))
            else:
                value = tape[pos] if incoming is None else str(known[e]^polarity)
            if int(value) != known[e]^polarity:
                step(0)
                return 'UNKNOWN', events, snapshot, None
        else:
            value = tape[pos] if incoming is None else zero[pos]
            if value != zero[pos]:
                step(0)
                return 'UNKNOWN', events, snapshot, None
        step(1)
    if tape[head] != '_':
        step(0)
        return 'UNKNOWN', events, snapshot, None
    word = sum(bit << e for e, bit in known.items())
    answer = word in yes
    step(-1)
    while head > 1:
        step(-1)
    step(0, 'Y' if answer else 'N')
    ready = steps
    cache = tape[head]
    step(-1)
    step(1, '1' if cache == 'Y' else '0')
    step(0, '|')
    assert tape[:2] == [str(int(answer)), '|']
    if incoming is not None:
        assert list(incoming) == []
    return answer, events, snapshot, dict(transitions=steps, physical_cm=cm,
                  peak_span=nbits+2, post_ready_transitions=steps-ready)


def main():
    results = []
    for q in (3, 4, 5):
        edges, tree, encode, zero, sites, stop, dims = prepare(q)
        k, r = len(edges), len(edges)-len(tree)
        yes = source_oracle(q, edges)
        chords = set(range(k))-tree
        words = (set(range(1 << k)) if q < 5 else
                 yes | {word^(1 << e) for word in yes for e in chords})
        fibers = defaultdict(set)
        balanced_fibers = defaultdict(set)
        sample = None
        all_traces = []
        for word in sorted(words):
            data = encode(word)
            expected = ''.join(str(int(ch) ^ ((word >> sites[pos][0]) & 1))
                               if pos in sites else ch for pos, ch in enumerate(zero))
            assert data == expected
            run = scan(data, zero, sites, stop, yes)
            label, events, snapshot, cost = run
            assert label == (word in yes)
            assert set(snapshot) == tree
            assert len(events) == k
            payload = [str(e[3]) for e in events]
            assert scan(zero, zero, sites, stop, yes, payload) == run
            suffix = [e for e in events if e[1] >= stop]
            assert {e[2] for e in suffix} == chords
            assert len(suffix) == r
            key = tuple(sorted(snapshot.items()))
            remaining = tuple((word >> e) & 1 for e in sorted(chords))
            fibers[key].add(remaining)
            if label:
                balanced_fibers[key].add(remaining)
                for e in chords:
                    neighbor = word^(1 << e)
                    assert neighbor not in yes
                    assert encode(neighbor)[:stop] == data[:stop]
                if sample is None:
                    sample = dict(word=word, first_chord_reads=suffix, costs=cost)
            all_traces.append(cost)
        assert len(balanced_fibers) == 2**(q-1)
        assert {len(f) for f in balanced_fibers.values()} == {1}
        if q < 5:
            assert {len(f) for f in fibers.values()} == {2**r}
        # A full-sign cache has no fresh source acquisition left; output still costs three.
        assert all(t['post_ready_transitions'] == 3 for t in all_traces)
        # Malformed public bit, inconsistent copy, truncation, and trailing input.
        repeat = sorted(pos for pos, (e, _) in sites.items() if e == 0)[1]
        broken = []
        for pos in (0, repeat):
            changed = list(zero)
            changed[pos] = str(1-int(changed[pos]))
            broken.append(''.join(changed))
        broken += [zero[:-1], zero+'0']
        assert all(scan(x, zero, sites, stop, yes)[0] == 'UNKNOWN' for x in broken)
        results.append(dict(q=q, k=k, n=dims[0], m=dims[1], N=len(zero),
             checkpoint=stop, valid_tape_traces=len(words), replays=len(words),
             balanced_traces=len(yes), residual_obligatory_events=r,
             balanced_conditional_entropy=0, legal_one_edge_neighbors=len(yes)*r,
             balanced_fibers=len(balanced_fibers), malformed_rejected=4,
             tested_all_signings=(q < 5), sample=sample))
    dependencies = {}
    for name in ('dynamic_accounting_signed_cycle_20261123',
                 'dynamic_construction_join_palette_20261122',
                 'dynamic_construction_triangle_bundle_20261122'):
        path = Path(sys.modules[name].__file__)
        dependencies[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    print(json.dumps(dict(cases=results, dependencies_sha256=dependencies), indent=2))


if __name__ == '__main__':
    main()
