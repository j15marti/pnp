"""Build the mixed source and audit its projections. Python 3, no dependencies.
Call compiled_source(rows) from the repository's experiments directory for target bits.
"""
import itertools
import json

def block(ids, allowed):
    return [tuple(-v if bit else v for v, bit in zip(ids, bits))
            for bits in itertools.product((0, 1), repeat=3) if not allowed(bits)]

def generate(rows):
    occurrences = {}
    factors, equalities = [], []
    for j, row in enumerate(rows):
        ids = tuple(range(3*j+1, 3*j+4))
        factors.append(block(ids, lambda bits: sum(bits) == 1))
        for name, v in zip(row, ids):
            occurrences.setdefault(name, []).append(v)
    n = 3*len(rows)
    for group in occurrences.values():
        for x, y in zip(group, group[1:]):
            a, b = n+1, n+2
            n += 2
            equalities.append((x, y, a, b,
                block((x,a,b), lambda bits: sum(bits)%2 == 0) +
                block((y,a,b), lambda bits: sum(bits)%2 == 0)))
    return n, factors, equalities

def compiled_source(rows):
    from dynamic_construction_dihedral_choice_20261121 import build, codec
    _, f, e = generate(rows)
    clauses = [c for g in f for c in g] + [c for *_, g in e for c in g]
    return build(codec.load_generator(), clauses)[0]

def holds(clauses, value):
    return all(any(value[abs(v)] == (v > 0) for v in row) for row in clauses)

def check(rows):
    n, factors, eq = generate(rows)
    ports = 3*len(rows)
    names = sorted(set(itertools.chain.from_iterable(rows)))
    original = {tuple(a[names.index(v)] for row in rows for v in row)
                for a in itertools.product((0,1), repeat=len(names))
                if all(sum(a[names.index(v)] for v in row)==1 for row in rows)}
    accepted = set()
    for bits in itertools.product((0,1), repeat=ports):
        val = dict(enumerate(bits,1))
        if all(holds(g,val) for g in factors) and all(
            any(holds(g,{**val,a:i,b:j}) for i,j in itertools.product((0,1),repeat=2))
            for x,y,a,b,g in eq):
            accepted.add(bits)
    assert accepted == original
    c = sum(map(len,factors)) + sum(len(g) for *_,g in eq)
    assert (n,c)==(ports+2*(ports-len(names)),5*len(rows)+8*(ports-len(names)))
    return dict(rows=rows, projected_assignments=len(accepted), names=n, clauses=c)

if __name__ == "__main__":
    triples=list(itertools.product((1,2), repeat=3))
    cases=[check(rows) for rows in itertools.product(triples, repeat=2)]
    from dynamic_synthesis_reachable_splice_20261121 import parse
    from hashlib import sha256
    images=[]
    for rows in [((1,1,2),(1,1,2)), ((1,1,2),(2,2,2))]:
        bits=compiled_source(rows)
        n, clauses, alpha, beta, release=parse(bits)
        assert sum(a!=b for a,b in zip(alpha,beta))==1
        for row in clauses:
            assignment=alpha if sum(v>0 for v in row)<=1 else beta
            assert any((assignment[abs(v)-1]=="1")==(v>0) for v in row)
        c,d=42,14
        r=c+1
        n0=d+(10*c+1)*r+2
        m0=(20*c+4)*r
        assert (n,len(clauses),release)==(n0+m0+3,2*m0+4,n0+1)
        m=len(clauses)
        w=n.bit_length()
        assert len(bits)==3*n+2+2*((m+1).bit_length()-1)+3*m*(w+1)+w
        images.append(dict(rows=rows,n=n,m=m,N=len(bits),sha256=sha256(bits.encode()).hexdigest()))
    print(json.dumps(dict(images=images,cases=cases,SAT=sum(x['projected_assignments']>0 for x in cases),
                          UNSAT=sum(x['projected_assignments']==0 for x in cases)),indent=1))
