#!/usr/bin/env python3
"""Standalone exact reproduction of the paired triangle-free Gram controls.
Python 3.10+, standard library only. No numerical SDP, SAT oracle or external data.
Run: python minirepro.py > minirepro_results.json
"""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

NO_EDGES = [(0,1),(0,4),(0,6),(0,9),(1,2),(1,5),(1,7),(2,3),
 (2,6),(2,8),(3,4),(3,7),(3,9),(4,5),(4,8),(5,10),(5,11),
 (6,10),(6,11),(7,8),(7,11),(8,10),(9,10),(9,11)]


def check_graph(edges: list[tuple[int,int]], p: int = 12) -> dict:
    checks = 0
    def check(ok: bool) -> None:
        nonlocal checks
        checks += 1
        if not ok:
            raise AssertionError(f"Exact check {checks} failed")
    a = [[0]*p for _ in range(p)]
    for u,v in edges:
        check(0 <= u < v < p and a[u][v] == 0)
        a[u][v] = a[v][u] = 1
    deg = [sum(row) for row in a]
    check(all(d <= 4 for d in deg))
    check(all(not (a[u][v] and a[v][w] and a[u][w])
              for u in range(p) for v in range(u+1,p) for w in range(v+1,p)))
    b = [[a[u][v] - 2*(u == v) for v in range(p)] for u in range(p)]
    x8 = [[sum(b[u][j]*b[v][j] for j in range(p))
            + (4-deg[u])*(u == v) for v in range(p)] for u in range(p)]
    for u in range(p):
        check(x8[u][u] == 8)
        for v in range(p):
            if a[u][v]: check(x8[u][v] == -4)
        check(sum(deg[v] for v in range(p) if a[u][v])-4*deg[u] <= 0)
    size = 1+3*p
    # All entries below are integers representing 72 times the moment matrix.
    target = [[0]*size for _ in range(size)]
    target[0][0] = 72
    for i in range(1,size): target[0][i] = target[i][0] = 24
    for u in range(p):
        for v in range(p):
            for c in range(3):
                for d in range(3):
                    target[1+3*u+c][1+3*v+d] = 8 + x8[u][v]*(3*(c==d)-1)
    factors = [(8,[3]+[1]*(3*p))]
    vertex_factors = [(1,[b[u][j] for u in range(p)]) for j in range(p)]
    for u in range(p):
        if deg[u] < 4:
            vertex_factors.append((4-deg[u],[int(u==v) for v in range(p)]))
    for weight, vec in vertex_factors:
        for c,d in [(0,1),(0,2),(1,2)]:
            row = [0]*size
            for u in range(p):
                row[1+3*u+c] = vec[u]; row[1+3*u+d] = -vec[u]
            factors.append((weight,row))
    check(all(weight > 0 for weight,_ in factors))
    for i in range(size):
        for j in range(size):
            check(target[i][j] == sum(w*row[i]*row[j] for w,row in factors))
    for u in range(p):
        for j in range(size):
            check(sum(target[1+3*u+c][j] for c in range(3)) == target[0][j])
        for c in range(3):
            check(target[1+3*u+c][1+3*u+c] == 24)
            for d in range(3):
                if c != d: check(target[1+3*u+c][1+3*u+d] == 0)
        for v in range(p):
            if a[u][v]:
                for c in range(3): check(target[1+3*u+c][1+3*v+c] == 0)
    # Count genuine colorings independently from the Gram construction.
    colors = [-1]*p
    def count() -> int:
        todo = [v for v in range(p) if colors[v] < 0]
        if not todo: return 1
        u = max(todo, key=lambda v: (len({colors[w] for w in range(p)
                         if a[v][w] and colors[w] >= 0}),deg[v],-v))
        forbidden = {colors[w] for w in range(p) if a[u][w] and colors[w] >= 0}
        total = 0
        for c in range(3):
            if c not in forbidden:
                colors[u] = c; total += count()
        colors[u] = -1
        return total
    return {"p":p,"e":len(edges),"colorings":count(),"checks":checks,
            "moment_dimension":size,"positive_factor_rows":len(factors),"edges":edges}


def main() -> None:
    yes = sorted((set(NO_EDGES)-{(0,1),(2,6)})|{(0,2),(1,6)})
    no_result = check_graph(NO_EDGES)
    yes_result = check_graph(yes)
    assert no_result["colorings"] == 0 and yes_result["colorings"] == 108
    print(json.dumps({"status":"COMPUTATIONAL exact finite controls; P versus NP OPEN",
          "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          "unsat":no_result,"sat":yes_result,
          "checks":no_result["checks"]+yes_result["checks"]+1},indent=2))

if __name__ == "__main__": main()
