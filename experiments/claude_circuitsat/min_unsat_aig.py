"""Minimal locally-nondegenerate UNSAT AIG using all n inputs (runtime << 30s for n<=3).
AIG: nodes 0..n-1 inputs; gate k = AND(lit a, lit b); literal = 2*node+neg.
Nondegenerate: a,b on distinct nodes (no x&x, x&~x), no duplicate gates (structural hashing).
Output = last gate; every gate and input must lie in output cone."""
import itertools, json, sys
def search(n, g):
    N0=n; res=[]
    def rec(gates):
        k=len(gates)
        if k==g:
            yield list(gates); return
        node=N0+k
        for a in range(2*node):
            for b in range(a+1,2*node):
                if a//2==b//2: continue
                if (a,b) in gates: continue
                gates.append((a,b)); yield from rec(gates); gates.pop()
    yield from rec([])
def evalall(n,gates):
    vals=[]
    for x in range(2**n):
        v=[(x>>i)&1 for i in range(n)]
        for a,b in gates:
            v.append((v[a//2]^(a&1)) & (v[b//2]^(b&1)))
        vals.append(v[-1])
    return vals
def cone_ok(n,gates):
    m=n+len(gates); seen={m-1}; st=[m-1]
    while st:
        u=st.pop()
        if u>=n:
            for l in gates[u-n]:
                if l//2 not in seen: seen.add(l//2); st.append(l//2)
    return len(seen)==m
out={}
for n in range(1,4):
    found=None
    for g in range(1,n+2):
        cnt=0
        for gates in search(n,g):
            if not cone_ok(n,gates): continue
            if not any(evalall(n,gates)): cnt+=1
        if cnt:
            found=(g,cnt); break
    out[n]=found; print(n,found)
json.dump(out,open(sys.argv[1],"w"))
