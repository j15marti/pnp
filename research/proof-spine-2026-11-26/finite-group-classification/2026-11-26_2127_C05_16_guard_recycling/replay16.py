"""Pure Python reproduction of the five acquired guard steps, not the greedy search.
Input: peer_source.json (X01-19 original q,T,guard, fingerprint below).
Run: python replay16.py peer_source.json
"""
import sys, json, hashlib
from collections import defaultdict
from functools import lru_cache
j=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'peer_source.json'))
assert hashlib.sha256(json.dumps({k:j[k] for k in ('q','T','guard')},separators=(',',':')).encode()).hexdigest()=='f2f17606f508eb8644f36634a32291fbdc84a121043eb4b0f44c76b4c5d19aeb'
n=j['q']; T={i:tuple(t) for i,t in enumerate(j['T']) if i not in j['guard']}
def supports(H,a,b,i):
 x,y=H[i][a],H[i][b];adj=[set() for _ in range(n)];match={}
 for t in H.values():
  u,v=t[a],t[b]
  if u!=x and v!=y:adj[u].add(v)
 def aug(u,seen):
  for v in sorted(adj[u]):
   if v in seen:continue
   seen.add(v)
   if v not in match or aug(match[v],seen):match[v]=u;return True
  return False
 return all(aug(u,set()) for u in range(n) if u!=x)
def close(H):
 trace=[]
 while True:
  G={(a,x):[i for i,t in H.items() if t[a]==x] for a in range(3) for x in range(n)}
  empty=[k for k,v in G.items() if not v]
  if empty:return None,trace+[{'empty_owners':empty}]
  drop=set()
  for ids in G.values():
   if len(ids)==1:
    i=ids[0]
    for a,x in enumerate(H[i]):drop.update(set(G[a,x])-{i})
  for i in H:
   if any(not supports(H,a,b,i) for a,b in [(0,1),(0,2),(1,2)]):drop.add(i)
  if not drop:return H,trace
  trace.append({'deleted':sorted(drop)});H={i:t for i,t in H.items() if i not in drop}
def support(H,rows):
 d=[[] for _ in range(n)];target=sum((h.bit_count()%2)<<k for k,h in enumerate(rows));steps=0
 for i,(x,y,z) in H.items():d[x].append((i,z,sum(((h>>y)&1)<<k for k,h in enumerate(rows))))
 R=[0]*(n+1);P=[0]*(n+1)
 for x in reversed(range(n)):
  R[x]=R[x+1];P[x]=P[x+1]
  for i,z,v in d[x]:R[x]|=1<<z;P[x]|=v
 if R[0]!=(1<<n)-1 or target&~P[0]:return 0,set(),0
 def trans(x,u,p):
  nonlocal steps
  rz=R[x]&~R[x+1];rp=P[x]&~P[x+1]
  for i,z,v in d[x]:
   steps+=1
   if u>>z&1:continue
   w=u|1<<z;q=p^v
   if rz&~w or (q^target)&rp:continue
   yield i,(w&R[x+1],q&P[x+1])
 @lru_cache(None)
 def suffix(x,u,p):
  if x==n:return int(u==0 and p==0)
  return sum(suffix(x+1,*s) for i,s in trans(x,u,p))
 count=suffix(0,0,0);live={(0,0)};edges=set()
 if not count:return 0,edges,steps
 for x in range(n):
  new=set()
  for u,p in live:
   for i,s in trans(x,u,p):
    if suffix(x+1,*s):edges.add(i);new.add(s)
  live=new
 return count,edges,steps
T,initial=close(T);assert sorted(T)==j['live_ids'];trail=[];prev=[]
expected=[(4,6492160,[]),(16384,2670592,[99]),(16,1165312,[6]),(1,235520,[9,44,49,50,75,81,95,98,102]),(8,83968,[18,20,51,83,88,89,90,103,111,116,117,119,122,123,124,126])]
for k,(h,c,drop) in enumerate(expected):
 if k==4:
  new=[v for v in prev if v!=16384]
  # Same graph, weaker guard. Equal exact counts certify no new matching.
  a,_,sa=support(T,prev);b,_,sb=support(T,new);assert a==b
  trail.append({'forgot_row':16384,'old_count':a,'new_count':b,'steps':sa+sb});prev=new
 prev.append(h);z,ids,steps=support(T,prev);assert z==c and sorted(set(T)-ids)==drop
 T,trace=close({i:t for i,t in T.items() if i in ids});trail.append({'rows':prev[:],'count':z,'deleted':drop,'frontier_steps':steps,'after_closure':None if T is None else len(T),'closure':trace})
assert T is None
print(json.dumps({'initial':initial,'trail':trail},indent=2))
