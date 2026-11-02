# Exact enumeration: number of distinct functions on n inputs computable by a
# fan-in-2 circuit over the full basis B2 with <= s gates (each gate = one of 16
# binary truth tables; trivial ones included). Wires = 2*gates. Runtime < 30s.
import sys, itertools, json
n=int(sys.argv[1]); smax=int(sys.argv[2])
N=1<<n; FULL=(1<<N)-1
inputs=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
def gate(t,x,y):
    r=0
    for k in range(4):
        if (t>>k)&1:
            xs = x if (k&1) else FULL^x
            ys = y if (k&2) else FULL^y
            r |= xs&ys
    return r
seen=[set() for _ in range(smax+1)]  # functions with exactly-first-found size
best={}
for f in inputs+[0,FULL]: best[f]=0
def dfs(fs,s):
    if s>0:
        f=fs[-1]
        if f not in best or best[f]>s: best[f]=s
    if s==smax: return
    k=len(fs)
    for i in range(k):
        for j in range(i+1,k):
            for t in range(1,15):
                dfs(fs+[gate(t,fs[i],fs[j])],s+1)
dfs(inputs,0)
cnt={}
for f,s in best.items(): cnt[s]=cnt.get(s,0)+1
# unique-SAT functions (exactly one satisfying assignment)
uniq={s:0 for s in range(smax+1)}
for f,s in best.items():
    if bin(f).count('1')==1: uniq[s]+=1
print(json.dumps({"n":n,"smax":smax,"funcs_by_min_size":cnt,"unique_sat_by_size":uniq,"total_funcs_found":len(best),"of":1<<N}))
