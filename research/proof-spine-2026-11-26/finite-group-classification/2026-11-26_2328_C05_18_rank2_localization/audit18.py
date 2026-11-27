"""C05-18 independent finite-group controls and native adversary replay.
Requires networkx. No determinant or matching-library dependency in the verifier.
"""
import itertools as it, random, json, collections, hashlib
import networkx as nx

def summ(a,b):return {x^y for x in a for y in b}
def prod(F):
 a={0}
 for s in F:a=summ(a,s)
 return a
def subspace(S):
 a={0}
 for s in S:a|={x^s for x in a}
 return a
def kernels(n,r):
 U=set(range(1<<n)); H={frozenset(U)};out=set(H)
 for _ in range(r):
  H={frozenset(x for x in h if (x&a).bit_count()%2==0) for h in H for a in U};out|=H
 return sorted(out,key=lambda a:-len(a))
def exists(S,t,K):return any(not any(t^x in h for x in S) for h in K)
def local(F,t,K):
 S=prod(F);b=next(iter(S));D=subspace(x^b for x in S)
 if t^b not in D:return True
 bases=[min(s) for s in F];p=0
 for a in bases:p^=a
 t^=p
 for i,s in enumerate(F):
  W=subspace(x^bases[j] for j,g in enumerate(F) if j!=i for x in g)
  A={x^bases[i] for x in s}
  if any(W<=h and all(x^t not in h for x in A) for h in K):return True
 return False
def local_general(F,t,K,r,n):
 b=[min(s) for s in F];a=0
 for v in b:a^=v
 w=t^a
 for k in range(min(len(F),2**r-2)+1):
  for I in it.combinations(range(len(F)),k):
   W=subspace(x^b[i] for i,s in enumerate(F) if i not in I for x in s)
   A=prod([{x^b[i] for x in F[i]} for i in I])
   if any(W<=h and all(x^w not in h for x in A) for h in K):return True
 return False

rng=random.Random(2611262328);stats=collections.Counter()
for n in [2,3,4]:
 K=kernels(n,2);K3=kernels(n,3);U=list(range(1<<n))
 if n==2:
  allS=[{x for x in U if m>>x&1} for m in range(1,1<<len(U))];cases=it.product(allS,repeat=3)
 else:
  cases=([set(rng.sample(U,rng.randint(1,min(7,len(U))))) for _ in range(rng.randint(1,5))] for _ in range(3000))
 for F in cases:
  S=prod(F);t=rng.choice(U)
  a=exists(S,t,K);b=local(F,t,K);assert a==b,(n,F,t,a,b);stats['rank2_checks']+=1;stats['target_absent']+=t not in S
  if n==3 and stats['rank3_checks']<600:
   assert exists(S,t,K3)==local_general(F,t,K3,3,n);stats['rank3_checks']+=1
  if a:stats['rank2_yes']+=1
  if t in S:stats['attained_falsifiers']+=1
for v in [3,4,5]:
 S={1<<i ^1<<j for i in range(v) for j in range(i)};K=kernels(v,2)
 assert exists(S,0,K)==(v<=4);stats['graph_checks']+=1
T={1:(0,0,1),2:(0,0,2),5:(0,1,2),8:(1,0,2),9:(1,1,0),13:(2,2,1),14:(2,2,3),17:(2,3,3),20:(3,2,3),21:(3,3,0)};n=4
G=nx.Graph();G.add_nodes_from((c,z) for c in range(3) for z in range(n))
for i,t in T.items():G.add_edges_from((('t',i),(c,z)) for c,z in enumerate(t))
assert nx.check_planarity(G)[0] and nx.is_connected(G)
assert all(G.degree[(c,z)]>=2 for c in range(3) for z in range(n))
sets=[];P=[(0,1,2),(0,2,1),(1,2,0)]
for p in P:
 S=set();supported=set();count=0
 for C in it.combinations(T,n):
  if all(len({T[i][c] for i in C})==n for c in p[:2]):
   v=0
   for i in C:v^=1<<T[i][p[2]]
   S.add(v);supported.update(C);count+=1
 assert supported==set(T) and 15 not in S
 rank=next(r for r in range(1,5) if exists(S,15,kernels(n,r)))
 sets.append({'projection':p,'responses':sorted(S),'matching_count':count,'min_separator_rank':rank})
assert [s['min_separator_rank'] for s in sets]==[3,2,2]
cols=[sum(1<<(n*c+z) for c,z in enumerate(t)) for t in T.values()]
assert (1<<(3*n))-1 in subspace(cols)
assert not any(all(len({T[i][c] for i in C})==n for c in range(3)) for C in it.combinations(T,n))
print(stats);print(sets)
json.dump(dict(stats=stats,hostile_source=T,hostile_fingerprint=hashlib.sha256(json.dumps(sorted(T.items()),separators=(',',':')).encode()).hexdigest(),native=sets),open('audit18.json','w'),indent=2)
