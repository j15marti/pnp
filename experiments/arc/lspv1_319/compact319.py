"""CIRCUIT-DIFFERENCE-MITER319 compact source-original reproducer."""
from itertools import product
from collections import Counter
import json
P9=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
N9=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
P6=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
N6=[(1,2,4),(1,3,6),(2,3,5),(4,5,6)]
def cnf(p,n):return list(p)+[tuple(-v for v in t) for t in n]
F9=cnf(P9,N9);Y6=cnf(P6,N6)
H15=F9+[tuple(v+9 if v>0 else v-9 for v in c) for c in Y6]
def valid(f,n):
 if 3*len(f)!=4*n:return False
 count=Counter();seen=set()
 for c in f:
  if len(c)!=3 or len({abs(v) for v in c})!=3 or any(not 1<=abs(v)<=n for v in c):return False
  if not(all(v>0 for v in c) or all(v<0 for v in c)):return False
  k=tuple(sorted(c))
  if k in seen:return False
  seen.add(k)
  for v in c:count[abs(v),v>0]+=1
 return all(count[v,s]==2 for v in range(1,n+1) for s in (True,False))
def sat(f,a):return all(any(a[abs(v)]==(v>0) for v in c) for c in f)
def miter(f,a,x):
 core=[c for c in f if all(abs(v)!=x for v in c)]
 plus=[c for c in f if x in c];minus=[c for c in f if -x in c]
 assert len(plus)==len(minus)==2
 val=lambda c:any(a[abs(v)]==(v>0) for v in c if abs(v)!=x)
 A=all(val(c) for c in plus);B=all(val(c) for c in minus)
 return all(any(a[abs(v)]==(v>0) for v in c) for c in core) and (A!=B)
def measure(f,n,x,p={}):
 assert valid(f,n)
 free=[v for v in range(1,n+1) if v!=x and v not in p]
 a0=a1=diff=0
 for bits in product((0,1),repeat=len(free)):
  a={**p,**dict(zip(free,bits))}
  a[x]=0;v0=sat(f,a);a[x]=1;v1=sat(f,a)
  d=miter(f,a,x);assert d==(v0!=v1)
  a0+=v0;a1+=v1;diff+=d
 return [a0,a1,diff,3*len(f)-3]
ps={1:0,3:0,5:1,6:0,7:0,8:0};pu={**ps,1:1}
res={'Y6':measure(Y6,6,1),'F9':measure(F9,9,1),
 'F9_forward_reverse':measure(F9,9,7,{2:0,3:0,6:1}),
 'H15':measure(H15,15,10),'H15_S':measure(H15,15,10,ps),
 'H15_U':measure(H15,15,10,pu)}
assert res=={'Y6':[10,10,12,21],'F9':[40,30,46,33],
'F9_forward_reverse':[0,1,1,33],'H15':[700,700,840,57],
'H15_S':[20,20,24,57],'H15_U':[0,0,0,57]}
print(json.dumps(res,sort_keys=True,indent=2))
