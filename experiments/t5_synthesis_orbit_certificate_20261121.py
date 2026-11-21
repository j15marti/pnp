"""Verify exact clause-multiset orbit certificates, including negative answers."""
from collections import Counter
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import random
import t5_construction_disjoint_cut_20261121 as f
import t5_construction_positive_offset1_20261121 as c


def verify(bits, a, b, permutation, proposed):
    try:
        n, clauses = c.decode(bits)
        k, rem = divmod(n-515,1476)
        if rem or k < 1 or sorted(permutation) != list(range(n)):
            return False
        source = f.image(k,a,b)[0]
        source_n, source_clauses = c.decode(source)
        if source_n != n:
            return False
        expected = Counter(tuple(sorted(permutation[v] for v in t)) for t in source_clauses)
        observed = Counter(tuple(sorted(t)) for t in clauses)
        count = 0 if a&b else 10 << (98+282*k+k-b.bit_count())
        return expected == observed and proposed == count
    except (AssertionError, ValueError, IndexError):
        return False


def main():
    rng = random.Random(83)
    rows = []
    for k in (1,2):
        for a,b in product(range(1<<k),repeat=2):
            source = f.image(k,a,b)[0]
            n, clauses = c.decode(source)
            mapping = list(range(n))
            rng.shuffle(mapping)
            clauses = [[mapping[x] for x in t] for t in clauses]
            for t in clauses:
                rng.shuffle(t)
            rng.shuffle(clauses)
            bits = c.encode(n,clauses)
            value = 0 if a&b else 10 << (98+282*k+k-b.bit_count())
            assert verify(bits,a,b,mapping,value)
            assert not verify(bits,a,b,mapping,value+1)
            bad_map = mapping.copy()
            bad_map[0] = bad_map[1]
            assert not verify(bits,a,b,bad_map,value)
            # Reverse row/slot changes remain semantically valid and still certified.
            reverse = c.encode(n,[t[::-1] for t in clauses[::-1]])
            assert verify(reverse,a,b,mapping,value)
            # Replace one occurrence by a distinct name, changing degree multiset.
            bad = [list(t) for t in clauses]
            replacement = next(v for v in range(n) if v not in bad[0])
            bad[0][0] = replacement
            assert not verify(c.encode(n,bad),a,b,mapping,value)
            rows.append(dict(k=k,a=a,b=b,N=len(bits),status="UNSAT" if value==0 else "SAT",
                             certificate_bits=2*k+n*n.bit_length(),
                             encoding_sha256=sha256(bits.encode()).hexdigest()))
    print(json.dumps(dict(seed=83,rows=rows,accepted_presentations=2*len(rows),
                          rejected_certificates=3*len(rows),
                          dependency_sha256=sha256(Path(f.__file__).read_bytes()).hexdigest()),indent=2))


if __name__ == "__main__":
    main()
