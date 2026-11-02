#!/usr/bin/env python3
"""No-import verifier for REFEREE291 raw JSON."""
import argparse,json,itertools,time,resource
from functools import lru_cache
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
def gt(t):
 o=[]
 for i in range(t):
  for k,c in enumerate(F9):o.append(tuple((1 if z>0 else -1)*((9*((i+1)%t)+5) if k==0 and z==5 else (9*i+abs(z))) for z in c))
 return tuple(o)
def sat(F,z):return all(any(((z>>(abs(x)-1))&1)==(x>0) for x in c) for c in F)
def rank(R):
 p={}
 for x in R:
  while x:
   b=x.bit_length()-1
   if b in p:x^=p[b]
   else:p[b]=x;break
 return len(p)
def table(F,n):return [int(sat(F,z)) for z in range(1<<n)]
def bdd(T,n,order):
 u={};nxt=[2]
 @lru_cache(None)
 def f(k,z):
  if k==n:return T[z]
  v=order[k];a=f(k+1,z);b=f(k+1,z|1<<(v-1))
  if a==b:return a
  q=(v,a,b)
  if q not in u:u[q]=nxt[0];nxt[0]+=1
  return u[q]
 f(0,0);return len(u)
def cut(T,A,B):
 R=[]
 for a in range(1<<len(A)):
  base=sum(((a>>i)&1)<<(v-1) for i,v in enumerate(A));r=0
  for b in range(1<<len(B)):
   z=base|sum(((b>>i)&1)<<(v-1) for i,v in enumerate(B));r|=T[z]<<b
  R.append(r)
 C=[sum(((r>>j)&1)<<i for i,r in enumerate(R)) for j in range(1<<len(B))]
 return rank(R),len(set(R)),len(set(C))
def pins(F,n,p):
 q=[v for v in range(1,n+1) if v not in p];base=sum(x<<(v-1) for v,x in p.items());c=0
 for b in range(1<<len(q)):
  z=base|sum(((b>>i)&1)<<(v-1) for i,v in enumerate(q));c+=sat(F,z)
 return c
def mat(F,i,p):
 b0=9*i+5;b1=9*((i+1)%2)+5;priv=[9*i+j for j in (1,2,3,4,6,7,8,9)];G=F[12*i:12*i+12];W=[[0,0],[0,0]]
 for u,v in itertools.product((0,1),repeat=2):
  a=dict(p)
  if (b0 in a and a[b0]!=u) or (b1 in a and a[b1]!=v):continue
  a[b0]=u;a[b1]=v;free=[x for x in priv if x not in a]
  for z in range(1<<len(free)):
   aa=dict(a);aa.update({x:(z>>k)&1 for k,x in enumerate(free)})
   W[u][v]+=all(any(aa[abs(x)]==(x>0) for x in c) for c in G)
 return W
def su(F):
 o={'SS':0,'SU':0,'US':0,'UU':0}
 for i,j in itertools.combinations(range(len(F)),2):
  for a,b in itertools.product('SU',repeat=2):
   r={};ok=True
   for c,m in ((F[i],a),(F[j],b)):
    for z in c:
     v=int(z>0) if m=='S' else int(z<0)
     if abs(z) in r and r[abs(z)]!=v:ok=False
     r[abs(z)]=v
   o[a+b]+=ok
 return o
def main():
 started=time.time();a=argparse.ArgumentParser();a.add_argument('raw');a.add_argument('--out',required=True);q=a.parse_args();o=json.load(open(q.raw));checks=0
 def ck(x,msg):
  nonlocal checks;checks+=1
  if not x:raise AssertionError(msg)
 ck(o['P_vs_NP']=='OPEN','open');ck(o['f9']['models']==sum(table(F9,9))==70,'f9 models')
 ck(o['f9']['circuit']=={'depth':6,'gates':35,'matches_all':True},'f9 circuit');ck(o['f9']['obdd_all_orders']['best']==52,'best');ck(o['f9']['obdd_all_orders']['natural']==66,'natural');ck(o['f9']['obdd_all_orders']['worst']==80,'worst');ck(o['f9']['SU_modes']==su(F9)=={'SS':37,'SU':49,'US':49,'UU':37},'SU')
 F=gt(2);T=table(F,18);ck(sum(T)==o['g2']['models']==4614,'g2 models')
 A=[1,2,3,4,10,11,12,13];B=[v for v in range(1,19) if v not in A];ck(cut(T,A,B)==(184,189,346),'cut')
 orders={'left_first':A+B,'right_first':B+A,'natural_blocks':list(range(1,19)),'reverse_blocks':list(range(18,0,-1))}
 for k,v in orders.items():ck(bdd(T,18,v)==o['g2']['fixed_order_obdd'][k],k)
 ck(o['g2']['fixed_order_obdd']=={'left_first':1132,'right_first':1373,'natural_blocks':204,'reverse_blocks':229},'bdd exact')
 p={8:1,6:0,1:0,15:0,11:0,13:0};s={**p,6:1};ck(pins(F,18,p)==0,'U');ck(pins(F,18,s)==38,'S')
 ck([mat(F,i,p) for i in range(2)]==[[[0,7],[0,7]],[[3,5],[0,0]]],'Umats');ck([mat(F,i,s) for i in range(2)]==[[[6,6],[4,4]],[[3,5],[0,0]]],'Smats')
 ck([o['g2']['antichain'][f't{i}']['maximal_antichain'] for i in (1,2,3)]==[10,100,1000],'antichain')
 ck(o['g2']['rank_tensor_seed']['rank']==o['g2']['rank_tensor_seed']['minor_rank']==9,'rank9')
 r={'run':'CONNECTED_REPRESENTATION_SEPARATION_REFEREE291_VERIFY','status':'PASS','checks':checks,'producer_imported':False,'seconds':time.time()-started,'peak_rss_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
 json.dump(r,open(q.out,'w'),indent=2,sort_keys=True);print(json.dumps(r))
if __name__=='__main__':main()
