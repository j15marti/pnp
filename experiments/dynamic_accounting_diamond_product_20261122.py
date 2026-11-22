"""Enumerate local diamond extensions and normalized S3 product trace fibers."""
from collections import Counter
from itertools import permutations, product
import json

P = tuple(permutations(range(3)))
I = P[0]

def mul(f, g):
    return tuple(f[a] for a in g)

def inv(f):
    return tuple(f.index(a) for a in range(3))

def edge(f, g, p):
    return all(f[a] != g[p[a]] for a in range(3))

def encode_ring(word):
    from dynamic_construction_triangle_bundle_20261122 import expand
    from dynamic_construction_join_palette_20261122 import encode
    d = len(word)
    labels = {}
    for i,p in enumerate(word):
        right, a, b = (i+1)%d, d+2*i, d+2*i+1
        labels.update({(i,a):I,(i,b):I,(right,a):p,(right,b):p,(a,b):I})
    return encode(*expand(3*d,labels))

def scan(word):
    acc = I
    for p in word:
        acc = mul(acc,p)
    return acc

def main():
    from dynamic_construction_join_palette_20261122 import recover
    local = 0
    for left,right,a,b,p in product(P, repeat=5):
        feasible = (edge(left,a,I) and edge(left,b,I) and edge(right,a,p)
                    and edge(right,b,p) and edge(a,b,I))
        if feasible:
            assert right == mul(left,p)
            local += 1
    for left,p in product(P,repeat=2):
        right = mul(left,p)
        assert any(edge(left,a,I) and edge(left,b,I) and edge(right,a,p)
                   and edge(right,b,p) and edge(a,b,I) for a,b in product(P,repeat=2))
    rows = []
    for d in (3,4,5):
        counts = Counter()
        for word in product(P,repeat=d):
            final = scan(word)
            counts[final] += 1
            for j in range(d):
                repair = mul(inv(scan(word[:j])), inv(scan(word[j+1:])))
                assert scan(word[:j]+(repair,)+word[j+1:]) == I
                assert (word[j] == repair) == (final == I)
        assert set(counts.values()) == {6**(d-1)}
        rows.append(dict(d=d,SAT=counts[I],UNSAT=5*counts[I],
                         singleton_opponent_checks=d*6**d))
    s,t = (1,0,2),(0,2,1)
    last = inv(mul(s,t))
    assert scan((s,t,last)) == I and scan((t,s,last)) != I
    for word in ((s,t,last),(t,s,last)):
        n,triples = encode_ring(word)
        assert (n,len(triples)) == (144*len(word),108*len(word))
        assert recover(n,triples) is not None
    print(json.dumps(dict(local_assignments=6**5,local_extensions=local,
                          fiber_counts=rows,order_pair_same_length=True,
                          source_roundtrips=2),indent=2))

if __name__ == "__main__":
    main()
