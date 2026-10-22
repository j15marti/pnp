"""Independent check of Lemma 77B: p_max root of p*s = d_F(p*c), d_F(x)=((x+2)/x^2 - x)/2."""
from fractions import Fraction
import json
def dF(x): return ((x+2)/x**2 - x)/2
def pmax(c,s):
    lo,hi=1.0,2.0
    f=lambda p: p*s-dF(p*c)
    assert f(lo)<0<f(hi)
    for _ in range(200):
        m=(lo+hi)/2
        (lo,hi)=(m,hi) if f(m)<0 else (lo,m)
    return lo
out=[]
for name,c,s,b in [("baseline",1.2,.5,.5),("safe",1.205,.5,.5),("retuned",1.2021,.505,.505)]:
    p=pmax(c,s); out.append(dict(name=name,c=c,s=s,beta=b,pmax=p,beta_pmax=b*p))
print(json.dumps(out,indent=1))
