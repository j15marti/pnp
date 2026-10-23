#!/usr/bin/env python3
"""ANTIPODAL79 exact-flow reproducer; Python standard library only.
Run: python 2026-10-23_1003_ANTIPODAL79_minirepro.py
Or:  python 2026-10-23_1003_ANTIPODAL79_minirepro.py path/to/DOECKER61_original_source.txt
"""
import ast, collections, hashlib, json, pathlib, sys

TOY=[
 [-2,-5,-6],[1,2,5],[3,4,5],[-2,-3,-6],
 [1,3,6],[2,4,6],[-1,-4,-5],[-1,-3,-4]]

class Flow:
    def __init__(self,size):
        self.g=[[] for _ in range(size)]
    def add(self,u,v):
        a=[v,1,len(self.g[v])]
        b=[u,0,len(self.g[u])]
        self.g[u].append(a);self.g[v].append(b)
        return (u,len(self.g[u])-1)
    def maxflow(self,s,t):
        value=0
        while True:
            lev=[-1]*len(self.g);lev[s]=0
            q=collections.deque([s])
            while q:
                u=q.popleft()
                for v,cap,r in self.g[u]:
                    if cap and lev[v]<0:lev[v]=lev[u]+1;q.append(v)
            if lev[t]<0:break
            ptr=[0]*len(self.g)
            def dfs(u):
                if u==t:return True
                while ptr[u]<len(self.g[u]):
                    i=ptr[u];v,cap,r=self.g[u][i]
                    if cap and lev[v]==lev[u]+1 and dfs(v):
                        self.g[u][i][1]=0;self.g[v][r][1]=1;return True
                    ptr[u]+=1
                return False
            while dfs(s):value+=1
        return value

def check(C,monotone):
    assert C
    n=max(abs(v) for c in C for v in c);m=len(C)
    assert 3*m==4*n
    assert len({tuple(c) for c in C})==m
    count=[[0,0] for _ in range(n+1)]
    for c in C:
        assert len(c)==3 and len({abs(v) for v in c})==3
        if monotone:assert all(v>0 for v in c) or all(v<0 for v in c)
        for v in c:count[abs(v)][v<0]+=1
    assert all(x==[2,2] for x in count[1:])
    return n,m

def antipodal_repair(C):
    n,m=check(C,True)
    positive=[i for i,c in enumerate(C) if all(x>0 for x in c)]
    negative=[i for i,c in enumerate(C) if all(x<0 for x in c)]
    assert len(positive)==len(negative)==m//2
    ps=1;vs=ps+len(positive);ns=vs+n;t=ns+len(negative)
    G=Flow(t+1);refs=[]
    for k,j in enumerate(positive):
        G.add(0,ps+k)
        for lit in C[j]:
            refs.append((j,lit,G.add(ps+k,vs+lit-1)))
    for k,j in enumerate(negative):
        G.add(ns+k,t)
        for lit in C[j]:
            refs.append((j,lit,G.add(vs-lit-1,ns+k)))
    f=G.maxflow(0,t)
    assert f==m//2
    changed=[list(c) for c in C]
    edits=[]
    for j,lit,(u,idx) in refs:
        if G.g[u][idx][1]==0:
            k=changed[j].index(lit)
            changed[j][k]=-lit
            edits.append((j,k))
    assert len(edits)==m
    check(changed,False)
    assert all(any(x>0 for x in c) and any(x<0 for x in c) for c in changed)
    assert [[abs(x) for x in c] for c in changed]==[[abs(x) for x in c] for c in C]
    return changed,edits,f

def load(path):
    text=pathlib.Path(path).read_text()
    return ast.literal_eval(text[text.find('[['):])

def run():
    C=load(sys.argv[1]) if len(sys.argv)>1 else TOY
    new,edits,flow=antipodal_repair(C)
    out={'n':max(abs(x) for c in C for x in c),'m':len(C),
         'integral_flow':flow,'sign_flips':len(edits),
         'both_zero_and_one_satisfy':True,'original_supports_unchanged':True,
         'flips_zero_based_first_12':edits[:12],
         'target_sha256':hashlib.sha256(json.dumps(new).encode()).hexdigest()}
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':run()
