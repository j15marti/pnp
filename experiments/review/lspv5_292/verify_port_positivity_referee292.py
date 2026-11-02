#!/usr/bin/env python3
"""Independent no-producer-import verifier for REFEREE292."""
import argparse,functools,itertools,json,math,resource,time
F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Z=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))
J=F+tuple(tuple((1 if x>0 else -1)*(abs(x)+9) for x in c) for c in Z)
def sat(C,a):return all(any(((a>>(abs(x)-1))&1)==(x>0) for x in c) for c in C)
def stats(C,n,p=None):
 p=p or {};free=[v for v in range(1,n+1) if v not in p];base=sum(b<<(v-1) for v,b in p.items());W=[[0]*3 for c in C];s=0;N3=0
 for q in range(1<<len(free)):
  a=base|sum(((q>>i)&1)<<(v-1) for i,v in enumerate(free));V=[]
  for c in C:V.append([((a>>(abs(x)-1))&1)==(x>0) for x in c])
  if not all(map(any,V)):continue
  s+=1
  for j,v in enumerate(V):
   if sum(v)==3:N3+=1
   if sum(v)>=2:
    for k,b in enumerate(v):W[j][k]+=b
 flat=sum(W,[]);return {'models':s,'sum':sum(flat),'positive':sum(x>0 for x in flat),'N3':N3,'W':W}
def obdd(C,n):
 T=tuple(int(sat(C,z)) for z in range(1<<n));E={}
 for S in range(1<<n):
  P=[i for i in range(n) if S>>i&1]
  for v in range(n):
   if S>>v&1:continue
   R=[i for i in range(n) if not(S>>i&1) and i!=v];Q=set()
   for a in range(1<<len(P)):
    b0=sum(((a>>j)&1)<<u for j,u in enumerate(P));pair=[]
    for bit in (0,1):
     q=0
     for b in range(1<<len(R)):
      z=b0|(bit<<v)|sum(((b>>j)&1)<<u for j,u in enumerate(R));q|=T[z]<<b
     pair.append(q)
    if pair[0]!=pair[1]:Q.add(tuple(pair))
   E[S,v]=len(Q)
 full=(1<<n)-1
 @functools.lru_cache(None)
 def lo(S):return 0 if S==full else min(E[S,v]+lo(S|1<<v) for v in range(n) if not S>>v&1)
 @functools.lru_cache(None)
 def hi(S):return 0 if S==full else max(E[S,v]+hi(S|1<<v) for v in range(n) if not S>>v&1)
 S=nat=0
 for v in range(n):nat+=E[S,v];S|=1<<v
 return lo(0),nat,hi(0)
def circ(C,n):
 g=[];out=[];d={i:0 for i in range(1,n+1)}
 def add(o,x,y):q=n+len(g)+1;g.append((q,o,x,y));d[q]=1+max(d[abs(x)],d[abs(y)]);return q
 for c in C:out.append(add('O',add('O',c[0],c[1]),c[2]))
 while len(out)>1:out=[add('A',out[i],out[i+1]) if i+1<len(out) else out[i] for i in range(0,len(out),2)]
 for z in range(1<<n):
  a={i:(z>>(i-1))&1 for i in range(1,n+1)}
  for q,o,x,y in g:
   X=a[abs(x)] if x>0 else 1-a[abs(x)];Y=a[abs(y)] if y>0 else 1-a[abs(y)];a[q]=int((X or Y) if o=='O' else (X and Y))
  assert a[out[0]]==sat(C,z)
 return len(g),d[out[0]],1<<n
def main():
 st=time.time();ap=argparse.ArgumentParser();ap.add_argument('raw');ap.add_argument('--out',required=True);a=ap.parse_args();o=json.load(open(a.raw));checks=0
 def ck(x,m):
  nonlocal checks;checks+=1
  if not x:raise AssertionError(m)
 f=stats(F,9);z=stats(Z,6);j=stats(J,15)
 ck((f['models'],z['models'],j['models'])==(70,18,1260),'models');ck((f['sum'],z['sum'],j['sum'])==(781,144,24138),'sums')
 ck(f['sum']==12*f['models']-f['N3'] and z['sum']==8*z['models']-z['N3'] and j['sum']==20*j['models']-j['N3'],'identity')
 ck((f['positive'],z['positive'],j['positive'])==(36,24,60),'ports');ck(z['W'][0][0]==6 and j['W'][12][0]==420==70*6,'fixed product port')
 u=stats(F,9,{2:0,4:0,6:0,1:0});s=stats(F,9,{2:0,4:0,6:0,1:1});ju=stats(J,15,{2:0,4:0,6:0,1:0});js=stats(J,15,{2:0,4:0,6:0,1:1})
 ck((u['models'],s['models'],ju['models'],js['models'])==(0,3,0,54),'same original labels');ck((ju['W'][12][0],js['W'][12][0])==(0,18),'same fixed port')
 ck(obdd(F,9)==(52,66,80),'obdd');ck(circ(F,9)==(35,6,512),'f circuit');ck(circ(J,15)==(59,7,32768),'J circuit')
 ck(o['product_F9_Z6']['fixed_Z6_port_W11']==420,'raw port');ck(o['P_vs_NP']=='OPEN','open');ck(o['malformed_rejected']==6,'malformed')
 r={'run':'PORT_POSITIVITY_ACQUISITION_REFEREE292_VERIFY','status':'PASS','checks':checks,'producer_imported':False,'seconds':time.time()-st,'peak_rss_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 json.dump(r,open(a.out,'w'),indent=2,sort_keys=True);print(json.dumps(r))
if __name__=='__main__':main()
