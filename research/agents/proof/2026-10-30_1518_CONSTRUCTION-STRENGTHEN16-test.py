#!/usr/bin/env python3
"""Local-pair strict22 compiler and charged output access. timeout 25s per mode."""
from collections import Counter,defaultdict
from pathlib import Path
import hashlib,itertools,json,signal,sys
signal.alarm(24)
W=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
Q=W[:7]+W[8:];PORT=(1,7,13)
def gamma(x):
 b=bin(x)[2:];return '0'*(len(b)-1)+b
def sat(F,a):return all(any(a[abs(x)-1]==(x>0) for x in c) for c in F)
def cid(j,d,k):return 12*j+6*d+k+1
def links(F):
 groups=defaultdict(list)
 for j,c in enumerate(F):
  for k,x in enumerate(c):groups[abs(x)].append(3*j+k)
 out=[0]*(3*len(F))
 for row in groups.values():
  for p,q in zip(row,row[1:]+row[:1]):out[p]=q
 return out
class Access:
 def __init__(self,F,link=None):
  self.F=F;self.m=len(F);self.link=link;self.reads=0;self.link_reads=0;self.queries=0;self.comparisons=0
  self.V=72*self.m;self.M=96*self.m;self.w=self.V.bit_length();self.header=gamma(self.V)+gamma(self.M)
 def read(self,p):
  self.reads+=1;return self.F[p//3][p%3]
 def successor(self,j,d,k):
  if d==0:return cid(j,1,k)
  if k==0:return cid((j+1)%self.m,0,0)
  if k>=4:return cid(j,0,k)
  pos=3*j+k-1
  if self.link is not None:
   self.link_reads+=1;q=self.link[pos]
  else:
   v=abs(self.read(pos));q=None
   for delta in range(1,3*self.m+1):
    t=(pos+delta)%(3*self.m);self.comparisons+=1
    if abs(self.read(t))==v:q=t;break
   assert q is not None
  return cid(q//3,0,q%3+1)
 def literal(self,i,l):
  if i<8*self.m:
   block,row=divmod(i,4);j,d=divmod(block,2)
   # tuple(kind, sign factor); source slots preserve original source sign.
   specs=(((0,1),(1,1),(4,1)),((4,-1),(2,1),(3,1)),((0,-1),(1,-1),(5,1)),((5,-1),(2,-1),(3,-1)))
   k,sgn=specs[row][l]
   if 1<=k<=3:sgn*=1 if self.read(3*j+k-1)>0 else -1
   return sgn*cid(j,d,k)
  g,r=divmod(i-8*self.m,22);off=12*self.m+15*g
  if r<3:
   v=3*g+r;j,dk=divmod(v,12);d,k=divmod(dk,6)
   if l==0:return -(v+1)
   if l==1:return self.successor(j,d,k)
   return off+PORT[r]
  x=Q[r-3][l];return (1 if x>0 else -1)*(off+abs(x))
 def bit(self,p):
  self.queries+=1
  if p<len(self.header):return self.header[p]
  p-=len(self.header);i,r=divmod(p,3*(self.w+1));l,b=divmod(r,self.w+1)
  x=self.literal(i,l)
  return str(int(x<0)) if b==0 else str((abs(x)>>(self.w-b))&1)
 def size(self):return len(self.header)+self.M*3*(self.w+1)
def materialize(F):
 # Independent group-key cycle construction; no Access.successor calls.
 m=len(F);out=[];groups=defaultdict(list)
 for j,(a,b,c) in enumerate(F):
  for d in range(2):
   v=[cid(j,d,k) for k in range(6)];s,A,B,C,y,z=v
   A*=1 if a>0 else -1;B*=1 if b>0 else -1;C*=1 if c>0 else -1
   out.extend([(s,A,y),(-y,B,C),(-s,-A,z),(-z,-B,-C)])
   keys=[('s',0),('x',abs(a)),('x',abs(b)),('x',abs(c)),('y',j),('z',j)]
   for key,x in zip(keys,v):groups[key].append(x)
 nxt={}
 for row in groups.values():
  for a,b in zip(row,row[1:]+row[:1]):nxt[a]=b
 for g in range(4*m):
  off=12*m+15*g
  out.extend([(-(3*g+r+1),nxt[3*g+r+1],off+PORT[r]) for r in range(3)])
  out.extend([tuple((1 if x>0 else -1)*(off+abs(x)) for x in c) for c in Q])
 w=(72*m).bit_length()
 bits=gamma(72*m)+gamma(96*m)+''.join(str(int(x<0))+format(abs(x),'0%db'%w) for c in out for x in c)
 return out,bits
def check(F,name):
 out,bits=materialize(F);m=len(F)
 assert len(out)==96*m and len(set(map(frozenset,out)))==len(out)
 assert all(len(set(map(abs,c)))==3 for c in out)
 count=Counter(x for c in out for x in c)
 assert all(count[v]==count[-v]==2 for v in range(1,72*m+1))
 L=links(F);scan=Access(F);linked=Access(F,L)
 for p,b in enumerate(bits):assert scan.bit(p)==linked.bit(p)==b
 # Reverse replay checks real multiplicity; no memoized output.
 for p in range(len(bits)-1,-1,-1):assert scan.bit(p)==linked.bit(p)==bits[p]
 return dict(name=name,m=m,target_bits=len(bits),queries=scan.queries,scan_reads=scan.reads,scan_comparisons=scan.comparisons,linked_source_reads=linked.reads,linked_link_reads=linked.link_reads,index_bits=len(L)*max(1,(len(L)-1).bit_length()),materialized_bits=len(bits))
def local():
 qm=[a for a in itertools.product((0,1),repeat=15) if sat(Q,a)]
 assert len(qm)==244 and all(a[p-1]==0 for a in qm for p in PORT)
 assert sat(Q,(0,)*15)
 assertions=0
 for signs in itertools.product((-1,1),repeat=3):
  for vals in itertools.product((0,1),repeat=3):
   lits=[vals[i] if signs[i]>0 else 1-vals[i] for i in range(3)]
   a,b,c=lits
   for s in (0,1):
    exists=any((s or a or y) and ((not y) or b or c) and ((not s) or (not a) or z) and ((not z) or (not b) or (not c)) for y,z in itertools.product((0,1),repeat=2))
    assert exists==(any(lits) if s==0 else any(not v for v in lits));assertions+=1
 # Wrong links can silently remove inter-occurrence equality.
 F=[(1,2,3),(-1,2,3)];L=links(F);bad=list(range(6))
 good=Access(F,L);wrong=Access(F,bad)
 witness=next(p for p in range(good.size()) if good.bit(p)!=wrong.bit(p))
 F=list(itertools.product((-1,1),(-2,2),(-3,3)))
 assert not any(sat(F,a) for a in itertools.product((0,1),repeat=3))
 bad=Access(F,list(range(24)))
 fake=[tuple(bad.literal(i,l) for l in range(3)) for i in range(bad.M)]
 a=[0]*bad.V
 for j,c in enumerate(F):
  for d in range(2):
   for k,x in enumerate(c,1):a[cid(j,d,k)-1]=int(x>0)
   a[cid(j,d,4)-1]=0;a[cid(j,d,5)-1]=0
 assert sat(fake,a)
 return dict(q_models=len(qm),local_selector_checks=assertions,malformed_link_first_different_bit=witness,multicycle_false_sat=True,multicycle_source_clauses=8)
mode=sys.argv[1] if len(sys.argv)>1 else 'small'
if mode=='local':result=local()
elif mode=='small':
 clauses=list(itertools.product((-1,1),(-2,2),(-3,3)))
 result=[check([clauses[i] for i in range(8) if mask>>i&1],str(mask)) for mask in range(1,256)]
elif mode=='scale':
 result=[]
 for m in [4,8,16,32,64]:
  # Disjoint clauses: source successors wrap to themselves after 3m probes.
  F=[(3*j+1,-(3*j+2),3*j+3) for j in range(m)]
  result.append(check(F,'disjoint'))
else:raise ValueError(mode)
print(json.dumps(dict(status='PASS',mode=mode,code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),result=result),indent=2))
