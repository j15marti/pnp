#!/usr/bin/env python3
"""TARGET-SCOPE278 compact independent checker. Full source/proof/ledger in run ZIP.
Usage: python compact278.py [path_to_Doecker61_original_source.txt]
stdlib only. P versus NP remains OPEN.
"""
import ast,collections,itertools,sys
Yp=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
Yn=[(1,2,4),(1,3,6),(2,3,5),(4,5,6)]
Zp=[(2,4,9),(1,5,8),(3,4,7),(3,6,7),(2,5,8),(1,6,9)]
Zn=[(1,3,6),(4,5,7),(3,6,9),(1,2,8),(2,4,8),(5,7,9)]
W="001110010011110001010001110100111110011011000101000101001010100001011010101011000100000111001010110101001110001001101000110001100010100101101110010101011001001100000110111001001101001101101001010101"
def source(P,Q):return [list(x) for x in P]+[[-v for v in row] for row in Q]
def valid(F):
 if not isinstance(F,list) or not F or any(len(c)!=3 or len({abs(v) for v in c})!=3 or len({v>0 for v in c})!=1 for c in F):return False
 if len({tuple(sorted(c)) for c in F})!=len(F):return False
 n=max(abs(z) for c in F for z in c)
 a=collections.Counter((abs(z),z>0) for c in F for z in c)
 return len(F)*3==4*n and all(a[v,s]==2 for v in range(1,n+1) for s in (True,False))
def satisfy(F,a):
 return all(any(a[abs(z)]==(z>0) for z in c) for c in F)
def feasible(c,d):
 out=[]
 for t,u in itertools.product((1,0),repeat=2):
  a={};good=True
  for row,mode in ((c,t),(d,u)):
   for z in row:
    b=(z>0) if mode else (z<0)
    if abs(z) in a and a[abs(z)]!=b:good=False
    a[abs(z)]=b
  out.append(good)
 return out
def audit(F):
 assert valid(F)
 n=max(abs(z) for c in F for z in c);m=len(F)
 assert m*3==n*4
 for flag in (0,1):
  a={v:bool(flag) for v in range(1,n+1)}
  assert sum(not any(a[abs(z)]==(z>0) for z in c) for c in F)==2*n//3
 count=0;wide=0
 for j,c in enumerate(F):
  for d in F[j+1:]:
   q=feasible(c,d);assert sum(q)>=2
   if any(z in d for z in (-c[0],-c[1],-c[2])):
    shared=len({abs(z) for z in c}&{abs(z) for z in d})
    if shared==1:wide+=1
   count+=1
 for bit in (False,True):
  residual=[tuple(z for z in c if abs(z)!=1) for c in F if not any(abs(z)==1 and ((z>0)==bit) for z in c)]
  assert sum(len(c)==2 for c in residual)==2
 return n,m,count,wide
def small(F):
 n=max(abs(z) for c in F for z in c)
 return sum(satisfy(F,{v:bool(t[v-1]) for v in range(1,n+1)}) for t in itertools.product((0,1),repeat=n))
def main():
 A=source(Yp,Yn);B=source(Zp,Zn)
 assert small(A)==20 and small(B)==93
 assert all(sum(x in (5,7,9) for x in c)==1 for c in Zp)
 assert (5,7,9) in Zn
 assert satisfy(B,{v:(v in (1,2,3)) for v in range(1,10)})
 assert not valid(A+[A[0]]) and not valid(A[:-1])
 print("Y6",audit(A),"Z9",audit(B))
 if len(sys.argv)>1:
  raw=open(sys.argv[1],encoding="utf8").read();U=ast.literal_eval(raw[raw.index("[["):])
  V=[list(c) for c in U];assert V[2]==[1,2,197] and V[44]==[33,34,196]
  V[2][-1]=196;V[44][-1]=197
  assert len(W)==198 and satisfy(V,{i+1:(v=="1") for i,v in enumerate(W)})
  assert not satisfy(U,{i+1:(v=="1") for i,v in enumerate(W)})
  print("U198 original",audit(U),"V198 original-derived SAT",audit(V))
 print("Restricted syntax checks PASS; no all-target polynomial algorithm or ARC/FLMV proof.")
if __name__=="__main__":main()
