import itertools,json
from pathlib import Path
rows=[]
for n in range(2,10):
 for family in ("and","parity","xor_unsat","tautology"):
  def f(a):
   if family=="and":return all(a)
   if family=="parity":return sum(a)%2==1
   if family=="xor_unsat":return a[0]==a[1] and a[0]!=a[1]
   return True
  b=any(f(a) for a in itertools.product((0,1),repeat=n))
  prefix=();calls=1
  for i in range(n):
   b0=any(f(prefix+(0,)+t) for t in itertools.product((0,1),repeat=n-i-1))
   calls+=1;prefix+=(0 if b0==b else 1,)
   assert any(f(prefix+t) for t in itertools.product((0,1),repeat=n-i-1))==b
  assert calls==n+1
  rows.append(dict(n=n,family=family,calls=calls,final_answer=b))
print(json.dumps(dict(status="COMPUTATIONAL",tested=len(rows),rows=rows),indent=2))
