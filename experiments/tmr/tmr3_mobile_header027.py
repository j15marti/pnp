#!/usr/bin/env python3
"""Independent finite-state proxy for TMR3 mobile-counter one-work-tape composition.

This models a single physical tape containing ordinary guest cells plus one
mobile t-bit register adjacent to a marked guest head. All block rewrites are
charged at O(t+1) per guest transition. It does not execute a compiled TM.
"""
import itertools
import json
import hashlib
from pathlib import Path
from time import perf_counter


def gamma_encode(v):
    assert v >= 1
    b = format(v, 'b')
    return '0' * (len(b) - 1) + b


def gamma_decode(bits):
    z = 0
    while z < len(bits) and bits[z] == '0':
        z += 1
    assert z < len(bits)
    width = 2*z + 1
    assert width <= len(bits)
    return int(bits[z:width], 2), width


def padded_truth(x, t):
    return ''.join(ch * (1 << t) for ch in x)


class MobileTape:
    """Actual symbolic one-tape representation: guest cells and mobile register."""
    def __init__(self, k):
        self.k = k
        self.cells = ['H:_'] + ['R:0'] * k
        self.position = 0  # physical location of marked head
        self.ops = 0        # conservative upper bound for local head sweeps/writes
        self.peak = len(self.cells)

    def _check(self):
        assert self.cells.count('H:_') + self.cells.count('H:0') + self.cells.count('H:1') == 1
        assert self.cells[self.position].startswith('H:')
        assert self.cells[self.position+1:self.position+1+self.k].count('R:0') + self.cells[self.position+1:self.position+1+self.k].count('R:1') == self.k

    def decoded(self):
        self._check()
        guest = [p[2:] if p.startswith('H:') else p for p in self.cells if not p.startswith('R:')]
        idx = sum(1 for p in self.cells[:self.position] if not p.startswith('R:'))
        return idx, tuple(guest)

    def register(self):
        return ''.join(self.cells[self.position+i+1][-1] for i in range(self.k))

    def set_register(self, value):
        assert 0 <= value < (1 << self.k)
        bits = format(value, '0{}b'.format(self.k)) if self.k else ''
        for i, bit in enumerate(bits):
            self.cells[self.position + 1 + i] = 'R:' + bit
        self.ops += 4*(self.k+2)

    def step(self, newchar, direction):
        assert newchar in ('_', '0', '1')
        assert direction in (-1, 0, 1)
        pos = self.position
        self.cells[pos] = 'H:' + newchar
        # A local contiguous rewrite of length k+2, realizable in a constant
        # number of one-head sweeps with an O(1)-symbol carry state.
        if direction == 1:
            right = pos+self.k+1
            if right == len(self.cells):
                self.cells.append('_')
            nxt = self.cells[right]
            assert nxt in ('_', '0', '1')
            self.cells[pos:right+1] = [newchar, 'H:'+nxt] + ['R:'+a[-1] for a in self.cells[pos+1:right]]
            self.position += 1
        elif direction == -1:
            if pos == 0:
                self.cells.insert(0, '_')
                pos += 1
                self.position += 1
            left = pos-1
            prv = self.cells[left]
            assert prv in ('_', '0', '1')
            self.cells[left:pos+self.k+1] = ['H:'+prv] + self.cells[pos+1:pos+1+self.k] + [newchar]
            self.position -= 1
        self.ops += 8*(self.k+2)
        self.peak = max(self.peak, len(self.cells))
        self._check()


class DirectTape:
    def __init__(self):
        self.d = {0:'_'}
        self.h = 0
        self.l = 0
        self.r = 0

    def get(self):
        return self.d.get(self.h, '_')

    def step(self, a, movement):
        self.d[self.h] = a
        self.h += movement
        self.l = min(self.l, self.h)
        self.r = max(self.r, self.h)

    def comparable(self):
        return self.h-self.l, tuple(self.d.get(i,'_') for i in range(self.l,self.r+1))


def guest_instruction(typ, phase, inp, work):
    # Fixed finite transition tables, input head always stays or moves right.
    if inp == '#':
        return ('1' if work == '1' else '0'), 0, False, True
    if typ == 0:
        return inp, 1 if inp == '1' else -1, True, False
    if typ == 1:
        return inp, -1 if inp == '1' else 1, True, False
    if typ == 2:
        return ('0' if work == '1' else '1'), 1 if phase % 2 == 0 else -1, phase % 2 == 1, False
    if typ == 3:
        return inp, 0, phase % 3 == 2, False
    if typ == 4:
        return ('0' if work == '1' else '1'), -1 if phase % 3 == 0 else 1, phase % 3 == 2, False
    raise AssertionError


def check_case(source, t, typ):
    h = gamma_encode(t+1)
    val, consumed = gamma_decode(h+source)
    assert val == t+1 and consumed == len(h)
    assert source == (h+source)[consumed:]
    virtual = padded_truth(source, t)
    physical = MobileTape(t)
    direct = DirectTape()
    source_pos = 0
    offset = 0
    guest_pos = 0
    phase = 0
    matches = 0
    rounds = 0
    while True:
        vi = virtual[guest_pos] if guest_pos < len(virtual) else '#'
        xi = source[source_pos] if source_pos < len(source) else '#'
        assert vi == xi
        write, movement, advance, halt = guest_instruction(typ, phase, vi, direct.get())
        assert physical.cells[physical.position] == 'H:'+direct.get()
        direct.step(write, movement)
        physical.step(write, movement)
        if advance and guest_pos < len(virtual):
            guest_pos += 1
            offset += 1
            if offset == (1 << t):
                offset = 0
                source_pos += 1
            physical.set_register(offset)
        assert physical.register() == (format(offset, '0{}b'.format(t)) if t else '')
        idx, words = physical.decoded()
        dpos, dwords = direct.comparable()
        assert idx == dpos and words == dwords, (idx, dpos, words, dwords)
        rounds += 1
        matches += 1
        assert rounds < 10*(len(virtual)+5)
        phase += 1
        if halt:
            assert physical.ops <= 20*(t+2)*(rounds+2)
            return rounds, physical.ops, physical.peak, matches


def zero_gate(table, n):
    if all(b == '0' for b in table) or all(b == '1' for b in table):
        return True
    return any(all(b == str((i >> j) & 1) for i, b in enumerate(table))
               for j in range(n))


def main():
    started = perf_counter()
    counts = dict(cases=0, transitions=0, charged_proxy_ops=0, max_ratio=0.0,
                  peak_physical_cells=0, max_virtual_length=0, sample_cases=[])
    for n in (1,2,3):
        for bits in itertools.product('01', repeat=1 << n):
            source = ''.join(bits)
            for t in (0,1,2,3):
                for typ in range(5):
                    rounds, ops, peak, matches = check_case(source,t,typ)
                    counts['cases'] += 1
                    counts['transitions'] += rounds
                    counts['charged_proxy_ops'] += ops
                    counts['peak_physical_cells'] = max(counts['peak_physical_cells'], peak)
                    counts['max_virtual_length'] = max(counts['max_virtual_length'], (1 << n)*(1 << t))
                    counts['max_ratio'] = max(counts['max_ratio'], ops/((t+2)*rounds))
                    if n == 3 and t == 3 and len(counts['sample_cases']) < 5:
                        counts['sample_cases'].append(dict(source=source,t=t,guest=typ,transitions=rounds,physical_proxy_ops=ops))
    semantic_checks = 0
    for n in (1,2,3,4):
        length = 1 << n
        sources = ((''.join(bits) for bits in itertools.product('01', repeat=length))
                   if n <= 3 else
                   (format((q * 0x9e3779b1) % (1 << length), '0{}b'.format(length)) for q in range(1024)))
        for source in sources:
            expect = zero_gate(source, n)
            for t in (0,1,2,3):
                assert zero_gate(padded_truth(source,t), n+t) == expect
                semantic_checks += 1
    counts['both_label_mcsp0_checks'] = semantic_checks
    header_pairs = 0
    finite_header_cases = 0
    for n in range(1,6):
        for np in range(n+1,7):
            hs = gamma_encode(n+1)
            hl = gamma_encode(np+1)
            assert not hs.startswith(hl) and not hl.startswith(hs)
            assert any(a != b for a,b in zip(hs,hl))
            header_pairs += 1
        if n <= 3:
            observed = set()
            for bits in itertools.product('01', repeat=1 << n):
                x = ''.join(bits)
                y = gamma_encode(n+1) + x
                assert y not in observed
                observed.add(y)
                finite_header_cases += 1
            assert len(observed) == (1 << (1 << n))
    counts['prefix_header_pairs'] = header_pairs
    counts['header_injection_cases'] = finite_header_cases
    counts['elapsed_seconds'] = round(perf_counter()-started,3)
    counts['status']='COMPUTATIONAL_ONLY; no native TM compiler executed'
    path=Path(__file__).resolve()
    counts['script_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    print(json.dumps(counts,indent=2,sort_keys=True))


if __name__ == '__main__':
    main()
