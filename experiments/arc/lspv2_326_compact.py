#!/usr/bin/env python3
"""LSPV2-326: source-authenticated mixed signed/NAE matched circuit.
Run in pnp root: python experiments/arc/lspv2_326_compact.py
Requires networkx. Restricted gate optimum ONLY, P versus NP OPEN.
"""
import ast,itertools,json,random
from pathlib import Path
import networkx as nx

Y6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
P9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
F9=P9+[tuple(-x for x in q) for q in [(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]]
P15=[(1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15)]
F15=P15+[tuple(-x for x in q) for q in [(1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15)]]
Z6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
Z6=Z6+[tuple(-x for x in q) for q in Z6]
MIXED9=P9+[tuple(-x for x in q) for q in [(4,5,6),(2,3,5),(7,8,9),(2,4,7),(1,6,8),(1,3,9)]]

def valid(F,n):
    if type(n)!=int or n<3 or n%3 or len(F)*3!=4*n:return False
    seen=set();quota={}
    for c in F:
        if len(c)!=3 or any(type(x)!=int or x==0 or abs(x)>n for x in c) or len(set(map(abs,c)))!=3:return False
        if not (all(x>0 for x in c) or all(x<0 for x in c)):return False
        k=tuple(sorted(c))
        if k in seen:return False
        seen.add(k)
        for x in c:quota[x]=quota.get(x,0)+1
    return all(quota.get(v,0)==quota.get(-v,0)==2 for v in range(1,n+1))

def compile(F,n):
    if not valid(F,n):raise ValueError('malformed canonical source')
    E={};G=nx.Graph();G.add_nodes_from(range(len(F)))
    for i in range(len(F)):
        for j in range(i+1,len(F)):
            a,b=F[i],F[j];A=set(map(abs,a));B=set(map(abs,b));s=len(A&B)
            if a[0]*b[0]>0 and s in (1,2):w=s;kind='same'
            elif a[0]*b[0]<0 and A==B:w=2;kind='NAE'
            else:continue
            E[i,j]=(w,kind);G.add_edge(i,j,weight=w)
    M=sorted(tuple(sorted(t)) for t in nx.max_weight_matching(G,weight='weight'))
    used=set();gates=[];roots=[]
    def gate(op,a,b):
        z=n+len(gates)+1;gates.append((op,a,b,z));return z
    for i,j in M:
        used.update((i,j));a,b=F[i],F[j];kind=E[i,j][1]
        A=set(map(abs,a));B=set(map(abs,b));shared=sorted(A&B)
        if kind=='NAE':
            x,y,z=sorted(A);u=gate('XOR',x,y);v=gate('XOR',y,z)
            o=gate('OR',u,v)
        elif len(shared)==2:
            x,y=shared;c=next(iter(A-B));d=next(iter(B-A));pos=a[0]>0
            u=gate('OR' if pos else 'AND',x,y)
            v=gate('AND' if pos else 'OR',c,d)
            o=gate('OR' if pos else 'NAND',u,v)
        else:
            x=shared[0];c,d=sorted(A-B);e,f=sorted(B-A);pos=a[0]>0
            u=gate('OR' if pos else 'AND',c,d)
            v=gate('OR' if pos else 'AND',e,f)
            q=gate('AND' if pos else 'OR',u,v)
            o=gate('OR' if pos else 'NAND',x,q)
        roots.append(o)
    for i,c in enumerate(F):
        if i in used:continue
        a,b,d=map(abs,c);pos=F[i][0]>0
        u=gate('OR' if pos else 'AND',a,b)
        roots.append(gate('OR' if pos else 'NAND',u,d))
    while len(roots)>1:
        roots=[gate('AND',roots[k],roots[k+1]) if k+1<len(roots) else roots[k] for k in range(0,len(roots),2)]
    W=sum(E[t][0] for t in M)
    assert len(gates)==3*len(F)-1-W
    return gates,roots[0],W,sum(E[t][1]=='NAE' for t in M)

def evalc(C,root,b):
    vals={i+1:b[i] for i in range(len(b))}
    for op,a,d,z in C:
        x,y=vals[a],vals[d]
        vals[z]=(x&y if op=='AND' else x|y if op=='OR' else 1-(x&y) if op=='NAND' else x^y)
    return vals[root]

def source(F,b):
    return int(all(any(b[abs(x)-1]==int(x>0) for x in c) for c in F))

def main():
    cases={'Y6':Y6,'F9':F9,'F15':F15,'Z6_NAE':Z6,'MIXED9_NAE':MIXED9}
    p=Path('research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt')
    if not p.exists():p=Path(__file__).with_name('U198_source.txt')
    if p.exists():
        t=p.read_text();U=ast.literal_eval(t[t.index('[['):])
        V=[list(c) for c in U];V[2][2],V[44][2]=V[44][2],V[2][2]
        cases.update(U198=U,V198=V)
    out={}
    for name,F in cases.items():
        n=max(abs(x) for c in F for x in c);C,root,W,NAE=compile(F,n)
        rng=random.Random(326+n);rows=range(1<<n) if n<=15 else range(128);sat=0
        for k in rows:
            b=[(k>>i)&1 for i in range(n)] if n<=15 else [rng.getrandbits(1) for _ in range(n)]
            v=source(F,b);assert evalc(C,root,b)==v;sat+=v
        out[name]={'gates':len(C),'matching_weight':W,'NAE_blocks':NAE,
                   'full_models':sat if n<=15 else None}
    expect={'Y6':19,'F9':28,'F15':48,'Z6_NAE':15,'MIXED9_NAE':27}
    assert all(out[k]['gates']==v for k,v in expect.items())
    for x1,want in ((0,2),(1,0)):
        pins={1:x1,3:0,5:1,6:0,7:0,8:0};count=0
        for x2,x4,x9 in itertools.product((0,1),repeat=3):
            q={**pins,2:x2,4:x4,9:x9}
            count+=source(F9,[q[i] for i in range(1,10)])
        assert count==want
    print(json.dumps({'status':'RESTRICTED_EXACT; P_VS_NP_OPEN','cases':out},indent=2))

if __name__=='__main__':main()
