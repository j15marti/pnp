import itertools as it,networkx as nx,json
from p4 import Q,graph,covers,blocks
U=[(3,5,0,0),(2,0,4,2),(1,1,2,2),(0,5,1,3),(1,4,2,4),(5,0,4,5),(3,2,5,0),(0,4,2,2),(5,3,4,1),(4,2,0,0),(4,2,5,1),(0,4,1,4),(5,3,3,5),(2,1,3,3),(3,3,5,3),(2,0,3,5),(4,5,0,1),(1,1,1,4)]
V=[(0,0,5,1),(0,1,0,1),(0,1,1,0),(1,0,0,1),(1,0,1,0),(1,1,0,0),(2,2,3,3),(2,3,2,3),(2,4,3,2),(3,2,2,3),(3,2,3,2),(3,3,2,2),(4,3,5,5),(4,5,4,5),(4,5,5,4),(5,4,4,5),(5,4,1,4),(5,5,4,4)]
def closure(T,guard={}):
 n=len(T)//3; cs=[{j for j,t in enumerate(T) if t[c]==a} for c in range(4) for a in range(n)];p=dict(guard);calls=0
 def pin(j,v):
  if j in p and p[j]!=v:raise ValueError
  p[j]=v
 try:
  while True:
   old=len(p)
   for c in cs:
    ones=[j for j in c if p.get(j)==1];free=[j for j in c if j not in p]
    if len(ones)>1 or not ones and not free:raise ValueError
    if ones:
     for j in free:pin(j,0)
    elif len(free)==1:pin(free[0],1)
   if len(p)>old:continue
   selected=[j for j in p if p[j]];free=[j for j in range(len(T)) if j not in p]
   for a,b in it.combinations(range(4),2):
    L=set(range(n))-{T[j][a] for j in selected};R=set(range(n))-{T[j][b] for j in selected}
    def match(force=None):
     nonlocal calls
     calls+=1; l=set(L);r=set(R)
     if force is not None:l.discard(T[force][a]);r.discard(T[force][b])
     g=nx.Graph();g.add_nodes_from((0,x) for x in l);g.add_nodes_from((1,x) for x in r);g.add_edges_from(((0,T[j][a]),(1,T[j][b])) for j in free if T[j][a] in l and T[j][b] in r)
     return len(nx.algorithms.bipartite.maximum_matching(g,top_nodes={(0,x) for x in l}))==2*len(l)
    if not match():raise ValueError
    for j in free:
     if not match(j):pin(j,0);break
    if len(p)>old:break
   if len(p)==old:return p,calls,False
 except ValueError:return p,calls,True

def quotient(T,p):
 G=graph(T);ok,E=nx.check_planarity(G);assert ok;seen=set();faces=[]
 for u,v in E.edges():
  if (u,v) not in seen:
   f=E.traverse_face(u,v,seen)
   if len(f)==4 and len(set(f))==4:faces.append(f)
 QG=nx.Graph();QG.add_nodes_from(range(len(faces))); owners={}
 for i,f in enumerate(faces):
  for a,b in zip(f,f[1:]+f[:1]):
   e=frozenset((a,b))
   if e in owners:QG.add_edge(i,owners[e])
   owners[e]=i
 cs={v:tuple(sorted(w[1] for w in G[v])) for v in G if v[0]=='e'}; groups=[];covered=set()
 for comp in nx.connected_components(QG):
  els={v for i in comp for v in faces[i] if v[0]=='e'}; vs=sorted({j for v in els for j in cs[v]});first=cs[min(els)];rows=[]
  for j in first:
   d={k:int(k==j) for k in first}
   if any(k in p and p[k]!=v for k,v in d.items()):continue
   d.update({k:v for k,v in p.items() if k in vs}); bad=False
   while True:
    old=len(d)
    for e in sorted(els):
     c=cs[e];ones=sum(d.get(k)==1 for k in c);free=[k for k in c if k not in d]
     if ones>1 or not ones and not free:bad=True;break
     if ones:d.update({k:0 for k in free})
     elif len(free)==1:d[free[0]]=1
    if bad or old==len(d):break
   if not bad:
    assert set(d)==set(vs);rows.append(d)
  # Guard overwriting first seed can duplicate rows; dedup and reject mismatched seeds before propagation
  rows=[dict(x) for x in {tuple(sorted(d.items())) for d in rows}];groups.append(rows);covered|=els
 for e,c in cs.items():
  if e not in covered:groups.append([{k:int(k==j) for k in c} for j in c if all(p.get(k,int(k==j))==int(k==j) for k in c)])
 if any(not r for r in groups):return False,0,0,0,None
 # binary core: state literals, tuple literals; signed ints
 m=len(T);B=[(j+1 if v else -j-1,)*2 for j,v in p.items()];tern=[];nvars=m
 for rows in groups:
  ids=list(range(nvars+1,nvars+len(rows)+1));nvars+=len(rows)
  for a,b in it.combinations(ids,2):B.append((-a,-b))
  for a,row in zip(ids,rows):B.extend((-a,j+1 if v else -j-1) for j,v in row.items())
  if len(ids)<=2:B.append((ids[0],ids[-1]))
  else:tern.append(ids)
 # Fixed-point state deletion and activation of binary demand clauses.
 while True:
  D=nx.DiGraph();D.add_nodes_from([i*s for i in range(1,nvars+1) for s in [-1,1]])
  for a,b in B:D.add_edge(-a,b);D.add_edge(-b,a)
  scc={v:i for i,S in enumerate(nx.strongly_connected_components(D)) for v in S}
  if any(scc[i]==scc[-i] for i in range(1,nvars+1)):return False,len(groups),len(tern),0,None
  reach={a:nx.descendants(D,a)|{a} for a in it.chain.from_iterable(tern)}
  def cons(s):return not any(-a in s for a in s)
  H=nx.Graph();H.add_nodes_from(a for a in reach if cons(reach[a]));H.add_edges_from((a,b) for a,b in it.combinations(H.nodes,2) if not cons(reach[a]|reach[b]))
  remove={a for group in tern for a in group if a not in H or any(not any(b in H and not H.has_edge(a,b) for b in other) for other in tern if other is not group)}
  if not remove:break
  new=[]
  for group in tern:
   live=[a for a in group if a not in remove]
   B.extend((-a,-a) for a in group if a in remove)
   if not live:return False,len(groups),len(tern),0,None
   if len(live)<=2:B.append((live[0],live[-1]))
   else:new.append(live)
  tern=new
 claw=next(((a,b,c,d) for a in H for b,c,d in it.combinations(H[a],3) if not any(H.has_edge(x,y) for x,y in [(b,c),(b,d),(c,d)])),None)
 def rec(i,S):
  if i==len(tern):return S
  for a in tern[i]:
   if a in H and all(not H.has_edge(a,b) for b in S):
    out=rec(i+1,S+[a]);
    if out is not None:return out
  return None
 out=rec(0,[])
 if out is not None:
  for a in out:D.add_edge(-a,a)
  sc={v:i for i,S in enumerate(nx.strongly_connected_components(D)) for v in S};sel=[j for j in range(m) if sc[j+1]<sc[-j-1]]
  assert all(sum(j in sel for j in c)==1 for c in cs.values()) and all((j in sel)==bool(v) for j,v in p.items())
 print("CORE",[list(g) for g in tern],sorted(H.edges()),"claw",claw) if len(T)==18 and not p else None
 return out is not None,len(groups),len(tern),H.number_of_edges(),claw

def neighbor():
 for a,b in it.combinations(range(len(U)),2):
  for c in range(4):
   W=list(U);p,q=list(W[a]),list(W[b]);p[c],q[c]=q[c],p[c];W[a],W[b]=tuple(p),tuple(q)
   if len(set(W))==len(W) and nx.check_planarity(graph(W))[0] and covers(W) is not None:return W
 return None
if __name__=='__main__':
 results=[];W=neighbor();print('neighbor',W,flush=True)
 for name,T in [('Q',Q),('U',U),('V',V)]+([('neighbor',W)] if W else [])+[(f'copies{k}',blocks(k)) for k in [2,4,8]]:
  assert len(set(T))==len(T) and all(sum(t[c]==a for t in T)==3 for c in range(4) for a in range(len(T)//3)) and nx.check_planarity(graph(T))[0]
  p,calls,bad=closure(T);truth=covers(T) is not None
  out=quotient(T,p) if not bad else (False,0,0,0,None);assert truth==out[0]
  row=dict(name=name,tuples=len(T),truth=truth,pins=len(p),matching_calls=calls,groups=out[1],ternary_groups=out[2],conflicts=out[3],claw=out[4],connected=nx.is_connected(graph(T)))
  print(row,flush=True);results.append(row)
 print(json.dumps(results))
