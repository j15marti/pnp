#!/usr/bin/env python3
"""Exact five-symbol beat CSP counter using directed modules and path quotients.
TMR-3/071, 2026-11-17. Source: 1^n 0 1^m 0, then 2m vertex IDs,
each in w=max(1,(n-1).bit_length()) low-bit-first bits. Repeated arcs legal.
Return exact #Hom(G,T5). Python big integers; see report for bit-machine ledger.
"""
import sys
from collections import defaultdict

PAIRS={sum(1<<j for j in (i,(i+2)%5)) for i in range(5)}
MASKS=set(1<<i for i in range(5))|PAIRS
COMP=[[all((b-a)%5 in (1,3) for a in range(5) if s>>a&1
            for b in range(5) if t>>b&1) for t in range(32)] for s in range(32)]

def parse(source):
    if set(source)-{'0','1'}: raise ValueError('nonbinary')
    a=source.find('0')
    if a<0: raise ValueError('missing n delimiter')
    b=source.find('0',a+1)
    if b<0: raise ValueError('missing m delimiter')
    n=a; m=b-a-1; w=max(1,(n-1).bit_length())
    if len(source)!=b+1+2*m*w: raise ValueError('wrong record length')
    edges=[]; k=b+1
    for _ in range(m):
        uv=[]
        for _ in range(2):
            uv.append(sum(1<<i for i in range(w) if source[k+i]=='1'))
            k+=w
        if max(uv)>=n:raise ValueError('bad vertex identifier')
        edges.append(tuple(uv))
    return n,edges

def closure(A,u,v):
    n=len(A); M={u,v}; todo=[v]
    while todo:
        t=todo.pop()
        for w in range(n):
            if w not in M and (A[u][w]!=A[t][w] or A[w][u]!=A[w][t]):
                M.add(w);todo.append(w)
                if len(M)==n:return M
    return M

def module(A):
    n=len(A)
    if n<3:return None
    for u in range(n):
        for v in range(u+1,n):
            M=closure(A,u,v)
            if len(M)<n:return sorted(M)
    return None

def path(A):
    n=len(A)
    if n<2:return list(range(n))
    deg=[sum(A[i][j] or A[j][i] for j in range(n) if j!=i) for i in range(n)]
    if sum(deg)!=2*n-2 or deg.count(1)!=2 or max(deg)>2:return None
    order=[]; prev=-1;cur=deg.index(1)
    while True:
        order.append(cur)
        nxt=[j for j in range(n) if j!=prev and (A[cur][j] or A[j][cur])]
        if not nxt:break
        if len(nxt)!=1:return None
        prev,cur=cur,nxt[0]
    return order if len(order)==n else None

def signature(W,A,stats):
    n=len(A);stats['calls']+=1
    if n==0:return {0:1}
    if any(A[i][i] for i in range(n)) or any(A[i][j] and A[j][i]
                                               for i in range(n) for j in range(i)):
        return {}
    if n==1:return dict(W[0])
    order=path(A)
    if order is not None:
        stats['paths']+=1
        D={(s,s):v for s,v in W[order[0]].items() if s in MASKS and v}
        for t in range(1,n):
            u,v=order[t-1],order[t]
            ND=defaultdict(int)
            for (sm,used),w in D.items():
                for tm,f in W[v].items():
                    if tm in MASKS and f and (COMP[sm][tm] if A[u][v] else COMP[tm][sm]):
                        ND[tm,used|tm]+=w*f
            D=ND
        out=defaultdict(int)
        for (_,used),v in D.items():out[used]+=v
        return dict(out)
    M=module(A)
    if M is not None:
        stats['modules']+=1
        sub=signature([W[i] for i in M],[[A[i][j] for j in M] for i in M],stats)
        if not sub:return {}
        S=set(M); rest=[i for i in range(n) if i not in S]; k=len(rest)
        NW=[W[i] for i in rest]+[sub]
        NA=[[False]*(k+1) for _ in range(k+1)]
        for i,u in enumerate(rest):
            for j,v in enumerate(rest):NA[i][j]=A[u][v]
            NA[i][k]=A[u][M[0]];NA[k][i]=A[M[0]][u]
            assert all(A[u][v]==NA[i][k] and A[v][u]==NA[k][i] for v in M)
        return signature(NW,NA,stats)
    stats['prime']=max(n,stats['prime'])
    deg=[sum(A[i][j] or A[j][i] for j in range(n) if i!=j) for i in range(n)]
    opt=[[(s,w) for s,w in W[i].items() if w and (s in MASKS if deg[i] else s)]
         for i in range(n)]
    out=defaultdict(int);assigned=[]
    def dfs(i,used,total):
        if i==n:out[used]+=total;return
        for s,w in opt[i]:
            if all((not A[j][i] or COMP[assigned[j]][s]) and
                   (not A[i][j] or COMP[s][assigned[j]]) for j in range(i)):
                assigned.append(s);dfs(i+1,used|s,total*w);assigned.pop()
    dfs(0,0,1)
    return dict(out)

def count(source):
    n,edges=parse(source)
    A=[[False]*n for _ in range(n)]
    for u,v in edges:A[u][v]=True
    stats=dict(calls=0,paths=0,modules=0,prime=0)
    weights=[{1<<c:1 for c in range(5)} for _ in range(n)]
    return sum(signature(weights,A,stats).values()),stats

if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: python tmr3_t5_module071_compact.py BINARY_SOURCE')
    try:
        z,statistics=count(sys.argv[1]);print(z)
    except ValueError as exc:
        raise SystemExit('INVALID: '+str(exc))
