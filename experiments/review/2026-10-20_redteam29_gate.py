#!/usr/bin/env python3
from fractions import Fraction as F
checks=0
for n in range(2,16):
 t=2**n
 for m in [t+1,t+2,2*t+1,4*t+1]:
  b=(m-1).bit_length();L=m*b
  assert m>t and L>=t*b and t<=L//b
  checks+=3
rhos=[F(1,4),F(1,3),F(1,2),F(3,5),F(2,3),F(3,4),F(4,5),F(1)]
time_fail=space_fail=0
for r in rhos:
 for c in range(1,65):
  for d in range(1,65):
   tb=r*c>max(F(11,10),F(3,5)+F(c,2))
   sb=r*d>max(F(1,2),F(d,2))
   if r<=F(1,2):assert not tb and not sb
   time_fail+=tb;space_fail+=sb
assert checks==168 and time_fail==19584 and space_fail==20480
print(dict(table_assertions=checks,grid_pairs=32768,time_fail=time_fail,space_fail=space_fail,p_vs_np="OPEN"))
