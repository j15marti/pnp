"""Audit paid backdoor search counts. Python 3, no third-party packages."""
from itertools import combinations, product
import json

def find_hit(rows, budget):
    supports = [set(map(abs,row)) for row in rows if len(row)==3]
    stats = {"calls":0,"support_checks":0}
    def visit(selected, left):
        stats["calls"] += 1
        uncovered = None
        for support in supports:
            stats["support_checks"] += 1
            if not support.intersection(selected):
                uncovered = support
                break
        if uncovered is None:
            return selected
        if left == 0:
            return None
        for variable in sorted(uncovered):
            answer = visit(selected+(variable,),left-1)
            if answer is not None:
                return answer
        return None
    return visit((),budget), stats

def restrict(rows, assignment):
    return tuple(tuple(lit for lit in row if abs(lit) not in assignment)
                 for row in rows
                 if not any(assignment.get(abs(lit)) == (lit>0)
                            for lit in row if abs(lit) in assignment))

def truth(rows):
    variables = sorted({abs(lit) for row in rows for lit in row})
    return any(all(any(values[abs(lit)] == (lit>0) for lit in row) for row in rows)
               for bits in product((False,True),repeat=len(variables))
               for values in [dict(zip(variables,bits))])

def main():
    clauses = [tuple(sign*v for sign,v in zip(signs,(1,2,3)))
               for signs in product((1,-1),repeat=3)]
    cases = 0
    for mask in range(256):
        rows = tuple(row for i,row in enumerate(clauses) if mask>>i&1)
        for budget in range(4):
            key, stats = find_hit(rows,budget)
            expected = not rows or budget>=1
            assert (key is not None)==expected
            assert stats["calls"] <= (3**(budget+1)-1)//2
            if key is not None:
                residuals = [restrict(rows,dict(zip(key,bits)))
                             for bits in product((False,True),repeat=len(key))]
                assert all(all(len(row)<=2 for row in residual) for residual in residuals)
                assert any(map(truth,residuals)) == truth(rows)
            cases += 1
    failed = []
    for h in range(6):
        rows = tuple(tuple(range(3*i+1,3*i+4)) for i in range(h+1))
        key, stats = find_hit(rows,h)
        assert key is None and stats["calls"] == (3**(h+1)-1)//2
        # A failed search can occur on a SAT input.
        assert truth(rows)
        failed.append(dict(budget=h,**stats))
    # Direct prefix-code and event-overlap audit for a cached decision.
    cache = []
    for repetitions in (1,2,8,64):
        events = [{0} for _ in range(repetitions)]
        rho = max(sum(t in event for event in events) for t in {0})
        assert rho == repetitions
        cache.append(dict(obligations=repetitions,entropy_sum=repetitions,
                          b=1,framing=0,rho=rho,time_floor=repetitions/rho))
    return dict(status="COMPUTATIONAL",exhaustive_cases=cases,
                failed_searches=failed,cache_overlap=cache,
                timing_claim="No Turing-machine timing or Kolmogorov complexity measured.")

if __name__=="__main__":
    print(json.dumps(main(),indent=2))
