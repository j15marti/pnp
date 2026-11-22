"""Audit the pinned one-pivot acquisition on connected affine cycles."""
from itertools import product
import json
from dynamic_accounting_paid_backdoor_20261121 import find_hit, restrict

def parity(names, rhs):
    return tuple(tuple(-v if bit else v for v,bit in zip(names,bits))
                 for bits in product((0,1),repeat=3) if sum(bits)%2 != rhs)

def family(signs):
    k = len(signs)
    rows = []
    for i in range(k):
        rows.extend(parity((3*i+1,3*i+2,3*i+3),0))
    for i,s in enumerate(signs):
        rows.extend(parity((3*i+3,3*((i+1)%k)+3,3*k+1),s))
    return tuple(rows)

def components(rows):
    todo = list(rows)
    result = []
    while todo:
        part = [todo.pop(0)]
        names = set(map(abs,part[0]))
        changed = True
        while changed:
            changed = False
            for row in todo[:]:
                if names.intersection(map(abs,row)):
                    todo.remove(row)
                    part.append(row)
                    names.update(map(abs,row))
                    changed = True
        result.append(tuple(part))
    return result

def admit(rows, budget):
    for pivot in [None]+sorted({abs(v) for row in rows for v in row}):
        branches = [rows] if pivot is None else [
            restrict(rows,{pivot:value}) for value in (False,True)]
        if all(find_hit(c,budget)[0] is not None
               for branch in branches for c in components(branch)):
            return pivot
    return None

def algebra(signs):
    k = len(signs)
    solutions = 0
    for g,z0 in product((0,1),repeat=2):
        z = z0
        for s in signs:
            z ^= g ^ s
        solutions += (z == z0)
    return solutions > 0

def main():
    cases = []
    for k in (4,6):
        signs_list = list(product((0,1),repeat=k)) if k==4 else [(0,)*k,(1,)+(0,)*(k-1)]
        for signs in signs_list:
            rows = family(signs)
            assert len(components(rows)) == 1
            assert algebra(signs) == (sum(signs)%2==0)
            assert admit(rows,k-2) is None
            pivot = admit(rows,k-1)
            assert pivot is not None
            cases.append(dict(k=k,signs=signs,sat=algebra(signs),p=k-1,pivot=pivot))
    trees=[]
    for k in (4,6,8,10):
        rows=family((0,)*k)
        hit,stats=find_hit(rows,k-2)
        assert hit is None
        assert stats["calls"] == (3**(k-1)-1)//2
        trees.append(dict(k=k,budget=k-2,**stats))
    # Independent truth-table validation of every local parity clause expansion.
    local=0
    for rhs in (0,1):
        rows=parity((1,2,3),rhs)
        for bits in product((False,True),repeat=3):
            actual=all(any(bits[abs(v)-1]==(v>0) for v in row) for row in rows)
            assert actual==(sum(bits)%2==rhs)
            local+=1
    return dict(status="COMPUTATIONAL",local_truth_rows=local,cases=cases,failed_trees=trees,
                scope="Source acquisition counts and algebra checks; no TM timings or new compiled SAT runs.")
if __name__=="__main__":
    print(json.dumps(main(),indent=2))
