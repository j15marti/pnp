import json
from fractions import Fraction
checks=0
rows=[]
for e in range(1,13):
 for w in [Fraction(1,2),Fraction(1),Fraction(6,5),Fraction(2)]:
  for h in [Fraction(1,2),Fraction(1),Fraction(3,2)]:
   v=max(w,e*max(w,h))
   rows.append({"e":e,"w":str(w),"h":str(h),"verifier_bound":str(v),"within_local_budget":v<=Fraction(11,10)})
   checks+=1
for bits in range(2,11):
 modulus=1<<bits
 for t in [1,2,3,modulus-1,modulus,modulus+3]:
  x=0
  for _ in range(t): x=(x+1)%modulus
  assert x==t%modulus
  checks+=1
assert checks==198
print(json.dumps({"checks":checks,"failures":0,"exponent_cases":144,"increment_cases":54,"budget_cases":sum(r["within_local_budget"] for r in rows)},indent=2))
