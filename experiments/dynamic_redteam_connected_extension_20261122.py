"""Connected extension audit. Python 3 standard library, no SAT package."""
from itertools import product
from pathlib import Path
import json


def clauses(ids, predicate):
    return [frozenset(-v if b else v for v, b in zip(ids, bits))
            for bits in product((0, 1), repeat=3) if not predicate(bits)]


def rank(rows):
    pivots = {}
    for value in rows:
        while value:
            bit = value.bit_length()-1
            if bit in pivots:
                value ^= pivots[bit]
            else:
                pivots[bit] = value
                break
    return len(pivots)


def build(types):
    base, equations, ports = [], [], []
    for block, kind in enumerate(types):
        offset = 18*block
        port = [offset+i+1 for i in range(12)]
        ports.extend(port)
        for start in range(0, 12, 3):
            base.extend(clauses(port[start:start+3], lambda bits: sum(bits)==1))
        checked = port[:8] + [port[8+kind]]
        aux = [offset+13+i for i in range(6)]
        local = [(checked[0], checked[1], aux[0])]
        local += [(aux[i-1], checked[i+1], aux[i]) for i in range(1,6)]
        local += [(aux[5], checked[7], checked[8])]
        equations.extend(local)
        for triple in local:
            base.extend(clauses(triple, lambda bits: sum(bits)%2==0))
    shared = 18*len(types)+1
    leaves = list(range(shared+1, shared+1+len(ports)))
    connected = list(base)
    for port, leaf in zip(ports, leaves):
        triple = (port, shared, leaf)
        equations.append(triple)
        connected.extend(clauses(triple, lambda bits: sum(bits)%2==0))
    return base, connected, equations, ports, leaves


def main():
    records = []
    for count in range(1,5):
        for types in product((0,1), repeat=count):
            base, cnf, equations, ports, leaves = build(types)
            assert len(cnf)==96*count
            names = set(abs(v) for clause in cnf for v in clause)
            assert len(names)==30*count+1
            visited = {next(iter(names))}
            while True:
                extended = visited | {abs(v) for clause in cnf
                    if any(abs(w) in visited for w in clause) for v in clause}
                if extended==visited:
                    break
                visited=extended
            assert visited==names
            reduced=list(cnf)
            for leaf in leaves:
                positive=[c for c in reduced if leaf in c]
                negative=[c for c in reduced if -leaf in c]
                resolvents=[(a-{leaf}) | (b-{-leaf}) for a in positive for b in negative]
                assert all(any(-v in r for v in r) for r in resolvents)
                reduced=[c for c in reduced if leaf not in c and -leaf not in c]
            assert reduced==base
            rows=[sum(1 << (v-1) for v in triple) for triple in equations]
            portmask=sum(1 << (v-1) for v in ports)
            codimension=rank(rows)-rank([r & ~portmask for r in rows])
            assert codimension==count
            records.append(dict(types=types, variables=len(names), clauses=len(cnf),
                connected=True, k=codimension, s=len(ports)-codimension,
                eliminated=len(leaves), base_recovered=True))
    # Sharing one leaf imposes equality on two otherwise free ports.
    mutation=[]
    for x,y in product((0,1), repeat=2):
        possible=any((x^g^a)==0 and (y^g^a)==0 for g,a in product((0,1),repeat=2))
        assert possible==(x==y)
        mutation.append([x,y,possible])
    destination=Path("results/raw/dynamic_redteam_connected_extension_20261122.json")
    destination.parent.mkdir(parents=True,exist_ok=True)
    destination.write_text(json.dumps(dict(cases=records,shared_leaf_control=mutation),indent=2)+"\n")
    print(json.dumps(dict(cases=len(records),all_passed=True)))


if __name__ == "__main__":
    main()
