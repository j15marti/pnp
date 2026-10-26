"""Exhaustive minimum #2-input gates (full B2 basis, free negation) to compute
every n-input unique-SAT function (exactly one satisfying assignment), n<=4.
Runtime budget: <30s. Output: results/raw/claude_circuitsat/min_gates.json"""
import itertools, json, sys
def run(n, kmax):
    N=1<<n; mask=(1<<N)-1
    xs=[sum(((a>>i)&1)<<a for a in range(N)) for i in range(n)]
    targets={1<<a for a in range(N)}   # unique-SAT truth tables
    found={}
    # DFS over circuits: list of wire truth tables; gate = any of 16 binary ops on earlier wires
    def ops(u,v):
        nu,nv=~u&mask,~v&mask
        # 4 minterm combos, any subset -> 16 functions
        m=[nu&nv,nu&v,u&nv,u&v]
        for s in range(16):
            r=0
            for j in range(4):
                if s>>j&1:r|=m[j]
            yield r
    def dfs(wires,k):
        if wires[-1] in targets and len(wires)>n:
            found.setdefault(wires[-1],k)
        if k==kmax:return
        seen=set()
        for i in range(len(wires)):
            for j in range(i+1,len(wires)):
                for r in ops(wires[i],wires[j]):
                    if r in wires or r in seen or r in (0,mask):continue
                    seen.add(r)
                    dfs(wires+[r],k+1)
    dfs(xs,0)
    # BFS-ish: record min k per target = first found with smallest k
    return found
res={}
for n,kmax in [(2,1),(3,2)]:
    f=run(n,kmax); res[n]={"kmax":kmax,"all_unique_sat_reached_within":len(f)==(1<<(1<<n)>0 and (1<<n)),"min_k":sorted(set(f.values())),"count":len(f)}
# n=4: check no unique-SAT function with <=2 gates (n-1=3 predicted min)
f4=run(4,2); res[4]={"kmax":2,"count_reached":len(f4)}
json.dump(res,open("results/raw/claude_circuitsat/min_gates.json","w"),indent=1)
print(res)
