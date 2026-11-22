#!/usr/bin/env python3
"""Exact three-variable minimal-cover enumeration and read-once resolution probe."""
from itertools import product, permutations
from collections import Counter
from pathlib import Path
import json, time, hashlib

N = 3
CLAUSES = [tuple(s) for s in product((-1, 0, 1), repeat=N)]
CLAUSES.sort(key=lambda c: (sum(x != 0 for x in c), c))
EMPTY = CLAUSES.index((0, 0, 0))
assert EMPTY == 0
NONEMPTY = CLAUSES[1:]
INDEX = {c: i for i, c in enumerate(CLAUSES)}
ASSIGNMENTS = list(product((0, 1), repeat=N))
FULL = (1 << len(ASSIGNMENTS)) - 1
BLOCK = []
for c in NONEMPTY:
    mask = 0
    for a, values in enumerate(ASSIGNMENTS):
        if not any(s and (values[v] == (1 if s > 0 else 0)) for v, s in enumerate(c)):
            mask |= 1 << a
    BLOCK.append(mask)

def minimal_masks(candidates):
    accepted = set()
    for mask in sorted(candidates, key=lambda x: (x.bit_count(), x)):
        sub = (mask - 1) & mask
        redundant = False
        while sub:
            if sub in accepted:
                redundant = True
                break
            sub = (sub - 1) & mask
        if not redundant:
            accepted.add(mask)
    return accepted

def covers():
    family = {0}
    stages = []
    for a in range(8):
        witness = [i for i, b in enumerate(BLOCK) if b & (1 << a)]
        output = set()
        for core in family:
            if any(core & (1 << i) for i in witness):
                output.add(core)
            else:
                for i in witness:
                    output.add(core | (1 << i))
        family = minimal_masks(output)
        stages.append({"points": a + 1, "candidates": len(output), "minimal": len(family)})
    return family, stages

TRANSFORMS = []
for perm in permutations(range(N)):
    for flip in product((-1, 1), repeat=N):
        trans = []
        for c in NONEMPTY:
            d = tuple(c[perm[i]] * flip[i] for i in range(N))
            trans.append(INDEX[d] - 1)
        TRANSFORMS.append(trans)

def transform_mask(mask, t):
    out = 0
    while mask:
        b = mask & -mask
        out |= 1 << t[b.bit_length() - 1]
        mask ^= b
    return out

def canonical(mask):
    return min(transform_mask(mask, t) for t in TRANSFORMS)

RESOLVENTS = [[0] * len(CLAUSES) for _ in CLAUSES]
for i, c in enumerate(CLAUSES):
    for j, d in enumerate(CLAUSES):
        result = 0
        for pivot in range(N):
            if c[pivot] == 0 or c[pivot] != -d[pivot]:
                continue
            e = []
            for v in range(N):
                if v == pivot:
                    e.append(0)
                elif c[v] and d[v] and c[v] != d[v]:
                    break
                else:
                    e.append(c[v] or d[v])
            else:
                result |= 1 << INDEX[tuple(e)]
        RESOLVENTS[i][j] = result

def bits(mask):
    while mask:
        b = mask & -mask
        yield b.bit_length() - 1
        mask ^= b

def read_once_proof(core):
    source = [i + 1 for i in bits(core)]
    count = len(source)
    derived = [0] * (1 << count)
    reasons = {}
    for p, c in enumerate(source):
        derived[1 << p] = 1 << c
        reasons[(1 << p, c)] = None
    for mask in range(1, 1 << count):
        if not mask & (mask - 1):
            continue
        anchor = mask & -mask
        part = (mask - 1) & mask
        results = 0
        while part:
            other = mask ^ part
            if other and part & anchor:
                for a in bits(derived[part]):
                    for b in bits(derived[other]):
                        new = RESOLVENTS[a][b]
                        for c in bits(new & ~results):
                            reasons[(mask, c)] = (part, a, other, b)
                        results |= new
            part = (part - 1) & mask
        derived[mask] = results
    root = (1 << count) - 1
    return bool(derived[root] & 1), source, derived[root]

def verify_core(core):
    ids = list(bits(core))
    union = 0
    for i in ids:
        union |= BLOCK[i]
    assert union == FULL
    private = {}
    for i in ids:
        others = 0
        for j in ids:
            if j != i:
                others |= BLOCK[j]
        p = BLOCK[i] & ~others & FULL
        assert p
        private[i] = list(bits(p))
    return private

def main():
    start = time.monotonic()
    family, stages = covers()
    for core in family:
        verify_core(core)
    orbit_sizes = Counter(canonical(core) for core in family)
    results = []
    for core, orbit_size in sorted(orbit_sizes.items(), key=lambda p: (p[0].bit_count(), p[0])):
        ok, source, final = read_once_proof(core)
        results.append({
            "mask": core, "size": core.bit_count(), "orbit_size": orbit_size,
            "clauses": [CLAUSES[i] for i in source],
            "read_once_refutable": ok,
            "private_assignments": verify_core(core),
        })
    out = {
        "scope": "All inclusion-minimal covers of the Boolean three-cube by the 26 nonempty-clause blocking subcubes; the empty-clause singleton is recorded separately.",
        "variables": N, "atom_count": len(NONEMPTY), "empty_clause_singleton": 1,
        "minimal_core_count": len(family),
        "size_histogram": dict(sorted(Counter(c.bit_count() for c in family).items())),
        "orbit_count": len(orbit_sizes),
        "read_once_failure_orbits": sum(not x["read_once_refutable"] for x in results),
        "stages": stages, "orbits": results,
        "seconds": time.monotonic() - start,
        "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
