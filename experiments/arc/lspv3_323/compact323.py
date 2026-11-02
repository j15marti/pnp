#!/usr/bin/env python3
"""GATE323 standalone checker. Truth matrices/OBDDs are OFFLINE, not mandatory SAT work."""
from collections import Counter
import json
F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
   (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
L=(1,2,3,4); R=(6,7,8,9)
def G(t):
 return tuple(tuple((1 if v>0 else -1)*(9*((i+1)%t)+5 if j==0 and v==5 else 9*i+abs(v))
       for v in c) for i in range(t) for j,c in enumerate(F))
def valid(F,n):
 if n%3 or 3*len(F)!=4*n:return False
 d=Counter();seen=set()
 for c in F:
  if len(c)!=3 or len(set(map(abs,c)))!=3 or not(all(v>0 for v in c) or all(v<0 for v in c)):return False
  if any(abs(v)>n or abs(v)<1 for v in c):return False
  if tuple(sorted(c)) in seen:return False
  seen.add(tuple(sorted(c)));d.update(c)
 return all(d[v]==d[-v]==2 for v in range(1,n+1))
def sat(F,z):
 for c in F:
  mask=sum(1<<(abs(v)-1) for v in c)
  if (c[0]>0 and not(z&mask)) or (c[0]<0 and (z&mask)==mask):return False
 return True
def setbits(k,names):
 return sum(((k>>j)&1)<<(v-1) for j,v in enumerate(names))
def rank(rows):
 piv={}
 for row in rows:
  while row:
   b=row.bit_length()-1
   if b in piv:row^=piv[b]
   else:piv[b]=row;break
 return len(piv)
def bdd(F,order):
 n=len(order);y=[]
 for q in range(1<<n):
  z=sum(((q>>(n-j-1))&1)<<(v-1) for j,v in enumerate(order))
  y.append(int(sat(F,z)))
 intern={};nextid=2;cuts={}
 for k in range(n-1,-1,-1):
  temp=[]
  for j in range(0,len(y),2):
   lo,hi=y[j:j+2]
   if lo==hi:u=lo
   else:
    key=(order[k],lo,hi)
    if key not in intern:intern[key]=nextid;nextid+=1
    u=intern[key]
   temp.append(u)
  y=temp;cuts[k]=len(set(y))
 return len(intern),cuts
def pins(F,p):
 n=max(abs(v) for c in F for v in c);free=[v for v in range(1,n+1) if v not in p]
 init=sum(b<<(v-1) for v,b in p.items())
 return sum(sat(F,init|setbits(i,free)) for i in range(1<<len(free)))
def main():
 assert valid(F,9)
 H=G(2);assert valid(H,18)
 K=[sum(int(sat(F,setbits(a,L)|setbits(b,R)))<<b for b in range(16)) for a in range(16)]
 minor_r=(1,3,4,5,6,9,11,12,13);minor_c=(2,3,4,5,7,8,9,10,14)
 minor=[sum(((K[a]>>c)&1)<<j for j,c in enumerate(minor_c)) for a in minor_r]
 assert rank(K)==rank(minor)==9
 left=(1,2,3,4,10,11,12,13);right=tuple(v for v in range(1,19) if v not in left)
 M=[sum(int(sat(H,setbits(a,left)|setbits(b,right)))<<b for b in range(1<<10)) for a in range(1<<8)]
 assert sum(row.bit_count() for row in M)==4614
 assert (rank(M),len(set(M)))==(184,189)
 stats={}
 for name,order in [('left_first',left+right),('right_first',right+left),('block',tuple(range(1,19))),('block_reverse',tuple(range(18,0,-1)))]:
  nodes,cuts=bdd(H,order);stats[name]=(nodes,cuts[8 if name=='left_first' else 10 if name=='right_first' else 9])
 assert stats=={'left_first':(1132,189),'right_first':(1373,346),'block':(204,5),'block_reverse':(229,5)}
 A={1:1,2:0,3:1,4:0,8:0};B={1:1,2:1,3:0,4:0,8:0}
 aa={v+9*i:b for i in range(2) for v,b in A.items()};ba={**B,**{v+9:b for v,b in A.items()}}
 assert (pins(H,aa),pins(H,ba))==(1,0)
 assert (pins(F,{1:0,2:0,8:1,9:1}),pins(F,{8:0,3:0,7:0,6:0,1:1,5:1}))==(2,0)
 assert not valid(F[:-1],9) and not valid(F+(F[0],),9)
 print(json.dumps({'G2_models':4614,'local_K_rank':rank(K),'full_cut_rank':rank(M),'distinct_forward':len(set(M)),
                   'OBDD_nodes_and_checkpoint_states':stats,'same_original_pins':[1,0],
                   'STATUS':'EXACT_RESTRICTED; P_vs_NP_OPEN'},sort_keys=True))
if __name__=='__main__':main()
