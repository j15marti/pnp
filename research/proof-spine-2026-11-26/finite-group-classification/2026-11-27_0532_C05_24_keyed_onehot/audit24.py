"""Independent row-syndrome checks: no Gaussian quotient code imported here."""
import random,json,itertools
from collections import defaultdict
from fractions import Fraction
rng=random.Random(26112724); checks=0;cases=0;nonempty=0
for p in (2,3,5,101,2305843009213693951):
 for _ in range(200):
  u=rng.randint(1,9);v=rng.randint(1,9);r=rng.randint(1,4)
  # random repeated keys; choose target to ensure some nonempty controls
  vals=[tuple(rng.randrange(min(p,3)) for _ in range(r)) for _ in range(rng.randint(1,5))]
  L=[rng.choice(vals) for _ in range(u)];R=[rng.choice(vals) for _ in range(v)];b=tuple((a+c)%p for a,c in zip(rng.choice(L),rng.choice(R))) if _%2==0 else tuple(rng.randrange(min(p,5)) for i in range(r))
  D=defaultdict(list)
  for j,s in enumerate(R):D[tuple((x-y)%p for x,y in zip(b,s))].append(j)
  got={(i,j) for i,s in enumerate(L) for j in D[s]};expected={(i,j) for i in range(u) for j in range(v) if all((L[i][k]+R[j][k])%p==b[k] for k in range(r))};assert got==expected;cases+=1;checks+=u*v;nonempty+=bool(got)
  # independent row consistency: for each possible pair, compare key conservation equations.
  keys=set(L)|{tuple((x-y)%p for x,y in zip(b,s)) for s in R}
  for i in range(u):
   for j in range(v):
    assert ((i,j) in got)==all((L[i]==k)==(tuple((x-y)%p for x,y in zip(b,R[j]))==k) for k in keys)
# hostile generic non-affine support path: its edge-affine hull also contains omitted (0,1)
assert (0b0101^0b0110^0b1010)==0b1001
print(json.dumps(dict(primes=5,cases=cases,pair_checks=checks,nonempty=nonempty,hostile_path=True)))
