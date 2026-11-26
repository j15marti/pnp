import itertools as it, json, networkx as nx
S=[(0,0,2),(0,2,0),(0,2,2),(1,0,1),(1,1,0),(1,1,1),(2,0,1),(2,1,0),(2,2,2)]
U=[(0,0,2),(0,1,1),(0,3,0),(1,1,2),(1,1,3),(1,2,3),(2,0,1),(2,2,2),(2,2,3),(3,0,0),(3,3,0),(3,3,1)]
Q=[t for t in it.product(range(2),repeat=3) if t not in [(0,0,0),(1,1,1)]]
def graph(T,n):
 g=nx.Graph();g.add_nodes_from((c,i) for c in range(3) for i in range(n));g.add_edges_from((('t',i),(c,t[c])) for i,t in enumerate(T) for c in range(3));return g
def valid(T,n):
 g=graph(T,n);assert len(set(T))==len(T)==3*n and set(dict(g.degree()).values())=={3} and nx.check_planarity(g)[0];return g
def solutions(T,n):
 return [p for p in it.combinations(range(len(T)),n) if all(len({T[i][c] for i in p})==n for c in range(3))]
def graft(T,n,i):
 a,b,c=T[i];return T[:i]+T[i+1:]+[(n,n,n),(a,n,n),(n,b,n),(n,n,c)],n+1
def closure(T,n):
 live=set(range(len(T))); selected=set(); scans=0;calls=0
 def has_matching(ids,c,d):
  nonlocal calls;calls+=1
  g=nx.Graph();left={(c,T[i][c]) for i in live};right={(d,T[i][d]) for i in live};g.add_nodes_from(left|right);g.add_edges_from(((c,T[i][c]),(d,T[i][d])) for i in ids)
  return len(left)==len(right) and len(nx.algorithms.bipartite.maximum_matching(g,top_nodes=left))==2*len(left)
 remaining={(c,i) for c in range(3) for i in range(n)}
 while True:
  scans+=1;changed=False
  for c,v in sorted(remaining):
   choices=[i for i in live if T[i][c]==v]
   if not choices:return 'UNSAT',scans,calls
   if len(choices)==1:
    i=choices[0];selected.add(i);live={j for j in live if all(T[i][k]!=T[j][k] for k in range(3))};remaining-={(k,T[i][k]) for k in range(3)};changed=True;break
  if changed:continue
  if not remaining:
   assert len(selected)==n and all(len({T[i][c] for i in selected})==n for c in range(3));return 'SAT',scans,calls
  for c,d in it.combinations(range(3),2):
   if not has_matching(live,c,d):return 'UNSAT',scans,calls
   for i in sorted(live):
    ids={j for j in live if j==i or (T[j][c]!=T[i][c] and T[j][d]!=T[i][d])}
    if not has_matching(ids,c,d):live.remove(i);changed=True;break
   if changed:break
  if not changed:return 'UNKNOWN',scans,calls
def mask(G,R,cut):
 triples=sorted(v for v in R if v[0]=='t');out=set()
 for vals in it.product((0,1),repeat=len(triples)+len(cut)):
  a=dict(zip(triples,vals));b=vals[len(triples):];wire=dict(zip(cut,b))
  if any(t in R and a[t]!=wire[t,e] for t,e in cut):continue
  if all(sum(a[w] if w in R else wire[w,v] for w in G[v])==1 for v in R if v[0]!='t'):out.add(b)
 return out
def cuts(T,n):
 G=valid(T,n);E=sorted((a,b) if a[0]=='t' else (b,a) for a,b in G.edges());out=[]
 for cut in it.combinations(E,3):
  H=G.copy();H.remove_edges_from(cut);parts=list(nx.connected_components(H))
  if len(parts)!=2 or min(map(len,parts))<=1:continue
  a,b=[mask(G,R,cut) for R in parts];colors=[e[0] for _,e in cut];assert len(set(colors)) in (1,3)
  allowed={(0,0,0),(1,1,1)} if len(set(colors))==3 else {(1,0,0),(0,1,0),(0,0,1)}
  assert a<=allowed and b<=allowed;assert bool(a&b)==bool(solutions(T,n));out.append([list(cut),sorted(a),sorted(b)])
 return out
for T,n in [(Q,2),(S,3),(U,4)]:valid(T,n)
assert len(solutions(Q,2))==3 and len(set.union(*(set(x) for x in solutions(Q,2))))==6
states=[]
for h,a,b,c in it.product((0,1),repeat=4):
 if h+b+c==h+a+c==h+a+b==1:states.append((h,a,b,c))
assert states==[(1,0,0,0)]
small=[]
for T,n in [(Q,2),(S,3),(U,4)]:
 base=solutions(T,n)
 for i in range(len(T)):
  W,k=graft(T,n,i);valid(W,k);actual=solutions(W,k);expected=[p for p in base if i not in p];assert len(actual)==len(expected)
  decoded={tuple(j if j<i else j+1 for j in p if j<len(T)-1) for p in actual};assert decoded==set(expected)
  small.append([n,i,len(actual)])
scaled=[]
for label,idx in [('SAT',0),('UNSAT',2)]:
 T,n=graft(S,3,idx)
 for target in (4,8,16,32,64):
  while n<target:T,n=graft(T,n,len(T)-1)
  valid(T,n);status,scans,calls=closure(T,n);assert status in (label,'UNKNOWN');scaled.append([label,n,len(T),status,scans,calls])
print(json.dumps({'networkx':nx.__version__,'gadget_states':states,'single_pin_cases':small,'cut_S':cuts(S,3),'cut_U':cuts(U,4),'scaled':scaled},sort_keys=True))
