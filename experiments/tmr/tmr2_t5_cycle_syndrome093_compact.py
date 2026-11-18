#!/usr/bin/env python3
"""TMR-2/093 compact, standalone source-to-syndrome verifier. Python 3 stdlib."""
from itertools import product
from collections import defaultdict, deque

def path_row(word):
    row=[1,0,0,0,0]
    for s in word:
        nxt=[0]*5
        for a,count in enumerate(row):
            for t in ((1,3) if s==1 else (2,4)):
                nxt[(a+t)%5]+=count
        row=nxt
    return row

def theta(words):
    n=2;E=[]
    for word in words:
        path=[0]+list(range(n,n+len(word)-1))+[1]
        n+=len(word)-1
        for u,v,s in zip(path,path[1:],word):E.append((u,v) if s==1 else (v,u))
    return n,E

def count_dp(n,edges):
    p=list(range(n))
    def find(v):
        while p[v]!=v:p[v]=p[p[v]];v=p[v]
        return v
    tree=[];chords=[]
    for i,(u,v) in enumerate(edges):
        a,b=find(u),find(v)
        if a==b:chords.append(i)
        else:p[a]=b;tree.append(i)
    components=len({find(v) for v in range(n)})
    beta=len(chords)
    assert beta==len(edges)-n+components
    adjacency=[[] for _ in range(n)]
    for i in tree:
        u,v=edges[i]
        adjacency[u].append((v,i,1));adjacency[v].append((u,i,-1))
    H=[]
    for ei in chords:
        u,v=edges[ei];parents={v:None};todo=deque([v])
        while todo and u not in parents:
            x=todo.popleft()
            for y,i,sign in adjacency[x]:
                if y not in parents:parents[y]=(x,i,sign);todo.append(y)
        row=[0]*len(edges);row[ei]=1;x=u
        while x!=v:
            prev,j,sign=parents[x];row[j]=sign%5;x=prev
        H.append(row)
    r=tuple((-3*sum(row))%5 for row in H)
    D={tuple([0]*beta):1};profile=[1];updates=0
    for ei in range(len(edges)):
        column=[row[ei] for row in H];nxt=defaultdict(int)
        for state,k in D.items():
            nxt[state]+=k
            nxt[tuple((a+b)%5 for a,b in zip(state,column))]+=k
            updates+=2
        D=dict(nxt);profile.append(len(D))
    return 5**components*D.get(r,0),profile,updates

def count_brute(n,edges):
    a=[0]*n;prior=[[] for _ in range(n)]
    for u,v in edges:
        s,t=sorted((u,v));prior[t].append((s,u==s))
    def go(k):
        if k==n:return 1
        count=0
        for x in range(5):
            a[k]=x
            if all(((x-a[j])%5 if fw else (a[j]-x)%5) in (1,3) for j,fw in prior[k]):count+=go(k+1)
        return count
    return go(0)

if __name__=='__main__':
    no=((1,1),(1,1,1),(1,1,-1),(-1,-1,-1))
    n,E=theta(no)
    EY=[(v,u) if i==0 else (u,v) for i,(u,v) in enumerate(E)]
    result=[]
    for key,arcs,expected in [('NO',E,0),('YES',EY,135)]:
        z,profile,updates=count_dp(n,arcs)
        assert z==expected==count_brute(n,arcs)
        result.append((key,z,profile,updates))
    assert result[0][2:]==result[1][2:]
    for words in [((1,)*3,)*5, ((1,)*3,(1,1,-1),(1,-1,-1),(-1,)*3,(1,)*3)]:
        n2,E2=theta(words)
        transfer=5*sum(__import__('math').prod(path_row(w)[d] for w in words) for d in range(5))
        assert count_dp(n2,E2)[0]==transfer>0
    all3=list(product((1,-1),repeat=3))
    rows=[path_row(w) for w in all3]
    minimum,maximum,total,unsat=10**9,0,0,0
    for a,b,c,d,e in product(range(8),repeat=5):
        z=5*sum(rows[a][j]*rows[b][j]*rows[c][j]*rows[d][j]*rows[e][j] for j in range(5))
        minimum=min(minimum,z);maximum=max(maximum,z);total+=z;unsat+=(z==0)
    assert (minimum,maximum,total,unsat)==(30,2440,8670020,0)
    print('matched controls:',[(x[0],x[1],x[3]) for x in result])
    print('identical full syndrome width profile:',result[0][2])
    print('five-path census: 32768 orientations, min 30, max 2440, total 8670020, UNSAT 0')
    print('P versus NP remains open')
