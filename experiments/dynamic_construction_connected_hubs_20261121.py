"""Connected shared-selector construction. Run from the repository root."""
from collections import defaultdict
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, product
import json

import dynamic_construction_dihedral_choice_20261121 as construction
import dynamic_discovery_switched_cut_20261121 as discovery


def family(k, satisfiable):
    z, w, a = range(2*k+1, 2*k+4)
    rows = []
    for x in range(1, k+1):
        y = k+x
        for triple in ((x,y,z), (-x,y,w)):
            rows.extend((triple, tuple(-v for v in triple)))
    core = [tuple(v*s for v,s in zip((z,w,a), signs))
            for signs in product((1,-1), repeat=3)]
    if satisfiable:
        core[-1] = core[0]
    return tuple(rows+core)


def restrict(rows, lit):
    return tuple(tuple(v for v in row if v != -lit) for row in rows if lit not in row)


def components(rows):
    by_variable = defaultdict(list)
    for i,row in enumerate(rows):
        for v in row:
            by_variable[abs(v)].append(i)
    pending = set(range(len(rows)))
    parts = []
    while pending:
        start = min(pending)
        pending.remove(start)
        group, stack = [start], [start]
        while stack:
            for v in rows[stack.pop()]:
                for j in by_variable[abs(v)]:
                    if j in pending:
                        pending.remove(j)
                        stack.append(j)
                        group.append(j)
        parts.append(tuple(rows[j] for j in sorted(group)))
    return parts


def component_solver(rows):
    stats = dict(splits=0, simplifications=0, cut_leaves=0)
    @lru_cache(None)
    def solve(f):
        if () in f or not f:
            return not f
        literals = {v for row in f for v in row}
        units = sorted(row[0] for row in f if len(row)==1)
        pure = sorted(v for v in literals if -v not in literals)
        if units or pure:
            stats["simplifications"] += 1
            return solve(restrict(f,(units or pure)[0]))
        parts = components(f)
        if len(parts)>1:
            stats["splits"] += 1
            return all(solve(part) for part in parts)
        value = discovery.energy_min(f)
        if value is not None:
            stats["cut_leaves"] += 1
            return value==0
        x = min(map(abs,literals))
        return solve(restrict(f,-x)) or solve(restrict(f,x))
    decision = solve(rows)
    return dict(sat=decision, **stats, misses=solve.cache_info().misses,
                hits=solve.cache_info().hits)


def binary_sat(rows):
    if () in rows:
        return False
    arcs = defaultdict(set)
    for row in rows:
        assert 1 <= len(row) <= 2
        u,v = row[0], row[-1]
        arcs[-u].add(v)
        arcs[-v].add(u)
    def reaches(u,v):
        visited, stack = {u}, [u]
        while stack:
            here = stack.pop()
            if here==v:
                return True
            for nxt in arcs.get(here,()):
                if nxt not in visited:
                    visited.add(nxt)
                    stack.append(nxt)
        return False
    return all(not (reaches(u,-u) and reaches(-u,u)) for u in tuple(arcs))


def backdoor(rows):
    ternary = [set(map(abs,row)) for row in rows if len(row)==3]
    names = sorted({abs(v) for row in rows for v in row})
    for size in range(3):
        for key in combinations(names,size):
            if not all(set(key)&row for row in ternary):
                continue
            outcomes = []
            for signs in product((1,-1),repeat=size):
                residual = rows
                for v,s in zip(key,signs):
                    residual = restrict(residual,s*v)
                outcomes.append(binary_sat(residual))
            return dict(key=key, branches=outcomes, sat=any(outcomes))
    return None


def main():
    mod = construction.codec.load_generator()
    records = []
    for k in range(1,9):
        for flag in (False,True):
            f = family(k,flag)
            slow, fast = component_solver(f), backdoor(f)
            assert slow["sat"]==fast["sat"]==flag
            if not flag:
                assert (slow["misses"],slow["hits"],slow["cut_leaves"])==(2**(k+1)-1,0,2**k)
                assert slow["splits"]==slow["simplifications"]==0
            rec = dict(k=k, sat=flag, component=slow, backdoor=fast)
            if k<=2:
                bits,_,r = construction.build(mod,list(f))
                assert discovery.extract(mod,bits)==list(f)
                n, rows, alpha,beta,_ = construction.codec.parse(bits)
                assert sum(a!=b for a,b in zip(alpha,beta))==1
                answer,version = construction.z3_result(rows,n)
                assert answer==("sat" if flag else "unsat")
                c,d = len(f),2*k+3
                n0,m0 = d+(10*c+1)*r+2,(20*c+4)*r
                assert (n,len(rows))==(n0+m0+3,2*m0+4)
                m=len(rows)
                assert len(bits)==3*n+2+2*((m+1).bit_length()-1)+3*m*(n.bit_length()+1)+n.bit_length()
                rec.update(n=n,m=m,N=len(bits),sha256_ascii=sha256(bits.encode()).hexdigest(),
                           target_z3=answer,z3_version=version)
            records.append(rec)
    # Outside admission: three disjoint proper triples need three hits.
    assert backdoor(((1,2,3),(4,5,6),(7,8,9))) is None
    return dict(status="COMPUTATIONAL",records=records)

if __name__=="__main__":
    print(json.dumps(main(),indent=2))
