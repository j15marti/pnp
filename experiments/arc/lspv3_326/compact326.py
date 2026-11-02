#!/usr/bin/env python3
"""GATE326, paid bounded-interface transfer. Known DP, restricted family only."""
from collections import Counter
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
def original(t):
    assert t>=2 and t%2==0
    F=[]
    for i in range(t):
        for j,c in enumerate(F9):
            F.append(tuple((1 if x>0 else -1)*(9*((i+1)%t)+5 if j==0 and x==5 else 9*i+abs(x)) for x in c))
    for i in range(0,t,2):
        a,b=12*i+2,12*(i+1)+2
        u,v=list(F[a]),list(F[b])
        u[0],v[0]=v[0],u[0]
        F[a],F[b]=tuple(u),tuple(v)
    return tuple(F)
def valid(F,n):
    if n%3 or len(F)*3!=4*n or len(set(map(lambda c:tuple(sorted(c)),F)))!=len(F):return False
    cnt=Counter(x for c in F for x in c)
    return all(len(c)==3 and len({abs(x) for x in c})==3 and len({x>0 for x in c})==1 for c in F) and all(cnt[x]==cnt[-x]==2 for x in range(1,n+1))
def sat(c,a):return any(a[abs(x)]==int(x>0) for x in c)
def count(F,t,p):
    n=9*t
    if not valid(F,n):return "MALFORMED",None
    if any(type(x)!=int or type(v)!=int or x<1 or x>n or v not in (0,1) for x,v in p.items()):return "MALFORMED_PIN",None
    local=[[] for _ in range(t)];edge=[[] for _ in range(t)];H=[set() for _ in range(t)]
    for c in F:
        blocks={(abs(x)-1)//9 for x in c}
        if len(blocks)==1:local[next(iter(blocks))].append(c)
        elif len(blocks)==2:
            j=next((i for i in range(t) if blocks=={i,(i+1)%t}),None)
            if j is None:return "UNRESOLVED",None
            edge[j].append(c)
            for x in c:H[(abs(x)-1)//9].add(abs(x))
        else:return "UNRESOLVED",None
    H=[sorted(x) for x in H]
    assert max(map(len,H))<=4
    L=[];E=[]
    for i in range(t):
        a=[0]*(1<<len(H[i]))
        for bits in range(512):
            z={9*i+j:(bits>>(j-1))&1 for j in range(1,10)}
            if any(x in p and p[x]!=v for x,v in z.items()):continue
            if all(sat(c,z) for c in local[i]):
                a[sum(z[x]<<j for j,x in enumerate(H[i]))]+=1
        L.append(a)
    for i in range(t):
        nxt=(i+1)%t;mat=[]
        for u in range(len(L[i])):
            z={x:(u>>j)&1 for j,x in enumerate(H[i])};row=[]
            for v in range(len(L[nxt])):
                y={x:(v>>j)&1 for j,x in enumerate(H[nxt])}
                row.append(int(all(sat(c,{**z,**y}) for c in edge[i])))
            mat.append(row)
        E.append(mat)
    total=0
    for start in range(len(L[0])):
        d={start:1}
        for i in range(t):
            nd={}
            for u,num in d.items():
                if L[i][u]:
                    for v,ok in enumerate(E[i][u]):
                        if ok:nd[v]=nd.get(v,0)+num*L[i][u]
            d=nd
        total+=d.get(start,0)
    return ("SAT" if total else "UNSAT"),total
if __name__=="__main__":
    for t,goal in ((2,4952),(4,23260326),(6,112060476824),(8,540246471390034),(10,2604591598112749432)):
        F=original(t)
        assert valid(F,9*t) and count(F,t,{})==("SAT",goal)
        print("t",t,"k",t,"#SAT",goal)
    F=original(2);p={1:1,2:1,3:1,5:1}
    assert count(F,2,p)==("UNSAT",0)
    assert count(F,2,p|{1:0})==("SAT",184)
    print("GATE326 PASS: same-original UNSAT0 / SAT184")
