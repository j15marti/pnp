#!/usr/bin/env python3
"""TMR-2/078: finite T5 controls, source-authenticated; stdlib only."""
import itertools,json,hashlib
R=lambda x,y:(y-x)%5 in (1,3)
S=range(5)
REV='tmr2-t5-ugirth078-compact.v1'

def source(n,e):
 e=sorted(set(e));return f'p t5 {n} {len(e)}\n'+''.join(f'v {i}\n' for i in range(n))+''.join(f'a {u} {v}\n' for u,v in e)

def parse(s):
 z=s.strip().splitlines(); h=z[0].split();assert h[:2]==['p','t5'] and len(h)==4
 n,m=map(int,h[2:]);assert len(z)==n+m+1 and n+m<=len(s)
 assert z[1:1+n]==[f'v {i}' for i in range(n)]
 e=[tuple(map(int,t.split()[1:])) for t in z[1+n:]]
 assert e==sorted(set(e)) and all(0<=u<n and 0<=v<n and u!=v for u,v in e)
 assert s==source(n,e)
 return n,e

def count(n,e):
 return sum(all(R(z[u],z[v]) for u,v in e) for z in itertools.product(S,repeat=n))

def pc(n,e):
 full={(a,b) for a in S for b in S}
 P=[[({(a,a) for a in S} if i==j else full.copy()) for j in range(n)] for i in range(n)]
 for u,v in e:
  P[u][v]&={(a,b) for a,b in full if R(a,b)}
  P[v][u]&={(b,a) for a,b in full if R(a,b)}
 rounds=0
 while True:
  rounds+=1;changes=0
  for i in range(n):
   for j in range(n):
    for k in range(n):
     right={a:{b for x,b in P[k][j] if x==a} for a in S}
     ok={(a,b) for a,x in P[i][k] for b in right[x]}
     bad=P[i][j]-ok
     if bad:P[i][j]-=bad;changes+=len(bad)
  if changes==0:break
 return sum(len(x) for row in P for x in row),rounds

def motif(n,e):
 M=[[0]*n for _ in range(n)]
 for u,v in e:M[u][v]=1;M[v][u]=-1
 for u in range(n):
  for v in range(u+1,n):
   seen=set()
   for w in range(n):
    if M[u][w] and M[v][w]:seen.add((M[u][w],M[v][w]))
   if len(seen)==4:return True
 return False

def ac(n,e,root,label):
 D=[set(S) for _ in range(n)];D[root]={label}
 while True:
  change=False
  for u,v in e:
   du={a for a in D[u] if any(R(a,b) for b in D[v])}
   dv={b for b in D[v] if any(R(a,b) for a in D[u])}
   if not du or not dv:return False
   if du!=D[u] or dv!=D[v]:change=True
   D[u],D[v]=du,dv
  if not change:return True

def main():
 no=[]
 for a,b in itertools.product((0,1),repeat=2):
  w=2+2*a+b;no.extend([(0,w) if a else (w,0),(1,w) if b else (w,1)])
 yes=[(u,w) for u in (0,1) for w in range(2,6)]
 no,yes=sorted(no),sorted(yes)
 checks=0
 def ck(b):
  nonlocal checks
  checks+=1
  assert b
 z={}
 for tag,e in [('no',no),('yes',yes)]:
  s=source(6,e);ck(parse(s)==(6,e));z[tag]={'Z':count(6,e),'pc_entries':pc(6,e)[0],'certificate':motif(6,e),'sha256':hashlib.sha256(s.encode()).hexdigest(),'arcs':e}
 ck(z['no']['Z']==0 and z['yes']['Z']==90)
 ck(z['no']['pc_entries']==0 and z['yes']['pc_entries']==400)
 ck(z['no']['certificate'] and not z['yes']['certificate'])
 for perm in itertools.permutations(range(6)):
  ck(motif(6,[(perm[u],perm[v]) for u,v in no]))
  ck(not motif(6,[(perm[u],perm[v]) for u,v in yes]))
 counts={'sat':0,'unsat':0,'unsat_PC_detected':0}
 for mask in range(256):
  arcs=[(u,w) if mask>>q&1 else (w,u) for q,(u,w) in enumerate([(u,w) for u in (0,1) for w in range(2,6)])]
  zz=count(6,arcs);counts['sat' if zz else 'unsat']+=1
  ck(not motif(6,arcs) or zz==0)
  if not zz and pc(6,arcs)[0]==0:counts['unsat_PC_detected']+=1
 ck(counts=={'sat':160,'unsat':96,'unsat_PC_detected':96})
 supports=[]
 for d in range(1,5):
  sizes=set()
  for signs in itertools.product((-1,1),repeat=d):
   X={0}
   for sg in signs:X={(a+sg*t)%5 for a in X for t in (1,3)}
   sizes.add(len(X))
  supports.append(sorted(sizes))
 ck(supports==[[2],[3],[4],[5]])
 c8=[];root_checks=0
 for mask in range(256):
  arcs=sorted((i,(i+1)%8) if mask>>i&1 else ((i+1)%8,i) for i in range(8))
  ck(parse(source(8,arcs))==(8,arcs))
  entries,rounds=pc(8,arcs)
  ck(entries==960)
  c8.append(rounds)
  for root in range(8):
   for col in S:ck(ac(8,arcs,root,col));root_checks+=1
 for mask in range(32):
  dom=[i for i in S if mask>>i&1]
  post=sum(1<<j for j in S if any(R(i,j) for i in dom))
  pre=sum(1<<j for j in S if any(R(j,i) for i in dom))
  ck(0<=post<32 and 0<=pre<32)
 print(json.dumps({'revision':REV,'checks':checks,'failures':0,'base':z,'K24_256_orientations':counts,'signed_path_support':supports,'C8_orientations':256,'C8_full_PC_entries':960,'C8_PC_rounds':sorted(set(c8)),'C8_singleton_AC_checks':root_checks,'status':'COMPUTATIONAL; theorem separately symbolic, external review OPEN','P_vs_NP':'OPEN'},sort_keys=True,indent=2))
if __name__=='__main__':main()
