"""Deterministic raw-encoding, certificate, and finite one-tape checks. Python 3.10+."""
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
import hashlib
import json
import sys

# The two peer encoders are existing repository modules.
from dynamic_construction_join_palette_20261122 import encode, recover
from dynamic_construction_triangle_bundle_20261122 import expand


def raw_source(q, edges, word):
    identity, swap = (0, 1, 2), (1, 0, 2)
    matching = {}
    for j, (u, v) in enumerate(edges):
        a, b = q + 2*j, q + 2*j + 1
        tag = swap if word >> j & 1 else identity
        matching.update({(u, a): identity, (u, b): identity, (a, b): identity,
                         (v, a): tag, (v, b): tag})
    h, graph = expand(q + 2*len(edges), matching)
    n, rows = encode(h, graph)
    assert recover(n, rows) == (h, graph)
    m = len(rows)
    assert (n, m) == (33*q + 111*len(edges), 21*q + 87*len(edges))
    gamma = format(m + 1, "b")
    width = n.bit_length()
    data = "1"*n + "0" + "0"*(len(gamma)-1) + gamma
    data += "".join(format(v+1, f"0{width}b") for row in rows for v in row)
    return data


def enumerate_cycles(edges):
    cycles = []
    for mask in range(1, 1 << len(edges)):
        adjacency = defaultdict(set)
        for i, (u, v) in enumerate(edges):
            if mask >> i & 1:
                adjacency[u].add(v)
                adjacency[v].add(u)
        if any(len(ns) != 2 for ns in adjacency.values()):
            continue
        reached = set()
        todo = [next(iter(adjacency))]
        while todo:
            u = todo.pop()
            if u not in reached:
                reached.add(u)
                todo.extend(adjacency[u] - reached)
        if len(reached) == len(adjacency):
            cycles.append(mask)
    return cycles


def source_oracle(q, edges):
    # Enumerate vertex potentials, independently of the cycle criterion.
    return {sum((((pot >> u) ^ (pot >> v)) & 1) << i
                for i, (u, v) in enumerate(edges)) for pot in range(1 << q)}


def inspect_graph(q, edges):
    edges = sorted(edges)
    count = 1 << len(edges)
    yes = source_oracle(q, edges)
    cycles = enumerate_cycles(edges)
    nonbridges = 0
    for cycle in cycles:
        nonbridges |= cycle
    sources = [raw_source(q, edges, word) for word in range(count)]
    nbits = len(sources[0])
    base = int(sources[0], 2)
    supports = [int(sources[1 << j], 2) ^ base for j in range(len(edges))]
    assert all(supports) and all(a & b == 0 for a, b in combinations(supports, 2))
    for word, data in enumerate(sources):
        combined = base
        for j, delta in enumerate(supports):
            if word >> j & 1:
                combined ^= delta
        assert len(data) == nbits and int(data, 2) == combined
    # Compute sound partial records directly from their full completion sets.
    labels = [word in yes for word in range(count)]
    fibers = []
    for mask in range(count):
        table = defaultdict(set)
        for word, label in enumerate(labels):
            table[word & mask].add(label)
        fibers.append(table)
    histogram = Counter()
    for word, label in enumerate(labels):
        for prefix in range(count):
            exact = min((extra & ~prefix).bit_count() for extra in range(count)
                        if len(fibers[extra | prefix][word & (extra | prefix)]) == 1)
            odd = [cycle for cycle in cycles if (word & cycle).bit_count() % 2]
            predicted = ((nonbridges & ~prefix).bit_count() if label else
                         min((cycle & ~prefix).bit_count() for cycle in odd))
            assert exact == predicted
            histogram[exact] += 1
    return (dict(q=q, edges=edges, bits=nbits, signings=count, sat=len(yes),
                 unsat=count-len(yes), comparisons=count*count,
                 variable_bits_per_edge=[s.bit_count() for s in supports],
                 additional_certificate_histogram=dict(sorted(histogram.items()))),
            sources, supports, yes)


def finite_trace(data, choices, filters, sites, yes, record=None):
    """Simulate the compiled finite guard. Replay mode supplies only first signals."""
    length = len(choices[0])  # compiled public fixture size, independent of this input
    last_source_cell = len(data) - 1  # measurement only
    mask = (1 << len(choices)) - 1
    known_tags = {}
    events, prefix = [], None
    head = time = cm = 0
    answers = iter(record) if record is not None else None
    tape = list(data) + ["_"]
    # Fixed finite controls i, mask and RETURN label are compiled for just this fixture.
    def step(move, write=None):
        nonlocal head, time, cm
        if write is not None:
            tape[head] = write
        head += move
        time += 1
        cm += 2 + max(head, last_source_cell)  # 1 + interval length, input retained.
    for pos in range(length):
        assert head == pos
        if tape[head] == "_":
            step(0)  # premature end
            return "UNKNOWN", events, prefix, None
        site = sites.get(pos)
        if site is None:
            value = tape[head] if answers is None else choices[0][pos]
        else:
            j, base_bit = site
            if j not in known_tags:
                value = tape[head] if answers is None else next(answers)
                known_tags[j] = int(value) ^ base_bit
                events.append((time+1, pos, j, int(value)))
            else:
                value = tape[head] if answers is None else str(base_bit ^ known_tags[j])
        # Masks are a fixed transition-table abbreviation for this finite guard.
        mask &= filters[pos][int(value)]
        step(1)
        if events and prefix is None:
            stop = 1 if events[0][3] else 3
            if len(events) == stop:
                prefix = tuple(e[3] for e in events)
    assert head == length
    if tape[head] != "_" or not mask or mask & (mask-1):
        step(0)  # cost the end check, including excess input or an empty candidate set
        return "UNKNOWN", events, prefix, None
    outcome = (mask.bit_length()-1) in yes
    step(-1)  # read the blank and enter the return state carrying the verdict
    while head > 1:
        step(-1)
    step(0, "Y" if outcome else "N")  # common READY at 1
    ready = time
    cache = tape[head]
    step(-1)
    step(1, "1" if cache == "Y" else "0")
    step(0, "|")
    assert tape[:2] == (["1", "|"] if outcome else ["0", "|"])
    if answers is not None:
        assert list(answers) == []
    trace = dict(time=time, span_max=length+2, physical_cm=cm,
                 ready_time=ready, post_ready_steps=time-ready)
    return outcome, events, prefix, trace


def guard_suite(sources, supports, yes):
    nbits = len(sources[0])
    filters = [(0, 0)]*nbits
    sites = {}
    for j, bits in enumerate(supports):
        while bits:
            low = bits & -bits
            pos = nbits - low.bit_length()
            sites[pos] = (j, int(sources[0][pos]))
            bits -= low
    for pos in range(nbits):
        ones = sum(1 << w for w, src in enumerate(sources) if src[pos] == "1")
        filters[pos] = ((1 << len(sources))-1-ones, ones)
    groups = defaultdict(list)
    unread_fibers = defaultdict(set)
    sample = None
    all_costs = set()
    for word, data in enumerate(sources):
        label, events, prefix, trace = finite_trace(data, sources, filters, sites, yes)
        assert label == (word in yes)
        payload = [str(e[3]) for e in events]
        # Replay receives a public dummy source for geometry, the stream supplies all unknowns.
        replay = finite_trace(sources[0], sources, filters, sites, yes, payload)
        assert replay == (label, events, prefix, trace)
        assert len(events) == len(supports)
        all_costs.add(tuple(trace.items()))
        if not label:
            suffix = tuple(e[3] for e in events[len(prefix):])
            groups[prefix].append(suffix)
            # The outward scan retains every cell. At a selected posttransition
            # configuration read one original representative per still-unseen tag.
            for i in range(1, len(suffix)+1):
                future = events[len(prefix)+i:]
                tail = tuple(int(data[pos]) for _, pos, _, _ in future)
                assert all(pos > events[len(prefix)+i-1][1] for _, pos, _, _ in future)
                unread_fibers[(prefix, suffix[:i], len(future))].add(tail)
            if sample is None:
                sample = dict(word=word, actual_first_reads=events, costs=trace)
    stats = []
    for prefix, suffixes in sorted(groups.items()):
        r = len(supports) - len(prefix)
        assert len(suffixes) == len(set(suffixes)) == 2**max(0, r-1)
        assert all(len(t) == r for t in suffixes)
        stats.append(dict(prefix=prefix, residual_tags=r, odd_inputs=len(suffixes),
                          conditional_entropy_bits=max(0, r-1)))
    for (_, _, remaining), witnesses in unread_fibers.items():
        assert len(witnesses) == 2**max(0, remaining-1)
    # Corrupt a public bit and a repeated copy separately. Both must miss the guard.
    second_copy = sorted(pos for pos, (j, _) in sites.items() if j == 0)[1]
    for pos in (0, second_copy):
        corrupted = list(sources[0])
        corrupted[pos] = "0" if corrupted[pos] == "1" else "1"
        assert finite_trace("".join(corrupted), sources, filters, sites, yes)[0] == "UNKNOWN"
    for malformed in (sources[0][:-1], sources[0]+"0"):
        assert finite_trace(malformed, sources, filters, sites, yes)[0] == "UNKNOWN"
    assert len(all_costs) == 1
    return dict(valid_runs=len(sources), replayed=len(sources), rejected_off_image=4,
                postevent_configuration_fibers=len(unread_fibers),
                odd_prefix_fibers=stats, sample_unsat=sample)


def main():
    graphs = [
        (4, [(0,1),(1,2),(0,2),(2,3)]),
        (4, [(0,1),(0,2),(1,2),(0,3),(1,3)]),
        (4, list(combinations(range(4), 2))),
        (6, [(0,1),(0,2),(1,2),(3,4),(3,5),(4,5)]),
        (5, [(0,1),(1,2),(2,3),(3,4),(0,4)]),
    ]
    checks = []
    for q, edges in graphs:
        graph, sources, supports, yes = inspect_graph(q, edges)
        checks.append(graph)
    tape = guard_suite(sources, supports, yes)
    deps = {}
    for mod in ("dynamic_construction_join_palette_20261122", "dynamic_construction_triangle_bundle_20261122"):
        path = Path(sys.modules[mod].__file__)
        deps[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    print(json.dumps(dict(graphs=checks, same_run_fixture=tape,
                          certificate_comparisons=sum(g["comparisons"] for g in checks),
                          raw_images=sum(g["signings"] for g in checks),
                          dependencies_sha256=deps), indent=2))


if __name__ == "__main__":
    main()
