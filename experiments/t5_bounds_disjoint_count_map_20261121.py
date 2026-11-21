"""Exact AND/OR/NOT encoded-input circuit audit on the canonical DISJ promise."""
from itertools import product
from pathlib import Path
from hashlib import sha256
import json
import t5_construction_disjoint_cut_20261121 as family


class Circuit:
    def __init__(self, length):
        self.length = length
        self.gates = []
        self.zero = self.add("zero")
        self.one = self.add("one")

    def add(self, op, *args):
        self.gates.append((op, *args))
        return self.length + len(self.gates) - 1

    def invert(self, x):
        return self.add("not", x)

    def xor(self, x, y):
        return self.add("and", self.add("or",x,y), self.invert(self.add("and",x,y)))

    def evaluate(self, bits):
        values = list(map(int, bits))
        for op, *args in self.gates:
            if op == "zero": v = 0
            elif op == "one": v = 1
            elif op == "not": v = 1-values[args[0]]
            elif op == "and": v = values[args[0]] & values[args[1]]
            else: v = values[args[0]] | values[args[1]]
            values.append(v)
        return values


def build(k):
    base = family.image(k,0,0)[0]
    circ = Circuit(len(base))
    coordinates = []
    for side, i in product(range(2),range(k)):
        a,b = (1<<i,0) if side == 0 else (0,1<<i)
        variant = family.image(k,a,b)[0]
        j = next(j for j,(x,y) in enumerate(zip(base,variant)) if x != y)
        coordinates.append(circ.invert(j) if base[j] == "1" else j)
    left,right = coordinates[:k],coordinates[k:]
    conflict = circ.zero
    for a,b in zip(left,right):
        conflict = circ.add("or",conflict,circ.add("and",a,b))
    good = circ.invert(conflict)
    width = k.bit_length()
    count = [circ.zero]*width
    for bit in right:
        carry = circ.invert(bit)
        updated = []
        for old in count:
            updated.append(circ.xor(old,carry))
            carry = circ.add("and",old,carry)
        count = updated
    negative = [circ.invert(bit) for bit in count]
    decoder = [circ.one]
    for digit in range(width-1,-1,-1):
        decoder = [circ.add("and",prefix,choice) for prefix in decoder
                   for choice in (negative[digit],count[digit])]
    # 3N output bits cover all five-color counts at this encoded length.
    output = [circ.zero]*(3*len(base))
    E = 98+282*k
    for shift in range(k+3):
        choices = [decoder[j] for j in (shift,shift-2) if 0 <= j <= k]
        term = choices[0]
        if len(choices) == 2:
            term = circ.add("or",*choices)
        output[E+1+shift] = circ.add("and",good,term)
    bound = 5*k*width+width+11*k+16
    assert len(circ.gates) <= bound
    return circ,output,good,bound


def main():
    rows = []
    for k in (1,2,3,4):
        circuit,output,decision,bound = build(k)
        seen = set()
        for a,b in product(range(1<<k),repeat=2):
            encoded = family.image(k,a,b)[0]
            values = circuit.evaluate(encoded)
            result = sum(values[node]<<i for i,node in enumerate(output))
            expected = 0 if a&b else 10 << (98+282*k+k-b.bit_count())
            assert result == expected
            assert values[decision] == int(a&b == 0)
            seen.add(result)
        rows.append(dict(k=k,N=circuit.length,gates=len(circuit.gates),bound=bound,
                         cases=4**k,output_width=len(output),range_size=len(seen)))
    print(json.dumps(dict(results=rows,source_sha256=sha256(Path(family.__file__).read_bytes()).hexdigest(),
                         basis="AND/OR/NOT with two charged constant nodes",
                         circuit_code_sha256=sha256(Path(__file__).read_bytes()).hexdigest()),indent=2))


if __name__ == "__main__":
    main()
