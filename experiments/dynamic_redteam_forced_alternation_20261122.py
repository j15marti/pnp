"""Audit forced alternating paths against pinned syndrome solver and enumeration."""
from itertools import combinations, product
import json
from dynamic_discovery_syndrome_trellis_20261122 import solve, oracle

def fast(top, bottom, rows):
    if any(a == b == "A" for a,b in zip(top,bottom)):
        return "UNKNOWN"
    t = len(top)
    if t % 2:
        return False
    for start in (0,1):
        if any(a != b and (start ^ (i % 2)) != 1
               for i,(a,b) in enumerate(zip(top,bottom))):
            continue
        if all(sum(start ^ (i % 2) for i in row) % 2 == 0 for row in rows):
            return True
    return False

def run():
    counts = {"cases":0,"SAT":0,"UNSAT":0}
    t = 6
    pool = [()] + [(r,) for r in combinations(range(t),3)]
    for links in product(("CC","AC","CA"),repeat=t):
        a = "".join(x[0] for x in links)
        b = "".join(x[1] for x in links)
        for rows in pool:
            answer = fast(a,b,rows)
            assert answer == oracle(a,b,rows) == solve(a,b,rows)[0]
            counts["cases"] += 1
            counts["SAT" if answer else "UNSAT"] += 1
    controls=[]
    for q in (1,2,4,8):
        t=6*q
        rows=[(2*j,2*q+2*j,4*q+2*j) for j in range(q)]
        for p in (0,1):
            a="C"*t
            b="C"*p+"A"+"C"*(t-p-1)
            answer,width,peak=solve(a,b,rows)
            assert fast(a,b,rows)==answer==(p==1)
            assert width==q
            controls.append(dict(q=q,p=p,SAT=answer,lambda_max=width,peak=peak))
    assert fast("AAA","AAA",[])=="UNKNOWN"
    assert fast("CCC","CCC",[]) is False
    print(json.dumps(dict(exhaustive=counts,controls=controls,
                         scope="projected semantics; no compiled tape simulation",
                         seed=None),indent=2))

if __name__ == "__main__":
    run()
