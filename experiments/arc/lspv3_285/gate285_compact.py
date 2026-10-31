#!/usr/bin/env python3
"""GATE285 exact standalone fixed-weight directional matching controls (no dependencies)."""
import functools
F={
'Y6':[[1,2,3],[1,4,5],[2,4,6],[3,5,6],[-1,-2,-4],[-1,-3,-6],[-2,-3,-5],[-4,-5,-6]],
'K33':[[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[-1,-5,-9],[-1,-6,-8],[-2,-4,-9],[-2,-6,-7],[-3,-4,-8],[-3,-5,-7]],
'CUBE12':[[1,2,3],[1,4,5],[2,6,7],[4,6,8],[3,9,10],[5,9,11],[7,10,12],[8,11,12],[-1,-9,-11],[-5,-7,-8],[-4,-6,-10],[-3,-6,-11],[-1,-2,-3],[-2,-8,-12],[-4,-9,-12],[-5,-7,-10]]}
def sat(cs,a):
 return all(any(bool(a>>(abs(z)-1)&1)==(z>0) for z in c) for c in cs)
def cover(cs,a,positive):
 bad=[c for c in cs if (c[0]>0)==positive and not any(bool(a>>(abs(z)-1)&1)==(z>0) for z in c)]
 masks={}
 for i,c in enumerate(bad):
  for z in c:masks[abs(z)]=masks.get(abs(z),0)|(1<<i)
 @functools.lru_cache(None)
 def rec(left):
  if not left:return 0
  i=(left&-left).bit_length()-1
  return 1+min(rec(left&~masks[abs(z)]) for z in bad[i])
 return rec((1<<len(bad))-1)
def run():
 out={}
 for name,f in F.items():
  n=max(abs(z) for c in f for z in c)
  assert len(f)*3==4*n
  assert all(sum(z in c for c in f)==2 and sum(-z in c for c in f)==2 for z in range(1,n+1))
  assert all(len({abs(z) for z in c})==3 for c in f)
  models=[b for b in range(1<<n) if sat(f,b)]
  rhos=[(cover(f,a,True),cover(f,a,False)) for a in range(1<<n)]
  swaps=0;bounds=0
  for a,(p,q) in enumerate(rhos):
   for b in models:
    u=((~a)&b&((1<<n)-1)).bit_count();v=(a&(~b)).bit_count()
    assert u>=p and v>=q
    d=b.bit_count()-a.bit_count()
    assert (a^b).bit_count()>=p+q+abs(d-(p-q));bounds+=1
   for i in range(n):
    if not (a>>i)&1:continue
    for j in range(n):
     if (a>>j)&1:continue
     r,s=rhos[a^(1<<i)^(1<<j)]
     assert abs(p-r)<=1 and abs(q-s)<=1
     assert abs(max(p,q)-max(r,s))<=1
     swaps+=1
  out[name]={'n':n,'m':len(f),'models':len(models),'bounds_checked':bounds,'swap_consistency_checks':swaps,'zero_directed_cover':rhos[0],'one_directed_cover':rhos[-1]}
 f=F['CUBE12'];a=27;p,q=cover(f,a,True),cover(f,a,False)
 best=min((a^b).bit_count()//2 for b in range(1<<12) if b.bit_count()==4 and sat(f,b))
 assert (p,q,best)==(2,0,2)
 out['strict_improvement']={'CUBE12_anchor':27,'weight':4,'rho_positive':p,'rho_negative':q,'undirected_half':(p+q+1)//2,'directional':max(p,q),'true_min_swaps':best}
 print(out)
if __name__=='__main__':run()
