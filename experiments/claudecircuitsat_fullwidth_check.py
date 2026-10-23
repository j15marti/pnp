"""Check: CNF over n vars whose possible clauses are all width-k clauses, presence bits as inputs.
SAT(p)=1 iff some assignment a satisfies every present clause. For k=n each a falsifies exactly one clause,
so SAT = NAND of all 2^n presence bits. Brute-force verify n<=3 (<=25 s)."""
import itertools
for n in (1,2,3):
    k=n
    clauses=[(vs,sg) for vs in itertools.combinations(range(n),k) for sg in itertools.product((0,1),repeat=k)]
    m=len(clauses); ok=True
    for p in range(1<<m):
        present=[clauses[i] for i in range(m) if p>>i&1]
        sat=any(all(any(a[v]==s for v,s in zip(vs,sg)) for vs,sg in present) for a in itertools.product((0,1),repeat=n))
        nand=0 if p==(1<<m)-1 else 1
        ok&=(sat==bool(nand))
    print(n,m,ok)
