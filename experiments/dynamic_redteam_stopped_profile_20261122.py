"""Independent stopped-profile audit. Python 3 standard library."""
from collections import Counter
from fractions import Fraction
from itertools import product
from math import log2, isclose
import json

def local_relation(right):
    rows = [(a, 3+b, 6+(a+b)%3) for a in range(3) for b in range(3)]
    return {(x[0], x[right]) for x in product((0,1), repeat=9)
            if all(sum(x[v] for v in row) == 1 for row in rows)}

def record(bits):
    count = 0
    for j, bit in enumerate(bits, 1):
        count += bit
        if count == 2:
            return bits[:j]
    return bits

def decode(code, q):
    if not code or len(code) > q:
        raise ValueError("length")
    count = 0
    profile = []
    for j, bit in enumerate(code):
        if bit not in (0,1) or count == 2:
            raise ValueError("after stop")
        count += bit
        profile.append(count)
    if count < 2 and len(code) != q:
        raise ValueError("incomplete")
    return tuple(profile + [2]*(q-len(code)))

def run():
    eq = local_relation(1)
    nand = local_relation(3)
    assert eq == {(0,0),(1,1)}
    assert nand == {(0,0),(0,1),(1,0)}
    data = []
    for q in range(1,13):
        frequencies = Counter()
        for bits in product((0,1), repeat=q):
            code = record(bits)
            profile = decode(code,q)
            assert profile == tuple(min(2,sum(bits[:j])) for j in range(1,q+1))
            possible = {1}
            for bit in bits:
                relation = nand if bit else eq
                possible = {b for a,b in relation if a in possible}
            assert (1 in possible) == (profile[-1] != 1)
            frequencies[code] += 1
        for code, frequency in frequencies.items():
            assert all(code[:j] not in frequencies for j in range(1,len(code)))
            assert Fraction(frequency, 2**q) == Fraction(1,2**len(code))
        mean = sum(Fraction(count*len(code),2**q) for code,count in frequencies.items())
        expected = 4-Fraction(q+2,2**(q-1))
        assert mean == expected
        entropy = -sum(count/2**q*log2(count/2**q) for count in frequencies.values())
        assert isclose(entropy,float(mean),abs_tol=1e-12)
        hard = [(0,)*q, (0,)*(q-1)+(1,)]
        assert all(len(record(x)) == q for x in hard)
        assert len({decode(record(x),q)[-1] != 1 for x in hard}) == 2
        data.append(dict(q=q, inputs=2**q, records=len(frequencies),
                         mean_reads=str(mean), entropy_bits=entropy,
                         worst_reads=q, balanced_pair_reads=q))
    return dict(status="PASS", local_assignments=1024,
                total_switch_inputs=sum(x["inputs"] for x in data), rows=data,
                scope="local semantics, exact stopped codes and logical read counts; no native tape")

if __name__ == "__main__":
    print(json.dumps(run(),indent=2))
