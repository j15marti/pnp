"""SEPARATOR-SCALING81: greedy min-fill treewidth upper bound and BFS-balanced-cut
estimate on primal graphs of random 3-CNF (ratio 4.2) and random 3-regular graphs.
Pure stdlib. Each n runs in seconds; chunk by n via argv."""
import random, sys, json, time
def primal_3cnf(n, m, rng):
    adj=[set() for _ in range(n)]
    for _ in range(m):
        c=rng.sample(range(n),3)
        for a in c:
            for b in c:
                if a!=b: adj[a].add(b)
    return adj
def reg3(n, rng):
    while True:
        pts=[v for v in range(n) for _ in range(3)]; rng.shuffle(pts)
        adj=[set() for _ in range(n)]; ok=True
        for i in range(0,len(pts),2):
            a,b=pts[i],pts[i+1]
            if a==b or b in adj[a]: ok=False;break
            adj[a].add(b);adj[b].add(a)
        if ok: return adj
def mindeg_width(adj):
    g=[set(s) for s in adj]; alive=set(range(len(g))); w=0
    while alive:
        v=min(alive,key=lambda x:len(g[x])); nb=g[v]; w=max(w,len(nb))
        for a in nb:
            g[a]|=nb; g[a].discard(a); g[a].discard(v)
        alive.remove(v); g[v]=set()
    return w
def balanced_sep(adj, rng):
    # BFS layering from random roots; smallest layer whose removal leaves every component <= 2n/3
    n=len(adj); best=n
    for _ in range(5):
        r=rng.randrange(n); dist={r:0}; q=[r]; layers=[[r]]
        for u in q:
            for w in adj[u]:
                if w not in dist: dist[w]=dist[u]+1; q.append(w)
                if dist[w]==len(layers): layers.append([])
                if w in dist and w not in layers[dist[w]]: layers[dist[w]].append(w)
        for L in layers:
            S=set(L); seen=set(S); mx=0
            for s in range(n):
                if s in seen: continue
                st=[s]; seen.add(s); c=0
                while st:
                    u=st.pop(); c+=1
                    for w in adj[u]:
                        if w not in seen: seen.add(w); st.append(w)
                mx=max(mx,c)
            if mx<=2*n/3: best=min(best,len(S))
    return best
if __name__=="__main__":
    out=[]
    for n in map(int,sys.argv[1:]):
        rng=random.Random(81*n); t=time.time()
        a=primal_3cnf(n,int(4.2*n),rng); b=reg3(n,rng)
        out.append(dict(n=n,cnf_tw_ub=mindeg_width(a),cnf_sep_ub=balanced_sep(a,rng),
                        reg3_tw_ub=mindeg_width(b),reg3_sep_ub=balanced_sep(b,rng),sec=round(time.time()-t,1)))
        print(out[-1],flush=True)
    json.dump(out,open("research/experiments/separator_scaling81_%s.json"%"_".join(sys.argv[1:]),"w"))
