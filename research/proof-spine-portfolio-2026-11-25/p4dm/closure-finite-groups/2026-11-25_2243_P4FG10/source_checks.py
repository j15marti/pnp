import networkx as nx, itertools as it
Q=[(0,0,0,0),(1,1,1,1),(0,0,1,1),(1,1,0,0),(0,1,0,1),(1,0,1,0)]
U=[(0,2,3,0),(1,3,4,5),(0,2,0,4),(3,5,3,3),(3,5,0,4),(1,1,4,2),(2,1,2,2),(5,3,1,1),(2,1,4,3),(1,0,2,2),(2,0,2,3),(3,0,0,5),(4,4,1,1),(5,3,5,0),(4,4,5,0),(0,5,3,4),(4,2,1,5),(5,4,5,1)]
C=[(6,0,5,1),(0,1,0,1),(0,1,1,0),(1,0,0,1),(1,0,1,0),(1,1,0,0),(2,2,3,3),(2,3,2,3),(2,4,3,2),(3,2,2,3),(3,2,3,2),(3,3,2,13),(4,3,5,5),(4,5,4,5),(4,5,5,4),(5,4,4,5),(5,4,11,4),(5,5,4,4),(0,12,1,7),(6,7,6,7),(6,7,7,6),(7,12,6,7),(7,6,7,6),(7,7,6,6),(8,8,9,9),(8,9,8,9),(8,10,9,8),(9,8,8,9),(9,8,9,8),(9,6,8,8),(10,9,11,11),(10,11,10,11),(10,11,11,10),(11,10,10,11),(11,10,7,10),(11,11,10,10),(12,9,17,2),(12,13,12,13),(12,13,17,12),(13,12,12,13),(13,6,13,12),(13,13,12,12),(14,14,15,15),(14,15,14,15),(14,16,15,14),(15,14,14,15),(15,14,15,14),(15,15,14,14),(16,15,13,17),(16,17,16,17),(16,17,17,16),(17,16,16,17),(17,16,13,16),(17,17,16,16)]
def swap(T,i,j,c):
 T=list(T);a,b=list(T[i]),list(T[j]);a[c],b[c]=b[c],a[c];T[i],T[j]=tuple(a),tuple(b);return T
V=swap(U,0,11,1)
def chain(k,base,out,inc,alternating):
 n=len(base)//3;T=[tuple(v+n*i for v in t) for i in range(k) for t in base]
 for i in range(k-1):T=swap(T,len(base)*i+out,len(base)*(i+1)+inc,i%2 if alternating else 0)
 return T
for name,T in [('Q',Q),('U',U),('V',V),('C',C)]+[(f'C2_{k}',chain(k,C,2,2,True)) for k in [2,4]]+[(f'Q_{k}',chain(k,Q,1,0,False)) for k in [2,4,8,16]]:
 n=len(T)//3;G=nx.Graph();G.add_nodes_from((c,v) for c in range(4) for v in range(n));G.add_edges_from((('t',j),(c,v)) for j,t in enumerate(T) for c,v in enumerate(t));ok,E=nx.check_planarity(G);E.check_structure();assert ok and nx.is_connected(G) and len(set(T))==len(T)==3*n and all(G.degree(('t',j))==4 for j in range(len(T))) and all(G.degree((c,v))==3 for c in range(4) for v in range(n));print(name,len(T),'PASS')
print('NetworkX',nx.__version__)
