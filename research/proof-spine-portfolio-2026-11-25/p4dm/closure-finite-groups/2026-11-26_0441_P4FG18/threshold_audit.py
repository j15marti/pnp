import itertools as I, random, json
from fractions import Fraction
from fg18 import local,offset,bits,old
from scipy.optimize import linprog
# Independent exact rational common-threshold check for incomparable translated modes.
rng=random.Random(2611261803);checks=0;strict=0;fractional=0
for _ in range(1500):
 p=rng.randrange(2);L=[x for x in range(16) if x.bit_count()%2==p]
 f={x:rng.randrange(-5,6) for x in L if rng.random()<.5}
 if not f:continue
 s=next((s for s in I.product((1,-1),repeat=4) if local(f,s)),None)
 if s is None:continue
 modes={offset(x,s):c for x,c in f.items()};T={tuple(a+t for a in x):c for x,c in modes.items() for t in range(-5,6) if all(-5<=a+t<=5 for a in x)}
 if not T:continue
 words=rng.choices(list(T),k=5);weights=[rng.randrange(1,10) for _ in words];total=sum(weights)
 q={(i,t):Fraction(sum(w for x,w in zip(words,weights) if x[i]>=t),total) for i in range(4) for t in range(-4,6)}
 cut=sorted(set(q.values())|{Fraction(0),Fraction(1)})
 avg=Fraction(sum(w*T[x] for w,x in zip(weights,words)),total);value=Fraction(0)
 for a,b in zip(cut,cut[1:]):
  theta=(a+b)/2;x=tuple(-5+sum(q[i,t]>=theta for t in range(-4,6)) for i in range(4));assert x in T;value+=(b-a)*T[x]
 assert value<=avg
 checks+=1;strict+=value<avg;fractional+=any(0<v<1 for v in q.values())
# Counterexample: all three pairwise supports full Boolean lattice, antiferromagnetic costs.
# Local distributions each 1/2 on 01 and 10 have shared threshold marginals 1/2 and cost 0.
# Any 3-bit integral word has equal pair. Exact true optimum is 1.
true=min(sum(x[i]==x[j] for i,j in ((0,1),(1,2),(2,0))) for x in I.product((0,1),repeat=3));assert true==1
res={'seed':2611261803,'checks':checks,'fractional':fractional,'strict_improvements':strict,'non_submodular_triangle_lp':0,'non_submodular_triangle_opt':true}
print(res);json.dump(res,open('threshold_results.json','w'),indent=2)
