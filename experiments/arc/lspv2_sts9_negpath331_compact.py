#!/usr/bin/env python3
"""LSPV-2 STS9 NEG-PATH331 reproducible restricted counterexample.
Original variables are the circuit/SAT inputs. P vs NP OPEN.
"""
from itertools import product
BASE=((1,4,7),(2,5,8),(3,6,9),(1,2,3),(4,5,6),(7,8,9),
      (-1,-5,-9),(-2,-6,-7),(-3,-4,-8),(-1,-6,-8),(-2,-4,-9),(-3,-5,-7))
def family(t):
    out=[]
    for i in range(t):
        for j,c in enumerate(BASE):
            a=[v+9*i if v>0 else v-9*i for v in c]
            if j==0 and i>0:a[0]=9*i-8
            if j==3 and i<t-1:a[0]=9*i+10
            out.append(tuple(a))
    return out
def valid(F,n):
    from collections import Counter
    assert len(F)==4*n//3 and len(set(tuple(sorted(c)) for c in F))==len(F)
    d=Counter()
    for c in F:
        assert len(c)==3 and len(set(map(abs,c)))==3
        assert all((v>0)==(c[0]>0) for v in c)
        for v in c:d[abs(v),v>0]+=1
    assert all(d[x,True]==d[x,False]==2 for x in range(1,n+1))
def truth(F,z):
    return all(any(z[abs(l)-1]==int(l>0) for l in c) for c in F)
def Ktable():
    K={}
    for a,b,c in product((0,1),repeat=3):
        q=0
        for rest in product((0,1),repeat=8):
            z={1:b,**{i+2:v for i,v in enumerate(rest)}}
            good=True
            for j,cl in enumerate(BASE):
                if j==0:v=[a,z[4],z[7]]
                elif j==3:v=[c,z[2],z[3]]
                else:v=[z[abs(l)] if l>0 else 1-z[abs(l)] for l in cl]
                if not any(v):good=False;break
            q+=good
        K[a,b,c]=q
    return K
def count(t,K):
    if t==1:return K[0,0,0]+K[1,1,1]
    dp={(b,c):K[b,b,c] for b,c in product((0,1),repeat=2)}
    for _ in range(1,t-1):
        nxt={(b,c):0 for b,c in product((0,1),repeat=2)}
        for (a,b),q in dp.items():
            for c in (0,1):nxt[b,c]+=q*K[a,b,c]
        dp=nxt
    return sum(q*K[a,b,b] for (a,b),q in dp.items())
def mincover(F,n):
    e=[sum(1<<(abs(l)-1) for l in c) for c in F]
    best=n+1;ways=0
    for b in range(1<<n):
        if b.bit_count()>best:continue
        if all(b&x for x in e):
            if b.bit_count()<best:best=b.bit_count();ways=1
            elif b.bit_count()==best:ways+=1
    return best,ways
def main():
    K=Ktable()
    assert [[[K[a,b,c] for c in (0,1)] for b in (0,1)] for a in (0,1)] == [[[9,34],[1,5]],[[34,66],[5,9]]]
    expected=(18,502,10384,226490,4895152,106030682,2294958744,49675751178)
    for t in range(1,9):
        F=family(t);valid(F,9*t)
        ans=count(t,K)
        assert ans==expected[t-1]
        if t<=2:
            brute=sum(truth(F,tuple((b>>i)&1 for i in range(9*t))) for b in range(1<<(9*t)))
            assert brute==ans
            assert mincover(F,9*t)==((5,54) if t==1 else (9,252))
        print("t",t,"models",ans,"backdoor_proved_lower",3*t+2)
    print("PASS; restrictions only; P versus NP OPEN")
if __name__=="__main__":main()
