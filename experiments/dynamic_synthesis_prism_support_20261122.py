"""Prism occurrence-to-compiled-support audit. Run from experiments with Python 3."""
from itertools import product
import json
from dynamic_construction_prism_matching_20261122 import family

def rows(q, bits):
    width = 9*q+6
    return [tuple(name+j*width for name in row)
            for j, bit in enumerate(bits) for row in family(q, bit)[1]]

def main():
    records = []
    comparisons = 0
    for q in range(3, 9):
        for k in range(1, 5):
            v, m = k*(9*q+6), k*(6*q+4)
            t, r = 5*v+6*m, 3*m
            d, c = 8*t, 26*t+4*r
            g = max(3, 2*((c+1)//2)+1)
            n0 = d+(10*c+1)*g+2
            m0 = (20*c+4)*g
            n, M = n0+m0+3, 2*m0+4
            W = n.bit_length()
            H = n+2+2*((M+1).bit_length()-1)
            N = H+3*M*(W+1)+2*n+W
            base = rows(q, (0,)*k)
            changes = []
            used = set()
            for j in range(k):
                other = rows(q, tuple(int(i == j) for i in range(k)))
                delta = {(a, slot): (x, y)
                         for a, (left, right) in enumerate(zip(base, other))
                         for slot, (x, y) in enumerate(zip(left, right)) if x != y}
                assert delta and used.isdisjoint(delta)
                used.update(delta)
                changes.append(delta)
            for bits in product((0, 1), repeat=k):
                current = rows(q, bits)
                for j in range(k):
                    alternate = rows(q, tuple(bit ^ (i == j) for i, bit in enumerate(bits)))
                    observed = {(a, slot): (x, y)
                                for a, (left, right) in enumerate(zip(current, alternate))
                                for slot, (x, y) in enumerate(zip(left, right)) if x != y}
                    expected = {key: pair[::-1] if bits[j] else pair
                                for key, pair in changes[j].items()}
                    assert observed == expected
                    comparisons += 1
            regions = []
            for delta in changes:
                count = 0
                for (a, slot), (x, y) in delta.items():
                    old, new = 15*x+6, 15*y+6
                    count += 32*g*(old ^ new).bit_count()
                    row_index = 3*a+slot
                    for clause in range(26*t+4*row_index, 26*t+4*row_index+4):
                        for instruction in (0, 2, 6, 8):
                            for vertex, branch in ((0, 0), (g-1, 1)):
                                s = 4*g+2*g*(10*clause+instruction)+2*vertex+branch
                                start = H+3*(5+2*s)*(W+1)+(W+1)+1
                                assert H <= start and start+W <= H+3*M*(W+1)
                regions.append(dict(occurrences=len(delta), predicted_changed_bits=count))
            records.append(dict(q=q,k=k,N=N,regions=regions))
    print(json.dumps(dict(comparisons=comparisons,records=records,
         scope="source occurrence differences and symbolic support counts/endpoints; no full compiled images",
         seed=None),indent=2))
if __name__ == "__main__":
    main()
