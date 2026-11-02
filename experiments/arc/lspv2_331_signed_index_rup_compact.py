#!/usr/bin/env python3
"""LSPV-2 signed-index/local-RUP 331, requires networkx and lspv2_326_compact.py.
The complete separately verified 7-source producer and proofs are in the run ZIP.
"""
from collections import defaultdict
import networkx as nx
from lspv2_326_compact import F9,Y6,valid,compile

def signed_index(F):
 buckets=defaultdict(list);supports=defaultdict(dict)
 for j,c in enumerate(F):
  sign=c[0]>0
  supports[tuple(sorted(abs(x) for x in c))][sign]=j
  for x in c:buckets[abs(x),sign].append(j)
 edges={}
 for ids in buckets.values():
  assert len(ids)==2
  key=tuple(sorted(ids));edges[key]=(edges.get(key,(0,'same'))[0]+1,'same')
 for signs in supports.values():
  if len(signs)==2:edges[tuple(sorted(signs.values()))]=(2,'nae')
 return edges

def gate_clauses(g):
 op,a,b,z=g
 if op=='AND':return [(z,-a,-b),(-z,a),(-z,b)]
 if op=='OR':return [(-z,a,b),(z,-a),(z,-b)]
 if op=='NAND':return [(-z,-a,-b),(z,a),(z,b)]
 assert op=='XOR'
 return [(-a,-b,-z),(a,b,-z),(a,-b,z),(-a,b,z)]

def locally_hinted_rup(F,C,blocks):
 clauses=[];gateids={}
 for g in C:
  first=len(clauses)+1
  clauses.extend(gate_clauses(g))
  gateids[g[3]]=list(range(first,len(clauses)+1))
 clauses.append((C[-1][3],))
 base=len(clauses)
 def hints(target,allowed):
  assignments={abs(x):int(x<0) for x in target};log=[]
  for _ in range(len(allowed)+1):
   progress=False
   for idx in allowed:
    cl=clauses[idx-1]
    if any(abs(x) in assignments and assignments[abs(x)]==int(x>0) for x in cl):continue
    undec=[x for x in cl if abs(x) not in assignments]
    if not undec:return log+[idx]
    if len(undec)==1:
     x=undec[0];assignments[abs(x)]=int(x>0);log.append(idx);progress=True;break
   if not progress:break
  raise AssertionError(('local RUP failed',target))
 groupouts={out for out,_,_ in blocks};byout={g[3]:g for g in C}
 units={C[-1][3]:base};queue=[C[-1][3]];proof=[]
 while queue:
  out=queue.pop(0)
  if out in groupouts:continue
  op,a,b,z=byout[out];assert op=='AND'
  for child in (a,b):
   h=hints([child],[units[z]]+gateids[z])
   proof.append(([child],h))
   clauses.append((child,));units[child]=len(clauses);queue.append(child)
 for j,c in enumerate(F,1):
  root,src,local=next(B for B in blocks if j in B[1])
  allowed=[units[root]]
  for wire in local:allowed.extend(gateids[wire])
  h=hints(c,allowed)
  proof.append((list(c),h));clauses.append(tuple(c))
 assert len(proof)==2*(len(blocks)-1)+len(F)
 return base,len(proof),sum(len(H) for _,H in proof)

def run(F):
 n=max(abs(x) for c in F for x in c);assert valid(F,n)
 edges=signed_index(F);G=nx.Graph();G.add_nodes_from(range(len(F)))
 for (i,j),(weight,kind) in edges.items():G.add_edge(i,j,weight=weight)
 M=sorted(tuple(sorted(e)) for e in nx.max_weight_matching(G,weight='weight'))
 C,root,W,nae=compile(F,n);assert root==C[-1][3]
 assert W==sum(edges[e][0] for e in M)
 off=0;blocks=[];used={v for pair in M for v in pair}
 for i,j in M:
  k=3 if edges[i,j][1]=='nae' or edges[i,j][0]==2 else 4
  chunk=C[off:off+k];off+=k
  blocks.append((chunk[-1][3],(i+1,j+1),[g[3] for g in chunk]))
 for i in range(len(F)):
  if i not in used:
   chunk=C[off:off+2];off+=2
   blocks.append((chunk[-1][3],(i+1,),[g[3] for g in chunk]))
 assert len(C)-off==len(blocks)-1
 initial,lines,antecedents=locally_hinted_rup(F,C,blocks)
 print(dict(n=n,m=len(F),gates=len(C),blocks=len(blocks),
    initial_Tseitin_clauses=initial,bridge_lines=lines,antecedent_hints=antecedents))
if __name__=='__main__':
 run(Y6);run(F9)
