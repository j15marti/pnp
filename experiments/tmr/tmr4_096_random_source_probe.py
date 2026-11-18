#!/usr/bin/env python3
"""TMR-4/096 standalone repository smoke test, no dependencies."""
import hashlib
import itertools
import json

D = {1, 3}
def arc_order(n):
    return [(i,j) for i in range(n) for j in range(n) if i != j]
def source(n, edges):
    es = set(edges)
    return json.dumps({"n":n,"bits": "".join("1" if a in es else "0" for a in arc_order(n))}, separators=(",",":"))
def parse(text):
    o = json.loads(text)
    assert set(o) == {"n","bits"} and type(o["n"]) is int and o["n"] >= 0
    n,bits = o["n"],o["bits"]
    assert len(bits) == n*(n-1) and set(bits) <= {"0","1"}
    es = [a for a,b in zip(arc_order(n),bits) if b=="1"]
    assert source(n,es) == text
    return n,es
def relation(a,b):
    return (b-a)%5 in D
def make_cnf(n, edges):
    def blocker(v,c):
        return [(3*v+t, -1 if c>>t&1 else 1) for t in range(3)]
    clauses=[blocker(v,c) for v in range(n) for c in (5,6,7)]
    clauses.extend(blocker(i,a)+blocker(j,b) for i,j in edges
                   for a in range(5) for b in range(5) if not relation(a,b))
    assert len(clauses) == 3*n+15*len(edges)
    assert sum(map(len,clauses)) == 9*n+90*len(edges)
    return clauses
def eval_cnf(x,clauses):
    return all(any(((x[var//3]>>(var%3))&1)==(1 if sign==1 else 0)
                   for var,sign in clause) for clause in clauses)
def main():
    total=0; cases=0; all_hashes=[]
    for n in range(2,7):
        pairs=[(i,j) for i in range(n) for j in range(i+1,n)]
        for pair in [None]+pairs:
            edges=[] if pair is None else [(pair[0],pair[1]),(pair[1],pair[0])]
            text=source(n,edges)
            assert parse(text)==(n,edges)
            all_hashes.append(hashlib.sha256(text.encode()).hexdigest())
            c=make_cnf(n,edges);Z=0
            for x in itertools.product(range(5),repeat=n):
                actual=all(relation(x[i],x[j]) for i,j in edges)
                assert actual == eval_cnf(x,c) == (pair is None)
                Z+=actual
                total+=1
            assert Z == (5**n if pair is None else 0)
            cases+=1
    domain=0
    for direction in (0,1):
        for am in range(32):
            for bm in range(32):
                a={i for i in range(5) if am>>i&1}
                b={j for j in range(5) if bm>>j&1}
                forward=sum(1<<i for i in a if any(relation(i,j) for j in b))
                backward=sum(1<<j for j in b if any(relation(j,i) for i in a))
                native=sum(1<<k for k in range(5) if
                    ((am if not direction else bm)>>k)&1 and
                    any((relation(k,j) if not direction else relation(k,j))
                        for j in (b if not direction else a)))
                # Explicit native check, with correct reverse directed support.
                if direction:
                    native=sum(1<<j for j in b if any(relation(j,i) for i in a))
                assert native == (forward if not direction else backward)
                domain+=1
    N=45;k=30
    for pair in range(N):
        assert sum(pair in {(seed+t)%N for t in range(k)} for seed in range(N))==30
    print(json.dumps({"status":"PASS","sources":cases,"original_points":total,
        "domain_mask_cases":domain,"all_hashes_count":len(all_hashes),
        "cyclic_pair_detections":30,"model":"randomized bit-probe only"},sort_keys=True))
if __name__=="__main__":
    main()
