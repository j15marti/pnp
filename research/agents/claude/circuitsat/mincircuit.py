# Exact minimum B2 circuit size for all n<=3 Boolean functions (up to complement).
# Staged: runs in a few seconds. Wires = 2*gates (fan-in 2), output wire +1 not counted.
import sys, itertools, json
n=int(sys.argv[1]) if len(sys.argv)>1 else 3
N=1<<n; FULL=(1<<N)-1
ins=[sum(1<<i for i in range(N) if (i>>j)&1) for j in range(n)]
def norm(f): return FULL^f if f&1 else f
ops=[lambda a,b:a&b, lambda a,b:a&~b&FULL, lambda a,b:~a&b&FULL, lambda a,b:a|b, lambda a,b:a^b]
level={frozenset(ins)}      # sets of available signals (normalized, no constants)
best={0:0}
for f in ins: best[f]=0
for g in range(1,8):
    nxt=set()
    for S in level:
        L=list(S)
        for i in range(len(L)):
            for j in range(i+1,len(L)):
                for op in ops:
                    h=op(L[i],L[j])
                    for hh in (h, FULL^h):   # complement free via gate type choice
                        hn=norm(hh)
                        if hn in S or hn==0: continue
                        if hn not in best: best[hn]=g
                        nxt.add(S|{hn})
    level=nxt
    tot=sum(1 for f in range(N and FULL+1) if f&1==0)
    print("gates",g,"states",len(level),"covered",len(best)-0,file=sys.stderr)
    if len([f for f in range(0,FULL+1,2)])<=len(best)+1: break
dist={}
for f in range(0,FULL+1,2):
    c=best.get(f,0 if f==0 else None)
    dist[c]=dist.get(c,0)+1
print(json.dumps({"n":n,"functions_up_to_complement":FULL//2+1,"gate_count_histogram":dist,"max_gates":max(k for k in dist if k is not None)}))
