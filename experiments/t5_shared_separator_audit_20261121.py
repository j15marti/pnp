#!/usr/bin/env python3
"""Finite exhaustive audit for growing separator shared suffix BDD."""
import json
from itertools import product

def audit(k):
    nodes = 2*k+2  # terminals, plus s_i and x_i decisions
    sat = sum(all(s[i] or x[i] for i in range(k))
              for s in product((0,1), repeat=k)
              for x in product((0,1), repeat=k))
    assert sat == 3**k
    fibers = [sum(all(s[i] or x[i] for i in range(k))
                  for x in product((0,1), repeat=k))
              for s in product((0,1), repeat=k)]
    assert all(v == 2**sum(s)
               for s,v in zip(product((0,1),repeat=k), fibers))
    return dict(k=k, separator_assignments=2**k,
                distinct_fiber_counts=len(set(fibers)),
                shared_BDD_nodes=nodes, count=sat)

if __name__ == "__main__":
    print(json.dumps(dict(status="PASS",
                          cases=[audit(k) for k in range(1,8)],
                          scope="Finite Boolean checks only; strict-T5 lift symbolic"),
                     indent=2))
