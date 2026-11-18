#!/usr/bin/env python3
"""Independent TMR-5/077 exact five-symbol cyclic-polymorphism obstruction.

Finite execution only corroborates a symbolic proof, not an asymptotic experiment.
Canonical template R(a,b) iff (b-a) modulo 5 is one of 1,3.
No external packages, random choices, or user-supplied advice.
"""
import hashlib
import itertools
import json
import sys
from pathlib import Path

REVISION = "tmr5-t5-cyclic-obstruction077.v1"

def R(a, b):
    return (b-a) % 5 in (1, 3)

def certificate(k):
    assert k >= 3
    j = (2*k) % 5
    assert 0 <= j <= k
    increments = [3]*j + [1]*(k-j)
    assert (sum(increments) % 5) == 0
    x = [0]
    for delta in increments[:-1]:
        x.append((x[-1]+delta) % 5)
    y = x[1:] + x[:1]
    assert len(x) == k and len(y) == k
    assert all(R(a,b) for a,b in zip(x,y))
    return j, x, y

def enumerate_binary():
    arcs = [(a,b) for a in range(5) for b in range(5) if R(a,b)]
    assert len(arcs) == 10
    good = []
    for c in itertools.product(range(5), repeat=5):
        f = lambda a,b: (a+c[(b-a)%5]) % 5
        if all(R(f(a,x), f(b,y)) for a,b in arcs for x,y in arcs):
            good.append(c)
    expected = []
    for t in range(5):
        expected.extend([tuple([t]*5), tuple((t+d)%5 for d in range(5))])
    assert set(good) == set(expected)
    assert len(good) == 10
    for c in good:
        f = lambda a,b: (a+c[(b-a)%5]) % 5
        assert any(f(a,b)!=f(b,a) for a in range(5) for b in range(5))
    return len(arcs), len(good)

def main():
    assert R(0,1) and R(0,3) and not R(0,0)
    listed = [(x,y) for x in range(5) for y in range(5) if R(x,y)]
    assert len(listed) == 10
    assert all((a,b) not in listed for b,a in listed)
    assert all((a,b) in listed or (b,a) in listed for a in range(5) for b in range(a+1,5))
    arcs, binary = enumerate_binary()
    k_min, k_max = 3, 1000
    examples = {}
    checked_arcs = 0
    for k in range(k_min,k_max+1):
        j,x,y = certificate(k)
        checked_arcs += k
        if k in (3,4,5,6,7,8,9,10,11,13,17,101,997,1000):
            examples[str(k)] = dict(j=j, cycle=x if k<=17 else x[:10], edges_complete=k)
    out = dict(revision=REVISION,python=sys.version.split()[0],
               template_edges=listed, binary_product_arcs=arcs,
               binary_polymorphism_profiles=binary,
               binary_commutative_profiles=0,
               k_min=k_min,k_max=k_max,cyclic_witnesses_checked=k_max-k_min+1,
               product_edges_checked=checked_arcs,
               no_binary_closed_walk=True,all_pass=True,examples=examples,
               source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    text=json.dumps(out,sort_keys=True,indent=2)+"\n"
    Path(__file__).with_name("TMR5_077_T5_CYCLIC_RAW.json").write_text(text,encoding="utf-8")
    print(json.dumps({k:v for k,v in out.items() if k not in ('examples','template_edges')},sort_keys=True))

if __name__ == '__main__':
    main()
