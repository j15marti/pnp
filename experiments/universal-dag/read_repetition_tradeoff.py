from functools import lru_cache
from itertools import permutations

# READ-REPETITION-Q4-7
# Greedy (1,+k) upper-bound curve for the Q4 edge-cover predicate.
# A chosen reread set K may be queried at both endpoints. Every other edge,
# once queried, is remembered in the DAG state and never queried again.

edges=[]
idx={}
for v in range(16):
    for d in range(4):
        w=v^(1<<d)
        if v<w:
            idx[(v,w)] = len(edges)
            edges.append((v,w))

inc=[[None]*4 for _ in range(16)]
for v in range(16):
    for d in range(4):
        a,b=sorted((v,v^(1<<d)))
        inc[v][d]=idx[(a,b)]

# Local orders inherited from READ-TWICE-Q4-6.
local_orders=[
(0,1,3,2),(2,3,1,0),(0,3,1,2),(3,1,2,0),
(2,3,1,0),(0,1,3,2),(2,1,3,0),(0,2,1,3),
(3,2,0,1),(1,0,2,3),(1,2,0,3),(0,3,1,2),
(0,2,3,1),(3,2,0,1),(1,3,0,2),(2,1,3,0)
]
vertex_order=list(range(16))

def bp_node_count(reread_set):
    pos={v:i for i,v in enumerate(vertex_order)}
    later=[max(pos[u],pos[v]) for (u,v) in edges]
    node_ids={}

    @lru_cache(None)
    def solve(t,j,m0,m1):
        if t>=16:
            return 1
        v=vertex_order[t]
        while j<4:
            e=inc[v][local_orders[v][j]]
            bit=1<<e
            if m1 & bit:
                drop=0
                for ee in range(32):
                    if later[ee]==t:
                        drop |= 1<<ee
                return solve(t+1,0,m0 & ~drop,m1 & ~drop)
            if m0 & bit:
                j+=1
                continue

            # Query e.
            # If e is reread-enabled we intentionally forget the first result;
            # otherwise retain it until the later endpoint.
            z0,z1=m0,m1
            if e not in reread_set and later[e]>t:
                z0 |= bit
            c0=solve(t,j+1,z0,z1)

            o0,o1=m0,m1
            if e not in reread_set and later[e]>t:
                o1 |= bit
            drop=0
            for ee in range(32):
                if later[ee]==t:
                    drop |= 1<<ee
            c1=solve(t+1,0,o0 & ~drop,o1 & ~drop)

            key=(e,c0,c1)
            if key not in node_ids:
                node_ids[key]=len(node_ids)+2
            return node_ids[key]
        return 0

    solve(0,0,0,0)
    return len(node_ids)

def greedy_curve():
    K=set()
    rows=[]
    for k in range(33):
        rows.append((k,bp_node_count(K),tuple(sorted(K))))
        if k==32:
            break
        candidates=[]
        for e in range(32):
            if e not in K:
                candidates.append((bp_node_count(K|{e}),e))
        candidates.sort()
        K.add(candidates[0][1])
    return rows

if __name__=="__main__":
    print("k,nodes,reread_edges")
    for k,nodes,K in greedy_curve():
        print(k,nodes,";".join(map(str,K)),sep=",")
