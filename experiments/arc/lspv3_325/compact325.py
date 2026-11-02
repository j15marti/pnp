#!/usr/bin/env python3
"""LSPV-3 GATE325, canonical exception-clause transfer. Restricted terminal only."""
from collections import Counter
from itertools import product

F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
PRIVATE=(1,2,3,4,6,7,8,9)

def G(t):
    return tuple(tuple((1 if l>0 else -1)*(9*((i+1)%t)+5
          if j==0 and l==5 else 9*i+abs(l))
          for l in c) for i in range(t) for j,c in enumerate(F9))

def valid(C,n):
    if n<3 or n%3 or len(C)*3!=4*n:return False
    seen=set();cnt=Counter()
    for c in C:
        if len(c)!=3 or any(type(v)!=int or not 1<=abs(v)<=n for v in c):return False
        if len({abs(v) for v in c})!=3 or len({v>0 for v in c})!=1:return False
        key=tuple(sorted(c))
        if key in seen:return False
        seen.add(key);cnt.update(c)
    return all(cnt[v]==cnt[-v]==2 for v in range(1,n+1))

def edit(t):
    C=list(G(t));i,j=2,14
    a=list(C[i]);b=list(C[j]);a[0],b[1]=b[1],a[0]
    C[i],C[j]=tuple(a),tuple(b)
    assert valid(C,9*t)
    return tuple(C)

def eval_clause(c,a):
    return any(a[abs(v)]==int(v>0) for v in c)

def count(F,p):
    n=max(abs(v) for c in F for v in c)
    if not valid(F,n):return 'MALFORMED',None
    if any(type(v)!=int or type(b)!=int or not 1<=v<=n or b not in (0,1)
           for v,b in p.items()):return 'MALFORMED_PIN',None
    if n%9:return 'UNRESOLVED',None
    t=n//9;B=G(t);actual={tuple(sorted(c)) for c in F}
    bset={tuple(sorted(c)) for c in B}
    A=[c for c in F if tuple(sorted(c)) not in bset]
    H=[c if tuple(sorted(c)) in actual else None for c in B]
    total=0;terms=[]
    for mask in range(1<<len(A)):
        pins=dict(p);conflict=False
        for j,c in enumerate(A):
            if mask>>j&1:
                for lit in c:
                    x=abs(lit);v=int(lit<0)
                    if x in pins and pins[x]!=v:conflict=True;break
                    pins[x]=v
                if conflict:break
        if conflict:terms.append(0);continue
        M=((1,0),(0,1))
        for i in range(t):
            tab=[[0,0],[0,0]]
            for u,v in product((0,1),repeat=2):
                if t==1 and u!=v:continue
                for bits in range(256):
                    q={9*i+5:u,**{9*i+x:(bits>>j)&1
                                   for j,x in enumerate(PRIVATE)}}
                    if t>1:q[9*((i+1)%t)+5]=v
                    if any(q.get(x)!=z for x,z in pins.items() if x in q):continue
                    if all(c is None or eval_clause(c,q)
                           for c in H[12*i:12*(i+1)]):tab[u][v]+=1
            M=tuple(tuple(sum(M[a][k]*tab[k][b] for k in (0,1))
                     for b in (0,1)) for a in (0,1))
        x=M[0][0]+M[1][1];terms.append(x)
        total+=(-1)**mask.bit_count()*x
    assert total>=0
    return ('SAT' if total else 'UNSAT'),{'models':total,'k':len(A),'terms':terms}

if __name__=='__main__':
    C=edit(2)
    p={18:1,10:0,16:1,1:0}
    kind,r=count(C,p);assert kind=='UNSAT' and r['terms']==[507,48,507,48]
    kind,s=count(C,p|{18:0});assert kind=='SAT' and s['models']==559
    kind,t=count(C,{});assert t['models']==4619 and t['k']==2
    print('GATE325 PASS: G2-edit source verified; UNSAT0/SAT559; root4619.')
