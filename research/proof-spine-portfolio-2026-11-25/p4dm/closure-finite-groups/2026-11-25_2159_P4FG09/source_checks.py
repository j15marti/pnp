import networkx as nx,itertools as it
Q=[(0,0,0,0),(1,1,1,1),(0,0,1,1),(1,1,0,0),(0,1,0,1),(1,0,1,0)]
U=[(0,2,3,0),(1,3,4,5),(0,2,0,4),(3,5,3,3),(3,5,0,4),(1,1,4,2),(2,1,2,2),(5,3,1,1),(2,1,4,3),(1,0,2,2),(2,0,2,3),(3,0,0,5),(4,4,1,1),(5,3,5,0),(4,4,5,0),(0,5,3,4),(4,2,1,5),(5,4,5,1)]
def swap(T,i,j,c):
 T=list(T);a,b=list(T[i]),list(T[j]);a[c],b[c]=b[c],a[c];T[i],T[j]=tuple(a),tuple(b);return T
def chain(k,out):
 T=[tuple(v+2*i for v in t) for i in range(k) for t in Q]
 for i in range(k-1):T=swap(T,6*i+out,6*(i+1),0)
 return T
def authenticate(T,n):
 G=nx.Graph();G.add_edges_from((('t',j),(c,v)) for j,t in enumerate(T) for c,v in enumerate(t))
 ok,E=nx.check_planarity(G);E.check_structure();assert ok and nx.is_connected(G) and len(set(T))==len(T)==3*n and all(G.degree(('t',j))==4 for j in range(len(T))) and all(G.degree((c,v))==3 for c in range(4) for v in range(n))
def cover(T,n,W):
 assert len(W)==n and all(len({T[j][c] for j in W})==n for c in range(4))
 return W
for name,T in [('U',U),('V',swap(U,0,11,1))]:
 authenticate(T,6)
 print(nx.__version__,name,sum(all(len({T[j][c] for j in w})==6 for c in range(4)) for w in it.combinations(range(18),6)))
for k in [1,2,4,8,16,32,64]:
 T=chain(k,1);authenticate(T,2*k)
 for t in range(3):cover(T,2*k,[6*i+j for i in range(k) for j in [2*t,2*t+1]])
 print('common',k,len(T))
for k in [2,4,8,16,32,64]:
 T=chain(k,3);authenticate(T,2*k)
 words=[[0]*(k+1)]+[[int(j==i) for j in range(k+1)] for i in range(k+1)]
 covers=[cover(T,2*k,[6*i+j for i in range(k) for j in ([0,1] if z[i] else [2,3] if z[i+1] else [4,5])]) for z in words]
 assert set().union(*map(set,covers))==set(range(6*k)) and not set.intersection(*map(set,covers))
 print('path',k,len(T),(k+1)//2,len(covers))
