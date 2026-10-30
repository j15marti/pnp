from fractions import Fraction as F
W='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
C=[tuple(map(int,x.split())) for x in W.split(';')]
D=[list(c) for c in C]
assert D[7][0]==1 and D[19][0]==-1
D[7][0]=-1;D[19][0]=1
def sat(cs,a):
    return all(any(bool((a>>(abs(l)-1))&1)==(l>0) for l in c) for c in cs)
assert sum(sat(C,a) for a in range(32768))==0
assert sum(sat(D,a) for a in range(32768))==168
assert sat(D,97)
def dstar(c):
    def f(k):return (c-1)/(1-(2-c)/(c**k))
    best=F(0)
    for k in range(1,100):
        d=min((1/f(k)-c)/k,c**(-k))
        best=max(best,d)
        if c**(-(k+1))<best:return best,k
    raise AssertionError('tail')
for c,v in ((F(6,5),F(23,45)),(F(241,200),F(11642479,23232400)),
            (F(7,5),F(949,5145)),(F(3,2),F(49,648)),
            (F(8,5),F(2145161,335544320))):
    got,k=dstar(c)
    assert got==v
assert F(11642479,23232400)-F(1,2)==F(26279,23232400)
assert (F(241,200)-F(6,5))/2==F(1,400)
assert F(241,200)-F(3,5)-F(1,2)==F(21,200)
for m in (8,16,64):
    for D in (2,3,4):
        p=m**D
        assert p>=m and p+1>m and p.bit_length()<=D*m.bit_length()
print('PASS: 2x32768 matched assignments, five rational FLMV envelopes with certified infinite tails, nine far-input counterexamples')
