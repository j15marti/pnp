"""Independent literal-image membership audit and legal slot-permutation control."""
from hashlib import sha256
from itertools import product, permutations
from pathlib import Path
import json

import t5_construction_disjoint_cut_20261121 as family
import t5_construction_positive_offset1_20261121 as compiler
import t5_bounds_disjoint_count_map_20261121 as peer


def descriptor(k):
    base = family.image(k,0,0)[0]
    owners = {}
    probes = []
    for coordinate in range(2*k):
        a,b = (1<<coordinate,0) if coordinate < k else (0,1<<(coordinate-k))
        one = family.image(k,a,b)[0]
        changes = [j for j,(x,y) in enumerate(zip(base,one)) if x != y]
        assert changes
        probes.append(changes[0])
        for j in changes:
            assert j not in owners
            owners[j] = coordinate
    return base,owners,probes


def admit(bits, desc):
    base,owners,probes = desc
    if len(bits) != len(base):
        return False
    coordinates = [int(bits[j] != base[j]) for j in probes]
    return all(int(value) == (int(base[j]) ^ (coordinates[owners[j]] if j in owners else 0))
               for j,value in enumerate(bits))


def output(circuit, outputs, bits):
    values = circuit.evaluate(bits)
    return sum(1<<i for i,node in enumerate(outputs) if values[node])


def audit(k):
    desc = descriptor(k)
    base, owners, probes = desc
    circuit, outputs, _, _ = peer.build(k)
    count = 0
    for a,b in product(range(1<<k),repeat=2):
        bits = family.image(k,a,b)[0]
        assert admit(bits,desc)
        coord = [(a>>i)&1 for i in range(k)]+[(b>>i)&1 for i in range(k)]
        assert all(int(bits[j]) == int(base[j]) ^ (coord[owners[j]] if j in owners else 0)
                   for j in range(len(bits)))
        expected = 0 if a&b else 10 << (98+282*k+k-b.bit_count())
        assert output(circuit, outputs,bits) == expected
        count += 1
    controls = []
    # Swap C slots in a clause containing a coordinate probe: same formula semantics.
    n, clauses = compiler.decode(base)
    w = n.bit_length()
    header = len(base)-3*len(clauses)*w
    candidate_rows = sorted({(j-header)//(3*w) for j in probes})
    for index in candidate_rows:
        original = clauses[index]
        for order in permutations(range(3)):
            changed = clauses.copy()
            changed[index] = tuple(original[i] for i in order)
            bits = compiler.encode(n,changed)
            if bits == base:
                continue
            assert sorted(changed[index]) == sorted(original)
            assert compiler.decode(bits) == (n,changed)
            assert not admit(bits,desc)
            predicted = output(circuit,outputs,bits)
            actual = 10 << (98+282*k+k)
            controls.append(dict(row=index,order=order,old_clause=original,new_clause=changed[index],
                                 true_count=str(actual),unguarded_count=str(predicted),
                                 encoding_sha256=sha256(bits.encode()).hexdigest()))
    assert any(x["true_count"] != x["unguarded_count"] for x in controls)
    # Unrelated full-domain strict-C instances of the same n,m, including both labels.
    m = len(clauses)
    independent = [(0,1,2)]*m
    # Four all-different triples on four names cannot all be cyclic C triples.
    impossible = [(0,1,2),(0,1,3),(0,2,3),(1,2,3)] + [(0,1,2)]*(m-4)
    assert not any(all(compiler.C(*(values[v] for v in t)) for t in impossible[:4])
                   for values in product(range(5),repeat=4))
    assert not admit(compiler.encode(n,independent),desc)
    assert not admit(compiler.encode(n,impossible),desc)
    return dict(k=k,N=len(base),coordinate_probes=probes,variable_positions=len(owners),
                canonical_cases=count,slot_controls=controls,
                unrelated_same_length_controls=["SAT: 30*5^(n-3)","UNSAT: four-triple obstruction"])


if __name__ == "__main__":
    rows = [audit(k) for k in (1,2)]
    print(json.dumps(dict(results=rows,
        dependencies={Path(x.__file__).name:sha256(Path(x.__file__).read_bytes()).hexdigest()
                      for x in (family,compiler,peer)}),indent=2))
