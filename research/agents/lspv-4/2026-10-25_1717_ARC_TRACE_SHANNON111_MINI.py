#!/usr/bin/env python3
"""Two-level exact trace-order Shannon and M22 restriction audit; stdlib only."""
from itertools import product
P=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
M=((-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
def chain(n):
 c=[]
 for i in range(n):
  c += [tuple(v+6*i for v in x) for x in P]
  c += [tuple(v-6*i for v in x) for x in M]
 for i in range(n-1):
  j=8*i+1;h=8*(i+1);a=list(c[j]);b=list(c[h])
  x=6*i+1;y=6*(i+1)+1
  a[a.index(x)]=y;b[b.index(y)]=x;c[j]=tuple(a);c[h]=tuple(b)
 return tuple(c)
def restrict(f,v,b):
 return tuple(tuple(x for x in c if x!=(-v if b else v))
              for c in f if (v if b else -v) not in c)
def sat(f):
 vs=sorted({abs(x) for c in f for x in c})
 for z in product((False,True),repeat=len(vs)):
  a=dict(zip(vs,z))
  if all(any(a[abs(x)]==(x>0) for x in c) for c in f):return True
 return False
def split(f,d,back):
 if not f:return True
 if d==0:return sat(f)
 c=f[-1] if back else f[0]
 if not c:return False
 v=abs(c[-1] if back else c[0])
 return split(restrict(f,v,0),d-1,back) or split(restrict(f,v,1),d-1,back)
def run():
 count=0
 universe=[tuple(-(j+1) if row>>j&1 else j+1 for j in range(3)) for row in range(8)]
 for mask in range(256):
  f=tuple(c for j,c in enumerate(universe) if mask>>j&1)
  for back in (False,True):
   assert split(f,2,back)==sat(f);count+=1
 for p in (1,2,4,8,16,32):
  f=chain(p)
  a={6*i+j:(j<=3) for i in range(p) for j in range(1,7)}
  assert all(any(a[abs(x)]==(x>0) for x in c) for c in f);count+=1
  for back in (False,True):
   v=abs(f[-1][-1] if back else f[0][0])
   for b in (0,1):
    g=restrict(f,v,b);w=abs(g[-1][-1] if back else g[0][0])
    for b2 in (0,1):
     h=restrict(g,w,b2)
     unchanged=sum(all(abs(x) not in (v,w) for x in c) for c in f)
     assert unchanged>=len(f)-8;count+=1
 return {'checks':count,'failures':0}
if __name__=='__main__':print(run())
