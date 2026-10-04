from functools import lru_cache
from collections import Counter

edges=[]; idx={}
for v in range(16):
    for d in range(4):
        w=v^(1<<d)
        if v<w:
            idx[(v,w)] = len(edges); edges.append((v,w))
incdim=[[None]*4 for _ in range(16)]
for v in range(16):
    for d in range(4):
        a,b=sorted((v,v^(1<<d))); incdim[v][d]=idx[(a,b)]

# Seed 20261004 local-search result. Each row orders the four dimensions at one Q4 vertex.
ord_dims=[
[1,3,0,2],[2,0,3,1],[2,0,3,1],[1,3,0,2],
[2,3,1,0],[0,3,1,2],[0,1,3,2],[2,1,3,0],
[2,0,3,1],[1,3,0,2],[1,3,0,2],[2,0,3,1],
[0,1,3,2],[2,1,3,0],[2,3,1,0],[0,3,1,2]
]
qseq=[[incdim[v][d] for d in ord_dims[v]] for v in range(16)]
other={(e,u):v for e,(u,v) in enumerate(edges)}
other.update({(e,v):u for e,(u,v) in enumerate(edges)})

def exact_max(metric):
    """Exact maximum over all consistent 32-bit inputs for this fixed 64-node BP."""
    @lru_cache(None)
    def stage(v,mem_t):
        if v==16: return 0
        @lru_cache(None)
        def step(j,mem_t2):
            if j==4: return 0
            mem=dict(mem_t2); e=qseq[v][j]; o=other[(e,v)]
            previous=e in mem
            vals=(mem[e],) if previous else (0,1)
            best=0
            for val in vals:
                m=mem.copy()
                if o>v: m[e]=val
                add=1 if metric=='queries' else (1 if previous else 0)
                if val:
                    nm={ee:b for ee,b in m.items() if max(edges[ee])>v}
                    z=add+stage(v+1,tuple(sorted(nm.items())))
                else:
                    if o<v: m.pop(e,None)
                    z=add+step(j+1,tuple(sorted(m.items())))
                best=max(best,z)
            return best
        return step(0,mem_t)
    return stage(0,tuple())

# Exact perfect-matching hostile subfamily.
adj=[[] for _ in range(16)]
for e,(u,v) in enumerate(edges):
    adj[u].append((v,e)); adj[v].append((u,e))
PM=[]
def enum_pm(rem,mask):
    if not rem: PM.append(mask); return
    u=min(rem)
    for v,e in adj[u]:
        if v in rem: enum_pm(rem-{u,v},mask|(1<<e))
enum_pm(set(range(16)),0)

def eval_bp(mask):
    reads=Counter(); q=0
    for v in range(16):
        covered=False
        for e in qseq[v]:
            q+=1; reads[e]+=1
            if (mask>>e)&1:
                covered=True; break
        if not covered:
            return False,q,sum(c>1 for c in reads.values())
    return True,q,sum(c>1 for c in reads.values())

pm=[eval_bp(m) for m in PM]
assert all(x[0] for x in pm)
print('query_nodes=64')
print('syntactic_read_twice=1')
print('exact_full_domain_max_queries=',exact_max('queries'),sep='')
print('exact_full_domain_max_repeated_variables=',exact_max('repeats'),sep='')
print('perfect_matchings=',len(PM),sep='')
print('pm_query_min=',min(x[1] for x in pm),sep='')
print('pm_query_max=',max(x[1] for x in pm),sep='')
print('pm_repeat_min=',min(x[2] for x in pm),sep='')
print('pm_repeat_avg=',sum(x[2] for x in pm)/len(pm),sep='')
print('pm_repeat_max=',max(x[2] for x in pm),sep='')
print('architecture_repeat_lower_bound=8')
