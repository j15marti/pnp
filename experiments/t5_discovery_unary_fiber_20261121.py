"""Build and check full named three-bit diagrams on canonical balanced DISJ images."""
from collections import defaultdict
from hashlib import sha256
from itertools import product
import json
import random
from pathlib import Path

import t5_construction_disjoint_cut_20261121 as family
import t5_construction_positive_offset1_20261121 as c


def row(k, gates, out, mask):
    wires = [(mask >> i) & 1 for i in range(k)]
    for op, *args in gates:
        wires.append(1-wires[args[0]] if op == "not" else wires[args[0]] | wires[args[1]])
    value = wires[out]
    assert value == 1
    wires.extend([1-value, value, 1-value])
    names = list(range(5)) + wires
    for bit in wires:
        for j in (2, 3, 4):
            allowed = [h for h in range(5) if c.C(j,bit,h) and c.C((j+2)%5,(j+3)%5,h)]
            h, = allowed
            names.append(h)
    for op, *args in gates:
        if op == "or":
            names.extend([0 if wires[args[0]] else 3, 2 if wires[args[1]] else 4])
    return names


class Diagram:
    def __init__(self):
        self.nodes = [("false",), ("true",)]
        self.memo = {}

    def put(self, node):
        if node not in self.memo:
            self.memo[node] = len(self.nodes)
            self.nodes.append(node)
        return self.memo[node]

    def both(self, x, y):
        return y if x == 1 else x if y == 1 else self.put(("and", x, y))

    def truth(self, names, alternatives):
        # A trie dispatches exact full color strings to the supplied continuations.
        rows = [(tuple((v >> bit) & 1 for v in colors for bit in (2,1,0)), tail)
                for colors, tail in alternatives]
        def build(j, subset):
            if not subset:
                return 0
            if j == 3*len(names):
                (bits, tail), = subset
                return tail
            kids = [build(j+1, [(s,t) for s,t in subset if s[j] == b]) for b in (0,1)]
            return self.put(("test", 3*names[j//3]+j%3, *kids))
        return build(0, rows)


def compile_image(k, a, b):
    _, _, gates, out, n, clauses = family.image(k,a,b)
    nn, split, links = c.split(n,clauses)
    dag = Diagram()
    if a & b:
        return dag, 0, nn, split
    base = row(k,gates,out,0)
    single = {i: row(k,gates,out,1<<i) for i in range(k) if not (b>>i)&1}
    copies = [[] for _ in range(n)]
    for j, triple in enumerate(clauses):
        for slot,v in enumerate(triple):
            copies[v].append(3*j+slot)
    groups = defaultdict(list)
    private = []
    cursor = 3*len(clauses)
    for v in range(n):
        affected = [i for i, changed in single.items() if changed[v] != base[v]]
        assert len(affected) <= 1
        groups[affected[0] if affected else -1].append(v)
        private.append(list(range(cursor,cursor+4*(len(copies[v])-1),4)))
        cursor += 4*(len(copies[v])-1)
    assert cursor == nn
    anchors = [copies[v][0] for v in range(5)]
    frames = []
    for origin, step in product(range(5),(-1,1)):
        def color(v):
            return (origin+step*v)%5
        root = 1
        for group, variables in groups.items():
            selector = copies[5+group][0] if group >= 0 else None
            options = []
            for values in ([base, single[group]] if group >= 0 else [base]):
                term = 1
                for v in variables:
                    port = color(values[v])
                    for copy in copies[v]:
                        if copy not in anchors and copy != selector:
                            term = dag.both(term, dag.truth([copy],[([port],1)]))
                    for start in private[v]:
                        variants = [([(port+d*j)%5 for j in (1,2,3,4)],1) for d in (-1,1)]
                        term = dag.both(term,dag.truth(range(start,start+4),variants))
                if selector is None:
                    root = dag.both(root,term)
                else:
                    options.append(([color(values[5+group])],term))
            if options:
                root = dag.both(root,dag.truth([selector],options))
        frames.append(([color(i) for i in range(5)],root))
    return dag, dag.truth(anchors,frames), nn, split


def audit(k,a,b):
    dag, root, n, clauses = compile_image(k,a,b)
    counts = [0,1]
    for op,*args in dag.nodes[2:]:
        x,y = args[-2:]
        counts.append(counts[x]*counts[y] if op == "and" else counts[x]+counts[y])
    expected = 0 if a & b else 10 << (98+282*k+k-b.bit_count())
    assert counts[root] == expected
    rng = random.Random(41)
    for _ in range(4 if root else 0):
        bits = {}
        todo = [root]
        while todo:
            j = todo.pop()
            if j == 1:
                continue
            op,*args = dag.nodes[j]
            if op == "and":
                todo.extend(args)
            else:
                bit, x, y = args
                assert bit not in bits
                bits[bit] = rng.choice([v for v,node in enumerate((x,y)) if counts[node]])
                todo.append((x,y)[bits[bit]])
        assert len(bits) == 3*n
        colors = [4*bits[3*i]+2*bits[3*i+1]+bits[3*i+2] for i in range(n)]
        assert max(colors)<5 and all(c.C(*(colors[v] for v in clause)) for clause in clauses)
    return dict(k=k,a=a,b=b,n=n,nodes=len(dag.nodes),count=str(counts[root]),
                checked_complete_witnesses=4 if root else 0)


if __name__ == "__main__":
    cases = [(1,0,0),(1,1,1),(2,2,1),(3,1,4),(5,0,0),(8,85,170)]
    print(json.dumps(dict(seed=41,results=[audit(*case) for case in cases],
        generator_sha256=sha256(Path(family.__file__).read_bytes()).hexdigest()),indent=2))
