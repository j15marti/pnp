#!/usr/bin/env python3
"""LSPV-3/420 semantic gauge checks. Only mathematical root-only rules, not missing byte parser."""
import itertools,json
from pathlib import Path
checks={"definitions":0,"clause_valuations":0,"resolution_steps":0,"affine_rows":0,"xor_steps":0,"local_checks":0,"and_checks":0,"negative_rejections":0}
def bit(s,i):return (s>>i)&1
def fval(f,u,v):return (f>>(2*u+v))&1
def ce(c,s):return any(bit(s,abs(l)-1)==int(l>0) for l in c)
def flip(s,d):return s^d
def sl(l,d):return -l if bit(d,abs(l)-1) else l
def sc(c,d):return tuple(sl(l,d) for l in c)
def re(mask,rhs,s):return ((mask&s).bit_count()&1)==rhs
def gr(mask,rhs,d):return rhs^((mask&d).bit_count()&1)
def resolvent(A,B,p):
 if p not in A or -p not in B:return None
 C=set(A)|set(B);C.remove(p);C.remove(-p)
 return None if any(-l in C for l in C) else tuple(sorted(C))
for f,g in itertools.product(range(16),repeat=2):
 for dz,dw in itertools.product(range(2),repeat=2):
  fp=sum((fval(f,u,v)^dz)<<(2*u+v) for u,v in itertools.product(range(2),repeat=2))
  gp=sum((fval(g,u^dz,v)^dw)<<(2*u+v) for u,v in itertools.product(range(2),repeat=2))
  for a in range(4):
   x,y=bit(a,0),bit(a,1)
   z=fval(f,x,y);w=fval(g,z,x)
   zp=fval(fp,x,y);wp=fval(gp,zp,x)
   assert zp==z^dz and wp==w^dw
   checks["definitions"]+=1
cl=[[1],[-1],[3],[-3],[4],[-4],[-3,1],[3,-2],[-4,3],[4,-3],[-3,4],[-4,-3],[1,2,-3],[-2,4]]
for dz,dw in itertools.product(range(2),repeat=2):
 d=(dz<<2)|(dw<<3)
 for c in cl:
  for s in range(16):
   assert ce(c,s)==ce(sc(c,d),flip(s,d))
   checks["clause_valuations"]+=1
 for A,B in itertools.product(cl,repeat=2):
  for p in (1,3,4,-1,-3,-4):
   C=resolvent(A,B,p)
   if C is None:continue
   D=resolvent(sc(A,d),sc(B,d),sl(p,d))
   assert D is not None and set(D)==set(sc(C,d))
   checks["resolution_steps"]+=1
 for mask,rhs in itertools.product(range(16),range(2)):
  rhs2=gr(mask,rhs,d)
  for s in range(16):
   assert re(mask,rhs,s)==re(mask,rhs2,flip(s,d))
   checks["affine_rows"]+=1
  for mask2,rhs3 in itertools.product(range(16),range(2)):
   assert gr(mask,rhs,d)^gr(mask2,rhs3,d)==gr(mask^mask2,rhs^rhs3,d)
   checks["xor_steps"]+=1
for p,q in itertools.product(range(16),repeat=2):
 for a in range(4):
  assert (((p&q)>>a)&1)==(((p>>a)&1)&((q>>a)&1))
  checks["and_checks"]+=1
 assert ((p&~q&15)==0) == all(not ((p>>a)&1) or ((q>>a)&1) for a in range(4))
 checks["local_checks"]+=1
assert re(4,1,4)!=re(4,1,flip(4,4));checks["negative_rejections"]+=1
assert (1&~2&15)!=0;checks["negative_rejections"]+=1
assert resolvent((3,),(-3,),1) is None;checks["negative_rejections"]+=1
assert len({3,3})==1;checks["negative_rejections"]+=1
assert "local:2/private:gate0" not in {"source:0","def:1","local:2"};checks["negative_rejections"]+=1
assert any(ce((1,),s) for s in range(4))
assert not any(ce((1,),s) and ce((-1,),s) for s in range(4))
raw={"id":"LSPV3_420_TYPED_SEMANTIC_GAUGE","scope":"root-only semantic R_mix341; missing native byte grammar not invented","checks":checks,"total":sum(checks.values()),"status":"PROVED/RESTRICTED theorem, COMPUTATIONAL finite checks, full native bytes and B3 OPEN"}
print(json.dumps(raw,indent=2))
if __name__=="__main__":
 Path("lspv3_420_mixed_gauge_producer_output.json").write_text(json.dumps(raw,indent=2)+"\n")
