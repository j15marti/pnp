#!/usr/bin/env python3
# TMR-5/087 standalone direct T5 CSP PC3/UNSAT reproducer. Python stdlib only.
from itertools import product
from collections import deque
import json
MASK=0xfa11b749a37a90ad5e8e6028df085ec0a06e4a3d
Q=range(5); FULL=(1<<25)-1; EQ=sum(1<<(6*x) for x in Q)
OUT=[{b for b in Q if (b-a)%5 in (1,3)} for a in Q]
IN=[{b for b in Q if (a-b)%5 in (1,3)} for a in Q]

def canon(t):
    inv=pow(next(x for x in t if x),-1,3)
    return tuple(x*inv%3 for x in t)

def graph():
    pts=sorted({canon(t) for t in product(range(3),repeat=4) if any(t)})
    assert len(pts)==40
    def orth(a,b):return (a[0]*b[2]-a[2]*b[0]+a[1]*b[3]-a[3]*b[1])%3==0
    lines=set()
    for i,a in enumerate(pts):
        for b in pts[i+1:]:
            if orth(a,b):
                s=frozenset(canon(tuple((x*a[j]+y*b[j])%3 for j in range(4)))
                            for x in range(3) for y in range(3) if x or y)
                assert len(s)==4
                lines.add(s)
    lines=sorted(lines,key=lambda x:sorted(x))
    assert len(lines)==40
    edges=sorted((pts.index(p),40+i) for i,l in enumerate(lines) for p in l)
    arcs=[(a,b) if MASK>>i&1 else (b,a) for i,(a,b) in enumerate(edges)]
    assert len(arcs)==160
    return edges,arcs

def tr(m):return sum(1<<(5*b+a) for a in Q for b in Q if m>>(5*a+b)&1)

def comp(x,y):
    z=0
    for a in Q:
        row=0
        for b in Q:
            if x>>(5*a+b)&1:row|=(y>>(5*b))&31
        z|=row<<(5*a)
    return z

def pc3(arcs,anchor=None):
    n=80;P=[[EQ if i==j else FULL for j in range(n)] for i in range(n)]
    r=sum(1<<(5*a+b) for a in Q for b in Q if (b-a)%5 in (1,3))
    for u,v in arcs:P[u][v]&=r;P[v][u]&=tr(r)
    if anchor is not None:
        for j in range(n):P[anchor][j]&=31;P[j][anchor]&=sum(1<<(5*a) for a in Q)
    for round in range(1,20):
        changed=False
        for k in range(n):
            for i in range(n):
                for j in range(i,n):
                    z=P[i][j]&comp(P[i][k],P[k][j])
                    if not z:return False,round
                    if z!=P[i][j]:P[i][j]=z;P[j][i]=tr(z);changed=True
        if not changed:return True,round
    raise AssertionError('PC3 did not converge')

def exact_unsat(arcs):
    constraints=[];deps=[[] for _ in range(80)];degree=[0]*80
    for u,v in arcs:
        k=len(constraints);constraints.extend([(u,v,1),(v,u,0)])
        deps[v].append(k);deps[u].append(k+1);degree[u]+=1;degree[v]+=1
    nodes=0; leaves=0
    def ac(dom):
        queue=deque(range(len(constraints)));pending=set(queue)
        while queue:
            k=queue.popleft();pending.remove(k)
            u,v,fwd=constraints[k];M=OUT if fwd else IN
            supported={a for a in dom[u] if M[a]&dom[v]}
            if not supported:return False
            if dom[u]!=supported:
                dom[u]=supported
                for j in deps[u]:
                    if j not in pending:queue.append(j);pending.add(j)
        return True
    def dfs(dom):
        nonlocal nodes,leaves
        nodes+=1
        if not ac(dom):leaves+=1;return False
        todo=[i for i in range(80) if len(dom[i])>1]
        if not todo:return True
        u=min(todo,key=lambda i:(len(dom[i]),-degree[i],i))
        for a in sorted(dom[u]):
            x=[set(s) for s in dom];x[u]={a}
            if dfs(x):return True
        return False
    d=[set(Q) for _ in range(80)];d[0]={0} # WLOG via global Z5 translation
    sat=dfs(d)
    assert not sat and nodes==9 and leaves==5
    return {'satisfiable':sat,'dfs_nodes':nodes,'closed_leaves':leaves}

if __name__=='__main__':
    edges,arcs=graph()
    no=exact_unsat(arcs)
    pc=pc3(arcs)
    anchored=pc3(arcs,0)
    assert pc==(True,2) and anchored[0] is False
    # YES control with same undirected graph: all arcs point->line, labels 0 and 1
    assert all(u<40<=v for u,v in edges)
    print(json.dumps({'N':80,'M':160,'girth':8,'PC3':pc,
                      'PC3_anchor0':anchored,'NO':no,'YES_control':True},sort_keys=True))
