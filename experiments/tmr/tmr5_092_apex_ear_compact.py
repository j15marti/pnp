"""TMR-5/092 compact exact verifier: T5 two-connected twin-free easy YES/NO."""
from itertools import product
from collections import defaultdict

A=[[int((b-a)%5 in (1,3)) for b in range(5)] for a in range(5)]
Y=((0,0,1),(0,0,1),(1,1,0))
N=((0,0,1),(0,1,0),(1,0,1))
def multiply(X,Y): return [[sum(X[i][k]*Y[k][j] for k in range(5)) for j in range(5)] for i in range(5)]
W=multiply(multiply(A,A),multiply(A,A))
assert W[0]==[4,4,1,6,1] and all(min(row)>0 for row in W)
for a,b in product(range(5),repeat=2):
    assert W[a][b]==sum(all(A[x][y] for x,y in zip((a,)+p,p+(b,))) for p in product(range(5),repeat=3))
for u,a,b,c,v in product(range(5),repeat=5):
    assert bool(A[u][a]*A[a][b]*A[b][c]*A[u][c]*A[c][v])==(
        a==(u+1)%5 and b==(u+2)%5 and c==(u+3)%5 and (v-u)%5 in (1,4))

def core(s,t,neg):
    seed=N if neg else Y
    return [(i,s+j) if seed[i if i<3 else 0][j if j<3 else 0]
            else (s+j,i) for i in range(s) for j in range(t)]
def augment(s,t,neg):
    n=s+t; arcs=core(s,t,neg)+[(n,n+1)]
    for v in range(n):
        p=n+2+3*v;h=n+(0 if v<s else 1)
        arcs+= [(v,p),(p,p+1),(p+1,p+2),(p+2,h)]
    return 4*n+2,arcs
def signatures(n,arcs):
    inc=[set() for _ in range(n)];out=[set() for _ in range(n)]
    for u,v in arcs:inc[v].add(u);out[u].add(v)
    return [(tuple(sorted(inc[i])),tuple(sorted(out[i]))) for i in range(n)]
def biconnected(n,arcs):
    adj=[set() for _ in range(n)]
    for u,v in arcs:adj[u].add(v);adj[v].add(u)
    for absent in range(n):
        seen={next(i for i in range(n) if i!=absent)};todo=list(seen)
        for u in todo:
            for v in adj[u]:
                if v!=absent and v not in seen:seen.add(v);todo.append(v)
        if len(seen)!=n-1:return False
    return True
def bipartite(n,arcs):
    adj=[[] for _ in range(n)]
    for u,v in arcs:adj[u].append(v);adj[v].append(u)
    labels={}
    for root in range(n):
        if root in labels:continue
        labels[root]=0;q=[root]
        for u in q:
            for v in adj[u]:
                if v not in labels:labels[v]=1-labels[u];q.append(v)
                elif labels[v]==labels[u]:return False
    return True
def weighted_surj(size,S,weights):
    return sum((-1)**(len(S)-len(T))*sum(weights[a] for a in T)**size
               for r in range(len(S)+1) for T in __import__('itertools').combinations(S,r))
def exact_count(s,t,neg):
    n=s+t;arcs=core(s,t,neg)
    sig=signatures(n,arcs)
    d=defaultdict(list)
    for v,k in enumerate(sig):d[k].append(v)
    groups=list(d.values());which={v:i for i,g in enumerate(groups) for v in g}
    ed={(which[u],which[v]) for u,v in arcs}
    opts=[tuple(a for a in range(5) if mask>>a&1) for mask in range(1,32)]
    result=0
    for hl,hr in product(range(5),repeat=2):
        if not A[hl][hr]:continue
        vals=[{S:weighted_surj(len(g),S,[W[a][hl if g[0]<s else hr] for a in range(5)])
               for S in opts} for g in groups]
        def walk(i,chosen,ways):
            if i==len(groups):return ways
            ans=0
            for S in opts:
                if not vals[i][S]:continue
                if all((j,i) not in ed or all(A[a][b] for a in T for b in S)
                       for j,T in enumerate(chosen)) and all(
                       (i,j) not in ed or all(A[a][b] for a in S for b in T)
                       for j,T in enumerate(chosen)):
                    ans+=walk(i+1,chosen+[S],ways*vals[i][S])
            return ans
        result+=walk(0,[],1)
    return result,len(groups)
for s,t in ((3,3),(3,4),(4,4),(5,6),(9,11),(20,23)):
    d=[];edge=[]
    for neg in (False,True):
        n,arcs=augment(s,t,neg)
        assert n==4*(s+t)+2 and len(arcs)==s*t+4*(s+t)+1
        assert biconnected(n,arcs) and bipartite(n,arcs)
        assert len(set(signatures(n,arcs)))==n
        count,k=exact_count(s,t,neg)
        assert k==(6 if neg else 4)
        assert (count==0)==neg
        sig=signatures(n,arcs)
        d.append(([len(x[0]) for x in sig],[len(x[1]) for x in sig]))
        edge.append(set(arcs))
        if not neg:print(s,t,n,len(arcs),count)
    assert d[0]==d[1] and len(edge[0]^edge[1])==8
print("TMR5_092 compact PASS")
