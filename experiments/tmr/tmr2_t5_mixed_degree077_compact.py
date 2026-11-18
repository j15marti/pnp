#!/usr/bin/env python3
"""TMR-2/077: exact, deterministic small controls for the mixed two-lift theorem.
No eligible LPS q is claimed tested. Python 3 standard library only.
"""
import itertools, json
R=lambda x,y:(y-x)%5 in (1,3)
def build(n,E):
 E=sorted(set(tuple(sorted(e)) for e in E));a,b=E[0]
 yes=sorted([(u,n+v) for u,v in E]+[(v,n+u) for u,v in E])
 no=sorted([(u+c,v+c) for c in (0,n) for u,v in E if (u,v)!=(a,b)]+[(a,n+a),(b,n+b)])
 return yes,no

def neighbors(n,E):
 N=[set() for _ in range(n)]
 for u,v in E:N[u].add(v);N[v].add(u)
 return N

def pc(n,E):
 U={(a,b) for a in range(5) for b in range(5)}
 e={(a,b) for a,b in U if R(a,b)}
 A=[[{(x,x) for x in range(5)} if i==j else set(U) for j in range(n)] for i in range(n)]
 for u,v in E:A[u][v]&=e;A[v][u]&={(b,a) for a,b in e}
 while True:
  change=False
  for k in range(n):
   for i in range(n):
    for j in range(n):
     new=A[i][j]&{(a,c) for a,b in A[i][k] for bb,c in A[k][j] if b==bb}
     if not new:return False
     if new!=A[i][j]:change=True;A[i][j]=new
  if not change:return True

def rank(M,p):
 M=[[x%p for x in row] for row in M];h=len(M);s=0
 for j in range(h):
  i=next((i for i in range(s,h) if M[i][j]),None)
  if i is None:continue
  M[s],M[i]=M[i],M[s];z=pow(M[s][j],-1,p)
  M[s]=[v*z%p for v in M[s]]
  for i in range(h):
   if i!=s and M[i][j]:
    z=M[i][j];M[i]=[(v-z*w)%p for v,w in zip(M[i],M[s])]
  s+=1
 return s

def run():
 checks=0;out=[]
 def chk(v):
  nonlocal checks
  checks+=1
  assert v
 for name,n,E in [('C7',7,[(i,(i+1)%7) for i in range(7)]),
                  ('C9',9,[(i,(i+1)%9) for i in range(9)]),
                  ('K8',8,list(itertools.combinations(range(8),2)))]:
  yes,no=build(n,E)
  G=neighbors(n,E)
  for label,F in [('YES',yes),('SWITCHED',no)]:
   N=neighbors(2*n,F)
   chk(len(F)==2*len(E))
   chk(all(len(N[i])==len(G[i%n]) for i in range(2*n)))
   chk(all(u<v for u,v in F))
   if label=='YES':chk(all(R(([0]*n+[1]*n)[u],([0]*n+[1]*n)[v]) for u,v in F))
   if name!='K8':chk(pc(2*n,F))
   out.append([name,label,2*n,len(F)])
  if name=='K8':
   a,b=min(E);H=set(no);K=[i for i in range(n) if i!=b]
   chk(all((u,v) in H for u,v in itertools.combinations(K,2)))
   chk(not pc(2*n,no))
  if name=='C7':
   N=neighbors(2*n,yes)
   for cut in (4,6,7,10):
    edges=[(u,v) for u,v in yes if (u<cut)!=(v<cut)]
    match=[]
    while edges:
     u,v=edges.pop(0);match.append((u,v))
     blocked=N[u]|N[v]
     edges=[(a,b) for a,b in edges if a not in blocked and b not in blocked]
    t=len(match);chk(t>=1)
    M=[]
    for row in range(1<<t):
     vals=[]
     for col in range(1<<t):
      color=[0]*n+[1]*n
      for j,(u,v) in enumerate(match):
       x,y=(u,v) if u<cut else (v,u)
       color[x]=((0,3) if x<n else (1,3))[(row>>j)&1]
       color[y]=((0,3) if y<n else (1,3))[(col>>j)&1]
      vals.append(int(all(R(color[a],color[b]) for a,b in yes)))
     M.append(vals)
    for p in (2,3,5,7):chk(rank(M,p)==1<<t)
    out.append(['C7','CUT',cut,t,1<<t])
 return {'revision':'tmr2-mixed077-compact-v1','assertions':checks,'failures':0,
         'LPS_large_executed':False,'cases':out,'P_vs_NP':'OPEN'}
if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
