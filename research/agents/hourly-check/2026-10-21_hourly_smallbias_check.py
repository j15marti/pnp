import itertools
k=4;q=16;poly=0b10011  # x^4+x+1 irreducible
def mul(a,b):
    r=0
    while b:
        if b&1:r^=a
        b>>=1;a<<=1
        if a&q:a^=poly
    return r
def tr(x):
    t=0;y=x
    for _ in range(k):
        t^=y;y=mul(y,y)
    return t&1
m=6
seeds=[]
for a in range(q):
    for z in range(q):
        zp=1;bits=[]
        for i in range(m):
            bits.append(tr(mul(a,zp)));zp=mul(zp,z)
        seeds.append(bits)
worst=0
for S in range(1,1<<m):
    s=sum((-1)**(sum(b[i] for i in range(m) if S>>i&1)%2) for b in seeds)/len(seeds)
    assert s>=-1e-12; worst=max(worst,s)
print("max bias",worst,"bound",(m-1)/q)
# L1 norm of OR and quadratic-phase m=6
import math
def L1(f):
    tot=0
    for S in range(1<<m):
        tot+=abs(sum(f(r)*(-1)**(bin(r&S).count('1')%2) for r in range(1<<m)))/2**m
    return tot
OR=lambda r:1 if r else 0
Q=lambda r:1 if (sum((r>>2*j&1)&(r>>(2*j+1)&1) for j in range(3))%2)==0 else 0
print("L1 OR",L1(OR),2-2**(1-m)," L1 Q",L1(Q),0.5+2**(m//2-1))
