from itertools import product
for k in (2,3):
 for t in product(range(k),repeat=2*k):
  D=[t[2*i:2*i+2] for i in range(k)]
  for n in (1,2,3):
   N=2**n
   R={(p,D[p][b]):(b,) for p in range(k) for b in (1,0)}
   for i in range(n):
    R={(p,q):R[p,m]+R[m,q] for p in range(k) for q in range(k) for m in range(k) if (p,m) in R and (m,q) in R}
   seen=set()
   for w in product((0,1),repeat=N):
    q=0
    for b in w:q=D[q][b]
    seen.add(q)
   assert seen=={q for p,q in R if p==0}
   for (p,q),w in R.items():
    z=p
    for b in w:z=D[z][b]
    assert z==q and len(w)==N
print('passed')
