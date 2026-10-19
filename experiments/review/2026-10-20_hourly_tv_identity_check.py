"""Independent brute-force check of the public-seed TV identity and erasure-tax copy bound."""
import itertools, json, math, random
from fractions import Fraction as Fr
random.seed(20261020)
def tv(P,Q):
    ks=set(P)|set(Q); return sum(abs(P.get(k,0)-Q.get(k,0)) for k in ks)/2
fails=0; trials=0
for _ in range(300):
    nz=random.randint(1,6); outs=random.randint(2,4)
    phi=[[random.randrange(outs) for _ in range(nz)] for _ in range(2)]  # phi[b][z]
    w=[Fr(random.randint(1,5)) for _ in range(nz)]; s=sum(w); w=[x/s for x in w]
    P=[{(z,phi[b][z]):w[z] for z in range(nz)} for b in (0,1)]
    alpha=sum(w[z] for z in range(nz) if phi[0][z]!=phi[1][z])
    trials+=1; fails+= tv(P[0],P[1])!=alpha
    # r independent copies (independent seeds)
    for r in (2,3):
        def prod(b):
            d={}
            for zs in itertools.product(range(nz),repeat=r):
                pr=Fr(1)
                for z in zs: pr*=w[z]
                key=tuple((z,phi[b][z]) for z in zs); d[key]=d.get(key,0)+pr
            return d
        trials+=1; fails+= tv(prod(0),prod(1))!=1-(1-alpha)**r
# minimal r for TV>=1/3
tab={}
for a in (Fr(1,16),Fr(1,8),Fr(3,16),Fr(1,100)):
    r=1
    while 1-(1-a)**r<Fr(1,3): r+=1
    ok=r==math.ceil(math.log(2/3)/math.log(1-float(a)))
    tab[str(a)]=(r,ok); fails+= (not ok)
print(json.dumps({"trials":trials,"fails":fails,"min_copies":tab}))
json.dump({"trials":trials,"fails":fails,"min_copies":tab},open("results/raw/hourly/2026-10-20_hourly_tv_identity_check.json","w"))
