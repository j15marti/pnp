#!/usr/bin/env python3
"""Independent finite controls for mod-2 pooled degree-three KT word aliasing.
This is NOT a link isotopy or FLMV simulator.
"""
import itertools, json, hashlib
GRAPHS={
 'K4': [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)],
 'prism': [(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4),(2,5)],
 'cube': [(a,b) for a in range(8) for b in range(a+1,8) if (a^b).bit_count()==1],
 'Petersen': [(i,(i+1)%5) for i in range(5)] + [(i,5+i) for i in range(5)] + [(5+i,5+((i+2)%5)) for i in range(5)]
}
def graph_data(edges):
 e=sorted(tuple(sorted(e)) for e in edges)
 assert len(e)==len(set(e))
 V=sorted(set(v for p in e for v in p)); neighbors={v:[] for v in V}
 for i,(u,v) in enumerate(e,1):neighbors[u].append(i);neighbors[v].append(i)
 assert len(V)>=4 and all(len(ns)==3 for ns in neighbors.values())
 seen={V[0]}; stack=[V[0]]
 while stack:
  x=stack.pop()
  for i in neighbors[x]:
   y=next(v for v in e[i-1] if v!=x)
   if y not in seen:seen.add(y);stack.append(y)
 assert seen==set(V)
 return e,V,neighbors
def build(edges,odd=False,repeat=2):
 e,V,neighbor=graph_data(edges); clauses=[]
 for u in V:
  a,b,c=sorted(neighbor[u])
  for y,z in itertools.product((0,1),repeat=2):
   x=int(bool(odd and u==V[0]))^y^z^1
   row=tuple((var if val==0 else -var) for var,val in ((a,x),(b,y),(c,z)))
   assert len({abs(i) for i in row})==3
   clauses.extend([row]*repeat)
 return e,V,clauses
def encode(n,clauses):
 w=max(1,n.bit_length())
 head=f'N={n};M={len(clauses)};W={w}\n'
 bits=''.join(('1' if lit<0 else '0')+format(abs(lit)-1,f'0{w}b') for C in clauses for lit in C)
 return head+bits
def pooled_mod2(clauses):
 P=set()
 for a,b,c in clauses:
  for word in ((a,b,c),(a,c,b),(b,c,a),(c,b,a)):
   if word in P:P.remove(word)
   else:P.add(word)
 return P
def models(n,clauses):
 cnt=0
 for x in range(1<<n):
  if all(any(((x>>(abs(lit)-1))&1)==int(lit>0) for lit in C) for C in clauses):cnt+=1
 return cnt
def run():
 rows=[]
 for name,edges in GRAPHS.items():
  e,V,_=graph_data(edges);tests=[]
  for odd in (False,True):
   _,_,src=build(edges,odd=odd,repeat=1)
   _,_,doubled=build(edges,odd=odd,repeat=2)
   assert len(src)==4*len(V) and len(doubled)==8*len(V)
   assert doubled==[x for c in src for x in (c,c)]
   assert pooled_mod2(doubled)==set()
   assert all(len(set(map(abs,c)))==3 for c in doubled)
   count=models(len(e),doubled)
   assert count==(0 if odd else 1<<(len(e)-len(V)+1))
   enc=encode(len(e),doubled)
   tests.append({'parity':'odd' if odd else 'even','SAT_count':count,'source_sha256':hashlib.sha256(enc.encode()).hexdigest(),'bytes':len(enc),'pooled_mod2_support':0})
  assert tests[0]['bytes']==tests[1]['bytes']
  assert tests[0]['source_sha256']!=tests[1]['source_sha256']
  rows.append({'graph':name,'H':len(V),'edge_vars':len(e),'clause_occurrences':8*len(V),'kt_components':2*len(e)+8*len(V),'tests':tests})
 _,_,doubled=build(GRAPHS['K4'],True,repeat=2)
 assert len(pooled_mod2(doubled[:-1]))==4
 C=list(doubled);C[0]=(-C[0][0],C[0][1],C[0][2]);assert pooled_mod2(C)
 print(json.dumps({'claim':'canonical KT clause-word cubic coefficients pooled modulo 2 vanish under exact clause doubling','scope':'ordered proper 3-clauses; repeated clauses permitted; not a link isotopy invariant','rows':rows,'hostile_controls':2,'verification':'PASS'},indent=2))
if __name__=='__main__':run()
