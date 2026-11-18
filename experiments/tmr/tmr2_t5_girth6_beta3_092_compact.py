#!/usr/bin/env python3
"""TMR-2/092: exhaustive finite-core support checker. Standard-library Python."""
from itertools import combinations_with_replacement, permutations

STATES=[(l,r) for l in (1,2,3) for r in range(l+1)]+[(6,0)]

def cores():
    for n in range(1,5):
        edge_types=[(a,b) for a in range(n) for b in range(a,n)]
        unique=set()
        for edges in combinations_with_replacement(edge_types,n+2):
            deg=[0]*n; adj=[set() for _ in range(n)]
            for a,b in edges:
                deg[a]+=1; deg[b]+=1; adj[a].add(b); adj[b].add(a)
            if min(deg)<3: continue
            seen={0}; pending=[0]
            while pending:
                u=pending.pop()
                for w in adj[u]-seen: seen.add(w); pending.append(w)
            if len(seen)!=n:continue
            unique.add(min(tuple(sorted((min(p[a],p[b]),max(p[a],p[b])) for a,b in edges))
                           for p in permutations(range(n))))
        for edges in sorted(unique):yield n,edges

def circuits(n,edges):
    out=[]
    for mask in range(1,1<<len(edges)):
        deg=[0]*n; adj=[[] for _ in range(n)]
        for k,(a,b) in enumerate(edges):
            if mask>>k&1:
                deg[a]+=1;deg[b]+=1;adj[a].append(b);adj[b].append(a)
        active=[u for u in range(n) if deg[u]>0]
        if not active or any(deg[u]!=2 for u in active) or len(active)!=mask.bit_count():continue
        seen={active[0]};q=[active[0]]
        while q:
            u=q.pop()
            for w in adj[u]:
                if w not in seen: seen.add(w);q.append(w)
        if len(seen)==len(active):out.append(mask)
    return out

def walk(l,r):
    if l==6:return [1]*5 # wildcard for all actual l>=4
    row=[1,0,0,0,0]
    for steps in [(1,3)]*(l-r)+[(2,4)]*r:
        nxt=[0]*5
        for a in range(5):
            for s in steps:nxt[(a+s)%5]+=row[a]
        row=nxt
    return row

def run():
    rows=[walk(*state) for state in STATES]
    complete=[];prefix=0;mins=[]
    for n,edges in cores():
        m=len(edges); cs=circuits(n,edges)
        labels=[]
        for p in range(5**(n-1)):
            vals=[0];k=p
            for _ in range(1,n):vals.append(k%5);k//=5
            labels.append(vals)
        filt=[]
        for a,b in edges:
            filt.append([sum(1<<p for p,x in enumerate(labels) if row[(x[b]-x[a])%5])
                         for row in rows])
        selected=[0]*m;done=0;small=5**(n-1)
        def dfs(depth,mask):
            nonlocal done,small,prefix
            if depth==m:
                assert mask!=0, (n,edges,[STATES[j] for j in selected])
                done+=1;small=min(small,mask.bit_count());return
            for si,(length,_) in enumerate(STATES):
                prefix+=1;selected[depth]=si
                if any(sum(STATES[selected[j]][0] for j in range(depth+1) if cycle>>j&1)<6
                       for cycle in cs if cycle>>depth&1 and not cycle>>(depth+1)):
                    continue
                dfs(depth+1,mask&filt[depth][si])
        dfs(0,(1<<len(labels))-1)
        complete.append(done);mins.append(small)
    expected=[1,10,140,35,645,350,100,3144,1400,11410,3500,1000,31440,122052,602916]
    assert complete==expected,(complete,expected)
    assert prefix==1428850,prefix
    assert sum(complete)==778143 and min(mins)==1
    print("cores",len(complete),"prefix visits",prefix,
          "girth-admissible",sum(complete),"UNSAT",0,"min pinned solutions",min(mins))
    print("admissible per core:",complete)

if __name__=="__main__":run()
