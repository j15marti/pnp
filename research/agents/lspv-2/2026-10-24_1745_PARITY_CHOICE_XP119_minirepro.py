#!/usr/bin/env python3
"""PARITY-CHOICE-XP119 compact stdlib reproducer (not the 12,627-check full audit).
Exact source model: negative binary CNF plus indexed affine XOR rows.
"""
import itertools, math, random, json

def valid(n, pairs, rows, rhs, selected):
    s=set(selected)
    return (all(not(a in s and b in s) for a,b in pairs)
            and all(sum(v in s for v in row)%2==bit for row,bit in zip(rows,rhs)))

def group_cert(n,pairs,rows,rhs):
    if not rows or any(b!=1 for b in rhs): return False
    seen=set()
    p=set(pairs)
    for row in rows:
        if not row or seen.intersection(row):return False
        seen.update(row)
        if any((min(a,b),max(a,b)) not in p for a,b in itertools.combinations(row,2)):return False
    return seen==set(range(n))

def adaptive(n,pairs,rows,rhs):
    if valid(n,pairs,rows,rhs,()):return True,(),"zero",1
    if group_cert(n,pairs,rows,rhs):
        tests=0
        for c in itertools.product(*rows):
            tests+=1
            if valid(n,pairs,rows,rhs,c):return True,c,"group",tests
        return False,None,"group",tests
    tests=0
    for j in range(min(len(rows),n)+1):
        for c in itertools.combinations(range(n),j):
            tests+=1
            if valid(n,pairs,rows,rhs,c):return True,c,"sparse",tests
    return False,None,"sparse",tests

def colored(k,g,shift):
    n=k*g
    rows=tuple(tuple(range(i*g,(i+1)*g)) for i in range(k))
    forbidden=set()
    for a in range(n):
        for b in range(a+1,n):
            ia,ib=a//g,b//g
            if ia==ib:forbidden.add((a,b));continue
            ok=(a%g==b%g)
            if shift and (ia,ib)==(0,k-1):ok=(b%g==(a%g+1)%g)
            if not ok:forbidden.add((a,b))
    return n,tuple(sorted(forbidden)),rows,(1,)*k

def brute(n,pairs,rows,rhs):
    return any(valid(n,pairs,rows,rhs,
      tuple(i for i in range(n) if mask>>i&1)) for mask in range(1<<n))

def run():
    results=[]
    for k,g in [(3,2),(3,3),(4,2),(4,3),(5,2),(5,4),(6,4)]:
      for shifted in (False,True):
        n,pairs,rows,rhs=colored(k,g,shifted)
        yes,witness,method,trials=adaptive(n,pairs,rows,rhs)
        assert yes==(not shifted)
        assert method=="group"
        assert yes==(witness is not None)
        if yes:assert valid(n,pairs,rows,rhs,witness)
        if n<=12:assert brute(n,pairs,rows,rhs)==yes
        results.append(dict(k=k,g=g,n=n,negative_pairs=len(pairs),
          rhs=rhs[0],label="SAT" if yes else "UNSAT",method=method,
          candidates=trials,max_group=g**k,max_sparse=sum(math.comb(n,j) for j in range(k+1))))
    rng=random.Random(202610241745)
    controls={"SAT":0,"UNSAT":0}
    for _ in range(100):
        n=rng.randint(3,7);k=rng.randint(0,4)
        pairs=tuple((a,b) for a in range(n) for b in range(a+1,n) if rng.randrange(2)==0)
        rows=tuple(tuple(v for v in range(n) if rng.randrange(3)==0) for _ in range(k))
        rhs=tuple(rng.randrange(2) for _ in range(k))
        yes,sol,_,_=adaptive(n,pairs,rows,rhs)
        assert yes==brute(n,pairs,rows,rhs)
        controls["SAT" if yes else "UNSAT"]+=1
    print(json.dumps(dict(run_id="PARITY-CHOICE-XP119",type="compact",
      large_cases=results,random_controls=controls,errors=0),indent=2))
if __name__=="__main__":run()
