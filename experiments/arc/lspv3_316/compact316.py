#!/usr/bin/env python3
"""GATE316 compact source-authenticated binary parity gate; restricted only."""
from collections import Counter,deque
from itertools import product
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
def valid(F):
 if not F or any(len(c)!=3 or len(set(map(abs,c)))!=3 or not(all(v>0 for v in c) or all(v<0 for v in c)) for c in F):return False
 n=max(abs(v) for c in F for v in c);f=Counter(v for c in F for v in c)
 return 3*len(F)==4*n and len(set(tuple(sorted(c)) for c in F))==len(F) and all(f[i]==f[-i]==2 for i in range(1,n+1))
def source(t):
 F=[];p={}
 for k in range(t):
  F.extend(tuple((1 if v>0 else -1)*(abs(v)+6*k) for v in c) for c in Y)
  p.update({6*k+3:0,6*k+4:1})
 for k in range(t-1):
  i,j=8*k+5,8*(k+1)+6
  a,b=list(F[i]),list(F[j]);a[0],b[2]=b[2],a[0];F[i],F[j]=tuple(a),tuple(b)
 assert valid(F)
 return tuple(F),p
def solve(F,p):
 if not valid(F):return "MALFORMED",0,{}
 n=max(abs(v) for c in F for v in c)
 if any(i not in range(1,n+1) or v not in (0,1) for i,v in p.items()):return "MALFORMED",0,{}
 covered=[];rows=[]
 for j,c in enumerate(F):
  if any(abs(v) in p and p[abs(v)]==int(v>0) for v in c):covered.append(j)
  else:rows.append((j,[v for v in c if abs(v) not in p]))
 if any(not row for j,row in rows):return "UNSAT_EMPTY",0,{}
 free=[i for i in range(1,n+1) if i not in p];f=len(free);u=len(rows);e=2*f-u
 s={v:(sum(v in F[j] for j in covered),sum(-v in F[j] for j in covered)) for v in free}
 eta=sum(min(a,b) for a,b in s.values());I=sum(abs(a-b) for a,b in s.values())
 u1=sum(len(r)==1 for j,r in rows);u3=sum(len(r)==3 for j,r in rows)
 assert 2*(e-eta)==I+u3-u1
 meta={"f":f,"u":u,"e":e,"eta":eta,"u1":u1,"u3":u3}
 if u1 or u3 or e!=eta:return "UNRESOLVED",0,meta
 adj={x:[] for x in free}
 for j,r in rows:
  a,b=map(abs,r);adj[a].append((b,j));adj[b].append((a,j))
 col={};cid={};k=0
 for root in free:
  if root in col:continue
  col[root]=0;cid[root]=k;q=deque([root])
  while q:
   x=q.popleft()
   for y,j in adj[x]:
    if y not in col:col[y]=1-col[x];cid[y]=k;q.append(y)
    elif col[y]==col[x]:return "UNSAT_ODD_CYCLE",0,meta
  k+=1
 assert all(any(({**p,**col})[abs(v)]==int(v>0) for v in c) for c in F)
 return "SAT_PARITY",1<<k,{**meta,"components":k,"colors":col,"component_id":cid}
def count_brute(F,p):
 free=[i for i in range(1,max(abs(v) for c in F for v in c)+1) if i not in p]
 return sum(all(any(({**p,**dict(zip(free,bits))})[abs(v)]==int(v>0) for v in c) for c in F) for bits in product((0,1),repeat=len(free)))
if __name__=="__main__":
 for t in (1,2,3,4,8,16):
  F,p=source(t);s,num,info=solve(F,p)
  assert s=="SAT_PARITY" and num==4**t and info["e"]==info["eta"]==4*t
  if t<=3:assert count_brute(F,p)==num
  print("connected",t,s,"variables",6*t,"model_count",num)
 for name,p,expected in (("SAT",{3:1,4:0,6:0,8:0,9:1},2),("UNSAT",{1:1,3:1,4:0,5:1,8:0},0)):
  s,num,info=solve(F9,p);assert num==expected and count_brute(F9,p)==expected
  print("F9",name,s,"model_count",num)
 print("RESTRICTED; P versus NP OPEN")
