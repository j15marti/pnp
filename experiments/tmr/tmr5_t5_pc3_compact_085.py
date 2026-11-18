#!/usr/bin/env python3
"""TMR-5/085: self-contained binary path-consistency audit of T5/C5 instances."""
Q=range(5)
T5={(a,b) for a in Q for b in Q if (b-a)%5 in (1,3)}
C5={(a,b) for a in Q for b in Q if (b-a)%5 in (1,4)}
ALL=(1<<25)-1
EQU=sum(1<<(6*a) for a in Q)
def mask(r):return sum(1<<(5*a+b) for a,b in r)
def transpose(r):return sum(1<<(5*b+a) for a in Q for b in Q if r>>(5*a+b)&1)
def comp(a,b):
    rows=[(b>>(5*z))&31 for z in Q]
    out=0
    for x in Q:
        support=0;row=(a>>(5*x))&31
        for z in Q:
            if (row>>z)&1:support|=rows[z]
        out|=support<<(5*x)
    return out
def pc(n,arcs,rel):
    r=mask(rel);p=[[EQU if i==j else ALL for j in range(n)] for i in range(n)]
    for u,v in arcs:
        p[u][v]&=r;p[v][u]&=transpose(r)
    scans=0
    while True:
        changed=False;scans+=1
        for z in range(n):
            for x in range(n):
                for y in range(x,n):
                    new=p[x][y]&comp(p[x][z],p[z][y])
                    if new==0:return False,scans,(x,y,z)
                    if new!=p[x][y]:
                        p[x][y]=new;p[y][x]=transpose(new);changed=True
        if not changed:return True,scans,None
def grot():
    rim=[(i,(i+1)%5) for i in range(5)]
    ed={tuple(sorted(e)) for e in rim}
    for u,v in rim:
        ed.add(tuple(sorted((u,5+v))))
        ed.add(tuple(sorted((v,5+u))))
    ed.update((5+i,10) for i in range(5))
    return sorted(ed)
def positive():return sorted((i,5+(i+d)%6) for i in range(5) for d in range(4))
def lift(edges):
    arcs=[];n=11
    for u,v in edges:
        a,b,c=n,n+1,n+2;n+=3
        arcs.extend([(u,a),(a,b),(b,c),(u,c),(c,v)])
    return n,arcs
def count_c5(edges):
    adj=[[] for _ in range(11)]
    for u,v in edges:adj[u].append(v);adj[v].append(u)
    order=sorted(range(11),key=lambda u:(-len(adj[u]),u))
    val=[-1]*11
    def back(i):
        if i==11:return 1
        u=order[i];s=0
        for a in Q:
            if all((a,val[v]) in C5 for v in adj[u] if val[v]!=-1):
                val[u]=a;s+=back(i+1);val[u]=-1
        return s
    return back(0)
if __name__=="__main__":
    for name,edges,expected_count in [("NO",grot(),0),("YES",positive(),660)]:
        assert len(edges)==20
        ct=count_c5(edges);assert ct==expected_count
        n,arcs=lift(edges);assert(n,len(arcs))==(71,100)
        source=pc(11,edges,C5);raw=pc(n,arcs,T5)
        assert source[0]==raw[0]==bool(ct)
        print(name,"source_hom_count",ct,"source_PC",source,"T5_PC",raw)
    print("PASS: no anchor or reduction-image recognizer used in PC decision")
