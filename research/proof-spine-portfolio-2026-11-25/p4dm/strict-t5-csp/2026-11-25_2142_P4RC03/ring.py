from audit import *
def ports(a,b):
 # Q's cube-radial embedding; two seam edges of distinct colors and state classes on one face.
 _,E=nx.check_planarity(graph(Q));seen=set()
 for u,v in E.edges():
  if (u,v) in seen:continue
  f=E.traverse_face(u,v,seen);es=[]
  for x,y in zip(f,f[1:]+f[:1]):
   if x[0]=='e':x,y=y,x
   es.append((x[1],y[1]))
  for (j,c),(k,d) in I.permutations(es,2):
   if c==a and d==b and min(j,5-j)!=min(k,5-k):return j,k
 raise ValueError((a,b))
def ring(k):
 colors=[i%2 for i in range(k)]
 if k%2:colors[-1]=2
 ps=[ports(colors[(i-1)%k],colors[i]) for i in range(k)]
 T=[tuple(v+2*b for v in t) for b in range(k) for t in Q]
 for i in range(k):T=swap(T,6*i+ps[i][1],6*((i+1)%k)+ps[(i+1)%k][0],colors[i])
 return T,ps,colors
if __name__=='__main__':
 out=[]
 for k in [5,7,9,17,33,65]:
  T,ps,colors=ring(k);assert nx.check_planarity(graph(T))[0] and nx.is_connected(graph(T));assert len(T)==len(set(T))
  # Independently produce covers: choose private state everywhere, or one seam event and private states elsewhere.
  def private(i):return next(j for j in range(3) if j not in {min(x,5-x) for x in ps[i]})
  def selected(events):return {6*i+j for i,a in enumerate(events) for j in (a,5-a)}
  witnesses=[selected([private(i) for i in range(k)])]
  for i in range(k):
   e=[private(j) for j in range(k)];j=(i+1)%k;e[i]=min(ps[i][1],5-ps[i][1]);e[j]=min(ps[j][0],5-ps[j][0]);witnesses.append(selected(e))
  assert all(verify(T,S) for S in witnesses) and set.union(*witnesses)==set(range(len(T))) and not set.intersection(*witnesses)
  p,uf,rs,s=closure(T,{},False);assert p=={};H,C=make_event(T,p,uf,rs);bags,tree,checks=decompose(H);r,t,w=solve(T,weighted=False,cap=0);assert r=='YES';B=max(bags,key=len);assert len(B)==k and nx.is_isomorphic(H.subgraph(B),nx.cycle_graph(k));assert len(H)==2*k
  row=dict(k=k,tuples=len(T),covers_checked=len(witnesses),all_supported=True,cycle_atom=len(B),chordal=nx.is_chordal(H),result=r,**t);out.append(row);print(row,flush=True)
 json.dump(out,open('ring_results.json','w'),indent=2)
