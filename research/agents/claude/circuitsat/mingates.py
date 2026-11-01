# Exact min #gates (fan-in-2 arbitrary binary gates, B2) for each Boolean function on n vars, by DFS over gate sequences.
import itertools, json, sys
n=int(sys.argv[1]); maxg=int(sys.argv[2])
N=1<<n; M=(1<<N)-1
vars_=[sum(1<<a for a in range(N) if (a>>i)&1) for i in range(n)]
best={}
def gate(op,x,y):  # op 4-bit table over (x,y)
    r=0
    if op&1: r|=~x&~y
    if op&2: r|=x&~y
    if op&4: r|=~x&y
    if op&8: r|=x&y
    return r&M
def dfs(fs,depth,limit):
    for f in fs[n:]:
        pass
    if depth==limit: return
    k=len(fs)
    for i in range(k):
        for j in range(i+1,k):
            for op in range(16):
                g=gate(op,fs[i],fs[j])
                if g in fs: continue
                if g not in best or best[g]>depth+1: best[g]=depth+1
                dfs(fs+[g],depth+1,limit)
for L in range(1,maxg+1):
    dfs(list(vars_),0,L)
for v in vars_: best[v]=0
best[0]=0;best[M]=0
uniq={}
for f,g in best.items():
    if bin(f).count('1')==1: uniq[g]=uniq.get(g,0)+1
byg={}
for f,g in best.items(): byg[g]=byg.get(g,0)+1
print(n,"funcs found",len(best),"of",1<<N,"by gates",sorted(byg.items()),"unique-sat gates",sorted(uniq.items()))
