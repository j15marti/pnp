import itertools as it, random, json
import networkx as nx
from collections import Counter
rng=random.Random(20261124); stats=Counter()
DIR=((1,0),(0,1),(1,1),(1,-1))
def dot(a,b): return sum(x*y for x,y in zip(a,b))
def ref(n,E):
    adj={v:[] for v in range(n)}
    for j,(u,v,w) in enumerate(E): adj[u].append((v,j));adj[v].append((u,j))
    def go(S):
        if not S: yield ();return
        u=min(S)
        for v,j in adj[u]:
            if v in S:
                for q in go(S-{u,v}): yield (j,)+q
    return list(go(set(range(n))))
def val(E,M): return tuple(sum(E[j][2][i] for j in M) for i in range(2))
def solve(n,E,b):
    m=len(E); pins={}; face=[0]*m; best=0
    rows=[({j:1 for j,(u,v,w) in enumerate(E) if i in (u,v)},1) for i in range(n)]
    rows += [({j:w[i] for j,(u,v,w) in enumerate(E) if w[i]},b[i]) for i in range(2)]
    def closure():
        while True:
            change=False
            for row,t in rows:
                t-=sum(c*pins[j] for j,c in row.items() if j in pins)
                free=[(j,c) for j,c in row.items() if j not in pins]
                def sums(skip=-1):
                    S={0}
                    for j,c in free:
                        if j!=skip: S|={x+c for x in S}
                    return S
                stats['row_checks']+=1
                if t not in sums(): return False
                for j,c in free:
                    S=sums(j); allowed=[a for a in (0,1) if t-c*a in S]
                    if len(allowed)==1:
                        pins[j]=allowed[0];stats['pins']+=1;change=True;break
                if change: break
            if not change:return True
    def opt(w):
        stats['weighted_calls']+=1
        B=1+2*sum(map(abs,w));G=nx.Graph();used=set();P=[]
        for j,a in pins.items():
            if a:
                u,v,_=E[j]
                if u in used or v in used:return None
                used.update((u,v));P.append(j)
        G.add_nodes_from(set(range(n))-used)
        for j,(u,v,_) in enumerate(E):
            if j not in pins and u not in used and v not in used:G.add_edge(u,v,weight=B*face[j]+w[j],idx=j)
        Q=nx.max_weight_matching(G,maxcardinality=True)
        if 2*len(Q)!=len(G):return None
        M=P+[G[u][v]['idx'] for u,v in Q]
        if sum(face[j] for j in M)!=best:return None
        return M
    while True:
        if not closure():return 'UNSAT',None
        M=opt([0]*m)
        if M is None:return 'UNSAT',None
        if val(E,M)==b:return 'SAT',M
        change=False
        for a in DIR:
            for s in (1,-1):
                w=[s*dot(a,v) for _,_,v in E];target=s*dot(a,b)
                M=opt(w);assert M is not None
                v=sum(w[j] for j in M)
                if target>v:return 'UNSAT',None
                if val(E,M)==b:return 'SAT',M
                if target==v:
                    L=opt([-z for z in w]);assert L is not None
                    if sum(w[j] for j in L)<v:
                        B=1+2*sum(map(abs,w));face=[B*f+z for f,z in zip(face,w)];best=B*best+v
                        stats['face_steps']+=1;change=True;break
            if change:break
        if not change:return 'UNKNOWN',None

def verify(n,E,b,truth=None):
    if truth is None:
        ms=ref(n,E);stats['reference_matchings']+=len(ms);truth=any(val(E,M)==b for M in ms)
    label,M=solve(n,E,b);stats[label]+=1;stats['true_SAT' if truth else 'true_UNSAT']+=1
    if label=='UNKNOWN':stats['unknown_SAT' if truth else 'unknown_UNSAT']+=1
    else: assert (label=='SAT')==truth
    if M is not None:
        assert sorted(v for j in M for v in E[j][:2])==list(range(n)) and val(E,M)==b
        stats['verified_witnesses']+=1
    return label
for _ in range(200):
    n=rng.choice([4,6,8]); E=[(u,v,(rng.randint(-1,1),rng.randint(-1,1))) for u,v in it.combinations(range(n),2) if rng.random()<.55]
    ms=ref(n,E); b=val(E,rng.choice(ms)) if ms and rng.random()<.5 else (rng.randint(-3,3),rng.randint(-3,3))
    verify(n,E,b)
# 8-cycle: red count 0 or 4; target 2 is an even interior hole.
E=[(i,(i+1)%8,(int(i%2==0),0)) for i in range(8)]
assert verify(8,E,(2,0))=='UNKNOWN'
assert verify(8,E,(4,0))=='SAT'
# K4 with every edge replaced by a length-three path. The three original
# perfect matchings contribute (0,3), (3,0), (1,1) respectively.
def gadget(r):
    E=[]
    for h in range(r):
        o=16*h
        specs=[(0,1,[(0,1),(0,1)]),(2,3,[(0,1),(0,0)]),(0,2,[(1,0),(1,0)]),(1,3,[(1,0),(0,0)]),(0,3,[(1,0),(0,0)]),(1,2,[(0,1),(0,0)])]
        for j,(u,v,(a,b)) in enumerate(specs):
            p=o+4+2*j;q=p+1;E.extend([(o+u,p,a),(p,q,(0,0)),(q,o+v,b)])
    return 16*r,E
scale=[]
for r in [1,2,4,8,16,32]:
    n,E=gadget(r);before=stats.copy();a=verify(n,E,(r,r),True);z=verify(n,E,(r,r-1),False)
    assert a=='SAT' and z=='UNSAT';scale.append(dict(copies=r,vertices=n,edges=len(E),width3=sum(sum(map(abs,w))==1 for _,_,w in E),calls=stats['weighted_calls']-before['weighted_calls'],face_steps=stats['face_steps']-before['face_steps']))
print(json.dumps(dict(seed=20261124,networkx=nx.__version__,stats=dict(stats),scaling=scale),sort_keys=True))
