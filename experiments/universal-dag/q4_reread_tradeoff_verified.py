from functools import lru_cache
import csv

# Q4 edges, vertex order 0..15.
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

vertex_order=tuple(range(16)); pos={v:i for i,v in enumerate(vertex_order)}
# Fixed simple local order: ascending Q4 edge id.
local_edges={v:tuple(sorted(incdim[v])) for v in range(16)}

def compile_nodes(forget_set):
    """Exact node count for the declared endpoint-scan STORE/RECOMP BP.

    For e outside forget_set, a first query result is retained until the other endpoint,
    so e is never reread. For e in forget_set, the result is discarded and a second
    endpoint query is permitted. Hence only forget_set variables may repeat, each at most twice.
    """
    R=frozenset(forget_set)
    nodes={}

    @lru_cache(None)
    def stage(i, mem_tuple):
        if i==16: return -2
        v=vertex_order[i]; mem=dict(mem_tuple)
        known={e:mem[e] for e in local_edges[v] if e in mem}
        if any(known.values()):
            nm={}
            for e,val in mem.items():
                u,w=edges[e]
                if max(pos[u],pos[w])>i: nm[e]=val
            return stage(i+1,tuple(sorted(nm.items())))
        cand=tuple(e for e in local_edges[v] if e not in known)
        return query(i,tuple(sorted(mem.items())),cand,0)

    @lru_cache(None)
    def query(i, mem_tuple, cand, j):
        if j==len(cand): return -1
        v=vertex_order[i]; mem=dict(mem_tuple); e=cand[j]
        u,w=edges[e]; other=w if u==v else u

        m0=mem.copy()
        if e not in R and pos[other]>i: m0[e]=0
        lo=query(i,tuple(sorted(m0.items())),cand,j+1)

        m1=mem.copy()
        if e not in R and pos[other]>i: m1[e]=1
        nm={}
        for ee,val in m1.items():
            a,b=edges[ee]
            if max(pos[a],pos[b])>i: nm[ee]=val
        hi=stage(i+1,tuple(sorted(nm.items())))

        if lo==hi: return lo
        key=(e,lo,hi)
        if key not in nodes: nodes[key]=len(nodes)
        return nodes[key]

    stage(0,tuple())
    return len(nodes)

# Greedy valid upper-bound curve.
R=set(); rows=[]
current=compile_nodes(R); best_le=current
rows.append((0,current,best_le,-1))
for k in range(1,33):
    best=None
    for e in range(32):
        if e in R: continue
        s=compile_nodes(R|{e})
        if best is None or (s,e)<best: best=(s,e)
    current,e=best; R.add(e); best_le=min(best_le,current)
    rows.append((k,current,best_le,e))

out='results/summaries/2026-10-03_READ_RECOMPUTE_Q4_8.csv'
with open('/tmp/READ_RECOMPUTE_Q4_8.csv','w',newline='') as f:
    w=csv.writer(f)
    w.writerow(['greedy_forget_set_size_k','nodes_for_greedy_exact_set',
                'best_nodes_seen_with_at_most_k','edge_added'])
    w.writerows(rows)

for r in rows: print(*r,sep=',')
