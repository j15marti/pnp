"""Essential-bit ladder for CSAT_{n,s}. Pure Python; each (n,s) call <30s for N<=16.
Encoding: gate j (0..s-1) = AND(lit_a, lit_b); a,b in [0,n+j) with ceil(log2(n+j)) bits + 1 neg bit each.
Output = last gate. Out-of-range index => code rejected. F(code)=1 iff exists x: C_code(x)=1."""
import json, sys, math
def run(n,s):
    widths=[max(0,math.ceil(math.log2(n+j))) for j in range(s)]
    N=sum(2*(w+1) for w in widths)
    M=(1<<(1<<n))-1
    xs=[sum(1<<x for x in range(1<<n) if (x>>i)&1) for i in range(n)]
    F=bytearray(1<<N)
    for code in range(1<<N):
        pos=0; nodes=list(xs); ok=True
        for j in range(s):
            w=widths[j]; lits=[]
            for _ in range(2):
                idx=(code>>pos)&((1<<w)-1); pos+=w
                neg=(code>>pos)&1; pos+=1
                if idx>=n+j: ok=False;break
                lits.append(nodes[idx]^(M if neg else 0))
            if not ok:break
            nodes.append(lits[0]&lits[1])
        if ok and nodes[-1]: F[code]=1
    ess=[b for b in range(N) if any(F[c]!=F[c^(1<<b)] for c in range(1<<N))]
    return dict(n=n,s=s,N=N,essential=len(ess),satisfiable_codes=sum(F),inessential=[b for b in range(N) if b not in ess])
if __name__=="__main__":
    print(json.dumps([run(int(a),int(b)) for a,b in zip(sys.argv[1::2],sys.argv[2::2])]))
