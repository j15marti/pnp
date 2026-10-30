"""Exhaustive check (n<=4): min #gates (fan-in<=2, any binary op) of a circuit whose
output depends on all n inputs equals n-1, hence wires = 2(n-1).  Runs in seconds."""
import itertools, json
def tt_ops(): return range(16)
def depends_all(tt, n):
    for i in range(n):
        if all(tt[x]==tt[x^(1<<i)] for x in range(1<<n)): return False
    return True
def search(n, g):
    # wires: list of truth tables (tuples); gates choose two earlier wires + op
    base=[tuple((x>>i)&1 for x in range(1<<n)) for i in range(n)]
    found=False
    def rec(ws,k):
        nonlocal found
        if found: return
        if k==0:
            if depends_all(ws[-1],n): found=True
            return
        for a in range(len(ws)):
            for b in range(a+1,len(ws)):
                for op in range(16):
                    t=tuple((op>>(2*ws[a][x]+ws[b][x]))&1 for x in range(1<<n))
                    rec(ws+[t],k-1)
    rec(base,g); return found
res={}
for n in range(2,5):
    res[n]={"g=n-2":search(n,n-2) if n>2 else None,"g=n-1":search(n,n-1)}
    print(n,res[n])
json.dump(res,open("ladder_check_results.json","w"))
