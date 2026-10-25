# Exact min fan-in-2 circuit size over full binary basis B2 (negations free) for all n-var functions, n<=3.
# gates = size; wires = 2*gates. DFS over straight-line programs; each new gate is any of the 16 binary
# functions of two earlier nodes; with free negation only a&b-type (4 sign choices up to complement) and a^b matter.
import itertools, json
def run(n, maxg):
    N=1<<n; full=(1<<N)-1
    base=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
    best={0:0,full:0}
    for b in base: best[b]=0; best[b^full]=0
    def cands(a,b):
        s=set()
        for x in (a,a^full):
            for y in (b,b^full):
                r=x&y; s.add(r); s.add(r^full)
        r=a^b; s.add(r); s.add(r^full)
        return s
    seen=set()
    def dfs(prog,k,limit):
        key=(tuple(sorted(prog)),limit)
        if key in seen: return
        seen.add(key)
        for a,b in itertools.combinations(range(len(prog)),2):
            for r in cands(prog[a],prog[b]):
                if r in prog or (r^full) in prog: continue
                if best.get(r,99)>k+1: best[r]=k+1; best[r^full]=k+1
                if k+1<limit: dfs(prog+[r],k+1,limit)
    for lim in range(1,maxg+1): dfs(list(base),0,lim)
    return best
res={}
for n,mg in ((1,1),(2,3),(3,5)):
    b=run(n,mg); N=1<<n
    cnt={}
    for tt in range(1<<N):
        k=b.get(tt); cnt[str(k)]=cnt.get(str(k),0)+1
    res[n]={"hist_gates":cnt}
    print(n,cnt,flush=True)
json.dump(res,open("ladder_results.json","w"),indent=1)
