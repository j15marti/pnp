"""CSAT ladder (pure Python). f_{n,s}(code)=1 iff encoded AND/NOT circuit (n inputs, s gates) is satisfiable.
Gate g reads nodes a,b<n+g (field mod n+g) with negation bits; output = last gate.
Reports N code bits, #sat codes, essential bits, max sensitivity. One (n,s) per invocation, N<=14 (<30s)."""
import sys, json
def run(n,s):
    fields=[(max(1,(n+g-1).bit_length()),n+g) for g in range(s)]
    N=sum(2*w+2 for w,_ in fields); full=(1<<(1<<n))-1
    base=[sum(1<<x for x in range(1<<n) if (x>>i)&1) for i in range(n)]
    f=bytearray(1<<N)
    for c in range(1<<N):
        tt=list(base); pos=0
        for w,m in fields:
            a=((c>>pos)&((1<<w)-1))%m; pos+=w
            b=((c>>pos)&((1<<w)-1))%m; pos+=w
            ta=tt[a]^(full if (c>>pos)&1 else 0); pos+=1
            tb=tt[b]^(full if (c>>pos)&1 else 0); pos+=1
            tt.append(ta&tb)
        f[c]=1 if tt[-1] else 0
    ess=0; sens=[0]*(1<<N)
    for i in range(N):
        d=False
        for c in range(1<<N):
            if f[c]!=f[c^(1<<i)]: d=True; sens[c]+=1
        ess+=d
    return dict(n=n,s=s,N=N,sat=sum(f),total=1<<N,essential_bits=ess,max_sens=max(sens),lb_gates_fanin2=max(0,ess-1))
if __name__=="__main__": print(json.dumps(run(int(sys.argv[1]),int(sys.argv[2]))))
