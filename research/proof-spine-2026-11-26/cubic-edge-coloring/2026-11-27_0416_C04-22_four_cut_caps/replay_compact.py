# Independent source-local verification of the three-shore Dot12 refutation.
import hashlib, json, itertools
E=[[12,31],[15,18],[7,27],[9,15],[12,25],[12,16],[8,24],[7,11],[5,25],[17,22],[1,24],[20,23],[1,3],[6,14],[14,17],[22,31],[0,1],[24,30],[10,11],[7,18],[6,30],[4,16],[4,5],[2,21],[8,29],[0,29],[26,31],[23,28],[19,33],[2,25],[3,13],[17,28],[9,20],[10,15],[9,26],[3,32],[19,32],[14,16],[8,13],[13,33],[18,30],[6,23],[10,21],[0,33],[21,27],[5,26],[4,22],[2,20],[11,19],[28,29],[27,32]]
assert hashlib.sha256(json.dumps(E,separators=(',',':')).encode()).hexdigest()=='ed3cf3f5af667f7471a5d1831d95b9c5f6336165b0147a3d359d5dd329a83301'
V=list(range(34)); nodes=0
words=[(0,0,0,0),(0,0,1,1),(0,1,0,1),(0,1,1,0)]
pairs=[((0,1),(2,3)),((0,2),(1,3)),((0,3),(1,2))]
def color(V,E,ports=(),word=()):
    global nodes
    adj={v:[] for v in V}; c={}
    for i,(u,v) in enumerate(E):
        if u==v:return False
        adj[u].append(i);adj[v].append(i)
    for j,(v,x) in enumerate(zip(ports,word),len(E)):
        adj[v].append(j);c[j]=x
    assert all(len(a)==3 for a in adj.values())
    if any(len({c[j] for j in a if j in c})!=sum(j in c for j in a) for a in adj.values()):return False
    A=[set(adj[u]+adj[v])-{i} for i,(u,v) in enumerate(E)]
    def go(left):
        global nodes
        nodes+=1
        if not left:return True
        i=min(left,key=lambda j:(len({0,1,2}-{c[k] for k in A[j] if k in c}),j))
        for x in {0,1,2}-{c[k] for k in A[i] if k in c}:
            c[i]=x
            if go(left-{i}):return True
            del c[i]
        return False
    return go(set(range(len(E))))
steps=[([4,5,12,16,22,25,26,31],[9,29,34,37],0),([2,6,9,14,17,20,23,28],[2,14,15,35],2),([0,1,3,8,13,24,29,33],[7,12,15,25],0)]
for S,C,k in steps:
    S=set(S);W=set(V)-S
    assert C==[i for i,(u,v) in enumerate(E) if (u in S)!=(v in S)]
    F=[e for e in E if set(e)<=S];ports=[next(v for v in E[i] if v in S) for i in C]
    types=[j for j,w in enumerate(words) if color(sorted(S),F,ports,w)]
    assert types==[0,k+1]
    ports=[next(v for v in E[i] if v in W) for i in C]
    E=[e for e in E if set(e)<=W]+[[ports[a],ports[b]] for a,b in pairs[k]];V=sorted(W)
    print(len(V),types)
assert len(V)==10 and not color(V,E)
print('NO; independent coloring recursion nodes:',nodes)
