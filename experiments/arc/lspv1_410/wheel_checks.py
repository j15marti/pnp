"""Odd-wheel Resolution upper bounds and indispensability certificates. Python 3.10+."""
import json
from pathlib import Path
from degree_reduction import structure
from shift_proofs import refute, replay, source
from verify_traces import verify


def wheel(r):
    return [(0,i,[1,2]) for i in range(1,r+1)] + [
        (i,1+i%r,[1,2]) for i in range(1,r+1)]


def run_wheel(r):
    edges = wheel(r)
    high, kept, order, _, _ = structure(r+1, [(u,v,0) for u,v,_ in edges])
    steps, _ = refute(r+1, edges, order=order)
    stats = replay(r+1, edges, steps)
    assert verify(dict(n=r+1, edges=edges, steps=steps)) == stats
    clauses, ids = source(r+1, edges)
    count = 0
    def check(colors, omit):
        # None means leave this vertex's three indicator bits false.
        true = {3*v+c+1 for v,c in enumerate(colors) if c is not None}
        bad = [i for i,clause in enumerate(clauses)
               if all((lit>0) != (abs(lit) in true) for lit in clause)]
        assert bad == [omit]
    # With a deleted spoke or rim-vertex ALO, the remaining rim is a path.
    for i in range(1,r+1):
        start = [2]+[None]*r
        for j in range(1,r):
            start[1+(i-1+j)%r] = j%2
        check(start,ids['alo',i])
        count += 1
        start[i] = 2
        for c in range(3):
            check([(x+c-2)%3 for x in start],ids['ban',i-1,c,c])
            count += 1
    # Delete the hub ALO and properly 3-color the odd rim.
    check([None]+[i%2 for i in range(r-1)]+[2],ids['alo',0])
    count += 1
    for i in range(1,r+1):
        start = [2]+[None]*r
        # Path begins immediately after the removed rim edge; endpoints match.
        for j in range(r):
            start[1+(i+j)%r] = j%2
        for c in range(3):
            check([(x+c)%3 for x in start],ids['ban',r+i-1,c,c])
            count += 1
    assert count == 7*r+1 and len(steps) >= count-1
    return dict(rim=r, vertices=r+1, residual_high=len(high), retained=len(kept),
                indispensable_source_clauses=count, binary_resolution_lower_bound=count-1,
                binary_resolution_steps=len(steps), maximum_clause_width=stats['maximum_width'])


if __name__ == '__main__':
    sizes = [3,5,7,15,31,63,127,255]
    rows = [run_wheel(r) for r in sizes]
    even = [4,6,8,16,32]
    for r in even:
        coloring = [2]+[i%2 for i in range(r)]
        assert all(coloring[u] != coloring[v] for u,v,_ in wheel(r))
        assert refute(r+1, wheel(r))[0] is None
    data = {'odd_wheels':rows,'even_wheel_sat_controls':even}
    Path(__file__).with_name('wheel_results.json').write_text(json.dumps(data,indent=2)+'\n')
    print(rows[-1])
