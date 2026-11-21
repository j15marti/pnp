"""Authenticate source-free canonical images and test the paired-record suffix."""
from hashlib import sha256
from pathlib import Path
from itertools import product
import json

import t5_construction_disjoint_cut_20261121 as construction


def positions(k):
    base = construction.image(k, 0, 0)[0]
    offsets = []
    for side, i in product(range(2), range(k)):
        a, b = ((1 << i, 0) if side == 0 else (0, 1 << i))
        variant = construction.image(k, a, b)[0]
        offsets.append(next(j for j, pair in enumerate(zip(base, variant)) if pair[0] != pair[1]))
    assert len(set(offsets)) == 2*k
    return base, offsets


def recover(bits, base, offsets):
    k = len(offsets)//2
    if len(bits) != len(base):
        return None
    masks = []
    for side in range(2):
        mask = 0
        for i in range(k):
            j = offsets[side*k+i]
            mask |= int(bits[j] != base[j]) << i
        masks.append(mask)
    if construction.image(k, *masks)[0] != bits:
        return None
    return masks


def authenticate(bits):
    n = bits.find("0")
    if n < 1991 or (n-515) % 1476:
        return None
    k = (n-515)//1476
    m = 629+1808*k
    expected = n+2+2*((m+1).bit_length()-1)+3*m*n.bit_length()
    if len(bits) != expected:
        return None
    return recover(bits, *positions(k))


class Tape:
    """Count cell moves only. Finite product tracks all share this head."""
    def __init__(self, pairs):
        self.pos = self.moves = self.peak = 0
        self.data = {i: p for i, p in enumerate(pairs)}
        self.data[len(pairs)] = "end"
        self.reg = {}
        self.out = {}
        self.mark = {}

    def step(self, d):
        assert d in (-1, 1) and self.pos+d >= 0
        self.pos += d
        self.moves += 1
        self.peak = max(self.peak, self.pos)

    def home(self):
        while self.pos:
            self.step(-1)

    def rewind(self):
        while self.pos not in self.mark:
            self.step(-1)

    def add(self, delta):
        # Little-endian digits with a blank high end. Carry is bounded by 283.
        carry = delta
        while carry:
            carry, bit = divmod(self.reg.get(self.pos, 0)+carry, 2)
            self.reg[self.pos] = bit
            self.step(1)
        self.rewind()

    def right(self):
        # Move register and start marker right by one cell, crossing local digits.
        old = None
        while self.pos in self.reg:
            old, self.reg[self.pos] = self.reg[self.pos], old
            if self.reg[self.pos] is None:
                del self.reg[self.pos]
            self.step(1)
        if old is not None:
            self.reg[self.pos] = old
        self.rewind()
        del self.mark[self.pos]
        self.step(1)
        self.mark[self.pos] = True

    def decrement(self):
        # Called only after a local nonzero test.
        while self.reg[self.pos] == 0:
            self.reg[self.pos] = 1
            self.step(1)
        self.reg[self.pos] = 0
        self.rewind()

    def nonzero(self):
        positive = False
        while self.pos in self.reg:
            positive |= bool(self.reg[self.pos])
            self.step(1)
        self.rewind()
        return positive


def suffix(pairs):
    tape = Tape(pairs)
    tape.mark[0] = True
    tape.add(98)
    conflict = False
    while tape.data[tape.pos] != "end":
        a,b = tape.data[tape.pos]
        conflict |= bool(a and b)
        tape.add(282 + (1-b))
        tape.right()
    if conflict:
        tape.home()
        tape.out[0] = "0"
        tape.step(1)
    else:
        # Move the register back to the origin. Read/write current cells only.
        while tape.pos:
            del tape.mark[tape.pos]
            tape.step(-1)
            tape.mark[tape.pos] = True
            tape.step(1)
            while tape.pos in tape.reg:
                bit = tape.reg.pop(tape.pos)
                tape.step(-1)
                tape.reg[tape.pos] = bit
                tape.step(1)
                tape.step(1)
            tape.rewind()
        for digit in "1010":
            tape.out[tape.pos] = digit
            tape.right()
        while tape.nonzero():
            tape.out[tape.pos] = "0"
            tape.decrement()
            tape.right()
    tape.out[tape.pos] = "#"
    word = "".join(tape.out[i] for i in range(len(tape.out)))
    return word, tape.peak, tape.moves


def main():
    rows = []
    for k in (1,2,3):
        base, offsets = positions(k)
        bad = list(base)
        bad[-1] = str(1-int(bad[-1]))
        assert recover("".join(bad),base,offsets) is None
        width = (515+1476*k).bit_length()
        # Swap two valid distinct names within the last symmetric C-clause.
        permuted = base[:-2*width] + base[-width:] + base[-2*width:-width]
        assert authenticate(permuted) is None
        assert authenticate(base) == [0,0]
        for a,b in product(range(1<<k),repeat=2):
            bits, cuts, *_ = construction.image(k,a,b)
            masks = recover(bits,base,offsets)
            assert masks == [a,b]
            pairs = [tuple(m>>i & 1 for m in masks) for i in range(k)]
            word,peak,moves = suffix(pairs)
            value = 0 if a & b else 10 << (98+282*k+k-b.bit_count())
            assert word == format(value,"b")+"#" and peak < cuts[0]
            rows.append(dict(k=k,a=a,b=b,peak=peak,moves=moves,cut=cuts[0],
                             output_length=len(word),output_sha256=sha256(word.encode()).hexdigest()))
    print(json.dumps(dict(cases=rows,modified_encodings_declined=6,
                          generator_sha256=sha256(Path(construction.__file__).read_bytes()).hexdigest()),
                     indent=2))


if __name__ == "__main__":
    main()
