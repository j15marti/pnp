"""Wire-sensitivity ladder for Circuit-SAT (fan-in-2 AND/OR, free negation, output = last gate).
s(C) = # wires whose re-sourcing can flip SAT status. Query-model lower bound: any exact decider
reading the wire list must probe >= s(C) wires on C (adversary: each sensitive wire has a flipping rewire).
Reports, per (n,g): max s over all circuits, and whether every wire can be fully sensitive (s=2g)."""
import itertools, json, sys
def sources(n,j): return [(k,neg) for k in range(n+j) for neg in (0,1)]
def evalsat(n,gates):
    for a in range(1<<n):
        v=[(a>>i)&1 for i in range(n)]
        for (op,(s1,n1),(s2,n2)) in gates:
            x=v[s1]^n1; y=v[s2]^n2
            v.append(x&y if op==0 else x|y)
        if v[-1]: return True
    return False
def circuits(n,g):
    def rec(j,acc):
        if j==g: yield tuple(acc); return
        S=sources(n,j)
        for op in (0,1):
            for a in S:
                for b in S:
                    if a<=b: yield from rec(j+1,acc+[(op,a,b)])
    yield from rec(0,[])
def sens(n,gates):
    base=evalsat(n,gates); s=0
    for j in range(len(gates)):
        for side in (1,2):
            ok=False
            for src in sources(n,j):
                gl=list(gates); t=list(gl[j]); t[side]=src; gl[j]=tuple(t)
                if evalsat(n,gl)!=base: ok=True;break
            s+=ok
    return s
res={}
for n in range(1,4):
    for g in range(1,4 if n<3 else 3):
        best=0;full=0;tot=0
        for C in circuits(n,g):
            tot+=1;s=sens(n,C);best=max(best,s);full+=(s==2*g)
        res[f"n{n}_g{g}"]=dict(circuits=tot,max_sens=best,fully_sensitive=full)
        print(n,g,res[f"n{n}_g{g}"],flush=True)
json.dump(res,open(sys.argv[1],"w"),indent=1)
