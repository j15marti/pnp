# Independent exhaustive check of CHMY-FIELDPAIR-CRITICAL4 Sec.4-5 (pair theorem, second moment). <1s per h.
from fractions import Fraction as F
from math import gcd
from itertools import combinations
POLY={3:0b1011,4:0b10011,5:0b100101,6:0b1000011}
def mul(a,b,h):
    r=0
    while b:
        if b&1: r^=a
        b>>=1; a<<=1
        if a>>h&1: a^=POLY[h]
    return r
def pw(a,j,h):
    r=1
    for _ in range(j): r=mul(r,a,h)
    return r
par=lambda x:bin(x).count('1')&1
bad=0
for h in (3,4,5,6):
    Q=1<<h; N=2*Q
    T={j:{(a,b):par(pw(a,j,h)&b) for a in range(Q) for b in range(Q)} for j in range(1,N)}
    for j,k in combinations(range(1,N),2):
        d=gcd(abs(j-k),Q-1)
        r=F(sum(T[j][s]&T[k][s] for s in T[j]),Q*Q)
        if r!=F(Q-1+d,4*Q): bad+=1
    for j in T:
        if F(sum(T[j].values()),Q*Q)!=F(Q-1,2*Q): bad+=1
    # second moment, S=residue class + extras, t=2 layers (independent pairs)
    S=[1,1+(Q-1),2,5]; t=2
    p=F(Q-1,2*Q)
    # exact E Z^2 for t independent layers = sum_{j,l} r_jl^t
    def r(j,l):
        return p if j==l else F(Q-1+gcd(abs(j-l),Q-1),4*Q)
    pred=sum(r(j,l)**t for j in S for l in S)
    # brute force over two layers
    keys=list(T[1]); tot=0
    for s1 in keys:
        for s2 in keys:
            z=sum(T[j][s1]&T[j][s2] for j in S); tot+=z*z
    if F(tot,(Q*Q)**2)!=pred: bad+=1; print('2nd moment fail',h)
    print('h',h,'ok so far, bad=',bad)
print('TOTAL FAILURES',bad)
