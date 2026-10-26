#!/usr/bin/env python3
"""Compact audit, BACKDOOR-SCC-CERT130; standard library only.
W1 source: PCRETRACT1 Appendix A. Uses exact source identity and independent brute truth.
"""
import itertools,json,collections,random
W='''-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'''
F=[tuple(map(int,x.split())) for x in W.split(';')];B=(2,4,7,14,15);checks=0

def test(v):
 global checks
 checks+=1
 assert v

def sat(f,n):
 return any(all(any(((z>>(abs(a)-1))&1)==(a>0) for a in c) for c in f) for z in range(1<<n))

def residual(f,assignment):
 out=[]
 for i,c in enumerate(f):
  if any(abs(a) in assignment and assignment[abs(a)]==(a>0) for a in c):continue
  out.append((i,tuple(a for a in c if abs(a) not in assignment)))
 return out

def scc_witness(R,n):
 if any(not c for i,c in R):return ('empty',next(i for i,c in R if not c))
 E=[[] for _ in range(2*n)]
 def node(l):return 2*(abs(l)-1)+(l<0)
 for i,c in R:
  test(len(c)<=2)
  a,b=(c[0],c[0]) if len(c)==1 else c
  E[node(-a)].append((node(b),i));E[node(-b)].append((node(a),i))
 def path(p,q):
  todo=collections.deque([p]);prev={p:None}
  while todo:
   x=todo.popleft()
   for y,ci in E[x]:
    if y not in prev:prev[y]=(x,ci);todo.append(y)
  if q not in prev:return None
  out=[];z=q
  while prev[z] is not None:
   x,ci=prev[z];out.append((x,z,ci));z=x
  return list(reversed(out))
 for v in range(n):
  p,q=2*v,2*v+1;a=path(p,q);b=path(q,p)
  if a is not None and b is not None:
   for vpath in (a,b):
    test(all((nxt,ci) in E[src] for src,nxt,ci in vpath))
   return ('cycle',v+1,a,b)
 return None

def serialize(C,n):
 s=f'p cnf {n} {len(C)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in C)
 hdr=s.splitlines()[0].split();test(int(hdr[2])==n and int(hdr[3])==len(C))
 check=[tuple(map(int,row.split()[:-1])) for row in s.splitlines()[1:]]
 test(check==C)
 return len(s.encode())

for v in range(1,16):test(sum(v in c for c in F)==2 and sum(-v in c for c in F)==2)
test(not sat(F,15));test(len(F)==20 and len(set(F))==20)
coverage=[tuple(s) for s in itertools.combinations(range(1,16),5) if all(any(abs(a) in s for a in c) for c in F)]
test(coverage==[B]);test(all(not all(any(abs(a) in s for a in c) for c in F) for s in itertools.combinations(range(1,16),4)))
branches=0;cycle_edges=0;first=[]
for bits in itertools.product((False,True),repeat=5):
 assignment=dict(zip(B,bits));R=residual(F,assignment)
 test(all(len(c)<=2 for _,c in R));serialize([c for _,c in R],15)
 w=scc_witness(R,15);test(w is not None)
 if w[0]=='cycle':cycle_edges+=len(w[2])+len(w[3])
 branches+=1
 if not any(bits):first=[w[0],w[1]]
# Real intermediate child followed by independently serialized 2-CNF grandchild.
L=residual(F,{2:False,4:False});Lsize=serialize([c for _,c in L],15)
R=residual(F,{2:False,4:False,7:False,14:False,15:False});Rsize=serialize([c for _,c in R],15)
# Honest SAT strict exact-(2,2) control: every claimed UNSAT branch set fails.
G=((1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3))
test(sat(G,3));test(any(scc_witness(residual(G,{1:z}),3) is None for z in (False,True)))
# Hostile Horn and same-name/fresh-name alias controls.
test(scc_witness(residual(((1,),(-1,)),{}),2) is not None)
test(scc_witness(residual(((1,2),(-1,2)),{}),2) is None)
def pin(l,a,b):return [(l,p*a,q*b) for p in (1,-1) for q in (1,-1)]
test(not sat(pin(1,2,3)+pin(-1,4,5),5))
test(sat(pin(1,2,3)+pin(-6,4,5),6))
# Odd/even ordinary signed cubic graph Tseitin, including Petersen.
def parity_graph(n,edges,odd):
 rows=[]
 for v in range(n):
  inc=[i+1 for i,e in enumerate(edges) if v in e]
  test(len(inc)==3)
  rhs=int(odd and v==0)
  rows.extend(tuple(a if bit else -a for a,bit in zip(inc,bits)) for bits in itertools.product((0,1),repeat=3) if sum(bits)%2!=rhs)
 return rows
K=list(itertools.combinations(range(4),2));P=([(i,(i+1)%5) for i in range(5)]+[(i,i+5) for i in range(5)]+[(i+5,((i+2)%5)+5) for i in range(5)])
for n,E in ((4,K),(10,P)):
 test(not sat(parity_graph(n,E,True),len(E)))
 test(sat(parity_graph(n,E,False),len(E)))
# Disconnected W1 products: large syntactic backdoor but one W1 copy suffices.
q=4;Q=[tuple((1 if x>0 else -1)*(abs(x)+15*i) for x in c) for i in range(q) for c in F]
test(len(Q)==80 and len({abs(x) for c in Q for x in c})==60)
test(all(c in Q for c in F))
print(json.dumps({'run':'BACKDOOR-SCC-CERT130','checks':checks,'W1_n':15,'W1_m':20,'W1_unique_cover':list(B),'W1_tree_leaves':branches,'W1_total_cycle_edges':cycle_edges,'first_leaf':first,'root_bytes':serialize(F,15),'child_bytes':Lsize,'grandchild_bytes':Rsize,'strict_sat_gadget_rejected':True,'tseitin_K4_Petersen_odd_even':True,'W1x4_backdoor':20,'W1x4_short_core':20},sort_keys=True,indent=2))
