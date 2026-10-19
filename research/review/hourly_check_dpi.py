# Independent check of the Markov-postprocessing claim (alpha=1/2 toy model assumed:
# each of r coordinates reveals source bit x w.p. alpha, else erased '?').
# Verifies TV(f(T|x=0), f(T|x=1)) <= 1-(1-alpha)^r for random compressors f.
import itertools, random
from fractions import Fraction as F
a=F(1,2)
def dist(r,x):
    d={}
    for t in itertools.product([0,1,'?'],repeat=r):
        p=F(1)
        for s in t:
            p*= (1-a) if s=='?' else (a if s==x else 0)
        if p: d[t]=p
    return d
worst=0;n=0
random.seed(1)
for r in (1,2,3):
    d0,d1=dist(r,0),dist(r,1); T=sorted(set(d0)|set(d1),key=str)
    bound=1-(1-a)**r
    for _ in range(3000):
        k=random.choice([2,3,4])
        f={t:random.randrange(k) for t in T}
        tv=sum(abs(sum(d0.get(t,0) for t in T if f[t]==y)-sum(d1.get(t,0) for t in T if f[t]==y)) for y in range(k))/2
        assert tv<=bound; worst=max(worst,tv/bound); n+=1
print(n,"compressors, max tv/bound =",float(worst))
