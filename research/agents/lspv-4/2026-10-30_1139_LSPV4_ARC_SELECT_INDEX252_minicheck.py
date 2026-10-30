from fractions import Fraction as F
from math import ceil,log2
def flmv(c):
    f=F(1); best=F(-100); winner=0
    for k in range(1,100):
        f=c*f/(1+f)
        d=min((1/f-c)/k,c**(-k))
        if d>best: best,winner=d,k
        if k>=2 and c**(-(k+1))<best:
            return (winner,best,k)
    raise AssertionError("tail not certified")
assert flmv(F(6,5))==(2,F(23,45),3)
assert flmv(F(241,200))==(2,F(11642479,23232400),3)
def checkpoint(bits,h):
    prefix=[0]
    for i in range(0,len(bits),h):
        prefix.append(prefix[-1]+sum(bits[i:i+h]))
    def select(j):
        seen=0
        for block in range(len(prefix)-1):
            if prefix[block+1]<j: continue
            seen=prefix[block]
            for index in range(block*h,min(len(bits),(block+1)*h)):
                seen+=bits[index]
                if bits[index] and seen==j:return index
        raise AssertionError("missing survivor")
    return prefix,select
for m in (64,128,256,512,1024):
    w=ceil(log2(m+1)); N=m*ceil(log2(m+2))
    h=next(h for h in range(1,m+1) if ceil(m/h)*w<=int(N**.5))
    bits=[int(i%h==h-1) for i in range(m)]
    pref,query=checkpoint(bits,h)
    assert len(pref)-1==ceil(m/h)
    for j,pos in enumerate([i for i,b in enumerate(bits) if b],1):
        assert query(j)==pos
print("PASS: FLMV exact tail and checkpoint SELECT checks")
