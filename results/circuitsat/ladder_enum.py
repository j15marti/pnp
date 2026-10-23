# Exhaustive minimum fan-in-2 circuit size (all 16 binary gates, free constants/negation via gate table)
# for n<=3 and minimum formula leaf-count for n<=4.  Each invocation <30s.
import sys, json, itertools
n=int(sys.argv[1]); mode=sys.argv[2]   # mode: circ | form
N=1<<n; M=(1<<N)-1
def var(i):
    t=0
    for x in range(N):
        if (x>>i)&1: t|=1<<x
    return t
ins=[var(i) for i in range(n)]
def ops(a,b):
    # all 16 binary functions of (a,b) as truth tables
    na,nb=M^a,M^b
    s={0,M,a,na,b,nb}
    for p in (a,na):
        for q in (b,nb):
            s.add(p&q); s.add(M^(p&q))
    s.add(a^b); s.add(M^(a^b))
    return s
def essential(f):
    k=0
    for i in range(n):
        v=0
        for x in range(N):
            if ((f>>x)&1)!=((f>>(x^(1<<i)))&1): v=1;break
        k+=v
    return k
if mode=="form":
    INF=99
    L={0:0,M:0}
    for i in range(n): L[ins[i]]=1; L[M^ins[i]]=1
    ch=True
    while ch:
        ch=False
        items=list(L.items())
        for a,la in items:
            for b,lb in items:
                for c in ops(a,b):
                    if L.get(c,INF)>la+lb:
                        L[c]=la+lb; ch=True
    # formula size = leaves; gates=leaves-1
    out={}
    for f,l in L.items():
        if essential(f)==n: out[f]=l
    from collections import Counter
    print(json.dumps({"n":n,"mode":"form","full-essential-count":len(out),"leafcount_hist":sorted(Counter(out.values()).items()),"max_leaves":max(L.values())}))
else:
    # BFS over circuits: level-by-level DFS with sorted gate set
    best={0:0,M:0}
    for i in range(n): best[ins[i]]=0; best[M^ins[i]]=0
    def dfs(nodes,g,limit):
        for f in nodes:
            if best.get(f,99)>g: best[f]=g
        if g==limit: return
        seen=set()
        for i in range(len(nodes)):
            for j in range(i+1,len(nodes)):
                for c in ops(nodes[i],nodes[j]):
                    if c in nodes or c in seen: continue
                    seen.add(c)
                    dfs(nodes+[c],g+1,limit)
    # iterative deepening to limit; nodes seeded with inputs
    limit=int(sys.argv[3])
    dfs(list(ins),0,limit)
    from collections import Counter
    out={f:g for f,g in best.items() if essential(f)==n}
    print(json.dumps({"n":n,"mode":"circ","limit":limit,"full-essential-count":len(out),"gate_hist":sorted(Counter(out.values()).items()),"all_functions_found":len(best)}))
