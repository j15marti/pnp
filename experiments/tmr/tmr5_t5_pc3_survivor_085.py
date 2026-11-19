#!/usr/bin/env python3
"""Standalone 143-vertex T5 PC3 false positive, no third-party dependencies."""
E=[(0,7),(0,15),(0,23),(1,2),(1,23),(1,24),(2,8),(2,19),
(3,8),(3,15),(3,21),(4,6),(4,15),(4,19),(5,16),(5,22),(5,24),
(6,13),(6,25),(7,11),(7,16),(8,25),(9,13),(9,17),(9,18),
(10,12),(10,18),(10,21),(11,13),(11,22),(12,20),(12,23),
(14,17),(14,21),(14,24),(16,25),(17,20),(18,20),(19,22)]
assert len(E)==39
Q=range(5);F=(1<<25)-1;EQ=sum(1<<(6*a) for a in Q)
C5={(a,b) for a in Q for b in Q if (b-a)%5 in (1,4)}
T5={(a,b) for a in Q for b in Q if (b-a)%5 in (1,3)}
def hom_exists():
    neighbors=[[] for _ in range(26)]
    for a,b in E:neighbors[a].append(b);neighbors[b].append(a)
    v=[-1]*26;v[0]=0;calls=[0]
    def dfs():
        calls[0]+=1;choices={}
        for x in range(26):
            if v[x]!=-1:continue
            allow=[c for c in Q if all((c,v[y]) in C5 for y in neighbors[x] if v[y]>=0)]
            if not allow:return False
            choices[x]=allow
        if not choices:return True
        x=min(choices,key=lambda z:(len(choices[z]),-sum(v[y]>=0 for y in neighbors[z]),z))
        for c in choices[x]:
            v[x]=c
            if dfs():return True
            v[x]=-1
        return False
    answer=dfs();assert not answer
    return calls[0]
def lift():
    n=26;arcs=[]
    for u,v in E:
        a,b,c=n,n+1,n+2;n+=3
        arcs.extend([(u,a),(a,b),(b,c),(u,c),(c,v)])
    return n,arcs
def tr(x):return sum(1<<(5*b+a) for a in Q for b in Q if x>>(5*a+b)&1)
def compose(x,y):
    rows=[(y>>(5*c))&31 for c in Q];z=0
    for a in Q:
        row=(x>>(5*a))&31;r=0
        for c in Q:
            if row>>c&1:r|=rows[c]
        z|=r<<(5*a)
    return z
def pc(n,arcs,allowed,anchor=None):
    p=[[EQ if i==j else F for j in range(n)] for i in range(n)]
    r=sum(1<<(5*a+b) for a,b in allowed)
    for u,v in arcs:p[u][v]&=r;p[v][u]&=tr(r)
    if anchor is not None:
        for j in range(n):
            p[anchor][j]&=31
            p[j][anchor]&=sum(1<<(5*a) for a in Q)
    rounds=0
    while True:
        rounds+=1;changes=0
        for k in range(n):
            for i in range(n):
                for j in range(i,n):
                    z=p[i][j]&compose(p[i][k],p[k][j])
                    if not z:return False,rounds
                    if z!=p[i][j]:p[i][j]=z;p[j][i]=tr(z);changes+=1
        if not changes:return True,rounds
if __name__=='__main__':
    calls=hom_exists()
    n,arcs=lift();assert (n,len(arcs))==(143,195)
    unrooted=pc(n,arcs,T5)
    rooted=pc(n,arcs,T5,0)
    source=pc(26,E,C5)
    assert unrooted[0] and source[0] and not rooted[0]
    print(dict(source_vertices=26,source_edges=39,T5_vertices=n,T5_arcs=len(arcs),
        source_C5_satisfiable=False,source_backtracking_nodes=calls,
        source_PC=source,T5_unanchored_PC=unrooted,T5_anchored_at_vertex0_PC=rooted))
