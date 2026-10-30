#!/usr/bin/env python3
"""Independent minimal finite core for EXTREME-CYCLE-UP240; stdlib only."""
import collections,itertools,json
W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
S='-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14'
def parse(s):return tuple(tuple(map(int,c.split())) for c in s.split(';'))
def truth(c,a):return tuple(int(a[abs(z)-1]==int(z>0)) for z in c)
def models(n,F):
 return sum(all(any(truth(c,[(mask>>i)&1 for i in range(n)])) for c in F)
            for mask in range(1<<n))
def parity_balance(F):
 m=len(F);edge=[];by=collections.defaultdict(list)
 for j,c in enumerate(F):
  for z in c:by[abs(z)].append((j,z<0))
 for v,occ in by.items():
  for (j,s),(k,t) in itertools.combinations(occ,2):
   edge.append((j,k,int(s!=t),v))
 graph=[[] for _ in F]
 for j,k,p,v in edge:
  graph[j].append((k,p,v));graph[k].append((j,p,v))
 labels=[None]*m
 for start in range(m):
  if labels[start]!=None:continue
  labels[start]=0;stack=[start]
  while stack:
   j=stack.pop()
   for k,p,v in graph[j]:
    if labels[k]==None:labels[k]=labels[j]^p;stack.append(k)
    elif labels[k]!=(labels[j]^p):return False,(j+1,k+1,v)
 return True,None
def pair(j,k):
 a={abs(z):int(z>0) for z in j}
 b={abs(z):int(z>0) for z in k}
 same=any(a[v]==b[v] for v in a.keys()&b.keys())
 opposite=any(a[v]!=b[v] for v in a.keys()&b.keys())
 return {'SS':not opposite,'SU':not same,'US':not same,'UU':not opposite}
def up(F,pin):
 a=dict(pin)
 while True:
  changed=False
  for c in F:
   if any(abs(z) in a and a[abs(z)]==int(z>0) for z in c):continue
   remaining=[z for z in c if abs(z) not in a]
   if not remaining:return False
   if len(remaining)==1:
    z=remaining[0];a[abs(z)]=int(z>0);changed=True
  if not changed:return True
def balanced(n,F):
 assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in F)
 z=collections.Counter(z for c in F for z in c)
 return all(z[i]==z[-i]==2 for i in range(1,n+1))
def audit():
 triad=((1,2,4),(1,3,5),(3,-2,6))
 assert all(sum(pair(x,y).values())==2 for x,y in itertools.combinations(triad,2))
 assert parity_balance(triad)[0] is False
 assert models(6,triad)>0
 for n in (3,6):
  F=((1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3)) if n==3 else (
   (1,2,3),(1,4,5),(2,4,6),(3,5,6),
   (-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))
  assert balanced(n,F)
  m=len(F);tested=compatible=0
  for J in itertools.combinations(range(m),m//4+1):
   ass={};ok=True
   for j in J:
    for z in F[j]:
     x=abs(z);s=int(z>0)
     if x in ass and ass[x]!=s:ok=False;break
     ass[x]=s
    if not ok:break
   tested+=1
   if ok:compatible+=1;assert not up(F,ass)
  print(json.dumps({'n':n,'m':m,'S_target_subsets_tested':tested,
   'compatible_S_targets_all_UP_rejected':compatible}))
 for label,txt in [('W1',W1),('S',S)]:
  F=parse(txt);assert balanced(15,F)
  sat=models(15,F)
  assert (sat==0)==(label=='W1')
  print(json.dumps({'source':label,'variables':15,'clauses':len(F),
   'models':sat,'enumerated':32768}))
 # Complement and 0/1/2/3 flip counts.
 F=triad
 for mask in [0,1,3,7,63,62,60]:
  a=[(mask>>i)&1 for i in range(6)]
  b=[1-i for i in a]
  x=[sum(truth(c,a)) for c in F]
  y=[sum(truth(c,b)) for c in F]
  assert all(u+v==3 for u,v in zip(x,y))
  print(json.dumps({'mask':mask,'source_literal_true_counts':x,
   'complement_counts':y,'N0123':[x.count(i) for i in range(4)]}))
 print('STATUS: finite controls verified; theorem uses counting proof in .tex; P versus NP OPEN')
if __name__=='__main__':audit()
