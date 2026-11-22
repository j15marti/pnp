"""Exact local projection audit. Python 3; no third-party dependencies.

Reuses pinned peer acquisition routines to test a new non-affine variant.
The generic projection routine uses exact finite tables, never hash equality.
"""
from itertools import combinations, product
import json
from dynamic_redteam_affine_pivot_20261121 import family, admit, components, algebra
from dynamic_accounting_paid_backdoor_20261121 import find_hit, truth


def nonaffine_family(signs):
    return family(signs) + tuple((3*i+1, 3*i+2, 3*i+3) for i in range(len(signs)))


def table(rows, scope):
    return frozenset(bits for bits in product((0, 1), repeat=len(scope))
                     if all(any(dict(zip(scope, bits))[abs(v)] == (v > 0)
                                for v in row) for row in rows))


def block_affine_filter(rows):
    blocks = {}
    for row in rows:
        blocks.setdefault(tuple(sorted(map(abs, row))), []).append(row)
    for scope, block in blocks.items():
        values = table(block, scope)
        if any(tuple(a^b^c for a,b,c in zip(x,y,z)) not in values
               for x in values for y in values for z in values):
            return False
    return True


def project_decision(rows, cap=4):
    """Smallest eligible variable; all incident factors must enter its bucket."""
    factors = [(tuple(sorted(set(map(abs, row)))),
                table([row], tuple(sorted(set(map(abs, row)))))) for row in rows]
    stats = dict(eliminations=0, candidate_checks=0, factor_scans=0,
                 joint_rows=0, max_union=0, peak_factors=len(factors))
    order = []
    while True:
        if any(not values for scope, values in factors):
            return "UNSAT", stats, order
        # Exact true factors impose no condition, so delete them.
        factors = [(scope, values) for scope, values in factors
                   if len(values) != 2**len(scope)]
        live = sorted({v for scope, values in factors for v in scope})
        if not live:
            return "SAT", stats, order
        chosen = None
        for v in live:
            stats["candidate_checks"] += 1
            bucket = []
            union = set()
            for factor in factors:
                stats["factor_scans"] += 1
                if v in factor[0]:
                    bucket.append(factor)
                    union.update(factor[0])
            if len(union) <= cap:
                chosen = v, bucket, tuple(sorted(union))
                break
        if chosen is None:
            return "UNKNOWN", stats, order
        v, bucket, union = chosen
        rest = tuple(x for x in union if x != v)
        projected = set()
        for bits in product((0, 1), repeat=len(union)):
            stats["joint_rows"] += 1
            assignment = dict(zip(union, bits))
            if all(tuple(assignment[x] for x in scope) in values
                   for scope, values in bucket):
                projected.add(tuple(assignment[x] for x in rest))
        factors = [factor for factor in factors if v not in factor[0]]
        factors.append((rest, frozenset(projected)))
        order.append(v)
        stats["eliminations"] += 1
        stats["max_union"] = max(stats["max_union"], len(union))
        stats["peak_factors"] = max(stats["peak_factors"], len(factors))


def satisfies(rows, bits):
    return all(any(bits[abs(v)-1] == (v>0) for v in row) for row in rows)


def main():
    cases = []
    for k in (4, 6):
        signs_list = list(product((0,1),repeat=k)) if k == 4 else [(0,)*k,(1,)+(0,)*(k-1)]
        for signs in signs_list:
            rows = nonaffine_family(signs)
            assert len(rows) == 9*k and len(components(rows)) == 1
            assert not block_affine_filter(rows)
            assert admit(rows,k-2) is None
            assert admit(rows,k-1) is not None
            decision, stats, order = project_decision(rows)
            expected = "SAT" if algebra(signs) else "UNSAT"
            assert decision == expected and stats["max_union"] <= 4
            if k == 4:
                assert truth(rows) == (decision == "SAT")
            cases.append(dict(k=k, signs=signs, decision=decision, p=k-1,
                              affine_filter=False, stats=stats, order=order))
    # Explicit non-affineness of a SAT relation, not just syntactic filter failure.
    k=4
    rows=nonaffine_family((0,)*k)
    a=tuple(bit for _ in range(k) for bit in (1,1,0))+(0,)
    b=tuple(bit for _ in range(k) for bit in (0,1,1))+(0,)
    c=(1,0,1)+tuple(bit for _ in range(k-1) for bit in (0,1,1))+(0,)
    xor=tuple(x^y^z for x,y,z in zip(a,b,c))
    assert all(satisfies(rows,v) for v in (a,b,c)) and not satisfies(rows,xor)
    trees=[]
    for k in (4,6,8,10):
        rows=nonaffine_family((0,)*k)
        hit,stats=find_hit(rows,k-2)
        assert hit is None and stats["calls"]==(3**(k-1)-1)//2
        decision,projection,order=project_decision(rows)
        assert decision=="SAT"
        trees.append(dict(k=k,budget=k-2,failed_search=stats,projection=projection))
    # UNKNOWN is not UNSAT, and all factors sharing a variable must be joined.
    dense=tuple(combinations(range(1,6),3))
    assert project_decision(dense)[0]=="UNKNOWN" and truth(dense)
    assert project_decision(((1,),(-1,)))[0]=="UNSAT"
    assert project_decision(())[0]=="SAT"
    assert project_decision(((1,2),(-1,2),(1,-2),(-1,-2)))[0]=="UNSAT"
    return dict(status="COMPUTATIONAL",cases=cases,failed_trees=trees,
                nonaffine_witness=dict(a=a,b=b,c=c,xor=xor),
                controls=dict(dense_positive="UNKNOWN but SAT",contradictory_units="UNSAT",
                              empty_formula="SAT",shared_bucket="UNSAT"),
                scope="Source decisions, acquisition counts and exact tables; no TM timings or new compiled runs.")


if __name__ == "__main__":
    print(json.dumps(main(),indent=2))
