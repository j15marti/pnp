"""Independent original-ID audit of C05-15 on X01-19 source.json (rename to peer_source.json or supply path). Pure Python; no determinant or NetworkX."""
import sys,json,hashlib
from collections import defaultdict
j=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'peer_source.json'))
assert hashlib.sha256(json.dumps({k:j[k] for k in ('q','T','guard')},separators=(',',':')).encode()).hexdigest()=='f2f17606f508eb8644f36634a32291fbdc84a121043eb4b0f44c76b4c5d19aeb'
n=j['q'];T={i:tuple(t) for i,t in enumerate(j['T']) if i not in j['guard']}
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
H=dict(T);removed=[]
while True:
 G={(a,x):[i for i,t in H.items() if t[a]==x] for a in range(3) for x in range(n)}
 assert all(G.values());drop=set()
 for ids in G.values():
  if len(ids)==1:
   i=ids[0]
   for a,x in enumerate(H[i]):drop.update(set(G[a,x])-{i})
 for i in H:
  for a,b in [(0,1),(0,2),(1,2)]:
   if not supports(H,a,b,i):drop.add(i);break
 if not drop:break
 removed.append(sorted(drop));H={i:t for i,t in H.items() if i not in drop}
assert sorted(H)==j['live_ids'] and not j['chosen_ids']
# X,Z projection, omitted Y; matching switch witness at indicated projected vertex.
E={i:(x,z,y) for i,(x,y,z) in H.items()};cl=list(range(n))
for a,b,side,u in [(9,11,1,10),(10,12,1,11),(20,21,0,21)]:
 star=[i for i,t in E.items() if t[side]==u];assert star
 for i in star:
  assert any(E[k][:2]==E[i][:2] and {cl[E[i][2]],cl[E[k][2]]}=={a,b} for k in E if i!=k)
 cl=[a if c==b else c for c in cl]
forms=[{2},{14},{4},{0},{3},{9,11},{13},{6}];expect=[6492160,2670592,1165312,235520,83968,22528,7680,0]
def frontier(forms):
 d=defaultdict(list)
 for x,z,y in E.values():d[x].append((z,sum(1<<i for i,f in enumerate(forms) if y in f)))
 R=[0]*(n+1);P=[0]*(n+1)
 for x in reversed(range(n)):
  R[x]=R[x+1];P[x]=P[x+1]
  for z,v in d[x]:R[x]|=1<<z;P[x]|=v
 target=sum((len(f)%2)<<i for i,f in enumerate(forms));A={(0,0):1};trans=0;peak=1
 if target&~P[0]:return 0,0,1
 for x in range(n):
  B=defaultdict(int);rz=R[x]&~R[x+1];rp=P[x]&~P[x+1]
  for (u,p),c in A.items():
   for z,v in d[x]:
    trans+=1
    if u>>z&1:continue
    w=u|1<<z;q=p^v
    if rz&~w or (q^target)&rp:continue
    B[w&R[x+1],q&P[x+1]]+=c
  A=B;peak=max(peak,len(A))
 return A.get((0,0),0),trans,peak
rows=[]
for k in range(1,len(forms)+1):
 count,tr,peak=frontier(forms[:k]);assert count==expect[k-1];rows.append({'rank':k,'count':count,'transitions':tr,'peak':peak})
print(json.dumps({'removed':removed,'periods':[[9,11],[10,12],[20,21]],'rows':rows},indent=2))
