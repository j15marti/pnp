"""C01-09 extracted protected-core and corrected effective frontier routines.
Requires rankcut08.py and its inherited archive dependencies.
Exact executed driver and raw results: C01_09_protected_frontier.tar.gz.
This is an extract, not the full executed driver.
"""
from rankcut08 import *

def coeff(B,v):
 c=0
 while v:
  p=v.bit_length()-1
  if p not in B:return v,c
  q,d=B[p];v^=q;c^=d
 return 0,c

def reps_basis(W,rep):
 B={}
 for v in W:add(B,v,0)
 for i,v in rep.items():assert add(B,v,1<<i) is True
 return B

def core(G,ids,W,detail=False):
 hard=[i for i in ids if len(G[i][1])!=1<<len(G[i][0]) and not (len(G[i][0])==2 and len(G[i][1])==3)]
 eligible=[i for i in ids if len(G[i][0])==2 and len(G[i][1])==3]
 W0=tuple(v for v,_ in basis(list(W)+[v for i in hard for v in G[i][0]]).values());rep={};probes=0
 D={i:(G[i][0][0],G[i][0][1],G[i][0][0]^G[i][0][1]) for i in eligible}
 while True:
  B=reps_basis(W0,rep);prev={i:None for i in eligible if i not in rep};queue=co.deque(prev);end=None
  while queue and end is None:
   i=queue.popleft()
   for v in D[i]:
    probes+=1;u,c=coeff(B,v)
    if u:end=(i,v);break
    while c:
     b=c&-c;j=b.bit_length()-1;c^=b
     if j not in prev:prev[j]=(i,v);queue.append(j)
  if end is None:break
  i,v=end
  while True:
   rep[i]=v
   if prev[i] is None:break
   i,v=prev[i]
 C=hard+list(prev);A=basis([v for i in C for v in G[i][0]]);prot=basis(list(W)+[v for v,_ in A.values()]);r=len(prot)
 for i in eligible:
  if i not in prev:assert add(prot,rep[i]) is True
 assert len(prot)==r+len(eligible)-len(prev)
 E=intersect(A,basis(W))
 return (E,len(C),probes,(C,{i:rep[i] for i in eligible if i not in prev})) if detail else (E,len(C),probes)

def effective_dp(G,o,W,E,cap=6):
 st={'width':max(map(len,E)),'trials':0,'peak':1,'raw_width':max(map(len,W))}
 if st['width']>cap:return 'OPEN',st
 S={():None};layers=[S]
 for j,i in enumerate(o):
  P,Q=G[i];H={}
  for u in S:
   for v in Q:
    B={}
    for x,b in zip(E[j]+P,u+v):
     if add(B,x,b) is None:break
    else:
     for w in it.product((0,1),repeat=len(E[j+1])):
      st['trials']+=1;C=B.copy()
      for x,b in zip(E[j+1],w):
       if add(C,x,b) is None:break
      else:H.setdefault(w,(u,v))
  S=H;layers.append(S);st['peak']=max(st['peak'],len(S))
  if not S:return None,st
 # Never reuse one fixed backpointer: replay against actual full suffix boundary.
 w=();full=();cert=[]
 for j in range(len(o)-1,-1,-1):
  i=o[j];P,Q=G[i];found=False
  for u in layers[j]:
   for v in Q:
    st['trials']+=1;B={}
    for x,b in zip(W[j+1]+E[j]+P,full+u+v):
     if add(B,x,b) is None:break
    else:found=True;break
   if found:break
  assert found
  full=tuple(red(B,x)[1] for x in W[j]);w=u
  cert.extend(Q[v])
 return dict(cert),st
