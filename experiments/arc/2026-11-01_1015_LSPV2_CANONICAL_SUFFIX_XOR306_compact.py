#!/usr/bin/env python3
"""LSPV-2 restricted canonical Y6-suffix child bit accessor, gamma source-index mapping.
Optional U198.txt is supplied in the full reproducibility archive. Host Python
is not an indexed-TM FLMV accounting. Both labels require separate certificates.
"""
import json,sys,hashlib
from collections import Counter
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F9=P+tuple(tuple(-x for x in c) for c in N)
def gamma(n):
 s=bin(n)[2:];return '0'*(len(s)-1)+s
def valid(F,n):
 cnt=Counter(x for c in F for x in c)
 return (len(F)*3==4*n and len(set(tuple(sorted(c)) for c in F))==len(F)
 and all(len(c)==3 and len(set(map(abs,c)))==3 and
       (all(x>0 for x in c) or all(x<0 for x in c)) and
       all(1<=abs(x)<=n for x in c) for c in F)
 and all(cnt[x]==cnt[-x]==2 for x in range(1,n+1)))
def encode(F,n):
 w=n.bit_length()
 return gamma(n)+gamma(len(F))+''.join(
 str(int(c[0]<0))+''.join(format(abs(v),f'0{w}b') for v in c) for c in F)
def source_bit(q,n,m):
 pn=n+6;pm=m+8
 hs=len(gamma(pn))+len(gamma(pm));hc=len(gamma(n))+len(gamma(m))
 if q<hc:return None
 wp=pn.bit_length();wc=n.bit_length()
 j,k=divmod(q-hc,1+3*wc)
 if k==0:return hs+j*(1+3*wp)
 slot,offset=divmod(k-1,wc)
 return hs+j*(1+3*wp)+1+slot*wp+(wp-wc)+offset
def audit(H,n):
 assert valid(H,n)
 suffix=tuple(tuple((abs(x)+n)*(1 if x>0 else -1) for x in c) for c in Y)
 parent=H+suffix;assert valid(parent,n+6)
 source=encode(parent,n+6);child=encode(H,n)
 width=(len(source)+1).bit_length()
 index='0'*width;out='0'*len(child)
 prior=index+out;changes=events=probes=0
 for i,bit in enumerate(child):
  a=source_bit(i,n,len(H))
  if a is None:
   assert bit==(gamma(n)+gamma(len(H)))[i]
  else:
   assert source[a]==bit
   target=format(a,f'0{width}b')
   index=target;events+=width;probes+=1
  out=out[:i]+bit+out[i+1:]
  events+=1
  state=index+out
  changes+=sum(x!=y for x,y in zip(prior,state));prior=state
 assert out==child
 return dict(parent_bits=len(source),child_bits=len(child),index_width=width,
             source_body_reads=probes,physical_write_events=events,
             sum_adjacent_phys_xor=changes,endpoint_phys_xor=state.count('1'),
             P_vs_NP='OPEN')
if __name__=='__main__':
 print(json.dumps({'F9+Y6':audit(F9,9)},indent=2))
 if len(sys.argv)>1:
  arr=json.loads(open(sys.argv[1]).read())
  U=tuple(tuple(c) for c in arr);assert valid(U,198)
  V=[list(c) for c in U]
  V[2][2],V[44][2]=V[44][2],V[2][2]
  V=tuple(tuple(c) for c in V);assert valid(V,198)
  print(json.dumps({'U198+Y6':audit(U,198),'V198+Y6':audit(V,198)},indent=2))
