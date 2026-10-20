#!/usr/bin/env python3
# Scope-restricted reproducible controls for the REDTEAM34 handoff.
import itertools
from collections import defaultdict

def sat_onevar(cnf):
    return any(all(any((lit > 0) == bool(z) for lit in clause)
                   for clause in cnf) for z in (0, 1))

checks = 0
for n in range(1, 11):
    output = set()
    for x in range(1 << n):
        bits = []
        for i in range(n):
            b = (x >> i) & 1
            query = ((1,),) if b else ((1,), (-1,))
            got = int(sat_onevar(query))
            assert got == b
            bits.append(got)
            checks += 1
        assert tuple(bits) not in output
        output.add(tuple(bits))
    assert len(output) == 1 << n
print("passed queries:", checks)
