"""LSPV-3 GATE324 compact reproducible SAT/Circuit-SAT source transfer.
Reads ORIGINAL clauses; all 2x2 table entries computed, never oracle-provided.
"""
from collections import Counter
F=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
P=(1,2,3,4,6,7,8,9)
def G(t):
 return tuple(tuple((1 if v>0 else -1)*(9*((i+1)%t)+5 if j==0 and v==5 else 9*i+abs(v)) for v in c) for i in range(t) for j,c in enumerate(F))
def check(C,n):
 if not C or n<3 or n%3 or len(C)*3!=4*n:return False
 counts=Counter();seen=set()
 for c in C:
  if len(c)!=3 or any(type(v)!=int or not 1<=abs(v)<=n for v in c):return False
  if len(set(map(abs,c)))!=3 or len(set(v>0 for v in c))!=1:return False
  key=tuple(sorted(c))
  if key in seen:return False
  seen.add(key);counts.update(c)
 return all(counts[v]==counts[-v]==2 for v in range(1,n+1))
def count(C,pins):
 if not C:return 'MALFORMED',None
 n=max(abs(v) for c in C for v in c)
 if not check(C,n):return 'MALFORMED',None
 if any(type(v)!=int or type(b)!=int or not 1<=v<=n or b not in (0,1) for v,b in pins.items()):return 'MALFORMED_PIN',None
 t=n//9
 if n!=9*t or {tuple(sorted(c)) for c in C}!={tuple(sorted(c)) for c in G(t)}:return 'UNRESOLVED',None
 idx={tuple(sorted(c)):c for c in C};source=G(t)
 T=[];checked=0
 for i in range(t):
  a=9*i;b=9*((i+1)%t)
  tab=[[0,0],[0,0]]
  for u in (0,1):
   for v in (0,1):
    for w in range(256):
     checked+=1
     A={a+5:u,b+5:v,**{a+x:(w>>j)&1 for j,x in enumerate(P)}}
     if t==1:A[a+5]=u
     if any(A.get(x)!=z for x,z in pins.items() if x in A):continue
     ok=True
     for j,c in enumerate(source[12*i:12*i+12]):
      orig=idx[tuple(sorted(c))]
      if not any((v if (t==1 and j==0 and abs(l)==5) else A[abs(l)])==int(l>0) for l in orig):
       ok=False;break
     if ok:tab[u][v]+=1
  T.append(tab)
 M=[[1,0],[0,1]]
 for B in T:M=[[sum(M[i][k]*B[k][j] for k in (0,1)) for j in (0,1)] for i in (0,1)]
 return ('SAT' if M[0][0]+M[1][1] else 'UNSAT'),{'models':M[0][0]+M[1][1],'matrices':T,'local_candidates':checked}
def antichain_cut(t):
 C=G(t);L=tuple(9*i+j for i in range(t) for j in (1,2,3,4));S=set(L)
 crossing=[j for j,c in enumerate(C) if any(abs(x) in S for x in c) and any(abs(x) not in S for x in c)]
 closed=[c for c in C if all(abs(x) in S for x in c)]
 masks=set()
 for z in range(1<<len(L)):
  A={v:(z>>j)&1 for j,v in enumerate(L)}
  if any(not any(A[abs(x)]==int(x>0) for x in c) for c in closed):continue
  masks.add(sum(1<<j for j in crossing if any(abs(x) in S and A[abs(x)]==int(x>0) for x in C[j])))
 maximal={m for m in masks if not any(m!=v and m&v==m for v in masks)}
 return len(maximal)
if __name__=='__main__':
 for t,want in ((1,70),(2,4614),(3,312970)):
  kind,data=count(G(t),{})
  assert kind=='SAT' and data['models']==want and data['local_candidates']==1024*t
  print('root G',t,kind,want)
 for t in (1,2,3):
  assert antichain_cut(t)==10**t
  print('bad-cut maximal masks',t,10**t)
 common={3:0,4:0,5:0,**{9+v:(75>>(v-1))&1 for v in range(1,10)}}
 assert count(G(2),common|{1:0})[1]['models']==0
 assert count(G(2),common|{1:1})[1]['models']==2
 print('same-G2 one-bit UNSAT0/SAT2 PASS')
