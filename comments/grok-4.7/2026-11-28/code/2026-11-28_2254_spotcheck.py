#!/usr/bin/env python3
"""Grok 4.7 spot-checks of numeric claims in T2 (dcadee6) and C04-39 (8de4131) reports."""
from fractions import Fraction as F
import itertools
dot = lambda x, y: sum(a*b for a, b in zip(x, y))
u=(1,1,-1,-1,0); v=(1,-1,-1,0,1); c=(1,0,-1,0,0)
D=dot(u,u)*dot(v,v)-dot(u,v)**2
al=dot(v,v)*dot(u,c)-dot(u,v)*dot(v,c); be=dot(u,u)*dot(v,c)-dot(u,v)*dot(u,c)
r=tuple(D*ci-al*ui-be*vi for ci,ui,vi in zip(c,u,v))
print("T2 Lemma A example: D=%d alpha=%d beta=%d r=%s L1=%d (<2D=%d: %s) 5||r||^2=%d (<(2D)^2=%d: %s)"%(D,al,be,r,sum(map(abs,r)),2*D,sum(map(abs,r))<2*D,5*dot(r,r),(2*D)**2,5*dot(r,r)<(2*D)**2))
# r orthogonal to u,v (projector residual)
print("  r.u=%d r.v=%d"%(dot(r,u),dot(r,v)))
# Gram identity on random integer r and spins
import random
rng=random.Random(1); ok=True
for _ in range(2000):
    k=rng.randint(1,6); rr=[rng.randint(-5,5) for _ in range(k)]; y=[rng.choice((-1,1)) for _ in range(k)]
    L=sum(map(abs,rr))*sum(abs(a)*b*b for a,b in zip(rr,y))-dot(rr,y)**2
    R=sum(abs(rr[i]*rr[j])*(y[i]-(1 if rr[i]*rr[j]>0 else -1)*y[j])**2 for i in range(k) for j in range(i+1,k) if rr[i]*rr[j]!=0)
    ok&=(L==R)
print("T2 diagonal Gram identity 2000 random checks:", ok)
# NO PSD control
u2=(2,1,1); v2=(2,1,-1)
Q=[[u2[i]*u2[j]+v2[i]*v2[j] for j in range(3)] for i in range(3)]
w=(2,1,0)
print("T2 NO PSD control: Q-diag(0,0,2) == 2 w w^T:", all(Q[i][j]-(2 if i==j==2 else 0)==2*w[i]*w[j] for i in range(3) for j in range(3)))
# C04-38 exported polynomial
p=lambda x41,x208,x416: -2*x41*x208+x208*x416+x416
vals={z:p(*z) for z in itertools.product((0,1),repeat=3)}
print("C04-38 polynomial values:", vals, "negative only at (1,1,0):", [z for z,v in vals.items() if v<0]==[(1,1,0)])
