"""Audit fixed peer branching and exact residual caching on a legal CNF family."""
from itertools import product
from hashlib import sha256
from pathlib import Path
import json
import dynamic_discovery_switched_cut_20261121 as peer


def family(k, unsat=True):
    rows = [(3*i+1,3*i+2,3*i+3) for i in range(k)]
    core = [tuple(sign*(3*k+i) for i,sign in enumerate(pattern,1))
            for pattern in product((1,-1),repeat=3)]
    return rows + (core if unsat else core[:-1])


def memoized(rows):
    cache = {}
    calls = hits = 0
    def visit(current):
        nonlocal calls,hits
        calls += 1
        if current in cache:
            hits += 1
            return cache[current]
        optimum = peer.energy_min(current)
        if optimum is not None:
            result = optimum == 0
        else:
            pivot = min(abs(l) for c in current for l in c)
            result = False
            for bit in (0,1):
                lit = pivot if bit else -pivot
                residual = tuple(tuple(l for l in c if l != -lit)
                                 for c in current if lit not in c)
                if visit(residual):
                    result = True
                    break
        cache[current] = result
        return result
    result = visit(tuple(rows))
    return dict(sat=result,calls=calls,hits=hits,distinct=len(cache),
                cached_literals=sum(sum(len(c) for c in f) for f in cache))


def main():
    rows=[]
    for k in range(1,7):
        cs=family(k)
        original=peer.decision_tree(cs)
        cached=memoized(cs)
        assert original["nodes"] == 4**k-1
        assert original["admitted_leaves"] == 2*4**(k-1)
        assert original["max_depth"] == 3*k-2 and not original["sat"]
        assert not cached["sat"] and cached["distinct"] == 3*k*(k+1)//2
        assert cached["calls"] == 3*k*k-k+1
        rows.append(dict(k=k,original=original,cached=cached))
    large=[dict(k=k,**memoized(family(k))) for k in (10,20,30)]
    assert all(not r["sat"] for r in large)
    controls=[dict(k=k,**memoized(family(k,False))) for k in (1,2,5,10)]
    assert all(r["sat"] for r in controls)
    import dynamic_construction_dihedral_choice_20261121 as construction
    mod=construction.codec.load_generator()
    encoded=[]
    for k in (1,2,3):
        for flag in (False,True):
            cs=family(k,flag)
            bits,_,_=construction.build(mod,cs)
            assert peer.extract(mod,bits)==cs
            assert memoized(cs)["sat"] == (not flag)
            n,target,*_=construction.codec.parse(bits)
            encoded.append(dict(k=k,unsat_core=flag,n=n,m=len(target),N=len(bits),
                                sha256=sha256(bits.encode()).hexdigest()))
    return dict(encoded=encoded,rows=rows,large=large,sat_controls=controls,
                peer_sha256=sha256(Path(peer.__file__).read_bytes()).hexdigest(),
                status="COMPUTATIONAL; solver nodes, not TM timings")


if __name__=="__main__":
    print(json.dumps(main(),indent=2))
