"""Exact tests of a signed-partition completion rule on Boolean wire scopes."""
import hashlib
import itertools
import json
from pathlib import Path

import t5_accounting_sil_parity_return_20261121 as source
import t5_construction_positive_offset1_20261121 as compiler

assert hashlib.sha256(Path(source.__file__).read_bytes()).hexdigest() == 'dc638ba9988a597361b67ec4476bf85c18e4909e74a04d284c958baf0bff1382'


def envelope(rows, width):
    # rows are actual distinct models in this test verifier.
    if not rows:
        return None
    pins, blocks = [], {}
    for i in range(width):
        column = tuple(row[i] for row in rows)
        if len(set(column)) == 1:
            pins.append((i, column[0]))
        else:
            normalized = tuple(bit ^ column[0] for bit in column)
            blocks.setdefault(normalized, []).append((i, column[0]))
    return pins, list(blocks.values())


def diagram(desc):
    # Constants 0,1; all other nodes refer to earlier ones.
    nodes = [None, None]

    def add(op, *args):
        nodes.append((op, *args))
        return len(nodes)-1

    def chain(pairs):
        root = 1
        for i, val in reversed(pairs):
            root = add('if', i, 0 if val else root, root if val else 0)
        return root

    if desc is None:
        return nodes, 0
    pins, blocks = desc
    roots = [chain(pins)] if pins else []
    for block in blocks:
        if len(block) == 1:
            continue
        i, sign = block[0]
        branches = [chain([(j, bit ^ sign ^ val) for j, bit in block[1:]]) for val in (0,1)]
        roots.append(add('if', i, *branches))
    root = roots.pop() if roots else 1
    for other in roots:
        root = add('and', root, other)
    return nodes, root


def evaluate(nodes, root, row):
    values = [False, True]
    for op, *args in nodes[2:]:
        if op == 'if':
            i, lo, hi = args
            values.append(values[hi if row[i] else lo])
        else:
            values.append(values[args[0]] and values[args[1]])
    return values[root]


def encode(bits, pin):
    n, clauses = source.images(bits)[pin]
    n, split, _ = compiler.split(n, clauses)
    return compiler.encode(n, split)


def recognize(data):
    n = data.find('0')
    if n < 997 or (n-641) % 356:
        return None
    k = (n-641)//356
    for pin in (0,1):
        zero = (0,)*k
        baseline = encode(zero, pin)
        if len(data) != len(baseline):
            continue
        switches = []
        for j in range(k):
            variant = encode(tuple(int(i == j) for i in range(k)), pin)
            at = next(i for i, (a,b) in enumerate(zip(baseline, variant)) if a != b)
            switches.append(int(data[at] != baseline[at]))
        if data == encode(switches, pin):
            return switches, pin
    return None


def wire_models(switches, pin):
    gates, out = source.circuit(switches)
    b = 1 + len(gates)
    gates += [('not', out), ('not', b), ('not', b+1)]
    rows = []
    for x in (0,1):
        row = [x]
        for op, *args in gates:
            row.append(1-row[args[0]] if op == 'not' else row[args[0]] | row[args[1]])
        if row[b+1-pin]:
            rows.append(tuple(row))
    return rows, 1+len(gates)


def main():
    width = 3
    universe = list(itertools.product(range(2), repeat=width))
    accepted = []
    for mask in range(256):
        rows = [r for i,r in enumerate(universe) if mask & (1<<i)]
        desc = envelope(rows,width)
        size = 0 if desc is None else 1 << len(desc[1])
        nodes,root = diagram(desc)
        actual = [r for r in universe if evaluate(nodes,root,r)]
        assert len(actual) == size and set(rows) <= set(actual)
        assert (len(rows) == size) == (rows == actual)
        assert len(nodes) <= 3*width+2
        if size == len(rows):
            accepted.append(mask)
    parity = [r for r in universe if sum(r)%2==0]
    assert len(parity) == 4 and len(envelope(parity,3)[1]) == 3
    cases = []
    for k in (1,2,3):
        for bits in itertools.product(range(2),repeat=k):
            for pin in (0,1):
                data = encode(bits,pin)
                assert recognize(data) == (list(bits),pin)
                rows, s = wire_models(bits,pin)
                desc = envelope(rows,s)
                size = 0 if desc is None else 1 << len(desc[1])
                nodes,root = diagram(desc)
                assert size == len(rows) == (2 if sum(bits)%2 == pin else 0)
                assert all(evaluate(nodes,root,r) for r in rows)
                assert len(nodes)<=3*s+2
                cases.append(dict(k=k,bits=bits,pin=pin,N=len(data),scope=s,
                                  wire_count=size,nodes=len(nodes),sha256=hashlib.sha256(data.encode()).hexdigest()))
    # A legal C input outside both canonical images: permute first triple slots.
    data = encode((0,),0)
    n,cs = compiler.decode(data)
    a,b,c = cs[0]
    cs[0] = (b,a,c)
    assert recognize(compiler.encode(n,cs)) is None
    print(json.dumps(dict(accepted_three_bit_masks=accepted, rejected_three_bit=256-len(accepted),
                          parity_count=4,parity_hull_count=8, canonical_cases=cases,
                          legal_noncanonical='UNKNOWN', script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2))


if __name__ == '__main__':
    main()
