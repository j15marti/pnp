#!/usr/bin/env python3
"""Self-contained canonical width-one support theorem control (Python 3)."""
from collections import Counter
P=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
Q=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
T=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
F=P+[tuple(-i for i in c) for c in Q]
G=T+[tuple(-i for i in c) for c in T]
H=F+[tuple((abs(i)+9)*(1 if i>0 else -1) for i in c) for c in G]
def valid(C,n):
 if len(C)*3!=4*n or len({tuple(sorted(c)) for c in C})!=len(C):return False
 a=Counter()
 for c in C:
  if len(c)!=3 or len({abs(x) for x in c})!=3 or any(x==0 or abs(x)>n for x in c):return False
  if not (all(x>0 for x in c) or all(x<0 for x in c)):return False
  for x in c:a[abs(x),x>0]+=1
 return all(a[i,b]==2 for i in range(1,n+1) for b in (False,True))
def models(C,n):
 return [v for v in range(1<<n) if all(any(((v>>(abs(x)-1))&1)==int(x>0) for x in c) for c in C)]
def fiber(M,pins,b):
 return [sum(all(((v>>(i-1))&1)==a for i,a in pins.items()) and ((v>>(b-1))&1)==z for v in M) for z in (0,1)]
assert valid(F,9) and valid(G,6) and valid(H,15)
fm,gm,hm=models(F,9),models(G,6),models(H,15)
assert (len(fm),len(gm),len(hm))==(70,18,1260)
assert fiber(gm,{},1)==[9,9]
p={1:0,3:0,5:1,6:0,7:0,8:0}
q={**p,1:1}
a={1:1,2:0,3:0}
b={1:1,2:1,3:0}
expected={'root':[630,630],'SAT_cube':[18,18],'UNSAT_cube':[0,0],
 'same_boundary_P':[72,72],'same_boundary_Q':[72,72],
 'future_P':[0,0],'future_Q':[18,18]}
checks={'root':{},'SAT_cube':p,'UNSAT_cube':q,'same_boundary_P':a,'same_boundary_Q':b,
 'future_P':{**a,6:1},'future_Q':{**b,6:1}}
for name,pins in checks.items():assert fiber(hm,pins,10)==expected[name]
assert not valid([F[0],F[0]]+F[2:],9)
assert not valid([(-1,5,6)]+F[1:],9)
assert not valid([(1,1,6)]+F[1:],9)
print('PASS',len(hm),'models; width-1 SAT/UNSAT and continuation fibers:',expected)
