import networkx as nx
parse=lambda s:[tuple(map(int,x)) for x in s.split()]
Q=parse('0011 0101 0110 1001 1010 1100');U=parse('3500 2042 1122 0513 1424 5045 3250 0422 5341 4200 4251 0414 5335 2133 3353 2035 4501 1114');V=parse('0051 0101 0110 1001 1010 1100 2233 2323 2432 3223 3232 3322 4355 4545 4554 5445 5414 5544');C=parse('0000 1111 0011 1100 0101 1010')
def swap(T,i,j,c):
 T=list(T);a,b=list(T[i]),list(T[j]);a[c],b[c]=b[c],a[c];T[i],T[j]=tuple(a),tuple(b);return T
W=swap(U,1,14,3)
def chain(k,mid):
 T=[tuple(v+6*i for v in t) for i in range(k) for t in (U if mid and i==k//2 else V)]
 for i in range(k-1): T=swap(T,18*i,18*(i+1),i%2)
 return T
def ring(k):
 T=[tuple(x+2*j for x in t) for j in range(k) for t in C]
 for j in range(0,k,2):T=swap(T,6*j+2,6*(j+1)+2,0)
 for j in range(1,k,2):T=swap(T,6*j,6*((j+1)%k),1)
 return T
print(nx.__version__)
for name,T in [('Q',Q),('U',U),('V',V),('W',W)]+[(f'{"U" if mid else "V"}{k}',chain(k,mid)) for k in [2,4,8] for mid in [False,True]]+[(f'R{k}',ring(k)) for k in [4,8,16,32]]:
 n=len(T)//3;G=nx.Graph();G.add_nodes_from(range(4*n+len(T)));G.add_edges_from((4*n+j,c*n+v) for j,t in enumerate(T) for c,v in enumerate(t));ok,E=nx.check_planarity(G);assert ok and nx.is_connected(G) and len(set(T))==len(T) and all(G.degree(i)==(3 if i<4*n else 4) for i in G);E.check_structure();print(name,len(T),'planar connected E3')
